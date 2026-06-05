from datetime import UTC, datetime, timedelta

from app.core.config import Settings
from app.models.market_data import DailyBar, SymbolProfile
from app.services.scanner import TechnicalScanner
from app.services.setup_detectors import BreakoutDetector, PullbackContinuationDetector, RelativeStrengthLeaderDetector


def test_technical_scanner_generates_ranked_phase_2_scan() -> None:
    scanner = TechnicalScanner(detectors=_detectors())
    symbols = [
        _symbol("LEAD", "Leader Co"),
        _symbol("PULL", "Pullback Co"),
        _symbol("THIN", "Thin Co"),
    ]
    bars_by_symbol = {
        "LEAD": _leader_bars("LEAD", count=260, latest_close=130.0, latest_volume=1_600_000),
        "PULL": _trend_bars("PULL", count=60, latest_close=126.0, latest_volume=1_000_000),
        "THIN": _trend_bars("THIN", count=20, latest_close=103.0, latest_volume=1_000_000),
    }

    scan = scanner.scan(
        symbols=symbols,
        bars_by_symbol=bars_by_symbol,
        provider="test",
        universe="unit",
        scan_id="technical_scan_test",
        now=_now(),
    )

    assert scan.scan_id == "technical_scan_test"
    assert scan.scan_type == "Technical Scanner MVP"
    assert scan.symbols_processed == 3
    assert scan.candidates_found == len(scan.candidates)
    assert scan.data_date == "2026-04-17"
    assert scan.candidates[0].status == "Actionable"
    assert scan.candidates[0].rank == 1
    assert scan.candidates[0].symbol == "LEAD"
    assert all(candidate.status != "Blocked" for candidate in scan.candidates)
    assert any(candidate.setup == "Pullback Continuation" for candidate in scan.candidates)
    assert "Research-only deterministic scanner output" in scan.warning


def test_technical_scanner_can_include_blocked_candidates_for_data_quality_inspection() -> None:
    scanner = TechnicalScanner(detectors=_detectors(), include_blocked=True)
    symbols = [_symbol("THIN", "Thin Co")]

    scan = scanner.scan(
        symbols=symbols,
        bars_by_symbol={"THIN": _trend_bars("THIN", count=20, latest_close=103.0, latest_volume=1_000_000)},
        provider="test",
        universe="unit",
        scan_id="technical_scan_blocked",
        now=_now(),
    )

    assert scan.candidates_found == 3
    assert {candidate.setup for candidate in scan.candidates} == {
        "Breakout",
        "Pullback Continuation",
        "Relative Strength Leader",
    }
    assert all(candidate.status == "Blocked" for candidate in scan.candidates)


def _detectors() -> list:
    settings = Settings(_env_file=None)
    return [
        BreakoutDetector(settings=settings),
        PullbackContinuationDetector(settings=settings),
        RelativeStrengthLeaderDetector(settings=settings),
    ]


def _symbol(symbol: str, company_name: str) -> SymbolProfile:
    return SymbolProfile(
        symbol=symbol,
        company_name=company_name,
        sector="Technology",
        industry="Software",
        exchange="TEST",
    )


def _trend_bars(
    symbol: str,
    count: int,
    latest_close: float,
    latest_volume: int,
) -> list[DailyBar]:
    first_date = datetime(2026, 2, 17, tzinfo=UTC)
    bars = []
    for index in range(count):
        close = 100.0 + (index * 0.5)
        if index == count - 1:
            close = latest_close
        bars.append(_bar(symbol, first_date, index, close, latest_volume if index == count - 1 else 1_000_000))
    return bars


def _leader_bars(
    symbol: str,
    count: int,
    latest_close: float,
    latest_volume: int,
) -> list[DailyBar]:
    first_date = datetime(2025, 8, 1, tzinfo=UTC)
    bars = []
    for index in range(count):
        close = 100.0 + (index * 0.1)
        if index == count - 1:
            close = latest_close
        bars.append(_bar(symbol, first_date, index, close, latest_volume if index == count - 1 else 1_000_000))
    return bars


def _bar(symbol: str, first_date: datetime, index: int, close: float, volume: int) -> DailyBar:
    return DailyBar(
        symbol=symbol,
        date=(first_date + timedelta(days=index)).date(),
        open=max(close - 0.5, 0.01),
        high=close + 1.0,
        low=max(close - 1.0, 0.01),
        close=close,
        adjusted_close=close,
        volume=volume,
    )


def _now() -> datetime:
    return datetime(2026, 4, 20, 12, 0, tzinfo=UTC)
