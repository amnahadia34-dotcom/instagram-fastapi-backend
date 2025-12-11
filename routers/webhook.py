# routers/webhook.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
from core.settings import load_settings
from services.queue_service import push_event
from services.ai_service import generate_ai_reply
from services.instagram_service import send_instagram_reply
from services.lead_service import save_lead
from services.keyword_service import detect_keywords

router = APIRouter()

GRAPH_VERSION = "v18.0"


# ---------------------------------------------------------
# Manual API Call Tester (from Streamlit)
# ---------------------------------------------------------
class ManualRequest(BaseModel):
    comment: str
    username: str = "test_user"
    comment_id: str = "0000"


@router.post("/manual")
def manual_reply(data: ManualRequest):
    reply = generate_ai_reply(data.comment)
    return {"reply": reply}


# ---------------------------------------------------------
# REAL INSTAGRAM WEBHOOK ENDPOINT
# ---------------------------------------------------------
@router.post("/instagram")
async def instagram_webhook(req: Request):

    body = await req.json()
    settings = load_settings()

    token = settings.get("instagram_token")
    page_id = settings.get("instagram_id")

    # Extract comment info from webhook (REAL IG structure)
    entry = body["entry"][0]["changes"][0]

    comment_text = entry["value"]["text"]
    comment_id = entry["value"]["id"]
    username = entry["value"].get("from", {}).get("username", "unknown")

    # Push to Queue so Streamlit shows real-time notification
    push_event({
        "username": username,
        "comment": comment_text,
        "comment_id": comment_id
    })

    # If autoreply is OFF → do nothing
    if settings.get("autoreply_status") == "OFF":
        return {"message": "Received. Autoreply is OFF."}

    # ------------------------------------------------------
    # AUTO-REPLY MODE (ON)
    # ------------------------------------------------------
    reply = generate_ai_reply(comment_text)

    # Actually send reply to Instagram
    send_instagram_reply(comment_id, reply, token)

    # Keyword detection (your keyword_service.py)
    keyword_group = detect_keywords(comment_text)

    # Save lead to Google Sheet
    save_lead(username, comment_text, reply, keyword_group)

    return {
        "received": comment_text,
        "reply_sent": reply,
        "keyword_group": keyword_group
    }


# ---------------------------------------------------------
# Streamlit "Generate Reply" → Call This
# ---------------------------------------------------------
class ReplyRequest(BaseModel):
    comment: str
    comment_id: str
    username: str


@router.post("/reply_now")
def reply_now(req: ReplyRequest):

    settings = load_settings()
    token = settings.get("instagram_token")

    reply = generate_ai_reply(req.comment)

    # Send reply to IG
    send_instagram_reply(req.comment_id, reply, token)

    # Save in sheet
    keyword_group = detect_keywords(req.comment)
    save_lead(req.username, req.comment, reply, keyword_group)

    return {"reply": reply, "keyword_group": keyword_group}
