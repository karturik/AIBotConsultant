from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

# Class for incoming request to api from telegram bot
class TelegramIncomingAPIRequest(BaseModel):
    type: str  # text, voice, photo, document
    content: Any
    metadata: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "type": "text",
                "content": "Hello, AI!",
                "metadata": {
                    "user_id": 123456789,
                    "chat_id": 987654321,
                    "timestamp": "2023-01-01T12:00:00",
                    "username": "john_doe",
                    "message_id": 12345
                }
            }
        }


# Class for outgoing request from api to nlp services 
class TelegramRequestAttachedImage(BaseModel):
    url: HttpUrl
    meta_data: Optional[str] = None

class TelegramRequestAttachedFile(BaseModel):
    url: HttpUrl
    meta_data: Optional[str] = None

class TelegramRequestAttachedVoice(BaseModel):
    url: HttpUrl
    meta_data: Optional[str] = None

class TelegramRequest(BaseModel):
    id: int
    type: str
    user_id: str
    chat_id: str
    timestamp: float
    username: str
    message_id: int
    text: Optional[str] = ""
    images: Optional[List[TelegramRequestAttachedImage]] = []
    files: Optional[List[TelegramRequestAttachedFile]] = []
    voice_files: Optional[List[TelegramRequestAttachedVoice]] = []
