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

VERIFY_TOKEN = "aurangzaib123"


# ---------------------------------------------------------
# META WEBHOOK VERIFICATION (GET)
# ---------------------------------------------------------
@router.get("/")
async def verify_token(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


# ---------------------------------------------------------
# Manual Reply (Streamlit Tester)
# ---------------------------------------------------------
class ManualRequest(BaseModel):
    comment: str
    username: str = "test_user"
    comment_id: str = "0000"


@router.post("/manual")
def manual_reply(data: ManualRequest):
    try:
        reply = generate_ai_reply(data.comment)
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------
# Instagram Webhook POST
# ---------------------------------------------------------
@router.post("/instagram")
async def instagram_webhook(req: Request):
    try:
        body = await req.json()
    except Exception:
        return {"status": "invalid json"}

    # Meta kabhi kabhi empty / test payload bhejta hai
    if "entry" not in body:
        return {"status": "ignored"}

    settings = load_settings()
    token = settings.get("instagram_token")

    if not token:
        return {"error": "Instagram token missing"}

    responses = []

    # Defensive loop (Meta-safe)
    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            comment_text = value.get("text")
            comment_id = value.get("id")
            username = value.get("from", {}).get("username", "unknown")

            # Agar proper comment nahi hai to skip
            if not comment_text or not comment_id:
                continue

            # Streamlit live notification
            push_event({
                "username": username,
                "comment": comment_text,
                "comment_id": comment_id
            })

            # Autoreply OFF check
            if settings.get("autoreply_status") == "OFF":
                responses.append({
                    "comment_id": comment_id,
                    "status": "autoreply off"
                })
                continue

            try:
                # AI Reply
                reply = generate_ai_reply(comment_text)

                # Send reply to Instagram
                send_instagram_reply(comment_id, reply, token)

                # Keyword detection
                keyword_group = detect_keywords(comment_text)

                # Save lead
                save_lead(username, comment_text, reply, keyword_group)

                responses.append({
                    "comment_id": comment_id,
                    "reply": reply,
                    "keyword_group": keyword_group
                })

            except Exception as e:
                responses.append({
                    "comment_id": comment_id,
                    "error": str(e)
                })

    return {
        "status": "processed",
        "results": responses
    }
