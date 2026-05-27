from app.models.risk import RiskRewardEstimate
from app.services.status_rules import CandidateStatusInput, determine_candidate_status


def test_status_rules_block_missing_required_inputs() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=95,
            setup_confirmed=True,
            risk_reward=_risk_reward(),
            missing_required_fields=["atr_14"],
        )
    )

    assert status == "Blocked"


def test_status_rules_block_stale_price_data() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=95,
            setup_confirmed=True,
            risk_reward=_risk_reward(),
            price_data_fresh=False,
        )
    )

    assert status == "Blocked"


def test_status_rules_allow_actionable_only_with_clean_confirmed_high_score_and_risk_reward() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=95,
            setup_confirmed=True,
            risk_reward=_risk_reward(),
            caution_flags=[],
        )
    )

    assert status == "Actionable"


def test_status_rules_keep_confirmed_candidate_on_watch_when_caution_exists() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=90,
            setup_confirmed=True,
            risk_reward=_risk_reward(),
            caution_flags=["Close is extended above the 20-day moving average."],
        )
    )

    assert status == "Watch"


def test_status_rules_keep_unconfirmed_candidate_on_watch_when_score_is_sufficient() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=40,
            setup_confirmed=False,
            risk_reward=_risk_reward(),
            caution_flags=["Breakout not confirmed yet."],
        )
    )

    assert status == "Watch"


def test_status_rules_keep_detected_setup_on_watch_when_score_is_low_but_not_weak() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=15,
            setup_confirmed=False,
            setup_detected=True,
            risk_reward=_risk_reward(),
            caution_flags=["Breakout not confirmed yet."],
        )
    )

    assert status == "Watch"


def test_status_rules_avoid_weak_unconfirmed_candidate() -> None:
    status = determine_candidate_status(
        CandidateStatusInput(
            score=25,
            setup_confirmed=False,
            risk_reward=None,
            caution_flags=[],
        )
    )

    assert status == "Avoid"


def _risk_reward(ratio: float = 2.0) -> RiskRewardEstimate:
    return RiskRewardEstimate(
        entry=125.0,
        invalidation=97.0,
        target=181.0,
        risk_per_share=28.0,
        reward_per_share=56.0,
        ratio=ratio,
        label=f"{ratio:.1f}:1",
        method="unit",
    )
