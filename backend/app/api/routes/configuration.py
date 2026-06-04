from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.core.security import is_local
from app.services.setup_detectors import ENABLED_SETUP_NAMES

router = APIRouter(tags=["configuration"])


@router.get("/settings/display")
def display_settings() -> dict:
    settings = get_settings()
    payload: dict = {
        "environment": settings.environment,
        "provider": settings.provider,
        "data_source_note": _data_source_note(settings.provider),
        "universe": "Persisted symbols",
        "enabled_setups": list(ENABLED_SETUP_NAMES),
        "ui_feature_notes": {
            "theme": "Dark",
            "sidebar_collapse": "Local UI state only",
            "chart_rsi_panel": "Resizable per session",
        },
        "ai_notes": {
            "trade_decisions": "Disabled",
            "summaries": "Disabled by default until post-MVP review",
        },
    }
    if is_local(settings.environment):
        payload["scanner"] = {
            "risk_reward_atr_buffer_multiplier": settings.scanner_risk_reward_atr_buffer_multiplier,
            "risk_reward_target_multiple": settings.scanner_risk_reward_target_multiple,
            "schedule": _scan_schedule(settings.allow_hosted_manual_scan),
        }
        payload["admin_controls"] = {
            "manual_scan": _manual_scan_note(settings),
        }
    return payload


def _data_source_note(provider: str) -> str:
    if provider.lower() == "mock":
        return "Mock/local provider mode for development."
    return "Configured provider mode; secrets are redacted."


def _scan_schedule(allow_hosted: bool) -> str:
    if allow_hosted:
        return "Hosted manual scan enabled."
    return "Manual/local daily scan."


def _manual_scan_note(settings: Settings) -> str:
    if settings.allow_hosted_manual_scan:
        return (
            f"Hosted scan enabled "
            f"(rate limit: {settings.manual_scan_rate_limit} req/min, "
            f"max {settings.hosted_manual_scan_max_symbols} symbols)."
        )
    return "Local/dev only until hosted rate limits are reviewed."
