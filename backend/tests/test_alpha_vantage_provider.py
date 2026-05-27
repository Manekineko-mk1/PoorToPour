import pytest

from app.providers.alpha_vantage_provider import (
    AlphaVantageError,
    AlphaVantageProvider,
    daily_bars_from_alpha_vantage_payload,
)


def test_daily_bars_from_standard_daily_payload() -> None:
    payload = {
        "Time Series (Daily)": {
            "2026-05-24": {
                "1. open": "100.00",
                "2. high": "110.50",
                "3. low": "99.50",
                "4. close": "108.25",
                "5. volume": "123456",
            }
        }
    }

    bars = daily_bars_from_alpha_vantage_payload("aapl", payload)

    assert len(bars) == 1
    assert bars[0].symbol == "AAPL"
    assert bars[0].date == "2026-05-24"
    assert bars[0].close == 108.25
    assert bars[0].adjusted_close == 108.25
    assert bars[0].volume == 123456


def test_daily_bars_from_adjusted_daily_payload() -> None:
    payload = {
        "Time Series (Daily)": {
            "2026-05-24": {
                "1. open": "100.00",
                "2. high": "110.50",
                "3. low": "99.50",
                "4. close": "108.25",
                "5. adjusted close": "107.75",
                "6. volume": "123456",
            }
        }
    }

    bars = daily_bars_from_alpha_vantage_payload("MSFT", payload)

    assert len(bars) == 1
    assert bars[0].adjusted_close == 107.75
    assert bars[0].volume == 123456


def test_daily_bars_are_sorted_oldest_first() -> None:
    payload = {
        "Time Series (Daily)": {
            "2026-05-25": {
                "1. open": "101.00",
                "2. high": "102.00",
                "3. low": "100.00",
                "4. close": "101.50",
                "5. volume": "20",
            },
            "2026-05-24": {
                "1. open": "100.00",
                "2. high": "101.00",
                "3. low": "99.00",
                "4. close": "100.50",
                "5. volume": "10",
            },
        }
    }

    bars = daily_bars_from_alpha_vantage_payload("NVDA", payload)

    assert [bar.date for bar in bars] == ["2026-05-24", "2026-05-25"]


def test_daily_bars_skip_invalid_dates_and_inconsistent_ohlc_rows() -> None:
    payload = {
        "Time Series (Daily)": {
            "bad-date": {
                "1. open": "100.00",
                "2. high": "110.00",
                "3. low": "99.00",
                "4. close": "108.00",
                "5. volume": "10",
            },
            "2026-05-24": {
                "1. open": "100.00",
                "2. high": "99.00",
                "3. low": "98.00",
                "4. close": "101.00",
                "5. volume": "10",
            },
            "2026-05-25": {
                "1. open": "100.00",
                "2. high": "101.00",
                "3. low": "99.00",
                "4. close": "100.50",
                "5. volume": "10",
            },
        }
    }

    bars = daily_bars_from_alpha_vantage_payload("NVDA", payload)

    assert [bar.date for bar in bars] == ["2026-05-25"]


def test_daily_bars_raise_on_rate_limit_message() -> None:
    payload = {"Note": "Thank you for using Alpha Vantage! Our standard API rate limit is ..."}

    with pytest.raises(AlphaVantageError):
        daily_bars_from_alpha_vantage_payload("AAPL", payload)


def test_provider_sends_expected_params_without_exposing_key() -> None:
    client = FakeClient(
        {
            "Time Series (Daily)": {
                "2026-05-24": {
                    "1. open": "100.00",
                    "2. high": "110.50",
                    "3. low": "99.50",
                    "4. close": "108.25",
                    "5. volume": "123456",
                }
            }
        }
    )
    provider = AlphaVantageProvider(api_key="test-key", client=client)

    bars = provider.get_daily_bars("AAPL")

    assert len(bars) == 1
    assert client.params["function"] == "TIME_SERIES_DAILY"
    assert client.params["symbol"] == "AAPL"
    assert client.params["apikey"] == "test-key"


class FakeClient:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.params: dict[str, str] = {}

    def get(self, url: str, params: dict[str, str], timeout: float) -> "FakeResponse":
        self.params = params
        return FakeResponse(self.payload)


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload
