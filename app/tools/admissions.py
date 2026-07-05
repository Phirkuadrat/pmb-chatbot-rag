import os
import json
import difflib
from langchain_core.tools import tool
from dotenv import load_dotenv
from app.utils.formatters import format_all_rupiah_in_dict
from app.utils.logger import log_tool_call

load_dotenv()
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")

# Module-level cache for directory listing
_jalur_files = []
_beasiswa_files = []


def _init_caches():
    global _jalur_files, _beasiswa_files
    if not _jalur_files:
        p = os.path.join(JSON_DATA_DIR, "jalur")
        if os.path.exists(p):
            _jalur_files = [f for f in os.listdir(p) if f.endswith(".json")]
    if not _beasiswa_files:
        p = os.path.join(JSON_DATA_DIR, "beasiswa")
        if os.path.exists(p):
            _beasiswa_files = [f for f in os.listdir(p) if f.endswith(".json")]


@tool
def get_admission_path(jalur: str) -> str:
    """Useful for getting information about Itenas admission paths/jalur masuk/jalur penerimaan/jalur seleksi.
    Use this when the user asks:
    - What admission paths are available at Itenas? ('ada jalur masuk apa saja?', 'jalur seleksi apa yang ada?')
    - About a specific admission path: PMDK, ODT (One Day Test), TKA, UTBK/SNBT, RPL, Magister.
    - Requirements (syarat), schedule (jadwal), procedures for any admission path.
    When the user asks for a general list, pass 'semua' or 'list' as the jalur argument.
    Args:
        jalur: The name of the admission path (e.g. 'pmdk', 'odt', 'tka', 'snbt', 'utbk', 'rpl', 'magister', 'semua')
    Returns:
        JSON string containing the admission path details and source metadata.
    """
    _init_caches()
    jalur_clean = jalur.lower().strip()

    # Jika user bertanya daftar umum semua jalur
    if any(
        kw in jalur_clean
        for kw in ["semua", "list", "semua jalur", "apa saja", "ada apa"]
    ):
        available_paths = [f.replace(".json", "").upper() for f in _jalur_files]
        content = f"Itenas saat ini membuka penerimaan melalui jalur-jalur berikut:\n"
        for idx, p in enumerate(available_paths, 1):
            content += f"{idx}. **{p}**\n"
        content += "\nKakak bisa tanyakan detail syarat, jadwal, atau biaya dari masing-masing jalur tersebut ya!"

        log_tool_call(
            "get_admission_path", {"jalur": jalur}, "hit", "Daftar semua jalur"
        )
        return json.dumps(
            {
                "content": content,
                "metadata": [
                    {
                        "document": "admissions_paths_list",
                        "type": "structured (JSON) - jalur",
                    }
                ],
            }
        )

    # Map common synonyms to actual JSON filenames
    jalur_map = {
        "pmdk": "pmdk.json",
        "odt": "odt.json",
        "one day test": "odt.json",
        "tka": "tka.json",
        "tes kemampuan akademik": "tka.json",
        "snbt": "snbt.json",
        "utbk": "snbt.json",
        "rpl": "rpl.json",
        "rekognisi pembelajaran lampau": "rpl.json",
        "magister": "magister.json",
        "s2": "magister.json",
    }

    filename = None
    for key, val in jalur_map.items():
        if key in jalur_clean or jalur_clean in key:
            filename = val
            break

    if not filename:
        matches = difflib.get_close_matches(
            jalur_clean, jalur_map.keys(), n=1, cutoff=0.6
        )
        if matches:
            filename = jalur_map[matches[0]]

    if not filename:
        available_paths = [
            v.replace(".json", "").upper() for v in set(jalur_map.values())
        ]
        log_tool_call(
            "get_admission_path", {"jalur": jalur}, "miss", "Synonym not found"
        )
        return json.dumps(
            {
                "content": f"Sayangnya, asisten tidak menemukan detail untuk '{jalur}'. Namun, Itenas memiliki beberapa jalur penerimaan yaitu: {', '.join(set(available_paths))}. Mohon sebutkan jalur mana yang ingin Kakak tanyakan secara spesifik.",
                "metadata": [],
            }
        )

    target_filepath = os.path.join(JSON_DATA_DIR, "jalur", filename)

    if not os.path.exists(target_filepath):
        log_tool_call(
            "get_admission_path", {"jalur": jalur}, "error", f"File {filename} missing"
        )
        return json.dumps(
            {
                "content": f"Data jalur '{jalur}' (file: {filename}) tidak ditemukan di database.",
                "metadata": [],
            }
        )

    try:
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        data = format_all_rupiah_in_dict(data)

        log_tool_call(
            "get_admission_path", {"jalur": jalur}, "hit", f"Mapped to {filename}"
        )
        return json.dumps(
            {
                "content": json.dumps(data, indent=2),
                "metadata": [
                    {"document": filename, "type": "structured (JSON) - jalur"}
                ],
            }
        )
    except Exception as e:
        log_tool_call("get_admission_path", {"jalur": jalur}, "error", str(e))
        return json.dumps(
            {
                "content": f"Error membaca data jalur untuk {jalur}: {str(e)}",
                "metadata": [],
            }
        )


