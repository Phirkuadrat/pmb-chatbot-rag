import streamlit as st
import requests
import uuid

# --- KONFIGURASI HALAMAN ---
# Set initial_sidebar_state="collapsed" agar sidebar benar-benar hilang secara default
st.set_page_config(
    page_title="Tenice - Chatbot PMB Itenas", 
    page_icon="🎓", 
    initial_sidebar_state="collapsed"
)

# --- SUNTIKAN CUSTOM CSS ---
st.markdown("""
<style>
    /* Menyembunyikan tombol expand sidebar bawaan Streamlit */
    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Mengatur kontainer baris obrolan */
    .chat-row {
        display: flex;
        margin-bottom: 15px;
        width: 100%;
        align-items: flex-end;
    }
    
    /* Rata kanan untuk pengguna */
    .row-user {
        justify-content: flex-end;
    }
    
    /* Rata kiri untuk asisten */
    .row-bot {
        justify-content: flex-start;
    }
    
    /* Styling dasar gelembung obrolan */
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }
    
    /* Gelembung Pengguna (Kanan - Hijau) */
    .bubble-user {
        background-color: #dcf8c6;
        color: #000000;
        border-bottom-right-radius: 4px;
    }
    
    /* Gelembung Asisten (Kiri - Abu/Putih) */
    .bubble-bot {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 4px;
    }
    
    /* Avatar Asisten */
    .bot-avatar {
        font-size: 24px;
        margin-right: 10px;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# API Endpoint (Sesuaikan dengan backend Anda)
API_URL = "http://127.0.0.1:8000/api/v1/chat"

# --- HEADER UI (Dengan Tombol Reset di Kanan) ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🎓 Tenice")
    st.markdown("Asisten virtual Penerimaan Mahasiswa Baru Itenas.")
with col2:
    st.write("")
    st.write("")
    if st.button("➕ Chat Baru", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

st.divider() 

def render_user_message(text):
    html = f"""
    <div class="chat-row row-user">
        <div class="chat-bubble bubble-user">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_bot_message(text):
    html = f"""
    <div class="chat-row row-bot">
        <div class="bot-avatar">🤖</div>
        <div class="chat-bubble bubble-bot">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # --- MENAMPILKAN RIWAYAT CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_user_message(msg["content"])
    else:
        render_bot_message(msg["content"])
        
        # Tampilkan sumber dokumen (jika ada) tepat di bawah gelembung
        if msg.get("sources"):
            with st.expander("📚 Lihat Sumber Referensi"):
                for source in msg["sources"]:
                    st.markdown(f"- **{source.get('document', 'Dokumen Internal')}** ({source.get('type', 'Data')})")

# --- INPUT PENGGUNA ---
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    
    # 1. Tampilkan pesan pengguna di UI langsung
    render_user_message(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Buat tempat kosong (placeholder) untuk animasi mengetik bot
    message_placeholder = st.empty()
    
    # Render animasi loading sementara
    html_loading = """
    <div class="chat-row row-bot">
        <div class="bot-avatar">🤖</div>
        <div class="chat-bubble bubble-bot">Tenice sedang mengetik... ⏳</div>
    </div>
    """
    message_placeholder.markdown(html_loading, unsafe_allow_html=True)
    
    try:
        # Panggil API RAG
        response = requests.post(
            API_URL, 
            json={"query": prompt, "session_id": st.session_state.session_id},
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})
            
            # Jika backend Anda merespon 'answer' (sesuaikan key json Anda)
            answer = data.get("answer", "Maaf, saya tidak dapat menemukan jawaban tersebut.")
            sources = data.get("sources", [])
            
            # Ganti animasi loading dengan jawaban asli
            html_answer = f"""
            <div class="chat-row row-bot">
                <div class="bot-avatar">🤖</div>
                <div class="chat-bubble bubble-bot">{answer}</div>
            </div>
            """
            message_placeholder.markdown(html_answer, unsafe_allow_html=True)
            
            # Simpan respons ke state memory UI
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "sources": sources
            })
            
            # Rerun agar expander sumber referensi muncul di posisi yang tepat
            st.rerun() 
            
        else:
            message_placeholder.markdown(f"**Error:** Layanan API bermasalah (Status {response.status_code})")
            
    except Exception as e:
        message_placeholder.markdown(f"**Error Koneksi:** Gagal menghubungi server. Pastikan Uvicorn menyala. Detail: {str(e)}")