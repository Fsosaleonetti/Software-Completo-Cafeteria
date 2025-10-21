from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Cafetería POS"
    environment: str = Field(default="development", description="Nombre del entorno")
    secret_key: str = Field(default="changeme", description="Clave secreta JWT")
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    database_url: str = Field(default="sqlite+aiosqlite:///./cafeteria.db")
    sync_database_url: str = Field(default="sqlite:///./cafeteria.db")

    cors_origins: List[AnyHttpUrl] | List[str] = Field(default_factory=list)

    mercado_pago_access_token: str | None = None
    whatsapp_token: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
