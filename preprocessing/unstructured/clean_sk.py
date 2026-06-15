"""
Script pembersihan data untuk SK Peraturan Akademik Itenas_2025.pdf

Strategi pembersihan:
- Melewati halaman lembar pengesahan, penutup SK, dan contoh data pribadi mahasiswa
- Menggabungkan baris pendek yang terpotong menjadi paragraf utuh
- Memisahkan dan menandai setiap Pasal
- Output berupa satu file TXT bersih
"""

import sys
import re
import os
import fitz

sys.stdout.reconfigure(encoding='utf-8')

INPUT_PDF = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\153 - SK Peraturan Akademik Itenas_2025.pdf"
OUTPUT_DIR = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Halaman yang dikecualikan (0-indexed)
SKIP_PAGES = {
    0,   # Halaman 1: Lembar Pengesahan (metadata administratif)
    22,  # Halaman 23: Halaman penutup/tembusan SK
    30,  # Halaman 31: Contoh data pribadi mahasiswa (Angelina Juliani)
    31,  # Halaman 32: Tabel poin contoh mahasiswa yang sama
}

def fix_split_words(text: str) -> str:
    """
    Memperbaiki kata yang terpenggal karena PDF memisahkan huruf kapital awal
    ke dalam text box terpisah.
    Contoh: "T eknologi" → "Teknologi", "T ahun" → "Tahun"
    
    CATATAN: Tidak menggabungkan dua kata kapital penuh yang memang harus terpisah
    (misalnya "YAYASAN PENDIDIKAN" harus tetap terpisah).
    """
    # Hanya gabungkan: huruf kapital TUNGGAL diikuti spasi + kata huruf kecil
    # Contoh: "T eknologi" → "Teknologi", "T ahun" → "Tahun"
    # Tidak menyentuh: "A Nomor" (huruf kapital + nomor), atau antar kata kapital penuh
    text = re.sub(r'(?<!\w)([A-Z]) ([a-z]{2,})', lambda m: m.group(1) + m.group(2), text)

    # Perbaiki spasi berlebih sebelum tanda baca
    text = re.sub(r'\s+([.,;:])', r'\1', text)

    return text


def fix_known_terms(text: str) -> str:
    """
    Memperbaiki kesalahan encoding font l/I dan OCR typos lainnya yang umum terjadi.
    """
    corrections = [
        # Nama institusi
        (r'\bltenas\b', 'Itenas'),
        (r'\bITENAS\b', 'ITENAS'),
        (r'\blnstitut\b', 'Institut'),
        (r'\blnstitute\b', 'Institute'),
        (r'\blndonesia\b', 'Indonesia'),
        (r'\blndeks\b', 'Indeks'),
        (r'\blndex\b', 'Index'),
        (r'\blPS\b', 'IPS'),
        (r'\blPK\b', 'IPK'),
        (r'\blll\b', 'III'),
        (r'\bll\b', 'II'),
        # OCR Typo Perbaikan
        (r'\bilndeks\b', 'indeks'),
        (r'\blntemasional\b', 'Internasional'),
        (r'\bKelas lntemasional\b', 'Kelas Internasional'),
        (r'\blntemasional\b', 'internasional'),
        (r'\bintemasional\b', 'internasional'),
        (r'\bPenaali\b', 'Pengali'),
        (r'\bpenaali\b', 'pengali'),
        (r'\bPenyelenaaara\b', 'Penyelenggara'),
        (r'\bpenyelenaaara\b', 'penyelenggara'),
        (r'\bMasvarakat\b', 'Masyarakat'),
        (r'\bmasvarakat\b', 'masyarakat'),
        (r'\bKeaiatan\b', 'Kegiatan'),
        (r'\bkeaiatan\b', 'kegiatan'),
        (r'\bpain\b', 'poin'),
        (r'\bPain\b', 'Poin'),
        (r'\biumal\b', 'jurnal'),
        (r'\bIumal\b', 'Jurnal'),
        (r'\bpresiding\b', 'prosiding'),
        (r'\bPresiding\b', 'Prosiding'),
        (r'\b1l persyaratan\b', '1. persyaratan'),
        # Tambahan typo baru
        (r'\blnggris\b', 'Inggris'),
        (r'\blnformasi\b', 'Informasi'),
        (r'\blndonesla\b', 'Indonesia'),
        (r'\blndonnia\b', 'Indonesia'),
        (r'\bljazah\b', 'Ijazah'),
        (r'\blntelektual\b', 'Intelektual'),
        (r'\blndustri\b', 'Industri'),
        (r'\bllmiah\b', 'Ilmiah'),
        (r'\bJumal llmiah\b', 'Jurnal Ilmiah'),
        (r'\bJurnal Jumal\b', 'Jurnal'),
        (r'\bMu,tof1\b', 'Mustofa'),
        (r'\bMuatofa\b', 'Mustofa'),
        (r'\blabel 2\b', 'Tabel 2'),
    ]
    for pattern, replacement in corrections:
        text = re.sub(pattern, replacement, text)
    return text


