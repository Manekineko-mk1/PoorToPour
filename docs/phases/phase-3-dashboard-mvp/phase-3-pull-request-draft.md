# PR Draft: Phase 3 Dashboard MVP

## Summary

Phase 3 turns the Phase 2 deterministic scanner output into the first complete Dashboard MVP workflow.

The user can now open the app, read the latest scan health, compare ranked candidates with practical filtering/sorting, open a candidate detail route with backend-derived chart evidence and rule context, review previous scan runs, view safe (secret-free) settings, trigger a manual scan that refreshes local yfinance data before running the deterministic scanner, and let a small scheduled job run that same refresh-and-scan workflow daily.

The dashboard, scan history, and settings screens follow the v0.2 mock render direction while staying inside MVP scope: research-only, deterministic, long-only, no automation, no AI trade decisions.

## Branch

- `feature/phase_3_dashboard_mvp`

## Scope of Change

Backend:

- Add `GET /api/symbols/{symbol}/chart` and a `chart_data` service that builds a deterministic chart payload server-side: candles, volume, SMA 20/50/200, RSI 14, insufficient-history warnings, and candidate context (setup, status, score, reasons, caution flags, risk/reward overlay).
- Add `GET /api/settings/display` and a `configuration` route that returns environment/provider context, scanner assumptions, safe user preferences, and explicit secret-visibility booleans — never secret values.
- Add `POST /api/scans/manual` with an optional yfinance refresh-before-scan path, plus a `market_data_refresh` service that refreshes persisted daily bars in chunks and returns a per-run refresh summary (requested/refreshed/failed/bars, bounded failure messages).
- Add an in-process scheduled scan service that starts with FastAPI, defaults to `06:00` `America/New_York`, reuses the yfinance refresh-before-scan pipeline, and performs local/dev startup catch-up when today's scheduled scan was missed.
- Add `get_latest_candidate_for_symbol` repository lookup to attach the most recent candidate context to a symbol chart.
- Add hosted manual-scan safeguards in config: disabled outside local/dev by default, opt-in via `POORTOPOUR_ALLOW_HOSTED_MANUAL_SCAN`, capped by `POORTOPOUR_HOSTED_MANUAL_SCAN_MAX_SYMBOLS` (default 25).

Frontend:

- Align the app shell with the v0.2 dashboard direction while preserving MVP boundaries.
- Add lightweight client-side routing for Dashboard, Candidate Detail, Scan History, and Settings.
- Improve the latest-scan summary cards, data-health states, freshness/staleness signalling, and empty/error/filtered-empty states.
- Upgrade the candidate ranking table with setup/status filtering, sorting, sticky headers, and click-through detail.
- Add a candidate detail page with a TradingView Lightweight Charts evidence panel (candles, volume, moving averages, RSI, research-estimate overlays), a chart toolbar (timeframe slicing, display options, fullscreen), a compact identity strip, and a color-coded right rail for explanation/score breakdown/caution flags/risk-reward.
- Add a Scan History page and a Settings page with read-only system/admin config and safe user preferences.
- Wire the manual scan action with loading/success/error states and active data-source/freshness labelling, and surface backend error detail on failure.
- Responsive, accessibility, and narrow/tall viewport polish.

Docs:

- Update product-requirements and dashboard-design docs, add Phase 3 implementation plan, execution tracker, and code/security/trading review.
- Refresh the mock render set (add `Mock_UI_PoorToPour_01_CandidateDetail.png`, archive superseded renders).

Implementation plan:

- `/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md`

Review artifact:

- `/docs/phases/phase-3-dashboard-mvp/phase-3-code-security-trading-review.md`

## Verification Performed

```powershell
docker compose run --rm backend pytest
npm.cmd run build
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
git diff --check
```

Observed results:

- `docker compose run --rm backend pytest`: 148 passed.
- `npm.cmd run build`: passed.
- `docker compose config --quiet`: passed.
- `docker compose run --rm backend python -m pip check`: no broken requirements.
- `npm.cmd audit --audit-level=moderate`: 0 vulnerabilities.
- `git diff --check`: passed (no whitespace errors).
- Secret scan found no private API keys, Supabase/database URLs, or private key material; expected hits were local Docker dev defaults, Alpha Vantage parameter names/test values, and the scan command quoted in docs.

