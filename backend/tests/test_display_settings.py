from fastapi.testclient import TestClient

from app.main import create_app
from app.services.setup_detectors import ENABLED_SETUP_NAMES


def test_display_settings_enabled_setups_matches_registry() -> None:
    client = TestClient(create_app())
    response = client.get("/api/settings/display")
    assert response.status_code == 200
    assert response.json()["enabled_setups"] == list(ENABLED_SETUP_NAMES)


def test_display_settings_redacts_secrets() -> None:
    client = TestClient(create_app())

    response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert "database_url" not in payload
    assert "alpha_vantage_api_key" not in payload
    assert "secrets" not in payload


def test_display_settings_local_includes_internal_fields() -> None:
    import unittest.mock as mock

    mock_cfg = mock.MagicMock(
        environment="local",
        provider="mock",
        scanner_risk_reward_atr_buffer_multiplier=0.5,
        scanner_risk_reward_target_multiple=2.0,
        allow_hosted_manual_scan=False,
        manual_scan_rate_limit=5,
        hosted_manual_scan_max_symbols=25,
        scheduled_scan_enabled=True,
        scheduled_scan_time="06:00",
        scheduled_scan_timezone="America/New_York",
        scheduled_scan_startup_catchup=True,
    )
    with mock.patch("app.api.routes.configuration.get_settings", return_value=mock_cfg):
        client = TestClient(create_app())
        response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert "scanner" in payload
    assert "admin_controls" in payload
    assert payload["scanner"]["risk_reward_atr_buffer_multiplier"] == 0.5
    assert payload["scanner"]["schedule"] == "Daily scheduled scan at 06:00 America/New_York with local startup catch-up."
    assert "Local/dev only" in payload["admin_controls"]["manual_scan"]


def test_display_settings_hosted_manual_scan_reflects_in_schedule() -> None:
    import unittest.mock as mock

    mock_cfg = mock.MagicMock(
        environment="local",
        provider="alpha_vantage",
        scanner_risk_reward_atr_buffer_multiplier=0.5,
        scanner_risk_reward_target_multiple=2.0,
        allow_hosted_manual_scan=True,
        manual_scan_rate_limit=10,
        hosted_manual_scan_max_symbols=50,
        scheduled_scan_enabled=True,
        scheduled_scan_time="06:00",
        scheduled_scan_timezone="America/New_York",
        scheduled_scan_startup_catchup=True,
    )
    with mock.patch("app.api.routes.configuration.get_settings", return_value=mock_cfg):
        client = TestClient(create_app())
        response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scanner"]["schedule"] == "Daily scheduled scan at 06:00 America/New_York with local startup catch-up."
    assert "10 req/min" in payload["admin_controls"]["manual_scan"]
    assert "50 symbols" in payload["admin_controls"]["manual_scan"]


def test_display_settings_production_strips_internal_fields() -> None:
    import unittest.mock as mock

    mock_cfg = mock.MagicMock(
        environment="production",
        provider="alpha_vantage",
        scanner_risk_reward_atr_buffer_multiplier=0.5,
        scanner_risk_reward_target_multiple=2.0,
    )
    with mock.patch("app.api.routes.configuration.get_settings", return_value=mock_cfg):
        client = TestClient(create_app())
        response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert "scanner" not in payload
    assert "admin_controls" not in payload
    assert payload["environment"] == "production"
    assert "secrets" not in payload
