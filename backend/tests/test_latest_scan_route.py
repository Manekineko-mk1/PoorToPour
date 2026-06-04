from fastapi.testclient import TestClient

from app.api.routes import scans
from app.main import create_app
from app.models.scans import ScanCandidate, ScanRun


def test_latest_scan_returns_404_when_no_scan_exists(monkeypatch) -> None:
    monkeypatch.setattr(scans.scans, "get_latest_scan", lambda db: None)

    response = TestClient(create_app()).get("/api/scans/latest")

    assert response.status_code == 404
    assert response.json()["detail"] == "No scan results found"


def test_latest_scan_returns_scan_data_when_scan_exists(monkeypatch) -> None:
    scan = ScanRun(
        scan_id="test-scan-001",
        scan_type="Technical Scanner MVP",
        universe="Persisted symbols",
        status="completed",
        provider="TechnicalScanner + persisted bars",
        symbols_processed=10,
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
    monkeypatch.setattr(scans.scans, "get_latest_scan", lambda db: scan)

    response = TestClient(create_app()).get("/api/scans/latest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scan_id"] == "test-scan-001"
    assert payload["candidates_found"] == 1
    assert payload["candidates"][0]["symbol"] == "AAPL"
