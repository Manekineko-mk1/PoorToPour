from datetime import date, timedelta

import pytest

from app.models.market_data import DailyBar
from app.services.indicators import (
    IndicatorService,
    average_true_range,
    exponential_moving_average,
    prior_rolling_high,
    simple_moving_average,
)


def test_simple_moving_average_requires_full_period() -> None:
    assert simple_moving_average([1, 2, 3], 5) is None
    assert simple_moving_average([1, 2, 3, 4, 5], 5) == 3


def test_exponential_moving_average_uses_sma_seed() -> None:
    assert exponential_moving_average([10, 11, 12], 5) is None
    assert exponential_moving_average([10, 11, 12, 13, 14], 5) == 12


def test_prior_rolling_high_excludes_latest_bar() -> None:
    assert prior_rolling_high([1, 2, 3], 3) is None
    assert prior_rolling_high([1, 2, 3, 4], 3) == 3


def test_average_true_range_uses_latest_true_ranges() -> None:
    bars = [_bar(index) for index in range(1, 16)]

    assert average_true_range(bars, 14) == 2


def test_indicator_snapshot_calculates_latest_values() -> None:
    service = IndicatorService()
    bars = [_bar(index) for index in range(1, 253)]

    snapshot = service.build_snapshot("AAPL", bars)

    assert snapshot.symbol == "AAPL"
    assert snapshot.latest_date == "2026-09-09"
    assert snapshot.close == 252
    assert snapshot.data_points == 252
    assert snapshot.sma_20 == 242.5
    assert snapshot.sma_50 == 227.5
    assert snapshot.sma_200 == 152.5
    assert snapshot.avg_volume_20 == 1242500
    assert snapshot.relative_volume_20 == pytest.approx(1.0076, abs=0.0001)
    assert snapshot.atr_14 == 2
    assert snapshot.atr_14_pct == pytest.approx(0.7937, abs=0.0001)
    assert snapshot.high_20_day == 253
    assert snapshot.high_50_day == 253
    assert snapshot.prior_high_20_day == 252
    assert snapshot.prior_high_50_day == 252
    assert snapshot.low_20_day == 232.5
    assert snapshot.close_distance_from_20_day_high_pct == pytest.approx(-0.3953, abs=0.0001)
    assert snapshot.close_distance_from_50_day_high_pct == pytest.approx(-0.3953, abs=0.0001)
    assert snapshot.close_position_in_20_day_range_pct == pytest.approx(95.122, abs=0.0001)
    assert snapshot.high_52_week == 253
    assert snapshot.high_52_week_distance_pct == pytest.approx(-0.3953, abs=0.0001)
    assert snapshot.close_above_sma_20 is True
    assert snapshot.close_above_sma_50 is True
    assert snapshot.close_above_sma_200 is True
    assert snapshot.close_above_prior_20_day_high is False
    assert snapshot.close_above_prior_50_day_high is False
    assert snapshot.warnings == []


def test_indicator_snapshot_reports_insufficient_history() -> None:
    service = IndicatorService()

    snapshot = service.build_snapshot("NVDA", [_bar(index) for index in range(1, 11)])

    assert snapshot.sma_20 is None
    assert snapshot.ema_21 is None
    assert snapshot.atr_14 is None
    assert snapshot.high_20_day is None
    assert snapshot.prior_high_20_day is None
    assert snapshot.high_52_week is None
    assert len(snapshot.warnings) == 5


def test_indicator_snapshot_detects_breakout_above_prior_highs() -> None:
    service = IndicatorService()
    bars = [_bar(index) for index in range(1, 60)]
    latest = bars[-1]
    bars[-1] = latest.model_copy(update={"close": latest.high + 1, "high": latest.high + 1.5})

    snapshot = service.build_snapshot("AAPL", bars)

    assert snapshot.close_above_prior_20_day_high is True
    assert snapshot.close_above_prior_50_day_high is True


def test_indicator_snapshot_requires_bars() -> None:
    service = IndicatorService()

    with pytest.raises(ValueError):
        service.build_snapshot("MSFT", [])


def _bar(index: int) -> DailyBar:
    bar_date = date(2026, 1, 1) + timedelta(days=index - 1)
    close = float(index)
    return DailyBar(
        symbol="AAPL",
        date=bar_date.isoformat(),
        open=max(close - 0.25, 0.01),
        high=close + 1,
        low=max(close - 0.5, 0.01),
        close=close,
        adjusted_close=close,
        volume=1_000_000 + index * 1_000,
    )
