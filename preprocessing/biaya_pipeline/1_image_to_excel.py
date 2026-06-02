import os
import pandas as pd
import easyocr

IMAGE_DIR = "./preprocessing/Biaya Pendidikan"
OUTPUT_EXCEL = "./preprocessing/biaya_pipeline/biaya_pendidikan_full_ocr.xlsx"
os.makedirs(os.path.dirname(OUTPUT_EXCEL), exist_ok=True)

# Pemetaan nama program studi ke nama file JSON
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

S2_MAJORS = ["Teknik Mesin", "Teknik Industri", "Teknik Sipil"]


def clean_int(val):
    if not val:
        return 0
    val_clean = str(val).lower()
    val_clean = val_clean.replace("o", "0").replace("q", "0").replace("i", "1").replace("l", "1").replace("s", "5")
    val_digits = "".join([c for c in val_clean if c.isdigit()])
    return int(val_digits) if val_digits else 0


def match_major_name(text):
    text_clean = text.lower().strip()
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


def group_by_rows(ocr_results, y_threshold=15):
    sorted_by_y = sorted(ocr_results, key=lambda x: (x[0][0][1] + x[0][2][1]) / 2)
    
    rows = []
    current_row = []
    current_y_sum = 0
    
    for box, text, prob in sorted_by_y:
        y_center = (box[0][1] + box[2][1]) / 2
        x_center = (box[0][0] + box[1][0]) / 2
        
        if not current_row:
            current_row = [(box, text, prob, x_center, y_center)]
            current_y_sum = y_center
        else:
            avg_y = current_y_sum / len(current_row)
            if abs(y_center - avg_y) <= y_threshold:
                current_row.append((box, text, prob, x_center, y_center))
                current_y_sum += y_center
            else:
                current_row = sorted(current_row, key=lambda item: item[3])
                rows.append(current_row)
                current_row = [(box, text, prob, x_center, y_center)]
                current_y_sum = y_center
                
    if current_row:
        current_row = sorted(current_row, key=lambda item: item[3])
        rows.append(current_row)
        
    return rows


def parse_sarjana_sem1(rows):
    merged_rows = []
    for r in rows:
        if not r:
            continue
        if len(r) == 1 and r[0][3] < 200:
            if merged_rows:
                prev_row = merged_rows[-1]
                merged_ok = False
                for idx, item in enumerate(prev_row):
                    if item[3] < 200:
                        prev_row[idx] = (item[0], item[1] + " " + r[0][1], item[2], item[3], item[4])
                        merged_ok = True
                        break
                if merged_ok:
                    continue
        merged_rows.append(r)

    excel_rows = []
    for r in merged_rows:
        major_col_texts = [item[1] for item in r if item[3] < 200]
        if not major_col_texts:
            continue
        combined_major = " ".join(major_col_texts)
        
        if any(kw in combined_major.lower() for kw in ["program", "studi", "no", "biaya"]):
            continue
            
        ukt = 0
        sks_count = 0
        sks_rate = 0
        sks_total = 0
        praktikum = 0
        total_uk = 0
        dpp = 0
        p1_pot = 0
        p1_tot = 0
        p2_pot = 0
        p2_tot = 0
        p3_pot = 0
        p3_tot = 0
        
        for item in r:
            x = item[3]
            val = item[1]
            
            if 200 <= x < 320:
                ukt = clean_int(val)
            elif 320 <= x < 400:
                sks_count = clean_int(val)
            elif 400 <= x < 500:
                sks_rate = clean_int(val)
            elif 500 <= x < 620:
                sks_total = clean_int(val)
            elif 620 <= x < 740:
                praktikum = clean_int(val)
            elif 740 <= x < 850:
                total_uk = clean_int(val)
            elif 850 <= x < 960:
                dpp = clean_int(val)
            elif 1090 <= x < 1190:
                p1_pot = clean_int(val)
            elif 1190 <= x < 1310:
                p1_tot = clean_int(val)
            elif 1310 <= x < 1400:
                p2_pot = clean_int(val)
            elif 1400 <= x < 1530:
                p2_tot = clean_int(val)
            elif 1530 <= x < 1620:
                p3_pot = clean_int(val)
            elif 1620 <= x < 1750:
                p3_tot = clean_int(val)
                
        if ukt == 0 and sks_rate == 0 and total_uk == 0:
            continue

        excel_rows.append({
            "Program Studi": combined_major.strip(),
            "UKT": ukt,
            "SKS Count": sks_count,
            "SKS Rate": sks_rate,
            "SKS Total": sks_total,
            "Praktikum": praktikum,
            "Total Uang Kuliah": total_uk,
            "DPP": dpp,
            "PMDK P1 Potongan": p1_pot,
            "PMDK P1 Total": p1_tot,
            "PMDK P2 Potongan": p2_pot,
            "PMDK P2 Total": p2_tot,
            "PMDK P3 Potongan": p3_pot,
            "PMDK P3 Total": p3_tot
        })
        
    return excel_rows


