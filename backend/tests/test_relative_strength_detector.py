from datetime import UTC, datetime, timedelta

from app.core.config import Settings
from app.models.market_data import DailyBar, SymbolProfile
from app.services.setup_detectors import RelativeStrengthLeaderDetector


def test_relative_strength_detector_returns_actionable_for_clean_confirmed_leader() -> None:
    detector = RelativeStrengthLeaderDetector(settings=_settings())
    bars = _leader_bars("LEAD", count=260, latest_close=130.0, latest_volume=1_600_000)

    candidate = detector.detect(_symbol("LEAD"), bars, now=_now())

    assert candidate is not None
    assert candidate.setup == "Relative Strength Leader"
    assert candidate.status == "Actionable"
    assert candidate.score >= 80
    assert candidate.risk_reward == "2.0:1"
    assert "Price leadership is near the 52-week high with trend confirmation." in candidate.reasons
    assert "Close is within 5% of the 52-week high." in candidate.reasons


def test_relative_strength_detector_returns_watch_for_shorter_term_leader_proxy() -> None:
    detector = RelativeStrengthLeaderDetector(settings=_settings())
    bars = _leader_bars("PROX", count=60, latest_close=108.0, latest_volume=1_100_000)

    candidate = detector.detect(_symbol("PROX"), bars, now=datetime(2025, 10, 2, 12, 0, tzinfo=UTC))

    assert candidate is not None
    assert candidate.status == "Watch"
    assert "Relative strength is based on shorter-term price leadership; 52-week confirmation is incomplete." in candidate.caution_flags


def test_relative_strength_detector_blocks_when_required_history_is_missing() -> None:
    detector = RelativeStrengthLeaderDetector(settings=_settings())

    candidate = detector.detect(_symbol("THIN"), _leader_bars("THIN", count=20), now=_now())

    assert candidate is not None
    assert candidate.status == "Blocked"
    assert candidate.score == 0
    assert "At least 50 daily bars are required for relative strength leader detection." in candidate.caution_flags


def test_relative_strength_detector_ignores_lagging_symbol() -> None:
    detector = RelativeStrengthLeaderDetector(settings=_settings())
    bars = _leader_bars("LAG", count=260, latest_close=100.0, latest_volume=900_000)

    candidate = detector.detect(_symbol("LAG"), bars, now=_now())

    assert candidate is None


def _symbol(symbol: str) -> SymbolProfile:
    return SymbolProfile(
        symbol=symbol,
        company_name=f"{symbol} Corp",
        sector="Technology",
        industry="Software",
        exchange="TEST",
    )


def _leader_bars(
    symbol: str,
    count: int,
    latest_close: float | None = None,
    latest_volume: int = 1_000_000,
) -> list[DailyBar]:
    first_date = datetime(2025, 8, 1, tzinfo=UTC)
    bars = []
    for index in range(count):
        close = 100.0 + (index * 0.1)
        volume = 1_000_000

        if index == count - 1:
            close = latest_close if latest_close is not None else close
            volume = latest_volume

        bars.append(
            DailyBar(
                symbol=symbol,
                date=(first_date + timedelta(days=index)).date().isoformat(),
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
    return datetime(2026, 4, 20, 12, 0, tzinfo=UTC)


def _settings() -> Settings:
    return Settings(_env_file=None)
