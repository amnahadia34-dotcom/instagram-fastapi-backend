from fastapi import APIRouter
from pydantic import BaseModel
from core.settings import save_settings, load_settings

router = APIRouter()

class Settings(BaseModel):
    openai_key: str
    instagram_token: str
    instagram_id: str
    autoreply_enabled: bool = True


@router.post("/save_all")
def save_all_settings(data: Settings):
    save_settings(data.dict())
    return {"status": "saved", "settings": data}


@router.get("/")
def get_settings():
    return load_settings()
