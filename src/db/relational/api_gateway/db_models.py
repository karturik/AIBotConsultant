from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association tables for many-to-many relationships
request_images = Table(
    'tg_request_attached_images',
    Base.metadata,
    Column('tg_request_id', Integer, ForeignKey('tg_requests.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True)
)

request_files = Table(
    'tg_request_attached_files',
    Base.metadata,
    Column('tg_request_id', Integer, ForeignKey('tg_requests.id'), primary_key=True),
    Column('file_id', Integer, ForeignKey('files.id'), primary_key=True)
)

request_voices = Table(
    'tg_request_attached_voices',
    Base.metadata,
    Column('tg_request_id', Integer, ForeignKey('tg_requests.id'), primary_key=True),
    Column('voice_id', Integer, ForeignKey('voices.id'), primary_key=True)
)


class DBTelegramRequest(Base):
    __tablename__ = 'tg_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    chat_id = Column(Integer, nullable=False)
    timestamp = Column(Float, nullable=False)
    text = Column(String(8192), nullable=False)
    username = Column(String(100), nullable=False)
    message_id = Column(Integer, nullable=False)
    
    # Relationships
    images = relationship("DBTelegramRequestAttachedImage", secondary=request_images, back_populates="tg_requests")
    files = relationship("DBTelegramRequestAttachedFile", secondary=request_files, back_populates="tg_requests")
    voices = relationship("DBTelegramRequestAttachedVoice", secondary=request_voices, back_populates="tg_requests")

    # Indexes for common queries
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
        {'postgresql_using': 'btree'},
        {'sqlite_on_conflict': 'ROLLBACK'},
    )

class DBTelegramRequestAttachedImage(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    meta_data = Column(String, nullable=True)
    
    # Relationship
    requests = relationship("DBTelegramRequest", secondary=request_images, back_populates="images")

class DBTelegramRequestAttachedFile(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    meta_data = Column(String, nullable=True)
    
    # Relationship
    requests = relationship("DBTelegramRequest", secondary=request_files, back_populates="files")

class DBTelegramRequestAttachedVoice(Base):
    __tablename__ = 'voices'
     
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    meta_data = Column(String, nullable=True)
     
    # Relationship
    requests = relationship("DBTelegramRequest", secondary=request_voices, back_populates="voices")

def init_db(engine):
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
