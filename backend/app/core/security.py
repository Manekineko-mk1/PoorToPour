from collections import deque
from threading import Lock
from time import time

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

_LOCAL_ENVIRONMENTS = {"local", "dev", "development", "test"}
_api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def _is_local(environment: str) -> bool:
    return environment.strip().lower() in _LOCAL_ENVIRONMENTS


def verify_manual_scan_auth(api_key: str | None = Depends(_api_key_scheme)) -> None:
    settings = get_settings()
    if _is_local(settings.environment):
        return
    configured_key = settings.manual_scan_api_key
    if not configured_key:
        return
    if api_key != configured_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


class _SlidingWindowRateLimiter:
    def __init__(self) -> None:
        self._calls: deque[float] = deque()
        self._lock = Lock()

    def check(self, max_calls: int, window_seconds: int = 60) -> bool:
        now = time()
        cutoff = now - window_seconds
        with self._lock:
            while self._calls and self._calls[0] < cutoff:
                self._calls.popleft()
            if len(self._calls) >= max_calls:
                return False
            self._calls.append(now)
            return True

    def reset(self) -> None:
        with self._lock:
            self._calls.clear()


manual_scan_limiter = _SlidingWindowRateLimiter()


def check_manual_scan_rate_limit() -> None:
    settings = get_settings()
    if _is_local(settings.environment):
        return
    if not manual_scan_limiter.check(settings.manual_scan_rate_limit):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.manual_scan_rate_limit} requests per minute.",
        )