def clean_page_text(raw_text: str) -> str:
    """
    Membersihkan teks mentah satu halaman PDF.
    """
    # === LANGKAH 1: Perbaiki kata yang terpenggal oleh spasi ===
    raw_text = fix_split_words(raw_text)

    # === LANGKAH 2: Koreksi kesalahan encoding font l/I ===
    raw_text = fix_known_terms(raw_text)

    lines = raw_text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Buang baris kosong berulang
        if not line:
            continue

        # Buang header/footer berulang yang tidak informatif
        skip_patterns = [
            r"^YAYASAN PENDIDIKAN DAYANG SUMBI",
            r"^INSTITUT TEKNOLOGI NASIONAL",
            r"^Jl[.].*Mustaf",
            r"^JI[.].*Mustof",
            r"^website:",
            r"^e-mail:",
            r"^Lampiran Surat Keputusan Rektor",
            r"^PERATURAN AKADEMIK$",
            r"^INSTITUTTTEKNOLOGI",   # setelah merge
            r"^INSTITUTTEKNOLOGI",
            r"^Nomor:\s*153/",
            r"^SK-Rektor/",
            r"^Revisi ke:",
            r"^TENTANG$",           # heading berulang yang tidak perlu (ada di halaman 2)
            r"^Tanggal\s*:",
            r"^Tanggal\s*:",
            r"^Telepon:",
            r"^Fax:",
        ]
        should_skip = any(re.match(p, line, re.IGNORECASE) for p in skip_patterns)
        if should_skip:
            continue

        cleaned_lines.append(line)

    # === LANGKAH 2: Gabungkan nomor/huruf yang terpisah dari teksnya ===
    # Contoh: ["1.", "bahwa Pemerintah..."] → ["1. bahwa Pemerintah..."]
    joined_lines = []
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        # Cek apakah baris ini hanya berisi marker daftar: "1." / "a." / "i." / "ii."
        is_orphan_marker = bool(re.match(r'^(\d+\.|[a-z]{1,3}\.|[ivxlc]+\.)$', line.strip()))
        if is_orphan_marker and i + 1 < len(cleaned_lines):
            # Gabungkan dengan baris berikutnya
            joined_lines.append(line.strip() + " " + cleaned_lines[i + 1].strip())
            i += 2
        else:
            joined_lines.append(line)
            i += 1

    # === LANGKAH 3: Gabungkan baris pendek yang terpenggal menjadi paragraf ===
    merged = []
    buffer = ""
    for line in joined_lines:
        is_heading = bool(re.match(r"^(Pasal\s*\d+|BAB\s+[IVXLC]+|[A-Z][A-Z\s]{4,}$)", line))
        is_numbered = bool(re.match(r"^\d+\.", line) or re.match(r"^[a-z]\.", line))
        is_bullet = line.startswith(("•", "-", "–"))

        if is_heading or is_numbered or is_bullet:
            # Simpan buffer sebelumnya dulu
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append(line)
        elif len(line) < 60 and not line.endswith((".", ":", ";")):
            # Baris pendek yang kemungkinan terpenggal — gabungkan dengan buffer
            buffer = (buffer + " " + line).strip()
        else:
            # Baris penuh — simpan buffer dulu, lalu tambahkan baris ini
            if buffer:
                buffer = (buffer + " " + line).strip()
                # Jika buffer sudah cukup panjang, flush
                if len(buffer) > 100 or line.endswith((".", ":", ";")):
                    merged.append(buffer.strip())
                    buffer = ""
            else:
                merged.append(line)

    if buffer:
        merged.append(buffer.strip())

    return "\n".join(merged)


