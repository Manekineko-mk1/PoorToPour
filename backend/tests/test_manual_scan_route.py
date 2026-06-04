from fastapi.testclient import TestClient

from app.api.routes import scans
from app.core.config import Settings
from app.main import create_app
from app.models.market_data import DailyBar, MarketDataRefreshSummary, SymbolProfile
from app.models.scans import ScanCandidate, ScanRun


def test_manual_scan_can_use_persisted_symbols_and_bars_without_refresh(monkeypatch) -> None:
    saved_scans = []

    monkeypatch.setattr(
        scans.market_data,
        "list_symbols",
        lambda db: [
            SymbolProfile(
                symbol="AAPL",
                company_name="Apple Inc.",
                sector="Technology",
                industry="Consumer Electronics",
                exchange="NASDAQ",
            )
        ],
    )
    monkeypatch.setattr(scans.market_data, "get_daily_bars", lambda db, symbol: [_bar(symbol)])
    monkeypatch.setattr(scans.scans, "upsert_scan_run", lambda db, scan: saved_scans.append(scan))
    monkeypatch.setattr(scans, "TechnicalScanner", lambda: FakeScanner())

    response = TestClient(create_app()).post("/api/scans/manual?refresh_market_data=false")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scan_id"] == "manual-test"
    assert payload["candidates_found"] == 1
    assert "market_data_refresh" not in payload
    assert len(saved_scans) == 1


def test_manual_scan_refreshes_yfinance_bars_before_scanning(monkeypatch) -> None:
    saved_scans = []
    symbols = [
        SymbolProfile(
            symbol="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            exchange="NASDAQ",
        )
    ]

    monkeypatch.setattr(scans.market_data, "list_symbols", lambda db: symbols)
    monkeypatch.setattr(scans.market_data, "get_daily_bars", lambda db, symbol: [_bar(symbol)])
    monkeypatch.setattr(scans.scans, "upsert_scan_run", lambda db, scan: saved_scans.append(scan))
    monkeypatch.setattr(scans, "TechnicalScanner", lambda: FakeScanner(expected_provider="TechnicalScanner + yfinance refreshed bars"))
    monkeypatch.setattr(
        scans,
        "refresh_yfinance_daily_bars",
        lambda db, symbols, period: MarketDataRefreshSummary(
            provider="Yahoo Finance via yfinance",
            period=period,
            symbols_requested=1,
            symbols_refreshed=1,
            bars_persisted=74,
        ),
    )

    response = TestClient(create_app()).post("/api/scans/manual")

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "TechnicalScanner + yfinance refreshed bars"
    assert payload["market_data_refresh"]["symbols_refreshed"] == 1
    assert payload["market_data_refresh"]["bars_persisted"] == 74
    assert len(saved_scans) == 1


def test_manual_scan_does_not_run_when_market_data_refresh_fails(monkeypatch) -> None:
    saved_scans = []
    monkeypatch.setattr(
        scans.market_data,
        "list_symbols",
        lambda db: [
            SymbolProfile(
                symbol="AAPL",
                company_name="Apple Inc.",
                sector="Technology",
                industry="Consumer Electronics",
                exchange="NASDAQ",
            )
        ],
    )
    monkeypatch.setattr(scans.scans, "upsert_scan_run", lambda db, scan: saved_scans.append(scan))
    monkeypatch.setattr(
        scans,
        "refresh_yfinance_daily_bars",
        lambda db, symbols, period: MarketDataRefreshSummary(
            provider="Yahoo Finance via yfinance",
            period=period,
            symbols_requested=1,
            symbols_failed=1,
            failure_messages=["AAPL: no daily bars returned"],
        ),
    )

    response = TestClient(create_app()).post("/api/scans/manual")

    assert response.status_code == 502
    assert response.json()["detail"] == "Market data refresh failed; scanner did not run."
    assert saved_scans == []


def test_manual_scan_is_disabled_in_hosted_environment_by_default(monkeypatch) -> None:
    monkeypatch.setattr(scans, "get_settings", lambda: Settings(environment="production"))

    response = TestClient(create_app()).post("/api/scans/manual")

    assert response.status_code == 403
    assert response.json()["detail"] == "Manual scan is disabled outside local/dev environments."


def test_hosted_manual_scan_uses_configured_symbol_cap(monkeypatch) -> None:
    saved_scans = []
    requested_symbols = [
        SymbolProfile(
            symbol="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            exchange="NASDAQ",
        ),
        SymbolProfile(
            symbol="MSFT",
            company_name="Microsoft Corporation",
            sector="Technology",
            industry="Software",
            exchange="NASDAQ",
        ),
    ]
    monkeypatch.setattr(
        scans,
        "get_settings",
        lambda: Settings(
            environment="production",
            allow_hosted_manual_scan=True,
            hosted_manual_scan_max_symbols=1,
        ),
    )

    monkeypatch.setattr(scans.market_data, "list_symbols", lambda db: requested_symbols)
    monkeypatch.setattr(scans.market_data, "get_daily_bars", lambda db, symbol: [_bar(symbol)])
    monkeypatch.setattr(scans.scans, "upsert_scan_run", lambda db, scan: saved_scans.append(scan))
    monkeypatch.setattr(
        scans,
        "TechnicalScanner",
        lambda: FakeScanner(
            expected_provider="TechnicalScanner + yfinance refreshed bars",
            expected_universe="Persisted symbols limited to 1",
        ),
    )
    monkeypatch.setattr(
        scans,
        "refresh_yfinance_daily_bars",
        lambda db, symbols, period: MarketDataRefreshSummary(
            provider="Yahoo Finance via yfinance",
            period=period,
            symbols_requested=len(symbols),
            symbols_refreshed=len(symbols),
            bars_persisted=74,
        ),
    )

    response = TestClient(create_app()).post("/api/scans/manual")

    assert response.status_code == 200
    payload = response.json()
    assert payload["universe"] == "Persisted symbols limited to 1"
    assert payload["market_data_refresh"]["symbols_requested"] == 1
    assert len(saved_scans) == 1


def test_manual_scan_rejects_non_positive_refresh_limit() -> None:
    response = TestClient(create_app()).post("/api/scans/manual?refresh_limit=0")

    assert response.status_code == 422


def test_manual_scan_rejects_unknown_refresh_period() -> None:
    response = TestClient(create_app()).post("/api/scans/manual?refresh_period=bogus")

    assert response.status_code == 422


class FakeScanner:
    def __init__(
        self,
        expected_provider: str = "TechnicalScanner + persisted bars",
        expected_universe: str = "Persisted symbols",
    ) -> None:
        self.expected_provider = expected_provider
        self.expected_universe = expected_universe

    def scan(self, symbols, bars_by_symbol, provider: str, universe: str) -> ScanRun:
        assert symbols[0].symbol == "AAPL"
        assert bars_by_symbol["AAPL"][0].symbol == "AAPL"
        assert provider == self.expected_provider
        assert universe == self.expected_universe
        return ScanRun(
            scan_id="manual-test",
            scan_type="Technical Scanner MVP",
            universe=universe,
            status="completed",
            provider=provider,
            symbols_processed=1,
            candidates_found=1,
            candidates=[
                ScanCandidate(
                    rank=1,
                    symbol="AAPL",
                    company_name="Apple Inc.",
                    setup="Breakout",
                    status="Watch",
                    score=55,
                    caution_flags=[],
                )
            ],
        )


def _bar(symbol: str) -> DailyBar:
    return DailyBar(
        symbol=symbol,
        date="2026-05-22",
        open=100,
        high=101,
        low=99,
        close=100,
        adjusted_close=100,
        volume=1_000_000,
    )
