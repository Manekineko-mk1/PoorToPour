# PR Draft: Phase 1 Data Foundation Baseline

## Summary

This PR delivers the full Phase 1 baseline for PoorToPour:

- local Docker Compose development stack;
- FastAPI backend and React/Vite frontend shell;
- PostgreSQL persistence with Alembic migrations;
- deterministic mock provider seed path;
- versioned S&P 500 universe seed;
- yfinance bootstrap OHLCV ingestion path;
- deterministic `IndicatorService`;
- scan-run and candidate persistence;
- first generated bootstrap trend/momentum scanner;
- Phase 1 code/security/trading-safety review documentation.

Phase 1 is local-first and remains inside MVP scope:

- long-only;
- daily/weekly swing research flow;
- deterministic explainable scanner logic;
- no broker automation;
- no AI-generated trade decisions.

## Branch

- `feature/phase_1_data_foundation`

## Scope of Change

### Backend

- Added baseline API routes:
  - `/api/health`
  - `/api/provider/status`
  - `/api/symbols`
  - `/api/symbols/{symbol}/bars`
  - `/api/symbols/{symbol}/indicators`
  - `/api/profiles/{symbol}`
  - `/api/earnings/{symbol}`
  - `/api/scans/latest`
  - `/api/scans`
  - `/api/scans/{scan_id}`
- Added Alembic migrations for:
  - market data tables;
  - scan persistence tables.
- Added idempotent seed scripts:
  - mock market data and mock scan output;
  - S&P 500 universe seed import.
- Added yfinance bootstrap provider and ingestion script.
- Added `IndicatorService` with deterministic snapshot outputs.
- Added first bootstrap generated scanner (`MomentumScanner`) and persistence runner.

### Frontend

- Added React/Vite dashboard shell consuming `/api/scans/latest`.
- Added resilience for nullable generated scanner fields.
- Added candidate reasons rendering in selected candidate panel.

### Infrastructure / Ops

- Added Docker services:
  - `backend`
  - `frontend`
  - `db` (PostgreSQL)
  - `adminer` (local DB inspection)
- Bound service ports to localhost for local security:
  - `127.0.0.1:5173`
  - `127.0.0.1:8000`
  - `127.0.0.1:5432`
  - `127.0.0.1:8080`

### Documentation

- Updated tracker and decision log for Phase 1 completion status.
- Added dedicated review document:
  - `/docs/phases/phase-1-data-foundation/phase-1-code-security-trading-review.md`
- Moved visual/reference assets under `/docs`:
  - `/docs/references/Mock_UI_Renders`
  - `/docs/references/Research_Docs`
- Removed stale temporary handoff document:
  - `/docs/99-session-handoff-to-codex.md`

## Data and Schema Notes

- Scan output is persisted in:
  - `scan_runs`
  - `scan_candidates`
- JSONB fields are used for evolving scanner payloads:
  - `indicator_snapshot`
  - `score_breakdown`
  - `reasons`
  - `caution_flags`
- Latest scan endpoint now prefers persisted scans and falls back to fixture only when no scan exists.

## Verification Performed

```powershell
docker compose config
docker compose up -d --build
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend pytest
docker compose run --rm backend python -m app.scripts.seed_sp500_universe
docker compose run --rm backend python -m app.scripts.ingest_yfinance_bars --symbols AAPL MSFT NVDA --period 3mo
docker compose run --rm backend python -m app.scripts.run_momentum_scan --limit 25
docker compose run --rm backend python -m pip check
npm.cmd run build
npm.cmd audit --audit-level=moderate
```

Observed results:

- Backend tests passed (`16 passed`).
- Frontend build passed.
- Python dependency check passed.
- Frontend audit reported `0 vulnerabilities`.
- Health and scan endpoints responded successfully.
- Persisted generated scanner output available via `/api/scans/latest`.

## Review Outcomes

Phase 1 review is complete and documented in:

- `/docs/phases/phase-1-data-foundation/phase-1-code-security-trading-review.md`

Highlights:

- Code review: frontend nullability fixes applied.
- Security review: localhost-only port bindings applied.
- Trading-safety review: bootstrap scanner no longer labels candidates `Actionable` before risk/reward exists.

## Known Limitations (Intentional for Phase 1)

- yfinance remains bootstrap-only and not final trading-grade source.
- Generated scanner is intentionally narrow (`Trend Momentum`) for pipeline validation.
- Risk/reward estimates are not yet implemented for generated scanner candidates.
- Local DB credentials remain development defaults.

## Reviewer Checklist

- [ ] Pull branch and run local stack with Docker Compose.
- [ ] Confirm Alembic migrations apply cleanly on a fresh DB.
- [ ] Confirm `pytest` and frontend build pass locally.
- [ ] Confirm `/api/scans/latest` returns persisted generated scan after running scanner script.
- [ ] Confirm localhost-only port bindings in `docker-compose.yml`.
- [ ] Confirm docs reflect current Phase 1 state and review outcomes.

## Suggested Follow-up (Post-Merge)

1. Start Phase 2 setup detection expansion.
2. Add risk/reward estimation before any `Actionable` status.
3. Add scanner fixtures/tests for multiple setup families.
4. Wire candidate detail/indicator context deeper into frontend workflow.
