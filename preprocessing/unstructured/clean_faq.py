import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

def clean_raw_faq(raw_txt_path: str, clean_md_path: str) -> str:
    print("Merapikan dan menata ulang teks FAQ menggunakan LLM (Groq Llama 3.3)...")
    
    if not os.path.exists(raw_txt_path):
        raise FileNotFoundError(f"File mentah tidak ditemukan: {raw_txt_path}. Jalankan extract_faq.py terlebih dahulu.")
        
    with open(raw_txt_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    prompt = f"""
    Rapihkan teks mentah hasil ekstraksi PDF berikut menjadi dokumen Markdown yang sangat rapi.
    
    Panduan:
    1. Ada bagian berupa tabel (Jenis seleksi, batas waktu, persyaratan). Ubah baris-baris berantakan tersebut menjadi daftar berpoin (bullet points) per jenis seleksi yang jelas narasi dan poin-poinnya (hindari bentuk tabel markdown, gunakan teks paragraf/list agar mudah dipecah (chunk)).
    2. Bagian FAQ (Daftar FAQ PMB Itenas): pertahankan format Q (Pertanyaan) dan A (Jawaban), dan gunakan sub-heading (###) untuk setiap kategori FAQ (Reguler, RPL, Magister, dll).
    3. Hapus noise, footer halaman, atau karakter yang rusak. Jangan meringkas konten, pertahankan semua detail angka, tanggal, dan biayanya.
    
    Teks Mentah:
    {raw_text}
    """
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=2048,
        api_key=os.getenv("GROQ_API_KEY", "")
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    clean_text = response.content.strip()
    
    os.makedirs(os.path.dirname(clean_md_path), exist_ok=True)
    with open(clean_md_path, "w", encoding="utf-8") as f:
        f.write(clean_text)
        
    print(f"[OK] Pembersihan selesai! File bersih disimpan di: {clean_md_path}")
    return clean_text

if __name__ == "__main__":
    raw_txt_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\FAQ_PMB_Itenas_2026_raw.txt"
    clean_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean\FAQ_PMB_Itenas_2026_clean.txt"
    
    clean_raw_faq(raw_txt_file, clean_file)
