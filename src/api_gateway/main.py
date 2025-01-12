from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import bot
from .middleware.auth import AuthMiddleware
from .middleware.logging import LoggingMiddleware
from .utils.config import Settings

settings = Settings()

app = FastAPI(
    title="AI Assistant API",
    description="API for handling bot requests and AI assistant interactions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Routers
app.include_router(bot.router, prefix="/api/v1", tags=["bot", "consultant"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
