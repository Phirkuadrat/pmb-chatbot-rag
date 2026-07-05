import re
import os

# Halaman yang dikecualikan (0-indexed)
SKIP_PAGES = {
    0,   # Halaman 1: Lembar Pengesahan (metadata administratif)
    22,  # Halaman 23: Halaman penutup/tembusan SK
    30,  # Halaman 31: Contoh data pribadi mahasiswa (Angelina Juliani)
    31,  # Halaman 32: Tabel poin contoh mahasiswa yang sama
}

def fix_split_words(text: str) -> str:
    text = re.sub(r'(?<!\w)([A-Z]) ([a-z]{2,})', lambda m: m.group(1) + m.group(2), text)
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    return text

def fix_known_terms(text: str) -> str:
    corrections = [
        # === Koreksi OCR: huruf l (kecil) vs I (kapital) ===
        (r'\bltenas\b', 'Itenas'),
        (r'\bITENAS\b', 'ITENAS'),
        (r'\blnstitut\b', 'Institut'),
        (r'\blnstitute\b', 'Institute'),
        (r'\blndonesia\b', 'Indonesia'),
        (r'\blndonesla\b', 'Indonesia'),
        (r'\blndonnian\b', 'Indonesia'),
        (r'\blndeks\b', 'Indeks'),
        (r'\bilndeks\b', 'indeks'),
        (r'\blndex\b', 'Index'),
        (r'\blPS\b', 'IPS'),
        (r'\blPK\b', 'IPK'),
        (r'\blll\b', 'III'),
        (r'\bll\b', 'II'),
        (r'\blntemasional\b', 'Internasional'),
        (r'\bKelas lntemasional\b', 'Kelas Internasional'),
        (r'\bintemasional\b', 'internasional'),
        (r'\blnggris\b', 'Inggris'),
        (r'\blnformasi\b', 'Informasi'),
        (r'\bljazah\b', 'Ijazah'),
        (r'\blntelektual\b', 'Intelektual'),
        (r'\blndustri\b', 'Industri'),
        (r'\bllmiah\b', 'Ilmiah'),
        # === Koreksi OCR: kata umum terpotong/salah karakter ===
        (r'\bSa[~8]ana\b', 'Sarjana'),          # Sa~ana / Sa8ana → Sarjana
        (r'\bSariana\b', 'Sarjana'),              # Sariana → Sarjana
        (r'\bSatjana\b', 'Sarjana'),              # Satjana → Sarjana
        (r'\bSanana\b', 'Sarjana'),               # Sanana → Sarjana
        (r'\bGanji!\b', 'Ganjil'),                # Ganji! → Ganjil
        (r'\bGanji1\b', 'Ganjil'),                # Ganji1 → Ganjil
        (r'TENT\s+ANG', 'TENTANG'),               # TENT ANG → TENTANG
        (r'EV\s+ALUASI', 'EVALUASI'),             # EV ALUASI → EVALUASI
        (r'PROSESPEMBELAJARAN', 'PROSES PEMBELAJARAN'),
        (r'DANPINDAH', 'DAN PINDAH'),
        (r'\bOlimpide\b', 'Olimpiade'),           # Olimpide → Olimpiade
        (r'\bolimpide\b', 'olimpiade'),
        (r'\bTinakat\b', 'Tingkat'),              # Tinakat → Tingkat
        (r'\btinakat\b', 'tingkat'),
        (r'\bCamoion\b', 'Champion'),             # Camoion → Champion
        (r'\bKeTa\b', 'Kerja'),                   # KeTa → Kerja
        (r'\bkeTa\b', 'kerja'),
        (r'\bdikeTakan\b', 'dikerjakan'),
        (r'\bSertta\b', 'Berita'),                # Sertta → Berita
        (r'\bbidana\b', 'bidang'),                # bidana → bidang
        (r'\bBidana\b', 'Bidang'),
        (r'\bT anggal\b', 'Tanggal'),             # T anggal → Tanggal
        (r'\bPeru\s+mus\b', 'Perumus'),           # Peru mus → Perumus
        (r'\bOekan\b', 'Dekan'),                  # Oekan → Dekan
        (r'\b~tika\b', 'Etika'),                  # ~tika → Etika
        (r'\bternasuk\b', 'termasuk'),            # tennasuk → termasuk
        (r'\btennasuk\b', 'termasuk'),
        (r'\bmemenuhui\b', 'memenuhi'),           # memenuhui → memenuhi
        (r'\biurnlah\b', 'jumlah'),               # iurnlah → jumlah
        (r'\biumlah\b', 'jumlah'),                # iumlah → jumlah
        (r'\biurnal\b', 'jurnal'),                # iurnal → jurnal
        (r'\bKeTa\s+Nyata\b', 'Kerja Nyata'),
        (r'\bKurikuler/Ekstrakurikuler', 'Kokurikuler/Ekstrakurikuler'),
        # === Koreksi singkatan dan istilah institusi ===
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
        (r'\bJumal llmiah\b', 'Jurnal Ilmiah'),
        (r'\bJurnal Jumal\b', 'Jurnal'),
        (r'\bMu,tof1\b', 'Mustofa'),
        (r'\bMuatofa\b', 'Mustofa'),
        (r'\bMu1tofa\b', 'Mustofa'),
        (r'\blabel 2\b', 'Tabel 2'),
        (r'\blndonesla\b', 'Indonesia'),
        (r'\blndonnia\b', 'Indonesia'),
        (r'\blndoneaia\b', 'Indonesia'),
        (r'\bwebllte\b', 'website'),
        (r'\be-mall\b', 'e-mail'),
        (r'\bPenaali\b', 'Pengali'),
        (r'\bSememester\b', 'Semester'),
        (r'\bbesamya\b', 'besarnya'),
        (r'\bbesamya\b', 'besarnya'),
        (r'rektorat@itenas\.ac\.i<!', 'rektorat@itenas.ac.id'),
    ]
    for pattern, replacement in corrections:
        text = re.sub(pattern, replacement, text)
    return text

