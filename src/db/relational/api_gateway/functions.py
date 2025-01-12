from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from typing import List, Optional, Any

# from src.api_gateway.models.telegram_models import *
# from src.api_gateway.models.conversation import ConversationMessage

from db.relational.api_gateway.db_models import Base, DBConversationLog
from core.config import SQLALCHEMY_DATABASE_URL


class RequestLogsDBManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def get_logs_by_id(self, request_id: int) -> Optional[DBConversationLog]:
        with Session(self.engine) as session:
            db_request = session.query(DBConversationLog).filter(DBConversationLog.id == request_id).first()
            if db_request:
                return db_request
            return None

    def get_logs_by_user_id(self, user_id: int) -> Optional[List[DBConversationLog]]:
        with Session(self.engine) as session:
            db_requests = session.query(DBConversationLog).filter(
                DBConversationLog.user_id == user_id
            ).all()
            return db_requests

    def get_logs_by_chat_id(self, conv_id: int, limit: int = 1000) -> Optional[List[DBConversationLog]]:
        with Session(self.engine) as session:
            db_requests = session.query(DBConversationLog).filter(
                DBConversationLog.conversation_id == conv_id
            ).all().order_by(
                DBConversationLog.timestamp.desc()
            ).limit(limit).all()
            return db_requests

    async def create_log(self, request: Any) -> DBConversationLog:
        async with Session(self.engine) as session:
            db_request = DBConversationLog(
            user_id=request.user_id,
            chat_id=request.chat_id,
            source=request.source,
            timestamp=request.timestamp,
            text=request.text,
            conversation_id=request.conversation_id,
            role=request.role,
            type=request.type
            )

            session.add(db_request)
            await session.commit()
            
            return db_request
    
    # def _convert_to_request_model(self, db_request: DBConversationLog) -> TelegramRequest:
    #     return TelegramRequest(
    #         id=db_request.id,
    #         type=db_request.type,
    #         user_id=db_request.user_id,
    #         chat_id=db_request.chat_id,
    #         timestamp=db_request.timestamp,
    #         text=db_request.text,
    #         username=db_request.username,
    #         message_id=db_request.message_id,
    #         images=db_request.images,
    #         files=db_request.files,
    #         voices=db_request.voices,
    #         conversation_id=db_request.conversation_id,
    #     )

requests_db_manager = RequestLogsDBManager(SQLALCHEMY_DATABASE_URL)
