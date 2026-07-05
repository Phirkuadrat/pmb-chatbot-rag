import os
import json
import difflib
from langchain_core.tools import tool
from dotenv import load_dotenv
from app.utils.formatters import format_all_rupiah_in_dict
from app.utils.logger import log_tool_call

load_dotenv()
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")

# Module-level cache for directory scan
_file_cache = None


def _get_file_cache():
    global _file_cache
    if _file_cache is None:
        _file_cache = {}
        for root, dirs, files in os.walk(JSON_DATA_DIR):
            for file in files:
                if file.endswith(".json"):
                    _file_cache[file] = os.path.join(root, file)
    return _file_cache


@tool
def get_tuition_fee(major: str) -> str:
    """Useful ONLY for getting tuition fee (biaya/UKT) information for a specific major/jurusan.
    Args:
        major: The name of the major (e.g. 'informatika', 'elektro', 'desain komunikasi visual', 'dkv')
    Returns:
        JSON string containing the tuition fees and source metadata.
    """
    major_clean = major.lower().strip()

    # Comprehensive Synonym Map
    major_map = {
        "elektro": "teknik_elektro.json",
        "teknik elektro": "teknik_elektro.json",
        "mesin": "teknik_mesin.json",
        "teknik mesin": "teknik_mesin.json",
        "industri": "teknik_industri.json",
        "teknik industri": "teknik_industri.json",
        "kimia": "teknik_kimia.json",
        "teknik kimia": "teknik_kimia.json",
        "informatika": "informatika.json",
        "if": "informatika.json",
        "sistem informasi": "sistem_informasi.json",
        "si": "sistem_informasi.json",
        "sipil": "teknik_sipil.json",
        "teknik sipil": "teknik_sipil.json",
        "geodesi": "teknik_geodesi.json",
        "teknik geodesi": "teknik_geodesi.json",
        "geomatika": "teknik_geodesi.json",
        "teknik geomatika": "teknik_geodesi.json",
        "perencanaan wilayah": "perencanaan_wilayah_dan_kota.json",
        "perencanaan wilayah dan kota": "perencanaan_wilayah_dan_kota.json",
        "pwk": "perencanaan_wilayah_dan_kota.json",
        "planologi": "perencanaan_wilayah_dan_kota.json",
        "lingkungan": "teknik_lingkungan.json",
        "teknik lingkungan": "teknik_lingkungan.json",
        "arsitektur": "arsitektur.json",
        "interior": "desain_interior.json",
        "desain interior": "desain_interior.json",
        "produk": "desain_produk.json",
        "desain produk": "desain_produk.json",
        "komunikasi visual": "desain_komunikasi_visual.json",
        "desain komunikasi visual": "desain_komunikasi_visual.json",
        "dkv": "desain_komunikasi_visual.json",
    }

    filename = None

    # Pemetaan sinonim program studi
    if major_clean in major_map:
        filename = major_map[major_clean]

    # Substring matching but with word boundaries to prevent 'si' matching 'komunikasi'
    if not filename:
        import re

        for key, val in major_map.items():
            # Check if key is a whole word in major_clean
            if re.search(r"\b" + re.escape(key) + r"\b", major_clean):
                filename = val
                break

    # Fuzzy match fallback
    if not filename:
        matches = difflib.get_close_matches(
            major_clean, major_map.keys(), n=1, cutoff=0.6
        )
        if matches:
            filename = major_map[matches[0]]

    if not filename:
        log_tool_call("get_tuition_fee", {"major": major}, "miss", "Synonym not found")
        return json.dumps(
            {
                "content": f"Sayangnya, asisten saat ini belum memiliki pemetaan file biaya untuk jurusan '{major}'.",
                "metadata": [],
            }
        )

    # Gunakan cache os.walk()
    file_cache = _get_file_cache()
    target_filepath = file_cache.get(filename)

    if not target_filepath:
        log_tool_call(
            "get_tuition_fee",
            {"major": major},
            "error",
            f"File {filename} missing from disk",
        )
        return json.dumps(
            {
                "content": f"Data untuk jurusan '{major}' (file: {filename}) tidak ditemukan di sistem/database. Silakan cek UI Kelola Data.",
                "metadata": [],
            }
        )

    try:
        # Membaca data JSON
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Format semua angka integer menjadi Rupiah
        data = format_all_rupiah_in_dict(data)

        log_tool_call(
            "get_tuition_fee", {"major": major}, "hit", f"Mapped to {filename}"
        )

        # Mengembalikan hasil JSON
        return json.dumps(
            {
                "content": json.dumps(data, indent=2),
                "metadata": [
                    {
                        "document": filename,
                        "type": f"structured (JSON) - {os.path.basename(os.path.dirname(target_filepath))}",
                    }
                ],
            }
        )
    except Exception as e:
        log_tool_call("get_tuition_fee", {"major": major}, "error", str(e))
        return json.dumps(
            {
                "content": f"Error membaca data biaya untuk {major} di sistem: {str(e)}",
                "metadata": [],
            }
        )
