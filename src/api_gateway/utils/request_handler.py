from datetime import datetime
from typing import Optional, List
import aiohttp
from fastapi import HTTPException

from models.telegram_models import TelegramIncomingAPIRequest
from db.relational.api_gateway.functions import bot_user_request_db_manager
from models.telegram_models import *


class RequestHandler:
    def __init__(self, storage_service_url: str = ""):
        self.storage_service_url = storage_service_url

    async def upload_file_to_storage(self, content: bytes, file_type: str) -> str:
        """Upload file to storage service and return URL"""
        try:
            # async with aiohttp.ClientSession() as session:
            #     files = {'file': content}
            #     async with session.post(
            #         f"{self.storage_service_url}/upload/{file_type}", 
            #         data=files
            #     ) as response:
            #         if response.status != 200:
            #             raise HTTPException(status_code=500, detail="Storage service error")
            #         result = await response.json()
            #         return result['url']
                return ""
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    async def _process(self, message: TelegramIncomingAPIRequest) -> TelegramRequest:
        """Process incoming telegram message and save to database"""
        try:
            # Convert timestamp string to float if needed
            timestamp = (
                datetime.fromisoformat(message.metadata["timestamp"]).timestamp()
                if isinstance(message.metadata["timestamp"], str)
                else float(message.metadata["timestamp"])
            )

            # Initialize base request data
            database_request_data = TelegramRequest(
                id=0,  # Will be set by database
                type=message.type,
                user_id=str(message.metadata["user_id"]),
                chat_id=str(message.metadata["chat_id"]),
                timestamp=timestamp,
                username=message.metadata["username"],
                message_id=message.metadata["message_id"],
                text="",
                images=[],
                files=[],
                voice_files=[]
            )

            # Process different types of content
            if message.type == "text":
                database_request_data.text = message.content

            elif message.type == "photo":
                url = await self.upload_file_to_storage(message.content, "image")
                database_request_data.images.append(
                    TelegramRequestAttachedImage(url=url, meta_data=None)
                )

            elif message.type == "document":
                url = await self.upload_file_to_storage(message.content, "file")
                database_request_data.files.append(
                    TelegramRequestAttachedFile(url=url, meta_data=None)
                )

            elif message.type == "voice":
                url = await self.upload_file_to_storage(message.content, "voice")
                database_request_data.voice_files.append(
                    TelegramRequestAttachedVoice(url=url, meta_data=None)
                )

            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported message type: {message.type}"
                )

            # Save to database
            saved_request = await bot_user_request_db_manager.create_request(database_request_data)
            return saved_request

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process message: {str(e)}"
            )

    async def process(self, message: TelegramIncomingAPIRequest):
        pass