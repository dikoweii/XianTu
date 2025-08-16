import os
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: Literal["development", "production"] = os.environ.get("ENVIRONMENT", "development")

    # JWT
    # 使用 'openssl rand -hex 32' 生成一个随机密钥
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 天

    # Cloudflare Turnstile
    TURNSTILE_SECRET_KEY: str = os.environ.get("TURNSTILE_SECRET_KEY", "0x4AAAAAABsSt1e6KypY0RwVuPJP14n7zNs")

    class Config:
        case_sensitive = True

settings = Settings()
