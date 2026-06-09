from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.config import Settings
from app.services.scheduled_scan import _seconds_until_next_run, _should_run_startup_catchup


EASTERN = ZoneInfo("America/New_York")


def test_seconds_until_next_run_uses_today_when_time_has_not_passed() -> None:
    now = datetime(2026, 6, 9, 5, 30, tzinfo=EASTERN)

    assert _seconds_until_next_run(now, "06:00", EASTERN) == 30 * 60


def test_seconds_until_next_run_rolls_to_tomorrow_after_scheduled_time() -> None:
    now = datetime(2026, 6, 9, 6, 30, tzinfo=EASTERN)

    assert _seconds_until_next_run(now, "06:00", EASTERN) == 23.5 * 60 * 60


def test_local_startup_catchup_runs_after_scheduled_time_when_no_scan_completed() -> None:
    settings = Settings(environment="local", scheduled_scan_time="06:00", _env_file=None)
    now = datetime(2026, 6, 9, 8, 0, tzinfo=EASTERN)

    assert _should_run_startup_catchup(settings, now, latest_completed_at=None) is True


def test_local_startup_catchup_skips_when_latest_scan_completed_after_schedule() -> None:
    settings = Settings(environment="local", scheduled_scan_time="06:00", _env_file=None)
    now = datetime(2026, 6, 9, 8, 0, tzinfo=EASTERN)
    latest_completed_at = datetime(2026, 6, 9, 6, 15, tzinfo=EASTERN)

    assert _should_run_startup_catchup(settings, now, latest_completed_at) is False


def test_startup_catchup_skips_before_scheduled_time() -> None:
    settings = Settings(environment="local", scheduled_scan_time="06:00", _env_file=None)
    now = datetime(2026, 6, 9, 5, 30, tzinfo=EASTERN)

    assert _should_run_startup_catchup(settings, now, latest_completed_at=None) is False


def test_startup_catchup_skips_outside_local_environments() -> None:
    settings = Settings(environment="production", scheduled_scan_time="06:00", _env_file=None)
    now = datetime(2026, 6, 9, 8, 0, tzinfo=EASTERN)

    assert _should_run_startup_catchup(settings, now, latest_completed_at=None) is False
