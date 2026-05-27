# PoorToPour Execution Tracker

**Project:** PoorToPour
**Description:** From broke to pouring champagne.
**Date created:** 2026-04-29
**Last updated:** 2026-05-27
**Status:** ✅ Phase 2 Review Complete - Technical Scanner MVP

---

## 1. Current Focus

**Current phase:** Phase 2 - Technical Scanner MVP
**Current branch:** `feature/phase_2_technical_scanner`

Current objective:

Build on the Phase 1 data foundation by expanding deterministic scanner logic: setup detectors, score breakdowns, risk/reward estimates, candidate status rules, tests, and frontend inspection hooks.

Detailed Phase 2 tracker and plan:

`/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`

`/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md`

Phase 1 closeout:

Phase 1 is complete, reviewed, pushed, and merged to `main`. Its detailed checklist, verification notes, review, and PR draft now live under `/docs/phases/phase-1-data-foundation/`.

---

## 2. Phase Progress

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| Phase | Description | Status | Detail |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | ✅ Done | Core planning docs created |
| Phase 1 | Data foundation | ✅ Done | `/docs/phases/phase-1-data-foundation/phase-1-execution-tracker.md` |
| Phase 2 | Technical scanner MVP | ✅ Review Complete | `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md` |
| Phase 3 | Dashboard MVP | ⬜ Not Started | Ranked candidates, chart views, score breakdown |
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

---

## 4. Current Phase Acceptance Snapshot

Canonical Phase 2 acceptance criteria live in `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`.

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P2-001 | Scanner setup families are documented for implementation | ✅ Done | Breakout first, then pullback continuation and relative strength leader |
| AC-P2-002 | Scanner rules are deterministic and explainable | ✅ Done | Breakout, pullback continuation, and relative strength leader detectors use explicit rules only |
| AC-P2-003 | Scanner output includes reasons and score breakdown | ✅ Done | Scanner candidates include reasons and structured score breakdowns visible in the frontend evidence panel |
| AC-P2-004 | Scanner output includes caution flags | ✅ Done | Detectors emit missing-data, weak-confirmation, and setup-specific caution flags |
| AC-P2-005 | Risk/reward estimate exists before `Actionable` status | ✅ Done | Breakout risk/reward scaffold, configurable assumptions, and shared status rules exist |
| AC-P2-006 | Generated candidates persist to database | ✅ Done | `run_technical_scan` persisted Phase 2 candidates to existing scan tables |
| AC-P2-007 | Alpha Vantage adapter does not expose secrets | ✅ Done | API key is read from env/config; `.env.example` contains only an empty placeholder |
| AC-P2-008 | S&P 500 plus Nasdaq 100 universe can be seeded without duplicates | ✅ Done | `seed_mvp_universe` imports 516 unique symbols and preserves S&P metadata for overlaps |
| AC-P2-009 | Tests cover indicator/scanner/provider behavior | ✅ Done | Unit tests cover provider mapping, indicators, setup detectors, scoring, risk/reward, and status rules |
| AC-P2-010 | Phase 2 review is complete before merge | ✅ Done | Code/security/trading review completed on 2026-05-27 |

---

## 5. Test Tracking Snapshot

