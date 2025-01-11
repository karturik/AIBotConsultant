from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from ..services.message_handler import MessageHandler
from ..models.message import MessageRequest

router = APIRouter()
message_handler = MessageHandler()

class MessageResponse(BaseModel):
    response: str
    status: str

@router.post("/message", response_model=MessageResponse)
async def process_message(message: MessageRequest):
    """
    Process incoming message from bot
    """
    try:
        response = await message_handler.process(message)
        return MessageResponse(
            response=response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/status")
async def get_bot_status():
    """
    Get bot processing status
    """
    return {"status": "active"}
