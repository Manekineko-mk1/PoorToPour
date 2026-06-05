from datetime import UTC, datetime, timedelta

from app.core.config import Settings
from app.models.market_data import DailyBar, SymbolProfile
from app.services.setup_detectors import PullbackContinuationDetector


def test_pullback_detector_returns_watch_for_confirmed_pullback() -> None:
    detector = PullbackContinuationDetector(settings=_settings())
    bars = _trend_bars("PULL", latest_close=126.0, latest_volume=1_000_000)

    candidate = detector.detect(_symbol("PULL"), bars, now=_now())

    assert candidate is not None
    assert candidate.setup == "Pullback Continuation"
    assert candidate.status == "Watch"
    assert candidate.risk_reward == "2.0:1"
    assert candidate.score >= 70
    assert candidate.score_breakdown["risk_reward"]["ratio"] == 2.0
    assert "Price is holding near short-term moving-average support." in candidate.reasons
    assert "Close is above the 50-day simple moving average." in candidate.reasons


def test_pullback_detector_returns_watch_for_developing_pullback() -> None:
    detector = PullbackContinuationDetector(settings=_settings())
    bars = _trend_bars("BASE", latest_close=123.0, latest_volume=900_000)

    candidate = detector.detect(_symbol("BASE"), bars, now=_now())

    assert candidate is not None
    assert candidate.status == "Watch"
    assert "Pullback is still developing; price has not reclaimed short-term support." in candidate.caution_flags
    assert "Close has not reclaimed the 20-day moving average." in candidate.caution_flags


def test_pullback_detector_blocks_when_required_history_is_missing() -> None:
    detector = PullbackContinuationDetector(settings=_settings())

    candidate = detector.detect(_symbol("THIN"), _trend_bars("THIN", count=20), now=_now())

    assert candidate is not None
    assert candidate.status == "Blocked"
    assert candidate.score == 0
    assert candidate.indicator_snapshot is None
    assert "At least 50 daily bars are required for pullback continuation detection." in candidate.caution_flags


def test_pullback_detector_ignores_broken_trend() -> None:
    detector = PullbackContinuationDetector(settings=_settings())
    bars = _trend_bars("DROP", latest_close=105.0, latest_volume=1_000_000)

    candidate = detector.detect(_symbol("DROP"), bars, now=_now())

    assert candidate is None


def _symbol(symbol: str) -> SymbolProfile:
    return SymbolProfile(
        symbol=symbol,
        company_name=f"{symbol} Corp",
        sector="Technology",
        industry="Software",
        exchange="TEST",
    )


def _trend_bars(
    symbol: str,
    count: int = 60,
    latest_close: float | None = None,
    latest_volume: int = 1_000_000,
) -> list[DailyBar]:
    first_date = datetime(2026, 1, 1, tzinfo=UTC)
    bars = []
    for index in range(count):
        close = 100.0 + (index * 0.5)
        volume = 1_000_000

        if index == count - 1:
            close = latest_close if latest_close is not None else close
            volume = latest_volume

        bars.append(
            DailyBar(
                symbol=symbol,
                date=(first_date + timedelta(days=index)).date(),
                open=max(close - 0.5, 0.01),
                high=close + 1.0,
                low=max(close - 1.0, 0.01),
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
