"""
Tahap 2: Excel → JSON
Membaca biaya_pendidikan.xlsx hasil Stage 1 dan menghasilkan JSON terstruktur.

Tidak ada hardcode:
- Daftar prodi S2 dideteksi dari sheet Magister_S2
- Akreditasi dibaca dari kolom Akreditasi di sheet RPL
- UKT S2 diambil langsung dari kolom UKT (ffill jika kosong)
- Biaya RPL diisi via ffill/bfill per Jenjang
"""
import os
import json
import pandas as pd

INPUT_EXCEL = "./preprocessing/biaya_pipeline/biaya_pendidikan_full_ocr.xlsx"
OUTPUT_DIR = "./data/structured/biaya"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Pemetaan nama program studi ke nama file JSON
# Ini adalah konfigurasi urutan output, bukan logika bisnis
MAJOR_MAP = {
    "Teknik Elektro": "teknik_elektro.json",
    "Teknik Mesin": "teknik_mesin.json",
    "Teknik Industri": "teknik_industri.json",
    "Teknik Kimia": "teknik_kimia.json",
    "Informatika": "informatika.json",
    "Sistem Informasi": "sistem_informasi.json",
    "Teknik Sipil": "teknik_sipil.json",
    "Teknik Geodesi": "teknik_geodesi.json",
    "Perencanaan Wilayah dan Kota": "perencanaan_wilayah_dan_kota.json",
    "Teknik Lingkungan": "teknik_lingkungan.json",
    "Arsitektur": "arsitektur.json",
    "Desain Interior": "desain_interior.json",
    "Desain Produk": "desain_produk.json",
    "Desain Komunikasi Visual": "desain_komunikasi_visual.json"
}


def clean_int(val):
    if pd.isna(val) or val is None:
        return 0
    try:
        return int(float(str(val).replace(".", "").replace(",", "")))
    except ValueError:
        return 0


def match_major_name(text):
    """Cocokkan teks OCR ke nama prodi kanonik."""
    if pd.isna(text) or not text:
        return None
    text_clean = str(text).lower().strip()
    for word in ["pmb", "itenas", "biaya", "pendidikan", "tabel"]:
        text_clean = text_clean.replace(word, "")
    text_clean = "".join(c for c in text_clean if c.isalnum())

    for major in MAJOR_MAP.keys():
        major_clean = "".join(c for c in major.lower() if c.isalnum())
        if major_clean == text_clean:
            return major

    for major in MAJOR_MAP.keys():
        major_clean = "".join(c for c in major.lower() if c.isalnum())
        if major_clean in text_clean:
            return major

    if len(text_clean) < 5:
        return None

    keywords = {
        "elektro": "Teknik Elektro",
        "mesin": "Teknik Mesin",
        "industri": "Teknik Industri",
        "kimia": "Teknik Kimia",
        "informatika": "Informatika",
        "sistem": "Sistem Informasi",
        "sipil": "Teknik Sipil",
        "geodesi": "Teknik Geodesi",
        "perencanaan": "Perencanaan Wilayah dan Kota",
        "wilayah": "Perencanaan Wilayah dan Kota",
        "pwk": "Perencanaan Wilayah dan Kota",
        "lingkungan": "Teknik Lingkungan",
        "arsitektur": "Arsitektur",
        "interior": "Desain Interior",
        "produk": "Desain Produk",
        "visual": "Desain Komunikasi Visual",
        "dkv": "Desain Komunikasi Visual"
    }

    for kw, major in keywords.items():
        if kw in text_clean:
            return major

    return None


def conform_to_schema(extracted, schema, key_name=None):
    """
    Susun ulang key output agar urutannya mengikuti schema.
    - Semua nilai murni dari extracted (hasil OCR).
    - Key yang ada di schema tapi tidak di extracted → null.
    - Key yang ada di extracted tapi tidak di schema → diabaikan.
    """
    if isinstance(schema, dict) and isinstance(extracted, dict):
        # Penanganan khusus untuk dict dinamis seperti rincian_per_semester
        if key_name == "rincian_per_semester":
            template = schema.get("semester_1")
            conformed = {}
            if template:
                for sem_key, sem_val in extracted.items():
                    conformed[sem_key] = conform_to_schema(sem_val, template, sem_key)
                return conformed
            return extracted

        conformed = {}
        for key, schema_val in schema.items():
            if key.startswith("_"):  # lewati komentar/metadata di schema
                continue
            if key in extracted:
                conformed[key] = conform_to_schema(extracted[key], schema_val, key)
            else:
                # Key tidak ditemukan di OCR → null, bukan diisi dari schema
                conformed[key] = None
        return conformed
    elif isinstance(schema, list) and isinstance(extracted, list):
        # List: susun setiap item mengikuti schema item pertama sebagai template
        template = schema[0] if schema else None
        return [conform_to_schema(item, template) if template else item for item in extracted]
    else:
        # Leaf node: kembalikan nilai extracted apa adanya
        return extracted


