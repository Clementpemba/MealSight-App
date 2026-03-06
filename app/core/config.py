from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project Info
    PROJECT_NAME: str = "MealSight API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "MealSight Backend API"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_7plRgCjifP1b@ep-falling-sun-airlm6hh-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Redis (optional - for caching)
    REDIS_URL: str = "redis://localhost:6379"
    
    # External APIs
    # OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
