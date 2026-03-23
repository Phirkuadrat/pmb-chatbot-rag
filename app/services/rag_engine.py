import json
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

from app.core.config import settings
from app.tools import get_tuition_fee, search_knowledge_base


# === DEFINE THE ENGINE ===

class PMBRagEngine:
    def __init__(self):
        print("🚀 Menginisialisasi Agentic RAG (Llama 3 via Groq)...")
        
        # 1. Initialize LLM
        self.llm = ChatGroq(
            model=settings.llm_model_name,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens
        )
        
        # 2. Register the Tools we created above
        self.tools = [get_tuition_fee, search_knowledge_base]

        # 3. Create instruction block (System Prompt)
        system_prompt = SystemMessage(content="""Anda adalah Asisten Virtual Cerdas untuk Penerimaan Mahasiswa Baru (PMB) Institut Teknologi Nasional (Itenas) Bandung yang bernama 'Tenice'.

# PANDUAN KARAKTER (PERSONA):
1. Anda sangat ramah, suportif, antusias, dan senatural manusia layaknya seorang kakak tingkat yang sedang membantu adik-adik calon mahasiswa.
2. Gunakan sapaan 'Kakak' untuk menyapa pengguna agar netral secara gender.
3. JANGAN mengulang-ulang sapaan pembuka (seperti "Halo Kak!") di setiap balasan jika percakapan sudah berlangsung. Langsung saja to the point menjawab pertanyaannya dengan ramah.
4. JANGAN pernah terdengar seperti robot AI yang sedang membaca buku petunjuk. Gunakan bahasa Indonesia kasual yang profesional dan luwes (gabungan bahasa formal dan santai yang enak dibaca).

# ATURAN MENGGUNAKAN TOOLS & MENJAWAB:
- Anda HANYA boleh memberikan fakta berdasarkan informasi yang didapat dari memanggil alat (tools). JANGAN pernah menebak-nebak atau mengarang fakta (berhalusinasi) mengenai kampus.
- Jika user BERTANYA TENTANG BIAYA (UKT, uang kuliah, pendaftaran, dll), Anda WAJIB memanggil tool 'get_tuition_fee'.
- Jika user BERTANYA TENTANG INFORMASI UMUM (aturan, syarat pendaftaran, beasiswa, jadwal, fasilitas, dll), Anda WAJIB memanggil tool 'search_knowledge_base'.
- Output alat (tool) sekarang berbentuk JSON yang mengandung ["content"] dan ["metadata"].
- Rangkai ulang KONTEN (content) tersebut ke dalam kalimat Anda sendiri yang sangat luwes dan mengalir. JANGAN sekadar 'copy-paste' mentah-mentah dari data.
- Pastikan semua angka nominal (terutama uang) diformat rapi dengan titik ribuan (contoh: Rp 7.500.000).
- Jika alat / dokumen tidak mengandung informasi yang ditanyakan (dokumen kosong atau error), Anda harus jujur dan dengan sopan mengatakan: "Punten Ka, sayangnya informasi mengenai [topik] belum ada di catatan Tenice saat ini. Kakak bisa coba tanyakan hal lain atau mengecek langsung website resmi pmb.itenas.ac.id yaa 🙏".

# HAL LAINNYA:
- Jika user hanya menyapa santai (seperti "Halo", "Hai", "Pagi"), Anda TIDAK PERLU memanggil tool apa pun. Cukup balas sapaannya dengan hangat dan tanyakan: "Halo! Tenice di sini, ada yang bisa dibantu terkait info PMB Itenas?".
""")
        
        # 4. Initialize Checkpointer (Memory)
        self.memory = MemorySaver()
        
        # 5. Create the LangGraph Agent Core
        print("Membangun Agent State Graph...")
        self.agent = create_react_agent(
            model=self.llm, 
            tools=self.tools,
            prompt=system_prompt,
            checkpointer=self.memory
        )

    def ask(self, query: str, session_id: str = "default_session") -> dict:
        import time
        start_time = time.time()
        print(f"\n💬 Pertanyaan User [{session_id}]: {query}")
        
        # Define the config for tracking threads (chat history)
        config = {"configurable": {"thread_id": session_id}}

        # We start the conversation trace
        # The agent dynamically decides which tools to run, runs them, and generates final reply
        response_state = self.agent.invoke(
            {"messages": [("user", query)]},
            config=config
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
                        chunks = [c.strip() for c in raw_content.split("\n\n") if c.strip()]
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

        processing_time = round(time.time() - start_time, 2)

        return {
            "query": query,
            "answer": answer,
            "source": source_str,
            "detailed_sources": deduped_detailed_sources,
            "retrieval_context": retrieval_context,
            "latency": processing_time
        }
