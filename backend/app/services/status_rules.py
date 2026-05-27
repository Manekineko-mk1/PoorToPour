from dataclasses import dataclass, field

from app.models.risk import RiskRewardEstimate


BLOCKED = "Blocked"
AVOID = "Avoid"
WATCH = "Watch"
ACTIONABLE = "Actionable"


@dataclass(frozen=True)
class CandidateStatusInput:
    score: int
    setup_confirmed: bool
    setup_detected: bool = False
    risk_reward: RiskRewardEstimate | None = None
    caution_flags: list[str] = field(default_factory=list)
    missing_required_fields: list[str] = field(default_factory=list)
    price_data_fresh: bool = True


def determine_candidate_status(status_input: CandidateStatusInput) -> str:
    if _has_blocking_data_issue(status_input):
        return BLOCKED

    if _is_actionable(status_input):
        return ACTIONABLE

    if status_input.setup_confirmed or status_input.score >= 40:
        return WATCH

    if status_input.setup_detected:
        return WATCH

    return AVOID


def _has_blocking_data_issue(status_input: CandidateStatusInput) -> bool:
    if status_input.missing_required_fields:
        return True
    if not status_input.price_data_fresh:
        return True
    return any(_is_blocking_caution(flag) for flag in status_input.caution_flags)


def _is_blocking_caution(flag: str) -> bool:
    normalized = flag.casefold()
    return (
        normalized.startswith("missing required")
        or normalized.startswith("at least ")
        or "price data is stale" in normalized
    )


def _is_actionable(status_input: CandidateStatusInput) -> bool:
    if not status_input.setup_confirmed:
        return False
    if status_input.score < 80:
        return False
    if status_input.caution_flags:
        return False
    if status_input.risk_reward is None:
        return False
    return status_input.risk_reward.ratio >= 2
