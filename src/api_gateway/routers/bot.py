from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from ..utils.request_handler import RequestHandler
from ..models.telegram_models import TelegramIncomingAPIRequest

router = APIRouter()
request_handler = RequestHandler()

class MessageResponse(BaseModel):
    response: str
    status: str

@router.post("/chat", response_model=MessageResponse)
async def process_message(message: TelegramIncomingAPIRequest):
    """
    Process incoming message from telegram bot
    """
    try:
        response = await request_handler.process(message)
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
