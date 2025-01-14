from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from typing import List, Optional, Any

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

    async def get_logs_by_conversation_id(self, conv_id: int, limit: int = 1000) -> Optional[List[DBConversationLog]]:
        async with Session(self.engine) as session:
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

request_logs_db_manager = RequestLogsDBManager(SQLALCHEMY_DATABASE_URL)
