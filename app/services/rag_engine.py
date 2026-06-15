import json
import redis
import logging
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.redis import RedisSaver
from langchain_core.messages import SystemMessage, HumanMessage
from groq import BadRequestError as GroqBadRequestError
from groq import RateLimitError as GroqRateLimitError

from app.core.config import settings
from app.tools import get_tuition_fee, search_knowledge_base, get_admission_path, get_scholarship_info

# Configure Logger
logger = logging.getLogger(__name__)


class PMBRagEngine:
    def __init__(self):
        logger.info("Menginisialisasi Agentic RAG (Llama 3 via Groq)...")

        # Inisialisasi model LLM via Groq
        self.llm = ChatGroq(
            model=settings.llm_model_name,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

        # Daftarkan tools pencarian data
        self.tools = [get_tuition_fee, search_knowledge_base, get_admission_path, get_scholarship_info]

        # System Prompt utama dengan persona asisten Itenas
        self.system_prompt = SystemMessage(
            content="""Kamu adalah Tenice, asisten virtual PMB (Penerimaan Mahasiswa Baru) Institut Teknologi Nasional (Itenas) Bandung.

Kamu adalah kakak tingkat yang helpful, hangat, dan tahu segalanya tentang Itenas. Kamu ngobrol seperti teman yang peduli — bukan mesin yang membaca SOP.

## Cara Berkomunikasi
- Bahasa Indonesia santai tapi sopan. Contoh: "Nah, untuk Sistem Informasi Kak..."
- Sapaan "Kakak" untuk user agar netral gender.
- Jika percakapan sudah berlangsung, langsung nyambung ke topik — jangan ulangi sapaan.
- Boleh pakai kata natural: "nah", "jadi gini Kak", "oh iya", "kalau untuk itu..." dll.
- Jawaban mengalir, bukan daftar kaku — kecuali data memang berbentuk list/tabel.
- Angka uang selalu pakai format: Rp 7.500.000.

## Memahami Pertanyaan dengan Konteks
Kamu memiliki riwayat percakapan. Gunakan itu untuk memahami pertanyaan yang ambigu:
- Singkatan → perluas (IF=Informatika, SI=Sistem Informasi, TI=Teknik Industri, DKV=Desain Komunikasi Visual, PWK=Perencanaan Wilayah dan Kota, dll)
- Pertanyaan lanjutan tanpa subjek → hubungkan ke topik sebelumnya. Contoh: jika sebelumnya membahas biaya Informatika lalu user bertanya "kalau di SI?", maka kamu tahu maksudnya adalah "biaya di Sistem Informasi".
- Referensi implisit → selesaikan dari konteks.

## Menggunakan Tools
Kamu punya 4 tools untuk mencari fakta dari database Itenas:
- `get_tuition_fee(major)` → biaya UKT, SKS, total biaya kuliah per prodi
- `get_admission_path(jalur)` → jalur masuk (PMDK, TKA, UTBK, RPL, Magister, dll) dan jadwal seleksi
- `get_scholarship_info(beasiswa)` → info beasiswa (KIP-K, JFLS, OSC, dll). Gunakan 'umum' untuk daftar lengkap.
- `search_knowledge_base(query)` → info umum kampus: akreditasi, fasilitas, prospek karir, dll.

Panduan penggunaan tools:
- **JANGAN memanggil tool** jika informasi penting dari user belum lengkap (misal: user bertanya biaya kuliah secara umum tanpa menyebutkan nama prodi). Cukup jawab dengan bertanya balik untuk melengkapi informasi tersebut (contoh: "Boleh tahu Kakak tertarik ke prodi apa?").
- **Hanya gunakan tool** saat parameter yang diperlukan sudah jelas disebutkan oleh user atau sudah diketahui dari konteks sebelumnya.
- Pertanyaan faktual tentang Itenas yang informasinya sudah lengkap → selalu gunakan tool yang sesuai sebelum menjawab.
- Sapaan, basa-basi, pertanyaan pendapat/non-faktual → jawab langsung secara ramah tanpa memanggil tool.
- Hasil tools kosong atau tidak relevan → jujur dan arahkan ke pmb.itenas.ac.id.

Selalu rangkai data dari tools ke dalam kalimatmu sendiri — jangan copy-paste mentah."""
        )

        # 4. Initialize Checkpointer (Memory)
        try:
            redis_conn = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                socket_timeout=1
            )
            redis_conn.ping()
            self.memory = RedisSaver(redis_conn)
            logger.info("✅ RedisSaver berhasil diinisialisasi.")
        except Exception as e:
            logger.warning(f"⚠️ Gagal koneksi ke Redis: {e}. Fallback ke MemorySaver.")
            from langgraph.checkpoint.memory import MemorySaver
            self.memory = MemorySaver()

        # 5. Build Agent with Memory-Trimming Prompt Modifier
        logger.info("Membangun Agent State Graph...")

        def messages_modifier(state):
            """
            Kirim ke LLM: System Prompt + 4 pesan Q&A terakhir + giliran saat ini.
            Tool messages & intermediate AI tool-call steps dibuang dari history
            untuk menjaga token tetap minimal.
            """
            messages = state["messages"]

            # Temukan batas antara history dan giliran saat ini
            latest_user_idx = 0
            for i in range(len(messages) - 1, -1, -1):
                if getattr(messages[i], "type", "") == "user":
                    latest_user_idx = i
                    break

            history = messages[:latest_user_idx]
            current_turn = messages[latest_user_idx:]

            # Dari history, hanya simpan: pertanyaan User + jawaban final AI
            # Buang: ToolMessage (hasil retrieval) & AIMessage perantara (tool_calls)
            filtered_history = []
            for msg in history:
                msg_type = getattr(msg, "type", "")
                if msg_type == "human":
                    filtered_history.append(msg)
                elif msg_type == "ai" and msg.content and not getattr(msg, "tool_calls", []):
                    filtered_history.append(msg)

            # Batasi maksimal 4 pesan (= 2 pasang tanya-jawab)
            trimmed_history = filtered_history[-4:]

            return [self.system_prompt] + trimmed_history + current_turn

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=messages_modifier,
            checkpointer=self.memory,
        )

    # ─────────────────────────────────────────────
    # Public Methods
    # ─────────────────────────────────────────────

    def ask(self, query: str, session_id: str = "default_session") -> dict:
        """Synchronous call — returns full answer dict."""
        import time
        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}]: {query}")

        config = {"configurable": {"thread_id": session_id}}

        try:
            response_state = self.agent.invoke(
                {"messages": [("user", query)]}, config=config
            )
            answer = self._strip_function_tags(response_state["messages"][-1].content)
            detailed_sources, retrieval_context = self._extract_sources(response_state["messages"])
        except GroqBadRequestError as e:
            # Groq 400: Model generated mixed text+tool_call in one response.
            # Smart fallback: parse tool call from error and execute manually.
            logger.warning(f"Groq 400 tool_use_failed — smart fallback: {type(e).__name__}")
            answer, detailed_sources, retrieval_context = self._smart_fallback(query, e)
        except GroqRateLimitError as e:
            # Groq 429: Token/request rate limit exceeded.
            logger.warning(f"Groq 429 rate limit: {e}")
            answer = (
                "Maaf Kak, saat ini server Tenice sedang sangat sibuk atau melampaui batas penggunaan "
                "(Sistem sedang beristirahat sebentar). Silakan coba lagi dalam beberapa menit ya, "
                "atau klik tombol **'Chat Baru'**."
            )
            detailed_sources, retrieval_context = [], []

        return {
            "answer": answer,
            "detailed_sources": detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": round(time.time() - start_time, 2),
        }

    async def ask_stream(self, query: str, session_id: str = "default_session"):
        """Async streaming call — yields chunks then final metadata."""
        import time
        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}] (Streaming): {query}")

        config = {"configurable": {"thread_id": session_id}}

        try:
            # Stream token-by-token
            async for msg, metadata in self.agent.astream(
                {"messages": [("user", query)]},
                config=config,
                stream_mode="messages"
            ):
                msg_type = getattr(msg, "type", "")
                if msg.content and msg_type in ("ai", "AIMessageChunk") and not getattr(msg, "tool_calls", []):
                    yield {"type": "chunk", "content": msg.content}

            # After streaming, extract metadata from final state
            state = self.agent.get_state(config)
            all_messages = state.values.get("messages", [])
            detailed_sources, retrieval_context = self._extract_sources(all_messages)

        except GroqBadRequestError as e:
            # Groq 400: Smart fallback—parse tool from error, execute it, answer with data.
            logger.warning(f"Groq 400 tool_use_failed (stream) — smart fallback: {type(e).__name__}")
            fallback_answer, detailed_sources, retrieval_context = self._smart_fallback(query, e)
            # Yield fallback answer word-by-word for consistent streaming UI
            for word in fallback_answer.split(" "):
                yield {"type": "chunk", "content": word + " "}
        except GroqRateLimitError as e:
            # Groq 429: Token/request rate limit exceeded.
            logger.warning(f"Groq 429 rate limit (stream): {e}")
            rate_msg = (
                "Maaf Kak, saat ini server Tenice sedang sangat sibuk atau melampaui batas penggunaan "
                "(Sistem sedang beristirahat sebentar). Silakan coba lagi dalam beberapa menit ya, "
                "atau klik tombol **'Chat Baru'**."
            )
            for word in rate_msg.split(" "):
                yield {"type": "chunk", "content": word + " "}
            detailed_sources, retrieval_context = [], []

        yield {
            "type": "metadata",
            "sources": detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": round(time.time() - start_time, 2),
        }

    # ─────────────────────────────────────────────
    # Private Helpers
    # ─────────────────────────────────────────────

    def _smart_fallback(self, query: str, error: GroqBadRequestError) -> tuple[str, list, list]:
        """
        Smart fallback ketika Groq mengembalikan 400 tool_use_failed.
        Langkah:
          1. Parse 'failed_generation' dari error untuk mengekstrak tool name + args.
          2. Eksekusi tool tersebut secara manual untuk mendapatkan data dari database.
          3. Berikan hasil tool ke LLM untuk dirangkai menjadi jawaban yang natural.
          4. Jika gagal, gunakan pure LLM fallback tanpa database.
        """
        import re, json as _json

        # Step 1: Extract failed_generation from error body
        failed_gen = ""
        try:
            # GroqBadRequestError stores response body as error.body
            body = getattr(error, 'body', None) or {}
            failed_gen = body.get("error", {}).get("failed_generation", "")
        except Exception:
            pass

        # Step 2: Parse tool name and args from <function=tool_name{...}> format
        # Llama 3 uses: <function=tool_name {"key": "val"}> or <function=tool_name{"key": "val"}>
        tool_result_text = None
        matched_tool_name = None
        if failed_gen:
            # Allow zero or more spaces between tool name and args
            pattern = re.search(r'<function=(\w+)\s*({.*?})\s*<?\/?function>', failed_gen, re.DOTALL)
            if not pattern:
                pattern = re.search(r'<function=(\w+)\s*({[^<]*})', failed_gen, re.DOTALL)
            if pattern:
                tool_name = pattern.group(1)
                try:
                    args = _json.loads(pattern.group(2))
                    tool_map = {t.name: t for t in self.tools}
                    if tool_name in tool_map:
                        logger.info(f"Smart fallback: manually calling {tool_name}({args})")
                        tool_result_text = tool_map[tool_name].invoke(args)
                        matched_tool_name = tool_name
                except Exception as te:
                    logger.warning(f"Smart fallback tool execution failed: {te}")

        # Step 3: Call LLM with tool result as injected context
        if tool_result_text:
            try:
                context_prompt = (
                    f"Berikut adalah data dari database Itenas untuk menjawab pertanyaan user:\n"
                    f"{tool_result_text}\n\n"
                    f"Gunakan data di atas untuk menjawab pertanyaan berikut secara natural "
                    f"(jangan tampilkan JSON mentah, rangkai dalam kalimat yang mengalir):"
                )
                response = self.llm.invoke([
                    self.system_prompt,
                    HumanMessage(content=query),
                    HumanMessage(content=context_prompt),
                ])
                answer = self._strip_function_tags(response.content)
                # Parse sources from tool result
                try:
                    parsed = _json.loads(tool_result_text)
                    sources = parsed.get("metadata", [])
                    context_chunks = [c.strip() for c in parsed.get("content", "").split("\n\n") if c.strip()]
                except Exception:
                    sources, context_chunks = [], []
                return answer, sources, context_chunks
            except Exception as llm_err:
                logger.warning(f"Smart fallback LLM with context failed: {llm_err}")

        # Step 4: Pure LLM fallback — no tools, no database
        # Tell the LLM explicitly: answer from knowledge, NO code blocks, NO function calls.
        strict_prompt = (
            "Jawab pertanyaan berikut dari pengetahuanmu secara natural dalam Bahasa Indonesia. "
            "JANGAN tampilkan kode Python, function call, atau blok kode apapun. "
            "Jika tidak tahu data pastinya, sampaikan dengan jujur dan sarankan user mengunjungi pmb.itenas.ac.id."
        )
        try:
            response = self.llm.invoke([
                self.system_prompt,
                HumanMessage(content=query),
                HumanMessage(content=strict_prompt),
            ])
            return self._strip_function_tags(response.content), [], []
        except Exception as final_err:
            logger.error(f"All fallbacks failed: {final_err}")
            return "Maaf Kak, ada gangguan sementara. Silakan coba ulangi pertanyaan dalam beberapa saat.", [], []

    def _strip_function_tags(self, text: str) -> str:
        """Remove any leaked <function=...> tags from LLM output.
        Llama 3 sometimes leaks these into the response content even when
        tools are not being used as formal tool calls.
        """
        import re
        # Remove <function=...>...</function> or <function=...> standalone tags
        text = re.sub(r'<function=\w+[^>]*>.*?</function>', '', text, flags=re.DOTALL)
        text = re.sub(r'<function=\w+[^<]*>', '', text)
        return text.strip()

    def _extract_sources(self, messages: list) -> tuple[list, list]:
        """Parse tool messages to extract source metadata and retrieval context chunks."""
        detailed_sources = []
        retrieval_context = []

        for msg in messages:
            if getattr(msg, "type", "") != "tool":
                continue
            try:
                tool_output = json.loads(msg.content)
                if "metadata" in tool_output:
                    detailed_sources.extend(tool_output["metadata"])
                if "content" in tool_output and tool_output["content"]:
                    chunks = [c.strip() for c in tool_output["content"].split("\n\n") if c.strip()]
                    retrieval_context.extend(chunks)
            except Exception:
                pass

        # Deduplicate sources
        seen = set()
        deduped = []
        for d in detailed_sources:
            key = tuple(sorted(d.items()))
            if key not in seen:
                seen.add(key)
                deduped.append(d)

        return deduped, retrieval_context
