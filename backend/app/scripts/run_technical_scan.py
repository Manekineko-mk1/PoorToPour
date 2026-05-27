import argparse

from app.db.base import SessionLocal
from app.repositories.market_data import get_daily_bars, list_symbols
from app.repositories.scans import upsert_scan_run
from app.services.scanner import TechnicalScanner


def run_technical_scan(limit: int | None = None, include_blocked: bool = False) -> str:
    db = SessionLocal()
    try:
        symbols = list_symbols(db)
        if limit is not None:
            symbols = symbols[:limit]

        bars_by_symbol = {symbol.symbol: get_daily_bars(db, symbol.symbol) for symbol in symbols}
        scan = TechnicalScanner(include_blocked=include_blocked).scan(
            symbols=symbols,
            bars_by_symbol=bars_by_symbol,
            provider="TechnicalScanner + persisted bars",
            universe="Persisted symbols",
        )
        upsert_scan_run(db, scan)
        db.commit()
        return scan.scan_id
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Phase 2 deterministic technical scanner.")
    parser.add_argument("--limit", type=int, default=None, help="Optional symbol limit for local testing.")
    parser.add_argument(
        "--include-blocked",
        action="store_true",
        help="Persist blocked candidates for data-quality inspection. Defaults to false to avoid noisy scans.",
    )
    args = parser.parse_args()

    scan_id = run_technical_scan(limit=args.limit, include_blocked=args.include_blocked)
    print(f"Persisted generated technical scan: {scan_id}")


if __name__ == "__main__":
    main()
