from datetime import UTC, datetime, timedelta

from app.core.config import Settings
from app.models.market_data import DailyBar, SymbolProfile
from app.services.setup_detectors import BreakoutDetector


def test_breakout_detector_returns_watch_for_confirmed_breakout() -> None:
    detector = BreakoutDetector(settings=_settings())
    bars = _bars("BOOM", count=60, latest_close=125, latest_high=126, latest_volume=3_000_000)

    candidate = detector.detect(_symbol("BOOM"), bars, now=_now())

    assert candidate is not None
    assert candidate.setup == "Breakout"
    assert candidate.status == "Watch"
    assert candidate.risk_reward == "2.0:1"
    assert candidate.score >= 80
    assert candidate.score_breakdown["risk_reward"]["ratio"] == 2.0
    assert "Close broke above the prior 20-day high." in candidate.reasons
    assert "Relative volume is at least 1.5x the 20-day average." in candidate.reasons


def test_breakout_detector_returns_watch_for_near_breakout_without_confirmation() -> None:
    detector = BreakoutDetector(settings=_settings())
    bars = _bars("NEAR", count=60, latest_close=119, latest_high=121, latest_volume=1_200_000)

    candidate = detector.detect(_symbol("NEAR"), bars, now=_now())

    assert candidate is not None
    assert candidate.status == "Watch"
    assert candidate.score < 80
    assert "Breakout not confirmed yet; price is near the 20-day high." in candidate.caution_flags
    assert "Relative volume is below the 1.5x breakout confirmation threshold." in candidate.caution_flags


def test_breakout_detector_blocks_when_required_history_is_missing() -> None:
    detector = BreakoutDetector(settings=_settings())

    candidate = detector.detect(_symbol("THIN"), _bars("THIN", count=20), now=_now())

    assert candidate is not None
    assert candidate.status == "Blocked"
    assert candidate.score == 0
    assert candidate.indicator_snapshot is None
    assert "At least 50 daily bars are required for breakout detection." in candidate.caution_flags


def test_breakout_detector_blocks_detected_setup_when_price_data_is_stale() -> None:
    detector = BreakoutDetector(settings=_settings())
    bars = _bars("STALE", count=60, latest_close=125, latest_high=126, latest_volume=3_000_000)

    candidate = detector.detect(_symbol("STALE"), bars, now=datetime(2026, 5, 26, 12, 0, tzinfo=UTC))

    assert candidate is not None
    assert candidate.status == "Blocked"
    assert "Price data is stale; latest bar is 2026-03-01." in candidate.caution_flags


def test_breakout_detector_ignores_weak_non_breakout() -> None:
    detector = BreakoutDetector(settings=_settings())
    bars = _bars("WEAK", count=60, latest_close=95, latest_high=96, latest_volume=900_000)

    candidate = detector.detect(_symbol("WEAK"), bars, now=_now())

    assert candidate is None


def _symbol(symbol: str) -> SymbolProfile:
    return SymbolProfile(
        symbol=symbol,
        company_name=f"{symbol} Corp",
        sector="Technology",
        industry="Software",
        exchange="TEST",
    )


def _bars(
    symbol: str,
    count: int,
    latest_close: float | None = None,
    latest_high: float | None = None,
    latest_volume: int = 1_000_000,
) -> list[DailyBar]:
    first_date = datetime(2026, 1, 1, tzinfo=UTC)
    bars = []
    for index in range(count):
        bar_date = (first_date + timedelta(days=index)).date()
        close = 100.0
        high = 120.0
        low = 98.0
        volume = 1_000_000

        if index == count - 1:
            close = latest_close if latest_close is not None else close
            high = latest_high if latest_high is not None else max(close + 1, high)
            low = min(low, close - 1)
            volume = latest_volume

        bars.append(
            DailyBar(
                symbol=symbol,
                date=bar_date,
                open=max(close - 1, 0.01),
                high=high,
                low=max(low, 0.01),
                close=close,
                adjusted_close=close,
                volume=volume,
            )
        )
    return bars


def _now() -> datetime:
    return datetime(2026, 3, 4, 12, 0, tzinfo=UTC)


def _settings() -> Settings:
    return Settings(_env_file=None)
