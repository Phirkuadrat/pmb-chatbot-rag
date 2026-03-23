import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def run_ingestion():
    pdf_dir = os.getenv("RAW_PDF_DIR")
    db_dir = os.getenv("VECTOR_DB_PATH")
    
    print(f"Memindai semua file PDF di direktori: {pdf_dir}")
    
    if not os.path.exists(pdf_dir):
        print(f"Error: Direktori {pdf_dir} tidak ditemukan.")
        return

    # Load PDF Documents
    loader = PyPDFDirectoryLoader(pdf_dir)
    documents = loader.load()
    
    if not documents:
        print("⚠️ Tidak ada file PDF ditemukan di folder tersebut.")
        return
        
    print(f"📄 Berhasil memuat total {len(documents)} halaman dari seluruh PDF.")

    # Split Documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Seluruh dokumen dipecah menjadi {len(chunks)} chunks.")

    # Embedding dan Simpan ke Vector Store
    print("Memuat model embedding lokal...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Menyimpan data vektor ke: {db_dir}")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    
    print("Proses Ingesti Massal Selesai!")

if __name__ == "__main__":
    run_ingestion()