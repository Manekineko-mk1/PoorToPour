from app.db.base import SessionLocal
from app.repositories.market_data import list_symbols


DEFAULT_DEVELOPMENT_SYMBOLS = ("AAPL", "MSFT", "NVDA", "AMZN", "META")


def resolve_symbols(requested_symbols: list[str] | None, limit: int | None) -> list[str]:
    if requested_symbols:
        symbols = [symbol.upper() for symbol in requested_symbols]
    else:
        symbols = _persisted_symbols() or list(DEFAULT_DEVELOPMENT_SYMBOLS)

    if limit is not None:
        symbols = symbols[:limit]
    return symbols


def _persisted_symbols() -> list[str]:
    db = SessionLocal()
    try:
        return [symbol.symbol for symbol in list_symbols(db)]
    finally:
        db.close()
