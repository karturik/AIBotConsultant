from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Union

class IncomingRequest(BaseModel):
    type: str = Field(description="Type of incoming message (text, voice, photo, document)")
    source: str = Field(description="Source of the message (telegram, whatsapp, etc)")
    content: Any = Field(description="Content of the message")
    text: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def unpack_metadata(self) -> None:
        self.user_id = self.metadata.get("user_id")
        self.timestamp = self.metadata.get("timestamp")
        self.conversation_id = self.metadata.get("conversation_id")
        
    class Config:
        json_schema_extra = {
            "example": {
                "type": "text",
                "source": "telegram",
                "content": "Hello, AI!",
                "user_id": 123456789,
                "timestamp": "2023-01-01T12:00:00",
                "conversation_id": "abc123"
            }
        }
