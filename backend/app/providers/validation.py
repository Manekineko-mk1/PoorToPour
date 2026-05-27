from datetime import date


def is_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_valid_daily_bar_values(
    open_value: float,
    high_value: float,
    low_value: float,
    close_value: float,
    adjusted_close: float,
    volume: int,
) -> bool:
    prices_are_positive = all(
        value > 0
        for value in (open_value, high_value, low_value, close_value, adjusted_close)
    )
    if not prices_are_positive or volume < 0:
        return False

    return low_value <= high_value and low_value <= open_value <= high_value and low_value <= close_value <= high_value
