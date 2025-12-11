# Core settings and configuration loader
import os


class Settings:
    INSTAGRAM_SECRET = os.getenv("INSTAGRAM_SECRET", "changeme")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-xxx")
    # Use the correct env var and default for the sheet name
    GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "LEAD AGENTE RRSS HBH")
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    # Instagram / Facebook Graph configuration
    INSTAGRAM_ID = os.getenv("INSTAGRAM_ID", "")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    # Dry run flag: when true the app will not post replies to Instagram (safe testing)
    DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes")
    # OpenAI model selection
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

settings = Settings()
