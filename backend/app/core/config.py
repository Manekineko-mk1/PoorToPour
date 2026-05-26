from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"
    provider: str = "mock"
    database_url: str = "postgresql://poortopour:poortopour@db:5432/poortopour"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POORTOPOUR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
