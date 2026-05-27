from pydantic import BaseModel


class RiskRewardEstimate(BaseModel):
    entry: float
    invalidation: float
    target: float
    risk_per_share: float
    reward_per_share: float
    ratio: float
    label: str
    method: str
