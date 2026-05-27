import argparse

from app.core.config import get_settings
from app.db.base import SessionLocal
from app.providers.alpha_vantage_provider import AlphaVantageProvider
from app.repositories.market_data import upsert_daily_bar
from app.scripts.symbol_resolution import resolve_symbols


def ingest_alpha_vantage_bars(
    symbols: list[str],
    outputsize: str,
    daily_function: str | None = None,
) -> dict[str, int]:
    settings = get_settings()
    provider = AlphaVantageProvider(
        api_key=settings.alpha_vantage_api_key,
        daily_function=daily_function or settings.alpha_vantage_daily_function,
    )
    counts: dict[str, int] = {}
    db = SessionLocal()
    try:
        for symbol in symbols:
            bars = provider.get_daily_bars(symbol, outputsize=outputsize)
            for bar in bars:
                upsert_daily_bar(db, bar, source="alpha_vantage")
            counts[symbol.upper()] = len(bars)
        db.commit()
        return counts
    finally:
        db.close()

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest daily OHLCV bars from Alpha Vantage into PostgreSQL.")
    parser.add_argument("--symbols", nargs="+", help="Symbols to ingest. Defaults to persisted symbols.")
    parser.add_argument("--limit", type=int, default=5, help="Limit symbols ingested from the persisted universe.")
    parser.add_argument("--outputsize", default="compact", choices=["compact", "full"])
    parser.add_argument(
        "--daily-function",
        choices=["TIME_SERIES_DAILY", "TIME_SERIES_DAILY_ADJUSTED"],
        help="Alpha Vantage daily function. Defaults to POORTOPOUR_ALPHA_VANTAGE_DAILY_FUNCTION.",
    )
    args = parser.parse_args()

    symbols = resolve_symbols(args.symbols, args.limit)
    counts = ingest_alpha_vantage_bars(symbols, args.outputsize, daily_function=args.daily_function)
    total = sum(counts.values())
    print(f"Ingested {total} daily bars from Alpha Vantage across {len(counts)} symbols.")
    for symbol, count in counts.items():
        print(f"- {symbol}: {count}")


if __name__ == "__main__":
    main()
