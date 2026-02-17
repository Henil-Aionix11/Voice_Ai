"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # LiveKit Configuration
    LIVEKIT_URL: str = "ws://localhost:7880"
    LIVEKIT_API_KEY: str = "devkey"
    LIVEKIT_API_SECRET: str = "secret"
    
    # ChromaDB Configuration
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # File Upload Configuration
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB in bytes
    
    # Application Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # API Settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Voice AI Agent"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

