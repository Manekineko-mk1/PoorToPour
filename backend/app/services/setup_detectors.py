from datetime import UTC, date, datetime

from app.core.config import Settings, get_settings
from app.models.indicators import IndicatorSnapshot
from app.models.market_data import DailyBar, SymbolProfile
from app.models.risk import RiskRewardEstimate
from app.models.scans import ScanCandidate
from app.services.indicators import IndicatorService
from app.services.risk_reward import estimate_breakout_risk_reward, estimate_pullback_risk_reward
from app.services.scoring import score_breakout, score_pullback, score_relative_strength_leader, total_score
from app.services.status_rules import CandidateStatusInput, determine_candidate_status


MAX_PRICE_DATA_AGE_DAYS = 7
RISK_REWARD_UNAVAILABLE_WARNING = "Risk/reward estimate is unavailable."


class BreakoutDetector:
    """Deterministic breakout setup detector.

    Phase 2 keeps this conservative: candidate status is assigned by shared
    status rules after setup evidence, scoring, and risk/reward are computed.
    """

    def __init__(self, indicator_service: IndicatorService | None = None, settings: Settings | None = None) -> None:
        self.indicator_service = indicator_service or IndicatorService()
        self.settings = settings or get_settings()

    def detect(
        self,
        symbol: SymbolProfile,
        bars: list[DailyBar],
        now: datetime | None = None,
    ) -> ScanCandidate | None:
        completed_at = now or datetime.now(UTC)
        if len(bars) < 50:
            return _blocked_candidate(
                symbol=symbol,
                bars=bars,
                setup="Breakout",
                reason="At least 50 daily bars are required for breakout detection.",
                completed_at=completed_at,
            )

        snapshot = self.indicator_service.build_snapshot(symbol.symbol, bars)
        snapshot_payload = snapshot.model_dump()
        missing_fields = _missing_required_fields(snapshot_payload)
        if missing_fields:
            caution_flags = [f"Missing required breakout inputs: {', '.join(missing_fields)}."]
            return _candidate(
                symbol=symbol,
                snapshot=snapshot_payload,
                setup="Breakout",
                status=determine_candidate_status(
                    CandidateStatusInput(
                        score=0,
                        setup_confirmed=False,
                        caution_flags=caution_flags,
                        missing_required_fields=missing_fields,
                    )
                ),
                score=0,
                score_breakdown={},
                reasons=[],
                caution_flags=caution_flags,
                completed_at=completed_at,
            )

        reasons = _breakout_reasons(snapshot_payload)
        caution_flags = _breakout_caution_flags(snapshot_payload)
        price_data_fresh = _is_price_data_fresh(snapshot_payload, completed_at)
        if not price_data_fresh:
            caution_flags.append(_stale_price_data_warning(snapshot_payload))
        risk_reward = estimate_breakout_risk_reward(
            snapshot_payload,
            atr_buffer_multiplier=self.settings.scanner_risk_reward_atr_buffer_multiplier,
            target_multiple=self.settings.scanner_risk_reward_target_multiple,
        )
        _append_risk_reward_caution(caution_flags, risk_reward)

        score_breakdown = score_breakout(snapshot_payload, risk_reward, caution_flags)
        score = total_score(score_breakdown)

        confirmed_breakout = (
            snapshot.close_above_prior_20_day_high is True
            and snapshot.close_above_sma_20 is True
            and snapshot.close_above_sma_50 is True
            and snapshot.relative_volume_20 is not None
            and snapshot.relative_volume_20 >= 1.5
        )
        near_breakout = (
            snapshot.close_distance_from_20_day_high_pct is not None
            and snapshot.close_distance_from_20_day_high_pct >= -2
            and snapshot.close_above_sma_20 is True
            and snapshot.close_above_sma_50 is True
        )

        if not confirmed_breakout and not near_breakout:
            return None

        if confirmed_breakout:
            reasons.insert(0, "Close broke above the prior 20-day high.")
        else:
            caution_flags.append("Breakout not confirmed yet; price is near the 20-day high.")

        status = determine_candidate_status(
            CandidateStatusInput(
                score=score,
                setup_confirmed=confirmed_breakout,
                setup_detected=confirmed_breakout or near_breakout,
                risk_reward=risk_reward,
                caution_flags=caution_flags,
                price_data_fresh=price_data_fresh,
            )
        )

        return _candidate(
            symbol=symbol,
            snapshot=snapshot_payload,
            setup="Breakout",
            status=status,
            score=score,
            score_breakdown=score_breakdown,
            risk_reward=risk_reward.model_dump() if risk_reward else None,
            reasons=reasons,
            caution_flags=caution_flags,
            completed_at=completed_at,
        )


