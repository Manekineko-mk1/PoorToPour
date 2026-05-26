from pydantic import BaseModel, Field


class IndicatorSnapshot(BaseModel):
    symbol: str
    latest_date: str
    close: float
    volume: int
    data_points: int
    sma_20: float | None = None
    sma_50: float | None = None
    sma_200: float | None = None
    ema_21: float | None = None
    avg_volume_20: float | None = None
    relative_volume_20: float | None = None
    high_52_week: float | None = None
    high_52_week_distance_pct: float | None = None
    close_above_sma_20: bool | None = None
    close_above_sma_50: bool | None = None
    close_above_sma_200: bool | None = None
    warnings: list[str] = Field(default_factory=list)
