from pathlib import Path

from app.scripts.seed_sp500_universe import parse_sp500_seed
from app.scripts.seed_mvp_universe import (
    merge_universe_symbols,
    parse_mvp_universe_seed,
    parse_nasdaq100_seed,
)


def test_sp500_seed_file_parses_expected_columns() -> None:
    path = Path(__file__).resolve().parents[2] / "data" / "seeds" / "sp500_seed.csv"

    symbols = parse_sp500_seed(path)

    assert len(symbols) >= 500
    assert symbols[0].symbol == "MMM"
    assert symbols[0].company_name == "3M"
    assert symbols[0].exchange == "UNKNOWN"


def test_nasdaq100_seed_file_parses_expected_columns() -> None:
    path = Path(__file__).resolve().parents[2] / "data" / "seeds" / "nasdaq100_seed.csv"

    symbols = parse_nasdaq100_seed(path)

    assert len(symbols) >= 100
    assert symbols[0].symbol == "ADBE"
    assert symbols[0].company_name == "Adobe Inc."
    assert symbols[0].exchange == "NASDAQ"


def test_mvp_universe_seed_merges_sp500_and_nasdaq100_without_duplicates() -> None:
    seed_dir = Path(__file__).resolve().parents[2] / "data" / "seeds"

    symbols = parse_mvp_universe_seed(
        seed_dir / "sp500_seed.csv",
        seed_dir / "nasdaq100_seed.csv",
    )
    unique_symbols = {symbol.symbol for symbol in symbols}

    assert len(symbols) == len(unique_symbols)
    assert len(symbols) > 503
    assert any(symbol.symbol == "ARM" and symbol.exchange == "NASDAQ" for symbol in symbols)


def test_universe_merge_keeps_primary_metadata_for_overlaps() -> None:
    seed_dir = Path(__file__).resolve().parents[2] / "data" / "seeds"
    sp500_symbols = parse_sp500_seed(seed_dir / "sp500_seed.csv")
    nasdaq100_symbols = parse_nasdaq100_seed(seed_dir / "nasdaq100_seed.csv")

    symbols = merge_universe_symbols(sp500_symbols, nasdaq100_symbols)
    by_symbol = {symbol.symbol: symbol for symbol in symbols}

    assert by_symbol["AAPL"].exchange == "UNKNOWN"
    assert by_symbol["AAPL"].sector == "Information Technology"
