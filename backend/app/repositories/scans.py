from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session, selectinload

from app.db.models import ScanCandidateRow, ScanRunRow
from app.models.scans import ScanCandidate, ScanRun


def get_latest_scan(db: Session) -> ScanRun | None:
    row = db.scalars(
        select(ScanRunRow)
        .options(selectinload(ScanRunRow.candidates))
        .order_by(ScanRunRow.completed_at.desc().nullslast(), ScanRunRow.created_at.desc())
        .limit(1)
    ).first()
    return _scan_run_from_row(row) if row else None


def get_scan(db: Session, scan_id: str) -> ScanRun | None:
    row = db.scalars(
        select(ScanRunRow)
        .where(ScanRunRow.id == scan_id)
        .options(selectinload(ScanRunRow.candidates))
    ).first()
    return _scan_run_from_row(row) if row else None


def list_scan_runs(db: Session, limit: int = 20) -> list[ScanRun]:
    rows = db.scalars(
        select(ScanRunRow)
        .options(selectinload(ScanRunRow.candidates))
        .order_by(ScanRunRow.completed_at.desc().nullslast(), ScanRunRow.created_at.desc())
        .limit(limit)
    ).all()
    return [_scan_run_from_row(row) for row in rows]


def upsert_scan_run(db: Session, scan: ScanRun) -> None:
    values = {
        "id": scan.scan_id,
        "scan_type": scan.scan_type,
        "universe": scan.universe,
        "status": scan.status,
        "provider": scan.provider,
        "data_date": _parse_date(scan.data_date),
        "started_at": _parse_datetime(scan.started_at),
        "completed_at": _parse_datetime(scan.completed_at),
        "symbols_processed": scan.symbols_processed,
        "candidates_found": scan.candidates_found,
        "warning": scan.warning,
    }
    statement = pg_insert(ScanRunRow).values(**values)
    statement = statement.on_conflict_do_update(
        index_elements=[ScanRunRow.id],
        set_={
            "scan_type": statement.excluded.scan_type,
            "universe": statement.excluded.universe,
            "status": statement.excluded.status,
            "provider": statement.excluded.provider,
            "data_date": statement.excluded.data_date,
            "started_at": statement.excluded.started_at,
            "completed_at": statement.excluded.completed_at,
            "symbols_processed": statement.excluded.symbols_processed,
            "candidates_found": statement.excluded.candidates_found,
            "warning": statement.excluded.warning,
        },
    )
    db.execute(statement)

    db.execute(delete(ScanCandidateRow).where(ScanCandidateRow.scan_run_id == scan.scan_id))
    for candidate in scan.candidates:
        db.add(_candidate_row(scan.scan_id, candidate))


def scan_run_from_payload(payload: dict[str, Any]) -> ScanRun:
    return ScanRun(
        scan_id=payload["scan_id"],
        scan_type=payload["scan_type"],
        universe=payload["universe"],
        status=payload["status"],
        provider=payload["provider"],
        data_date=payload.get("data_date"),
        started_at=payload.get("started_at"),
        completed_at=payload.get("completed_at"),
        symbols_processed=payload.get("symbols_processed", 0),
        candidates_found=payload.get("candidates_found", len(payload.get("candidates", []))),
        warning=payload.get("warning"),
        candidates=[ScanCandidate(**candidate) for candidate in payload.get("candidates", [])],
    )


def _candidate_row(scan_id: str, candidate: ScanCandidate) -> ScanCandidateRow:
    return ScanCandidateRow(
        scan_run_id=scan_id,
        symbol=candidate.symbol.upper(),
        rank=candidate.rank,
        company_name=candidate.company_name,
        setup=candidate.setup,
        status=candidate.status,
        score=candidate.score,
        price=candidate.price,
        relative_volume=candidate.relative_volume,
        rsi=candidate.rsi,
        risk_reward=candidate.risk_reward,
        indicator_snapshot=candidate.indicator_snapshot,
        score_breakdown=candidate.score_breakdown,
        reasons=candidate.reasons,
        caution_flags=candidate.caution_flags,
        last_updated=_parse_datetime(candidate.last_updated),
    )


def _scan_run_from_row(row: ScanRunRow) -> ScanRun:
    return ScanRun(
        scan_id=row.id,
        scan_type=row.scan_type,
        universe=row.universe,
        status=row.status,
        provider=row.provider,
        data_date=row.data_date.isoformat() if row.data_date else None,
        started_at=_format_datetime(row.started_at),
        completed_at=_format_datetime(row.completed_at),
        symbols_processed=row.symbols_processed,
        candidates_found=row.candidates_found,
        warning=row.warning,
        candidates=[_candidate_from_row(candidate) for candidate in row.candidates],
    )


def _candidate_from_row(row: ScanCandidateRow) -> ScanCandidate:
    return ScanCandidate(
        rank=row.rank,
        symbol=row.symbol,
        company_name=row.company_name,
        setup=row.setup,
        status=row.status,
        score=row.score,
        price=_to_float(row.price),
        relative_volume=_to_float(row.relative_volume),
        rsi=_to_float(row.rsi),
        risk_reward=row.risk_reward,
        indicator_snapshot=row.indicator_snapshot,
        score_breakdown=row.score_breakdown,
        reasons=row.reasons or [],
        caution_flags=row.caution_flags or [],
        last_updated=_format_datetime(row.last_updated),
    )


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _format_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat().replace("+00:00", "Z")


def _to_float(value: Decimal | None) -> float | None:
    return float(value) if value is not None else None
