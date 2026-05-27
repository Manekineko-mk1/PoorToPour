from datetime import date
from typing import Any

import pandas as pd
import yfinance as yf

from app.models.market_data import DailyBar, ProviderStatus
from app.providers.validation import is_valid_daily_bar_values


class YFinanceProvider:
    """Bootstrap OHLCV provider for local MVP development.

    yfinance is useful for Phase 1 experimentation, but it is not treated as
    the final trading-grade market data provider.
    """

    def get_status(self) -> ProviderStatus:
        return ProviderStatus(
            provider="Yahoo Finance via yfinance",
            mode="bootstrap",
            status="ok",
            message="Manual bootstrap provider for local OHLCV ingestion. Not final trading-grade data.",
            data_date=date.today().isoformat(),
        )

    def get_daily_bars(self, symbol: str, period: str = "1y") -> list[DailyBar]:
        yf_symbol = to_yfinance_symbol(symbol)
        frame = yf.download(
            yf_symbol,
            period=period,
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False,
        )
        return daily_bars_from_frame(symbol, frame)


def to_yfinance_symbol(symbol: str) -> str:
    return symbol.upper().replace(".", "-")


def daily_bars_from_frame(symbol: str, frame: pd.DataFrame) -> list[DailyBar]:
    if frame.empty:
        return []

    normalized = _normalize_columns(frame, symbol)
    bars: list[DailyBar] = []
    for timestamp, row in normalized.iterrows():
        open_value = row.get("open")
        high_value = row.get("high")
        low_value = row.get("low")
        close_value = row.get("close")
        adjusted_close = row.get("adjusted_close", close_value)
        volume = row.get("volume", 0)

        if any(pd.isna(value) for value in [open_value, high_value, low_value, close_value, adjusted_close]):
            continue

        open_float = float(open_value)
        high_float = float(high_value)
        low_float = float(low_value)
        close_float = float(close_value)
        adjusted_close_float = float(adjusted_close)
        volume_int = int(volume) if not pd.isna(volume) else 0

        if not is_valid_daily_bar_values(
            open_float,
            high_float,
            low_float,
            close_float,
            adjusted_close_float,
            volume_int,
        ):
            continue

        bars.append(
            DailyBar(
                symbol=symbol.upper(),
                date=timestamp.date().isoformat(),
                open=open_float,
                high=high_float,
                low=low_float,
                close=close_float,
                adjusted_close=adjusted_close_float,
                volume=volume_int,
            )
        )
    return bars


def _normalize_columns(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    normalized = frame.copy()
    if isinstance(normalized.columns, pd.MultiIndex):
        normalized.columns = [_field_from_multiindex(column, symbol) for column in normalized.columns]
    else:
        normalized.columns = [_canonical_field(column) for column in normalized.columns]
    return normalized


def _field_from_multiindex(column: tuple[Any, ...], symbol: str) -> str:
    symbol_parts = {symbol.upper(), to_yfinance_symbol(symbol).upper()}
    parts = [str(part) for part in column if str(part).upper() not in symbol_parts]
    for part in parts:
        canonical = _canonical_field(part)
        if canonical in {"open", "high", "low", "close", "adjusted_close", "volume"}:
            return canonical
    return _canonical_field(parts[0] if parts else column[0])


def _canonical_field(value: Any) -> str:
    field = str(value).strip().lower().replace(" ", "_")
    if field == "adj_close":
        return "adjusted_close"
    return field
