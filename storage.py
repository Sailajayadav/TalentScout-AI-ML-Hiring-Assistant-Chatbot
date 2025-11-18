# storage.py
import json
import os
import hashlib
from datetime import datetime

STORAGE_FILE = "candidates_simulated.json"


def _anon_id(name: str, email: str) -> str:
    return hashlib.sha256((name + "|" + email).encode()).hexdigest()[:16]


def save_candidate(candidate: dict) -> str:
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    anon = _anon_id(candidate["full_name"], candidate["email"])

    record = {
        "id": anon,
        "timestamp": datetime.utcnow().isoformat(),
        "years_experience": candidate.get("years_experience"),
        "desired_positions": candidate.get("desired_positions"),
        "location": candidate.get("location"),
        "tech_stack": candidate.get("tech_stack"),
        "questions": candidate.get("generated_questions"),
    }

    data.append(record)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return anon
