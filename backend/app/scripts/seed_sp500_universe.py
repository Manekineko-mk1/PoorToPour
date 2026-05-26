import argparse
import csv
from pathlib import Path

from app.db.base import SessionLocal
from app.models.market_data import SymbolProfile
from app.repositories.market_data import upsert_symbol

DEFAULT_SEED_PATHS = [
    Path("/data/seeds/sp500_seed.csv"),
    Path(__file__).resolve().parents[3] / "data" / "seeds" / "sp500_seed.csv",
]


def parse_sp500_seed(path: Path) -> list[SymbolProfile]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = csv.DictReader(file)
        symbols = []
        for row in rows:
            symbol = row["Symbol"].strip().upper()
            if not symbol:
                continue
            symbols.append(
                SymbolProfile(
                    symbol=symbol,
                    company_name=row["Security"].strip(),
                    sector=row["GICS Sector"].strip(),
                    industry=row["GICS Sub-Industry"].strip(),
                    exchange="UNKNOWN",
                    is_active=True,
                )
            )
        return symbols


def resolve_default_seed_path() -> Path:
    for path in DEFAULT_SEED_PATHS:
        if path.exists():
            return path
    return DEFAULT_SEED_PATHS[0]


def seed_sp500_universe(path: Path) -> int:
    symbols = parse_sp500_seed(path)
    db = SessionLocal()
    try:
        for symbol in symbols:
            upsert_symbol(db, symbol)
        db.commit()
        return len(symbols)
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed S&P 500 universe into PostgreSQL.")
    parser.add_argument(
        "--path",
        type=Path,
        default=resolve_default_seed_path(),
        help="Path to sp500_seed.csv",
    )
    args = parser.parse_args()

    count = seed_sp500_universe(args.path)
    print(f"Seeded S&P 500 universe from {args.path} ({count} symbols).")


if __name__ == "__main__":
    main()
