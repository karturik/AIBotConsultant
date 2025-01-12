from typing import Optional, Dict, Any
import aiohttp
import logging
from datetime import datetime
from uuid import uuid4
import asyncio
from .exceptions import (
    BackendConnectionError, 
    MessageProcessingError,
    RateLimitExceeded,
    InvalidMessageFormat
)
from ..bot_config import (
    API_GATEWAY_URL,
    MAX_MESSAGE_SIZE,
    MAX_REQUESTS_PER_MINUTE,
    REQUEST_TIMEOUT,
    ALLOWED_FILE_TYPES,
    RETRY_ATTEMPTS
)

logger = logging.getLogger(__name__)

class MessageProcessor:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self._rate_limit_dict = {}
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self):
        if not self.session.closed:
            await self.session.close()
            
    async def check_rate_limit(self, user_id: int) -> bool:
        """Check if user hasn't exceeded rate limit"""
        current_time = datetime.now()
        user_requests = self._rate_limit_dict.get(user_id, [])
        
        # Remove old requests
        user_requests = [time for time in user_requests 
                        if (current_time - time).seconds < 60]
        
        if len(user_requests) >= MAX_REQUESTS_PER_MINUTE:
            return False
            
        user_requests.append(current_time)
        self._rate_limit_dict[user_id] = user_requests
        return True

    async def handle_command(self, update: Any, context: Any):
        if update.message.text == '/reset':
            # Создаем новый диалог
            new_conversation_id = str(uuid4())
            context.user_data['conversation_id'] = new_conversation_id
            await update.message.reply_text("Started new conversation!")
            return
    
    async def process_message(self, update: Any, context: Any) -> Optional[str]:
        """Main entry point for message processing"""
        try:
            user_id = update.effective_user.id

            # Получаем или создаем conversation_id
            if 'conversation_id' not in context.user_data:
                context.user_data['conversation_id'] = str(uuid4())
            
            if not await self.check_rate_limit(user_id):
                raise RateLimitExceeded("Too many requests. Please wait.")
                
            if update.message.text:
                return await self.process_text_message(update, context)
            elif update.message.voice:
                return await self.process_voice_message(update, context)
            # elif update.message.photo:
            #     return await self.process_photo_message(update, context)
            # elif update.message.document:
            #     return await self.process_document_message(update, context)
            else:
                raise InvalidMessageFormat("Unsupported message type")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return "Sorry, there was an error processing your message."

    async def process_text_message(self, update: Any, context: Any) -> Optional[str]:
        """Process text messages"""
        try:
            if len(update.message.text) > MAX_MESSAGE_SIZE:
                raise InvalidMessageFormat("Message too long")
                
            message_data = {
                "type": "text",
                "source": "telegram",
                "content": update.message.text,
                "metadata": self._get_metadata(update, context)
            }
            
            return await self._send_to_backend(message_data)
            
        except Exception as e:
            logger.error(f"Error processing text message: {str(e)}", exc_info=True)
            raise MessageProcessingError(str(e))

    async def process_voice_message(self, update: Any, context: Any) -> Optional[str]:
        """Process voice messages"""
        try:
            voice_file = await update.message.voice.get_file()
            voice_bytes = await voice_file.download_as_bytearray()
            
            if len(voice_bytes) > MAX_MESSAGE_SIZE:
                raise InvalidMessageFormat("Voice message too large")
                
            message_data = {
                "type": "voice",
                "source": "telegram",
                "content": voice_bytes,
                "metadata": self._get_metadata(update, context)
            }
            
            return await self._send_to_backend(message_data)
            
        except Exception as e:
            logger.error(f"Error processing voice message: {str(e)}", exc_info=True)
            raise MessageProcessingError(str(e))

    def _get_metadata(self, update: Any, context: Any) -> Dict[str, Any]:
        """Extract metadata from update"""
        return {
            "user_id": update.effective_user.id,
            # "chat_id": update.effective_chat.id,
            "timestamp": datetime.now().isoformat(),
            # "username": update.effective_user.username,
            # "message_id": update.message.message_id,
            "conversation_id": context.user_data['conversation_id']
        }

    async def _send_to_backend(self, message_data: Dict[str, Any]) -> Optional[str]:
        """Send message data to backend with retry logic"""
        for attempt in range(RETRY_ATTEMPTS):
            try:
                async with self.session.post(
                    API_GATEWAY_URL,
                    json=message_data,
                    timeout=REQUEST_TIMEOUT
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        error_text = await response.text()
                        logger.error(f"Backend error: {error_text}")
                        raise BackendConnectionError(f"Backend returned {response.status}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Request timeout, attempt {attempt + 1}/{RETRY_ATTEMPTS}")
                if attempt == RETRY_ATTEMPTS - 1:
                    raise BackendConnectionError("Backend request timeout")
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error sending to backend: {str(e)}", exc_info=True)
                if attempt == RETRY_ATTEMPTS - 1:
                    raise BackendConnectionError(str(e))
                await asyncio.sleep(1)

