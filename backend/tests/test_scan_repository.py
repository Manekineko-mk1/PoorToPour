from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session

from app.db.base import Base, engine
from app.db.models import ScanCandidateRow, ScanRunRow, SymbolProfileRow
from app.repositories.scans import get_latest_candidate_for_symbol, scan_run_from_payload


@pytest.fixture
def db_session():
    # Ensure the schema exists (idempotent; no-op when migrations already ran),
    # then run the test inside a transaction that is rolled back so inserted
    # rows never leak into the shared container database.
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def _symbol(session: Session, symbol: str) -> None:
    session.add(
        SymbolProfileRow(
            symbol=symbol,
            company_name=f"{symbol} Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            exchange="NASDAQ",
        )
    )


def _scan_run(session: Session, scan_id: str, *, completed_at: datetime | None) -> None:
    session.add(
        ScanRunRow(
            id=scan_id,
            scan_type="technical",
            universe="Test Universe",
            status="completed",
            provider="TechnicalScanner",
            completed_at=completed_at,
        )
    )


def _candidate(session: Session, scan_id: str, symbol: str, *, rank: int, setup: str) -> None:
    session.add(
        ScanCandidateRow(
            scan_run_id=scan_id,
            symbol=symbol,
            rank=rank,
            company_name=f"{symbol} Inc.",
            setup=setup,
            status="Watch",
            score=50,
        )
    )


def test_get_latest_candidate_with_scan_id_returns_lowest_rank_regardless_of_insert_order(
    db_session: Session,
) -> None:
    _symbol(db_session, "QATEST")
    _scan_run(db_session, "scan-det", completed_at=datetime(2026, 5, 22, tzinfo=timezone.utc))
    # Insert out of rank order to prove ordering is driven by rank, not insertion.
    _candidate(db_session, "scan-det", "QATEST", rank=3, setup="Pullback Continuation")
    _candidate(db_session, "scan-det", "QATEST", rank=1, setup="Momentum Breakout")
    _candidate(db_session, "scan-det", "QATEST", rank=2, setup="Relative Strength Leader")
    db_session.flush()

    result = get_latest_candidate_for_symbol(db_session, "QATEST", scan_id="scan-det")

    assert result is not None
    scan, candidate = result
    assert scan.scan_id == "scan-det"
    assert candidate.rank == 1
    assert candidate.setup == "Momentum Breakout"


def test_get_latest_candidate_with_scan_id_and_setup_selects_that_setup(
    db_session: Session,
) -> None:
    _symbol(db_session, "QATEST")
    _scan_run(db_session, "scan-det", completed_at=datetime(2026, 5, 22, tzinfo=timezone.utc))
    _candidate(db_session, "scan-det", "QATEST", rank=1, setup="Momentum Breakout")
    _candidate(db_session, "scan-det", "QATEST", rank=2, setup="Pullback Continuation")
    db_session.flush()

    result = get_latest_candidate_for_symbol(
        db_session, "QATEST", setup="Pullback Continuation", scan_id="scan-det"
    )

    assert result is not None
    _, candidate = result
    assert candidate.setup == "Pullback Continuation"
    assert candidate.rank == 2


def test_get_latest_candidate_without_scan_id_prefers_most_recent_run(
    db_session: Session,
) -> None:
    _symbol(db_session, "QATEST")
    _scan_run(db_session, "scan-old", completed_at=datetime(2026, 5, 20, tzinfo=timezone.utc))
    _scan_run(db_session, "scan-new", completed_at=datetime(2026, 5, 22, tzinfo=timezone.utc))
    _candidate(db_session, "scan-old", "QATEST", rank=1, setup="Momentum Breakout")
    _candidate(db_session, "scan-new", "QATEST", rank=1, setup="Momentum Breakout")
    db_session.flush()

    result = get_latest_candidate_for_symbol(db_session, "QATEST")

    assert result is not None
    scan, _ = result
    assert scan.scan_id == "scan-new"


def test_scan_run_from_payload_preserves_fixture_shape() -> None:
    payload = {
        "scan_id": "scan_1",
        "scan_type": "Daily Momentum",
        "universe": "S&P 500",
        "status": "completed",
        "provider": "Mock Provider",
        "data_date": "2026-05-22",
        "symbols_processed": 3,
        "candidates_found": 1,
        "warning": "Fixture",
        "candidates": [
            {
                "rank": 1,
                "symbol": "AAPL",
                "company_name": "Apple Inc.",
                "setup": "Momentum Breakout",
                "status": "Actionable",
                "score": 86,
                "price": 308.82,
                "relative_volume": 1.25,
                "rsi": 61.3,
                "risk_reward": "3.2:1",
                "caution_flags": ["Earnings Soon"],
                "last_updated": "2026-05-22T21:08:13Z",
            }
        ],
    }

    scan = scan_run_from_payload(payload)

    assert scan.scan_id == "scan_1"
    assert scan.candidates_found == 1
    assert scan.candidates[0].symbol == "AAPL"
    assert scan.candidates[0].caution_flags == ["Earnings Soon"]
