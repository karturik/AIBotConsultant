from pydantic import BaseModel
from typing import Dict, Any, Optional

class MessageRequest(BaseModel):
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
                    "timestamp": "2023-01-01T12:00:00"
                }
            }
        }
