from datetime import datetime
from typing import Optional, List
import aiohttp
from fastapi import HTTPException

from db.relational.api_gateway.functions import bot_user_request_db_manager
from models.incoming_request import IncomingRequest
from models.telegram_models import *


class RequestHandler:

    async def _process_and_save(self, message: TelegramIncomingAPIRequest) -> TelegramRequest:
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
                conversation_id=message.metadata["conversation_id"],
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
                database_request_data.images.append(url)

            elif message.type == "document":
                url = await self.upload_file_to_storage(message.content, "file")
                database_request_data.files.append(url)

            elif message.type == "voice":
                url = await self.upload_file_to_storage(message.content, "voice")
                database_request_data.voice_files.append(url)

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

    async def _get_conversation_history(
        self, 
        conversation_id: int,
        limit: int = 100  # Ограничение на количество сообщений
    ) -> List[ConversationMessage]:
        async with Session() as session:
            messages = await session.query(TelegramRequest).filter(
                TelegramRequest.conversation_id == conversation_id
            ).order_by(
                TelegramRequest.timestamp.desc()
            ).limit(limit).all()
            
            return [
                ConversationMessage(
                    role="user" if msg.type == "user" else "assistant",
                    content=msg.text,
                    timestamp=msg.timestamp
                )
                for msg in reversed(messages)
            ]

    async def _transcribe_voice_message(self, message: TelegramIncomingAPIRequest) -> str:
        """Send voice message to NLP service for transcription"""
        try:
            # Подготовка данных для отправки
            transcription_request = {
                "content": message.content,
            }

            # Отправка в NLP сервис
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.nlp_service_url}/transcribe",
                    json=transcription_request
                ) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=response.status, 
                            detail="Transcription service error"
                        )
                    result = await response.json()
                    return result["text"]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )

    async def process(self, message: IncomingRequest):
        try:

            # Определяем нужную модель для обработки сообщения


            # Сохраняем запрос пользователя в БД
            saved_request = await self._process_and_save(message)

            # Если юзер обратился голосом - транскрибируем и сохраняем текст в БД
            if saved_request.type == "voice":
                transcription_result = await self._transcribe_voice_message(message)
                
                # Обновляем запись в БД с транскрибированным текстом
                await bot_user_request_db_manager.save_text_to_tg_request(
                    transcription_result,
                    saved_request.id
                )
                
                # Обновляем объект saved_request
                saved_request.text = transcription_result
            
            # При отправке в NLP сервис добавляем историю
            messages_history = await self._get_conversation_history(saved_request.conversation_id)

            # Готовим данные для NLP сервиса
            nlp_request_data = {
                "request_id": saved_request.id,
                "type": message.type,
                "content": message.content,
            }

            # Отправляем в NLP сервис
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.nlp_service_url}/process", 
                    json=nlp_request_data
                ) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail="NLP service error")
                    nlp_response = await response.json()
                    
            return nlp_response

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Processing error: {str(e)}"
            )
        # TODO сохранить в бд ответ модели