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


def test_hosted_fail_closed_when_api_key_empty(monkeypatch) -> None:
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(environment="production", allow_hosted_manual_scan=True, manual_scan_api_key=""),
    )

    response = TestClient(create_app()).post("/api/scans/manual")
    assert response.status_code == 401  # key required but not configured — deny


def test_hosted_fail_closed_when_api_key_empty_and_scan_disabled(monkeypatch) -> None:
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(environment="production", allow_hosted_manual_scan=False, manual_scan_api_key=""),
    )

    response = TestClient(create_app()).post("/api/scans/manual")
    assert response.status_code == 401  # empty key in non-local always denies


# --- rate limiting ---


def test_rate_limit_blocks_after_max_requests(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="test-key",
        hosted_manual_scan_max_symbols=25,
        manual_scan_rate_limit=2,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    headers = {"X-API-Key": "test-key"}
    assert client.post("/api/scans/manual", headers=headers).status_code == 400  # req 1 — allowed
    assert client.post("/api/scans/manual", headers=headers).status_code == 400  # req 2 — allowed
    assert client.post("/api/scans/manual", headers=headers).status_code == 429  # req 3 — blocked


def test_rate_limit_skipped_in_local_environment(monkeypatch) -> None:
    local_settings = Settings(environment="local", manual_scan_rate_limit=1)
    monkeypatch.setattr(security, "get_settings", lambda: local_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: local_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    for _ in range(5):
        assert client.post("/api/scans/manual").status_code == 400  # never 429


def test_rate_limit_is_per_client_not_global(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="",  # no key configured — IP-based
        manual_scan_rate_limit=1,
    )
    # Bypass auth (key empty + scan enabled = fail-closed), so configure a key
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="key-a",
        manual_scan_rate_limit=1,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    client = TestClient(create_app())
    # key-a exhausts its own bucket
    assert client.post("/api/scans/manual", headers={"X-API-Key": "key-a"}).status_code == 400
    assert client.post("/api/scans/manual", headers={"X-API-Key": "key-a"}).status_code == 429

    # key-b still has a fresh bucket — but auth rejects it (wrong key), so patch
    # auth to accept any key for this check by swapping the configured key
    hosted_settings_b = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="key-b",
        manual_scan_rate_limit=1,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings_b)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings_b)
    assert client.post("/api/scans/manual", headers={"X-API-Key": "key-b"}).status_code == 400  # not 429


def test_rate_limit_429_response_includes_limit(monkeypatch) -> None:
    hosted_settings = Settings(
        environment="production",
        allow_hosted_manual_scan=True,
        manual_scan_api_key="test-key",
        manual_scan_rate_limit=1,
    )
    monkeypatch.setattr(security, "get_settings", lambda: hosted_settings)
    monkeypatch.setattr(scans, "get_settings", lambda: hosted_settings)
    _no_symbols(monkeypatch)

    headers = {"X-API-Key": "test-key"}
    client = TestClient(create_app())
    client.post("/api/scans/manual", headers=headers)  # consume the one allowed request
    response = client.post("/api/scans/manual", headers=headers)

    assert response.status_code == 429
    assert "1" in response.json()["detail"]
