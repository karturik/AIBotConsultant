from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any

class NLPRequest(BaseModel):
    request_id: int
    type: str
    content: Any
    user_id: str
    chat_id: str

app = FastAPI()

@app.post("/process")
async def process_request(request: NLPRequest):
    try:
        # Обработка с помощью LangChain
        result = await process_with_langchain(request)
        return {
            "status": "success",
            "response": result,
            "request_id": request.request_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
