# Phase 3 Execution Tracker: Dashboard MVP

**Project:** PoorToPour
**Phase:** Phase 3 - Dashboard MVP
**Status:** 🟨 In Progress
**Branch:** `feature/phase_3_dashboard_mvp`
**Last updated:** 2026-05-28

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
| P3-D | Upgrade candidate ranking table | ⬜ Not Started | Table supports score-first ranking, candidate selection/open detail, setup/status filters, sortable key columns, visible cautions, responsive overflow, and mock-aligned density |
| P3-E | Add candidate detail route/page | ⬜ Not Started | Clicking a candidate opens a detail view with candidate header, chart, explanation, score, risk/reward, and context panels |
| P3-F | Add chart data API and chart-ready payloads | ⬜ Not Started | Backend exposes selected symbol bars plus indicators needed by the frontend chart without recomputing indicators in React |
| P3-G | Add candidate chart evidence | ⬜ Not Started | Candidate detail shows mock-aligned candlestick chart, volume bars, SMA 20/50/200, RSI, and basic risk/entry/invalidation/target overlays if simple |
| P3-H | Add explanation, score, caution, and risk panels | ⬜ Not Started | Detail page surfaces deterministic reasons, caution flags, score breakdown, and research-only risk/reward copy |
| P3-I | Add scan history page | ⬜ Not Started | Scan History route follows v0.2 mock direction and shows prior scan runs, statuses, candidate counts, data dates, and selected scan candidates |
| P3-J | Add settings page MVP | ⬜ Not Started | Settings route follows v0.2 mock direction, shows read-only system/admin config, safe user preferences, setup/config display, and never exposes secrets |
| P3-K | Wire manual scan action safely | ⬜ Not Started | Manual scan button triggers a local/dev yfinance-backed scan flow or clearly labelled hosted fallback, shows loading/error/success states, and refreshes latest output |
| P3-L | Add freshness, empty, partial, and error states | ⬜ Not Started | Dashboard and detail pages clearly show stale/missing/failed/partial scan states |
| P3-M | Add frontend accessibility and responsive polish | ⬜ Not Started | Keyboard navigation, color-not-only status labels, contrast, and tall/narrow viewport checks pass |
| P3-N | Add tests and build verification | ⬜ Not Started | Backend API tests, frontend component tests where practical, backend suite, and frontend build pass |
| P3-O | Phase 3 review checkpoint | ⬜ Not Started | Code, security, trading-safety, UX, and test review completed in `phase-3-code-security-trading-review.md` |

---

## 3. Acceptance Criteria

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P3-001 | Dashboard Home shows latest scan summary and data health | ⬜ Not Started | Must not hide stale, missing, failed, or partial states |
| AC-P3-002 | Dashboard Home shows ranked candidates from persisted scanner output | ⬜ Not Started | Sorted by score by default, with setup/status context |
| AC-P3-003 | Candidate table supports practical scan review | ⬜ Not Started | Filtering, sorting, visible cautions, and click-through detail |
| AC-P3-004 | Candidate Detail page exists | ⬜ Not Started | Dedicated route or durable view state is acceptable if UX is clear |
| AC-P3-005 | Candidate Detail shows chart evidence | ⬜ Not Started | Candles, volume, SMA 20/50/200, RSI, and optional research estimate lines |
| AC-P3-006 | Candidate Detail shows deterministic explanation | ⬜ Not Started | Reasons, cautions, score components, and risk/reward fields are visible |
| AC-P3-007 | Scan History page exists | ⬜ Not Started | Prior runs are inspectable and traceable |
| AC-P3-008 | Settings page exists for MVP config visibility | ⬜ Not Started | System/admin options are read-only first; safe user preferences may be editable |
| AC-P3-009 | Manual scan is usable from the dashboard | ⬜ Not Started | Must show progress and failure clearly |
| AC-P3-010 | Frontend remains research-only and not trade-instructional | ⬜ Not Started | Copy and visual hierarchy avoid "buy/sell" implication |
| AC-P3-011 | UI looks recognizably close to the v0.2 mock renders within MVP scope | ⬜ Not Started | Match layout hierarchy, dark style, density, header/sidebar/main structure, cards, tables, chart evidence, and branding; do not implement MVP+ function just because it appears in a mock |
| AC-P3-012 | Tests and review are complete before merge | ⬜ Not Started | Review artifact and PR draft are updated |

---

## 4. Test Tracking

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P3-001 | Backend chart/candidate API tests | API/Unit | TBD | ⬜ Not Started | Cover bars, indicators, missing symbol, and stale data behavior |
| T-P3-002 | Scan history API/page tests | API/UI | TBD | ⬜ Not Started | Cover prior runs and selected run candidates |
| T-P3-003 | Settings API/page tests | API/UI | TBD | ⬜ Not Started | Cover config display and secret redaction |
| T-P3-004 | Manual scan flow test | Integration | TBD | ⬜ Not Started | Confirm scan trigger, loading state, persistence, and refresh |
| T-P3-005 | Frontend component/build tests | Frontend | `npm.cmd run build` plus TBD | 🟨 In Progress | Build passed for P3-B and P3-C UI updates; add component tests if the current frontend test stack supports it cleanly |
| T-P3-006 | Backend regression suite | Regression | `docker compose run --rm backend pytest` | ⬜ Not Started | Must pass before review |
| T-P3-007 | Local smoke check | Manual | `http://localhost:5173`, `/api/health`, `/api/scans/latest` | 🟨 In Progress | Frontend and latest scan endpoint returned 200 after P3-C; complete full route/manual-scan smoke later |
| T-P3-008 | Responsive visual checks | Manual/UI | Browser viewports | ⬜ Not Started | Check desktop, tall/narrow 1080x2560, and mobile-ish widths |
| T-P3-009 | Mock alignment visual review | Manual/UI | Compare against v0.2 mock renders | ⬜ Not Started | Review Dashboard, Scan History, and Settings against the v0.2 mock references |
| T-P3-010 | Security/dependency checks | Review | `docker compose config --quiet`, `pip check`, `npm audit`, secret scan | ⬜ Not Started | Run before Phase 3 closeout |

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