class PullbackContinuationDetector:
    """Deterministic pullback-continuation setup detector."""

    def __init__(self, indicator_service: IndicatorService | None = None, settings: Settings | None = None) -> None:
        self.indicator_service = indicator_service or IndicatorService()
        self.settings = settings or get_settings()

    def detect(
        self,
        symbol: SymbolProfile,
        bars: list[DailyBar],
        now: datetime | None = None,
    ) -> ScanCandidate | None:
        completed_at = now or datetime.now(UTC)
        if len(bars) < 50:
            return _blocked_candidate(
                symbol=symbol,
                bars=bars,
                setup="Pullback Continuation",
                reason="At least 50 daily bars are required for pullback continuation detection.",
                completed_at=completed_at,
            )

        snapshot = self.indicator_service.build_snapshot(symbol.symbol, bars)
        snapshot_payload = snapshot.model_dump()
        missing_fields = _missing_pullback_required_fields(snapshot_payload)
        if missing_fields:
            caution_flags = [f"Missing required pullback inputs: {', '.join(missing_fields)}."]
            return _candidate(
                symbol=symbol,
                snapshot=snapshot_payload,
                setup="Pullback Continuation",
                status=determine_candidate_status(
                    CandidateStatusInput(
                        score=0,
                        setup_confirmed=False,
                        caution_flags=caution_flags,
                        missing_required_fields=missing_fields,
                    )
                ),
                score=0,
                score_breakdown={},
                reasons=[],
                caution_flags=caution_flags,
                completed_at=completed_at,
            )

        reasons = _pullback_reasons(snapshot_payload)
        caution_flags = _pullback_caution_flags(snapshot_payload)
        price_data_fresh = _is_price_data_fresh(snapshot_payload, completed_at)
        if not price_data_fresh:
            caution_flags.append(_stale_price_data_warning(snapshot_payload))
        risk_reward = estimate_pullback_risk_reward(
            snapshot_payload,
            atr_buffer_multiplier=self.settings.scanner_risk_reward_atr_buffer_multiplier,
            target_multiple=self.settings.scanner_risk_reward_target_multiple,
        )
        _append_risk_reward_caution(caution_flags, risk_reward)

        score_breakdown = score_pullback(snapshot_payload, risk_reward, caution_flags)
        score = total_score(score_breakdown)

        near_support = _near_reference(snapshot.close, snapshot.sma_20, 3) or _near_reference(snapshot.close, snapshot.ema_21, 3)
        confirmed_pullback = (
            near_support
            and snapshot.close_above_sma_20 is True
            and snapshot.close_above_sma_50 is True
            and snapshot.relative_volume_20 is not None
            and snapshot.relative_volume_20 >= 0.7
        )
        developing_pullback = (
            near_support
            and snapshot.close_above_sma_50 is True
            and snapshot.close_above_prior_20_day_high is not True
        )

        if not confirmed_pullback and not developing_pullback:
            return None

        if confirmed_pullback:
            reasons.insert(0, "Price is holding near short-term moving-average support.")
        else:
            caution_flags.append("Pullback is still developing; price has not reclaimed short-term support.")

        status = determine_candidate_status(
            CandidateStatusInput(
                score=score,
                setup_confirmed=confirmed_pullback,
                setup_detected=confirmed_pullback or developing_pullback,
                risk_reward=risk_reward,
                caution_flags=caution_flags,
                price_data_fresh=price_data_fresh,
            )
        )

        return _candidate(
            symbol=symbol,
            snapshot=snapshot_payload,
            setup="Pullback Continuation",
            status=status,
            score=score,
            score_breakdown=score_breakdown,
            risk_reward=risk_reward.model_dump() if risk_reward else None,
            reasons=reasons,
            caution_flags=caution_flags,
            completed_at=completed_at,
        )


