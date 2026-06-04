# Phase 3 Execution Tracker: Dashboard MVP

**Project:** PoorToPour
**Phase:** Phase 3 - Dashboard MVP
**Status:** ✅ Done
**Branch:** `feature/phase_3_dashboard_mvp`
**Last updated:** 2026-06-04

---

## 1. Phase Goal

Turn the Phase 2 deterministic scanner output into the first complete Dashboard MVP workflow.

Phase 3 should let the user open the app, understand the latest scan, compare ranked candidates, inspect one candidate with chart evidence and rule context, review previous scan runs, and adjust basic dashboard-facing settings.

MVP boundaries remain:

- long-only swing-trade research;
- daily/weekly scanner output only;
- deterministic scanner evidence only;
- no broker automation;
- no AI-generated trade decisions;
- no notification alerts;
- no sector/theme scanner;
- no watchlist persistence unless explicitly re-approved.

Primary references:

- `/docs/01-product-requirements.md`
- `/docs/05-dashboard-design.md`
- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_01_MainScreen_v0.2.png`
- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_02_ScanHistory_v0.2.png`
- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_03_Settings_v0.2.png`
- `/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md`

---

## 2. Detailed Checklist

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| ID | Work Item | Status | Verification / Exit Criteria |
| --- | --- | --- | --- |
| P3-A | Confirm Dashboard MVP scope and UI sequence | ✅ Done | Phase 3 tracker and implementation plan preserve MVP scope and defer MVP+ items |
| P3-B | Align app shell with v0.2 dashboard direction | ✅ Done | Desktop shell now has mock-style global header, sidebar navigation/status rail, main workspace, responsive collapse, champagne branding, and local smoke checks |
| P3-C | Improve latest scan summary surface | ✅ Done | Dashboard shows scan status, scan type/provider, universe, symbols processed, candidates, data health, warning banner, and mock-aligned summary card layout |
| P3-D | Upgrade candidate ranking table | ✅ Done | Table supports score-first ranking, candidate selection, setup/status filters, sortable rank/score/risk-reward columns, visible cautions, responsive overflow, empty filtered state, and mock-aligned density |
| P3-E | Add candidate detail route/page | ✅ Done | Clicking a candidate opens a route-compatible detail view with candidate header, deterministic explanation, score, risk/reward, context panels, and an explicit chart placeholder for P3-F/P3-G |
| P3-F | Add chart data API and chart-ready payloads | ✅ Done | Backend exposes selected symbol OHLCV bars enriched with SMA 20/50/200, RSI 14, candidate context, warnings, and risk/reward overlays without requiring React to recompute indicators |
| P3-G | Add candidate chart evidence | ✅ Done | Candidate detail renders a TradingView Lightweight Charts candlestick chart with volume bars, SMA 20/50/200, RSI 14 strip with draggable divider, chart warnings, and entry/invalidation/target price lines when available |
| P3-H | Add explanation, score, caution, and risk panels | ✅ Done | Detail page groups setup context, deterministic reasons, caution flags, risk/reward estimate, and score breakdown under the Research Context panel |
| P3-I | Add scan history page | ✅ Done | Scan History route shows prior persisted scan runs, statuses, candidate counts, data dates, selected run metadata, and selected run candidates with click-through to candidate detail |
| P3-J | Add settings page MVP | ✅ Done | Settings route shows display-safe runtime/provider config, enabled setup families, scanner risk/reward config, safe user preferences, read-only admin/system options, AI disabled state, and explicit secret redaction |
| P3-K | Wire manual scan action safely | ✅ Done | Manual scan button triggers a persisted-bar deterministic scan, shows loading/error/success states, persists the run, and refreshes latest output |
| P3-K.1 | Add market data refresh before manual scan | ✅ Done | Manual scan flow refreshes yfinance daily bars, persists updated bars, runs the deterministic scanner, and returns refresh metadata; dev/test calls can limit the refresh scope |
| P3-L | Add freshness, empty, partial, and error states | ✅ Done | Dashboard and scan history now distinguish loading, API failure, stale data, partial/warning scan output, zero-candidate scans, and filter-empty states |
| P3-M | Add frontend accessibility and responsive polish | ✅ Done | Candidate table owns dynamic overflow; Candidate Detail follows the mock direction with slim identity/context rows, exchange/setup badges, functional chart timeframe slicing, chart options panel, reversible fullscreen toggle, larger Chart Evidence area, and color-coded right-side research/trade/caution panels; user browser confirmation completed through latest detail-screen polish |
| P3-N | Add tests and build verification | ✅ Done | Backend regression suite passed with 78 tests, frontend production build passed, Docker Compose config passed, backend dependency check passed, npm audit passed, and diff whitespace check passed; no frontend component test runner exists yet, so build verification is the practical frontend check for MVP |
| P3-O | Phase 3 review checkpoint | ✅ Done | Code, security, trading-safety, UX, and test review completed in `phase-3-code-security-trading-review.md`; hosted manual scan guard and env example mismatch were fixed during review |
| P3-P | Secondary review and follow-up fixes | ✅ Done | Independent secondary review re-ran gates (83 backend tests, 0 npm vulnerabilities, clean whitespace) and confirmed primary findings; chart RSI moved to Wilder's smoothing and manual-scan `refresh_limit`/`refresh_period` are now validated, each with regression tests |

---

## 3. Acceptance Criteria

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P3-001 | Dashboard Home shows latest scan summary and data health | ✅ Done | Data Health now ignores hidden single-user research-only copy while surfacing failed, partial/warning, and stale scan states |
| AC-P3-002 | Dashboard Home shows ranked candidates from persisted scanner output | ✅ Done | Sorted by score by default, with setup/status context |
| AC-P3-003 | Candidate table supports practical scan review | ✅ Done | Filtering, sorting, visible cautions, candidate selection, and click-through detail are complete |
| AC-P3-004 | Candidate Detail page exists | ✅ Done | Dedicated candidate route exists and supports direct deep links |
| AC-P3-005 | Candidate Detail shows chart evidence | ✅ Done | Candles, volume, SMA 20/50/200, RSI 14, chart warnings, and optional research estimate price lines are visible |
| AC-P3-006 | Candidate Detail shows deterministic explanation | ✅ Done | Reasons, cautions, score components, setup context, and risk/reward fields are visible in the Research Context panel |
| AC-P3-007 | Scan History page exists | ✅ Done | Prior runs are inspectable, selected run metadata is visible, and candidates can open detail pages |
| AC-P3-008 | Settings page exists for MVP config visibility | ✅ Done | Settings page exists with read-only system/admin options, safe user-preference display, and no exposed secrets |
| AC-P3-009 | Manual scan is usable from the dashboard | ✅ Done | Button shows running/success/error state; backend endpoint persisted a local manual scan successfully |
| AC-P3-009A | Manual scan can optionally refresh market data first | ✅ Done | Default manual scan refreshes yfinance bars before scanning; persisted-only mode remains available through `refresh_market_data=false` |
| AC-P3-010 | Frontend remains research-only and not trade-instructional | ✅ Done | Copy and visual hierarchy avoid buy/sell implication; risk/reward remains framed as research context, and single-user MVP warning copy has been removed from the primary workflow |
| AC-P3-011 | UI looks recognizably close to the v0.2 mock renders within MVP scope | ✅ Done | Dashboard, app shell, Candidate Detail, Scan History, and Settings follow mock direction within MVP scope; residual mobile-width visual QA is tracked as a post-merge follow-up |
| AC-P3-012 | Tests and review are complete before merge | ✅ Done | P3-N verification and P3-O review artifact are complete; PR draft has been updated |

---

## 4. Test Tracking

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P3-001 | Backend chart/candidate API tests | API/Unit | `docker compose run --rm backend pytest tests/test_chart_data.py`; live endpoint smoke | ✅ Done | Covers chart indicator enrichment, insufficient-history warnings, and a Wilder's-smoothing RSI reference case; live `/api/symbols/AAPL/chart` returned 200 and missing symbol returned 404 |
| T-P3-002 | Scan history API/page tests | API/UI | `/api/scans`; `/scans`; `npm.cmd run build` | 🟨 In Progress | API and route smoke checks previously passed; no automated frontend route test runner exists yet |
| T-P3-003 | Settings API/page tests | API/UI | `docker compose run --rm backend pytest tests/test_display_settings.py`; `/settings`; `/api/settings/display` | ✅ Done | Secret-redaction API test passed; Settings page and display settings endpoint returned 200; API keys and database URLs are not visible |
| T-P3-004 | Manual scan flow test | Integration | `docker compose run --rm backend pytest tests/test_manual_scan_route.py`; `POST /api/scans/manual` | ✅ Done | Confirms scan trigger uses persisted symbols/bars, persists the scan, and local endpoint returned 200; also rejects non-positive `refresh_limit` and unknown `refresh_period` with 422 |
| T-P3-005 | Frontend component/build tests | Frontend | `npm.cmd run build` | ✅ Done | Production build passed; no frontend component test runner is configured in this Vite app yet |
| T-P3-006 | Backend regression suite | Regression | `docker compose run --rm backend pytest` | ✅ Done | Backend suite passed after P3-P follow-up fixes: 83 tests |
| T-P3-007 | Local smoke check | Manual | `http://localhost:5173`, `/scans`, `/settings`, `/api/health`, `/api/scans/latest`, `/api/scans`, `/api/scans/manual`, `/api/settings/display`, `/api/symbols/AAPL/chart` | ✅ Done | Browser/user smoke checks passed through latest Candidate Detail and manual scan changes; local endpoints were checked throughout Phase 3 |
| T-P3-008 | Responsive visual checks | Manual/UI | Browser viewports | ✅ Done | Horizontal table overflow, sticky table headers, mock-style Candidate Detail right rail, functional chart toolbar/timeframes/options/fullscreen toggle, and overlap fixes have user browser confirmation |
| T-P3-009 | Mock alignment visual review | Manual/UI | Compare against v0.2 mock renders | ✅ Done | Dashboard, Candidate Detail, Scan History, and Settings were aligned to mock direction within MVP scope; MVP+ controls remain deferred/disabled |
| T-P3-010 | Security/dependency checks | Review | `docker compose config --quiet`, `pip check`, `npm audit`, secret scan, `git diff --check` | ✅ Done | Compose config, backend `pip check`, npm audit, secret scan review, and diff whitespace check passed; expected local Docker/test/doc hits only |
| T-P3-011 | Market data refresh before scan | Integration | `docker compose run --rm backend pytest tests/test_manual_scan_route.py tests/test_yfinance_provider.py`; limited live smoke `POST /api/scans/manual?refresh_market_data=true&refresh_period=3mo&refresh_limit=2` | ✅ Done | Confirms yfinance refresh metadata, total-refresh-failure handling, persisted-only escape hatch, batch yfinance frame parsing, and limited live refresh+scan path |

