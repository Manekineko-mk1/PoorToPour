from pydantic import BaseModel, Field


class ProviderStatus(BaseModel):
    provider: str
    mode: str
    status: str
    message: str
    data_date: str


class SymbolProfile(BaseModel):
    symbol: str
    company_name: str
    sector: str
    industry: str
    exchange: str
    is_active: bool = True


class CompanyProfile(BaseModel):
    symbol: str
    company_name: str
    sector: str
    industry: str
    market_cap: int
    average_volume: int
    exchange: str


class EarningsEvent(BaseModel):
    symbol: str
    last_earnings_date: str | None = None
    next_earnings_date: str | None = None
    source: str = "mock"


class DailyBar(BaseModel):
    symbol: str
    date: str
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    adjusted_close: float = Field(gt=0)
    volume: int = Field(ge=0)


class ChartIndicatorBar(DailyBar):
    sma_20: float | None = None
    sma_50: float | None = None
    sma_200: float | None = None
    rsi_14: float | None = None


class RiskRewardOverlay(BaseModel):
    entry: float | None = None
    invalidation: float | None = None
    target: float | None = None
    risk_per_share: float | None = None
    ratio: str | None = None


class ChartCandidateContext(BaseModel):
    scan_id: str
    setup: str
    status: str
    score: int
    risk_reward: str | None = None
    reasons: list[str] = Field(default_factory=list)
    caution_flags: list[str] = Field(default_factory=list)
    risk_reward_overlay: RiskRewardOverlay | None = None


class SymbolChartPayload(BaseModel):
    symbol: str
    company_name: str | None = None
    exchange: str | None = None
    data_date: str | None = None
    bars: list[ChartIndicatorBar] = Field(default_factory=list)
    candidate: ChartCandidateContext | None = None
    warnings: list[str] = Field(default_factory=list)


class MarketDataRefreshSummary(BaseModel):
    provider: str
    period: str
    symbols_requested: int
    symbols_refreshed: int = 0
    symbols_failed: int = 0
    bars_persisted: int = 0
    failure_messages: list[str] = Field(default_factory=list)
