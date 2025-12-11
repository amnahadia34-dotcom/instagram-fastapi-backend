from fastapi import APIRouter, Request
from pydantic import BaseModel
from core.settings import load_settings
from services.queue_service import push_event
from services.ai_service import generate_ai_reply
from services.instagram_service import send_instagram_reply
from services.lead_service import save_lead
from services.keyword_service import detect_keywords

router = APIRouter()


# ---------------------------------------------------------
# META VERIFY ENDPOINT
# ---------------------------------------------------------
@router.get("/")
async def verify_token(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    VERIFY_TOKEN = "aurangzaib123"

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}



# ---------------------------------------------------------
# Manual Reply (Streamlit)
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
# Instagram Webhook POST
# ---------------------------------------------------------
@router.post("/instagram")
async def instagram_webhook(req: Request):
    body = await req.json()
    settings = load_settings()

    token = settings.get("instagram_token")

    entry = body["entry"][0]["changes"][0]
    comment_text = entry["value"]["text"]
    comment_id = entry["value"]["id"]
    username = entry["value"].get("from", {}).get("username", "unknown")

    push_event({
        "username": username,
        "comment": comment_text,
        "comment_id": comment_id
    })

    if settings.get("autoreply_status") == "OFF":
        return {"message": "Autoreply OFF"}

    reply = generate_ai_reply(comment_text)
    send_instagram_reply(comment_id, reply, token)

    keyword_group = detect_keywords(comment_text)
    save_lead(username, comment_text, reply, keyword_group)

    return {"reply": reply}