---

## 5. Open Questions

| ID | Question | Owner | Status | Current Leaning |
| --- | --- | --- | --- | --- |
| Q-P3-001 | Which chart library should be used first? | Jesse + AI | 🟩 Resolved | Use TradingView Lightweight Charts |
| Q-P3-002 | Should candidate detail be a real route or right-side panel first? | Jesse + AI | 🟩 Resolved | Use a real route for MVP traceability; selected panel can remain on dashboard |
| Q-P3-003 | Should settings be editable or read-only first? | Jesse + AI | 🟩 Resolved | Read-only system/admin options first, plus safe UI preferences for users; MVP is single-user Jesse-only |
| Q-P3-004 | Should manual scan call Alpha Vantage in hosted demo? | Jesse + AI | 🟩 Resolved | Local/dev manual scan should default to yfinance for cost and rate-limit practicality; hosted manual scan must respect rate limits and secrets |
| Q-P3-005 | Should entry/stop/target chart lines ship in Phase 3? | Jesse + AI | 🟩 Resolved | Include if simple from existing risk/reward payload; otherwise defer to MVP+ |

---

## 6. Phase Risks

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-P3-001 | UI polish expands into MVP+ signal-dashboard scope | Medium | 🟧 Watching | Keep chart evidence and scan-review workflow first; defer sector scanner, watchlist, and AI panels |
| R-P3-002 | Chart implementation recomputes trading logic in React | High | 🟧 Watching | Backend should provide chart-ready bars and indicator values; frontend renders evidence |
| R-P3-003 | Manual scan can trigger costly/rate-limited provider calls | Medium | 🟧 Watching | Show mode clearly, rate-limit where needed, and avoid exposing provider secrets |
| R-P3-004 | Candidate visuals create false confidence | High | 🟧 Watching | Keep research-only copy, cautions, freshness, and score breakdown visible |
| R-P3-005 | Settings page exposes secrets or unsafe controls | High | 🟧 Watching | Never display API keys or database URLs; keep broker/AI controls out of MVP |
| R-P3-006 | Responsive layout breaks on tall/narrow viewports | Medium | 🟧 Watching | Preserve the previously confirmed sidebar/table behavior and test 1080x2560 |
| R-P3-007 | Mock fidelity pulls MVP+ features into Phase 3 | Medium | 🟧 Watching | Match the mock's structure and visual treatment, but keep watchlist, sector scanner, AI insight, and rich signal panels disabled, labelled, or omitted |
| R-P3-008 | yfinance MVP data is convenient but not trading-grade | Medium | 🟧 Watching | Use it pragmatically for cost-constrained MVP scanning, show freshness/source clearly, and keep provider abstraction ready for Alpha Vantage or better sources later |
| R-P3-009 | Manual scan may appear fresh while using stale persisted bars | High | 🟧 Watching | Add explicit market-data refresh step before scan, separate refresh and scan statuses in the UI, and keep stale-data warnings visible when refresh is skipped or fails |

