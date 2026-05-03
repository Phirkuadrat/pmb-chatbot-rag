import os
import json
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "./data/structured/")

@tool
def get_admission_path(jalur: str) -> str:
    """Useful ONLY for getting information about admission paths/jalur seleksi (e.g. PMDK, ODT, TKA, UTBK/SNBT, RPL, Magister).
    Use this to answer questions about requirements (syarat), schedule (jadwal), fees, and procedures for a specific admission path.
    Args:
        jalur: The name of the admission path (e.g. 'pmdk', 'odt', 'tka', 'snbt', 'utbk', 'rpl', 'magister')
    Returns:
        JSON string containing the admission path details and source metadata.
    """
    jalur_clean = jalur.lower()
    
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
        "s2": "magister.json"
    }
    
    filename = None
    for key, val in jalur_map.items():
        if key in jalur_clean:
            filename = val
            break
            
    if not filename:
        # Return a list of available paths
        available_paths = [v.replace(".json", "").upper() for v in set(jalur_map.values())]
        return json.dumps({
            "content": f"Sayangnya, asisten tidak menemukan detail untuk '{jalur}'. Namun, Itenas memiliki beberapa jalur penerimaan yaitu: {', '.join(set(available_paths))}. Mohon sebutkan jalur mana yang ingin Kakak tanyakan secara spesifik.",
            "metadata": []
        })

    # Search for the file in the jalur directory
    target_dir = os.path.join(JSON_DATA_DIR, "jalur")
    target_filepath = os.path.join(target_dir, filename)

    if not os.path.exists(target_filepath):
        return json.dumps({
            "content": f"Data jalur '{jalur}' (file: {filename}) tidak ditemukan di sistem database.",
            "metadata": []
        })

    try:
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return json.dumps({
            "content": json.dumps(data, indent=2),
            "metadata": [{
                "document": filename,
                "type": "structured (JSON) - jalur"
            }]
        })
    except Exception as e:
        return json.dumps({
            "content": f"Error membaca data jalur untuk {jalur}: {str(e)}",
            "metadata": []
        })


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
    beasiswa_clean = beasiswa.lower()
    
    target_dir = os.path.join(JSON_DATA_DIR, "beasiswa")
    if not os.path.exists(target_dir):
         return json.dumps({
            "content": "Direktori beasiswa tidak ditemukan di database.",
            "metadata": []
        })

    target_filepath = None
    matched_filename = None
    
    # Find matching filename based on keywords
    for file in os.listdir(target_dir):
        if not file.endswith(".json"):
            continue
            
        filename_lower = file.lower()
        
        # Keyword mapping logic
        if ("kip" in beasiswa_clean or "kartu indonesia pintar" in beasiswa_clean) and "kip" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break
        elif ("jfls" in beasiswa_clean or "jabar" in beasiswa_clean or "future leaders" in beasiswa_clean) and "jfls" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break
        elif "osc" in beasiswa_clean and "osc" in filename_lower:
            # Jika user nanya s1/s2
            if "s2" in beasiswa_clean or "magister" in beasiswa_clean:
                if "s2" in filename_lower:
                    target_filepath = os.path.join(target_dir, file)
                    matched_filename = file
                    break
            else:
                if "s1" in filename_lower:
                    target_filepath = os.path.join(target_dir, file)
                    matched_filename = file
                    break
        elif "bni" in beasiswa_clean and "bni" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break
        elif ("rmp" in beasiswa_clean or "rawan melanjutkan pendidikan" in beasiswa_clean) and "rmp" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break
        elif ("taekwang" in beasiswa_clean or "tkg" in beasiswa_clean) and "taekwang" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break
        elif ("inhealth" in beasiswa_clean or "mandiri" in beasiswa_clean) and "inhealth" in filename_lower:
            target_filepath = os.path.join(target_dir, file)
            matched_filename = file
            break

    # If no specific match, try a generic substring match
    if not target_filepath:
        for file in os.listdir(target_dir):
             if file.endswith(".json") and beasiswa_clean in file.lower():
                 target_filepath = os.path.join(target_dir, file)
                 matched_filename = file
                 break

    if not target_filepath:
        # Return a list of all available scholarships
        all_scholarships = []
        for file in os.listdir(target_dir):
            if file.endswith(".json"):
                all_scholarships.append(file.replace(".json", ""))
                
        return json.dumps({
            "content": f"Berdasarkan catatan, berikut adalah daftar beasiswa yang tersedia di Itenas saat ini: {', '.join(all_scholarships)}. Kakak bisa menanyakan salah satu nama beasiswa tersebut secara spesifik (misalnya: 'Apa syarat beasiswa KIP-K?') untuk info lebih lanjut.",
            "metadata": []
        })

    try:
        with open(target_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return json.dumps({
            "content": json.dumps(data, indent=2),
            "metadata": [{
                "document": matched_filename,
                "type": "structured (JSON) - beasiswa"
            }]
        })
    except Exception as e:
        return json.dumps({
            "content": f"Error membaca data beasiswa untuk {beasiswa}: {str(e)}",
            "metadata": []
        })
