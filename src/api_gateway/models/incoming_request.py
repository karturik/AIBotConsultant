from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Union

from .telegram_models import TelegramIncomingAPIRequest

class IncomingRequest(BaseModel):
    type: str = Field(description="Type of incoming message (text, voice, photo, document)")
    source: str = Field(description="Source of the message (telegram, whatsapp, etc)")
    content: Any = Field(description="Content of the message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def to_valid_request_model(self) -> Any:
        model_data = {
                "type": self.type,
                "source": self.source,
                "content": self.content,

                "user_id": self.metadata.get("user_id"),
                "timestamp": self.metadata.get("timestamp"),
                "conversation_id": self.metadata.get("conversation_id")
            }
        
        if self.source == "telegram":
            return TelegramIncomingAPIRequest(**model_data)
        else:
            raise ValueError(f"Unsupported source: {self.source}")
