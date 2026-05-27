# Phase 2 Code, Security, and Trading Review

**Project:** PoorToPour
**Phase:** Phase 2 - Technical Scanner MVP
**Status:** ✅ Done
**Last updated:** 2026-05-27

---

## 1. Review Scope

Reviewed Phase 2 changes against:

- `/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md`
- `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`

Review areas:

- S&P 500 plus Nasdaq 100 universe seeding and dedupe;
- Alpha Vantage provider and env-only secret handling;
- expanded indicator snapshot fields;
- breakout, pullback continuation, and relative strength leader detectors;
- scoring, risk/reward estimates, candidate status rules, and scan persistence;
- focused frontend scanner evidence display;
- dependency, configuration, and trading-safety posture.

---

## 2. Code Review

**Status:** ✅ Complete.

Findings:

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| High | Stale price-data gate existed in shared status rules, but detectors were not passing a real freshness result. An otherwise clean stale candidate could become higher confidence than intended. | `backend/app/services/setup_detectors.py`; `backend/app/services/status_rules.py` | ✅ Fixed during review. Detectors now compute freshness from `latest_date`, add a stale-data caution flag, pass `price_data_fresh`, and regression tests cover stale breakout blocking. |
| Medium | External OHLCV provider parsing validated positive numeric fields but did not reject malformed dates or internally inconsistent OHLC rows. Bad provider rows could be persisted and later affect indicators. | `backend/app/providers/alpha_vantage_provider.py`; `backend/app/providers/yfinance_provider.py` | ✅ Fixed during second review. Shared provider validation now rejects non-ISO Alpha Vantage dates and inconsistent daily bars; Alpha Vantage and yfinance tests cover skipped invalid rows. |

Additional notes:

- Scanner setup detection is deterministic and test-covered.
- Risk/reward assumptions are configurable through reviewed settings/env defaults.
- Scanner output persists through existing Phase 1 scan tables.
- Frontend candidate detail now surfaces reasons, caution flags, score components, and risk context for manual review.

---

## 3. Security Review

**Status:** ✅ Complete.

Checks performed:

```powershell
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH)" -S --glob '!.env' --glob '!frontend/node_modules/**' --glob '!frontend/dist/**' --glob '!backend/.venv/**' .
```

Results:

- Compose configuration validated with `docker compose config --quiet`.
- Python dependency check passed: no broken requirements.
- Frontend audit passed: 0 moderate-or-higher vulnerabilities reported.
- No real Alpha Vantage API key was found in tracked files.
- Expected secret-scan hits are limited to `.env.example` placeholders, local-only Compose database password values, provider parameter names, README/setup docs, and test fixtures.

Security notes:

- `.env` remains local and gitignored.
- `docker-compose.yml` contains local development database credentials only; this is acceptable for local Docker Compose, but production/cloud deployment must use managed secrets and non-default credentials.
- Prefer `docker compose config --quiet` for validation because the non-quiet output can print resolved environment values.

---

## 4. Trading-Safety Review

**Status:** ✅ Complete.

Checks:

- ✅ Scanner rules are deterministic; no AI-generated trade decisions are used.
- ✅ No broker automation or order placement exists.
- ✅ `Actionable` requires setup confirmation, score threshold, risk/reward estimate, fresh price data, and no blocking caution flags.
- ✅ Missing required inputs and stale price data block detected candidates.
- ✅ Reasons, caution flags, risk context, and score components are visible in backend output and frontend candidate detail.
- ✅ Scanner warning frames output as research-only and not a trading recommendation.

Trading-safety notes:

- `Actionable` is still a manual-review research status, not a buy signal.
- Relative strength leader detection is a price-leadership proxy only; true SPY/QQQ-relative strength remains documented MVP/MVP+ follow-up work.
- No backtesting has been added yet, so setup performance remains unvalidated.
- Alpha Vantage rate limits can make full-universe refreshes slow or stale if ingestion is not scheduled carefully.

---

## 5. Final Verification

Verification performed on 2026-05-27:

```powershell
docker compose run --rm backend pytest
npm.cmd run build
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
```

Observed results:

- Backend tests: 69 passed.
- Frontend build: passed.
- Compose config: passed.
- Python dependency check: passed.
- Frontend audit: 0 vulnerabilities.

Manual/user-confirmed UI checks:

- Candidate row click selection works.
- Sidebar collapse toggle works.
- Provider summary text wrapping works.
- Summary cards/table horizontal overflow behavior works on the tall/narrow viewport.

---

## 6. Remaining Risks / Follow-Ups

- Add true benchmark-relative strength once SPY/QQQ benchmark bars are available to the scanner.
- Add candidate visual evidence in MVP/MVP+ so each candidate can be inspected with chart context.
- Add backtesting before treating scanner scores as strategy-quality evidence.
- Review cloud secret handling and database credentials before any hosted MVP/MVP+ deployment.

---

## 7. Coding-Standards Follow-Up

Completed after the initial review checkpoint:

- Centralized ingest script symbol resolution in `backend/app/scripts/symbol_resolution.py` instead of duplicating fallback development symbols in provider-specific scripts.
- Replaced repeated risk/reward warning literals with a named constant/helper.
- Extracted relative-strength signal-state and annotation helpers out of `RelativeStrengthLeaderDetector.detect()` to reduce method complexity.
- Added symbol resolution unit tests.

---

## 8. Second Review Against Updated Guidelines

Completed after adding the explicit coding, security, and trading-strategy standards to `/docs/10-ai-working-guidelines.md`.

Additional checks:

- Reviewed provider parsing against external-data validation expectations.
- Reviewed scanner output against trading-strategy standards for determinism, reasons, cautions, freshness, and risk context.
- Re-ran security checks against OWASP/NIST-inspired MVP expectations.
- Re-ran backend, frontend, dependency, and secret-scan verification.

Additional fix:

- Added shared daily-bar validation for provider adapters so malformed external OHLCV rows are skipped before persistence.
