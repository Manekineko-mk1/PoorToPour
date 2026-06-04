import os
import warnings
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"
    provider: str = "mock"
    database_url: str = "postgresql://poortopour:poortopour@db:5432/poortopour"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    alpha_vantage_api_key: str = ""
    alpha_vantage_daily_function: str = "TIME_SERIES_DAILY"
    scanner_risk_reward_atr_buffer_multiplier: float = Field(default=0.5, gt=0)
    scanner_risk_reward_target_multiple: float = Field(default=2.0, gt=0)
    allow_hosted_manual_scan: bool = False
    hosted_manual_scan_max_symbols: int = Field(default=25, gt=0)
    manual_scan_api_key: str = ""
    manual_scan_rate_limit: int = Field(default=5, gt=0)

    @model_validator(mode="before")
    @classmethod
    def _migrate_legacy_env_var(cls, values: dict) -> dict:
        old = os.environ.get("POORTOPOUR_ENV")
        new = os.environ.get("POORTOPOUR_ENVIRONMENT")
        if old is not None and new is None:
            warnings.warn(
                "POORTOPOUR_ENV is deprecated and will be removed in a future release. "
                "Rename it to POORTOPOUR_ENVIRONMENT.",
                DeprecationWarning,
                stacklevel=2,
            )
            values.setdefault("environment", old)
        return values

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POORTOPOUR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
