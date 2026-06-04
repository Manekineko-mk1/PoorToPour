from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["configuration"])


@router.get("/settings/display")
def display_settings() -> dict:
    settings = get_settings()
    return {
        "environment": settings.environment,
        "provider": settings.provider,
        "data_source_note": _data_source_note(settings.provider),
        "universe": "Persisted symbols",
        "enabled_setups": [
            "Breakout",
            "Pullback Continuation",
            "Relative Strength Leader",
        ],
        "scanner": {
            "risk_reward_atr_buffer_multiplier": settings.scanner_risk_reward_atr_buffer_multiplier,
            "risk_reward_target_multiple": settings.scanner_risk_reward_target_multiple,
            "schedule": "Manual/local daily scan",
        },
        "safe_user_preferences": {
            "theme": "Dark",
            "sidebar_collapse": "Local UI state only",
            "chart_rsi_panel": "Resizable per session",
        },
        "admin_controls": {
            "system_options": "Read-only in MVP",
            "manual_scan": "Local/dev only until hosted rate limits are reviewed",
        },
        "ai": {
            "trade_decisions": "Disabled",
            "summaries": "Disabled by default until post-MVP review",
        },
        "secrets": {
            "api_keys_visible": False,
            "database_urls_visible": False,
        },
    }


def _data_source_note(provider: str) -> str:
    if provider.lower() == "mock":
        return "Mock/local provider mode for development."
    return "Configured provider mode; secrets are redacted."
