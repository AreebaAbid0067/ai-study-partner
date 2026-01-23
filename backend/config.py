from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./ai_study_partner.db"
    # For production, use PostgreSQL:
    # DATABASE_URL: str = "postgresql://user:password@localhost/ai_study_partner"
    
    # App Configuration
    APP_NAME: str = "AI Study Partner API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
