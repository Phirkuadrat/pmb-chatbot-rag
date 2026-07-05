import os
import fitz

def extract_raw_sk_pdf(input_path: str, raw_txt_path: str):
    doc = fitz.open(input_path)
    total = len(doc)
    print(f"Mengekstrak teks mentah dari PDF SK ({total} halaman)...")
    
    raw_sections = []
    for i in range(total):
        page = doc[i]
        # Urutkan blok secara fisik atas-bawah
        blocks = sorted(page.get_text("blocks"), key=lambda b: (round(b[1] / 20), b[0]))
        page_text = "\n".join(b[4].strip() for b in blocks if b[4].strip())
        raw_sections.append(f"--- HALAMAN {i+1} ---\n{page_text}")
        
    doc.close()
    full_raw_text = "\n\n".join(raw_sections)
    
    os.makedirs(os.path.dirname(raw_txt_path), exist_ok=True)
    with open(raw_txt_path, "w", encoding="utf-8") as f:
        f.write(full_raw_text)
        
    print(f"[OK] Ekstraksi selesai! File mentah disimpan di: {raw_txt_path}")

if __name__ == "__main__":
    input_pdf = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\153 - SK Peraturan Akademik Itenas_2025.pdf"
    raw_txt_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\153 - SK Peraturan Akademik Itenas_2025_raw.txt"
    extract_raw_sk_pdf(input_pdf, raw_txt_file)
