from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional, List

from models.models import NLPChatRequest
from utils.text_processor import llm_processing

app = FastAPI()

@app.post("/chat")
async def process_request(request: NLPChatRequest):
    try:
        # Обработка с помощью LangChain
        result = await llm_processing(request)
        return {
            "status": "success",
            "response": result,
            "request_id": request.request_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
