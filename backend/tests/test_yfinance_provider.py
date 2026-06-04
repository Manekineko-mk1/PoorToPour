from datetime import date

import pandas as pd

from app.providers import yfinance_provider
from app.providers.yfinance_provider import (
    YFinanceProvider,
    _frame_for_downloaded_symbol,
    daily_bars_from_frame,
    to_yfinance_symbol,
)


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
    assert bars[0].date == date(2026, 5, 22)
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

    assert [bar.date for bar in bars] == [date(2026, 5, 22)]


def test_frame_for_downloaded_symbol_flat_frame_returned_unchanged() -> None:
    frame = pd.DataFrame(
        [{"Open": 100.0, "High": 110.0, "Low": 99.5, "Close": 108.0, "Volume": 123456}],
        index=pd.to_datetime(["2026-05-22"]),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    pd.testing.assert_frame_equal(result, frame)


def test_frame_for_downloaded_symbol_empty_frame_returned_unchanged() -> None:
    frame = pd.DataFrame()
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert result.empty


def test_frame_for_downloaded_symbol_symbol_in_level_1_field_ticker_layout() -> None:
    # yfinance sometimes returns (field, ticker) with the symbol at level 1
    frame = pd.DataFrame(
        [[100.0, 110.0, 99.5, 108.0, 123456]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples(
            [("Open", "AAPL"), ("High", "AAPL"), ("Low", "AAPL"), ("Close", "AAPL"), ("Volume", "AAPL")]
        ),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert list(result.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert result.iloc[0]["Open"] == 100.0


def test_frame_for_downloaded_symbol_symbol_in_level_0_ticker_field_layout() -> None:
    # yfinance sometimes returns (ticker, field) with the symbol at level 0
    frame = pd.DataFrame(
        [[100.0, 110.0, 99.5, 108.0, 123456]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples(
            [("AAPL", "Open"), ("AAPL", "High"), ("AAPL", "Low"), ("AAPL", "Close"), ("AAPL", "Volume")]
        ),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert list(result.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert result.iloc[0]["Close"] == 108.0


def test_frame_for_downloaded_symbol_symbol_absent_returns_empty_with_original_index() -> None:
    frame = pd.DataFrame(
        [[200.0, 202.0]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples([("Open", "MSFT"), ("High", "MSFT")]),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert result.empty
    assert list(result.index) == list(frame.index)


def test_frame_for_downloaded_symbol_match_is_case_insensitive() -> None:
    frame = pd.DataFrame(
        [[100.0]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples([("Open", "aapl")]),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert not result.empty
    assert result.iloc[0]["Open"] == 100.0


def test_frame_for_downloaded_symbol_none_values_in_level_do_not_crash() -> None:
    # A corrupted MultiIndex with None in one level should not raise
    frame = pd.DataFrame(
        [[100.0, 110.0]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples([(None, "AAPL_Open"), (None, "AAPL_High")]),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert isinstance(result, pd.DataFrame)


def test_frame_for_downloaded_symbol_three_level_multiindex_does_not_crash() -> None:
    # A 3-level MultiIndex is unexpected but must not raise
    frame = pd.DataFrame(
        [[100.0, 110.0]],
        index=pd.to_datetime(["2026-05-22"]),
        columns=pd.MultiIndex.from_tuples([("extra", "Open", "AAPL"), ("extra", "High", "AAPL")]),
    )
    result = _frame_for_downloaded_symbol(frame, "AAPL")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


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
