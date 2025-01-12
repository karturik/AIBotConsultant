from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any


class ConversationMessage(BaseModel):
    role: str
    content=str
    timestamp: float
    