from app.repositories.scans import scan_run_from_payload


def test_scan_run_from_payload_preserves_fixture_shape() -> None:
    payload = {
        "scan_id": "scan_1",
        "scan_type": "Daily Momentum",
        "universe": "S&P 500",
        "status": "completed",
        "provider": "Mock Provider",
        "data_date": "2026-05-22",
        "symbols_processed": 3,
        "candidates_found": 1,
        "warning": "Fixture",
        "candidates": [
            {
                "rank": 1,
                "symbol": "AAPL",
                "company_name": "Apple Inc.",
                "setup": "Momentum Breakout",
                "status": "Actionable",
                "score": 86,
                "price": 308.82,
                "relative_volume": 1.25,
                "rsi": 61.3,
                "risk_reward": "3.2:1",
                "caution_flags": ["Earnings Soon"],
                "last_updated": "2026-05-22T21:08:13Z",
            }
        ],
    }

    scan = scan_run_from_payload(payload)

    assert scan.scan_id == "scan_1"
    assert scan.candidates_found == 1
    assert scan.candidates[0].symbol == "AAPL"
    assert scan.candidates[0].caution_flags == ["Earnings Soon"]
