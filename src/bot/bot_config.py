import os
from dotenv import load_dotenv
import pytz

load_dotenv()

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN') 
TIMEZONE = pytz.timezone('Europe/Minsk')

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000/api/v1/chat")
MAX_MESSAGE_SIZE = int(os.getenv("MAX_MESSAGE_SIZE", 20 * 1024 * 1024))  # 20MB
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", 30))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
ALLOWED_FILE_TYPES = [
    "image/jpeg",
    "image/png",
    "audio/ogg",
    "audio/mpeg",
    "application/pdf"
]

NLP_SERVICE_URL = os.getenv("NLP_SERVICE_URL", "")

