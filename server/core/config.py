from typing import Literal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    _env_file = Path(__file__).resolve().parents[1] / ".env"
    model_config = SettingsConfigDict(
        env_file=str(_env_file),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENVIRONMENT: Literal["development", "production"] = "development"

    # JWT
    # 使用 `openssl rand -hex 32` 生成一个随机密钥；生产环境务必通过环境变量注入。
    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 天

    # Cloudflare Turnstile
    TURNSTILE_ENABLED: bool = True
    TURNSTILE_SECRET_KEY: str | None = None
    TURNSTILE_VERIFY_URL: str = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    # Database (optional, used by server/database.py via env)
    DDCT_DB_URL: str | None = None

settings = Settings()
