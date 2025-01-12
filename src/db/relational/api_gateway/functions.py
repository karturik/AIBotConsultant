from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from typing import List, Optional

from src.api_gateway.models.telegram_models import *

from db.relational.api_gateway.db_models import Base, DBTelegramRequest, TelegramRequestAttachedImage, TelegramRequestAttachedFile, TelegramRequestAttachedVoice
from core.config import SQLALCHEMY_DATABASE_URL


class TelegramRequestDBManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def get_request_by_id(self, request_id: int) -> Optional[TelegramRequest]:
        with Session(self.engine) as session:
            db_request = session.query(DBTelegramRequest).filter(DBTelegramRequest.id == request_id).first()
            if db_request:
                return self._convert_to_request_model(db_request)
            return None

    def get_requests_by_user_id(self, user_id: int) -> List[TelegramRequest]:
        with Session(self.engine) as session:
            db_requests = session.query(DBTelegramRequest).filter(
                DBTelegramRequest.user_id == user_id
            ).all()
            return [self._convert_to_request_model(r) for r in db_requests]

    def get_requests_by_type(self, request_type: str) -> List[TelegramRequest]:
        with Session(self.engine) as session:
            db_requests = session.query(DBTelegramRequest).filter(
                DBTelegramRequest.type == request_type
            ).all()
            return [self._convert_to_request_model(r) for r in db_requests]

    def get_requests_by_chat_id(self, chat_id: int) -> List[TelegramRequest]:
        with Session(self.engine) as session:
            db_requests = session.query(DBTelegramRequest).filter(
                DBTelegramRequest.chat_id == chat_id
            ).all()
            return [self._convert_to_request_model(r) for r in db_requests]

    def create_request(self, request: TelegramRequest) -> TelegramRequest:
        with Session(self.engine) as session:
            db_request = DBTelegramRequest(
            type=request.type,
            user_id=request.user_id,
            chat_id=request.chat_id,
            timestamp=request.timestamp,
            text=request.text,
            username=request.username,
            message_id=request.message_id
            )
            
            # Add images
            for image in request.images:
                db_image = TelegramRequestAttachedImage(
                    url=image.url,
                    meta_data=image.meta_data
                )
                db_request.images.append(db_image)

            # Add files  
            for file in request.files:
                db_file = TelegramRequestAttachedFile(
                    url=file.url,
                    meta_data=file.meta_data
                )
                db_request.files.append(db_file)

            # Add voices
            for voice in request.voices:
                db_voice = TelegramRequestAttachedVoice(
                    url=voice.url,
                    meta_data=voice.meta_data
                )
                db_request.voices.append(db_voice)

            session.add(db_request)
            session.commit()
            
            return self._convert_to_request_model(db_request)

    def _convert_to_request_model(self, db_request: DBTelegramRequest) -> TelegramRequest:
        return TelegramRequest(
            id=db_request.id,
            type=db_request.type,
            user_id=db_request.user_id,
            chat_id=db_request.chat_id,
            timestamp=db_request.timestamp,
            text=db_request.text,
            username=db_request.username,
            message_id=db_request.message_id,
            images=[
                TelegramRequestAttachedImage(
                    url=img.url,
                    meta_data=img.meta_data
                ) for img in db_request.images
            ],
            files=[
                TelegramRequestAttachedFile(
                    url=f.url,
                    meta_data=f.meta_data
                ) for f in db_request.files
            ],
            voices=[
                TelegramRequestAttachedVoice(
                    url=v.url,
                    meta_data=v.meta_data
                ) for v in db_request.voices
            ]
        )

bot_user_request_db_manager = TelegramRequestDBManager(SQLALCHEMY_DATABASE_URL)
