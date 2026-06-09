import asyncio
import logging
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.orm import Session

from app.api.routes.scans import run_scheduled_scan
from app.core.config import Settings
from app.core.security import is_local
from app.db.base import SessionLocal
from app.repositories import scans

logger = logging.getLogger(__name__)


SessionFactory = Callable[[], Session]


class ScheduledScanService:
    """Small in-process daily scanner for local/dev and single-instance demos."""

    def __init__(
        self,
        settings: Settings,
        session_factory: SessionFactory = SessionLocal,
    ) -> None:
        self.settings = settings
        self.session_factory = session_factory
        self._task: asyncio.Task | None = None
        self._scan_lock = asyncio.Lock()

    def start(self) -> None:
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._run_loop(), name="scheduled-scan-service")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def _run_loop(self) -> None:
        timezone = _scan_timezone(self.settings.scheduled_scan_timezone)
        logger.info(
            "Scheduled scan service started: enabled=%s time=%s timezone=%s",
            self.settings.scheduled_scan_enabled,
            self.settings.scheduled_scan_time,
            timezone.key,
        )

        if _should_run_startup_catchup(self.settings, datetime.now(timezone), self._latest_scan_completed_at(timezone)):
            await self._run_once("startup catch-up")

        while True:
            now = datetime.now(timezone)
            wait_seconds = _seconds_until_next_run(
                now,
                self.settings.scheduled_scan_time,
                timezone,
            )
            await asyncio.sleep(wait_seconds)
            await self._run_once("daily schedule")

    async def _run_once(self, reason: str) -> None:
        if self._scan_lock.locked():
            logger.info("Scheduled scan skipped because another scheduled scan is already running.")
            return

        async with self._scan_lock:
            logger.info("Starting scheduled scan (%s).", reason)
            try:
                payload = await asyncio.to_thread(self._run_once_sync)
            except Exception:
                logger.exception("Scheduled scan failed.")
                return
            logger.info(
                "Scheduled scan completed: scan_id=%s candidates=%s",
                payload.get("scan_id"),
                payload.get("candidates_found"),
            )

    def _run_once_sync(self) -> dict:
        db = self.session_factory()
        try:
            return run_scheduled_scan(db, self.settings)
        finally:
            db.close()

    def _latest_scan_completed_at(self, timezone: ZoneInfo) -> datetime | None:
        db = self.session_factory()
        try:
            latest = scans.get_latest_scan(db)
        finally:
            db.close()
        if latest is None or latest.completed_at is None:
            return None
        return _parse_completed_at(latest.completed_at, timezone)


def _should_run_startup_catchup(
    settings: Settings,
    now: datetime,
    latest_completed_at: datetime | None,
) -> bool:
    if not settings.scheduled_scan_startup_catchup:
        return False
    if not is_local(settings.environment):
        return False

    scheduled_at = _scheduled_datetime(now, settings.scheduled_scan_time, now.tzinfo)
    if now < scheduled_at:
        return False
    if latest_completed_at is None:
        return True
    return latest_completed_at < scheduled_at


def _seconds_until_next_run(now: datetime, scheduled_time: str, timezone: ZoneInfo) -> float:
    scheduled_at = _scheduled_datetime(now, scheduled_time, timezone)
    if now >= scheduled_at:
        scheduled_at += timedelta(days=1)
    return max((scheduled_at - now).total_seconds(), 0)


def _scheduled_datetime(now: datetime, scheduled_time: str, timezone) -> datetime:
    hour, minute = (int(part) for part in scheduled_time.split(":"))
    local_now = now.astimezone(timezone)
    return datetime.combine(local_now.date(), time(hour=hour, minute=minute), tzinfo=timezone)


def _scan_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        logger.warning("Unknown scheduled scan timezone %r; falling back to UTC.", name)
        return ZoneInfo("UTC")


def _parse_completed_at(value: str, timezone: ZoneInfo) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(timezone)
