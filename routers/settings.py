from fastapi import APIRouter
from pydantic import BaseModel
from core.settings import save_settings, load_settings

router = APIRouter()  # ❌ yahan prefix NAHI hoga

class SettingsPayload(BaseModel):
    instagram_token: str | None = None
    instagram_id: str | None = None
    openai_key: str | None = None
    dataset_mode: str | None = "Use OpenAI"

class AutoReplyPayload(BaseModel):
    status: str  # "ON" or "OFF"


@router.post("/save_all")
def save_all_settings(data: SettingsPayload):
    save_settings(data.model_dump())
    return {"status": "saved"}


@router.post("/autoreply")
def update_autoreply(data: AutoReplyPayload):
    settings = load_settings()
    settings["autoreply_status"] = data.status
    save_settings(settings)
    return {"status": "updated", "autoreply": data.status}


@router.get("/")
def get_settings():
    return load_settings()
