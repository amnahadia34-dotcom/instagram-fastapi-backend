import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

# Configuration
import importlib
try:
    cfg = importlib.import_module('core.config')
    SHEET_NAME = getattr(cfg.settings, 'GOOGLE_SHEET_NAME', None)
except Exception:
    SHEET_NAME = None
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
# Optional: allow using a sheet ID instead of name
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Scopes and client (authorize only; do not open sheet at import-time)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

_cached_sheet = None

def get_sheet():
    """Lazily open and cache the Google Sheet. Raises the original gspread exception if not found.

    This avoids raising exceptions at import time (which causes the whole backend to fail
    when the sheet is temporarily unavailable or the name is slightly different).
    """
    global _cached_sheet
    if _cached_sheet is not None:
        return _cached_sheet

    try:
        # Prefer explicit sheet id first, then configured sheet name, then env var fallback
        if SHEET_ID:
            sh = client.open_by_key(SHEET_ID)
        else:
            name_to_try = SHEET_NAME or os.getenv("GOOGLE_SHEET_NAME", "InstagramLeads")
            sh = client.open(name_to_try)
        _cached_sheet = sh.sheet1
        return _cached_sheet
    except Exception as e:
        # Provide a helpful message including configured values to ease debugging
        msg = (
            f"Failed to open Google Sheet. Tried name='{SHEET_NAME}'"
            + (f" and id='{SHEET_ID}'" if SHEET_ID else "")
            + f". Service account file='{SERVICE_ACCOUNT_FILE}'. Error: {e}"
        )
        # Re-raise the original exception type but with augmented message for logs
        raise type(e)(msg)


def append_lead_to_sheet(lead):
    """
    Append a lead to Google Sheets with required columns and error handling.
    Columns: timestamp, platform, user_handle, message_text, intent_group, lead_score, priority_level, contact_status
    """
    # Include contact fields if present
    row = [
        lead.get("timestamp"),
        lead.get("platform"),
        lead.get("user_handle"),
        lead.get("message_text"),
        lead.get("keyword_group"),  # intent_group
        lead.get("lead_score"),
        lead.get("priority"),       # priority_level
        lead.get("status"),         # contact_status
        lead.get("name"),
        lead.get("email"),
        lead.get("phone")
    ]
    # Respect DRY_RUN setting to avoid writing during tests
    try:
        from core.config import settings as cfg_settings
        if bool(getattr(cfg_settings, 'DRY_RUN', True)):
            print("[DRY RUN] Would append row to Google Sheet:", row)
            return
    except Exception:
        # if config can't be read, proceed to actual append
        pass

    try:
        sheet = get_sheet()
        sheet.append_row(row)
    except Exception as e:
        # Log or handle error as needed; keep the application running
        print(f"Failed to append lead to Google Sheet: {e}")
