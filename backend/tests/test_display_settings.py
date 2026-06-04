from fastapi.testclient import TestClient

from app.main import create_app


def test_display_settings_redacts_secrets() -> None:
    client = TestClient(create_app())

    response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert payload["secrets"]["api_keys_visible"] is False
    assert payload["secrets"]["database_urls_visible"] is False
    assert "database_url" not in payload
    assert "alpha_vantage_api_key" not in payload


def test_display_settings_local_includes_internal_fields() -> None:
    import unittest.mock as mock

    mock_cfg = mock.MagicMock(
        environment="local",
        provider="mock",
        scanner_risk_reward_atr_buffer_multiplier=0.5,
        scanner_risk_reward_target_multiple=2.0,
    )
    with mock.patch("app.api.routes.configuration.get_settings", return_value=mock_cfg):
        client = TestClient(create_app())
        response = client.get("/api/settings/display")

    assert response.status_code == 200
    payload = response.json()
    assert "scanner" in payload
    assert "admin_controls" in payload
    assert payload["scanner"]["risk_reward_atr_buffer_multiplier"] == 0.5


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
    assert payload["secrets"]["api_keys_visible"] is False
