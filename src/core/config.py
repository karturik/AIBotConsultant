from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"

POOL_SIZE = 5
MAX_OVERFLOW = 10

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

PROXY_URL = os.getenv("PROXY_URL", "")