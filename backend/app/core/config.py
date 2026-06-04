import logging
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

_legacy_env_warning_emitted = False


def _warn_legacy_env_var_once() -> None:
    """Log the POORTOPOUR_ENV deprecation at most once per process."""
    global _legacy_env_warning_emitted
    if _legacy_env_warning_emitted:
        return
    _legacy_env_warning_emitted = True
    logger.warning(
        "POORTOPOUR_ENV is deprecated and will be removed in a future release. "
        "Rename it to POORTOPOUR_ENVIRONMENT.",
    )


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
    log_dir: str = "logs"
    log_retention_days: int = Field(default=3, gt=0)
    log_max_bytes: int = Field(default=10 * 1024 * 1024, gt=0)

    # Legacy alias for ``environment``. Read through the settings sources (via the
    # explicit validation alias) so the migration does not touch os.environ
    # directly. Excluded from serialization; only used to drive the migration.
    legacy_environment: str | None = Field(
        default=None,
        validation_alias="POORTOPOUR_ENV",
        exclude=True,
    )

    @model_validator(mode="after")
    def _migrate_legacy_env_var(self) -> "Settings":
        # The legacy var is honored only when the canonical ``environment``
        # (POORTOPOUR_ENVIRONMENT / init kwarg) was not explicitly supplied.
        if self.legacy_environment is not None and "environment" not in self.model_fields_set:
            _warn_legacy_env_var_once()
            self.environment = self.legacy_environment
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POORTOPOUR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
