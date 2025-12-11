# services/sheet_writer.py

import gspread
from google.oauth2.service_account import Credentials
from core.settings import load_settings

def save_lead(lead_data: dict):
    """
    Saves username, comment, reply and metadata 
    into Google Sheets.
    """

    settings = load_settings()
    sheet_name = settings.get("google_sheet_name", "Leads")
    sheet_id = settings.get("google_sheet_id")

    if not sheet_id:
        return "❌ No Google Sheet ID found."

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(
        "service_account.json", scopes=SCOPES
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    row = [
        lead_data.get("username"),
        lead_data.get("comment"),
        lead_data.get("reply")
    ]

    sheet.append_row(row)

    return "Lead saved"
