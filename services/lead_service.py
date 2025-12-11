# services/lead_service.py

import json
from datetime import datetime

LEAD_DB = "lead_db.json"


def _load_db():
    """Load local DB file."""
    try:
        with open(LEAD_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def _save_db(data):
    """Save list to DB file."""
    with open(LEAD_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_lead(username: str, comment: str, reply: str, keyword_group: str):
    """
    Save lead to local DB + Google Sheet (optional).
    """
    lead = {
        "username": username,
        "comment": comment,
        "reply": reply,
        "keyword_group": keyword_group,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # Save locally
    data = _load_db()
    data.append(lead)
    _save_db(data)

    # TODO: If you want, here you can also send to Google Sheet

    return {"status": "ok", "lead": lead}


def get_leads():
    """Return all stored leads."""
    return _load_db()
