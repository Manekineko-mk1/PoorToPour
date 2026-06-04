from collections.abc import Iterable

from sqlalchemy.orm import Session

from app.models.market_data import MarketDataRefreshSummary, SymbolProfile
from app.providers.yfinance_provider import YFinanceProvider
from app.repositories.market_data import upsert_daily_bar

DEFAULT_REFRESH_CHUNK_SIZE = 50
MAX_FAILURE_MESSAGES = 12
YFINANCE_PROVIDER_LABEL = "Yahoo Finance via yfinance"


def refresh_yfinance_daily_bars(
    db: Session,
    symbols: list[SymbolProfile],
    period: str = "1y",
    provider: YFinanceProvider | None = None,
    chunk_size: int = DEFAULT_REFRESH_CHUNK_SIZE,
) -> MarketDataRefreshSummary:
    provider = provider or YFinanceProvider()
    summary = MarketDataRefreshSummary(
        provider=YFINANCE_PROVIDER_LABEL,
        period=period,
        symbols_requested=len(symbols),
    )

    for symbol_chunk in _chunks([symbol.symbol for symbol in symbols], chunk_size):
        try:
            bars_by_symbol = provider.get_daily_bars_for_symbols(symbol_chunk, period=period)
        except Exception as exc:
            for symbol in symbol_chunk:
                _record_failure(summary, f"{symbol}: {exc}")
            continue

        for symbol in symbol_chunk:
            normalized_symbol = symbol.upper()
            bars = bars_by_symbol.get(normalized_symbol, [])
            if not bars:
                _record_failure(summary, f"{normalized_symbol}: no daily bars returned")
                continue

            summary.symbols_refreshed += 1
            summary.bars_persisted += len(bars)
            for bar in bars:
                upsert_daily_bar(db, bar, source="yfinance")

    return summary


def _chunks(values: list[str], size: int) -> Iterable[list[str]]:
    safe_size = max(size, 1)
    for index in range(0, len(values), safe_size):
        yield values[index:index + safe_size]


def _record_failure(summary: MarketDataRefreshSummary, message: str) -> None:
    summary.symbols_failed += 1
    if len(summary.failure_messages) < MAX_FAILURE_MESSAGES:
        summary.failure_messages.append(message)