@tool
def get_scholarship_info(beasiswa: str) -> str:
    """Useful ONLY for getting information about scholarships/beasiswa.
    Use this to answer questions about scholarship requirements, benefits, schedule, and procedures.
    If the user asks for a general list of available scholarships (e.g. "ada beasiswa apa saja?"), you MUST use this tool and pass 'umum' or 'semua' as the beasiswa argument.
    Args:
        beasiswa: The name or keyword of the scholarship (e.g. 'kip', 'jfls', 'osc', 'rmp', 'umum', 'semua').
    Returns:
        JSON string containing the scholarship details and source metadata.
    """
    _init_caches()
    beasiswa_clean = beasiswa.lower().strip()
    target_dir = os.path.join(JSON_DATA_DIR, "beasiswa")

    if any(kw in beasiswa_clean for kw in ["semua", "umum", "apa saja", "list"]):
        all_scholarships = [f.replace(".json", "") for f in _beasiswa_files]
        log_tool_call(
            "get_scholarship_info", {"beasiswa": beasiswa}, "hit", "Daftar beasiswa"
        )
        return json.dumps(
            {
                "content": f"Berikut adalah beasiswa yang tersedia di Itenas saat ini: {', '.join(all_scholarships)}. Kakak bisa menanyakan spesifik (misal: 'Apa syarat beasiswa KIP-K?').",
                "metadata": [],
            }
        )

    matched_filename = None

    # 1. Rules-based matching
    for file in _beasiswa_files:
        filename_lower = file.lower()
        if (
            "kip" in beasiswa_clean or "kartu indonesia pintar" in beasiswa_clean
        ) and "kip" in filename_lower:
            matched_filename = file
            break
        elif (
            "jfls" in beasiswa_clean or "jabar" in beasiswa_clean
        ) and "jfls" in filename_lower:
            matched_filename = file
            break
        elif "osc" in beasiswa_clean and "osc" in filename_lower:
            if "s2" in beasiswa_clean or "magister" in beasiswa_clean:
                if "s2" in filename_lower:
                    matched_filename = file
                    break
            else:
                if "s1" in filename_lower:
                    matched_filename = file
                    break
        elif "bni" in beasiswa_clean and "bni" in filename_lower:
            matched_filename = file
            break
        elif (
            "rmp" in beasiswa_clean or "rawan" in beasiswa_clean
        ) and "rmp" in filename_lower:
            matched_filename = file
            break
        elif (
            "taekwang" in beasiswa_clean or "tkg" in beasiswa_clean
        ) and "taekwang" in filename_lower:
            matched_filename = file
            break
        elif (
            "inhealth" in beasiswa_clean or "mandiri" in beasiswa_clean
        ) and "inhealth" in filename_lower:
            matched_filename = file
            break

    # 2. Substring matching
    if not matched_filename:
        for file in _beasiswa_files:
            if (
                beasiswa_clean in file.lower()
                or file.replace(".json", "").lower() in beasiswa_clean
            ):
                matched_filename = file
                break

    # 3. Fuzzy matching
    if not matched_filename:
        base_names = [f.replace(".json", "").lower() for f in _beasiswa_files]
        matches = difflib.get_close_matches(beasiswa_clean, base_names, n=1, cutoff=0.5)
        if matches:
            matched_filename = matches[0] + ".json"

    if not matched_filename:
        all_scholarships = [f.replace(".json", "") for f in _beasiswa_files]
        log_tool_call(
            "get_scholarship_info",
            {"beasiswa": beasiswa},
            "miss",
            "Keyword not matched",
        )
        return json.dumps(
            {
                "content": f"Berdasarkan catatan, berikut adalah beasiswa yang tersedia di Itenas saat ini: {', '.join(all_scholarships)}.",
                "metadata": [],
            }
        )

    target_filepath = os.path.join(target_dir, matched_filename)
    try:
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        data = format_all_rupiah_in_dict(data)

        log_tool_call(
            "get_scholarship_info",
            {"beasiswa": beasiswa},
            "hit",
            f"Mapped to {matched_filename}",
        )
        return json.dumps(
            {
                "content": json.dumps(data, indent=2),
                "metadata": [
                    {
                        "document": matched_filename,
                        "type": "structured (JSON) - beasiswa",
                    }
                ],
            }
        )
    except Exception as e:
        log_tool_call("get_scholarship_info", {"beasiswa": beasiswa}, "error", str(e))
        return json.dumps(
            {
                "content": f"Error membaca data beasiswa untuk {beasiswa}: {str(e)}",
                "metadata": [],
            }
        )


