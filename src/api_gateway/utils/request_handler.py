from datetime import datetime
from typing import Optional, List, Tuple, SimpleNamespace
import aiohttp
from fastapi import HTTPException

from db.relational.api_gateway.functions import request_logs_db_manager
from models.incoming_request import IncomingRequest
from models.conversation import ConversationMessage


class RequestHandler:

    async def _db_log_save(self, request_model: IncomingRequest) -> int:
        """Process incoming telegram message and save to database
        Retruns id of saved record
        """
        try:
            # Convert timestamp string to float if needed
            timestamp = (
                datetime.fromisoformat(request_model.timestamp).timestamp()
                if isinstance(request_model.timestamp, str)
                else float(request_model.timestamp)
            )

            # Initialize base request data
            database_request_data = SimpleNamespace(
                type=request_model.type,
                user_id=request_model.user_id,
                timestamp=timestamp,
                conversation_id=request_model.conversation_id,
                text=request_model.text,
                role="user",
                source=request_model.source
            )

            # Save to database
            saved_request = await request_logs_db_manager.create_log(database_request_data)
            return saved_request.id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process message: {str(e)}"
            )

    async def _get_conversation_history(self, conv_id: int, limit: int = 100) -> Optional[List[Tuple[str, str]]]:
        conv_logs_entries = await request_logs_db_manager.get_logs_by_conversation_id(conv_id, limit)
        messages_list = [
            (db_log.role, db_log.text) for db_log in conv_logs_entries
        ]
        return messages_list


    async def _transcribe_voice_message(self, message: IncomingRequest) -> Tuple[Any, str]:
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
                    return None, result["response"]
        except Exception as e:
            return HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            ), ""

    async def process(self, incoming_request: IncomingRequest):
        try:

            # Распаковываем метадату в модели
            request_model = incoming_request.unpack_metadata()

            # Если юзер обратился голосом - транскрибируем и сохраняем текст в БД
            if incoming_request.type == "voice":
                transcription_error, transcription_result = await self._transcribe_voice_message(request_model)
                request_model.text = transcription_result
            else:
                transcription_error = None 
            
            # Сохраняем запрос пользователя в БД
            saved_log_id = await self._db_log_save(request_model)
            
            if transcription_error:
                raise transcription_error
            
            # При отправке в NLP сервис добавляем историю
            messages_history = await self._get_conversation_history(incoming_request.conversation_id)

            # Готовим данные для NLP сервиса
            nlp_request_data = {
                "source": incoming_request.source,
                "messages": messages_history,
            }

            # Отправляем в NLP сервис
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.nlp_service_url}/chat", 
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