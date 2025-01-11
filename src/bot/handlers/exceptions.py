from typing import Optional

class TelegramBotError(Exception):
    """Base exception class for Telegram bot errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        # Сообщение для логирования
        self.message = message
        # Сообщение для пользователя
        self.user_message = user_message or "Sorry, something went wrong. Please try again later."

class MessageProcessingError(TelegramBotError):
    """Base class for message processing errors"""
    pass

class TextMessageError(MessageProcessingError):
    """Errors related to text message processing"""
    pass
    
class VoiceMessageError(MessageProcessingError):
    """Errors related to voice message processing"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            user_message="Sorry, I couldn't process your voice message. Please try again."
        )

class BackendConnectionError(TelegramBotError):
    """Raised when backend is unavailable"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            user_message="Service is temporarily unavailable. Please try again later."
        )

class RateLimitExceeded(TelegramBotError):
    """Raised when user exceeds rate limit"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            user_message="You're sending messages too frequently. Please wait a moment."
        )

class MessageSizeError(TelegramBotError):
    """Raised when message size exceeds limit"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            user_message="Your message is too large. Please send a shorter message."
        )

class UnsupportedContentError(TelegramBotError):
    """Raised when message contains unsupported content"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            user_message="Sorry, this type of content is not supported."
        )
