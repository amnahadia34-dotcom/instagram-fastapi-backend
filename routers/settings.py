# routers/settings.py

from fastapi import APIRouter
from pydantic import BaseModel
from core.settings import save_settings, load_settings

router = APIRouter(prefix="/settings", tags=["Settings"])


# -----------------------------
# MODELS
# -----------------------------
class SettingsPayload(BaseModel):
    instagram_token: str | None = None
    instagram_id: str | None = None
    openai_key: str | None = None
    dataset_mode: str | None = "Use OpenAI"


class AutoReplyPayload(BaseModel):
    status: str  # "ON" or "OFF"


# -----------------------------
# SAVE ALL SETTINGS
# -----------------------------
@router.post("/save_all")
def save_all_settings(data: SettingsPayload):
    settings = load_settings()
    settings.update({k: v for k, v in data.dict().items() if v is not None})
    save_settings(settings)
    return {"status": "saved", "settings": settings}


# -----------------------------
# GET SETTINGS
# -----------------------------
@router.get("/")
def get_settings():
    return load_settings()


# -----------------------------
# AUTOREPLY ON / OFF  🔥
# -----------------------------
@router.post("/autoreply")
def update_autoreply(payload: AutoReplyPayload):
    settings = load_settings()
    settings["autoreply_status"] = payload.status
    save_settings(settings)
    return {
        "status": "ok",
        "autoreply_status": payload.status
    }
