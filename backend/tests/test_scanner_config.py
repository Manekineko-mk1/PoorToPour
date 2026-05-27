import pytest
from pydantic import ValidationError

from app.core.config import Settings


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