@tool
def search_admission_requirements(keyword: str) -> str:
    """Useful for searching specific requirements (persyaratan, buta warna, umur, dokumen, rapor, dll) across ALL admission paths.
    Use this when the user asks a general requirement question but does not specify which admission path (jalur).
    Args:
        keyword: The specific requirement keyword to search for (e.g. 'buta warna', 'rapor', 'dokumen').
    Returns:
        JSON string containing the matching requirements grouped by admission path.
    """
    _init_caches()
    keyword_clean = keyword.lower().strip()

    results = {}
    for filename in _jalur_files:
        filepath = os.path.join(JSON_DATA_DIR, "jalur", filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            path_name = data.get(
                "nama_jalur_seleksi", filename.replace(".json", "").upper()
            )
            matches = []

            if "persyaratan_umum" in data and isinstance(
                data["persyaratan_umum"], list
            ):
                for req in data["persyaratan_umum"]:
                    if keyword_clean in req.lower():
                        matches.append(f"[Syarat Umum] {req}")

            if "dokumen_pendaftaran" in data and isinstance(
                data["dokumen_pendaftaran"], list
            ):
                for doc in data["dokumen_pendaftaran"]:
                    if keyword_clean in doc.lower():
                        matches.append(f"[Dokumen] {doc}")

            if "tata_cara_pendaftaran" in data and isinstance(
                data["tata_cara_pendaftaran"], list
            ):
                for tata in data["tata_cara_pendaftaran"]:
                    if keyword_clean in tata.lower():
                        matches.append(f"[Tata Cara] {tata}")

            if matches:
                results[path_name] = matches
        except Exception:
            pass

    if not results:
        log_tool_call(
            "search_admission_requirements",
            {"keyword": keyword},
            "miss",
            "Keyword not found in any path",
        )
        return json.dumps(
            {
                "content": f"Tidak ditemukan persyaratan terkait '{keyword}' di jalur masuk manapun.",
                "metadata": [],
            }
        )

    log_tool_call(
        "search_admission_requirements",
        {"keyword": keyword},
        "hit",
        f"Found in {len(results)} paths",
    )

    output_lines = [
        f"Berikut adalah persyaratan terkait '{keyword}' di berbagai jalur masuk:"
    ]
    for path, matches in results.items():
        output_lines.append(f"\n**Jalur {path}**:")
        for m in matches:
            output_lines.append(f"- {m}")

    return json.dumps(
        {
            "content": "\n".join(output_lines),
            "metadata": [
                {
                    "document": "all_admission_paths",
                    "type": "structured (JSON) - global search",
                }
            ],
        }
    )
