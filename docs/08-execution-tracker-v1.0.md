# PoorToPour Execution Tracker

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-05-26
**Status:** Phase 2 Active - Technical Scanner MVP

---

## 1. Current Focus

**Current phase:** Phase 2 - Technical Scanner MVP
**Current branch:** `feature/phase_2_technical_scanner`

Current objective:

Build on the Phase 1 data foundation by expanding deterministic scanner logic: setup detectors, score breakdowns, risk/reward estimates, candidate status rules, tests, and frontend inspection hooks.

Detailed Phase 2 tracker:

`/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`

Phase 1 closeout:

Phase 1 is complete, reviewed, pushed, and merged to `main`. Its detailed checklist, verification notes, review, and PR draft now live under `/docs/phases/phase-1-data-foundation/`.

---

## 2. Phase Progress

Legend: `Not Started` | `In Progress` | `Done` | `Blocked`

| Phase | Description | Status | Detail |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | Done | Core planning docs created |
| Phase 1 | Data foundation | Done | `/docs/phases/phase-1-data-foundation/phase-1-execution-tracker.md` |
| Phase 2 | Technical scanner MVP | In Progress | `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md` |
| Phase 3 | Dashboard MVP | Not Started | Ranked candidates, chart views, score breakdown |
| Phase 4 | Research context layer | Not Started | Company profile, earnings, news headlines |
| Phase 5 | Risk and backtesting | Not Started | Historical validation and risk calculations |
| Phase 6 | Intraday intelligence | Not Started | Intraday scans, social/news/event context |
| Phase 7 | Paper trading | Not Started | Simulated real-time trade tracking |
| Phase 8 | Controlled broker automation | Not Started | Broker integration with strict guardrails |
| Phase 9 | Personal trading assistant | Not Started | Semi/fully automated trading system under tested rules |

---

## 3. Phase Artifact Index

| Phase | Tracker | Review | PR Draft |
| --- | --- | --- | --- |
| Phase 1 - Data Foundation | `/docs/phases/phase-1-data-foundation/phase-1-execution-tracker.md` | `/docs/phases/phase-1-data-foundation/phase-1-code-security-trading-review.md` | `/docs/phases/phase-1-data-foundation/phase-1-pull-request-draft.md` |
| Phase 2 - Technical Scanner | `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md` | `/docs/phases/phase-2-technical-scanner/phase-2-code-security-trading-review.md` | `/docs/phases/phase-2-technical-scanner/phase-2-pull-request-draft.md` |

---

## 4. Current Phase Acceptance Snapshot

Canonical Phase 2 acceptance criteria live in `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`.

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P2-001 | Scanner setup families are documented for implementation | Not Started | Breakout, pullback continuation, relative strength leader |
| AC-P2-002 | Scanner rules are deterministic and explainable | Not Started | No AI-generated trade decisions |
| AC-P2-003 | Scanner output includes reasons and score breakdown | Not Started | Candidate detail must show why it appeared |
| AC-P2-004 | Scanner output includes caution flags | Not Started | Missing data and weak confirmations should be visible |
| AC-P2-005 | Risk/reward estimate exists before `Actionable` status | Not Started | Trading-safety requirement |
| AC-P2-006 | Generated candidates persist to database | Not Started | Uses Phase 1 `scan_runs` and `scan_candidates` |
| AC-P2-007 | Tests cover indicator/scanner behavior | Not Started | Unit tests for setup detectors and scoring |
| AC-P2-008 | Phase 2 review is complete before merge | Not Started | Dedicated review artifact required |

---

## 5. Test Tracking Snapshot

Canonical Phase 2 test tracking lives in `/docs/phases/phase-2-technical-scanner/phase-2-execution-tracker.md`.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P2-001 | Setup detector tests | Unit | TBD | Not Started | One test group per setup family |
| T-P2-002 | Score breakdown tests | Unit | TBD | Not Started | Verify component contributions and thresholds |
| T-P2-003 | Risk/reward estimate tests | Unit | TBD | Not Started | Required before `Actionable` status |
| T-P2-004 | Scanner persistence tests | Unit/Integration | TBD | Not Started | Verify generated scan writes cleanly |
| T-P2-005 | Backend test suite | Regression | `docker compose run --rm backend pytest` | Not Started | Must pass before Phase 2 review |
| T-P2-006 | Frontend build | Build | `npm.cmd run build` | Not Started | Must pass before Phase 2 review |

---

## 6. Resolved Questions / Standing Clarifications

| ID | Question | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first for trading-grade MVP data? | Jesse + AI | Resolved | Use Alpha Vantage as the first real provider adapter. Keep yfinance as a Phase 1/bootstrap development source only. |
| Q-002 | Should the MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | Jesse | Resolved | Use S&P 500 plus Nasdaq 100. Deduplicate overlapping symbols. |
| Q-003 | Should the first dashboard be built before backtesting? | Jesse + AI | Resolved | Build Dashboard MVP before full backtesting. |
| Q-004 | Should alerts be dashboard-only at first? | Jesse | Resolved | Yes. Alerts should be dashboard-only before any notification channel or automation. |
| Q-005 | Should deployment be local-only for MVP? | Jesse | Resolved | MVP development stays local Docker Compose. MVP+ and later should be designed to run on cloud. |
| Q-006 | What is the first acceptable monthly operating budget? | Jesse | Resolved | Hosted MVP should stay under $50/month if possible, with hard review before exceeding $100/month. |
| Q-007 | Which AI features, if any, should be allowed in MVP? | Jesse + AI | Resolved | No AI trade decisions. AI summaries are post-MVP, disabled by default, and should be reviewed again after MVP+. |

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

Legend: `Open` | `Watching` | `Closed` | `Blocked`

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-001 | Scope creep from scanner MVP into full autonomous trading too early | High | Watching | Keep MVP focused on data, scanner, and dashboard |
| R-002 | Using unreliable or stale market data | High | Watching | Data freshness must be shown in dashboard and required stale price data must block candidates |
| R-003 | False confidence from untested signals | High | Watching | Explainability and backtesting required before automation |
| R-004 | Overbuilding architecture before proving scanner value | Medium | Watching | Keep stack simple: FastAPI, React, PostgreSQL, Docker Compose |
| R-005 | Mixing research output with trade execution too early | High | Watching | Broker integration is post-paper-trading only |
| R-006 | Choosing a market-data provider before validating practical limits | Medium | Watching | Prototype with sample symbols before committing to one provider |
| R-007 | Documentation filename drift between phase artifacts and cross-doc references | Low | Watching | Keep active tracker references accurate |

---

## 9. Next Steps

1. Confirm Phase 2 scanner scope and first setup detector order.
2. Implement the first deterministic setup detector, likely breakout.
3. Add score breakdown and risk/reward scaffolding before allowing `Actionable` status.
4. Keep backend tests and frontend build green as scanner behavior expands.

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
