import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
LOG_FILE = os.path.join("data", "logs", "tool_calls_log.jsonl")

def log_tool_call(tool_name: str, args: dict, status: str, detail: str = ""):
    """
    Mencatat penggunaan tool ke dalam file JSONL untuk analisa performa/skripsi.
    status: 'hit', 'miss', 'error'
    """
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "args": args,
            "status": status,
            "detail": detail
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.warning(f"Gagal mencatat log tool call: {e}")
