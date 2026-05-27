from app.models.risk import RiskRewardEstimate
from app.services.scoring import score_breakout, score_pullback, score_relative_strength_leader, total_score


def test_score_breakout_includes_risk_reward_and_caution_penalty() -> None:
    score = score_breakout(
        {
            "close_above_prior_20_day_high": True,
            "close_above_prior_50_day_high": True,
            "close_above_sma_20": True,
            "close_above_sma_50": True,
            "relative_volume_20": 2.1,
            "high_52_week_distance_pct": -2.0,
        },
        _risk_reward(),
        ["Close is extended."],
    )

    assert score["setup_break_above_prior_20_day_high"] == 25
    assert score["risk_reward_estimate_present"] == 10
    assert score["risk_reward_ratio_2r_or_better"] == 5
    assert score["caution_penalty"] == -5
    assert total_score(score) == 95


def test_total_score_is_clamped_between_zero_and_100() -> None:
    assert total_score({"a": -200}) == 0
    assert total_score({"a": 200}) == 100


def test_score_pullback_includes_support_trend_volume_and_risk_reward() -> None:
    score = score_pullback(
        {
            "close": 126.0,
            "sma_20": 125.0,
            "ema_21": 124.5,
            "close_above_sma_20": True,
            "close_above_sma_50": True,
            "relative_volume_20": 1.0,
            "high_52_week_distance_pct": -8.0,
        },
        _risk_reward(),
        [],
    )

    assert score["setup_near_20_day_support"] == 20
    assert score["setup_near_21_day_ema"] == 15
    assert score["trend_close_above_sma_50"] == 20
    assert score["volume_constructive_pullback"] == 10
    assert score["risk_reward_ratio_2r_or_better"] == 5
    assert total_score(score) == 100


def test_score_relative_strength_leader_includes_leadership_trend_and_volume() -> None:
    score = score_relative_strength_leader(
        {
            "high_52_week_distance_pct": -2.0,
            "close_distance_from_50_day_high_pct": -1.0,
            "close_above_prior_20_day_high": True,
            "close_above_sma_20": True,
            "close_above_sma_50": True,
            "relative_volume_20": 1.6,
        },
        _risk_reward(),
        [],
    )

    assert score["leadership_close_near_52_week_high"] == 25
    assert score["leadership_close_near_50_day_high"] == 15
    assert score["setup_break_above_prior_20_day_high"] == 15
    assert score["volume_relative_volume_1_5x"] == 5
    assert total_score(score) == 100


def _risk_reward() -> RiskRewardEstimate:
    return RiskRewardEstimate(
        entry=125.0,
        invalidation=97.0,
        target=181.0,
        risk_per_share=28.0,
        reward_per_share=56.0,
        ratio=2.0,
        label="2.0:1",
        method="unit",
    )
