import os
import fitz

def extract_raw_faq(pdf_path: str, raw_txt_path: str):
    print("Mengekstrak teks mentah dari PDF FAQ...")
    doc = fitz.open(pdf_path)
    raw_text = ""
    for i, page in enumerate(doc):
        raw_text += f"\n--- HALAMAN {i+1} ---\n"
        raw_text += page.get_text() + "\n"
    doc.close()
    
    os.makedirs(os.path.dirname(raw_txt_path), exist_ok=True)
    with open(raw_txt_path, "w", encoding="utf-8") as f:
        f.write(raw_text)
        
    print(f"[OK] Ekstraksi selesai! File mentah disimpan di: {raw_txt_path}")

if __name__ == "__main__":
    pdf_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\FAQ PMB Itenas 2026.pdf"
    raw_txt_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\FAQ_PMB_Itenas_2026_raw.txt"
    extract_raw_faq(pdf_file, raw_txt_file)
