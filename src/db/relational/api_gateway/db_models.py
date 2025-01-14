from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Table, DateTime, Boolean, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBConversationLog(Base):
    __tablename__ = 'conv_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(Float, nullable=False)
    text = Column(String(8192), nullable=False)
    type = Column(String(255), default=False)
    conversation_id = Column(String(100), nullable=False, index=True)
    role = Column(String(50), nullable=False)

    # Create indexes
    __table_args__ = (
        Index('ix_conv_logs_user_timestamp', 'user_id', 'timestamp'),  # Для поиска сообщений пользователя по времени
        Index('ix_conv_logs_conv_id_timestamp', 'conversation_id', 'timestamp'),  # Для получения истории конкретного разговора
        Index('ix_conv_logs_source_user', 'source', 'user_id'),  # Для фильтрации по источнику и пользователю
    )

def init_db(engine):
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
