import os
import hashlib
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger(__name__)

def run_ingestion():
    pdf_dir = os.getenv("RAW_PDF_DIR")
    db_dir = os.getenv("VECTOR_DB_PATH")
    
    logger.info(f"Memindai semua file PDF di direktori: {pdf_dir}")
    
    if not os.path.exists(pdf_dir):
        logger.error(f"Error: Direktori {pdf_dir} tidak ditemukan.")
        return

    # Load PDF Documents
    loader = PyPDFDirectoryLoader(pdf_dir)
    documents = loader.load()
    
    if not documents:
        logger.warning("Tidak ada file PDF ditemukan di folder tersebut.")
        return
        
    logger.info(f"Berhasil memuat total {len(documents)} halaman dari seluruh PDF.")

    # Split Documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Seluruh dokumen dipecah menjadi {len(chunks)} chunks.")

    # Generate unique IDs based on MD5 hash of the content to prevent duplicates
    chunk_ids = [hashlib.md5(chunk.page_content.encode("utf-8")).hexdigest() for chunk in chunks]

    # Embedding dan Simpan ke Vector Store
    logger.info("Memuat model embedding lokal...")
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

    logger.info(f"Menyimpan data vektor ke: {db_dir} (Menggunakan upsert untuk mencegah duplikasi)")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=chunk_ids,
        persist_directory=db_dir
    )
    
    logger.info("Proses Ingesti Massal Selesai!")

if __name__ == "__main__":
    run_ingestion()