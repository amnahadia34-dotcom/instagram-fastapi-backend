# routers/realtime.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# Global memory (production me Redis use karna hota)
latest_comment_event = None


@router.get("/events")
def get_latest_event():
    """
    Streamlit dashboard calls this every 2 seconds.
    If a new IG comment comes, webhook will update this value.
    """
    global latest_comment_event
    return JSONResponse(latest_comment_event or {"event": None})


def send_event_to_ui(event: dict):
    """
    Called from webhook.py when IG comment arrives.
    """
    global latest_comment_event
    latest_comment_event = event
