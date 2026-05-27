from app.services.risk_reward import estimate_breakout_risk_reward, estimate_pullback_risk_reward


def test_estimate_breakout_risk_reward_uses_atr_buffer_and_2r_target() -> None:
    estimate = estimate_breakout_risk_reward(
        {
            "close": 125.0,
            "prior_high_20_day": 120.0,
            "low_20_day": 98.0,
            "atr_14": 2.0,
        }
    )

    assert estimate is not None
    assert estimate.entry == 125.0
    assert estimate.invalidation == 97.0
    assert estimate.target == 181.0
    assert estimate.risk_per_share == 28.0
    assert estimate.reward_per_share == 56.0
    assert estimate.ratio == 2.0
    assert estimate.label == "2.0:1"
    assert "0.5 ATR buffer" in estimate.method
    assert "target at 2R" in estimate.method


def test_estimate_breakout_risk_reward_accepts_configurable_assumptions() -> None:
    estimate = estimate_breakout_risk_reward(
        {
            "close": 125.0,
            "prior_high_20_day": 120.0,
            "low_20_day": 98.0,
            "atr_14": 2.0,
        },
        atr_buffer_multiplier=1.0,
        target_multiple=3.0,
    )

    assert estimate is not None
    assert estimate.invalidation == 96.0
    assert estimate.target == 212.0
    assert estimate.risk_per_share == 29.0
    assert estimate.reward_per_share == 87.0
    assert estimate.ratio == 3.0
    assert estimate.label == "3.0:1"
    assert "1 ATR buffer" in estimate.method
    assert "target at 3R" in estimate.method


def test_estimate_breakout_risk_reward_returns_none_when_inputs_missing() -> None:
    assert estimate_breakout_risk_reward({"close": 125.0}) is None


def test_estimate_breakout_risk_reward_returns_none_when_risk_is_invalid() -> None:
    estimate = estimate_breakout_risk_reward(
        {
            "close": 90.0,
            "prior_high_20_day": 120.0,
            "low_20_day": 100.0,
            "atr_14": 2.0,
        }
    )

    assert estimate is None


def test_estimate_breakout_risk_reward_returns_none_when_config_is_invalid() -> None:
    estimate = estimate_breakout_risk_reward(
        {
            "close": 125.0,
            "prior_high_20_day": 120.0,
            "low_20_day": 98.0,
            "atr_14": 2.0,
        },
        atr_buffer_multiplier=0,
        target_multiple=2.0,
    )

    assert estimate is None


def test_estimate_pullback_risk_reward_uses_sma_50_or_recent_low_anchor() -> None:
    estimate = estimate_pullback_risk_reward(
        {
            "close": 126.0,
            "sma_50": 116.0,
            "low_20_day": 119.0,
            "atr_14": 2.0,
        }
    )

    assert estimate is not None
    assert estimate.entry == 126.0
    assert estimate.invalidation == 115.0
    assert estimate.target == 148.0
    assert estimate.risk_per_share == 11.0
    assert estimate.reward_per_share == 22.0
    assert estimate.ratio == 2.0
    assert estimate.label == "2.0:1"
    assert "50-day SMA/recent 20-day low" in estimate.method


def test_estimate_pullback_risk_reward_returns_none_when_inputs_missing() -> None:
    assert estimate_pullback_risk_reward({"close": 126.0}) is None
