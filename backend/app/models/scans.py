from pydantic import BaseModel, Field


class ScanCandidate(BaseModel):
    rank: int
    symbol: str
    company_name: str
    setup: str
    status: str
    score: int
    price: float | None = None
    relative_volume: float | None = None
    rsi: float | None = None
    risk_reward: str | None = None
    indicator_snapshot: dict | None = None
    score_breakdown: dict | None = None
    reasons: list[str] = Field(default_factory=list)
    caution_flags: list[str] = Field(default_factory=list)
    last_updated: str | None = None


class ScanRun(BaseModel):
    scan_id: str
    scan_type: str
    universe: str
    status: str
    provider: str
    data_date: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    symbols_processed: int = 0
    candidates_found: int = 0
    warning: str | None = None
    candidates: list[ScanCandidate] = Field(default_factory=list)
