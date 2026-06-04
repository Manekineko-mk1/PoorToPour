from datetime import date, timedelta

from fastapi.testclient import TestClient
import pytest

from app.api.routes import market_data
from app.main import create_app
from app.models.market_data import CompanyProfile, DailyBar
from app.models.scans import ScanCandidate, ScanRun
from app.services.chart_data import _relative_strength_index, _rolling_rsi, build_symbol_chart_payload


def test_chart_payload_includes_indicator_bars_and_candidate_context() -> None:
    bars = [_bar(index) for index in range(1, 61)]
    candidate = ScanCandidate(
        rank=1,
        symbol="AAPL",
        company_name="Apple Inc.",
        setup="Breakout",
        status="Watch",
        score=55,
        risk_reward="2.0:1",
        score_breakdown={
            "risk_reward": {
                "entry": 60.0,
                "invalidation": 52.0,
                "target": 76.0,
                "risk_per_share": 8.0,
            }
        },
        reasons=["Close is above the 20-day simple moving average."],
        caution_flags=["SMA 200 is incomplete."],
    )

    payload = build_symbol_chart_payload(
        "aapl",
        bars,
        profile=CompanyProfile(
            symbol="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=1_000_000,
            average_volume=10_000,
            exchange="NASDAQ",
        ),
        candidate_context=(
            ScanRun(
                scan_id="scan-1",
                scan_type="technical",
                universe="Persisted Symbols",
                status="completed",
                provider="TechnicalScanner",
            ),
            candidate,
        ),
    )

    assert payload.symbol == "AAPL"
    assert payload.company_name == "Apple Inc."
    assert payload.exchange == "NASDAQ"
    assert payload.data_date == date(2026, 3, 1)
    assert len(payload.bars) == 60
    assert payload.bars[-1].sma_20 == 90.5
    assert payload.bars[-1].sma_50 == 75.5
    assert payload.bars[-1].sma_200 is None
    assert payload.bars[-1].rsi_14 == 100
    assert payload.candidate is not None
    assert payload.candidate.scan_id == "scan-1"
    assert payload.candidate.risk_reward_overlay is not None
    assert payload.candidate.risk_reward_overlay.entry == 60.0


def test_chart_payload_reports_insufficient_history_warnings() -> None:
    payload = build_symbol_chart_payload("THIN", [_bar(index) for index in range(1, 11)])

    assert payload.bars[-1].sma_20 is None
    assert payload.bars[-1].rsi_14 is None
    assert "Only 10 bars available; SMA 20 is incomplete." in payload.warnings
    assert "Only 10 bars available; RSI 14 is incomplete." in payload.warnings


def test_chart_route_uses_requested_setup_for_candidate_context(monkeypatch) -> None:
    requested_context = {}
    candidate = ScanCandidate(
        rank=2,
        symbol="AAPL",
        company_name="Apple Inc.",
        setup="Pullback Continuation",
        status="Watch",
        score=50,
        risk_reward="2.0:1",
        score_breakdown={
            "risk_reward": {
                "entry": 100.0,
                "invalidation": 90.0,
                "target": 120.0,
                "risk_per_share": 10.0,
            }
        },
    )

    monkeypatch.setattr(market_data.market_data, "get_daily_bars", lambda db, symbol: [_bar(index) for index in range(1, 61)])
    monkeypatch.setattr(market_data.market_data, "get_company_profile", lambda db, symbol: None)

    def fake_candidate_lookup(db, symbol, setup=None, scan_id=None):
        requested_context["symbol"] = symbol
        requested_context["setup"] = setup
        requested_context["scan_id"] = scan_id
        return (
            ScanRun(
                scan_id="scan-setup",
                scan_type="technical",
                universe="Persisted Symbols",
                status="completed",
                provider="TechnicalScanner",
            ),
            candidate,
        )

    monkeypatch.setattr(market_data.scans, "get_latest_candidate_for_symbol", fake_candidate_lookup)

    response = TestClient(create_app()).get("/api/symbols/AAPL/chart?setup=Pullback%20Continuation&scan_id=scan-setup")

    assert response.status_code == 200
    payload = response.json()
    assert requested_context == {
        "symbol": "AAPL",
        "setup": "Pullback Continuation",
        "scan_id": "scan-setup",
    }
    assert payload["candidate"]["setup"] == "Pullback Continuation"
    assert payload["candidate"]["risk_reward_overlay"]["entry"] == 100.0


def test_relative_strength_index_uses_wilder_smoothing() -> None:
    # EN: Wilder's smoothing over [10, 11, 10, 11] with period 2 yields RSI 75.0.
    # A simple (non-Wilder) average over the same closes would return 50.0,
    # so this pins the calculation to the standard method.
    assert _relative_strength_index([10.0, 11.0, 10.0, 11.0], 2) == pytest.approx(75.0)


def test_relative_strength_index_requires_more_than_period_closes() -> None:
    assert _relative_strength_index([10.0, 11.0], 2) is None


def test_rolling_rsi_produces_none_until_enough_history_then_matches_single_rsi() -> None:
    closes = [10.0, 11.0, 10.0, 11.0]
    result = _rolling_rsi(closes, 2)
    assert result[0] is None
    assert result[1] is None
    assert result[2] == pytest.approx(50.0)
    assert result[3] == pytest.approx(75.0)


def _bar(index: int) -> DailyBar:
    close = float(index + 40)
    return DailyBar(
        symbol="AAPL",
        date=date(2026, 1, 1) + timedelta(days=index - 1),
        open=close,
        high=close + 1,
        low=close - 1,
        close=close,
        adjusted_close=close,
        volume=1_000_000 + index,
    )
