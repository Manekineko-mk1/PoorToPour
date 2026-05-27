# PoorToPour Phase 1 Review

**Project:** PoorToPour  
**Date:** 2026-05-26  
**Scope:** Phase 1 data foundation baseline  
**Status:** ✅ Complete

---

## 1. Review Scope

This review covered the Phase 1 baseline before first commit/push:

- local Docker Compose app shell;
- FastAPI backend;
- React/Vite frontend shell;
- PostgreSQL persistence and Alembic migrations;
- Adminer local database inspection;
- S&P 500 universe seed;
- mock provider fixtures;
- yfinance bootstrap OHLCV ingestion;
- deterministic indicator snapshots;
- scan-run and candidate persistence;
- first bootstrap trend/momentum scanner.

MVP boundaries remain unchanged:

- long-only;
- daily/weekly swing research;
- manual review only;
- deterministic scanner logic;
- no broker automation;
- no AI-generated trade decisions.

---

## 2. Code Review

**Status:** ✅ Passed after fixes.

Findings fixed:

| Finding | Resolution |
| --- | --- |
| Frontend assumed generated scanner fields were always non-null. | Updated frontend API types and rendering for nullable `relative_volume`, `risk_reward`, `rsi`, and timestamp/context fields. |
| Generated scanner output had richer `reasons` data than the original fixture-focused frontend type. | Added optional `reasons` support in the frontend selected-candidate panel. |

Verification:

```powershell
docker compose run --rm backend pytest
npm.cmd run build
git diff --check
```

Result:

- Backend tests: 16 passed.
- Frontend build: passed.
- Diff whitespace check: passed.

---

## 3. Security Review

**Status:** ✅ Passed for local MVP development after fixes.

Findings fixed:

| Finding | Resolution |
| --- | --- |
| Docker Compose ports were published on all host interfaces. | Bound frontend, backend, Postgres, and Adminer ports to `127.0.0.1`. |

Checks performed:

```powershell
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|UPZU|Alpha Vantage|PRIVATE|BEGIN RSA|BEGIN OPENSSH)" -S .
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
docker compose config
```

Result:

- No committed API keys found.
- Only expected local dev database password references found.
- Python dependency check passed.
- Frontend audit found 0 vulnerabilities.
- Compose config passed.

Residual security notes:

- Local database credentials are development-only defaults.
- Adminer is for local inspection only and is bound to `127.0.0.1`.
- The previously shared Alpha Vantage key was not committed.

---

## 4. Trading-Safety Review

**Status:** ✅ Passed for Phase 1 bootstrap scope after fixes.

Findings fixed:

| Finding | Resolution |
| --- | --- |
| Bootstrap scanner could label a candidate `Actionable` even though risk/reward is not implemented. | Changed bootstrap generated scanner status logic so generated candidates max out at `Watch` until risk/reward exists. |

Trading-safety notes:

- The generated scanner is a narrow trend/momentum detector for validating the data-to-candidate pipeline.
- Scanner output includes the warning: `Bootstrap scanner for Phase 1 validation. Not a trading recommendation.`
- yfinance remains a bootstrap source only, not final trading-grade data.
- Generated candidates include reasons, score breakdown, and caution flags.
- Incomplete indicator history is surfaced as warnings.

---

## 5. Final Verification

Final verification commands:

```powershell
docker compose config
docker compose run --rm backend pytest
npm.cmd run build
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
git diff --check
```

Final runtime checks:

- `GET http://localhost:8000/api/health` passed.
- `GET http://localhost:8000/api/scans/latest` returned the generated bootstrap trend/momentum scan.
- Docker services were running on localhost-bound ports:
  - frontend: `127.0.0.1:5173`
  - backend: `127.0.0.1:8000`
  - Postgres: `127.0.0.1:5432`
  - Adminer: `127.0.0.1:8080`

---

## 6. Review Outcome

Phase 1 is ready for Jesse's final local inspection, commit, and push.

Recommended next phase:

> Phase 2 - Technical Scanner MVP

First likely Phase 2 work:

1. Expand setup detection beyond the bootstrap trend/momentum detector.
2. Add risk/reward estimates before any candidate can be labelled `Actionable`.
3. Add richer score component tests and scanner fixtures.
4. Start wiring candidate inspection into the frontend.
