from datetime import UTC, datetime, timedelta

from app.models.market_data import DailyBar, SymbolProfile
from app.services.scanner import MomentumScanner


def test_momentum_scanner_generates_ranked_candidates() -> None:
    scanner = MomentumScanner()
    symbols = [
        _symbol("AAA", "Alpha A"),
        _symbol("BBB", "Beta B"),
        _symbol("CCC", "Cold C"),
    ]
    bars_by_symbol = {
        "AAA": _bars("AAA", start=100, count=60, volume=2_000_000, latest_volume=2_600_000),
        "BBB": _bars("BBB", start=50, count=60, volume=2_000_000, latest_volume=1_500_000),
        "CCC": _bars("CCC", start=200, count=20, volume=2_000_000, latest_volume=2_600_000),
    }

    scan = scanner.scan(
        symbols=symbols,
        bars_by_symbol=bars_by_symbol,
        provider="test",
        universe="unit",
        scan_id="scan_test",
        now=datetime(2026, 5, 26, 12, 0, tzinfo=UTC),
    )

    assert scan.scan_id == "scan_test"
    assert scan.symbols_processed == 3
    assert scan.candidates_found == 2
    assert [candidate.symbol for candidate in scan.candidates] == ["AAA", "BBB"]
    assert scan.candidates[0].rank == 1
    assert scan.candidates[0].score > scan.candidates[1].score
    assert scan.candidates[0].setup == "Trend Momentum"
    assert "Volume is at or above the 20-day average." in scan.candidates[0].reasons
    assert "Relative volume below 20-day average." in scan.candidates[1].caution_flags


def test_momentum_scanner_does_not_force_candidates() -> None:
    scanner = MomentumScanner()
    symbols = [_symbol("AAA", "Alpha A")]

    scan = scanner.scan(
        symbols=symbols,
        bars_by_symbol={"AAA": _bars("AAA", start=100, count=10, volume=1_000_000, latest_volume=1_000_000)},
        provider="test",
        universe="unit",
        scan_id="empty_scan",
        now=datetime(2026, 5, 26, 12, 0, tzinfo=UTC),
    )

    assert scan.candidates_found == 0
    assert scan.candidates == []


def _symbol(symbol: str, company_name: str) -> SymbolProfile:
    return SymbolProfile(
        symbol=symbol,
        company_name=company_name,
        sector="Technology",
        industry="Software",
        exchange="TEST",
    )


def _bars(
    symbol: str,
    start: int,
    count: int,
    volume: int,
    latest_volume: int,
) -> list[DailyBar]:
    first_date = datetime(2026, 1, 1, tzinfo=UTC)
    bars = []
    for index in range(count):
        close = float(start + index)
        bar_date = (first_date + timedelta(days=index)).date().isoformat()
        bars.append(
            DailyBar(
                symbol=symbol,
                date=bar_date,
                open=close - 0.5,
                high=close + 1,
                low=close - 1,
                close=close,
                adjusted_close=close,
                volume=latest_volume if index == count - 1 else volume,
            )
        )
    return bars
