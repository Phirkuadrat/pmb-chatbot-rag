import os
import shutil
import hashlib
import logging
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
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Seluruh dokumen dipecah menjadi {len(chunks)} chunks.")

    # Generate unique IDs dari MD5 hash konten untuk mencegah duplikasi
    chunk_ids = [hashlib.md5(chunk.page_content.encode("utf-8")).hexdigest() for chunk in chunks]

    # === LOGGING UNTUK LAPORAN SKRIPSI ===
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "ingestion_chunks_log.md")
    
    logger.info(f"Mengekspor wujud hasil chunking ke file log: {log_path}")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Log Hasil Chunking (Ingestion)\n\n")
        f.write(f"Total Dokumen Sumber: {len(documents)}\n")
        f.write(f"Total Chunks Dihasilkan: {len(chunks)}\n")
        f.write(f"Metode: RecursiveCharacterTextSplitter (size=800, overlap=150)\n\n")
        f.write("---\n\n")
        
        for i, chunk in enumerate(chunks):
            source = chunk.metadata.get("source", "Unknown Source")
            f.write(f"### Chunk [{i+1}]\n")
            f.write(f"**Sumber File**: `{source}`\n")
            f.write(f"**ID Unik (Hash)**: `{chunk_ids[i]}`\n\n")
            f.write(f"> {chunk.page_content}\n\n")
            f.write("---\n\n")

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

    logger.info("Proses Ingesti Selesai!")


if __name__ == "__main__":
    # reset=True → hapus ChromaDB lama dan mulai dari awal
    run_ingestion(reset=True)