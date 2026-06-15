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
                # Untuk exception SDK baru (biasanya tipe Exception beda tapi mengandung 429)
                if "429" in str(e) or "Quota exceeded" in str(e):
                    wait_time = 60
                    print(f"\n  [RATE LIMIT API] Google API Kuota habis (429). Menunggu {wait_time} detik untuk retry ke-{attempt+1}...")
                    time.sleep(wait_time)
                else:
                    print(f"  [ERROR] Gagal memproses VLM: {e}")
                    return ""
        
        print("  [ERROR FATAL] Gagal setelah beberapa kali retry akibat Rate Limit.")
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

    def extract_image_vlm(self, pil_image: Image.Image, page_num: int, img_idx: int) -> str:
        """Kirim gambar (hasil crop dari PDF) ke VLM untuk dideskripsikan."""
        prompt = f"""
        Ini adalah gambar yang diekstrak dari halaman {page_num} dokumen profil program studi sebuah kampus.
        Tugasmu: Deskripsikan informasi faktual yang ada dalam gambar ini dalam kalimat prosa natural.
        - Jika berisi tabel atau daftar, tuliskan isinya sebagai kalimat: "Tabel ini memuat..."
        - Jika berisi foto kegiatan mahasiswa, cukup tulis satu kalimat deskripsi singkat.
        - Jika berisi infografis data/angka, ekstrak angka dan labelnya.
        - Jika gambar dekoratif tanpa informasi faktual (logo, background, ornamen), kembalikan string kosong.
        """
        return self.extract_page(pil_image, prompt, max_retries=3)

    def process_hybrid_page(self, page, filename: str, page_num: int) -> str:
        """
        Mengekstrak teks murni dan mendeteksi gambar untuk diproses VLM.
        Hasilnya diurutkan berdasarkan posisi vertikal (Y) dari atas ke bawah.
        """
        # Ambil semua blok teks dari PDF
        blocks = page.get_text("blocks")
        items = []

        for block in blocks:
            if block[6] == 0:  # Deteksi blok teks biasa
                text = block[4].strip()
                if text:
                    items.append((block[1], text))
                    
        # Deteksi gambar di dalam halaman
        image_list = page.get_images(full=True)
        api_called = False
        img_count = 0

        for img in image_list:
            xref = img[0]
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                continue

            for rect in rects:
                # Abaikan ornamen atau gambar kecil
                if rect.width < 100 or rect.height < 100:
                    continue
                    
                img_count += 1
                y0 = rect.y0
                print(f"    [Hybrid] Menemukan gambar di y={y0:.1f} ({rect.width:.1f}x{rect.height:.1f} px), memanggil VLM...")
                
                # Potong gambar sesuai area
                mat = fitz.Matrix(150 / 72, 150 / 72)
                pix = page.get_pixmap(matrix=mat, clip=rect)
                img_bytes = pix.tobytes("png")
                pil_img = Image.open(io.BytesIO(img_bytes))

                # Minta deskripsi gambar ke VLM
                description = self.extract_image_vlm(pil_img, page_num, img_count)
                if description.strip():
                    items.append((y0, f"[Informasi dari gambar]: {description.strip()}"))
                    api_called = True

                # Jeda API jika VLM baru saja dipanggil
                if api_called:
                    time.sleep(5)
                    api_called = False

        # Urutkan elemen dari atas ke bawah halaman
        items.sort(key=lambda x: x[0])

        # Gabungkan hasil teks dan teks dari gambar
        return "\n\n".join(content for _, content in items if content.strip())

    def process_hybrid_pdf(self, pdf_path: str, out_dir: str):
        """Proses PDF campuran teks+gambar dengan Hybrid Extraction."""
        if not os.path.exists(pdf_path):
            print(f"File tidak ditemukan: {pdf_path}")
            return

        filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(filename)[0]
        out_path = os.path.join(out_dir, f"{base_name}_hybrid_clean.txt")

        print(f"\n=== Memproses HYBRID: {filename} ===")
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        all_text_parts = []

        for i, page in enumerate(doc):
            page_num = i + 1
            print(f"-> Halaman {page_num}/{total_pages}...")
            page_content = self.process_hybrid_page(page, filename, page_num)
            if page_content.strip():
                all_text_parts.append(page_content.strip())

        doc.close()

        final_text = "\n\n".join(all_text_parts)
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        print(f"[OK] Hybrid Extraction selesai! Disimpan di: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="VLM Extractor Service for Documents")
    parser.add_argument("--file", type=str, help="Path ke satu file PDF yang ingin diekstrak", required=True)
    parser.add_argument("--outdir", type=str, default="c:/laragon/www/pmb-chatbot-rag/preprocessing/unstructured/clean", help="Folder output")
    parser.add_argument("--start-page", type=int, default=1, help="Halaman awal (1-indexed, default: 1)")
    parser.add_argument("--end-page", type=int, default=None, help="Halaman akhir inklusif (default: semua halaman)")
    parser.add_argument("--mode", type=str, default="vlm", choices=["vlm", "hybrid"],
                        help="Mode ekstraksi: 'vlm' (seluruh halaman ke VLM) atau 'hybrid' (teks asli + VLM gambar)")
    
    args = parser.parse_args()
    extractor = VLMExtractor()
    
    if args.mode == "hybrid":
        extractor.process_hybrid_pdf(args.file, args.outdir)
    else:
        extractor.process_pdf(args.file, args.outdir, start_page=args.start_page, end_page=args.end_page)

if __name__ == "__main__":
    main()