def build_akreditasi_map(df_rpl):
    """
    Bangun mapping akreditasi dari sheet RPL secara dinamis.
    Lebih diprioritaskan dari kolom Akreditasi di sheet Sarjana_Sem1 (opsional).
    """
    akreditasi_map = {}
    for _, row in df_rpl.iterrows():
        major_match = match_major_name(row.get("Program Studi", ""))
        if not major_match:
            continue
        akreditasi = str(row.get("Akreditasi", "")).strip()
        if akreditasi and akreditasi.lower() not in ("nan", "none", ""):
            akreditasi_map[major_match] = akreditasi
    return akreditasi_map


def main():
    if not os.path.exists(INPUT_EXCEL):
        print(f"Error: File Excel {INPUT_EXCEL} tidak ditemukan. Jalankan Tahap 1 terlebih dahulu.")
        return

    # Muat schema.json sebagai referensi urutan key
    schema_path = "./preprocessing/biaya_pipeline/schema.json"
    if not os.path.exists(schema_path):
        print(f"Error: File {schema_path} tidak ditemukan.")
        return
    with open(schema_path, "r", encoding="utf-8") as f:
        unified_schema = json.load(f)

    df_sem1 = pd.read_excel(INPUT_EXCEL, sheet_name="Sarjana_Sem1")
    df_sem2 = pd.read_excel(INPUT_EXCEL, sheet_name="Sarjana_Sem2")
    df_s2 = pd.read_excel(INPUT_EXCEL, sheet_name="Magister_S2")
    df_rpl = pd.read_excel(INPUT_EXCEL, sheet_name="RPL")

    # ── Deteksi S2_MAJORS secara dinamis dari sheet Magister_S2 ──────────────
    s2_majors_detected = set()
    for val in df_s2["Program Studi"].dropna():
        m = match_major_name(val)
        if m:
            s2_majors_detected.add(m)
    print(f"Prodi S2 terdeteksi: {sorted(s2_majors_detected)}")

    # ── Bangun akreditasi_map secara dinamis dari kolom Akreditasi RPL ────────
    # Forward-fill kolom Akreditasi (merged cells di gambar)
    df_rpl[["Jenjang", "Program Studi", "Akreditasi"]] = (
        df_rpl[["Jenjang", "Program Studi", "Akreditasi"]].ffill()
    )
    akreditasi_map = build_akreditasi_map(df_rpl)
    print(f"Akreditasi terdeteksi dari OCR RPL: {akreditasi_map}")

    # ── Normalisasi label Jenjang untuk groupby ──────────────────────────────
    # OCR menghasilkan variasi: 'Sarjana (sı)', 'Sarjana S1)', 'Sarjana', dsb.
    # Semua varian S1 dinormalisasi menjadi 'S1', S2 menjadi 'S2'.
    def normalize_jenjang(val):
        if pd.isna(val):
            return ""
        v = str(val).lower()
        if "magister" in v or "s2" in v:
            return "S2"
        return "S1"

    df_rpl["Jenjang_Norm"] = df_rpl["Jenjang"].apply(normalize_jenjang)

    # ── Interpolasi biaya RPL per Jenjang (bfill + ffill) ────────────────────
    # bfill terlebih dahulu agar baris-baris di ATAS baris berbiaya juga terisi
    for col in ["Biaya Pendaftaran", "Konversi Per SKS", "Uang Kuliah"]:
        df_rpl[col] = df_rpl[col].replace(0, None)
        df_rpl[col] = (
            df_rpl.groupby("Jenjang_Norm", sort=False)[col]
            .transform(lambda g: g.bfill().ffill())
            .fillna(0)
            .astype(int)
        )

    # ── Build RPL data map ────────────────────────────────────────────────────
    rpl_data_map = {}
    for _, row in df_rpl.iterrows():
        major_match = match_major_name(row["Program Studi"])
        if not major_match:
            continue
        jenjang = str(row["Jenjang"]).lower()
        key = (major_match, "s1" if "s1" in jenjang or "sarjana" in jenjang else "s2")
        rpl_data_map[key] = {
            "biaya_pendaftaran": clean_int(row["Biaya Pendaftaran"]),
            "biaya_konversi_per_sks": clean_int(row["Konversi Per SKS"]),
            "jumlah_uang_kuliah": clean_int(row["Uang Kuliah"])
        }

    # ── Interpolasi UKT S2 jika ada yang kosong (OCR miss) ──────────────────
    df_s2["UKT"] = df_s2["UKT"].replace(0, None)
    df_s2["UKT"] = (
        df_s2.groupby("Program Studi", sort=False)["UKT"]
        .transform(lambda g: g.ffill().bfill())
        .fillna(0)
        .astype(int)
    )
    # Interpolasi SKS Rate S2
    df_s2["SKS Rate"] = df_s2["SKS Rate"].replace(0, None)
    df_s2["SKS Rate"] = (
        df_s2.groupby("Program Studi", sort=False)["SKS Rate"]
        .transform(lambda g: g.ffill().bfill())
        .fillna(0)
        .astype(int)
    )

    # ── Parse data Magister S2 ────────────────────────────────────────────────
    mag_data_map = {}
    for major_name, group in df_s2.groupby("Program Studi", sort=False):
        if not major_name or pd.isna(major_name):
            continue
        major_match = match_major_name(major_name)
        if not major_match:
            continue

        for idx, (_, row) in enumerate(group.iterrows()):
            sem_num = idx + 1
            sem_label = f"semester_{sem_num}"

            sks_count = clean_int(row["Jumlah SKS"])
            ukt = clean_int(row["UKT"])
            biaya_per_sks = clean_int(row["SKS Rate"])
            ukv_total = clean_int(row["UKV Total"])
            # Hitung SKS secara dinamis jika OCR gagal membaca angka kecil
            if sks_count == 0 and biaya_per_sks > 0 and ukv_total > 0:
                sks_count = round(ukv_total / biaya_per_sks)
            total_biaya_semester = clean_int(row["Total Biaya"])
            if total_biaya_semester == 0 and ukt > 0:
                total_biaya_semester = ukt + (sks_count * biaya_per_sks)

            if major_match not in mag_data_map:
                rpl_s2 = rpl_data_map.get((major_match, "s2"))
                if rpl_s2:
                    rpl_s2 = rpl_s2.copy()
                    rpl_s2["keterangan"] = "Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S2"

                mag_data_map[major_match] = {
                    "estimasi_total_hingga_lulus": 0,
                    "rincian_per_semester": {},
                    "jalur_rpl": rpl_s2
                }

            mag_data_map[major_match]["rincian_per_semester"][sem_label] = {
                "ukt": ukt,
                "sks": sks_count,
                "biaya_per_sks": biaya_per_sks,
                "total_biaya_semester": total_biaya_semester,
                "total": total_biaya_semester
            }

    for major_name, data in mag_data_map.items():
        total_val = sum(sem["total_biaya_semester"] for sem in data["rincian_per_semester"].values())
        data["estimasi_total_hingga_lulus"] = total_val

    # ── Parse Sarjana S1 Semester 1 ───────────────────────────────────────────
    sem1_map = {}
    for _, row in df_sem1.iterrows():
        major_match = match_major_name(row["Program Studi"])
        if not major_match:
            continue

        ukt = clean_int(row["UKT"])
        sks_rate = clean_int(row["SKS Rate"])
        sks_total = clean_int(row["SKS Total"])
        praktikum = clean_int(row["Praktikum"])
        total_uk = clean_int(row["Total Uang Kuliah"])
        dpp = clean_int(row["DPP"])

        p1_pot = clean_int(row["PMDK P1 Potongan"])
        p2_pot = clean_int(row["PMDK P2 Potongan"])
        p3_pot = clean_int(row["PMDK P3 Potongan"])

        sks_jumlah = clean_int(row.get("SKS Count"))

        # Validasi matematika: total_uk = ukt + sks_total + praktikum
        if total_uk > 0 and ukt > 0:
            calc_sks_total = total_uk - ukt - praktikum
            if calc_sks_total > 0 and calc_sks_total != sks_total:
                sks_total = calc_sks_total

        # Fallback jika OCR gagal membaca angka kecil
        if sks_jumlah == 0 and sks_rate > 0:
            sks_jumlah = round(sks_total / sks_rate)
        total_biaya_masuk_tes = total_uk + dpp

        sem1_map[major_match] = {
            "ukt": ukt,
            "sks": {
                "jumlah": sks_jumlah,
                "biaya_per_sks": sks_rate,
                "total_biaya_sks": sks_total
            },
            "praktikum": praktikum,
            "total_biaya_semester": total_uk,
            "keterangan": "Biaya ini berlaku untuk semester ganjil awal masuk.",
            "dana_pengembangan_pendidikan_dpp": dpp,
            "simulasi_total_biaya_jalur_tes": total_biaya_masuk_tes,
            "potongan_beasiswa_pmdk": {
                "periode_1": {
                    "keterangan": "Potongan UKT 100%",
                    "potongan": p1_pot,
                    "total_biaya_masuk": total_biaya_masuk_tes - p1_pot
                },
                "periode_2": {
                    "keterangan": "Potongan UKT 50%",
                    "potongan": p2_pot,
                    "total_biaya_masuk": total_biaya_masuk_tes - p2_pot
                },
                "periode_3": {
                    "keterangan": "Potongan UKT 25%",
                    "potongan": p3_pot,
                    "total_biaya_masuk": total_biaya_masuk_tes - p3_pot
                }
            }
        }

    # ── Parse Sarjana S1 Semester 2 ───────────────────────────────────────────
    sem2_map = {}
    for _, row in df_sem2.iterrows():
        major_match = match_major_name(row["Program Studi"])
        if not major_match:
            continue

        ukt = clean_int(row["UKT"])
        sks_rate = clean_int(row["SKS Rate"])
        sks_total = clean_int(row["SKS Total"])
        praktikum = clean_int(row["Praktikum"])
        total_uk = clean_int(row["Total Uang Kuliah"])

        sks_jumlah = clean_int(row.get("SKS Count"))

        if total_uk > 0 and ukt > 0:
            calc_sks_total = total_uk - ukt - praktikum
            if calc_sks_total > 0 and calc_sks_total != sks_total:
                sks_total = calc_sks_total

        # Fallback jika OCR gagal membaca angka kecil
        if sks_jumlah == 0 and sks_rate > 0:
            sks_jumlah = round(sks_total / sks_rate)

        sem2_map[major_match] = {
            "ukt": ukt,
            "sks": {
                "jumlah": sks_jumlah,
                "biaya_per_sks": sks_rate,
                "total_biaya_sks": sks_total
            },
            "praktikum": praktikum,
            "total_biaya_semester": total_uk if total_uk > 0 else (ukt + sks_total + praktikum)
        }

    # ── Satukan dan Simpan ke JSON ────────────────────────────────────────────
    print("\nMenyusun JSON terstruktur dan melakukan rekonsiliasi skema...")
    for major, filename in MAJOR_MAP.items():
        json_path = os.path.join(OUTPUT_DIR, filename)

        s1_sem1 = sem1_map.get(major)
        s1_sem2 = sem2_map.get(major)

        if not s1_sem1:
            print(f"[Warning] Data Semester 1 untuk {major} tidak ditemukan. Melewati.")
            continue

        # Pilih schema sesuai jenjang prodi
        has_s2 = major in s2_majors_detected and major in mag_data_map
        use_s2_style = has_s2  # prodi S1+S2 pakai schema s1_s2

        # Akreditasi: dari OCR RPL
        akreditasi = akreditasi_map.get(major, None)

        # RPL S1
        rpl_s1 = rpl_data_map.get((major, "s1"))
        if rpl_s1:
            rpl_s1 = rpl_s1.copy()
            # Tentukan keterangan RPL berdasarkan apakah prodi juga punya S2
            has_s2 = major in s2_majors_detected and major in mag_data_map
            if has_s2 or use_s2_style:
                rpl_s1["keterangan"] = "Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S1"
            else:
                rpl_s1["keterangan"] = "Jalur Rekognisi Pembelajaran Lampau (RPL)"


        has_s2 = major in s2_majors_detected and major in mag_data_map

        jenjang_list = ["Sarjana (S1)"]
        if has_s2:
            jenjang_list.append("Magister (S2)")

        output_data = {
            "program_studi": major,
            "akreditasi": akreditasi,
            "jenjang_tersedia": jenjang_list,
            "biaya_sarjana_s1": {
                "semester_1_ganjil": s1_sem1,
                "semester_2_genap": s1_sem2 if s1_sem2 else s1_sem1,
                "jalur_rpl": rpl_s1
            },
            "biaya_magister_s2": mag_data_map[major] if has_s2 else None
        }
        output_data = conform_to_schema(output_data, unified_schema)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved: {json_path}")


if __name__ == "__main__":
    main()
