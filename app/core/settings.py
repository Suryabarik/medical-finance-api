from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # APP
    APP_NAME: str = "Medical Billing Finance API"
    DEBUG: bool = True

    # DATABASE
    DATABASE_URL: str = "sqlite:///./medical.db"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440


    # EXTERNAL API
    GROQ_API_KEY: str | None = None   # ✅ ADD THIS FIX

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


# ✅ GLOBAL SINGLE INSTANCE (IMPORTANT FIX)
settings = get_settings()