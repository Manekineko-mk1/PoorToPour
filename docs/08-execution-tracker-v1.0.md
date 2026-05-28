# PoorToPour Execution Tracker

**Project:** PoorToPour
**Description:** From broke to pouring champagne.
**Date created:** 2026-04-29
**Last updated:** 2026-05-28
**Status:** 🟨 Phase 3 Active - Dashboard MVP

---

## 1. Current Focus

**Current phase:** Phase 3 - Dashboard MVP
**Current branch:** `feature/phase_3_dashboard_mvp`

Current objective:

Turn the Phase 2 deterministic scanner output into the first complete Dashboard MVP workflow: latest scan summary, ranked candidate review, candidate detail with chart evidence, scan history, settings, manual scan flow, and clear data-health states.

Detailed Phase 3 tracker and plan:

`/docs/phases/phase-3-dashboard-mvp/phase-3-execution-tracker.md`

`/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md`

Prior phase closeout:

Phase 1 and Phase 2 are complete, reviewed, pushed, and merged to `main`. Their detailed checklists, verification notes, reviews, and PR drafts live under `/docs/phases/`.

---

## 2. Phase Progress

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| Phase | Description | Status | Detail |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | ✅ Done | Core planning docs created |
| Phase 1 | Data foundation | ✅ Done | `/docs/phases/phase-1-data-foundation/phase-1-execution-tracker.md` |
| Phase 2 | Technical scanner MVP | ✅ Done | `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md` |
| Phase 3 | Dashboard MVP | 🟨 In Progress | `/docs/phases/phase-3-dashboard-mvp/phase-3-execution-tracker.md` |
| Phase 4 | Research context layer | ⬜ Not Started | Company profile, earnings, news headlines |
| Phase 5 | Risk and backtesting | ⬜ Not Started | Historical validation and risk calculations |
| Phase 6 | Intraday intelligence | ⬜ Not Started | Intraday scans, social/news/event context |
| Phase 7 | Paper trading | ⬜ Not Started | Simulated real-time trade tracking |
| Phase 8 | Controlled broker automation | ⬜ Not Started | Broker integration with strict guardrails |
| Phase 9 | Personal trading assistant | ⬜ Not Started | Semi/fully automated trading system under tested rules |

---

## 3. Phase Artifact Index

| Phase | Tracker | Plan | Review | PR Draft |
| --- | --- | --- | --- | --- |
| Phase 1 - Data Foundation | `/docs/phases/phase-1-data-foundation/phase-1-execution-tracker.md` | N/A | `/docs/phases/phase-1-data-foundation/phase-1-code-security-trading-review.md` | `/docs/phases/phase-1-data-foundation/phase-1-pull-request-draft.md` |
| Phase 2 - Technical Scanner | `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md` | `/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md` | `/docs/phases/phase-2-technical-scanner/phase-2-code-security-trading-review.md` | `/docs/phases/phase-2-technical-scanner/phase-2-pull-request-draft.md` |
| Phase 3 - Dashboard MVP | `/docs/phases/phase-3-dashboard-mvp/phase-3-execution-tracker.md` | `/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md` | `/docs/phases/phase-3-dashboard-mvp/phase-3-code-security-trading-review.md` | `/docs/phases/phase-3-dashboard-mvp/phase-3-pull-request-draft.md` |

---

## 4. Current Phase Acceptance Snapshot

Canonical Phase 3 acceptance criteria live in `/docs/phases/phase-3-dashboard-mvp/phase-3-execution-tracker.md`.

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
| AC-P3-011 | UI matches the v0.2 mock direction within MVP scope | ⬜ Not Started | Header/sidebar/main structure and candidate evidence take priority over MVP+ panels |
| AC-P3-012 | Tests and review are complete before merge | ⬜ Not Started | Review artifact and PR draft are updated |

---

## 5. Test Tracking Snapshot

