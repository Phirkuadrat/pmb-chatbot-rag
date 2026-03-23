import streamlit as st
import os
import json
import pandas as pd
from io import BytesIO

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Tenice KB Manager",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- KUSTOMISASI CSS ---
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E88E5; margin-bottom: 0;}
    .sub-header { font-size: 1.1rem; color: #555; margin-bottom: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --- KONFIGURASI PATH ---
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./data/chromadb")
UPLOAD_TEMP_DIR = "./data/raw"

# Pastikan direktori ada
for path in [JSON_DATA_DIR, VECTOR_DB_DIR, UPLOAD_TEMP_DIR]:
    os.makedirs(path, exist_ok=True)

# --- HEADER APLIKASI ---
st.markdown('<p class="main-header">🗄️ Manajemen Knowledge Base</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Data Manager (Admin) untuk mengelola otak (sumber pengetahuan) dari Chatbot Tenice secara langsung.</p>', unsafe_allow_html=True)

# --- TABS ---
tab_json, tab_vector = st.tabs(["📝 Data Terstruktur (JSON Biaya)", "📚 Data Tak Terstruktur (PDF Aturan)"])

# ==========================================
# TAB 1: DATA TERSTRUKTUR (JSON)
# ==========================================
with tab_json:
    st.info("💡 **Tips:** Anda dapat mengelola berbagai jenis data terstruktur di sini. Folder akan dipetakan dengan Tools yang ada pada Agent.")
    
    # Deteksi Subfolder sebagai "Kategori"
    categories = [item for item in os.listdir(JSON_DATA_DIR) if os.path.isdir(os.path.join(JSON_DATA_DIR, item))]
    
    st.markdown("### 🗂️ 1. Kelola Data Terstruktur (Kategori/Folder)")
    col_cat, col_new_cat = st.columns([3, 1])
    
    with col_cat:
        if categories:
            selected_category = st.selectbox("📂 Pilih Kategori (Folder):", categories)
            target_dir = os.path.join(JSON_DATA_DIR, selected_category)
        else:
            st.warning("Belum ada kategori/folder. Buat terlebih dahulu.")
            selected_category, target_dir = None, None
            
    with col_new_cat:
        st.write("") # Spacer
        st.write("") # Spacer
        with st.popover("➕ Buat Kategori Baru", use_container_width=True):
            new_cat_name = st.text_input("Nama Kategori (tanpa spasi):", placeholder="misal: jadwal_pendaftaran")
            if st.button("Buat Folder", use_container_width=True, type="primary"):
                if new_cat_name:
                    os.makedirs(os.path.join(JSON_DATA_DIR, new_cat_name.lower().replace(" ", "_")), exist_ok=True)
                    st.success("Kategori dibuat!")
                    st.rerun()

    # --- TAMPILAN SATU FILE JSON PILIHAN ---
    if target_dir:
        json_files = [f for f in os.listdir(target_dir) if f.endswith('.json')]
        
        st.markdown("---")
        st.markdown(f"### 📄 2. Lihat & Kelola File JSON")
        
        if json_files:
            # Pilih spesifik JSON yang ingin dilihat
            selected_file = st.selectbox("🔍 Pilih file JSON yang ingin dilihat isinya:", json_files)
            
            if selected_file:
                filepath = os.path.join(target_dir, selected_file)
                
                # Tampilkan dalam sebuah Container (Kartu) agar terlihat eksklusif dan rapi
                with st.container(border=True):
                    col_title, col_del = st.columns([4, 1])
                    with col_title:
                        st.markdown(f"#### 📜 Detail Data: `{selected_file}`")
                    with col_del:
                        # Tombol hapus khusus untuk file yang sedang dibuka
                        if st.button("🗑️ Hapus File Ini", key=f"del_{selected_file}", use_container_width=True):
                            os.remove(filepath)
                            st.toast(f"File {selected_file} berhasil dihapus!", icon="✅")
                            st.rerun()
                    
                    st.divider()
                    
                    # Langsung tampilkan isi JSON tanpa expander tambahan agar langsung terbaca
                    with open(filepath, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            st.json(data)
                        except Exception as e:
                            st.error(f"Gagal membaca JSON: {e}")
        else:
            st.info(f"📂 Belum ada file JSON di kategori '{selected_category}'. Silakan unggah di bawah.")
            
        st.markdown("---")
        
        # Area Upload
        st.markdown(f"### 📤 3. Unggah / Perbarui File JSON")
        with st.container(border=True):
            uploaded_json = st.file_uploader(f"Seret dan lepas file JSON ke folder '{selected_category}'", type=["json"])
            
            if uploaded_json is not None:
                if st.button("💾 Simpan Data Terstruktur", type="primary", use_container_width=True):
                    save_path = os.path.join(target_dir, uploaded_json.name)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_json.getbuffer())
                    st.success(f"🎉 File `{uploaded_json.name}` berhasil disimpan ke `{selected_category}`!")
                    st.rerun()

# ==========================================
# TAB 2: DATA TAK TERSTRUKTUR (VECTOR DB)
# ==========================================
with tab_vector:
    st.markdown("### 📥 1. Ingest Data PDF ke Vector Database (ChromaDB)")
    st.info("Kecerdasan utama chatbot RAG berasal dari dokumen (*Knowledge Base*) yang dimasukkan ke dalam Vector Database. Anda bisa menyuntikkan dokumen aturan PMB baru di sini.")
    
    with st.container(border=True):
        uploaded_pdfs = st.file_uploader("Pilih dokumen PDF (Mendukung multple files)", type=["pdf", "txt"], accept_multiple_files=True)
        
        if uploaded_pdfs:
            if st.button("🚀 Proses & Embed ke ChromaDB", type="primary", use_container_width=True):
                with st.status("⚙️ Menginisialisasi Model Embedding dan VectorStore...", expanded=True) as status:
                    try:
                        from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
                        from langchain_text_splitters import RecursiveCharacterTextSplitter
                        from langchain_huggingface import HuggingFaceEmbeddings
                        from langchain_chroma import Chroma
                        
                        st.write("Memuat Model Embedding...")
                        EMBEDDING_MODEL = "all-MiniLM-L6-v2"
                        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
                        vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
                        
                        all_chunks = []
                        
                        # 1. Simpan & Load tiap file
                        for uploaded_file in uploaded_pdfs:
                            st.write(f"📄 Membaca {uploaded_file.name}...")
                            temp_path = os.path.join(UPLOAD_TEMP_DIR, uploaded_file.name)
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                                
                            if uploaded_file.name.endswith(".pdf"):
                                loader = PyMuPDFLoader(temp_path)
                            else:
                                loader = TextLoader(temp_path, encoding="utf-8")
                                
                            docs = loader.load()
                            
                            # Cek spesifik kalau docs kosong (biasanya PDF hasil scan/gambar)
                            if not docs or all(not d.page_content.strip() for d in docs):
                                st.warning(f"⚠️ Peringatan: Dokumen '{uploaded_file.name}' nol teks. Kemungkinan ini adalah PDF hasil Scan (Gambar) atau terenkripsi ketat. Harap gunakan PDF berbasis teks atau jalankan proses OCR terlebih dahulu.")
                                continue

                            for doc in docs:
                                doc.metadata["source"] = uploaded_file.name
                            
                            # 2. Split teks
                            text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size=1000,
                                chunk_overlap=150,
                                separators=["\n\n", "\n", " ", ""]
                            )
                            chunks = text_splitter.split_documents(docs)
                            all_chunks.extend(chunks)
                            
                        # 3. Masukkan ke Vector Database
                        st.write("Menyuntikkan data ke ChromaDB...")
                        if all_chunks:
                            vector_store.add_documents(documents=all_chunks)
                            status.update(label="✅ Selesai memproses dokumen!", state="complete", expanded=False)
                            st.success(f"✅ Sukses! {len(all_chunks)} potong teks (chunks) dari {len(uploaded_pdfs)} dokumen berhasil disuntikkan permanen ke dalam otak Tenice (ChromaDB).")
                        else:
                            status.update(label="⚠️ Gagal diproses", state="error")
                            st.warning("Dokumen kosong atau tidak dapat di-parse.")
                            
                    except Exception as e:
                        status.update(label="❌ Terjadi Kesalahan", state="error")
                        st.error(f"Gagal memproses dokumen: {e}")
                    
    st.markdown("---")
    st.markdown("### 📚 2. Isi Dokumen Saat Ini (Koleksi ChromaDB)")
    
    # 4. Fitur Visualisasi & Hapus Dokumen ChromaDB
    with st.spinner("Memuat isi Vector Database..."):
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_chroma import Chroma
            
            EMBEDDING_MODEL = "all-MiniLM-L6-v2"
            embeddings_viz = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            vector_store_viz = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings_viz)
            
            # Ambil semua data di koleksi
            collection_data = vector_store_viz.get()
            
            if not collection_data or not collection_data.get("ids"):
                st.info("Koleksi basis pengetahuan (VectorDB) saat ini masih kosong. Silakan unggah dokumen di atas.")
            else:
                # Grouping ID berdasarkan metadata 'source'
                docs_by_source = {}
                for idx, doc_id in enumerate(collection_data["ids"]):
                    meta = collection_data["metadatas"][idx] if collection_data.get("metadatas") else {}
                    source = meta.get("source", "Dokumen_Tidak_Dikenal")
                    
                    if source not in docs_by_source:
                        docs_by_source[source] = []
                    docs_by_source[source].append(doc_id)
                
                st.markdown(f"**Total Database:** {len(docs_by_source)} Dokumen PDF | {len(collection_data['ids'])} Potongan Teks (Chunks)")
                
                # Render UI list & tombol Hapus
                for source, ids in docs_by_source.items():
                    with st.container(border=True):
                        col_icon, col_info, col_btn = st.columns([1, 6, 2])
                        with col_icon:
                            st.markdown("📄")
                        with col_info:
                            st.markdown(f"**{source}**")
                            st.caption(f"Terdiri dari {len(ids)} potongan kalimat/chunks")
                        with col_btn:
                            safe_key = source.replace(" ", "_").replace(".", "_")
                            if st.button("🗑️ Hapus Dokumen", key=f"del_{safe_key}", use_container_width=True):
                                vector_store_viz.delete(ids=ids)
                                st.success(f"`{source}` berhasil dihapus secara permanen dari otak AI!")
                                st.rerun()

        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca ChromaDB: {e}")