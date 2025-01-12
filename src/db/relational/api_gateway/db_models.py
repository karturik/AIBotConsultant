from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBConversationLog(Base):
    __tablename__ = 'conv_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False, index=True) # tg / vk / whatsapp
    user_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(Float, nullable=False)
    text = Column(String(8192), nullable=False)
    type = Column(String(255), default=False)
    conversation_id = Column(String(100), nullable=False, index=True)
    role = Column(String(50), nullable=False) # user / assistant

    # Indexes for common queries
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
        {'postgresql_using': 'btree'},
        {'sqlite_on_conflict': 'ROLLBACK'},
    )

def init_db(engine):
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
