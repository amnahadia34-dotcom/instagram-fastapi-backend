# services/instagram_service.py

import requests

GRAPH_API = "https://graph.facebook.com/v18.0"


def send_instagram_reply(comment_id: str, reply_text: str, token: str):
    """
    Sends reply to a specific Instagram comment using Graph API.
    """

    if not token:
        return {"error": "Missing Instagram Access Token"}

    url = f"{GRAPH_API}/{comment_id}/replies"

    payload = {
        "message": reply_text,
        "access_token": token
    }

    try:
        response = requests.post(url, data=payload)

        # Return API result for debugging
        try:
            return response.json()
        except:
            return {"status": "ok", "raw": response.text}

    except Exception as e:
        return {"error": str(e)}
