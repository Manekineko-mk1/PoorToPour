import argparse

from app.db.base import SessionLocal
from app.providers.yfinance_provider import YFinanceProvider
from app.repositories.market_data import list_symbols, upsert_daily_bar


DEFAULT_SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]


def ingest_yfinance_bars(symbols: list[str], period: str) -> dict[str, int]:
    provider = YFinanceProvider()
    counts: dict[str, int] = {}
    db = SessionLocal()
    try:
        for symbol in symbols:
            bars = provider.get_daily_bars(symbol, period=period)
            for bar in bars:
                upsert_daily_bar(db, bar, source="yfinance")
            counts[symbol.upper()] = len(bars)
        db.commit()
        return counts
    finally:
        db.close()


def resolve_symbols(requested_symbols: list[str] | None, limit: int | None) -> list[str]:
    if requested_symbols:
        symbols = [symbol.upper() for symbol in requested_symbols]
    else:
        db = SessionLocal()
        try:
            symbols = [symbol.symbol for symbol in list_symbols(db)]
        finally:
            db.close()
        if not symbols:
            symbols = DEFAULT_SYMBOLS

    if limit is not None:
        symbols = symbols[:limit]
    return symbols


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest daily OHLCV bars from yfinance into PostgreSQL.")
    parser.add_argument("--symbols", nargs="+", help="Symbols to ingest. Defaults to persisted symbols.")
    parser.add_argument("--limit", type=int, default=5, help="Limit symbols ingested from the persisted universe.")
    parser.add_argument("--period", default="1y", help="yfinance period, such as 3mo, 6mo, 1y, or 5y.")
    args = parser.parse_args()

    symbols = resolve_symbols(args.symbols, args.limit)
    counts = ingest_yfinance_bars(symbols, args.period)
    total = sum(counts.values())
    print(f"Ingested {total} daily bars from yfinance across {len(counts)} symbols.")
    for symbol, count in counts.items():
        print(f"- {symbol}: {count}")


if __name__ == "__main__":
    main()
