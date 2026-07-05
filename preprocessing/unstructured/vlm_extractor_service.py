import os
import io
import time
import argparse
import fitz  # PyMuPDF
from PIL import Image
from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

# Memuat variabel environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

# Menggunakan SDK Google GenAI versi terbaru (google-genai) sesuai warning deprecation
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except AttributeError:
    # Fallback ke SDK lama jika library baru belum diinstal sempurna
    import google.generativeai as genai_old
    genai_old.configure(api_key=GEMINI_API_KEY)
    client = genai_old.GenerativeModel('gemini-2.5-flash')

class VLMExtractor:
    def __init__(self):
        self.model_name = 'gemini-2.5-flash'
        
    def _get_dynamic_prompt(self, filename: str, page_num: int) -> str:
        """Membuat prompt pintar berdasarkan kata kunci di nama file."""
        filename_lower = filename.lower()
        
        base_prompt = f"Kamu adalah AI Pengolah Data Kampus. Ini adalah halaman ke-{page_num} dari dokumen '{filename}'.\n\n"
        
        if "kurikulum" in filename_lower:
            return base_prompt + """
            Tugasmu:
            Ekstrak seluruh daftar mata kuliah dari gambar ini dan tulis dalam bentuk kalimat prosa natural yang mudah dipahami. JANGAN gunakan format tabel Markdown (|), bullet list, atau heading.
            
            Panduan Khusus:
            1. Tulis setiap semester sebagai paragraf tersendiri.
            2. Format tiap baris: "Semester X berisi mata kuliah: [Nama MK] ([SKS] SKS), [Nama MK] ([SKS] SKS), ..."
            3. Untuk mata kuliah pilihan, tulis: "Mata kuliah pilihan yang tersedia: [daftar nama MK]."
            4. Abaikan elemen dekoratif. Jika tidak ada data kurikulum di halaman ini, kembalikan string kosong.
            """
        else:
            return base_prompt + """
            Tugasmu:
            Ekstrak semua teks dan informasi penting dari gambar ini menjadi paragraf prosa yang mengalir. JANGAN gunakan format tabel Markdown (|) atau bullet list.
            
            Panduan Khusus:
            1. Jika ada daftar item (fasilitas, prodi, dll), tulis sebagai kalimat: "Fasilitas yang dimiliki antara lain: A, B, dan C."
            2. Jika ada data angka atau akreditasi, sebutkan dalam kalimat natural.
            3. Abaikan teks dekoratif ("Hello", "Welcome", dll) yang tidak mengandung informasi faktual.
            4. Jika halaman hanya berisi sampul atau ornamen kosong, kembalikan string kosong.
            """

    def extract_page(self, pil_image: Image.Image, prompt: str, max_retries=3) -> str:
        """Mengirim gambar ke VLM API dengan auto-retry rate limit."""
        for attempt in range(max_retries):
            try:
                # Cek jika menggunakan SDK baru (Client)
                if hasattr(client, 'models'):
                    response = client.models.generate_content(
                        model=self.model_name,
                        contents=[pil_image, prompt]
                    )
                    return response.text
                else:
                    # SDK lama (GenerativeModel)
                    response = client.generate_content([pil_image, prompt])
                    return response.text
                    
            except ResourceExhausted as e:
                wait_time = 60 # Cooldown 1 menit jika kena limit
                print(f"\n  [RATE LIMIT API] Google API Kuota habis. Menunggu {wait_time} detik untuk retry ke-{attempt+1}...")
                time.sleep(wait_time)
            except Exception as e:
                # Untuk exception SDK baru (biasanya tipe Exception beda tapi mengandung 429 atau 503)
                if "429" in str(e) or "Quota exceeded" in str(e) or "503" in str(e):
                    wait_time = 60
                    print(f"\n  [RATE LIMIT/BUSY API] Server Google sibuk/habis kuota (429/503). Menunggu {wait_time} detik untuk retry ke-{attempt+1}...")
                    time.sleep(wait_time)
                else:
                    print(f"  [ERROR] Gagal memproses VLM: {e}")
                    return ""
        
        print("  [ERROR FATAL] Gagal setelah beberapa kali retry akibat Rate Limit/Server Busy.")
        return ""

    def process_pdf(self, pdf_path: str, out_dir: str, start_page: int = 1, end_page: int = None):
        if not os.path.exists(pdf_path):
            print(f"File tidak ditemukan: {pdf_path}")
            return
            
        filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(filename)[0]
        
        # Suffix nama file jika hanya sebagian halaman
        page_suffix = f"_p{start_page}-{end_page}" if end_page else ""
        out_path = os.path.join(out_dir, f"{base_name}_vlm_clean{page_suffix}.txt")
        
        print(f"\n=== Memproses VLM: {filename} ===")
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Tentukan range halaman
        page_start_idx = start_page - 1  # convert to 0-indexed
        page_end_idx = (end_page if end_page else total_pages)  # inclusive end
        pages_to_process = list(doc.pages(page_start_idx, page_end_idx))
        
        print(f"Memproses halaman {start_page} s/d {page_end_idx} dari total {total_pages} halaman.")
        
        markdown_results = [f"# Data Ekstraksi VLM: {base_name}\n\n"]
        
        for i, page in enumerate(pages_to_process):
            page_num = start_page + i
            print(f"-> Merender & Menganalisa Halaman {page_num}/{page_end_idx}...")
            
            # Render halaman menjadi gambar
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            pil_image = Image.open(io.BytesIO(img_bytes))
            
            # Buat prompt sesuai konteks dokumen
            prompt = self._get_dynamic_prompt(filename, page_num)
            
            # Kirim gambar ke VLM
            page_md = self.extract_page(pil_image, prompt)
            
            if page_md.strip():
                markdown_results.append(f"## Bagian {page_num}\n\n")
                markdown_results.append(page_md.strip() + "\n\n---\n\n")
                
            # Jeda untuk mencegah rate limit API gratis
            if page_num < total_pages:
                time.sleep(5)
        
        doc.close()
        
        final_text = "".join(markdown_results)
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_text)
            
        print(f"[OK] Selesai! Disimpan di: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="VLM Extractor Service for Documents")
    parser.add_argument("--file", type=str, help="Path ke satu file PDF yang ingin diekstrak", required=True)
    parser.add_argument("--outdir", type=str, default="c:/laragon/www/pmb-chatbot-rag/preprocessing/unstructured/clean", help="Folder output")
    parser.add_argument("--start-page", type=int, default=1, help="Halaman awal (1-indexed, default: 1)")
    parser.add_argument("--end-page", type=int, default=None, help="Halaman akhir inklusif (default: semua halaman)")

    args = parser.parse_args()
    extractor = VLMExtractor()
    extractor.process_pdf(args.file, args.outdir, start_page=args.start_page, end_page=args.end_page)

if __name__ == "__main__":
    main()
