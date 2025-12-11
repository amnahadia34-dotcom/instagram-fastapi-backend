# services/ai_service.py

import json
from core.settings import load_settings
from openai import OpenAI
from services.dataset_service import get_dataset_text
from services.keyword_service import detect_keywords


def sanitize(text: str) -> str:
    """ Ensures clean UTF-8 text """
    return text.encode("utf-8", "ignore").decode()


def build_prompt(comment: str, use_dataset: bool):
    """
    Creates dynamic prompt for OpenAI depending on mode:
    - Dataset mode
    - Normal AI mode
    """

    if use_dataset:
        dataset_text = get_dataset_text() or "[No dataset found]"
        return f"""
You are an AI assistant replying to Instagram comments.
Use ONLY the dataset information below to answer.

DATASET:
----------------
{dataset_text}
----------------

USER COMMENT: {comment}

Return a natural, friendly reply.
"""

    else:
        return f"""
You are a friendly Instagram assistant.
Reply to this user comment in a warm and engaging tone.

Comment: {comment}

Keep reply short, natural and positive.
"""


def generate_ai_reply(comment: str) -> str:
    """
    Generates reply using OpenAI GPT-4o or DATASET model.
    """

    settings = load_settings()
    api_key = settings.get("openai_key")

    if not api_key:
        return "⚠️ Missing OpenAI Key"

    use_dataset = settings.get("dataset_mode") == "Use Dataset"

    prompt = sanitize(build_prompt(comment, use_dataset))

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        reply_text = response.choices[0].message.content
        return sanitize(reply_text)

    except Exception as e:
        return f"⚠️ OpenAI Error: {str(e)}"
