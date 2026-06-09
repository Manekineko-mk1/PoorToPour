# Phase 3 Code, Security, Trading, and UX Review

**Project:** PoorToPour
**Phase:** Phase 3 - Dashboard MVP
**Status:** ✅ Complete
**Last updated:** 2026-06-09

---

## 1. Review Scope

Reviewed Phase 3 Dashboard MVP changes:

- dashboard shell, routing, and responsive layout;
- latest scan summary and data-health states;
- candidate ranking table;
- candidate detail route, chart evidence, chart toolbar, and right rail;
- backend chart, scan, settings, and market-data refresh APIs;
- manual scan flow with yfinance refresh-before-scan;
- scheduled scan flow with daily yfinance refresh-before-scan reuse and local/dev startup catch-up;
- scan history;
- settings page and secret redaction;
- accessibility and MVP UX polish;
- trading-safety wording and deterministic evidence display;
- Phase 3 docs, tracker, and PR draft.

---

## 2. Code Review

**Status:** ✅ Passed with fixes.

Findings:

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| Medium | Public hosted manual scans could refresh the full persisted universe without auth or a symbol cap. | `backend/app/api/routes/scans.py` | ✅ Fixed |
| Low | `.env.example` used `POORTOPOUR_ENV`, but the app setting is `environment`, so the real env var is `POORTOPOUR_ENVIRONMENT`. | `.env.example` | ✅ Fixed |
| Low | Manual scan running copy still implied a persisted-bars-only scan after yfinance refresh became the default path. | `frontend/src/App.tsx` | ✅ Fixed |
| Low | Frontend API errors hid backend details, including the new hosted manual-scan guard message. | `frontend/src/api.ts` | ✅ Fixed |

Code notes:

- Backend chart payload keeps indicator computation server-side; React does not recompute scanner indicators.
- Candidate Detail chart controls are client-side presentation controls only; timeframe buttons slice existing daily bars and do not alter scanner logic.
- Settings display endpoint returns explicit secret visibility booleans and not secret values.
- Frontend remains a single large `App.tsx`; acceptable for MVP, but a Phase 4/5 refactor should split route/page/chart/table components.

---

## 3. Security Review

**Status:** ✅ Passed for MVP/local demo scope.

Commands run:

```powershell
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH|DATABASE_URL|SUPABASE|postgresql\+|postgres://|password=)" -S --glob '!.env' --glob '!.env.*' --glob '!frontend/node_modules/**' --glob '!frontend/dist/**' --glob '!backend/.venv/**' --glob '!data/**' .
git diff --check
```

Results:

- ✅ Docker Compose config validation passed.
- ✅ Backend dependency check passed with no broken requirements.
- ✅ npm audit found 0 moderate-or-higher vulnerabilities.
- ✅ `git diff --check` passed.
- ✅ Secret scan found no private API keys, Supabase URLs, or private key material.

Expected secret-scan hits:

- `docker-compose.yml` contains local-only development database defaults.
- Alpha Vantage docs/tests/provider code mention API key names and test values.
- Review/implementation docs contain the secret-scan command itself.

Security fixes added during review:

- Hosted/non-local manual scans are disabled by default.
- Hosted manual scans can only be enabled explicitly with `POORTOPOUR_ALLOW_HOSTED_MANUAL_SCAN=true`.
- Enabled hosted manual scans are capped by `POORTOPOUR_HOSTED_MANUAL_SCAN_MAX_SYMBOLS`, default `25`.
- Frontend now surfaces backend error details for manual scan failures.

Residual security notes:

- There is still no authentication layer. Keep hosted/demo deployments read-only or explicitly constrained.
- Set `POORTOPOUR_ENVIRONMENT=production` on hosted services so non-local safeguards apply.

---

## 4. Trading-Safety Review

**Status:** ✅ Passed for research-only MVP.

Checks:

- ✅ Candidate statuses remain `Actionable`, `Watch`, `Avoid`, and `Blocked`; no buy/sell execution language was introduced.
- ✅ Risk/reward appears as research context and not a trade instruction.
- ✅ Data source, provider status, data date, stale/partial/failed states, and warnings are visible.
- ✅ Chart overlays come from deterministic backend/scanner payloads.
- ✅ yfinance-backed scans are labelled through provider/source/freshness context.
- ✅ No broker automation or AI trade decisions were introduced.
- ✅ Single-user MVP warning copy was removed from cluttered UI surfaces, but the system remains non-executional.