def clean_tables(text: str) -> str:
    # 1. Format Tabel 1
    # We will match the messy Tabel 1 block and replace it with a clean markdown version.
    tabel1_pattern = r"Tabel 1\..*?D\.2 Ekstrakurikuler 1,0"
    tabel1_replacement = """Tabel 1. Indeks Pengali Poin Kegiatan SKK

### A. Tingkat Kegiatan
| No | Tingkat Kegiatan | Indeks Pengali Poin |
|---|---|---|
| A.1 | Itenas/Kecamatan/RT/RW/Desa | 1,0 |
| A.2 | Provinsi/Kota/Kabupaten | 1,5 |
| A.3 | Nasional | 2,0 |
| A.4 | Internasional | 3,0 |

### B. Lama Kegiatan
| No | Lama Kegiatan | Indeks Pengali Poin |
|---|---|---|
| B.1 | 4 - 16 Jam | 1,0 |
| B.2 | 17 - 32 Jam | 1,5 |
| B.3 | 33 - 48 Jam | 2,0 |
| B.4 | 49 - 64 Jam | 2,5 |
| B.5 | Lebih dari 64 Jam | 3,0 |
| B.6 | 1 Semester | 2,0 |

### C. Status Penyelenggara
| No | Penyelenggara | Indeks Pengali Poin |
|---|---|---|
| C.1 | Masyarakat Umum | 2,0 |
| C.2 | Pemerintah / Profesional | 2,0 |
| C.3 | Itenas/Fakultas/Program Studi | 1,0 |
| C.4 | Mahasiswa | 1,0 |

### D. Kokurikuler/Ekstrakurikuler
| No | Jenis Kegiatan | Indeks Pengali Poin |
|---|---|---|
| D.1 | Kokurikuler | 1,5 |
| D.2 | Ekstrakurikuler | 1,0 |"""

    text = re.sub(tabel1_pattern, tabel1_replacement, text, flags=re.DOTALL)

    # 2. Format Tabel 2
    tabel2_pattern = r"Tabel 2\. Indeks Penilaian Kegiatan Publikasi.*?(?=1l\s+persyaratan|ii\.)"
    tabel2_replacement = """Tabel 2. Indeks Penilaian Kegiatan Publikasi
| Posisi | Jurnal Ilmiah Internasional | Jurnal Ilmiah Nasional (S1/S2) | Jurnal Ilmiah Nasional (S3/S4) | Jurnal Ilmiah Nasional (S5/S6) | Prosiding Internasional | Prosiding Nasional | Media Populer | Blog |
|---|---|---|---|---|---|---|---|---|
| Sendiri | 6,0 | 6,0 | 5,0 | 4,0 | 5,0 | 4,0 | 3,0 | 0,25 [catatan 2] |
| Penulis Pertama | 5,0 | 5,0 | 4,0 | 3,0 | 4,0 | 3,0 | 2,0 | - |
| Non Pertama | 4,0 | 4,0 | 3,0 | 2,0 | 3,0 | 2,0 | 1,0 | - |

Keterangan:
"""
    text = re.sub(tabel2_pattern, tabel2_replacement, text, flags=re.DOTALL)

    # 3. Format Tabel 3
    tabel3_pattern = r"Tabel 3\. Indeks Pengali Poin Hak Kekayaan.*?(?=iii\.)"
    tabel3_replacement = """Tabel 3. Indeks Pengali Poin Hak Kekayaan Intelektual (HKI)
| Posisi | Hak Paten / Paten Sederhana | Hak Desain Industri, Desain Sirkuit Terpadu, Merek | Hak Cipta |
|---|---|---|---|
| Sendiri | 6 | 5 | 2 |
| Bersama | 5 | 4 | 1 |

"""
    text = re.sub(tabel3_pattern, tabel3_replacement, text, flags=re.DOTALL)

    # 4. Format Tabel 4
    tabel4_pattern = r"Tabel 4\..*?Tabel 4\. Indeks Pengali Poin Kegiatan Workshop.*?(?=iv\.)"
    tabel4_replacement = """Tabel 4. Indeks Pengali Poin Kegiatan Workshop/Training/Seminar
| No | Status | Indeks Pengali Poin |
|---|---|---|
| 1 | Peserta | 0,5 |
| 2 | Fasilitator / Asisten Lab | 2,0 |
| 3 | Koordinator Fasilitator / Koordinator Asisten Lab | 3,0 |

"""
    text = re.sub(tabel4_pattern, tabel4_replacement, text, flags=re.DOTALL)

    # 5. Format Tabel 5
    tabel5_pattern = r"Tabel 5\..*?Tabel 5\. Indeks Pengali Poin Kegiatan Organisasi.*?(?=v\.)"
    tabel5_replacement = """Tabel 5. Indeks Pengali Poin Kegiatan Organisasi/Kepanitiaan
| No | Status | Organisasi | Panitia |
|---|---|---|---|
| 1 | Anggota Organisasi selain HM Prodi (HMPS) | 0,5 | 1,0 |
| 2 | Pengurus / Panitia Non Inti / Koordinator | 2,0 | 2,0 |
| 3 | Pengurus Inti (Wakil, Bendahara, Sekretaris) | 3,0 | 3,0 |
| 4 | Ketua | 5,0 | 4,0 |

"""
    text = re.sub(tabel5_pattern, tabel5_replacement, text, flags=re.DOTALL)

    # 6. Format Tabel 6
    tabel6_pattern = r"Tabel 6\..*?Tabel 6\. Indeks Pengali Poin Kegiatan Mengikuti Perlombaan.*?(?=vi\.)"
    tabel6_replacement = """Tabel 6. Indeks Pengali Poin Kegiatan Mengikuti Perlombaan (Tidak Tergantung Pada Lama Kegiatan)
| No | Status | Kokurikuler | Ekstrakurikuler |
|---|---|---|---|
| 1 | Peserta | 0,5 | 0,5 |
| 2 | Juara Harapan Perorangan | 2,0 | 1,5 |
| 3 | Juara Harapan Beregu | 1,25 | 0,75 |
| 4 | Juara 2 atau 3 Perorangan | 2,5 | 2,0 |
| 5 | Juara 2 atau 3 Beregu | 1,5 | 1,25 |
| 6 | Juara I Perorangan | 3,5 | 3,0 |
| 7 | Juara I Beregu | 2,25 | 2,0 |

"""
    text = re.sub(tabel6_pattern, tabel6_replacement, text, flags=re.DOTALL)

    return text


