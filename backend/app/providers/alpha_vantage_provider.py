from datetime import date
from typing import Any

import httpx

from app.models.market_data import DailyBar, ProviderStatus
from app.providers.validation import is_iso_date, is_valid_daily_bar_values

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
DEFAULT_DAILY_FUNCTION = "TIME_SERIES_DAILY"
SUPPORTED_DAILY_FUNCTIONS = {"TIME_SERIES_DAILY", "TIME_SERIES_DAILY_ADJUSTED"}
TIME_SERIES_DAILY_KEY = "Time Series (Daily)"


class AlphaVantageError(RuntimeError):
    pass


class AlphaVantageProvider:
    """Alpha Vantage OHLCV provider.

    The adapter defaults to the standard daily endpoint so a normal API key can
    be tested without premium-only assumptions. If the adjusted endpoint is
    enabled later, the parser will use its adjusted close field.
    """

    def __init__(
        self,
        api_key: str,
        daily_function: str = DEFAULT_DAILY_FUNCTION,
        base_url: str = ALPHA_VANTAGE_URL,
        timeout: float = 20.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key
        self.daily_function = daily_function
        self.base_url = base_url
        self.timeout = timeout
        self.client = client

        if self.daily_function not in SUPPORTED_DAILY_FUNCTIONS:
            supported = ", ".join(sorted(SUPPORTED_DAILY_FUNCTIONS))
            raise ValueError(f"Unsupported Alpha Vantage daily function: {daily_function}. Use one of: {supported}.")

    def get_status(self) -> ProviderStatus:
        status = "configured" if self.api_key else "missing_api_key"
        message = (
            "Alpha Vantage provider configured for manual daily OHLCV ingestion."
            if self.api_key
            else "Alpha Vantage API key is missing. Set POORTOPOUR_ALPHA_VANTAGE_API_KEY."
        )
        return ProviderStatus(
            provider="Alpha Vantage",
            mode="provider",
            status=status,
            message=message,
            data_date=date.today().isoformat(),
        )

    def get_daily_bars(self, symbol: str, outputsize: str = "compact") -> list[DailyBar]:
        if not self.api_key:
            raise AlphaVantageError("Alpha Vantage API key is missing.")

        params = {
            "function": self.daily_function,
            "symbol": symbol.upper(),
            "outputsize": outputsize,
            "datatype": "json",
            "apikey": self.api_key,
        }
        payload = self._get(params)
        return daily_bars_from_alpha_vantage_payload(symbol, payload)

    def _get(self, params: dict[str, str]) -> dict[str, Any]:
        if self.client is not None:
            response = self.client.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()

        with httpx.Client() as client:
            response = client.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()


def daily_bars_from_alpha_vantage_payload(symbol: str, payload: dict[str, Any]) -> list[DailyBar]:
    _raise_for_alpha_vantage_message(payload)
    series = payload.get(TIME_SERIES_DAILY_KEY)
    if not isinstance(series, dict):
        raise AlphaVantageError(f"Alpha Vantage payload missing '{TIME_SERIES_DAILY_KEY}'.")

    bars: list[DailyBar] = []
    for bar_date in sorted(series):
        values = series[bar_date]
        if not isinstance(values, dict) or not is_iso_date(bar_date):
            continue

        open_value = _positive_float(values.get("1. open"))
        high_value = _positive_float(values.get("2. high"))
        low_value = _positive_float(values.get("3. low"))
        close_value = _positive_float(values.get("4. close"))
        adjusted_close = _positive_float(values.get("5. adjusted close")) or close_value
        volume = _nonnegative_int(values.get("6. volume") or values.get("5. volume"))

        if None in {open_value, high_value, low_value, close_value, adjusted_close, volume}:
            continue
        if not is_valid_daily_bar_values(open_value, high_value, low_value, close_value, adjusted_close, volume):
            continue

        bars.append(
            DailyBar(
                symbol=symbol.upper(),
                date=date.fromisoformat(bar_date),
                open=open_value,
                high=high_value,
                low=low_value,
                close=close_value,
                adjusted_close=adjusted_close,
                volume=volume,
            )
        )
    return bars


def _raise_for_alpha_vantage_message(payload: dict[str, Any]) -> None:
    for key in ("Error Message", "Note", "Information"):
        message = payload.get(key)
        if message:
            raise AlphaVantageError(str(message))


def _positive_float(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _nonnegative_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None
