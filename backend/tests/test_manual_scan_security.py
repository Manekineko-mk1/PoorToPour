import pytest
from fastapi.testclient import TestClient

from app.api.routes import scans
from app.core import security
from app.core.config import Settings
from app.main import create_app


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    security.manual_scan_limiter.reset()
    yield
    security.manual_scan_limiter.reset()


def _no_symbols(monkeypatch) -> None:
    monkeypatch.setattr(scans.market_data, "list_symbols", lambda db: [])


# --- auth ---


def test_auth_skipped_in_local_environment(monkeypatch) -> None:
    monkeypatch.setattr(security, "get_settings", lambda: Settings(environment="local"))
    monkeypatch.setattr(scans, "get_settings", lambda: Settings(environment="local"))
    _no_symbols(monkeypatch)

    response = TestClient(create_app()).post("/api/scans/manual")
    assert response.status_code == 400  # no symbols — not 401


def test_hosted_rejects_missing_api_key(monkeypatch) -> None:
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(environment="production", manual_scan_api_key="secret-key"),
    )

    response = TestClient(create_app()).post("/api/scans/manual")
    assert response.status_code == 401


def test_hosted_rejects_wrong_api_key(monkeypatch) -> None:
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(environment="production", manual_scan_api_key="secret-key"),
    )

    response = TestClient(create_app()).post(
        "/api/scans/manual", headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401


def test_hosted_accepts_correct_api_key(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="secret-key",
        hosted_manual_scan_max_symbols=25,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    response = TestClient(create_app()).post(
        "/api/scans/manual", headers={"X-API-Key": "secret-key"}
    )
    assert response.status_code == 400  # no symbols — not 401


def test_hosted_open_when_api_key_not_configured(monkeypatch) -> None:
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(environment="production", manual_scan_api_key=""),
    )
    monkeypatch.setattr(
        scans,
        "get_settings",
        lambda: Settings(environment="production", allow_hosted_manual_scan=False, manual_scan_api_key=""),
    )

    response = TestClient(create_app()).post("/api/scans/manual")
    assert response.status_code == 403  # scan disabled — not 401


# --- rate limiting ---


def test_rate_limit_blocks_after_max_requests(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="",
        hosted_manual_scan_max_symbols=25,
        manual_scan_rate_limit=2,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    assert client.post("/api/scans/manual").status_code == 400  # req 1 — allowed
    assert client.post("/api/scans/manual").status_code == 400  # req 2 — allowed
    assert client.post("/api/scans/manual").status_code == 429  # req 3 — blocked


def test_rate_limit_skipped_in_local_environment(monkeypatch) -> None:
    local_settings = Settings(environment="local", manual_scan_rate_limit=1)
    monkeypatch.setattr(security, "get_settings", lambda: local_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: local_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    for _ in range(5):
        assert client.post("/api/scans/manual").status_code == 400  # never 429


def test_rate_limit_429_response_includes_limit(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="",
        manual_scan_rate_limit=1,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    client.post("/api/scans/manual")  # consume the one allowed request
    response = client.post("/api/scans/manual")

    assert response.status_code == 429
    assert "1" in response.json()["detail"]
