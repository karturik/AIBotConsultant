from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from typing import Generator
from contextlib import contextmanager

from src.core.config import SQLALCHEMY_DATABASE_URL, POOL_SIZE, MAX_OVERFLOW


class DatabaseSession:
    _instance = None
    _engine: Engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize database connection"""
        self._engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_pre_ping=True  # Enable automatic reconnection
        )
        
        # Create session factory
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )
        
        # Create thread-safe session factory
        self.SessionLocal = scoped_session(self._session_factory)
    
    @property
    def engine(self) -> Engine:
        """Get SQLAlchemy engine instance"""
        return self._engine
    
    @contextmanager
    def get_session(self) -> Generator:
        """Context manager for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def close(self):
        """Close database connections"""
        if self._engine:
            self._engine.dispose()

# Create global instance
db = DatabaseSession()

# Helper function to get DB session
def get_db() -> Generator:
    """Get database session"""
    with db.get_session() as session:
        yield session
