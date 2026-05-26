from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.providers.mock_provider import MockProvider
from app.repositories import scans

router = APIRouter(tags=["scans"])
provider = MockProvider()


@router.get("/scans/latest")
def latest_scan(db: Session = Depends(get_db)) -> dict:
    scan = scans.get_latest_scan(db)
    if scan is not None:
        return scan.model_dump()
    return provider.get_latest_scan()


@router.get("/scans")
def list_scan_runs(db: Session = Depends(get_db), limit: int = 20) -> list[dict]:
    return [scan.model_dump() for scan in scans.list_scan_runs(db, limit=limit)]


@router.get("/scans/{scan_id}")
def get_scan(scan_id: str, db: Session = Depends(get_db)) -> dict:
    scan = scans.get_scan(db, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail=f"No persisted scan found for {scan_id}")
    return scan.model_dump()