Canonical Phase 3 test tracking lives in `/docs/phases/phase-3-dashboard-mvp/phase-3-execution-tracker.md`.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P3-001 | Backend chart/candidate API tests | API/Unit | TBD | ⬜ Not Started | Cover bars, indicators, missing symbol, and stale data behavior |
| T-P3-002 | Scan history API/page tests | API/UI | TBD | ⬜ Not Started | Cover prior runs and selected run candidates |
| T-P3-003 | Settings API/page tests | API/UI | TBD | ⬜ Not Started | Cover config display and secret redaction |
| T-P3-004 | Manual scan flow test | Integration | TBD | ⬜ Not Started | Confirm scan trigger, loading state, persistence, and refresh |
| T-P3-005 | Frontend component/build tests | Frontend | `npm.cmd run build` plus TBD | ⬜ Not Started | Add component tests if the current frontend test stack supports it cleanly |
| T-P3-006 | Backend regression suite | Regression | `docker compose run --rm backend pytest` | ⬜ Not Started | Must pass before review |
| T-P3-007 | Local smoke check | Manual | `http://localhost:5173`, `/api/health`, `/api/scans/latest` | ⬜ Not Started | Include dashboard, detail, scan history, settings, and manual scan |
| T-P3-008 | Responsive visual checks | Manual/UI | Browser viewports | ⬜ Not Started | Check desktop, tall/narrow 1080x2560, and mobile-ish widths |
| T-P3-009 | Mock alignment visual review | Manual/UI | Compare against v0.2 mock renders | ⬜ Not Started | Review Dashboard, Scan History, and Settings against the v0.2 mock references |
| T-P3-010 | Security/dependency checks | Review | `docker compose config --quiet`, `pip check`, `npm audit`, secret scan | ⬜ Not Started | Run before Phase 3 closeout |

---

## 6. Resolved Questions / Standing Clarifications

| ID | Question | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first for MVP scan data? | Jesse + AI | 🟩 Resolved | Use yfinance pragmatically for cost-constrained MVP scan data. Keep Alpha Vantage as the first real provider adapter and future stable-source candidate after scanner/strategy value is proven. |
| Q-002 | Should the MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | Jesse | 🟩 Resolved | Use S&P 500 plus Nasdaq 100. Deduplicate overlapping symbols. |
| Q-003 | Should the first dashboard be built before backtesting? | Jesse + AI | 🟩 Resolved | Build Dashboard MVP before full backtesting. |
| Q-004 | Should alerts be dashboard-only at first? | Jesse | 🟩 Resolved | Yes. Alerts should be dashboard-only before any notification channel or automation. |
| Q-005 | Should deployment be local-only for MVP? | Jesse | 🟩 Resolved | MVP development stays local Docker Compose. MVP+ and later should be designed to run on cloud. |
| Q-006 | What is the first acceptable monthly operating budget? | Jesse | 🟩 Resolved | Hosted MVP should stay under $50/month if possible, with hard review before exceeding $100/month. |
| Q-007 | Which AI features, if any, should be allowed in MVP? | Jesse + AI | 🟩 Resolved | No AI trade decisions. AI summaries are post-MVP, disabled by default, and should be reviewed again after MVP+. |

---

## 7. Decisions Log Snapshot

The canonical decision log is `/docs/09-decision-log-v1.1.md`.

| Date | Decision | Impact |
| --- | --- | --- |
| 2026-04-29 | Project name is PoorToPour | Sets repo identity and documentation tone |
| 2026-04-29 | MVP starts as long-only daily/weekly swing scanner | Keeps first build manageable and testable |
| 2026-04-29 | No automated trading in MVP | Avoids unsafe execution before validation |
| 2026-04-30 | Phase 0 planning package completed | Establishes PRD, strategy, architecture, data, dashboard, risk, cost, glossary, tracker, decision log, and AI guidelines |
| 2026-05-25 | Phase 1 local data foundation started | Adds FastAPI, React/Vite, Docker Compose, PostgreSQL, mock provider, migrations, S&P seed, yfinance bootstrap, indicators, and scanner persistence |
| 2026-05-26 | Phase 1 review completed | Code/security/trading-safety review completed and fixes applied before merge |
| 2026-05-26 | Phase-specific docs adopted | Detailed phase checklists, reviews, and PR drafts now live under `/docs/phases/<phase>/` |
| 2026-05-26 | Open MVP direction questions resolved | Alpha Vantage initially selected as real adapter; S&P 500 plus Nasdaq 100, dashboard-before-backtesting, dashboard-only alerts, local-to-cloud path, budget ceiling, and AI boundaries confirmed |
| 2026-05-28 | Phase 3 implementation choices resolved | TradingView Lightweight Charts, real candidate detail route, read-only admin settings first, yfinance-first MVP scan data, constrained hosted manual scan, and optional risk/reward chart lines confirmed |

---

## 8. Risks / Issues

