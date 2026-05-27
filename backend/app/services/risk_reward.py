from app.models.risk import RiskRewardEstimate


def estimate_breakout_risk_reward(
    snapshot: dict,
    atr_buffer_multiplier: float = 0.5,
    target_multiple: float = 2.0,
) -> RiskRewardEstimate | None:
    close = snapshot.get("close")
    prior_high = snapshot.get("prior_high_20_day")
    low_20_day = snapshot.get("low_20_day")
    atr_14 = snapshot.get("atr_14")
    if close is None or prior_high is None or low_20_day is None or atr_14 is None:
        return None
    if atr_buffer_multiplier <= 0 or target_multiple <= 0:
        return None

    entry = float(close)
    invalidation_anchor = min(float(prior_high), float(low_20_day))
    invalidation = invalidation_anchor - (atr_buffer_multiplier * float(atr_14))
    risk_per_share = entry - invalidation
    if risk_per_share <= 0:
        return None

    target = entry + (target_multiple * risk_per_share)
    reward_per_share = target - entry
    ratio = reward_per_share / risk_per_share

    return RiskRewardEstimate(
        entry=round(entry, 4),
        invalidation=round(invalidation, 4),
        target=round(target, 4),
        risk_per_share=round(risk_per_share, 4),
        reward_per_share=round(reward_per_share, 4),
        ratio=round(ratio, 4),
        label=f"{ratio:.1f}:1",
        method=(
            "Breakout estimate: entry at close, invalidation below prior 20-day "
            f"high/recent 20-day low with {atr_buffer_multiplier:g} ATR buffer, "
            f"target at {target_multiple:g}R."
        ),
    )


def estimate_pullback_risk_reward(
    snapshot: dict,
    atr_buffer_multiplier: float = 0.5,
    target_multiple: float = 2.0,
) -> RiskRewardEstimate | None:
    close = snapshot.get("close")
    sma_50 = snapshot.get("sma_50")
    low_20_day = snapshot.get("low_20_day")
    atr_14 = snapshot.get("atr_14")
    if close is None or sma_50 is None or low_20_day is None or atr_14 is None:
        return None
    if atr_buffer_multiplier <= 0 or target_multiple <= 0:
        return None

    entry = float(close)
    invalidation_anchor = min(float(sma_50), float(low_20_day))
    invalidation = invalidation_anchor - (atr_buffer_multiplier * float(atr_14))
    risk_per_share = entry - invalidation
    if risk_per_share <= 0:
        return None

    target = entry + (target_multiple * risk_per_share)
    reward_per_share = target - entry
    ratio = reward_per_share / risk_per_share

    return RiskRewardEstimate(
        entry=round(entry, 4),
        invalidation=round(invalidation, 4),
        target=round(target, 4),
        risk_per_share=round(risk_per_share, 4),
        reward_per_share=round(reward_per_share, 4),
        ratio=round(ratio, 4),
        label=f"{ratio:.1f}:1",
        method=(
            "Pullback estimate: entry at close, invalidation below the lower "
            f"of 50-day SMA/recent 20-day low with {atr_buffer_multiplier:g} ATR buffer, "
            f"target at {target_multiple:g}R."
        ),
    )
