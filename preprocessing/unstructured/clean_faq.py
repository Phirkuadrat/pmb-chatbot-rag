import os
import json
import fitz
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# Konfigurasi LLM via Groq untuk merapikan teks
# Menggunakan model Llama
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=2048,
    api_key=os.getenv("GROQ_API_KEY", "")

)

def extract_and_clean_faq(pdf_path: str, clean_path: str):
    print(f"Membaca PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    raw_text = ""
    for page in doc:
        raw_text += page.get_text() + "\n"
        
    print("Merapikan teks menggunakan LLM (Groq)...")
    prompt = f"""
    Rapihkan teks mentah hasil ekstraksi PDF berikut menjadi dokumen Markdown yang sangat rapi.
    
    Panduan:
    1. Ada bagian berupa tabel (Jenis seleksi, batas waktu, persyaratan). Ubah baris-baris berantakan tersebut menjadi daftar berpoin (bullet points) per jenis seleksi yang jelas narasi dan poin-poinnya (hindari bentuk tabel markdown, gunakan teks paragraf/list agar mudah dipecah (chunk)).
    2. Bagian FAQ (Daftar FAQ PMB Itenas): pertahankan format Q (Pertanyaan) dan A (Jawaban), dan gunakan sub-heading (###) untuk setiap kategori FAQ (Reguler, RPL, Magister, dll).
    3. Hapus noise, footer halaman, atau karakter yang rusak. Jangan meringkas konten, pertahankan semua detail angka, tanggal, dan biayanya.
    
    Teks Mentah:
    {raw_text}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    clean_text = response.content.strip()
    
    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(clean_text)
        
    print(f"[OK] Cleaning selesai. Hasil disimpan di: {clean_path}")
    return clean_text

def chunk_text(clean_text: str, chunks_output_path: str):
    print("Memotong teks menjadi dokumen-dokumen kecil (Chunking)...")
    
    # Pisahkan berdasarkan Heading, lalu berdasar karakter
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(clean_text)
    
    # Pecah lagi jika ada bagian yang terlalu panjang (meski FAQ umumnya pendek)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50
    )
    
    final_chunks = text_splitter.split_documents(md_header_splits)
    
    # Simpan hasil chunk ke file JSON / Markdown agar user bisa baca
    output_data = []
    markdown_preview = "# Hasil Chunking FAQ\n\n"
    
    for i, chunk in enumerate(final_chunks):
        metadata = chunk.metadata
        content = chunk.page_content
        
        output_data.append({
            "chunk_id": i + 1,
            "metadata": metadata,
            "content": content
        })
        
        # Format ke Markdown untuk di-preview
        meta_str = " | ".join([f"{k}: {v}" for k, v in metadata.items()])
        markdown_preview += f"### Chunk {i + 1}\n"
        if meta_str:
            markdown_preview += f"**Konteks**: *{meta_str}*\n\n"
        markdown_preview += f"> {content}\n\n"
        markdown_preview += "---\n\n"

    with open(chunks_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_preview)

    print(f"[OK] Chunking selesai. Menghasilkan {len(final_chunks)} potongan dokumen.")
    print(f"Hasil chunk bisa dilihat di: {chunks_output_path}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    pdf_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\FAQ PMB Itenas 2026.pdf"
    clean_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean\FAQ_PMB_Itenas_2026_clean.md"
    chunks_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean\FAQ_chunks_preview.md"
    
    cleaned = extract_and_clean_faq(pdf_file, clean_file)
    chunk_text(cleaned, chunks_file)
