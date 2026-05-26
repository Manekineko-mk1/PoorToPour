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