class RelativeStrengthLeaderDetector:
    """Deterministic relative-strength leader proxy detector.

    This Phase 2 version uses price leadership and trend evidence only. A true
    benchmark-relative return comparison can be added once benchmark bars are
    part of scanner input.
    """

    def __init__(self, indicator_service: IndicatorService | None = None, settings: Settings | None = None) -> None:
        self.indicator_service = indicator_service or IndicatorService()
        self.settings = settings or get_settings()

    def detect(
        self,
        symbol: SymbolProfile,
        bars: list[DailyBar],
        now: datetime | None = None,
    ) -> ScanCandidate | None:
        completed_at = now or datetime.now(UTC)
        if len(bars) < 50:
            return _blocked_candidate(
                symbol=symbol,
                bars=bars,
                setup="Relative Strength Leader",
                reason="At least 50 daily bars are required for relative strength leader detection.",
                completed_at=completed_at,
            )

        snapshot = self.indicator_service.build_snapshot(symbol.symbol, bars)
        snapshot_payload = snapshot.model_dump()
        missing_fields = _missing_relative_strength_required_fields(snapshot_payload)
        if missing_fields:
            caution_flags = [f"Missing required relative strength inputs: {', '.join(missing_fields)}."]
            return _candidate(
                symbol=symbol,
                snapshot=snapshot_payload,
                setup="Relative Strength Leader",
                status=determine_candidate_status(
                    CandidateStatusInput(
                        score=0,
                        setup_confirmed=False,
                        caution_flags=caution_flags,
                        missing_required_fields=missing_fields,
                    )
                ),
                score=0,
                score_breakdown={},
                reasons=[],
                caution_flags=caution_flags,
                completed_at=completed_at,
            )

        reasons = _relative_strength_reasons(snapshot_payload)
        caution_flags = _relative_strength_caution_flags(snapshot_payload)
        price_data_fresh = _is_price_data_fresh(snapshot_payload, completed_at)
        if not price_data_fresh:
            caution_flags.append(_stale_price_data_warning(snapshot_payload))
        risk_reward = estimate_breakout_risk_reward(
            snapshot_payload,
            atr_buffer_multiplier=self.settings.scanner_risk_reward_atr_buffer_multiplier,
            target_multiple=self.settings.scanner_risk_reward_target_multiple,
        )
        _append_risk_reward_caution(caution_flags, risk_reward)

        score_breakdown = score_relative_strength_leader(snapshot_payload, risk_reward, caution_flags)
        score = total_score(score_breakdown)

        confirmed_leader, developing_leader = _relative_strength_signal_state(snapshot)

        if not confirmed_leader and not developing_leader:
            return None

        _annotate_relative_strength_confirmation(confirmed_leader, reasons, caution_flags)

        status = determine_candidate_status(
            CandidateStatusInput(
                score=score,
                setup_confirmed=confirmed_leader,
                setup_detected=confirmed_leader or developing_leader,
                risk_reward=risk_reward,
                caution_flags=caution_flags,
                price_data_fresh=price_data_fresh,
            )
        )

        return _candidate(
            symbol=symbol,
            snapshot=snapshot_payload,
            setup="Relative Strength Leader",
            status=status,
            score=score,
            score_breakdown=score_breakdown,
            risk_reward=risk_reward.model_dump() if risk_reward else None,
            reasons=reasons,
            caution_flags=caution_flags,
            completed_at=completed_at,
        )


def _missing_required_fields(snapshot: dict) -> list[str]:
    required_fields = [
        "close",
        "sma_20",
        "sma_50",
        "prior_high_20_day",
        "relative_volume_20",
        "atr_14",
    ]
    return [field for field in required_fields if snapshot.get(field) is None]


def _missing_pullback_required_fields(snapshot: dict) -> list[str]:
    required_fields = [
        "close",
        "sma_20",
        "sma_50",
        "ema_21",
        "relative_volume_20",
        "atr_14",
        "low_20_day",
    ]
    return [field for field in required_fields if snapshot.get(field) is None]


def _missing_relative_strength_required_fields(snapshot: dict) -> list[str]:
    required_fields = [
        "close",
        "sma_20",
        "sma_50",
        "prior_high_20_day",
        "relative_volume_20",
        "atr_14",
        "low_20_day",
        "close_distance_from_50_day_high_pct",
    ]
    return [field for field in required_fields if snapshot.get(field) is None]


