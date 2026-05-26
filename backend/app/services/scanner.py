from datetime import UTC, datetime
from uuid import uuid4

from app.models.market_data import DailyBar, SymbolProfile
from app.models.scans import ScanCandidate, ScanRun
from app.services.indicators import IndicatorService


class MomentumScanner:
    """First deterministic setup detector for Phase 1.

    This intentionally detects a narrow trend/momentum candidate, not a full
    strategy. It exists to prove stored bars can become persisted scan output.
    """

    def __init__(self, indicator_service: IndicatorService | None = None) -> None:
        self.indicator_service = indicator_service or IndicatorService()

    def scan(
        self,
        symbols: list[SymbolProfile],
        bars_by_symbol: dict[str, list[DailyBar]],
        provider: str,
        universe: str,
        scan_id: str | None = None,
        now: datetime | None = None,
    ) -> ScanRun:
        completed_at = now or datetime.now(UTC)
        candidates = []

        for symbol in symbols:
            bars = bars_by_symbol.get(symbol.symbol.upper(), [])
            candidate = self._candidate_for_symbol(symbol, bars, completed_at)
            if candidate is not None:
                candidates.append(candidate)

        ranked_candidates = sorted(candidates, key=lambda candidate: (-candidate.score, candidate.symbol))
        for index, candidate in enumerate(ranked_candidates, start=1):
            candidate.rank = index

        data_dates = [
            candidate.indicator_snapshot["latest_date"]
            for candidate in ranked_candidates
            if candidate.indicator_snapshot and candidate.indicator_snapshot.get("latest_date")
        ]

        return ScanRun(
            scan_id=scan_id or f"momentum_scan_{completed_at.strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}",
            scan_type="Bootstrap Trend Momentum",
            universe=universe,
            status="completed",
            provider=provider,
            data_date=max(data_dates) if data_dates else None,
            started_at=_format_datetime(completed_at),
            completed_at=_format_datetime(completed_at),
            symbols_processed=len(symbols),
            candidates_found=len(ranked_candidates),
            warning="Bootstrap scanner for Phase 1 validation. Not a trading recommendation.",
            candidates=ranked_candidates,
        )

    def _candidate_for_symbol(
        self,
        symbol: SymbolProfile,
        bars: list[DailyBar],
        completed_at: datetime,
    ) -> ScanCandidate | None:
        if len(bars) < 50:
            return None

        snapshot = self.indicator_service.build_snapshot(symbol.symbol, bars)
        score_breakdown = _score_snapshot(snapshot.model_dump())
        score = sum(score_breakdown.values())
        if score < 45:
            return None

        reasons = _reasons(snapshot.model_dump())
        caution_flags = list(snapshot.warnings)
        if snapshot.relative_volume_20 is not None and snapshot.relative_volume_20 < 1:
            caution_flags.append("Relative volume below 20-day average.")

        return ScanCandidate(
            rank=0,
            symbol=symbol.symbol,
            company_name=symbol.company_name,
            setup="Trend Momentum",
            status=_status_for_score(score),
            score=score,
            price=snapshot.close,
            relative_volume=snapshot.relative_volume_20,
            rsi=None,
            risk_reward=None,
            indicator_snapshot=snapshot.model_dump(),
            score_breakdown=score_breakdown,
            reasons=reasons,
            caution_flags=caution_flags,
            last_updated=_format_datetime(completed_at),
        )


def _score_snapshot(snapshot: dict) -> dict[str, int]:
    score = {
        "close_above_sma_20": 25 if snapshot["close_above_sma_20"] else 0,
        "close_above_sma_50": 25 if snapshot["close_above_sma_50"] else 0,
        "close_above_ema_21": 20 if snapshot["ema_21"] is not None and snapshot["close"] > snapshot["ema_21"] else 0,
        "relative_volume_confirmation": 15 if snapshot["relative_volume_20"] is not None and snapshot["relative_volume_20"] >= 1 else 0,
        "relative_volume_expansion": 10 if snapshot["relative_volume_20"] is not None and snapshot["relative_volume_20"] >= 1.2 else 0,
        "near_52_week_high": 10
        if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -10
        else 0,
    }
    return score


def _reasons(snapshot: dict) -> list[str]:
    reasons = []
    if snapshot["close_above_sma_20"]:
        reasons.append("Close is above the 20-day simple moving average.")
    if snapshot["close_above_sma_50"]:
        reasons.append("Close is above the 50-day simple moving average.")
    if snapshot["ema_21"] is not None and snapshot["close"] > snapshot["ema_21"]:
        reasons.append("Close is above the 21-day exponential moving average.")
    if snapshot["relative_volume_20"] is not None and snapshot["relative_volume_20"] >= 1:
        reasons.append("Volume is at or above the 20-day average.")
    if snapshot["high_52_week_distance_pct"] is not None and snapshot["high_52_week_distance_pct"] >= -10:
        reasons.append("Close is within 10% of the 52-week high.")
    return reasons


def _status_for_score(score: int) -> str:
    if score >= 45:
        return "Watch"
    return "Avoid"


def _format_datetime(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
