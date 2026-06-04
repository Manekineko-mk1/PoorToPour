from collections.abc import Sequence

from app.models.market_data import (
    ChartCandidateContext,
    ChartIndicatorBar,
    CompanyProfile,
    DailyBar,
    RiskRewardOverlay,
    SymbolChartPayload,
)
from app.models.scans import ScanCandidate, ScanRun
from app.services.indicators import simple_moving_average

RSI_PERIOD = 14
CHART_SMA_PERIODS = (20, 50, 200)


def build_symbol_chart_payload(
    symbol: str,
    bars: Sequence[DailyBar],
    *,
    profile: CompanyProfile | None = None,
    candidate_context: tuple[ScanRun, ScanCandidate] | None = None,
) -> SymbolChartPayload:
    ordered_bars = sorted(bars, key=lambda bar: bar.date)
    closes = [bar.close for bar in ordered_bars]

    return SymbolChartPayload(
        symbol=symbol.upper(),
        company_name=profile.company_name if profile else None,
        exchange=profile.exchange if profile else None,
        data_date=ordered_bars[-1].date if ordered_bars else None,
        bars=[
            _chart_bar(bar, closes[: index + 1])
            for index, bar in enumerate(ordered_bars)
        ],
        candidate=_candidate_context(candidate_context),
        warnings=_chart_warnings(ordered_bars),
    )


def _chart_bar(bar: DailyBar, closes_to_date: Sequence[float]) -> ChartIndicatorBar:
    return ChartIndicatorBar(
        **bar.model_dump(),
        sma_20=_round_optional(simple_moving_average(closes_to_date, 20)),
        sma_50=_round_optional(simple_moving_average(closes_to_date, 50)),
        sma_200=_round_optional(simple_moving_average(closes_to_date, 200)),
        rsi_14=_round_optional(_relative_strength_index(closes_to_date, RSI_PERIOD)),
    )


def _candidate_context(
    candidate_context: tuple[ScanRun, ScanCandidate] | None,
) -> ChartCandidateContext | None:
    if candidate_context is None:
        return None

    scan, candidate = candidate_context
    return ChartCandidateContext(
        scan_id=scan.scan_id,
        setup=candidate.setup,
        status=candidate.status,
        score=candidate.score,
        risk_reward=candidate.risk_reward,
        reasons=candidate.reasons,
        caution_flags=candidate.caution_flags,
        risk_reward_overlay=_risk_reward_overlay(candidate),
    )


def _risk_reward_overlay(candidate: ScanCandidate) -> RiskRewardOverlay | None:
    risk_reward = (candidate.score_breakdown or {}).get("risk_reward")
    if not isinstance(risk_reward, dict):
        return None

    return RiskRewardOverlay(
        entry=_to_float_or_none(risk_reward.get("entry")),
        invalidation=_to_float_or_none(risk_reward.get("invalidation")),
        target=_to_float_or_none(risk_reward.get("target")),
        risk_per_share=_to_float_or_none(risk_reward.get("risk_per_share")),
        ratio=candidate.risk_reward,
    )


def _chart_warnings(bars: Sequence[DailyBar]) -> list[str]:
    warnings = []
    for period in CHART_SMA_PERIODS:
        if len(bars) < period:
            warnings.append(f"Only {len(bars)} bars available; SMA {period} is incomplete.")
    if len(bars) <= RSI_PERIOD:
        warnings.append(f"Only {len(bars)} bars available; RSI {RSI_PERIOD} is incomplete.")
    return warnings


def _relative_strength_index(closes: Sequence[float], period: int) -> float | None:
    # EN: Wilder's RSI. Seed with a simple average of the first `period` changes,
    # then apply Wilder's smoothing so values match standard charting platforms.
    if len(closes) <= period:
        return None

    changes = [current - previous for previous, current in zip(closes, closes[1:])]
    gains = [max(change, 0.0) for change in changes]
    losses = [abs(min(change, 0.0)) for change in changes]

    average_gain = sum(gains[:period]) / period
    average_loss = sum(losses[:period]) / period
    for gain, loss in zip(gains[period:], losses[period:]):
        average_gain = (average_gain * (period - 1) + gain) / period
        average_loss = (average_loss * (period - 1) + loss) / period

    if average_loss == 0:
        return 100.0

    relative_strength = average_gain / average_loss
    return 100 - (100 / (1 + relative_strength))


def _to_float_or_none(value: object) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def _round_optional(value: float | None) -> float | None:
    return round(value, 4) if value is not None else None