def _breakout_reasons(snapshot: dict) -> list[str]:
    reasons = []
    if snapshot["close_above_prior_50_day_high"]:
        reasons.append("Close also broke above the prior 50-day high.")
    if snapshot["close_above_sma_20"]:
        reasons.append("Close is above the 20-day simple moving average.")
    if snapshot["close_above_sma_50"]:
        reasons.append("Close is above the 50-day simple moving average.")
    if snapshot["relative_volume_20"] >= 1.5:
        reasons.append("Relative volume is at least 1.5x the 20-day average.")
    if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -10:
        reasons.append("Close is within 10% of the 52-week high.")
    return reasons


def _breakout_caution_flags(snapshot: dict) -> list[str]:
    caution_flags = list(snapshot.get("warnings", []))

    if snapshot["relative_volume_20"] < 1.5:
        caution_flags.append("Relative volume is below the 1.5x breakout confirmation threshold.")

    if _is_extended_from_sma_20(snapshot):
        caution_flags.append("Close is extended above the 20-day moving average.")

    if snapshot["close_position_in_20_day_range_pct"] is not None and snapshot["close_position_in_20_day_range_pct"] > 100:
        caution_flags.append("Close is above the recent 20-day range; wait for a cleaner risk/reward estimate.")

    return caution_flags


def _is_extended_from_sma_20(snapshot: dict) -> bool:
    sma_20 = snapshot.get("sma_20")
    atr_14 = snapshot.get("atr_14")
    close = snapshot.get("close")
    if sma_20 is None or atr_14 is None or close is None:
        return False
    return close > sma_20 + (2 * atr_14)


def _pullback_reasons(snapshot: dict) -> list[str]:
    reasons = []
    if _near_reference(snapshot["close"], snapshot["sma_20"], 3):
        reasons.append("Close is near the 20-day simple moving average.")
    if _near_reference(snapshot["close"], snapshot["ema_21"], 3):
        reasons.append("Close is near the 21-day exponential moving average.")
    if snapshot["close_above_sma_20"]:
        reasons.append("Close is above the 20-day simple moving average.")
    if snapshot["close_above_sma_50"]:
        reasons.append("Close is above the 50-day simple moving average.")
    if snapshot["relative_volume_20"] is not None and 0.7 <= snapshot["relative_volume_20"] <= 1.3:
        reasons.append("Volume is constructive for a pullback continuation setup.")
    if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -15:
        reasons.append("Close remains within 15% of the 52-week high.")
    return reasons


def _pullback_caution_flags(snapshot: dict) -> list[str]:
    caution_flags = list(snapshot.get("warnings", []))

    if snapshot["close_above_sma_20"] is not True:
        caution_flags.append("Close has not reclaimed the 20-day moving average.")

    if snapshot["relative_volume_20"] < 0.7:
        caution_flags.append("Relative volume is light; continuation confirmation is weak.")

    if snapshot["relative_volume_20"] > 1.5:
        caution_flags.append("Relative volume is elevated for a pullback; review for distribution risk.")

    if snapshot["close_above_prior_20_day_high"] is True:
        caution_flags.append("Price already broke above the prior 20-day high; classify as breakout first.")

    return caution_flags


def _relative_strength_reasons(snapshot: dict) -> list[str]:
    reasons = []
    if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -5:
        reasons.append("Close is within 5% of the 52-week high.")
    if snapshot["close_distance_from_50_day_high_pct"] is not None and snapshot["close_distance_from_50_day_high_pct"] >= -3:
        reasons.append("Close is within 3% of the 50-day high.")
    if snapshot["close_above_prior_20_day_high"]:
        reasons.append("Close is above the prior 20-day high.")
    if snapshot["close_above_sma_20"]:
        reasons.append("Close is above the 20-day simple moving average.")
    if snapshot["close_above_sma_50"]:
        reasons.append("Close is above the 50-day simple moving average.")
    if snapshot["relative_volume_20"] >= 1:
        reasons.append("Volume is at or above the 20-day average.")
    return reasons


