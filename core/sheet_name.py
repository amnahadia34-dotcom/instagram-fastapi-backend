import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

try:
    sheets = client.openall()
    print("Sheets accessible by service account:")
    for s in sheets:
        print(" -", s.title)
except Exception as e:
    print("ERROR:", e)