def clean_page_text(raw_text: str) -> str:
    raw_text = fix_split_words(raw_text)
    raw_text = fix_known_terms(raw_text)
    
    lines = raw_text.split("\n")
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        skip_patterns = [
            r"^YAYASAN PENDIDIKAN DAYANG SUMBI",
            r"^INSTITUT TEKNOLOGI NASIONAL",
            r"^Jl[.].*Mustaf",
            r"^JI[.].*Mustof",
            r"^website:",
            r"^e-mail:",
            r"^Lampiran Surat Keputusan Rektor",
            r"^PERATURAN AKADEMIK$",
            r"^INSTITUTTTEKNOLOGI",
            r"^INSTITUTTEKNOLOGI",
            r"^Nomor:\s*153/",
            r"^SK-Rektor/",
            r"^Revisi ke:",
            r"^TENTANG$",
            r"^Tanggal\s*:",
            r"^Telepon:",
            r"^Fax:",
        ]
        should_skip = any(re.match(p, line, re.IGNORECASE) for p in skip_patterns)
        if should_skip:
            continue
            
        cleaned_lines.append(line)
        
    joined_lines = []
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        is_orphan_marker = bool(re.match(r'^(\d+\.|[a-z]{1,3}\.|[ivxlc]+\.)$', line.strip()))
        if is_orphan_marker and i + 1 < len(cleaned_lines):
            joined_lines.append(line.strip() + " " + cleaned_lines[i + 1].strip())
            i += 2
        else:
            joined_lines.append(line)
            i += 1
            
    merged = []
    buffer = ""
    for line in joined_lines:
        is_heading = bool(re.match(r"^(Pasal\s*\d+|BAB\s+[IVXLC]+|[A-Z][A-Z\s]{4,}$)", line))
        is_numbered = bool(re.match(r"^\d+\.", line) or re.match(r"^[a-z]\.", line))
        is_bullet = line.startswith(("•", "-", "–"))
        
        if is_heading or is_numbered or is_bullet:
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append(line)
        elif len(line) < 60 and not line.endswith((".", ":", ";")):
            buffer = (buffer + " " + line).strip()
        else:
            if buffer:
                buffer = (buffer + " " + line).strip()
                if len(buffer) > 100 or line.endswith((".", ":", ";")):
                    merged.append(buffer.strip())
                    buffer = ""
            else:
                merged.append(line)
                
    if buffer:
        merged.append(buffer.strip())
        
    return "\n".join(merged)

