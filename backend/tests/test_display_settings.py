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
