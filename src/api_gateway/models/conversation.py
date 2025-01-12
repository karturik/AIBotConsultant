from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any, Tuple


class ConversationMessage(BaseModel):
    db_id: int
    role: str
    content: str
    timestamp: float

    def to_llm_messages(self) -> List[Tuple[str, str]]:
        return [(self.role, self.content)]
    