def parse_sarjana_sem2(rows):
    merged_rows = []
    for r in rows:
        if not r:
            continue
        if len(r) == 1 and r[0][3] < 200:
            if merged_rows:
                prev_row = merged_rows[-1]
                merged_ok = False
                for idx, item in enumerate(prev_row):
                    if item[3] < 200:
                        prev_row[idx] = (item[0], item[1] + " " + r[0][1], item[2], item[3], item[4])
                        merged_ok = True
                        break
                if merged_ok:
                    continue
        merged_rows.append(r)

    excel_rows = []
    for r in merged_rows:
        major_col_texts = [item[1] for item in r if item[3] < 200]
        if not major_col_texts:
            continue
        combined_major = " ".join(major_col_texts)
        
        if any(kw in combined_major.lower() for kw in ["program", "studi", "no", "biaya"]):
            continue
            
        ukt = 0
        sks_count = 0
        sks_rate = 0
        sks_total = 0
        praktikum = 0
        total_uk = 0
        
        for item in r:
            x = item[3]
            val = item[1]
            
            if 200 <= x < 320:
                ukt = clean_int(val)
            elif 320 <= x < 400:
                sks_count = clean_int(val)
            elif 400 <= x < 500:
                sks_rate = clean_int(val)
            elif 500 <= x < 620:
                sks_total = clean_int(val)
            elif 620 <= x < 740:
                praktikum = clean_int(val)
            elif 740 <= x < 850:
                total_uk = clean_int(val)
                
        if ukt == 0 and sks_rate == 0 and total_uk == 0:
            continue

        excel_rows.append({
            "Program Studi": combined_major.strip(),
            "UKT": ukt,
            "SKS Count": sks_count,
            "SKS Rate": sks_rate,
            "SKS Total": sks_total,
            "Praktikum": praktikum,
            "Total Uang Kuliah": total_uk
        })
        
    return excel_rows


def parse_magister_s2(rows, majors_y):
    skip_keywords = ["total", "sks", "studi", "kuliah", "biaya", "no", "program", "tetap", "jumlah", "variabel", "ukv"]
    
    excel_rows = []
    for r in rows:
        if not r:
            continue
            
        is_skip = False
        for item in r:
            if any(kw in item[1].lower() for kw in skip_keywords):
                is_skip = True
                break
        if is_skip:
            continue
            
        y_row = sum(item[4] for item in r) / len(r)
        
        closest_major = None
        if majors_y:
            closest_major = min(majors_y, key=lambda item: abs(item[1] - y_row))[0]
            
        sem_label = ""
        ukt = 0
        sks_count = 0
        sks_rate = 0
        ukv_total = 0
        total_biaya = 0
        
        for item in r:
            x = item[3]
            val = item[1]
            
            if 200 <= x < 300:
                sem_label = val.strip()
            elif 300 <= x < 450:
                ukt = clean_int(val)
            elif 450 <= x < 520:
                sks_count = clean_int(val)
            elif 520 <= x < 630:
                sks_rate = clean_int(val)
            elif 630 <= x < 740:
                ukv_total = clean_int(val)
            elif 740 <= x < 880:
                total_biaya = clean_int(val)
                
        if ukt == 0 and total_biaya == 0:
            continue
            
        # Hitung jumlah SKS secara dinamis dari Uang Kuliah Variabel (UKV) / SKS Rate
        # untuk menghindari angka 0 di Excel akibat OCR yang gagal mendeteksi angka kecil
        if sks_count == 0 and sks_rate > 0:
            sks_count = round(ukv_total / sks_rate)
            
        excel_rows.append({
            "Program Studi": closest_major if closest_major else "",
            "Semester": sem_label,
            "UKT": ukt,
            "Jumlah SKS": sks_count,
            "SKS Rate": sks_rate,
            "UKV Total": ukv_total,
            "Total Biaya": total_biaya
        })
        
    return excel_rows


