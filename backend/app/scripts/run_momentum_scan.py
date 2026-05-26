import argparse

from app.db.base import SessionLocal
from app.repositories.market_data import get_daily_bars, list_symbols
from app.repositories.scans import upsert_scan_run
from app.services.scanner import MomentumScanner


def run_momentum_scan(limit: int | None = None) -> str:
    db = SessionLocal()
    try:
        symbols = list_symbols(db)
        if limit is not None:
            symbols = symbols[:limit]

        bars_by_symbol = {symbol.symbol: get_daily_bars(db, symbol.symbol) for symbol in symbols}
        scan = MomentumScanner().scan(
            symbols=symbols,
            bars_by_symbol=bars_by_symbol,
            provider="Internal MomentumScanner + persisted bars",
            universe="Persisted symbols",
        )
        upsert_scan_run(db, scan)
        db.commit()
        return scan.scan_id
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Phase 1 bootstrap momentum scanner.")
    parser.add_argument("--limit", type=int, default=None, help="Optional symbol limit for local testing.")
    args = parser.parse_args()

    scan_id = run_momentum_scan(limit=args.limit)
    print(f"Persisted generated momentum scan: {scan_id}")


if __name__ == "__main__":
    main()
