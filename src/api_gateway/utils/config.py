from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Assistant API"
    debug: bool = False
    api_prefix: str = "/api/v1"
    
    # NOTE JWT Settings (for future use)
    jwt_secret: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
