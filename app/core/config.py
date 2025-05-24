from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Matrix Flag"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Webhook settings
    WEBHOOK_TIMEOUT: int = 5  # seconds

    # Security settings
    ALGORITHM: str = "HS256"
    PASSWORD_MIN_LENGTH: int = 8

    class Config:
        case_sensitive = True


settings = Settings()
