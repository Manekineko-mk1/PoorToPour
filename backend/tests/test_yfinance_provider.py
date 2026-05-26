import pandas as pd

from app.providers.yfinance_provider import daily_bars_from_frame, to_yfinance_symbol


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
