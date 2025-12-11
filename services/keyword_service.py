import json
import os

KEYWORDS_FILE = "keywords.json"


def load_keywords():
    """Load keyword groups from JSON file."""
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def detect_keyword_group(text: str):
    """Return single keyword group for given text."""
    keywords = load_keywords()

    for group, words in keywords.items():
        for w in words:
            if w.lower() in text.lower():
                return group

    return "unknown"


def detect_keywords(text: str):
    """
    COMPATIBILITY FUNCTION
    Backend expects this name.
    Returns detected keyword group (same as detect_keyword_group)
    """
    return detect_keyword_group(text)
