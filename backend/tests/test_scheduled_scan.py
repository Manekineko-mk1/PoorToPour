import asyncio
import contextlib
import logging
import threading
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.config import Settings
from app.services import scheduled_scan
from app.services.scheduled_scan import SCHEDULED_SCAN_ADVISORY_LOCK_KEY, ScheduledScanService
from app.services.scheduled_scan import _seconds_until_next_run, _should_run_startup_catchup


EASTERN = ZoneInfo("America/New_York")


class FakeScalarResult:
    def __init__(self, value: bool) -> None:
        self.value = value

    def scalar_one(self) -> bool:
        return self.value


class FakeLockSession:
    def __init__(self, *, lock_acquired: bool) -> None:
        self.lock_acquired = lock_acquired
        self.executed: list[tuple[str, dict]] = []
        self.closed = False

    def execute(self, statement, params) -> FakeScalarResult:
        sql = str(statement)
        self.executed.append((sql, params))
        if "pg_try_advisory_lock" in sql:
            return FakeScalarResult(self.lock_acquired)
        if "pg_advisory_unlock" in sql:
            return FakeScalarResult(True)
        raise AssertionError(f"Unexpected SQL: {sql}")

    def close(self) -> None:
        self.closed = True


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


def test_run_once_sync_skips_when_advisory_lock_is_unavailable(monkeypatch) -> None:
    session = FakeLockSession(lock_acquired=False)
    service = ScheduledScanService(Settings(_env_file=None), session_factory=lambda: session)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("run_scheduled_scan should not run without the advisory lock")

    monkeypatch.setattr(scheduled_scan, "run_scheduled_scan", fail_if_called)

    payload = service._run_once_sync()

    assert payload == {"scan_id": None, "candidates_found": None, "skipped": True}
    assert session.closed is True
    assert len(session.executed) == 1
    sql, params = session.executed[0]
    assert "pg_try_advisory_lock" in sql
    assert params == {"lock_key": SCHEDULED_SCAN_ADVISORY_LOCK_KEY}


def test_run_once_sync_releases_advisory_lock_after_scan(monkeypatch) -> None:
    session = FakeLockSession(lock_acquired=True)
    service = ScheduledScanService(Settings(_env_file=None), session_factory=lambda: session)

    def fake_run_scheduled_scan(db, settings):
        assert db is session
        assert settings is service.settings
        return {"scan_id": "scan-1", "candidates_found": 2}

    monkeypatch.setattr(scheduled_scan, "run_scheduled_scan", fake_run_scheduled_scan)

    payload = service._run_once_sync()

    assert payload == {"scan_id": "scan-1", "candidates_found": 2}
    assert session.closed is True
    assert [params for _, params in session.executed] == [
        {"lock_key": SCHEDULED_SCAN_ADVISORY_LOCK_KEY},
        {"lock_key": SCHEDULED_SCAN_ADVISORY_LOCK_KEY},
    ]
    assert "pg_try_advisory_lock" in session.executed[0][0]
    assert "pg_advisory_unlock" in session.executed[1][0]


def test_stop_waits_for_inflight_scan_thread(monkeypatch) -> None:
    async def run_test() -> None:
        service = ScheduledScanService(Settings(_env_file=None))
        started = threading.Event()
        release = threading.Event()
        completed = threading.Event()

        def run_once_sync() -> dict:
            started.set()
            release.wait(timeout=2)
            completed.set()
            return {"scan_id": "scan-1", "candidates_found": 0}

        monkeypatch.setattr(service, "_run_once_sync", run_once_sync)

        run_task = asyncio.create_task(service._run_once("test"))
        assert await asyncio.to_thread(started.wait, 2)

        service._task = asyncio.create_task(asyncio.sleep(60))
        stop_task = asyncio.create_task(service.stop())
        await asyncio.sleep(0.05)

        assert not stop_task.done()

        release.set()
        await asyncio.wait_for(stop_task, timeout=2)
        await asyncio.wait_for(run_task, timeout=2)

        assert completed.is_set()
        assert service._inflight is None

    asyncio.run(run_test())


def test_stop_logs_warning_when_inflight_scan_exceeds_timeout(
    monkeypatch,
    caplog,
) -> None:
    async def run_test() -> None:
        service = ScheduledScanService(Settings(_env_file=None))
        service._task = asyncio.create_task(asyncio.sleep(60))
        service._inflight = asyncio.create_task(asyncio.sleep(60))
        monkeypatch.setattr(scheduled_scan, "SHUTDOWN_SCAN_WAIT_SECONDS", 0.01)

        with caplog.at_level(logging.WARNING, logger="app.services.scheduled_scan"):
            await service.stop()

        assert "Scheduled scan is still running after" in caplog.text
        assert service._inflight is not None
        assert not service._inflight.done()

        service._inflight.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await service._inflight

    asyncio.run(run_test())
