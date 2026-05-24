import json
import redis
import logging
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.redis import RedisSaver
from langchain_core.messages import SystemMessage

from app.core.config import settings
from app.tools import get_tuition_fee, search_knowledge_base, get_admission_path, get_scholarship_info

# Configure Logger
logger = logging.getLogger(__name__)

# === DEFINE THE ENGINE ===


class PMBRagEngine:
    def __init__(self):
        logger.info("Menginisialisasi Agentic RAG (Llama 3 via Groq)...")

        # 1. Initialize LLM
        self.llm = ChatGroq(
            model=settings.llm_model_name,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

        # 2. Register the Tools we created above
        self.tools = [get_tuition_fee, search_knowledge_base, get_admission_path, get_scholarship_info]

        # 3. Create instruction block (giving direction & specify format)
        system_prompt = SystemMessage(
            content="""Anda adalah Asisten Virtual Cerdas untuk Penerimaan Mahasiswa Baru (PMB) Institut Teknologi Nasional (Itenas) Bandung yang bernama 'Tenice'.
                # PANDUAN KARAKTER (PERSONA):
                1. Anda sangat ramah, suportif, antusias, dan senatural manusia layaknya seorang kakak tingkat yang sedang membantu adik-adik calon mahasiswa.
                2. Gunakan sapaan 'Kakak' untuk menyapa pengguna agar netral secara gender.
                3. JANGAN mengulang-ulang sapaan pembuka (seperti "Halo Kak!") di setiap balasan jika percakapan sudah berlangsung. Langsung saja to the point menjawab pertanyaannya dengan ramah.
                4. JANGAN pernah terdengar seperti robot AI yang sedang membaca buku petunjuk. Gunakan bahasa Indonesia kasual yang profesional dan luwes (gabungan bahasa formal dan santai yang enak dibaca).

                # ATURAN MENGGUNAKAN TOOLS & MENJAWAB:
                - Anda HANYA boleh memberikan fakta berdasarkan informasi yang didapat dari memanggil alat (tools). JANGAN pernah menebak-nebak atau mengarang fakta (berhalusinasi) mengenai kampus.
                - Jika user BERTANYA TENTANG BIAYA (UKT, uang kuliah, pendaftaran, dll), Anda WAJIB memanggil tool 'get_tuition_fee'.
                - Jika user BERTANYA TENTANG JALUR PENDAFTARAN ATAU JADWAL SELEKSI (PMDK, ODT, TKA, UTBK, RPL, Magister dll), Anda WAJIB memanggil tool 'get_admission_path'.
                - Jika user BERTANYA TENTANG BEASISWA (Daftar beasiswa, Syarat, KIP-K, JFLS, OSC dll), Anda WAJIB memanggil tool 'get_scholarship_info' (Gunakan argumen 'umum' jika ditanya daftarnya).
                - Jika user BERTANYA TENTANG INFORMASI UMUM (aturan kampus, fasilitas, prospek karir prodi, akreditasi), Anda WAJIB memanggil tool 'search_knowledge_base'.
                - Output alat (tool) sekarang berbentuk JSON yang mengandung ["content"] dan ["metadata"].
                - Rangkai ulang KONTEN (content) tersebut ke dalam kalimat Anda sendiri yang sangat luwes dan mengalir. JANGAN sekadar 'copy-paste' mentah-mentah dari data.
                - Pastikan semua angka nominal (terutama uang) diformat rapi dengan titik ribuan (contoh: Rp 7.500.000).
                - Jika alat / dokumen tidak mengandung informasi yang ditanyakan (dokumen kosong atau error), Anda harus jujur dan dengan sopan mengatakan: "Maaf Ka, sayangnya informasi mengenai [topik] belum ada di catatan Tenice saat ini. Kakak bisa coba tanyakan hal lain atau mengecek langsung website resmi pmb.itenas.ac.id yaa 🙏".

                # HAL LAINNYA:
                - Jika user hanya menyapa santai (seperti "Halo", "Hai", "Pagi"), Anda TIDAK PERLU memanggil tool apa pun. Cukup balas sapaannya dengan hangat dan tanyakan: "Halo! Tenice di sini, ada yang bisa dibantu terkait info PMB Itenas?".
                """
        )

        # 4. Initialize Checkpointer (Memory)
        try:
            redis_conn = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                socket_timeout=1
            )
            # PING to ensure connection is valid
            redis_conn.ping()
            self.memory = RedisSaver(redis_conn)
            logger.info("✅ RedisSaver berhasil diinisialisasi untuk memori percakapan.")
        except Exception as e:
            logger.warning(f"⚠️ Gagal koneksi ke Redis untuk Checkpointer: {e}. Fallback ke MemorySaver.")
            from langgraph.checkpoint.memory import MemorySaver
            self.memory = MemorySaver()

        # 5. Create the LangGraph Agent Core
        logger.info("Membangun Agent State Graph...")
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=system_prompt,
            checkpointer=self.memory,
        )

    GREETING_WORDS = {
        "halo",
        "hai",
        "hi",
        "hey",
        "pagi",
        "siang",
        "sore",
        "malam",
        "hola",
        "hello",
        "assalamualaikum",
        "selamat",
    }

    def _is_greeting(self, query: str) -> bool:
        """Cek apakah query hanya sapaan singkat yang tidak perlu di-rewrite."""
        words = set(query.lower().strip().rstrip("!?.").split())
        # Jika seluruh kata dalam query adalah sapaan, maka ini greeting
        return len(words) <= 3 and bool(words & self.GREETING_WORDS)

    def _rewrite_query(self, query: str) -> str:
        if self._is_greeting(query):
            return query  

        rewrite_prompt = f"""Tulis ulang pertanyaan berikut agar lebih jelas, lengkap, dan optimal untuk pencarian di database informasi kampus.

        Aturan:
        - Jika ada kata 'Itenas' atau 'ITENAS', pastikan konteksnya selalu mengarah ke 'Institut Teknologi Nasional (Itenas) Bandung'.
        - Perluas singkatan (IF→Informatika, SI→Sistem Informasi, TI→Teknik Industri, DKV→Desain Komunikasi Visual, PWK→Perencanaan Wilayah dan Kota, dll)
        - Tambahkan konteks yang implisit (misal: "biaya" → "rincian biaya UKT dan SKS")
        - Pertahankan bahasa Indonesia
        - HANYA kembalikan query yang sudah ditulis ulang, TANPA penjelasan tambahan
        - Jika query sudah cukup jelas, kembalikan apa adanya tanpa perubahan

        Pertanyaan asli: "{query}"
        Pertanyaan yang ditulis ulang:"""

        try:
            response = self.llm.invoke(rewrite_prompt)
            rewritten = response.content.strip().strip('"')
            if len(rewritten) < 5:
                return query
            logger.info(f'Query Rewrite: "{query}" → "{rewritten}"')
            return rewritten
        except Exception as e:
            logger.warning(f"Query rewrite gagal (menggunakan query asli): {e}")
            return query

    def ask(self, query: str, session_id: str = "default_session") -> dict:
        import time

        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}]: {query}")

        # Step 1-2: Query Rewriting (Agentic RAG)
        rewritten_query = self._rewrite_query(query)

        # Define the config for tracking threads (chat history)
        config = {"configurable": {"thread_id": session_id}}

        # Prompt Repetition
        repeated_query_prompt = f"Tolong jawab pertanyaan berikut: {rewritten_query}\n\n(Sekali lagi, ingat kembali pertanyaan utamanya: '{rewritten_query}')"

        # The agent dynamically decides which tools to run, runs them, and generates final reply
        response_state = self.agent.invoke(
            {"messages": [("user", repeated_query_prompt)]}, config=config
        )

        # The final answer is the last AI message in the state
        answer = response_state["messages"][-1].content

        # Extract traces (what tools were called) for logging and metadata extraction
        sources_used = []
        detailed_sources = []
        retrieval_context = []  # Teks chunk asli untuk DeepEval

        for msg in response_state["messages"]:
            if msg.type == "tool":
                sources_used.append(msg.name)
                # Try parsing the metadata from our new JSON tool outputs
                try:
                    tool_output = json.loads(msg.content)

                    # Ekstrak metadata sumber dokumen
                    if "metadata" in tool_output:
                        detailed_sources.extend(tool_output["metadata"])

                    # Ekstrak teks chunk asli (content) untuk DeepEval retrieval_context
                    if "content" in tool_output and tool_output["content"]:
                        # Pisahkan per paragraf jika ada beberapa chunk
                        raw_content = tool_output["content"]
                        chunks = [
                            c.strip() for c in raw_content.split("\n\n") if c.strip()
                        ]
                        retrieval_context.extend(chunks)

                except Exception:
                    pass

        source_str = "Agent (General Knowledge)"
        if sources_used:
            # deduplicate string names
            sources_used = list(set(sources_used))
            source_str = f"Agent Tools: {', '.join(sources_used)}"

        # Deduplicate the parsed metadata dicts (by document name and row/page)
        seen = set()
        deduped_detailed_sources = []
        for d in detailed_sources:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                deduped_detailed_sources.append(d)

        # 5. Build Result Dictionary
        result = {
            "answer": answer,
            "detailed_sources": deduped_detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": round(time.time() - start_time, 2),
        }
        return result

    async def ask_stream(self, query: str, session_id: str = "default_session"):
        import time
        start_time = time.time()
        logger.info(f"\nPertanyaan User [{session_id}] (Streaming): {query}")

        # Step 1-2: Query Rewriting
        rewritten_query = self._rewrite_query(query)

        # Define the config for tracking threads (chat history)
        config = {"configurable": {"thread_id": session_id}}

        # Prompt Repetition
        repeated_query_prompt = f"Tolong jawab pertanyaan berikut: {rewritten_query}\n\n(Sekali lagi, ingat kembali pertanyaan utamanya: '{rewritten_query}')"

        # 1. Stream the tokens (AI message chunks)
        async for msg, metadata in self.agent.astream(
            {"messages": [("user", repeated_query_prompt)]}, 
            config=config, 
            stream_mode="messages"
        ):
            if msg.content and getattr(msg, "type", "") == "ai" and not msg.tool_calls:
                yield {"type": "chunk", "content": msg.content}
                
        # 2. Get the final state to extract metadata
        state = self.agent.get_state(config)
        messages = state.values.get("messages", [])
        
        sources_used = []
        detailed_sources = []
        retrieval_context = []

        import json
        for msg in messages:
            if msg.type == "tool":
                sources_used.append(msg.name)
                try:
                    tool_output = json.loads(msg.content)
                    if "metadata" in tool_output:
                        detailed_sources.extend(tool_output["metadata"])
                    if "content" in tool_output and tool_output["content"]:
                        raw_content = tool_output["content"]
                        chunks = [c.strip() for c in raw_content.split("\n\n") if c.strip()]
                        retrieval_context.extend(chunks)
                except Exception:
                    pass

        # Deduplicate sources
        seen = set()
        deduped_detailed_sources = []
        for d in detailed_sources:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                deduped_detailed_sources.append(d)

        latency = round(time.time() - start_time, 2)
        
        # 3. Yield the final metadata chunk
        yield {
            "type": "metadata",
            "sources": deduped_detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": latency
        }

        processing_time = round(time.time() - start_time, 2)

        return {
            "query": query,
            "rewritten_query": rewritten_query,
            "answer": answer,
            "source": source_str,
            "detailed_sources": deduped_detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": processing_time,
        }
