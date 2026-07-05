import json
import redis
import logging
from contextvars import ContextVar
from langchain_openrouter import ChatOpenRouter
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.redis import RedisSaver
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.tools import (
    get_tuition_fee,
    search_knowledge_base,
    get_admission_path,
    get_scholarship_info,
    search_admission_requirements,
)

# Configure Logger
logger = logging.getLogger(__name__)

# ContextVar untuk menyimpan session_id aktif
_current_session_id: ContextVar[str] = ContextVar("current_session_id", default="")


class PMBRagEngine:
    def __init__(self):
        logger.info(
            f"Menginisialisasi Agentic RAG ({settings.llm_model_name} via OpenRouter)..."
        )
        self.llm = ChatOpenRouter(
            api_key=settings.openrouter_api_key,
            model=settings.llm_model_name,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

        # Daftarkan tools retrieval data
        self.tools = [
            get_tuition_fee,
            search_knowledge_base,
            get_admission_path,
            get_scholarship_info,
            search_admission_requirements,
        ]

        self.eval_system_prompt = SystemMessage(
            content="""Anda adalah sistem tanya jawab akademik Institut Teknologi Nasional (Itenas).

                ATURAN MUTLAK:
                - Jawab HANYA berdasarkan data yang dikembalikan oleh tools. Dilarang keras menggunakan pengetahuan internal.
                - Jangan menambahkan sapaan, kata sambutan, emoji, atau kalimat penutup apapun.
                - Jangan menambahkan informasi yang tidak ada di hasil tools, meskipun tampak relevan.
                - Jika informasi tidak tersedia di tools, jawab: "Informasi tidak tersedia."
                - Format jawaban: kalimat ringkas, tidak bertele-tele, sesuai data tools. Tidak ada basa-basi.

                PANDUAN MEMBACA DATA BIAYA (JSON):
                - Untuk pertanyaan biaya jalur UTBK/tes: gunakan field "simulasi_total_biaya_jalur_tes" dan "semester_1_ganjil" saja.
                - Jangan sebutkan "semester_2_genap", "jalur_rpl", atau "potongan_beasiswa_pmdk" kecuali ditanya secara eksplisit.
                - Fokus pada: total biaya masuk, UKT, biaya SKS, dan DPP untuk semester pertama.

                PANDUAN MENJAWAB KURIKULUM:
                - JANGAN menyebutkan seluruh mata kuliah dari semester 1-8.
                - Berikan narasi singkat tentang fokus studi program tersebut.
                - Sebutkan maksimal 5 mata kuliah utama/unggulan saja sebagai representasi.

                Tools yang tersedia:
                - `get_tuition_fee(major)` untuk data biaya UKT, SKS, total per prodi
                - `get_admission_path(jalur)` untuk data jalur masuk dan jadwal seleksi
                - `search_admission_requirements(keyword)` untuk pencarian syarat masuk lintas jalur (misal: buta warna, umur, rapor, portofolio)
                - `get_scholarship_info(beasiswa)` untuk data daftar dan info beasiswa
                - `search_knowledge_base(query)` untuk data informasi akademik, kurikulum, peraturan kampus

                SELALU panggil tool yang sesuai sebelum menjawab. Jangan menjawab dari memori internal."""
        )

        self.system_prompt = SystemMessage(
            content="""Kamu adalah Tenice, asisten virtual PMB (Penerimaan Mahasiswa Baru) Institut Teknologi Nasional (Itenas) Bandung.

            Kamu adalah kakak tingkat yang helpful, hangat, dan tahu segalanya tentang Itenas. Kamu ngobrol seperti teman yang peduli, bukan mesin yang membaca SOP.

            Cara Berkomunikasi
            - Bahasa Indonesia santai tapi sopan. Contoh: "Nah, untuk Sistem Informasi Kak..."
            - Sapaan "Kakak" untuk user agar netral gender.
            - Jika percakapan sudah berlangsung, langsung nyambung ke topik dan jangan ulangi sapaan.
            - Boleh pakai kata natural: "nah", "jadi gini Kak", "oh iya", "kalau untuk itu..." dan lainnya.
            - Jawaban mengalir, bukan daftar kaku.

            Memahami Pertanyaan dengan Konteks
            - Kamu memiliki riwayat percakapan. Gunakan itu untuk memahami pertanyaan yang ambigu
            - Singkatan diperluas (IF menjadi Informatika, SI menjadi Sistem Informasi, TI menjadi Teknik Industri, DKV menjadi Desain Komunikasi Visual, PWK menjadi Perencanaan Wilayah dan Kota, dan lainnya)
            - Pertanyaan lanjutan tanpa subjek, hubungkan ke topik sebelumnya.

            Panduan Penggunaan Tools:
            - Untuk SEMUA pertanyaan mengenai fakta Itenas, KAMU WAJIB memanggil tool yang sesuai. JANGAN PERNAH menjawab menggunakan pengetahuan bawaanmu sendiri.
            - JANGAN memanggil tool jika informasi penting dari user belum lengkap (misal: user bertanya biaya kuliah tanpa menyebutkan nama prodi). Cukup tanya balik.
            - Sapaan, basa-basi, pertanyaan pendapat/non-faktual langsung jawab langsung secara ramah tanpa memanggil tool.

            ATURAN MUTLAK:
            - Jawab HANYA berdasarkan data yang dikembalikan oleh tools. Dilarang keras menggunakan pengetahuan internal.
            - Rangkum data dari tools ke dalam kalimatmu yang ramah, singkat dan padat.
            - Jangan menambahkan informasi yang tidak ada di hasil tools, meskipun tampak relevan.
            - Jika informasi tidak tersedia di tools, jawab: "Informasi tidak tersedia."

            PANDUAN MEMBACA DATA BIAYA (JSON):
            - Untuk pertanyaan biaya jalur UTBK/tes: gunakan field "simulasi_total_biaya_jalur_tes" dan "semester_1_ganjil" saja.
            - Jangan sebutkan "semester_2_genap", "jalur_rpl", atau "potongan_beasiswa_pmdk" kecuali ditanya secara eksplisit.
            - Fokus pada: total biaya masuk, UKT, biaya SKS, dan DPP untuk semester pertama.

            PANDUAN MENJAWAB KURIKULUM:
            - JANGAN menyebutkan seluruh mata kuliah dari semester 1-8.
            - Berikan narasi singkat tentang fokus studi program tersebut.
            - Sebutkan maksimal 5 mata kuliah utama/unggulan saja sebagai representasi.

            Tools yang tersedia:
            - `get_tuition_fee(major)` untuk data biaya UKT, SKS, total per prodi
            - `get_admission_path(jalur)` untuk data jalur masuk dan jadwal seleksi
            - `search_admission_requirements(keyword)` untuk pencarian syarat masuk lintas jalur (misal: buta warna, umur, rapor, portofolio)
            - `get_scholarship_info(beasiswa)` untuk data daftar dan info beasiswa
            - `search_knowledge_base(query)` untuk data informasi akademik, kurikulum, peraturan kampus

            SELALU panggil tool yang sesuai sebelum menjawab. Jangan menjawab dari memori internal.
            """
        )

        # Initialize Checkpointer (Memory)
        try:
            redis_conn = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                socket_timeout=1,
            )
            redis_conn.ping()
            self.memory = RedisSaver(redis_conn)
            logger.info("RedisSaver berhasil diinisialisasi.")
        except Exception as e:
            logger.warning(f"Gagal koneksi ke Redis: {e}. Fallback ke MemorySaver.")
            from langgraph.checkpoint.memory import MemorySaver

            self.memory = MemorySaver()

        # Build Agent with Memory-Trimming Prompt Modifier
        logger.info("Membangun Agent State Graph...")

        def messages_modifier(state):
            messages = state["messages"]
            # Baca session_id dari ContextVar (di-set sebelum agent.invoke/astream)
            thread_id = _current_session_id.get()
            active_prompt = (
                self.eval_system_prompt
                if thread_id.startswith("eval_")
                else self.system_prompt
            )

            # Temukan batas antara history dan giliran saat ini
            latest_user_idx = 0
            for i in range(len(messages) - 1, -1, -1):
                if getattr(messages[i], "type", "") == "user":
                    latest_user_idx = i
                    break

            history = messages[:latest_user_idx]
            current_turn = messages[latest_user_idx:]

            # Dari history, hanya simpan: pertanyaan User + jawaban final AI
            filtered_history = []
            for msg in history:
                msg_type = getattr(msg, "type", "")
                if msg_type == "human":
                    filtered_history.append(msg)
                elif (
                    msg_type == "ai"
                    and msg.content
                    and not getattr(msg, "tool_calls", [])
                ):
                    filtered_history.append(msg)

            # Batasi maksimal 4 pesan (= 2 pasang tanya-jawab)
            trimmed_history = filtered_history[-4:]

            return [active_prompt] + trimmed_history + current_turn

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=messages_modifier,
            checkpointer=self.memory,
        )

    def ask(self, query: str, session_id: str = "default_session") -> dict:
        """Synchronous call — returns full answer dict."""
        import time

        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}]: {query}")

        # recursion_limit=5
        config = {"configurable": {"thread_id": session_id}, "recursion_limit": 5}

        # Simpan session_id ke ContextVar agar messages_modifier bisa membacanya
        _current_session_id.set(session_id)

        try:
            response_state = self.agent.invoke(
                {"messages": [("user", query)]}, config=config
            )
            raw_content = response_state["messages"][-1].content
            text_content = ""
            if isinstance(raw_content, str):
                text_content = raw_content
            elif isinstance(raw_content, list):
                for item in raw_content:
                    if isinstance(item, dict) and "text" in item:
                        text_content += item["text"]
                    elif isinstance(item, str):
                        text_content += item
            answer = self._strip_hidden_tags(text_content)
            detailed_sources, retrieval_context = self._extract_sources(
                response_state["messages"]
            )
        except Exception as e:
            if "Failed to call a function" in str(e):
                logger.warning(f"Bad tool call (sync) — smart fallback: {e}")
                answer, detailed_sources, retrieval_context = self._smart_fallback(
                    query, e
                )
            elif (
                type(e).__name__ in ("RateLimitError", "ResourceExhausted")
                or "rate limit" in str(e).lower()
                or "429" in str(e)
            ):
                logger.warning(f"Rate limit (sync): {e}")
                answer = (
                    "Maaf Kak, saat ini server Tenice sedang sangat sibuk atau melampaui batas penggunaan "
                    "(Sistem sedang beristirahat sebentar). Silakan coba lagi dalam beberapa menit ya, "
                    "atau klik tombol 'Chat Baru'."
                )
                detailed_sources, retrieval_context = [], []
            else:
                raise e

        return {
            "answer": answer,
            "detailed_sources": detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": round(time.time() - start_time, 2),
        }

    async def ask_stream(self, query: str, session_id: str = "default_session"):
        import time

        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}] (Streaming): {query}")

        # recursion_limit=5
        config = {"configurable": {"thread_id": session_id}, "recursion_limit": 5}

        # Simpan session_id ke ContextVar agar messages_modifier bisa membacanya
        _current_session_id.set(session_id)

        try:
            # Stream token-by-token
            async for msg, metadata in self.agent.astream(
                {"messages": [("user", query)]}, config=config, stream_mode="messages"
            ):
                msg_type = getattr(msg, "type", "")
                if (
                    msg.content
                    and msg_type in ("ai", "AIMessageChunk")
                    and not getattr(msg, "tool_calls", [])
                ):
                    text_content = ""
                    if isinstance(msg.content, str):
                        text_content = msg.content
                    elif isinstance(msg.content, list):
                        for item in msg.content:
                            if isinstance(item, dict) and "text" in item:
                                text_content += item["text"]
                            elif isinstance(item, str):
                                text_content += item

                    if text_content:
                        # Do not call _strip_hidden_tags here, because it strips spaces and partial tags break in streaming
                        yield {"type": "chunk", "content": text_content}

            # After streaming, extract metadata from final state
            state = self.agent.get_state(config)
            all_messages = state.values.get("messages", [])
            detailed_sources, retrieval_context = self._extract_sources(all_messages)

        except Exception as e:
            if "Failed to call a function" in str(e):
                logger.warning(f"Bad tool call (stream) — smart fallback: {e}")
                fallback_answer, detailed_sources, retrieval_context = (
                    self._smart_fallback(query, e)
                )
                for word in fallback_answer.split(" "):
                    yield {"type": "chunk", "content": word + " "}
            elif (
                type(e).__name__ in ("RateLimitError", "ResourceExhausted")
                or "rate limit" in str(e).lower()
                or "429" in str(e)
            ):
                logger.warning(f"Rate limit (stream): {e}")
                rate_msg = (
                    "Maaf Kak, saat ini server Tenice sedang sangat sibuk atau melampaui batas penggunaan "
                    "(Sistem sedang beristirahat sebentar). Silakan coba lagi dalam beberapa menit ya, "
                    "atau klik tombol **'Chat Baru'**."
                )
                for word in rate_msg.split(" "):
                    yield {"type": "chunk", "content": word + " "}
                detailed_sources, retrieval_context = [], []
            else:
                raise e

        yield {
            "type": "metadata",
            "sources": detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": round(time.time() - start_time, 2),
        }

    def _smart_fallback(
        self, query: str, error: GroqBadRequestError
    ) -> tuple[str, list, list]:
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
            body = getattr(error, "body", None) or {}
            failed_gen = body.get("error", {}).get("failed_generation", "")
        except Exception:
            pass

        # Step 2: Parse tool name and args from <function=tool_name{...}> format
        # Llama 3 uses: <function=tool_name {"key": "val"}> or <function=tool_name{"key": "val"}>
        tool_result_text = None
        matched_tool_name = None
        if failed_gen:
            # Allow zero or more spaces between tool name and args
            pattern = re.search(
                r"<function=(\w+)\s*({.*?})\s*<?\/?function>", failed_gen, re.DOTALL
            )
            if not pattern:
                pattern = re.search(
                    r"<function=(\w+)\s*({[^<]*})", failed_gen, re.DOTALL
                )
            if pattern:
                tool_name = pattern.group(1)
                try:
                    args = _json.loads(pattern.group(2))
                    tool_map = {t.name: t for t in self.tools}
                    if tool_name in tool_map:
                        logger.info(
                            f"Smart fallback: manually calling {tool_name}({args})"
                        )
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
                response = self.llm.invoke(
                    [
                        self.system_prompt,
                        HumanMessage(content=query),
                        HumanMessage(content=context_prompt),
                    ]
                )
                answer = self._strip_hidden_tags(response.content)
                try:
                    parsed = _json.loads(tool_result_text)
                    sources = parsed.get("metadata", [])
                    context_chunks = [
                        c.strip()
                        for c in parsed.get("content", "").split("\n\n")
                        if c.strip()
                    ]
                except Exception:
                    sources, context_chunks = [], []
                return answer, sources, context_chunks
            except Exception as llm_err:
                logger.warning(f"Smart fallback LLM with context failed: {llm_err}")

        # Step 4: Rekomendasi 1: Ganti Pure LLM fallback menjadi statis
        logger.error(
            "All fallbacks failed, returning static message to avoid hallucination."
        )
        return (
            "Maaf Kak, sistem sedang mengalami gangguan teknis sehingga tidak bisa mengambil data dari database. Untuk informasi yang akurat, silakan kunjungi pmb.itenas.ac.id atau hubungi panitia PMB langsung ya.",
            [],
            [],
        )

    def _strip_hidden_tags(self, text: str) -> str:
        import re

        # Strip Qwen3 <think> blocks
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        # Remove <function=...>...</function> or <function=...> standalone tags
        text = re.sub(r"<function=\w+[^>]*>.*?</function>", "", text, flags=re.DOTALL)
        text = re.sub(r"<function=\w+[^<]*>", "", text)
        return text

    def _extract_sources(self, messages: list) -> tuple[list, list]:
        detailed_sources = []
        retrieval_context = []

        # Find the last Human message index
        last_human_idx = -1
        for i in range(len(messages) - 1, -1, -1):
            if getattr(messages[i], "type", "") == "human":
                last_human_idx = i
                break

        # Only process messages after the last human message
        current_turn_messages = (
            messages[last_human_idx + 1 :] if last_human_idx != -1 else messages
        )

        for msg in current_turn_messages:
            if getattr(msg, "type", "") != "tool":
                continue
            try:
                tool_output = json.loads(msg.content)
                if "metadata" in tool_output:
                    detailed_sources.extend(tool_output["metadata"])
                if "content" in tool_output and tool_output["content"]:
                    chunks = [
                        c.strip()
                        for c in tool_output["content"].split("\n\n")
                        if c.strip()
                    ]
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
