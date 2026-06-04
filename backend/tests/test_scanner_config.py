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
