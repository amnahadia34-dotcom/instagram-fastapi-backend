
def score_lead(text, keyword_group=None):
    """
    Score a lead based on keyword group, contact details, message clarity, and intent.
    Returns a score between 0 and 100.
    """
    score = 0
    text_lower = text.lower()
    # Keyword group weighting
    if keyword_group == "purchase":
        score += 40
    elif keyword_group == "inquiry":
        score += 25
    elif keyword_group == "feedback":
        score += 10
    # Contact details (simple check for email/phone)
    if any(x in text_lower for x in ["@", ".com", "+", "phone", "call"]):
        score += 20
    # Message clarity (length)
    if len(text) > 30:
        score += 20
    elif len(text) > 10:
        score += 10
    # Intent (look for strong intent words)
    if any(x in text_lower for x in ["buy", "order", "purchase", "interested"]):
        score += 20
    elif any(x in text_lower for x in ["help", "question", "support"]):
        score += 10
    return min(score, 100)

def get_priority(score):
    if score >= 70:
        return "hot"
    elif score >= 40:
        return "warm"
    return "cold"
