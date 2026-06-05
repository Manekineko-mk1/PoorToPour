import logging
from datetime import date
from typing import Any

import pandas as pd
import yfinance as yf

from app.models.market_data import DailyBar, ProviderStatus
from app.providers.validation import is_valid_daily_bar_values

logger = logging.getLogger(__name__)


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
        logger.debug("yfinance single download", extra={"yf_symbol": yf_symbol, "period": period})
        frame = yf.download(
            yf_symbol,
            period=period,
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False,
        )
        return daily_bars_from_frame(symbol, frame)

    def get_daily_bars_for_symbols(self, symbols: list[str], period: str = "1y") -> dict[str, list[DailyBar]]:
        normalized_symbols = [symbol.upper() for symbol in symbols]
        if not normalized_symbols:
            return {}

        if len(normalized_symbols) == 1:
            symbol = normalized_symbols[0]
            return {symbol: self.get_daily_bars(symbol, period=period)}

        yfinance_symbols = [to_yfinance_symbol(symbol) for symbol in normalized_symbols]
        logger.debug(
            "yfinance batch download",
            extra={"symbol_count": len(yfinance_symbols), "period": period},
        )
        frame = yf.download(
            tickers=yfinance_symbols,
            period=period,
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=True,
            group_by="ticker",
        )
        return {
            symbol: daily_bars_from_frame(symbol, _frame_for_downloaded_symbol(frame, to_yfinance_symbol(symbol)))
            for symbol in normalized_symbols
        }


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
                date=timestamp.date(),
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


def _frame_for_downloaded_symbol(frame: pd.DataFrame, yf_symbol: str) -> pd.DataFrame:
    if frame.empty:
        return frame
    if not isinstance(frame.columns, pd.MultiIndex):
        # Single-symbol download: columns are already flat OHLCV fields.
        return frame

    target = _normalize_symbol_label(yf_symbol)
    for level in range(frame.columns.nlevels):
        raw_values = frame.columns.get_level_values(level)
        # Match tolerantly: yfinance may label a ticker with different casing,
        # surrounding whitespace, or a "." separator where we requested "-"
        # (e.g. "BRK.B" vs "BRK-B"). An exact-only match would silently drop
        # data that is actually present under one of these variant labels.
        actual_label = next(
            (v for v in raw_values if _normalize_symbol_label(v) == target),
            None,
        )
        if actual_label is not None:
            try:
                return frame.xs(actual_label, axis=1, level=level, drop_level=True)
            except (KeyError, TypeError, ValueError) as exc:
                logger.debug(
                    "yfinance frame cross-section failed, trying next level",
                    extra={"yf_symbol": yf_symbol, "level": level, "exc_type": type(exc).__name__},
                )
                continue

    # No column level matched the requested symbol. The frame is non-empty, so
    # data may be present under a label we did not anticipate. Surface this
    # loudly instead of returning a silently-empty result that downstream code
    # cannot distinguish from a genuinely empty download.
    logger.warning(
        "yfinance batch frame has no columns matching requested symbol; "
        "returning empty result (data may exist under an unexpected label)",
        extra={
            "yf_symbol": yf_symbol,
            "available_labels": _column_label_preview(frame.columns),
        },
    )
    return pd.DataFrame(index=frame.index)


def _normalize_symbol_label(value: Any) -> str:
    """Canonicalize a ticker label for tolerant matching.

    Uppercases, trims whitespace, and treats "." and "-" as equivalent so
    requested symbols match yfinance's column labels across separator and
    casing variations.
    """
    return str(value).strip().upper().replace(".", "-")


def _column_label_preview(columns: pd.MultiIndex, limit: int = 20) -> list[str]:
    """Distinct, stringified column labels across all levels for diagnostics."""
    seen: list[str] = []
    for level in range(columns.nlevels):
        for value in columns.get_level_values(level):
            label = str(value)
            if label not in seen:
                seen.append(label)
                if len(seen) >= limit:
                    return seen
    return seen


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
