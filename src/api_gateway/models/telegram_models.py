from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

# Class for incoming request to api from telegram bot
class TelegramIncomingAPIRequest(BaseModel):
    type: str  # text, voice, photo, document
    source: str
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
                    "message_id": 12345,
                    "conversation_id": "abc123"
                }
            }
        }

class TelegramRequest(BaseModel):
    id: int
    type: str
    user_id: str
    chat_id: str
    timestamp: float
    username: str
    message_id: int
    conversation_id: str
    text: Optional[str] = ""
    images: Optional[List[HttpUrl]] = []
    files: Optional[List[HttpUrl]] = []
    voice_files: Optional[List[HttpUrl]] = []

# TODO add llm answer to message request and save it to database
