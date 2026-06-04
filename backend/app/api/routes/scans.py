from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import check_manual_scan_rate_limit, is_local, verify_manual_scan_auth
from app.db.base import get_db
from app.models.market_data import MarketDataRefreshSummary
from app.repositories import market_data
from app.repositories import scans
from app.services.market_data_refresh import refresh_yfinance_daily_bars
from app.services.scanner import TechnicalScanner

router = APIRouter(tags=["scans"])


@router.get("/scans/latest")
def latest_scan(db: Session = Depends(get_db)) -> dict:
    scan = scans.get_latest_scan(db)
    if scan is None:
        raise HTTPException(status_code=404, detail="No scan results found")
    return scan.model_dump(mode="json")


@router.get("/scans")
def list_scan_runs(db: Session = Depends(get_db), limit: int = 20) -> list[dict]:
    return [scan.model_dump(mode="json") for scan in scans.list_scan_runs(db, limit=limit)]


@router.get("/scans/{scan_id}")
def get_scan(scan_id: str, db: Session = Depends(get_db)) -> dict:
    scan = scans.get_scan(db, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail=f"No persisted scan found for {scan_id}")
    return scan.model_dump(mode="json")


RefreshPeriod = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


@router.post(
    "/scans/manual",
    dependencies=[Depends(verify_manual_scan_auth), Depends(check_manual_scan_rate_limit)],
)
def run_manual_scan(
    db: Session = Depends(get_db),
    refresh_market_data: bool = True,
    refresh_period: RefreshPeriod = "1y",
    refresh_limit: int | None = Query(default=None, ge=1),
    min_refresh_ratio: float | None = Query(default=None, ge=0, le=1),
) -> dict:
    settings = get_settings()
    symbols = market_data.list_symbols(db)
    if not symbols:
        raise HTTPException(status_code=400, detail="No persisted symbols are available for scanning")

    refresh_limit = _validated_refresh_limit(
        settings.environment,
        settings.allow_hosted_manual_scan,
        settings.hosted_manual_scan_max_symbols,
        refresh_limit,
    )
    run_symbols = symbols[:refresh_limit] if refresh_limit is not None else symbols

    refresh_summary = None
    if refresh_market_data:
        refresh_summary = refresh_yfinance_daily_bars(db, run_symbols, period=refresh_period)
        required_ratio = (
            min_refresh_ratio if min_refresh_ratio is not None else settings.manual_scan_min_refresh_ratio
        )
        _enforce_refresh_threshold(db, refresh_summary, required_ratio)

    try:
        if refresh_summary is not None:
            db.flush()
        bars_by_symbol = {symbol.symbol: market_data.get_daily_bars(db, symbol.symbol) for symbol in run_symbols}
        scan = TechnicalScanner().scan(
            symbols=run_symbols,
            bars_by_symbol=bars_by_symbol,
            provider=_manual_scan_provider(refresh_market_data),
            universe=_manual_scan_universe(refresh_limit),
        )
        if refresh_summary is not None:
            scan.warning = _manual_scan_warning(refresh_summary)
        scans.upsert_scan_run(db, scan)
        db.commit()
    except Exception:
        db.rollback()
        raise

    payload = scan.model_dump(mode="json")
    if refresh_summary is not None:
        payload["market_data_refresh"] = refresh_summary.model_dump(mode="json")
    return payload


def _enforce_refresh_threshold(
    db: Session,
    refresh_summary: MarketDataRefreshSummary,
    required_ratio: float,
) -> None:
    """Abort the scan when the refresh fell below the required success ratio.

    ``required_ratio`` of 0.0 keeps the lenient default: only a total refresh
    failure (no symbols refreshed) blocks the scan. A higher ratio enforces
    stricter handling of partial refreshes, rolling back the persisted bars so
    the scanner never runs on a known-incomplete data set.
    """
    if refresh_summary.symbols_requested == 0:
        return

    if refresh_summary.symbols_refreshed == 0:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Market data refresh failed; scanner did not run.",
        )

    success_ratio = refresh_summary.symbols_refreshed / refresh_summary.symbols_requested
    if success_ratio < required_ratio:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail=(
                "Market data refresh below required threshold; scanner did not run. "
                f"Refreshed {refresh_summary.symbols_refreshed} of "
                f"{refresh_summary.symbols_requested} symbols ({success_ratio:.0%}); "
                f"required at least {required_ratio:.0%}."
            ),
        )


def _manual_scan_provider(refresh_market_data: bool) -> str:
    if refresh_market_data:
        return "TechnicalScanner + yfinance refreshed bars"
    return "TechnicalScanner + persisted bars"


def _manual_scan_universe(refresh_limit: int | None) -> str:
    if refresh_limit is not None:
        return f"Persisted symbols limited to {refresh_limit}"
    return "Persisted symbols"


def _validated_refresh_limit(
    environment: str,
    allow_hosted_manual_scan: bool,
    hosted_manual_scan_max_symbols: int,
    refresh_limit: int | None,
) -> int | None:
    if is_local(environment):
        return refresh_limit

    if not allow_hosted_manual_scan:
        raise HTTPException(
            status_code=403,
            detail="Manual scan is disabled outside local/dev environments.",
        )

    if refresh_limit is None:
        return hosted_manual_scan_max_symbols

    return min(refresh_limit, hosted_manual_scan_max_symbols)


def _manual_scan_warning(refresh_summary: MarketDataRefreshSummary) -> str:
    if refresh_summary.symbols_failed == 0:
        return "Research-only deterministic scanner output. Not a trading recommendation."

    return (
        "Market data refresh partial: "
        f"refreshed {refresh_summary.symbols_refreshed} of {refresh_summary.symbols_requested} symbols; "
        f"{refresh_summary.symbols_failed} failed. Scanner used the latest persisted bars after refresh."
    )
