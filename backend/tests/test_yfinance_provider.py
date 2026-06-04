import pandas as pd

from app.providers import yfinance_provider
from app.providers.yfinance_provider import YFinanceProvider, daily_bars_from_frame, to_yfinance_symbol


def test_to_yfinance_symbol_converts_share_class_dot() -> None:
    assert to_yfinance_symbol("BRK.B") == "BRK-B"


def test_daily_bars_from_single_level_frame() -> None:
    frame = pd.DataFrame(
        [
            {
                "Open": 100.0,
                "High": 110.0,
                "Low": 99.5,
                "Close": 108.0,
                "Adj Close": 107.5,
                "Volume": 123456,
            }
        ],
        index=pd.to_datetime(["2026-05-22"]),
    )

    bars = daily_bars_from_frame("AAPL", frame)

    assert len(bars) == 1
    assert bars[0].symbol == "AAPL"
    assert bars[0].date == "2026-05-22"
    assert bars[0].adjusted_close == 107.5
    assert bars[0].volume == 123456


def test_daily_bars_from_multiindex_frame() -> None:
    frame = pd.DataFrame(
        [[108.0, 110.0, 99.5, 100.0, 123456]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples(
            [
                ("Close", "AAPL"),
                ("High", "AAPL"),
                ("Low", "AAPL"),
                ("Open", "AAPL"),
                ("Volume", "AAPL"),
            ]
        ),
    )

    bars = daily_bars_from_frame("AAPL", frame)

    assert len(bars) == 1
    assert bars[0].close == 108.0
    assert bars[0].adjusted_close == 108.0


def test_daily_bars_from_frame_skips_inconsistent_ohlc_rows() -> None:
    frame = pd.DataFrame(
        [
            {
                "Open": 100.0,
                "High": 99.0,
                "Low": 98.0,
                "Close": 100.5,
                "Adj Close": 100.5,
                "Volume": 123456,
            },
            {
                "Open": 100.0,
                "High": 101.0,
                "Low": 99.0,
                "Close": 100.5,
                "Adj Close": 100.5,
                "Volume": 123456,
            },
        ],
        index=pd.to_datetime(["2026-05-21", "2026-05-22"]),
    )

    bars = daily_bars_from_frame("AAPL", frame)

    assert [bar.date for bar in bars] == ["2026-05-22"]


def test_provider_parses_batch_download_frame(monkeypatch) -> None:
    frame = pd.DataFrame(
        [[100.0, 110.0, 99.5, 108.0, 107.5, 123456, 200.0, 202.0, 198.0, 201.0, 201.0, 654321]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples(
            [
                ("AAPL", "Open"),
                ("AAPL", "High"),
                ("AAPL", "Low"),
                ("AAPL", "Close"),
                ("AAPL", "Adj Close"),
                ("AAPL", "Volume"),
                ("MSFT", "Open"),
                ("MSFT", "High"),
                ("MSFT", "Low"),
                ("MSFT", "Close"),
                ("MSFT", "Adj Close"),
                ("MSFT", "Volume"),
            ]
        ),
    )

    monkeypatch.setattr(yfinance_provider.yf, "download", lambda **kwargs: frame)

    bars_by_symbol = YFinanceProvider().get_daily_bars_for_symbols(["AAPL", "MSFT"], period="1y")

    assert bars_by_symbol["AAPL"][0].close == 108.0
    assert bars_by_symbol["MSFT"][0].close == 201.0
