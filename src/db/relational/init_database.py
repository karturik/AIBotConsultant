import sys
import os

# Add src directory to Python path
HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src'))
print(HOME_DIR)
sys.path.append(HOME_DIR)

from sqlalchemy import create_engine
from core.config import SQLALCHEMY_DATABASE_URL
from db.relational.nlp.db_models import Base as nlp_base
from db.relational.api_gateway.db_models import Base as api_base

def init_database():
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Create all tables
    nlp_base.metadata.create_all(bind=engine)
    api_base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