def clean_tables(text: str) -> str:
    # Tabel nilai huruf (Pasal 42) - rekonstruksi dari baris tersebar
    nilai_huruf_pattern = r"NO\.\s*NILAI HURUF\s*INDEKS NILAI\s*NILAIANGKA\s*KATEGORI.*?(?=Pasal\s*43)"
    nilai_huruf_replacement = """Tabel Penilaian Hasil Belajar Mata Kuliah:
| No | Nilai Huruf | Indeks Nilai | Nilai Angka | Kategori |
|---|---|---|---|---|
| 1 | A | 4 | 80 sampai dengan 100 | Amat sangat baik |
| 2 | AB | 3,5 | 73 sampai dengan < 80 | Sangat baik |
| 3 | B | 3 | 65 sampai dengan < 73 | Baik |
| 4 | BC | 2,5 | 60 sampai dengan < 65 | Cukup baik |
| 5 | C | 2 | 50 sampai dengan < 60 | Cukup |
| 6 | D | 1 | 40 sampai dengan < 50 | Kurang baik |
| 7 | E | 0 | < 40 | Gagal |

"""
    text = re.sub(nilai_huruf_pattern, nilai_huruf_replacement, text, flags=re.DOTALL)

    # Tabel Konversi SKS Lomba (Halaman 26) - rekonstruksi dari baris tersebar
    konversi_lomba_pattern = r"No\.\s*Jenis Kegiatan\s*Konversi sks.*?(?=B\. PEDOMAN SISTEM KREDIT|No\.\s*Jenis Program)"
    konversi_lomba_replacement = """Tabel Konversi SKS Kegiatan Lomba Nasional (Program Dikti):
| No | Jenis Kegiatan | Lolos Seleksi Wilayah | Finalis / Maju ke Final | Menjadi Juara Tingkat Nasional |
|---|---|---|---|---|
| 1 | Pagelaran mahasiswa nasional bidang TIK | 2 | 2 | 4 |
| 2 | Kompetisi mahasiswa nasional bidang ilmu bisnis, manajemen dan keuangan | 2 | 2 | 4 |
| 3 | National University Debating Champion (NUDC) | 2 | 2 | 4 |
| 4 | Kompetisi bangunan gedung Indonesia | 2 | 2 | 4 |
| 5 | Kontes kapal cepat tak berawak nasional | 2 | 2 | 4 |
| 6 | Kontes mobil hemat energi | 2 | 2 | 4 |
| 7 | Olimpiade nasional matematika dan IPA | 2 | 2 | 4 |
| 8 | Kontes robot Indonesia | 2 | 2 | 4 |
| 9 | Kontes robot terbang Indonesia | 2 | 2 | 4 |
| 10 | Lomba inovasi digital mahasiswa | 2 | 2 | 4 |

Tabel Konversi SKS Program Kemahasiswaan Nasional:
| No | Jenis Program | Lolos | Selesai / PIMNAS |
|---|---|---|---|
| 1 | Program pembinaan mahasiswa wirausaha | 2 | 4 |
| 2 | Program holistik pembinaan dan pemberdayaan desa | 2 | 4 |
| 3 | Program Kreativitas Mahasiswa (PKM) | 2 | 5 |
| 4 | Program Penguatan Kapasitas Organisasi Kemahasiswaan (PPK Ormawa) | 2 | 4 |

"""
    text = re.sub(konversi_lomba_pattern, konversi_lomba_replacement, text, flags=re.DOTALL)

    # Tabel 1
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

    # Tabel 2
    tabel2_pattern = r"Tabel 2\. Indeks Penilaian Kegiatan Publikasi.*?(?=1l\s+persyaratan|ii\.)"
    tabel2_replacement = """Tabel 2. Indeks Penilaian Kegiatan Publikasi
| Posisi | Jurnal Ilmiah Internasional | Jurnal Ilmiah Nasional (S1/S2) | Jurnal Ilmiah Nasional (S3/S4) | Jurnal Ilmiah Nasional (S5/S6) | Prosiding Internasional | Prosiding Nasional | Media Populer | Blog |
|---|---|---|---|---|---|---|---|---|
| Sendiri | 6,0 | 6,0 | 5,0 | 4,0 | 5,0 | 4,0 | 3,0 | 0,25 [catatan 2] |
| Penulis Pertama | 5,0 | 5,0 | 4,0 | 3,0 | 4,0 | 3,0 | 2,0 | - |
| Non Pertama | 4,0 | 4,0 | 3,0 | 2,0 | 3,0 | 2,0 | 1,0 | - |

Keterangan:"""
    text = re.sub(tabel2_pattern, tabel2_replacement, text, flags=re.DOTALL)

    # Tabel 3
    tabel3_pattern = r"Tabel 3\. Indeks Pengali Poin Hak Kekayaan.*?(?=iii\.)"
    tabel3_replacement = """Tabel 3. Indeks Pengali Poin Hak Kekayaan Intelektual (HKI)
| Posisi | Hak Paten / Paten Sederhana | Hak Desain Industri, Desain Sirkuit Terpadu, Merek | Hak Cipta |
|---|---|---|---|
| Sendiri | 6 | 5 | 2 |
| Bersama | 5 | 4 | 1 |

"""
    text = re.sub(tabel3_pattern, tabel3_replacement, text, flags=re.DOTALL)

    # Tabel 4
    tabel4_pattern = r"Tabel 4\..*?Tabel 4\. Indeks Pengali Poin Kegiatan Workshop.*?(?=iv\.)"
    tabel4_replacement = """Tabel 4. Indeks Pengali Poin Kegiatan Workshop/Training/Seminar
| No | Status | Indeks Pengali Poin |
|---|---|---|
| 1 | Peserta | 0,5 |
| 2 | Fasilitator / Asisten Lab | 2,0 |
| 3 | Koordinator Fasilitator / Koordinator Asisten Lab | 3,0 |

"""
    text = re.sub(tabel4_pattern, tabel4_replacement, text, flags=re.DOTALL)

    # Tabel 5
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

    # Tabel 6
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