Residual trading-safety notes:

- yfinance is practical for MVP validation but not trading-grade.
- Benchmark-relative strength remains MVP/MVP+ follow-up when SPY/QQQ benchmark bars are part of scanner input.
- Backtesting is still required before trusting setup quality or considering alerts/paper trading.

---

## 5. UX and Accessibility Review

**Status:** ✅ Passed for MVP, with known follow-ups.

Checks:

- ✅ Dashboard layout follows the mock direction while preserving MVP scope.
- ✅ Candidate table supports filtering, sorting, sticky headers, dynamic overflow, and click-through detail.
- ✅ Candidate Detail uses compact identity/context rows, chart-first layout, right-side research/trade panels, and avoids chart/header overlap.
- ✅ Chart toolbar timeframe controls, display options, and fullscreen toggle are functional.
- ✅ Statuses are communicated with text plus color.
- ✅ Navigation and primary buttons are native anchors/buttons and keyboard-reachable.
- ✅ User browser checks confirmed the main dashboard, Candidate Detail, manual scan, Scan History, and Settings flows during Phase 3.

Known UX follow-ups:

- Add automated frontend component or route tests once a frontend test runner is introduced.
- Continue visual QA on mobile-ish widths before public demo polish.
- Split `App.tsx` into focused components after MVP stabilization.

---

## 6. Final Verification

Commands run:

```powershell
docker compose run --rm backend pytest
npm.cmd run build
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
git diff --check
```

Results:

- ✅ Backend suite passed: 148 tests.
- ✅ Frontend production build passed.
- ✅ Docker Compose config validation passed.
- ✅ Backend dependency check passed.
- ✅ npm audit found 0 vulnerabilities.
- ✅ Diff whitespace check passed.

Manual/browser checks completed during Phase 3:

- Dashboard loads.
- Candidate table filters, sorts, scrolls, and opens detail.
- Candidate detail chart renders nonblank evidence.
- Chart toolbar options and fullscreen work.
- Scan History loads.
- Settings loads without secrets.
- Manual scan refreshes yfinance data locally and runs deterministic scan.

---

## 7. Remaining Risks / Follow-Ups

| Risk / Follow-up | Severity | Recommendation |
| --- | --- | --- |
| No authentication for hosted demo | Medium | Keep manual scan disabled by default in non-local environments; add auth before any broader hosted/admin controls. |
| yfinance is unofficial data | Medium | Keep freshness/source labels visible; revisit Alpha Vantage or paid provider after scanner value is proven. |
| No frontend test runner | Low | Add Vitest/Testing Library or Playwright-style route checks when frontend complexity grows. |
| Large `App.tsx` | Low | Split page, chart, table, settings, and scan-history components after MVP feature stabilization. |
| Strategy not backtested | High | Do not add alerts, paper trading, or automation until Phase 5 validation exists. |
| In-process scheduler is not cloud-grade orchestration | Medium | Accept for single-instance MVP/demo; move to Render Cron, a worker, or a DB/distributed lock before relying on hosted schedule reliability. |

---

## 8. Review Outcome

✅ Phase 3 is ready for final PR preparation from code, security, trading-safety, UX, and test-review perspectives.

The remaining work before merge is ordinary PR hygiene: review the diff, confirm hosted environment variables, and make sure the PR draft matches the final scope.

---

## 9. Secondary Review

**Reviewer:** Independent secondary pass (AI), 2026-06-04.
**Status:** ✅ Passed. Primary findings confirmed; two additional Low findings raised and fixed.

### 9.1 Gates re-run independently

| Check | Result |
| --- | --- |
| `docker compose run --rm backend pytest` | ✅ 148 passed |
| `npm.cmd audit --audit-level=moderate` | ✅ 0 vulnerabilities |
| `git diff --check` | ✅ Clean |

### 9.2 Agreement with primary findings

- ✅ Agree: hosted manual-scan guard (`_validated_refresh_limit`) correctly defaults non-local to 403, gates on `allow_hosted_manual_scan`, caps via `min(refresh_limit, max)`, and is covered by tests.
- ✅ Agree: `.env.example` env var name (`POORTOPOUR_ENVIRONMENT`) matches the `POORTOPOUR_` prefix over the `environment` field.
- ✅ Agree: manual scan running copy now reflects yfinance refresh-before-scan.
- ✅ Agree: frontend now surfaces backend error detail via `responseErrorMessage` with a safe fallback.
- ✅ Confirmed: chart indicators are computed server-side; candidate `rsi` is `None` in real scans, so there is no scanner-vs-chart RSI inconsistency.

