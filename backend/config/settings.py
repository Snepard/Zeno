from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Zeno"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT Authentication
    SECRET_KEY: str = "super-secret-key-for-jwt-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Groq LLM
    GROQ_API_KEY: str = ""           # Legacy / default fallback
    GROQ_API_KEY_CLASS: str = ""     # PPT / Class generation
    GROQ_API_KEY_PODCAST: str = ""   # Podcast generation
    GROQ_API_KEY_VIDEO: str = ""     # Video generation
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_FALLBACK_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL_2: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
