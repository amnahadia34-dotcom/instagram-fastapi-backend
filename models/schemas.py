from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InstagramComment(BaseModel):
    username: str
    text: str
    timestamp: datetime

class Lead(BaseModel):
    timestamp: datetime
    platform: str
    user_handle: str
    message_text: str
    keyword_group: str
    lead_score: int
    priority: str
    status: str
    reply: Optional[str] = None
