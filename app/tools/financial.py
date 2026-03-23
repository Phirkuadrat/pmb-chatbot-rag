import os
import json
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")

@tool
def get_tuition_fee(major: str) -> str:
    """Useful ONLY for getting tuition fee (biaya/UKT) information for a specific major/jurusan.
    Args:
        major: The name of the major (e.g. 'informatika', 'elektro', 'desain komunikasi visual', 'dkv')
    Returns:
        JSON string containing the tuition fees and source metadata.
    """
    major_clean = major.lower()
    
    # Map synonyms to actual JSON filenames
    major_map = {
        "elektro": "teknik_elektro.json",
        "mesin": "teknik_mesin.json",
        "industri": "teknik_industri.json",
        "kimia": "teknik_kimia.json",
        "informatika": "informatika.json",
        "sistem informasi": "sistem_informasi.json",
        "sipil": "teknik_sipil.json",
        "geodesi": "teknik_geodesi.json",
        "perencanaan wilayah": "perencanaan_wilayah_dan_kota.json",
        "pwk": "perencanaan_wilayah_dan_kota.json",
        "lingkungan": "teknik_lingkungan.json",
        "arsitektur": "arsitektur.json",
        "interior": "desain_interior.json",
        "produk": "desain_produk.json",
        "komunikasi visual": "desain_komunikasi_visual.json",
        "dkv": "desain_komunikasi_visual.json"
    }
    
    filename = None
    for key, val in major_map.items():
        if key in major_clean:
            filename = val
            break
            
    if not filename:
        return json.dumps({
            "content": f"Sayangnya, asisten saat ini belum memiliki pemetaan file biaya untuk jurusan '{major}'.",
            "metadata": []
        })

    # Cari file JSON secara rekursif di seluruh sub-folder kategori
    target_filepath = None
    for root, dirs, files in os.walk(JSON_DATA_DIR):
        if filename in files:
            target_filepath = os.path.join(root, filename)
            break

    if not target_filepath:
        return json.dumps({
            "content": f"Data untuk jurusan '{major}' (file: {filename}) tidak ditemukan di sistem/database. Silakan cek UI Kelola Data.",
            "metadata": []
        })

    try:
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return json.dumps({
            "content": json.dumps(data, indent=2),
            "metadata": [{
                "document": filename,
                "type": f"structured (JSON) - {os.path.basename(os.path.dirname(target_filepath))}"
            }]
        })
    except Exception as e:
        return json.dumps({
            "content": f"Error membaca data biaya untuk {major} di sistem: {str(e)}",
            "metadata": []
        })
