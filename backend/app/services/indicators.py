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
        volumes = [bar.volume for bar in ordered_bars]

        sma_20 = simple_moving_average(closes, 20)
        sma_50 = simple_moving_average(closes, 50)
        sma_200 = simple_moving_average(closes, 200)
        ema_21 = exponential_moving_average(closes, 21)
        avg_volume_20 = simple_moving_average([float(volume) for volume in volumes], 20)
        high_52_week = rolling_high(highs, 252)

        warnings = []
        for period in (20, 50, 200, 252):
            if len(ordered_bars) < period:
                warnings.append(f"Only {len(ordered_bars)} bars available; {period}-day indicator is incomplete.")

        return IndicatorSnapshot(
            symbol=symbol.upper(),
            latest_date=latest.date,
            close=round(latest.close, 4),
            volume=latest.volume,
            data_points=len(ordered_bars),
            sma_20=_round_optional(sma_20),
            sma_50=_round_optional(sma_50),
            sma_200=_round_optional(sma_200),
            ema_21=_round_optional(ema_21),
            avg_volume_20=_round_optional(avg_volume_20),
            relative_volume_20=_round_optional(latest.volume / avg_volume_20 if avg_volume_20 else None),
            high_52_week=_round_optional(high_52_week),
            high_52_week_distance_pct=_round_optional(
                ((latest.close - high_52_week) / high_52_week) * 100 if high_52_week else None
            ),
            close_above_sma_20=_above(latest.close, sma_20),
            close_above_sma_50=_above(latest.close, sma_50),
            close_above_sma_200=_above(latest.close, sma_200),
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


def _above(value: float, threshold: float | None) -> bool | None:
    return value > threshold if threshold is not None else None


def _round_optional(value: float | None) -> float | None:
    return round(value, 4) if value is not None else None
