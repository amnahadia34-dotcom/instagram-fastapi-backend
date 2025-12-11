import re


def extract_contact_details(text: str) -> dict:
    """Extract simple contact details from a text blob.

    Returns a dict with possible keys: name, email, phone
    Uses simple heuristics and regexes; not perfect but useful for parsing comments.
    """
    result = {"name": None, "email": None, "phone": None}
    if not text:
        return result
    # Email regex
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email_match:
        result["email"] = email_match.group(0)

    # Phone number heuristic: look for sequences of 7-15 digits with optional separators
    phone_match = re.search(r"(\+?\d[\d\-(). ]{6,}\d)", text)
    if phone_match:
        # normalize
        phone = re.sub(r"[^0-9+]", "", phone_match.group(0))
        result["phone"] = phone

    # Name heuristic: look for patterns like 'my name is X' or 'I'm X' or 'I am X'
    name_match = re.search(r"(?:my name is|I'm|I am)\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)", text)
    if name_match:
        result["name"] = name_match.group(1)
    else:
        # fallback: if the comment contains two capitalized words at start, consider as name
        first_words = re.findall(r"\b([A-Z][a-z]+)\b", text)
        if len(first_words) >= 2:
            result["name"] = f"{first_words[0]} {first_words[1]}"

    return result
