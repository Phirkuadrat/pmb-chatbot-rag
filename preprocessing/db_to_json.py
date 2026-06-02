import os
import json
import pymysql
from dotenv import load_dotenv

# Load env variables from the workspace root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "pmb_itenas")
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

kegiatan_map_reverse = {
    "0": "Pendaftaran",
    "1": "Ujian",
    "2": "Pengumuman Hasil",
    "3": "Registrasi Ulang"
}

def export_jalur_seleksi():
    conn = get_db_connection()
    target_dir = os.path.join(JSON_DATA_DIR, "jalur")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"Starting export of admission paths to: {target_dir}")
    
    try:
        with conn.cursor() as cursor:
            # 1. Fetch all jalur_seleksi records
            cursor.execute("SELECT * FROM jalur_seleksi")
            jalur_records = cursor.fetchall()
            
            for js in jalur_records:
                jalur_id = js["id"]
                slug = js["slug"]
                
                # Fetch period details
                p_name = None
                p_start = None
                p_end = None
                if js["periode_id"]:
                    cursor.execute("SELECT * FROM periode WHERE id = %s", (js["periode_id"],))
                    p_rec = cursor.fetchone()
                    if p_rec:
                        p_name = p_rec["nama"]
                        p_start = str(p_rec["tanggal_mulai"])
                        p_end = str(p_rec["tanggal_selesai"])
                
                # 2. Fetch persyaratan_umum
                cursor.execute("SELECT persyaratan FROM persyaratan_umum WHERE jalur_id = %s ORDER BY id", (jalur_id,))
                persyaratan = [r["persyaratan"] for r in cursor.fetchall()]
                
                # 3. Fetch cara_pendaftaran
                cursor.execute("SELECT deskripsi FROM cara_pendaftaran WHERE jalur_id = %s ORDER BY id", (jalur_id,))
                cara = [r["deskripsi"] for r in cursor.fetchall()]
                
                # 4. Fetch dokumen_pendaftaran
                cursor.execute("SELECT dokumen FROM dokumen_pendaftaran WHERE jalur_id = %s ORDER BY id", (jalur_id,))
                dokumen = [r["dokumen"] for r in cursor.fetchall()]
                
                # 5. Fetch jadwal_pendaftaran
                cursor.execute("SELECT tanggal_mulai, tanggal_selesai, type FROM jadwal_pendaftaran WHERE jalur_id = %s ORDER BY id", (jalur_id,))
                jadwal = []
                for r in cursor.fetchall():
                    t_end = str(r["tanggal_selesai"]) if r["tanggal_selesai"] else None
                    jadwal.append({
                        "jenis_kegiatan": kegiatan_map_reverse.get(r["type"], "Pendaftaran"),
                        "tanggal_mulai": str(r["tanggal_mulai"]),
                        "tanggal_selesai": t_end
                    })
                
                # Handle specific names matching file expectations
                nama_display = js["nama"]
                if js["nama"] == "MAGISTER":
                    nama_display = "Magister (S2)"
                elif js["nama"] == "TKA":
                    nama_display = "TKA"
                elif js["nama"] == "RPL":
                    nama_display = "RPL"
                elif js["nama"] == "ODT":
                    nama_display = "ODT"
                elif js["nama"] == "PMDK":
                    nama_display = "PMDK"
                elif js["nama"] == "SNBT":
                    nama_display = "SNBT"
                
                res = {
                    "nama_jalur_seleksi": nama_display,
                    "biaya_pendaftaran": js["biaya_daftar"],
                    "deskripsi": js["deskripsi"],
                    "periode": {
                        "nama_periode": p_name,
                        "tanggal_mulai": p_start,
                        "tanggal_selesai": p_end
                    } if p_name else None,
                    "jadwal_pelaksanaan": jadwal,
                    "persyaratan_umum": persyaratan,
                    "tata_cara_pendaftaran": cara,
                    "dokumen_pendaftaran": dokumen,
                    "materi_ujian": None
                }
                
                # Write file
                output_filepath = os.path.join(target_dir, f"{slug}.json")
                with open(output_filepath, "w", encoding="utf-8") as out:
                    json.dump(res, out, indent=2, ensure_ascii=False)
                print(f" -> Exported admission path: {slug} to {os.path.basename(output_filepath)}")
                
    finally:
        conn.close()

def export_beasiswa():
    conn = get_db_connection()
    target_dir = os.path.join(JSON_DATA_DIR, "beasiswa")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"Starting export of scholarships to: {target_dir}")
    
    try:
        with conn.cursor() as cursor:
            # 1. Fetch all beasiswa records
            cursor.execute("SELECT * FROM beasiswa")
            beasiswa_records = cursor.fetchall()
            
            for b in beasiswa_records:
                b_id = b["id"]
                name = b["nama"]
                
                # 2. Fetch syarat
                cursor.execute("SELECT syarat FROM beasiswa_syarat WHERE beasiswa_id = %s ORDER BY id", (b_id,))
                syarat = [r["syarat"] for r in cursor.fetchall()]
                
                # 3. Fetch benefit
                cursor.execute("SELECT benefit FROM beasiswa_benefit WHERE beasiswa_id = %s ORDER BY id", (b_id,))
                benefit = [r["benefit"] for r in cursor.fetchall()]
                
                # 4. Fetch timeline
                cursor.execute("SELECT judul, tanggal_mulai, tanggal_selesai FROM beasiswa_timeline WHERE beasiswa_id = %s ORDER BY id", (b_id,))
                timeline = []
                for r in cursor.fetchall():
                    t_end = str(r["tanggal_selesai"]) if r["tanggal_selesai"] else None
                    timeline.append({
                        "jenis_kegiatan": r["judul"],
                        "tanggal_mulai": str(r["tanggal_mulai"]),
                        "tanggal_selesai": t_end
                    })
                    
                # 5. Fetch tata_cara
                cursor.execute("SELECT tata_cara FROM beasiswa_tata_cara WHERE beasiswa_id = %s ORDER BY id", (b_id,))
                tata_cara = [r["tata_cara"] for r in cursor.fetchall()]
                
                res = {
                    "nama_beasiswa": name,
                    "deskripsi": b["deskripsi"],
                    "periode_awal": str(b["periode_awal"]),
                    "periode_akhir": str(b["periode_akhir"]),
                    "batas_pendaftaran": str(b["batas_daftar"]),
                    "jenis_beasiswa": "Full" if str(b["jenis"]) == "0" else "Partial",
                    "kategori_beasiswa": "External" if str(b["kategori"]) == "1" else "Internal",
                    "persyaratan_umum": syarat,
                    "benefit": benefit,
                    "timeline_beasiswa": timeline,
                    "tata_cara_pendaftaran": tata_cara if tata_cara else None
                }
                
                # Write file (using scholarship name as file name)
                output_filepath = os.path.join(target_dir, f"{name}.json")
                with open(output_filepath, "w", encoding="utf-8") as out:
                    json.dump(res, out, indent=2, ensure_ascii=False)
                print(f" -> Exported scholarship: {name} to {os.path.basename(output_filepath)}")
                
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== START DATABASE EXPORT ===")
    export_jalur_seleksi()
    print()
    export_beasiswa()
    print("=== EXPORT COMPLETED ===")
