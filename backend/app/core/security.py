from collections import deque
from threading import Lock
from time import time

from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

_LOCAL_ENVIRONMENTS = {"local", "dev", "development", "test"}
_api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def is_local(environment: str) -> bool:
    return environment.strip().lower() in _LOCAL_ENVIRONMENTS


def verify_manual_scan_auth(api_key: str | None = Depends(_api_key_scheme)) -> None:
    settings = get_settings()
    if is_local(settings.environment):
        return
    configured_key = settings.manual_scan_api_key
    if not configured_key or api_key != configured_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


class _PerClientRateLimiter:
    """Sliding-window rate limiter keyed by client identity (API key or remote IP).

    Each distinct client gets its own call bucket so one heavy caller cannot
    exhaust the limit for everyone else.  For multi-instance deployments this
    should be replaced with a Redis-backed implementation (e.g. redis-py +
    EVALSHA Lua script) so all nodes share a single counter per client key.
    """

    def __init__(self) -> None:
        self._clients: dict[str, deque[float]] = {}
        self._lock = Lock()

    # Sweep the client dict when it reaches this many entries.
    _MAX_CLIENTS = 10_000

    def check(self, client_key: str, max_calls: int, window_seconds: int = 60) -> bool:
        now = time()
        cutoff = now - window_seconds
        with self._lock:
            calls = self._clients.get(client_key)
            if calls is None:
                if len(self._clients) >= self._MAX_CLIENTS:
                    self._sweep(cutoff)
                calls = deque()
                self._clients[client_key] = calls
            else:
                while calls and calls[0] < cutoff:
                    calls.popleft()
            if len(calls) >= max_calls:
                return False
            calls.append(now)
            return True

    def _sweep(self, cutoff: float) -> None:
        # Remove entries whose entire window has expired (newest call is stale).
        stale = [k for k, v in self._clients.items() if not v or v[-1] < cutoff]
        for k in stale:
            del self._clients[k]

    def reset(self) -> None:
        with self._lock:
            self._clients.clear()


manual_scan_limiter = _PerClientRateLimiter()


def _client_key(request: Request, api_key: str | None) -> str:
    if api_key:
        return f"key:{api_key}"
    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


def check_manual_scan_rate_limit(
    request: Request,
    api_key: str | None = Depends(_api_key_scheme),
) -> None:
    settings = get_settings()
    if is_local(settings.environment):
        return
    key = _client_key(request, api_key)
    if not manual_scan_limiter.check(key, settings.manual_scan_rate_limit):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.manual_scan_rate_limit} requests per minute.",
        )
