import os
import json
from datetime import datetime
from utils.signature import validate_signature
from services.keyword_service import detect_keyword_group
from services.ai_service import generate_reply
from services.lead_service import save_lead
from services.instagram_service import send_instagram_reply

async def process_instagram_comment(payload, signature, raw_body=None, dry_run: bool | None = None):
    """
    Process an incoming Instagram webhook event:
    - Validate signature
    - Parse username, text, comment_id
    - Detect keyword group
    - Generate AI reply
    - Send reply to Instagram
    - Save lead to DB and Google Sheets
    """
    # Validate signature (use raw_body if provided)
    if raw_body is not None:
        if not validate_signature(raw_body, signature):
            raise Exception("Invalid signature.")
    else:
        if not validate_signature(payload, signature):
            raise Exception("Invalid signature.")

    try:
        # Parse username, text, and comment_id
        username = payload.get("username") or payload.get("from", {}).get("username")
        text = payload.get("text") or payload.get("message") or payload.get("comment")
        comment_id = payload.get("comment_id") or payload.get("id")
        timestamp = payload.get("timestamp") or datetime.utcnow().isoformat()
        if not (username and text and comment_id):
            raise Exception("Missing required fields in webhook payload.")

        # Detect keyword group
        keyword_group = detect_keyword_group(text)

        # Generate AI reply
        reply = generate_reply(text, keyword_group)

        # Determine dry_run default from settings if not provided
        if dry_run is None:
            from core.config import settings as cfg_settings
            dry_run = bool(getattr(cfg_settings, 'DRY_RUN', True))

        # Send reply to Instagram via Graph API (respect dry_run)
        send_instagram_reply(comment_id, reply, dry_run=dry_run)

        # Save to internal DB and Google Sheet
        lead = save_lead(username, text, reply, keyword_group, timestamp)

        return {"status": "success", "reply": reply, "lead": lead}
    except Exception as e:
        # Log error or handle as needed
        raise Exception(f"Webhook processing failed: {str(e)}")