### 9.3 Additional findings (raised in secondary review)

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| Low | Chart RSI used a simple gain/loss mean instead of Wilder's smoothing, so values diverged from standard charting platforms. Display-only and deterministic, but the dashboard frames it as evidence (guideline §7.3). | `backend/app/services/chart_data.py` | ✅ Fixed |
| Low | `POST /api/scans/manual` `refresh_limit`/`refresh_period` were unbounded; a negative `refresh_limit` passed through `min()` in hosted mode and sliced symbols from the end. | `backend/app/api/routes/scans.py` | ✅ Fixed |

Fix detail:

- Chart RSI now uses Wilder's smoothing (seed with a simple average of the first `period` changes, then Wilder-smooth the remainder). Added a reference-value regression test that distinguishes Wilder's (75.0) from the previous simple mean (50.0) for `[10, 11, 10, 11]` at period 2.
- Manual scan now validates `refresh_limit` with `Query(ge=1)` and constrains `refresh_period` to a `Literal` of yfinance-supported periods; both reject bad input with 422. Added regression tests for the 422 paths.

### 9.4 Minor notes (no action taken)

- `display_settings` secret-visibility booleans are hardcoded `False` constants rather than derived from config. Accurate (the endpoint never includes secret values) but decorative; the meaningful coverage is the `database_url`/`alpha_vantage_api_key` not-in-payload assertions.
- `chart_data._chart_bar` recomputes SMA/RSI per bar (O(n²)); negligible at daily 1–2y scale (~250–500 bars). Acceptable for MVP.

### 9.5 Secondary review outcome

✅ Phase 3 remains ready for PR. The two new Low findings were fixed during this pass and do not change the overall outcome.

---

## 10. Code Review Follow-Up

**Reviewer:** Code review follow-up, 2026-06-04.
**Status:** ✅ Passed after fixes.

Findings fixed:

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| Medium | Candidate Detail opened from Scan History could show "Candidate not found" if the clicked historical candidate was no longer present in the latest scan. | `frontend/src/App.tsx` | ✅ Fixed |
| Medium | Chart endpoint attached candidate context by latest symbol/rank only, so duplicate-symbol setups could show the wrong setup's risk overlay. | `backend/app/repositories/scans.py`, `backend/app/api/routes/market_data.py`, `frontend/src/api.ts`, `frontend/src/App.tsx` | ✅ Fixed |

Fix detail:

- Candidate detail routing now carries clicked candidate context and the selected source scan/run so historical candidates opened from Scan History remain inspectable.
- Chart requests now include selected `setup` and `scan_id`; backend chart context lookup filters by both when provided.
- Added regression coverage for setup/scan-aware chart context lookup.

Verification:

- `docker compose run --rm backend pytest tests/test_chart_data.py`: ✅ 5 passed.
- `docker compose run --rm backend pytest`: ✅ 148 passed.
- `npm.cmd run build`: ✅ passed.

---

## 11. Scheduled Scan Follow-Up

**Reviewer:** Scheduled scan follow-up, 2026-06-09.
**Status:** ✅ Passed for single-instance MVP/demo scope.

Changes reviewed:

- Added a small FastAPI lifespan-managed scheduler that starts with the deployed app.
- Defaults to `06:00` in `America/New_York`.
- Reuses the same yfinance refresh-before-scan and deterministic scan path as manual scans.
- Adds local/dev startup catch-up when today's scheduled scan was missed.
- Keeps public hosted manual-scan safeguards separate from the trusted in-process scheduled job.
- Adds environment settings and safe display-settings copy.

Risk notes:

- This is an in-process scheduler. It only runs while the app process is awake.
- Single-instance Render-style demos are acceptable for MVP, but scaled/cloud production should use a dedicated cron/worker or a database/distributed lock to prevent missed or duplicate runs.

Verification:

- `docker compose run --rm backend pytest tests/test_scheduled_scan.py tests/test_scanner_config.py tests/test_display_settings.py`: ✅ 32 passed.
- `docker compose run --rm backend pytest`: ✅ 148 passed.
