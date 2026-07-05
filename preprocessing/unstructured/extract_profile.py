"""
Script ekstraksi untuk PDF Profil Program Studi.
- Teks langsung diambil dari layer PDF (presisi 100%, tanpa OCR, tanpa API)
- Output: satu file .txt bersih per prodi
"""
import os
import re
import fitz

RAW_DIR = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\Halaman Website"
OUT_DIR = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean"

PROFILE_FILES = [
    "Arsitektur - Profile.pdf",
    "DI - Profile.pdf",
    "DKV - Profile.pdf",
    "DP - Profile.pdf",
    "Elektro Profile.pdf",
    "Geodesi - Profile.pdf",
    "Industri - Profile.pdf",
    "Informatika - Profile.pdf",
    "Kimia - Profile.pdf",
    "Lingkungan - Profile.pdf",
    "Magister Industri - Profile.pdf",
    "Magister Mesin - Profile.pdf",
    "Magister Sipil - Profile.pdf",
    "Mesin - Profile.pdf",
    "PWK - Profile.pdf",
    "Sipil - Profile.pdf",
    "Sistem Informasi - Profile.pdf",
]


def extract_text(pdf_path: str, out_path: str):
    print(f"-> {os.path.basename(pdf_path)}")
    doc = fitz.open(pdf_path)
    all_pages = []

    for page in doc:
        raw = page.get_text("text")
        lines = []
        for line in raw.splitlines():
            line = line.strip()
            if len(line) < 3 or re.match(r'^\d+$', line):
                continue
            lines.append(line)
        text = "\n".join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        if text.strip():
            all_pages.append(text.strip())

    doc.close()

    final = "\n\n".join(all_pages)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"   [OK] {len(final):,} karakter")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("\n=== Profile Extraction ===\n")

    for filename in PROFILE_FILES:
        pdf_path = os.path.join(RAW_DIR, filename)
        if not os.path.exists(pdf_path):
            print(f"   [SKIP] {filename}")
            continue
        base_name = os.path.splitext(filename)[0]
        out_path = os.path.join(OUT_DIR, f"{base_name}_profile_clean.txt")
        extract_text(pdf_path, out_path)

    print("\n=== Selesai ===")


if __name__ == "__main__":
    main()