def process_sk_pdf(input_path: str, output_dir: str):
    doc = fitz.open(input_path)
    total = len(doc)
    print(f"Membuka: {os.path.basename(input_path)} ({total} halaman)")

    all_sections = []
    pages_kept = 0
    pages_skipped = 0

    for i in range(total):
        if i in SKIP_PAGES:
            print(f"  [SKIP] Halaman {i+1} dikecualikan")
            pages_skipped += 1
            continue

        page = doc[i]
        # Gunakan blocks yang diurutkan atas-bawah untuk urutan baca yang benar
        blocks = sorted(page.get_text("blocks"), key=lambda b: (round(b[1] / 20), b[0]))
        raw_text = "\n".join(b[4].strip() for b in blocks if b[4].strip())

        cleaned = clean_page_text(raw_text)
        if not cleaned.strip():
            print(f"  [SKIP] Halaman {i+1} kosong setelah pembersihan")
            pages_skipped += 1
            continue

        all_sections.append(f"[Halaman {i+1}]\n{cleaned}")
        pages_kept += 1

    doc.close()

    # Gabungkan semua isi
    full_text = "\n\n".join(all_sections)

    # Normalisasi whitespace berganda
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    full_text = re.sub(r" {2,}", " ", full_text)

    # Format semua tabel berantakan menjadi Markdown terstruktur
    full_text = clean_tables(full_text)

    # Simpan output
    base = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, base + "_clean.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"\nSelesai!")
    print(f"  Halaman diproses : {pages_kept}")
    print(f"  Halaman dilewati : {pages_skipped}")
    print(f"  Total karakter   : {len(full_text)}")
    print(f"  Output disimpan di: {output_path}")
    return output_path


if __name__ == "__main__":
    output = process_sk_pdf(INPUT_PDF, OUTPUT_DIR)
    
    # Preview hasil
    print("\n--- PREVIEW 30 BARIS PERTAMA ---")
    with open(output, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[:30]:
        print(line, end="")