Canonical Phase 2 test tracking lives in `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P2-001 | Nasdaq 100 seed/import tests | Unit/Data | `backend/tests/test_sp500_seed.py` | ✅ Pass | Verifies required columns, symbol normalization, and dedupe behavior |
| T-P2-002 | Alpha Vantage adapter mapping tests | Unit | `backend/tests/test_alpha_vantage_provider.py` | ✅ Pass | Uses fixtures, not live API calls; malformed dates/OHLC rows are skipped |
| T-P2-003 | Indicator expansion tests | Unit | `backend/tests/test_indicator_service.py` | ✅ Pass | Verifies breakout inputs, ATR, range position, prior highs, and insufficient-history warnings |
| T-P2-004 | Breakout detector tests | Unit | `backend/tests/test_breakout_detector.py` | ✅ Pass | Covers confirmed, near, blocked, and weak non-breakout cases |
| T-P2-004A | Pullback continuation detector tests | Unit | `backend/tests/test_pullback_detector.py` | ✅ Pass | Covers confirmed, developing, blocked, and broken-trend cases |
| T-P2-004B | Relative strength leader detector tests | Unit | `backend/tests/test_relative_strength_detector.py` | ✅ Pass | Covers confirmed leader, shorter-term proxy, blocked, and lagging cases |
| T-P2-005 | Score breakdown tests | Unit | `backend/tests/test_scoring.py` | ✅ Pass | Verifies component contributions, caution penalty, and score clamping |
| T-P2-006 | Risk/reward estimate tests | Unit | `backend/tests/test_risk_reward.py` | ✅ Pass | Verifies ATR-buffered invalidation, 2R target, missing inputs, and invalid risk |
| T-P2-006A | Risk/reward config tests | Unit | `backend/tests/test_scanner_config.py` | ✅ Pass | Verifies configurable ATR buffer and target multiple defaults and validation |
| T-P2-007 | Candidate status rule tests | Unit | `backend/tests/test_status_rules.py` | ✅ Pass | Confirms conservative `Actionable`, `Watch`, `Avoid`, and `Blocked` behavior |
| T-P2-008 | Scanner persistence tests | Unit/Integration | `backend/tests/test_technical_scanner.py`; `python -m app.scripts.run_technical_scan --limit 10` | ✅ Pass | Unit tests cover composed scan output; local command persisted 10-symbol scan with 2 candidates |
| T-P2-009 | Backend test suite | Regression | `docker compose run --rm backend pytest` | ✅ Pass | 69 passed after review freshness, symbol-resolution, and provider-validation coverage |
| T-P2-011 | Technical scanner command | Manual/Integration | `docker compose run --rm backend python -m app.scripts.run_technical_scan --limit 10` | ✅ Pass | Persisted `technical_scan_20260527_044237_959bb63a` with 2 candidates |
| T-P2-010 | Frontend build | Build | `npm.cmd run build` | ✅ Pass | Build passed after focused scanner evidence display |
| T-P2-012 | Frontend local smoke check | Manual | `Invoke-WebRequest http://localhost:5173`; `GET /api/scans/latest` | ✅ Pass | Frontend returned 200; latest scan returned `Technical Scanner MVP` with 2 candidates |
| T-P2-013 | Review security/dependency checks | Review | `docker compose config --quiet`; `pip check`; `npm audit`; secret scan | ✅ Pass | No real API key found in tracked files; dependency checks passed |

---

## 6. Resolved Questions / Standing Clarifications

| ID | Question | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first for trading-grade MVP data? | Jesse + AI | 🟩 Resolved | Use Alpha Vantage as the first real provider adapter. Keep yfinance as a Phase 1/bootstrap development source only. |
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
| 2026-05-26 | Open MVP direction questions resolved | Alpha Vantage, S&P 500 plus Nasdaq 100, dashboard-before-backtesting, dashboard-only alerts, local-to-cloud path, budget ceiling, and AI boundaries confirmed |

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
| R-006 | Choosing a market-data provider before validating practical limits | Medium | 🟧 Watching | Prototype with sample symbols before committing to one provider |
| R-007 | Documentation filename drift between phase artifacts and cross-doc references | Low | 🟧 Watching | Keep active tracker references accurate |
| R-008 | Hardcoded scanner assumptions become hidden strategy rules | Medium | ✅ Closed | Risk/reward ATR buffer and target multiple are now explicit configurable defaults |
| R-009 | Relative strength proxy is mistaken for benchmark-relative strength | Medium | 🟦 Open | Current Phase 2 detector uses price leadership only; revisit SPY/QQQ-relative return once benchmark bars are available |

---

## 9. Next Steps

1. Review the Phase 2 PR draft and code/security/trading review before opening or finalizing the PR.
2. Revisit true SPY/QQQ-relative strength after benchmark bars are available.
3. Use Phase 3 to turn scanner output into the Dashboard MVP, including candidate visual evidence.

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