Manual/user-confirmed checks (completed during Phase 3):

- Dashboard loads the latest scan summary and is visually close to the v0.2 main-screen mock within MVP scope.
- Candidate table filters, sorts, scrolls, and opens detail.
- Candidate detail follows the v0.2 candidate-detail direction; chart renders non-blank candles, volume, moving averages, RSI, and research-estimate lines where available.
- Chart toolbar timeframe controls, display options, and fullscreen work without overlapping the chart or identity strip.
- Scan History loads previous runs.
- Settings loads without exposing secrets.
- Manual scan refreshes yfinance data locally, runs the deterministic scan, and labels source/freshness; loading/error/success states are clear.
- Scheduled scan defaults and local/dev startup catch-up are covered by focused backend tests; hosted scheduling remains an in-process MVP/demo mechanism.
- Narrow/tall (1080x2560) layout remains usable.

## Review Outcomes

Phase 3 code/security/trading/UX review completed on 2026-06-04, with an independent secondary review the same day.

Fixes made during the primary review:

- Hosted/non-local manual scan is disabled by default and only enabled via `POORTOPOUR_ALLOW_HOSTED_MANUAL_SCAN=true`, with a symbol cap (`POORTOPOUR_HOSTED_MANUAL_SCAN_MAX_SYMBOLS`).
- Manual scan frontend errors now surface backend detail.
- Manual scan running copy now reflects yfinance refresh-before-scan.
- `.env.example` now uses `POORTOPOUR_ENVIRONMENT` and documents the hosted manual-scan flags.

Secondary review outcome:

- Independently re-ran pytest, `npm audit` (0 vulnerabilities), and `git diff --check` (clean); all primary findings confirmed.
- Two additional Low findings were raised and fixed during the secondary pass:
  - Chart RSI moved from a simple mean to Wilder's smoothing so values match standard charting platforms (display-only, deterministic), with a reference-value regression test.
  - `POST /api/scans/manual` now validates `refresh_limit` (`Query(ge=1)`) and constrains `refresh_period` to supported yfinance periods, returning 422 on bad input, with regression tests.
- Backend suite is now 148 passed after scheduled scan follow-up work.

## Known Limitations and Follow-Ups

Expected MVP boundaries:

- No broker automation.
- No AI-generated trade decisions.
- No watchlist persistence.
- No alert notifications.
- No sector/theme scanner grid.
- No full backtesting UI.
- No intraday scanner.
- yfinance-backed MVP scan data is not trading-grade and is labelled with source/freshness.
- No authentication layer; hosted/demo deployments must stay read-only or explicitly constrained, with `POORTOPOUR_ENVIRONMENT=production` set so non-local safeguards apply.
- Scheduled scans are in-process and suitable for single-instance MVP/demo use; use Render Cron, a worker, or a database/distributed lock before depending on cloud schedule reliability.

Follow-ups:

- No frontend test runner yet; add Vitest/Testing Library or Playwright route checks as frontend complexity grows.
- `App.tsx` remains a single large component; split page/chart/table/settings components after MVP stabilization.
- Strategy is not yet backtested; do not add alerts, paper trading, or automation until Phase 5 validation exists.

## Reviewer Checklist

- [x] Confirm backend tests pass (148 passed).
- [x] Confirm frontend build passes.
- [x] Confirm dashboard UX matches MVP scope.
- [x] Confirm candidate chart evidence is deterministic and backend-derived.
- [x] Confirm copy remains research-only, not trade-instructional.
- [x] Confirm no secrets are exposed in frontend, logs, docs, or committed files.
- [x] Confirm Phase 3 code/security/trading/UX review has been read.
- [ ] Confirm hosted environment variables (`POORTOPOUR_ENVIRONMENT`, manual-scan flags, scheduled-scan flags) before any non-local deploy.
