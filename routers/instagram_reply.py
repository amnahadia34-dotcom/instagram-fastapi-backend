# routers/instagram_reply.py

from fastapi import APIRouter
import requests
from core.settings import load_settings
from services.openai_ai import generate_reply
from services.sheet_writer import save_lead

router = APIRouter()

GRAPH_URL = "https://graph.facebook.com/v18.0"


@router.post("/send_reply")
def send_reply(comment_id: str, comment_text: str, username: str):
    settings = load_settings()

    token = settings["instagram_token"]
    page_id = settings["instagram_id"]
    openai_key = settings["openai_key"]

    # 1. AI reply from dataset or model
    ai_reply = generate_reply(comment_text, openai_key)

    # 2. Send reply to Instagram
    url = f"{GRAPH_URL}/{comment_id}/replies"
    payload = {"message": ai_reply, "access_token": token}

    ig_res = requests.post(url, data=payload).json()

    # 3. Save lead
    save_lead({
        "username": username,
        "comment": comment_text,
        "reply": ai_reply,
    })

    return {
        "status": "sent",
        "reply": ai_reply,
        "instagram_response": ig_res
    }
