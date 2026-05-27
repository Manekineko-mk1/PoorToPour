from app.models.risk import RiskRewardEstimate


def score_breakout(snapshot: dict, risk_reward: RiskRewardEstimate | None, caution_flags: list[str]) -> dict[str, int]:
    return {
        "setup_break_above_prior_20_day_high": 25 if snapshot["close_above_prior_20_day_high"] else 0,
        "setup_break_above_prior_50_day_high": 10 if snapshot["close_above_prior_50_day_high"] else 0,
        "trend_close_above_sma_20": 10 if snapshot["close_above_sma_20"] else 0,
        "trend_close_above_sma_50": 10 if snapshot["close_above_sma_50"] else 0,
        "volume_relative_volume_1_5x": 15 if snapshot["relative_volume_20"] >= 1.5 else 0,
        "volume_relative_volume_2_0x": 5 if snapshot["relative_volume_20"] >= 2 else 0,
        "leadership_near_52_week_high": 10
        if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -10
        else 0,
        "risk_reward_estimate_present": 10 if risk_reward is not None else 0,
        "risk_reward_ratio_2r_or_better": 5 if risk_reward is not None and risk_reward.ratio >= 2 else 0,
        "caution_penalty": -min(15, len(caution_flags) * 5),
    }


def score_pullback(snapshot: dict, risk_reward: RiskRewardEstimate | None, caution_flags: list[str]) -> dict[str, int]:
    return {
        "setup_near_20_day_support": 20 if _near_reference(snapshot["close"], snapshot["sma_20"], 3) else 0,
        "setup_near_21_day_ema": 15 if _near_reference(snapshot["close"], snapshot["ema_21"], 3) else 0,
        "trend_close_above_sma_20": 10 if snapshot["close_above_sma_20"] else 0,
        "trend_close_above_sma_50": 20 if snapshot["close_above_sma_50"] else 0,
        "volume_constructive_pullback": 10
        if snapshot["relative_volume_20"] is not None and 0.7 <= snapshot["relative_volume_20"] <= 1.3
        else 0,
        "leadership_near_52_week_high": 10
        if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -15
        else 0,
        "risk_reward_estimate_present": 10 if risk_reward is not None else 0,
        "risk_reward_ratio_2r_or_better": 5 if risk_reward is not None and risk_reward.ratio >= 2 else 0,
        "caution_penalty": -min(15, len(caution_flags) * 5),
    }


def score_relative_strength_leader(
    snapshot: dict,
    risk_reward: RiskRewardEstimate | None,
    caution_flags: list[str],
) -> dict[str, int]:
    return {
        "leadership_close_near_52_week_high": 25
        if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -5
        else 0,
        "leadership_close_near_50_day_high": 15
        if snapshot["close_distance_from_50_day_high_pct"] is not None
        and snapshot["close_distance_from_50_day_high_pct"] >= -3
        else 0,
        "setup_break_above_prior_20_day_high": 15 if snapshot["close_above_prior_20_day_high"] else 0,
        "trend_close_above_sma_20": 10 if snapshot["close_above_sma_20"] else 0,
        "trend_close_above_sma_50": 15 if snapshot["close_above_sma_50"] else 0,
        "volume_relative_volume_1_0x": 5 if snapshot["relative_volume_20"] >= 1 else 0,
        "volume_relative_volume_1_5x": 5 if snapshot["relative_volume_20"] >= 1.5 else 0,
        "risk_reward_estimate_present": 5 if risk_reward is not None else 0,
        "risk_reward_ratio_2r_or_better": 5 if risk_reward is not None and risk_reward.ratio >= 2 else 0,
        "caution_penalty": -min(15, len(caution_flags) * 5),
    }


def total_score(score_breakdown: dict[str, int]) -> int:
    return max(0, min(100, sum(score_breakdown.values())))


def _near_reference(value: float | None, reference: float | None, max_distance_pct: float) -> bool:
    if value is None or reference is None or reference == 0:
        return False
    return abs(((value - reference) / reference) * 100) <= max_distance_pct
