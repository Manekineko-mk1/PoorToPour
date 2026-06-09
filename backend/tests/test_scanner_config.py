import logging

import pytest
from pydantic import ValidationError

import app.core.config as config
from app.core.config import Settings


@pytest.fixture
def reset_legacy_warning() -> None:
    config._legacy_env_warning_emitted = False
    yield
    config._legacy_env_warning_emitted = False


def test_scanner_risk_reward_settings_have_conservative_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.scanner_risk_reward_atr_buffer_multiplier == 0.5
    assert settings.scanner_risk_reward_target_multiple == 2.0


def test_scanner_risk_reward_settings_can_be_overridden() -> None:
    settings = Settings(
        scanner_risk_reward_atr_buffer_multiplier=1.0,
        scanner_risk_reward_target_multiple=3.0,
        _env_file=None,
    )

    assert settings.scanner_risk_reward_atr_buffer_multiplier == 1.0
    assert settings.scanner_risk_reward_target_multiple == 3.0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scanner_risk_reward_atr_buffer_multiplier", 0),
        ("scanner_risk_reward_target_multiple", 0),
    ],
)
def test_scanner_risk_reward_settings_reject_non_positive_values(field: str, value: float) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value}, _env_file=None)


def test_log_level_defaults_to_info() -> None:
    assert Settings(_env_file=None).log_level == "INFO"


def test_scheduled_scan_defaults_to_6am_eastern_with_local_catchup() -> None:
    settings = Settings(_env_file=None)

    assert settings.scheduled_scan_enabled is True
    assert settings.scheduled_scan_time == "06:00"
    assert settings.scheduled_scan_timezone == "America/New_York"
    assert settings.scheduled_scan_refresh_period == "1y"
    assert settings.scheduled_scan_max_symbols is None
    assert settings.scheduled_scan_startup_catchup is True


def test_scheduled_scan_time_is_normalized() -> None:
    assert Settings(scheduled_scan_time="6:05", _env_file=None).scheduled_scan_time == "06:05"


def test_scheduled_scan_timezone_accepts_known_timezone() -> None:
    assert Settings(scheduled_scan_timezone="America/New_York", _env_file=None).scheduled_scan_timezone == "America/New_York"


def test_scheduled_scan_timezone_falls_back_to_utc_for_unknown_value(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(scheduled_scan_timezone="Mars/Base", _env_file=None)

    assert settings.scheduled_scan_timezone == "UTC"
    assert "Unknown scheduled_scan_timezone" in caplog.text


def test_blank_scheduled_scan_timezone_falls_back_to_utc(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(scheduled_scan_timezone="   ", _env_file=None)

    assert settings.scheduled_scan_timezone == "UTC"
    assert "Blank scheduled_scan_timezone" in caplog.text


def test_blank_scheduled_scan_max_symbols_is_unlimited() -> None:
    settings = Settings(scheduled_scan_max_symbols="", _env_file=None)

    assert settings.scheduled_scan_max_symbols is None


@pytest.mark.parametrize("value", ["24:00", "06:60", "bogus", "6"])
def test_scheduled_scan_time_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(scheduled_scan_time=value, _env_file=None)


def test_scheduled_scan_period_rejects_unknown_values() -> None:
    with pytest.raises(ValidationError):
        Settings(scheduled_scan_refresh_period="bogus", _env_file=None)


def test_log_level_is_normalized_to_upper_case() -> None:
    assert Settings(log_level="debug", _env_file=None).log_level == "DEBUG"


def test_log_level_rejects_unknown_values() -> None:
    with pytest.raises(ValidationError):
        Settings(log_level="verbose", _env_file=None)


def test_legacy_env_var_migrates_to_environment(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.delenv("POORTOPOUR_ENVIRONMENT", raising=False)
    monkeypatch.setenv("POORTOPOUR_ENV", "production")

    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(_env_file=None)

    assert settings.environment == "production"
    assert "POORTOPOUR_ENV is deprecated" in caplog.text


def test_canonical_env_var_takes_precedence_over_legacy(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.setenv("POORTOPOUR_ENVIRONMENT", "staging")
    monkeypatch.setenv("POORTOPOUR_ENV", "production")

    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(_env_file=None)

    assert settings.environment == "staging"
    assert "deprecated" not in caplog.text


def test_blank_canonical_env_var_does_not_override_legacy(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.setenv("POORTOPOUR_ENVIRONMENT", "")
    monkeypatch.setenv("POORTOPOUR_ENV", "production")

    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(_env_file=None)

    assert settings.environment == "production"
    assert "POORTOPOUR_ENV is deprecated" in caplog.text


def test_blank_canonical_env_var_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.setenv("POORTOPOUR_ENVIRONMENT", "   ")
    monkeypatch.delenv("POORTOPOUR_ENV", raising=False)

    settings = Settings(_env_file=None)

    assert settings.environment == "local"


def test_blank_legacy_env_var_is_ignored(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.delenv("POORTOPOUR_ENVIRONMENT", raising=False)
    monkeypatch.setenv("POORTOPOUR_ENV", "   ")

    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        settings = Settings(_env_file=None)

    assert settings.environment == "local"
    assert "deprecated" not in caplog.text


def test_legacy_env_var_deprecation_warns_only_once(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    reset_legacy_warning: None,
) -> None:
    monkeypatch.delenv("POORTOPOUR_ENVIRONMENT", raising=False)
    monkeypatch.setenv("POORTOPOUR_ENV", "production")

    with caplog.at_level(logging.WARNING, logger="app.core.config"):
        Settings(_env_file=None)
        Settings(_env_file=None)

    assert caplog.text.count("POORTOPOUR_ENV is deprecated") == 1
