'''
import os
from functools import lru_cache
from dotenv import load_dotenv
from typing import List

# ✅ FORCE correct .env path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    # 🔹 App
    APP_NAME: str = "Medical Billing Finance API"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # 🔹 Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./medical.db")

    # 🔹 Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

    # 🔹 CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # 🔹 External APIs
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")


@lru_cache()
def get_settings():
    return Settings()
'''


from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ======================
    # APP CONFIG
    # ======================
    APP_NAME: str = "Medical Billing Finance API"
    DEBUG: bool = True

    # ======================
    # DATABASE
    # ======================
    DATABASE_URL: str = "sqlite:///./medical.db"

    # ======================
    # SECURITY (JWT)
    # ======================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day

    # ======================
    # CORS
    # ======================
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # ======================
    # EXTERNAL API
    # ======================
    GROQ_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()