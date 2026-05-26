from pathlib import Path

from app.scripts.seed_sp500_universe import parse_sp500_seed


def test_sp500_seed_file_parses_expected_columns() -> None:
    path = Path(__file__).resolve().parents[2] / "data" / "seeds" / "sp500_seed.csv"

    symbols = parse_sp500_seed(path)

    assert len(symbols) >= 500
    assert symbols[0].symbol == "MMM"
    assert symbols[0].company_name == "3M"
    assert symbols[0].exchange == "UNKNOWN"