def _relative_strength_caution_flags(snapshot: dict) -> list[str]:
    caution_flags = list(snapshot.get("warnings", []))

    if snapshot["high_52_week_distance_pct"] is None:
        caution_flags.append("52-week high confirmation is unavailable; using shorter-term leadership proxy.")

    if snapshot["relative_volume_20"] < 1:
        caution_flags.append("Relative volume is below the 20-day average.")

    if snapshot["close_above_prior_20_day_high"] is not True:
        caution_flags.append("Close has not cleared the prior 20-day high.")

    return caution_flags


def _relative_strength_signal_state(snapshot: IndicatorSnapshot) -> tuple[bool, bool]:
    near_52_week_high = _is_at_or_above(snapshot.high_52_week_distance_pct, -5)
    near_50_day_high = _is_at_or_above(snapshot.close_distance_from_50_day_high_pct, -3)
    trend_confirmed = snapshot.close_above_sma_20 is True and snapshot.close_above_sma_50 is True
    volume_confirmed = snapshot.relative_volume_20 is not None and snapshot.relative_volume_20 >= 1

    confirmed_leader = near_52_week_high and trend_confirmed and volume_confirmed
    developing_leader = (near_52_week_high or near_50_day_high) and trend_confirmed
    return confirmed_leader, developing_leader


def _annotate_relative_strength_confirmation(
    confirmed_leader: bool,
    reasons: list[str],
    caution_flags: list[str],
) -> None:
    if confirmed_leader:
        reasons.insert(0, "Price leadership is near the 52-week high with trend confirmation.")
    else:
        caution_flags.append("Relative strength is based on shorter-term price leadership; 52-week confirmation is incomplete.")


def _is_at_or_above(value: float | None, threshold: float) -> bool:
    return value is not None and value >= threshold


def _near_reference(value: float | None, reference: float | None, max_distance_pct: float) -> bool:
    if value is None or reference is None or reference == 0:
        return False
    return abs(((value - reference) / reference) * 100) <= max_distance_pct


def _append_risk_reward_caution(caution_flags: list[str], risk_reward: RiskRewardEstimate | None) -> None:
    if risk_reward is None:
        caution_flags.append(RISK_REWARD_UNAVAILABLE_WARNING)


def _is_price_data_fresh(snapshot: dict, completed_at: datetime) -> bool:
    latest_date = snapshot.get("latest_date")
    if not latest_date:
        return False
    try:
        parsed_latest_date = date.fromisoformat(latest_date)
    except ValueError:
        return False
    return (completed_at.date() - parsed_latest_date).days <= MAX_PRICE_DATA_AGE_DAYS


def _stale_price_data_warning(snapshot: dict) -> str:
    latest_date = snapshot.get("latest_date", "unknown")
    return f"Price data is stale; latest bar is {latest_date}."


def _blocked_candidate(
    symbol: SymbolProfile,
    bars: list[DailyBar],
    setup: str,
    reason: str,
    completed_at: datetime,
) -> ScanCandidate:
    latest = max(bars, key=lambda bar: bar.date) if bars else None
    return ScanCandidate(
        rank=0,
        symbol=symbol.symbol,
        company_name=symbol.company_name,
        setup=setup,
        status="Blocked",
        score=0,
        price=latest.close if latest else None,
        relative_volume=None,
        rsi=None,
        risk_reward=None,
        indicator_snapshot=None,
        score_breakdown={},
        reasons=[],
        caution_flags=[reason],
        last_updated=_format_datetime(completed_at),
    )


def _candidate(
    symbol: SymbolProfile,
    snapshot: dict,
    setup: str,
    status: str,
    score: int,
    score_breakdown: dict[str, int],
    reasons: list[str],
    caution_flags: list[str],
    completed_at: datetime,
    risk_reward: dict | None = None,
) -> ScanCandidate:
    return ScanCandidate(
        rank=0,
        symbol=symbol.symbol,
        company_name=symbol.company_name,
        setup=setup,
        status=status,
        score=score,
        price=snapshot["close"],
        relative_volume=snapshot["relative_volume_20"],
        rsi=None,
        risk_reward=risk_reward["label"] if risk_reward else None,
        indicator_snapshot=snapshot,
        score_breakdown={**score_breakdown, "risk_reward": risk_reward} if risk_reward else score_breakdown,
        reasons=reasons,
        caution_flags=caution_flags,
        last_updated=_format_datetime(completed_at),
    )


def _format_datetime(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