def clean_raw_sk(raw_txt_path: str, clean_txt_path: str) -> str:
    print("Merapikan, memfilter halaman, dan merekonstruksi tabel SK...")
    
    if not os.path.exists(raw_txt_path):
        raise FileNotFoundError(f"File mentah tidak ditemukan: {raw_txt_path}. Jalankan extract_sk.py terlebih dahulu.")
        
    with open(raw_txt_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    parts = re.split(r'--- HALAMAN (\d+) ---\n', raw_text)
    
    pages = {}
    for j in range(1, len(parts), 2):
        page_num = int(parts[j])
        page_text = parts[j+1]
        pages[page_num] = page_text
        
    all_sections = []
    pages_kept = 0
    pages_skipped = 0
    
    for page_num in sorted(pages.keys()):
        if (page_num - 1) in SKIP_PAGES:
            pages_skipped += 1
            continue
            
        page_text = pages[page_num].strip()
        cleaned = clean_page_text(page_text)
        if not cleaned.strip():
            pages_skipped += 1
            continue
            
        all_sections.append(f"[Halaman {page_num}]\n{cleaned}")
        pages_kept += 1
        
    full_text = "\n\n".join(all_sections)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    full_text = re.sub(r" {2,}", " ", full_text)
    full_text = clean_tables(full_text)
    
    os.makedirs(os.path.dirname(clean_txt_path), exist_ok=True)
    with open(clean_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"[OK] Pembersihan selesai! File bersih disimpan di: {clean_txt_path}")
    return full_text

if __name__ == "__main__":
    raw_txt_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\raw\153 - SK Peraturan Akademik Itenas_2025_raw.txt"
    clean_txt_file = r"c:\laragon\www\pmb-chatbot-rag\preprocessing\unstructured\clean\153 - SK Peraturan Akademik Itenas_2025_clean.txt"
    clean_raw_sk(raw_txt_file, clean_txt_file)
