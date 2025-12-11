# services/openai_ai.py

import openai
from core.settings import load_settings

def generate_reply(comment_text: str, openai_key: str = None):
    """
    Generates AI reply using OpenAI (GPT-4 or GPT-3.5)
    plus your dataset.
    """

    settings = load_settings()
    key = openai_key or settings.get("openai_key")

    if not key:
        return "⚠ No OpenAI key provided."

    openai.api_key = key

    prompt = f"""
You are the Instagram assistant for Creafitness.
Use the company dataset and answer this comment:

Comment: {comment_text}

Your reply must be friendly, short and helpful.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response["choices"][0]["message"]["content"].strip()