def parse_rpl(rows):
    """
    Parse RPL table dari image.
    
    Strategi:
    - Simpan SEMUA baris yang memiliki nama program studi (combined_major),
      meskipun kolom biaya bernilai 0 (karena merged cells di gambar).
    - Baris yang hanya punya biaya (tanpa nama major) digunakan untuk
      melengkapi baris sebelumnya yang punya major tapi belum dapat biaya.
    - Nama multi-baris (mis. 'Perencanaan Wilayah' + 'dan Kota') digabung
      ke baris sebelumnya.
    - Stage 2 akan mengisi 0-value biaya via ffill/bfill per Jenjang.
    """
    excel_rows = []
    for r in rows:
        if not r:
            continue

        jenjang_texts = [item[1] for item in r if 50 <= item[3] < 180]
        jenjang = " ".join(jenjang_texts).strip()

        # Lewati header baris
        if any(kw in jenjang.lower() for kw in ["jenjang", "no", "biaya", "pendidikan"]):
            continue

        major_texts = [item[1] for item in r if 180 <= item[3] < 380]
        combined_major = " ".join(major_texts).strip()

        akreditasi_texts = [item[1] for item in r if 380 <= item[3] < 500]
        akreditasi = " ".join(akreditasi_texts).strip()

        pendaftaran = 0
        konversi_sks = 0
        uang_kuliah = 0

        for item in r:
            x = item[3]
            val = item[1]

            if 500 <= x < 620:
                pendaftaran = clean_int(val)
            elif 620 <= x < 750:
                konversi_sks = clean_int(val)
            elif 750 <= x < 900:
                uang_kuliah = clean_int(val)

        # Kasus 1: Baris lanjutan nama prodi (mis. 'dan Kota', 'Visual')
        # tidak punya jenjang dan tidak punya biaya, tapi punya combined_major
        if not jenjang and not pendaftaran and not uang_kuliah and combined_major:
            # Gabungkan ke baris sebelumnya
            if excel_rows:
                excel_rows[-1]["Program Studi"] = (
                    excel_rows[-1]["Program Studi"] + " " + combined_major
                ).strip()
            continue

        # Kasus 2: Baris yang hanya punya biaya tanpa nama prodi (orphan biaya row)
        # Terjadi karena merged cell di kolom Jenjang — biaya muncul di baris kedua
        if not combined_major and (pendaftaran > 0 or uang_kuliah > 0):
            if excel_rows:
                # Pasangkan ke baris terakhir yang belum punya biaya
                last = excel_rows[-1]
                if last["Biaya Pendaftaran"] == 0:
                    last["Biaya Pendaftaran"] = pendaftaran
                    last["Konversi Per SKS"] = konversi_sks
                    last["Uang Kuliah"] = uang_kuliah
            continue

        # Kasus 3: Baris normal (punya jenjang dan/atau major)
        # Simpan bahkan jika biaya=0 (akan diisi ffill/bfill di Stage 2)
        if not jenjang and not combined_major:
            continue  # Benar-benar kosong, lewati

        excel_rows.append({
            "Jenjang": jenjang,
            "Program Studi": combined_major,
            "Akreditasi": akreditasi,
            "Biaya Pendaftaran": pendaftaran,
            "Konversi Per SKS": konversi_sks,
            "Uang Kuliah": uang_kuliah
        })

    return excel_rows


def main():
    print("Membaca model EasyOCR...")
    reader = easyocr.Reader(['id', 'en'], verbose=False)
    
    sem1_img = os.path.join(IMAGE_DIR, "BIAYA_PENDIDIKAN_Biaya Pendidikan Sarjana_LOKMK0.png")
    print(f"Memproses OCR {sem1_img}...")
    sem1_ocr = reader.readtext(sem1_img)
    sem1_rows = group_by_rows(sem1_ocr, y_threshold=15)
    sem1_data = parse_sarjana_sem1(sem1_rows)
    print(f"Mendapatkan {len(sem1_data)} baris data Sarjana Sem 1.")
    
    sem2_img = os.path.join(IMAGE_DIR, "BIAYA_PENDIDIKAN_Biaya Pendidikan Sarjana_QX0WJ0.png")
    print(f"Memproses OCR {sem2_img}...")
    sem2_ocr = reader.readtext(sem2_img)
    sem2_rows = group_by_rows(sem2_ocr, y_threshold=15)
    sem2_data = parse_sarjana_sem2(sem2_rows)
    print(f"Mendapatkan {len(sem2_data)} baris data Sarjana Sem 2.")
    
    mag_img = os.path.join(IMAGE_DIR, "BIAYA_PENDIDIKAN_Biaya Pendidikan Magister_92ZJT7.png")
    print(f"Memproses OCR {mag_img}...")
    mag_ocr = reader.readtext(mag_img)
    
    # Cari nama prodi Magister S2 dan Y koordinatnya di image
    s2_majors_in_image = []
    for box, text, prob in mag_ocr:
        x_center = (box[0][0] + box[1][0]) / 2
        y_center = (box[0][1] + box[2][1]) / 2
        if x_center < 200:
            major = match_major_name(text)
            if major and major in S2_MAJORS:
                s2_majors_in_image.append((major, y_center))
                
    mag_rows = group_by_rows(mag_ocr, y_threshold=15)
    mag_data = parse_magister_s2(mag_rows, s2_majors_in_image)
    print(f"Mendapatkan {len(mag_data)} baris data Magister S2.")
    
    rpl_img = os.path.join(IMAGE_DIR, "BIAYA_PENDIDIKAN_Biaya Pendidikan RPL_9Z5XY0.png")
    print(f"Memproses OCR {rpl_img}...")
    rpl_ocr = reader.readtext(rpl_img)
    rpl_rows = group_by_rows(rpl_ocr, y_threshold=15)
    rpl_data = parse_rpl(rpl_rows)
    print(f"Mendapatkan {len(rpl_data)} baris data RPL.")
    
    print(f"\nMenyimpan hasil ke Excel: {OUTPUT_EXCEL}...")
    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
        pd.DataFrame(sem1_data).to_excel(writer, sheet_name="Sarjana_Sem1", index=False)
        pd.DataFrame(sem2_data).to_excel(writer, sheet_name="Sarjana_Sem2", index=False)
        pd.DataFrame(mag_data).to_excel(writer, sheet_name="Magister_S2", index=False)
        pd.DataFrame(rpl_data).to_excel(writer, sheet_name="RPL", index=False)
        
    print("Tahap 1 selesai!")


if __name__ == "__main__":
    main()
