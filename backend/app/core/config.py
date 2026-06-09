import logging
from functools import lru_cache

from pydantic import Field, field_validator, model_validator
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
    # Minimum fraction (0.0-1.0) of requested symbols that must refresh
    # successfully before a manual scan is allowed to run. 0.0 preserves the
    # lenient default (any partial refresh proceeds on persisted bars with a
    # warning); 1.0 requires every symbol to refresh. Overridable per request.
    manual_scan_min_refresh_ratio: float = Field(default=0.0, ge=0, le=1)
    scheduled_scan_enabled: bool = True
    scheduled_scan_time: str = "06:00"
    scheduled_scan_timezone: str = "America/New_York"
    scheduled_scan_refresh_period: str = "1y"
    scheduled_scan_max_symbols: int | None = Field(default=None, gt=0)
    scheduled_scan_startup_catchup: bool = True
    log_dir: str = "logs"
    log_level: str = "INFO"
    log_retention_days: int = Field(default=3, gt=0)
    log_max_bytes: int = Field(default=10 * 1024 * 1024, gt=0)

    @field_validator("log_level", mode="before")
    @classmethod
    def _normalize_log_level(cls, value: object) -> str:
        # Accept any case (e.g. "debug", "Info") and reject unknown levels up
        # front so a typo fails fast at startup instead of silently defaulting.
        if not isinstance(value, str):
            raise ValueError("log_level must be a string")
        normalized = value.strip().upper()
        if normalized not in logging.getLevelNamesMapping():
            raise ValueError(
                f"Unknown log_level {value!r}; expected one of "
                f"{', '.join(sorted(logging.getLevelNamesMapping()))}"
            )
        return normalized

    @field_validator("scheduled_scan_time")
    @classmethod
    def _validate_scheduled_scan_time(cls, value: str) -> str:
        parts = value.strip().split(":")
        if len(parts) != 2:
            raise ValueError("scheduled_scan_time must use HH:MM format")
        try:
            hour, minute = (int(part) for part in parts)
        except ValueError as exc:
            raise ValueError("scheduled_scan_time must use HH:MM format") from exc
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("scheduled_scan_time must use HH:MM format")
        return f"{hour:02d}:{minute:02d}"

    @field_validator("scheduled_scan_refresh_period")
    @classmethod
    def _validate_scheduled_scan_refresh_period(cls, value: str) -> str:
        allowed = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}
        if value not in allowed:
            raise ValueError(f"scheduled_scan_refresh_period must be one of {', '.join(sorted(allowed))}")
        return value

    @field_validator("scheduled_scan_max_symbols", mode="before")
    @classmethod
    def _blank_scheduled_scan_max_symbols_as_none(cls, value: object) -> object:
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

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
        # Treat a blank canonical ``environment`` (e.g. POORTOPOUR_ENVIRONMENT="")
        # as unset: an empty value must not silently override the legacy alias or
        # leave the app running with no environment. The canonical var wins only
        # when it was explicitly supplied *and* carries a non-blank value.
        canonical_supplied = (
            "environment" in self.model_fields_set and self.environment.strip() != ""
        )
        if not canonical_supplied and self.legacy_environment is not None:
            legacy = self.legacy_environment.strip()
            if legacy:
                _warn_legacy_env_var_once()
                self.environment = legacy
        # Never let a blank value survive; fall back to the safe default so
        # downstream checks (e.g. is_local) behave predictably.
        if self.environment.strip() == "":
            self.environment = "local"
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POORTOPOUR_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