Legend: `🟦 Open` | `🟧 Watching` | `✅ Closed` | `⛔ Blocked`

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-001 | Scope creep from scanner MVP into full autonomous trading too early | High | 🟧 Watching | Keep MVP focused on data, scanner, and dashboard |
| R-002 | Using unreliable or stale market data | High | 🟧 Watching | Data freshness must be shown in dashboard and required stale price data must block candidates |
| R-003 | False confidence from untested signals | High | 🟧 Watching | Explainability and backtesting required before automation |
| R-004 | Overbuilding architecture before proving scanner value | Medium | 🟧 Watching | Keep stack simple: FastAPI, React, PostgreSQL, Docker Compose |
| R-005 | Mixing research output with trade execution too early | High | 🟧 Watching | Broker integration is post-paper-trading only |
| R-006 | Choosing a market-data provider before validating practical limits | Medium | 🟧 Watching | yfinance is pragmatic for MVP scan iteration; keep provider abstraction and revisit Alpha Vantage or paid/stable sources after scanner value is proven |
| R-007 | Documentation filename drift between phase artifacts and cross-doc references | Low | 🟧 Watching | Keep active tracker references accurate |
| R-008 | Hardcoded scanner assumptions become hidden strategy rules | Medium | ✅ Closed | Risk/reward ATR buffer and target multiple are now explicit configurable defaults |
| R-009 | Relative strength proxy is mistaken for benchmark-relative strength | Medium | 🟦 Open | Current Phase 2 detector uses price leadership only; revisit SPY/QQQ-relative return once benchmark bars are available |

---

## 9. Next Steps

1. Start Phase 3 with app shell/routing and latest scan dashboard improvements.
2. Add candidate detail and chart evidence after the chart API contract is stable.
3. Keep SPY/QQQ-relative strength, watchlist, sector scanner, and AI insight panels parked in MVP+/later docs unless explicitly re-approved.

---

## 10. Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-04-29 | Created initial execution tracker with Phase 0 status and current decisions | Jesse + AI |
| 2026-04-30 | Completed Phase 0 planning docs and moved Phase 1 data foundation into active focus | Jesse + AI |
| 2026-05-25 | Added Phase 1 local FastAPI/React/Docker/PostgreSQL scaffold, mock provider, persisted data, S&P seed, yfinance bootstrap, indicators, and scanner persistence | Jesse + AI |
| 2026-05-26 | Added first deterministic bootstrap trend/momentum scanner and persisted generated output | Jesse + AI |
| 2026-05-26 | Completed Phase 1 code/security/trading-safety review and merged Phase 1 to `main` | Jesse + AI |
| 2026-05-26 | Reorganized phase-specific docs under `/docs/phases/` and made this tracker high-level for Phase 2 onward | Jesse + AI |
| 2026-05-26 | Resolved standing MVP direction questions and linked them to decision-log updates | Jesse + AI |
| 2026-05-26 | Added Phase 2 implementation plan and aligned Phase 2 acceptance/test snapshots with provider, universe, and scanner-safety decisions | Jesse + AI |
| 2026-05-26 | Started Phase 2 with Nasdaq 100 seed, combined MVP universe seeder, dedupe tests, and local DB verification for 516 unique symbols | Jesse + AI |
| 2026-05-26 | Added Alpha Vantage provider adapter, ingest command, env-only config, fixture tests, and Compose env wiring | Jesse + AI |
| 2026-05-26 | Expanded IndicatorService with breakout-ready highs, prior highs, ATR, range-position fields, and tests | Jesse + AI |
| 2026-05-26 | Added deterministic breakout detector returning conservative Watch/Blocked candidates with reasons, caution flags, and tests | Jesse + AI |
| 2026-05-26 | Added breakout score components, caution penalties, risk/reward scaffold, and focused tests | Jesse + AI |
| 2026-05-26 | Added shared candidate status rules and wired breakout detector through the conservative status gate | Jesse + AI |
| 2026-05-26 | Made breakout risk/reward ATR buffer and target multiple configurable through app settings/env defaults | Jesse + AI |
| 2026-05-27 | Added pullback continuation and relative strength leader detectors with scoring, risk/reward, cautions, and tests | Jesse + AI |
| 2026-05-27 | Added Phase 2 technical scanner run composition and persistence command using existing scan tables | Jesse + AI |
| 2026-05-27 | Added focused frontend scanner evidence display for selected generated candidates | Jesse + AI |
| 2026-05-27 | Completed Phase 2 code/security/trading-safety review and fixed stale price-data gating in setup detectors | Jesse + AI |
| 2026-05-27 | Completed coding-standards follow-up for shared symbol resolution, repeated risk/reward warning text, and relative-strength detector complexity | Jesse + AI |
| 2026-05-27 | Re-ran Phase 2 review against updated guidelines and added shared provider daily-bar validation | Jesse + AI |
| 2026-05-28 | Started Phase 3 dashboard MVP with phase-specific tracker, implementation plan, and PR draft scaffold | Jesse + AI |
| 2026-05-28 | Resolved Phase 3 open questions and updated MVP scan data direction to yfinance-first with Alpha Vantage retained as future stable-source candidate | Jesse + AI |
