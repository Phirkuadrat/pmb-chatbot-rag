import os
import shutil
import hashlib
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger(__name__)


def run_ingestion(reset: bool = False):
    clean_dir = os.getenv("CLEAN_DATA_DIR")
    db_dir = os.getenv("VECTOR_DB_PATH")

    # Hapus seluruh ChromaDB lama jika diminta
    if reset and os.path.exists(db_dir):
        logger.info(f"Menghapus ChromaDB lama di: {db_dir}")
        shutil.rmtree(db_dir)
        logger.info("ChromaDB lama berhasil dihapus.")

    # Memuat file TXT bersih
    if not clean_dir or not os.path.exists(clean_dir):
        logger.error(f"Direktori tidak ditemukan: {clean_dir}")
        return

    logger.info(f"Memuat file TXT dari: {clean_dir}")
    loader = DirectoryLoader(
        clean_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    documents = loader.load()

    if not documents:
        logger.warning("Tidak ada file TXT ditemukan. Proses dihentikan.")
        return

    logger.info(f"Berhasil memuat {len(documents)} file TXT.")

    # Pemotongan teks (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Seluruh dokumen dipecah menjadi {len(chunks)} chunks.")

    # Generate unique IDs dari MD5 hash konten + index untuk mencegah duplikasi antar chunk yang isinya persis sama
    chunk_ids = [f"{hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()}_{i}" for i, chunk in enumerate(chunks)]

    # === LOGGING UNTUK LAPORAN SKRIPSI ===
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"ingestion_chunks_log_{timestamp}.txt")
    
    logger.info(f"Mengekspor wujud hasil chunking ke file log: {log_path}")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("LOG HASIL CHUNKING (INGESTION)\n")
        f.write("=" * 50 + "\n")
        f.write(f"Tanggal & Jam    : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Total Dokumen    : {len(documents)} file\n")
        f.write(f"Total Chunks     : {len(chunks)} chunks\n")
        f.write(f"Metode Chunking  : RecursiveCharacterTextSplitter\n")
        f.write(f"Chunk Size       : 1200 karakter\n")
        f.write(f"Chunk Overlap    : 250 karakter\n")
        f.write("=" * 50 + "\n\n")
        
        for i, chunk in enumerate(chunks):
            source = chunk.metadata.get("source", "Unknown Source")
            f.write(f"[Chunk {i+1}]\n")
            f.write(f"Sumber File : {source}\n")
            f.write(f"ID Unik     : {chunk_ids[i]}\n")
            f.write(f"Isi         :\n{chunk.page_content}\n")
            f.write("-" * 50 + "\n\n")

    # === EMBEDDING & SIMPAN ===
    logger.info("Memuat model embedding lokal...")
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

    logger.info(f"Menyimpan {len(chunks)} chunks ke ChromaDB: {db_dir}")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=chunk_ids,
        persist_directory=db_dir
    )

    # === LOGGING EMBEDDING UNTUK LAPORAN SKRIPSI ===
    emb_log_path = os.path.join(log_dir, f"ingestion_embeddings_log_{timestamp}.txt")
    logger.info(f"Mengekspor wujud vektor embedding ke file log: {emb_log_path}")
    
    # Ambil data dari ChromaDB menggunakan ID chunk
    db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    db_data = db.get(ids=chunk_ids, include=["embeddings"])
    
    # Petakan hasil ke dictionary berdasarkan ID agar urutannya tetap sesuai
    vector_map = {id_: emb for id_, emb in zip(db_data["ids"], db_data["embeddings"])}
    
    with open(emb_log_path, "w", encoding="utf-8") as f:
        f.write("LOG HASIL EMBEDDING VEKTOR\n")
        f.write("=" * 50 + "\n")
        f.write(f"Tanggal & Jam    : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}\n")
        f.write(f"Model Embedding  : paraphrase-multilingual-MiniLM-L12-v2\n")
        f.write(f"Dimensi Vektor   : 384 dimensi\n")
        f.write(f"Total Vektor     : {len(chunks)} vektor\n")
        f.write("=" * 50 + "\n\n")
        
        for i, chunk_id in enumerate(chunk_ids):
            source = chunks[i].metadata.get("source", "Unknown Source")
            vector = vector_map.get(chunk_id, [])
            f.write(f"[Chunk {i+1}]\n")
            f.write(f"ID Unik     : {chunk_id}\n")
            f.write(f"Sumber File : {source}\n")
            if vector is not None and len(vector) > 0:
                # Menampilkan seluruh 384 nilai angka dengan presisi 5 desimal
                vector_str = ", ".join([f"{v:.5f}" for v in vector])
                f.write(f"Vektor (384 dim) :\n[{vector_str}]\n")
            else:
                f.write("Vektor      : [Data Tidak Ditemukan]\n")
            f.write("-" * 50 + "\n\n")

    logger.info("Proses Ingesti Selesai!")


if __name__ == "__main__":
    # reset=True → hapus ChromaDB lama dan mulai dari awal
    run_ingestion(reset=True)