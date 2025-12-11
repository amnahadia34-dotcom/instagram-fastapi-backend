import hmac
import hashlib
import os
import importlib

# Prefer secret from core.config.settings, fallback to env var APP_SECRET
try:
    cfg = importlib.import_module('core.config')
    SECRET = getattr(cfg.settings, 'INSTAGRAM_SECRET', None) or os.getenv("APP_SECRET", "be5a948c0aa275d0198dc2150995ad06")
except Exception:
    SECRET = os.getenv("APP_SECRET", "be5a948c0aa275d0198dc2150995ad06")

def validate_signature(payload, signature):
    """
    Validate Instagram webhook signature using HMAC SHA256.
    payload: raw request body (bytes)
    signature: value from 'X-Instagram-Signature' header
    """
    if not signature:
        return False
    if isinstance(payload, str):
        payload = payload.encode()
    expected = hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
