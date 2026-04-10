import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Zeno"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/zeno")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT Authentication Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-jwt-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