---

## 7. Review Artifacts

| Artifact | Path |
| --- | --- |
| Implementation plan | `/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md` |
| Code/security/trading review | `/docs/phases/phase-3-dashboard-mvp/phase-3-code-security-trading-review.md` |
| Pull request draft | `/docs/phases/phase-3-dashboard-mvp/phase-3-pull-request-draft.md` |

---

## 8. Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-05-28 | Created Phase 3 dashboard MVP tracker and marked scope planning complete | Jesse + AI |
| 2026-05-28 | Clarified that Phase 3 should visually align closely with the v0.2 mock renders while preserving MVP scope | Jesse + AI |
| 2026-05-28 | Resolved Phase 3 open questions for chart library, candidate detail routing, settings scope, yfinance-first MVP scan data, hosted manual scan limits, and risk/reward chart lines | Jesse + AI |
| 2026-05-28 | Completed P3-B app shell alignment with mock-style global header, sidebar navigation/status rail, and main workspace structure | Jesse + AI |
| 2026-05-28 | Completed P3-C latest scan summary surface with scan type, universe, symbols processed, candidates found, data health, and warning visibility | Jesse + AI |
| 2026-06-01 | Completed P3-D candidate ranking table with setup/status filters, sortable rank/score/risk-reward columns, expanded review columns, visible caution counts, and filtered empty state | Jesse + AI |
| 2026-06-01 | Completed P3-E candidate detail route/page with deep-linkable candidate URLs, detail header, deterministic evidence panels, score/risk context, and explicit chart placeholder for P3-F/P3-G | Jesse + AI |
| 2026-06-01 | Completed P3-F backend chart-ready payload with OHLCV, SMA 20/50/200, RSI 14, latest candidate context, risk/reward overlay values, frontend API types, backend tests, and live endpoint smoke checks | Jesse + AI |
| 2026-06-01 | Completed P3-G frontend chart evidence with TradingView Lightweight Charts, candlesticks, volume, SMA overlays, RSI strip, chart warnings, risk estimate price lines, and local route/API smoke checks | Jesse + AI |
| 2026-06-02 | Polished P3-G chart layout with compact detail view, grouped Research Context panel, draggable RSI divider, and suppressed single-user MVP research-only warning copy | Jesse + AI |
| 2026-06-02 | Marked P3-H complete because the candidate detail page now surfaces reasons, caution flags, risk/reward estimate, setup context, and score components in one Research Context panel | Jesse + AI |
| 2026-06-02 | Completed P3-I Scan History page with `/scans` route, prior run list, selected run summary, selected run candidate table, candidate click-through, build verification, and local route/API smoke checks | Jesse + AI |
| 2026-06-02 | Completed P3-J Settings MVP with display-safe backend settings endpoint, read-only Settings page, secret-redaction test, backend regression suite, frontend build, and local route/API smoke checks | Jesse + AI |
| 2026-06-02 | Completed P3-K manual scan flow with safe persisted-bar backend endpoint, dashboard loading/success/error state, scan refresh behavior, backend test coverage, frontend build, and local endpoint smoke check | Jesse + AI |
| 2026-06-04 | Completed P3-L freshness, empty, partial, and error state handling with dashboard notices, scan-history freshness/warning notices, zero-candidate copy, filter-empty copy, Data Health refinements, and frontend build verification | Jesse + AI |
| 2026-06-04 | Added explicit P3-K.1 task for yfinance market-data refresh before manual scan so stale persisted bars are not confused with a fresh scan | Jesse + AI |
| 2026-06-04 | Completed P3-K.1 with yfinance refresh-before-scan endpoint flow, batch yfinance parsing, refresh metadata in manual scan responses, failure handling, dev refresh limit, frontend success copy, backend regression tests, frontend build, and limited live refresh smoke | Jesse + AI |
| 2026-06-04 | Started P3-M responsive polish with dynamic Top Candidates pane scrolling, sticky table headers, compact Candidate Detail evidence strip, hidden success notice on detail route, frontend build verification, and local HTTP smoke | Jesse + AI |
| 2026-06-04 | Refined Candidate Detail toward `Mock_UI_PoorToPour_01_CandidateDetail.png` by removing top Price/Relative Volume/RSI/Data Date cards, expanding chart real estate, and moving key setup/trade/reason/caution details into color-coded right-side panels | Jesse + AI |
| 2026-06-04 | Added Candidate Detail exchange badge, setup badge styling, chart toolbar tabs/timeframe controls/options/fullscreen button, chart endpoint exchange metadata, and layout changes to prevent Chart Evidence overlap with the candidate header | Jesse + AI |
| 2026-06-04 | Made Candidate Detail chart toolbar functional with timeframe-based bar slicing, volume/RSI chart options, visible bars count, and fullscreen enter/exit toggle | Jesse + AI |
| 2026-06-04 | Completed P3-P secondary review: re-ran gates (83 backend tests, 0 npm vulnerabilities, clean whitespace), switched chart RSI to Wilder's smoothing, validated manual-scan `refresh_limit`/`refresh_period`, added regression tests, and marked Phase 3 ✅ Done | Jesse + AI |
