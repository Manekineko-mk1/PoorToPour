import argparse
import csv
from pathlib import Path

from app.db.base import SessionLocal
from app.models.market_data import SymbolProfile
from app.repositories.market_data import upsert_symbol
from app.scripts.seed_sp500_universe import parse_sp500_seed

DEFAULT_SP500_SEED_PATHS = [
    Path("/data/seeds/sp500_seed.csv"),
    Path(__file__).resolve().parents[3] / "data" / "seeds" / "sp500_seed.csv",
]
DEFAULT_NASDAQ100_SEED_PATHS = [
    Path("/data/seeds/nasdaq100_seed.csv"),
    Path(__file__).resolve().parents[3] / "data" / "seeds" / "nasdaq100_seed.csv",
]


def parse_nasdaq100_seed(path: Path) -> list[SymbolProfile]:
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
                    sector=row["ICB Industry"].strip(),
                    industry=row["ICB Subsector"].strip(),
                    exchange="NASDAQ",
                    is_active=True,
                )
            )
        return symbols


def merge_universe_symbols(
    primary_symbols: list[SymbolProfile],
    secondary_symbols: list[SymbolProfile],
) -> list[SymbolProfile]:
    merged: dict[str, SymbolProfile] = {}
    for symbol in primary_symbols + secondary_symbols:
        normalized_symbol = symbol.symbol.strip().upper()
        if normalized_symbol not in merged:
            merged[normalized_symbol] = symbol.model_copy(update={"symbol": normalized_symbol})
    return list(merged.values())


def parse_mvp_universe_seed(sp500_path: Path, nasdaq100_path: Path) -> list[SymbolProfile]:
    sp500_symbols = parse_sp500_seed(sp500_path)
    nasdaq100_symbols = parse_nasdaq100_seed(nasdaq100_path)
    return merge_universe_symbols(sp500_symbols, nasdaq100_symbols)


def resolve_default_seed_path(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def seed_mvp_universe(sp500_path: Path, nasdaq100_path: Path) -> int:
    symbols = parse_mvp_universe_seed(sp500_path, nasdaq100_path)
    db = SessionLocal()
    try:
        for symbol in symbols:
            upsert_symbol(db, symbol)
        db.commit()
        return len(symbols)
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed PoorToPour MVP universe into PostgreSQL: S&P 500 plus Nasdaq 100."
    )
    parser.add_argument(
        "--sp500-path",
        type=Path,
        default=resolve_default_seed_path(DEFAULT_SP500_SEED_PATHS),
        help="Path to sp500_seed.csv",
    )
    parser.add_argument(
        "--nasdaq100-path",
        type=Path,
        default=resolve_default_seed_path(DEFAULT_NASDAQ100_SEED_PATHS),
        help="Path to nasdaq100_seed.csv",
    )
    args = parser.parse_args()

    count = seed_mvp_universe(args.sp500_path, args.nasdaq100_path)
    print(
        "Seeded MVP universe from "
        f"{args.sp500_path} and {args.nasdaq100_path} ({count} unique symbols)."
    )


if __name__ == "__main__":
    main()
