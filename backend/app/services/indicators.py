from collections.abc import Sequence

from app.models.indicators import IndicatorSnapshot
from app.models.market_data import DailyBar


class IndicatorService:
    """Deterministic technical indicator calculations over persisted daily bars."""

    def build_snapshot(self, symbol: str, bars: Sequence[DailyBar]) -> IndicatorSnapshot:
        ordered_bars = sorted(bars, key=lambda bar: bar.date)
        if not ordered_bars:
            raise ValueError("Indicator snapshot requires at least one daily bar.")

        latest = ordered_bars[-1]
        closes = [bar.close for bar in ordered_bars]
        highs = [bar.high for bar in ordered_bars]
        lows = [bar.low for bar in ordered_bars]
        volumes = [bar.volume for bar in ordered_bars]

        sma_20 = simple_moving_average(closes, 20)
        sma_50 = simple_moving_average(closes, 50)
        sma_200 = simple_moving_average(closes, 200)
        ema_21 = exponential_moving_average(closes, 21)
        avg_volume_20 = simple_moving_average([float(volume) for volume in volumes], 20)
        atr_14 = average_true_range(ordered_bars, 14)
        high_20_day = rolling_high(highs, 20)
        high_50_day = rolling_high(highs, 50)
        prior_high_20_day = prior_rolling_high(highs, 20)
        prior_high_50_day = prior_rolling_high(highs, 50)
        low_20_day = rolling_low(lows, 20)
        high_52_week = rolling_high(highs, 252)

        warnings = []
        for period in (20, 50, 200, 252):
            if len(ordered_bars) < period:
                warnings.append(f"Only {len(ordered_bars)} bars available; {period}-day indicator is incomplete.")
        if len(ordered_bars) < 15:
            warnings.append(f"Only {len(ordered_bars)} bars available; 14-day ATR is incomplete.")

        return IndicatorSnapshot(
            symbol=symbol.upper(),
            latest_date=latest.date.isoformat(),
            close=round(latest.close, 4),
            volume=latest.volume,
            data_points=len(ordered_bars),
            sma_20=_round_optional(sma_20),
            sma_50=_round_optional(sma_50),
            sma_200=_round_optional(sma_200),
            ema_21=_round_optional(ema_21),
            avg_volume_20=_round_optional(avg_volume_20),
            relative_volume_20=_round_optional(latest.volume / avg_volume_20 if avg_volume_20 else None),
            atr_14=_round_optional(atr_14),
            atr_14_pct=_round_optional((atr_14 / latest.close) * 100 if atr_14 else None),
            high_20_day=_round_optional(high_20_day),
            high_50_day=_round_optional(high_50_day),
            prior_high_20_day=_round_optional(prior_high_20_day),
            prior_high_50_day=_round_optional(prior_high_50_day),
            low_20_day=_round_optional(low_20_day),
            close_distance_from_20_day_high_pct=_round_optional(
                _percent_distance(latest.close, high_20_day)
            ),
            close_distance_from_50_day_high_pct=_round_optional(
                _percent_distance(latest.close, high_50_day)
            ),
            close_position_in_20_day_range_pct=_round_optional(
                _range_position_pct(latest.close, low_20_day, high_20_day)
            ),
            high_52_week=_round_optional(high_52_week),
            high_52_week_distance_pct=_round_optional(
                ((latest.close - high_52_week) / high_52_week) * 100 if high_52_week else None
            ),
            close_above_sma_20=_above(latest.close, sma_20),
            close_above_sma_50=_above(latest.close, sma_50),
            close_above_sma_200=_above(latest.close, sma_200),
            close_above_prior_20_day_high=_above(latest.close, prior_high_20_day),
            close_above_prior_50_day_high=_above(latest.close, prior_high_50_day),
            warnings=warnings,
        )


def simple_moving_average(values: Sequence[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def exponential_moving_average(values: Sequence[float], period: int) -> float | None:
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)
    ema = simple_moving_average(values[:period], period)
    if ema is None:
        return None

    for value in values[period:]:
        ema = (value - ema) * multiplier + ema
    return ema


def rolling_high(values: Sequence[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return max(values[-period:])


def prior_rolling_high(values: Sequence[float], period: int) -> float | None:
    if len(values) <= period:
        return None
    return max(values[-(period + 1):-1])


def rolling_low(values: Sequence[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return min(values[-period:])


def average_true_range(bars: Sequence[DailyBar], period: int) -> float | None:
    if len(bars) <= period:
        return None

    ordered_bars = sorted(bars, key=lambda bar: bar.date)
    true_ranges = []
    for previous, current in zip(ordered_bars, ordered_bars[1:]):
        true_ranges.append(
            max(
                current.high - current.low,
                abs(current.high - previous.close),
                abs(current.low - previous.close),
            )
        )
    return simple_moving_average(true_ranges, period)


def _above(value: float, threshold: float | None) -> bool | None:
    return value > threshold if threshold is not None else None


def _round_optional(value: float | None) -> float | None:
    return round(value, 4) if value is not None else None


def _percent_distance(value: float, reference: float | None) -> float | None:
    if reference is None:
        return None
    return ((value - reference) / reference) * 100


def _range_position_pct(value: float, low: float | None, high: float | None) -> float | None:
    if low is None or high is None or high == low:
        return None
    return ((value - low) / (high - low)) * 100
