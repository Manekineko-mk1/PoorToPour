# PoorToPour Execution Tracker

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-05-05  
**Status:** 🟨 Phase 1 Active — Data foundation started

---

## 1. Current Focus

**Current phase:** Phase 1 - Data Foundation

Current objective:

Begin the first engineering phase by creating a local development skeleton, establishing backend/frontend/Docker structure, adding a versioned S&P 500 seed-data path, defining provider interfaces, and preparing for small Tier 1 provider experiments before full OHLCV ingestion.

Phase 1 should stay local-first, deterministic, and provider-flexible. No broker automation, AI trade decisions, intraday scanning, or post-MVP context sources belong in this phase.

---

## 2. Phase Progress

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| Phase | Description | Status | Notes |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | ✅ Done | Main planning docs created: project plan, PRD, strategy, glossary, architecture, data sources, dashboard design, risk/backtesting, cost/ops, tracker, decision log, AI guidelines |
| Phase 1 | Data foundation | 🟨 In Progress | Active focus: local dev skeleton, Docker/Postgres baseline, S&P 500 seed file, provider interfaces, first OHLCV provider experiment |
| Phase 2 | Technical scanner MVP | ⬜ Not Started | Indicators, setup detection, scoring |
| Phase 3 | Dashboard MVP | ⬜ Not Started | Ranked candidates, chart views, score breakdown |
| Phase 4 | Research context layer | ⬜ Not Started | Company profile, earnings, news headlines |
| Phase 5 | Risk and backtesting | ⬜ Not Started | Historical validation and risk calculations |
| Phase 6 | Intraday intelligence | ⬜ Not Started | Intraday scans, social/news/event context |
| Phase 7 | Paper trading | ⬜ Not Started | Simulated real-time trade tracking |
| Phase 8 | Controlled broker automation | ⬜ Not Started | Broker integration with strict guardrails |
| Phase 9 | Personal trading assistant | ⬜ Not Started | Semi/fully automated trading system under tested rules |

---

## 3. Active Tasks

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| ID | Task | Status | Owner | Notes |
| --- | --- | --- | --- | --- |
| P0-001 | Create GitHub repository | ✅ Done | Jesse | Repo created as PoorToPour |
| P0-002 | Create project plan | ✅ Done | Jesse + AI | Saved as `/docs/00-project-plan-v0.3.md` |
| P0-003 | Create execution tracker | ✅ Done | Jesse + AI | Saved as `/docs/08-execution-tracker-v1.0.md` |
| P0-004 | Create decision log | ✅ Done | Jesse + AI | Saved as `/docs/09-decision-log-v1.1.md` |
| P0-005 | Create AI working guidelines | ✅ Done | Jesse + AI | Saved as `/docs/10-ai-working-guidelines.md` |
| P0-006 | Create product requirements document | ✅ Done | Jesse + AI | Saved as `/docs/01-product-requirements.md` |
| P0-007 | Create cost and operations document | ✅ Done | Jesse + AI | Saved as `/docs/07-cost-and-operations.md` |
| P0-008 | Create trading strategy requirements document | ✅ Done | Jesse + AI | Saved as `/docs/02-trading-strategy-requirements.md` |
| P0-009 | Create trading concepts glossary | ✅ Done | Jesse + AI | Saved as `/docs/02a-trading-concepts-glossary.md` |
| P0-010 | Create technical architecture document | ✅ Done | Jesse + AI | Saved as `/docs/03-technical-architecture-v0.2.md` |
| P0-011 | Create data sources document | ✅ Done | Jesse + AI | Saved as `/docs/04-data-sources-v0.2.md` |
| P0-012 | Create dashboard design document | ✅ Done | Jesse + AI | Saved as `/docs/05-dashboard-design.md` |
| P0-013 | Create risk and backtesting document | ✅ Done | Jesse + AI | Saved as `/docs/06-risk-and-backtesting.md` |
| P1-001 | Create local development skeleton | 🟨 In Progress | Jesse + AI | Next work item: backend/frontend folders, Docker Compose, env example, README run notes |
| P1-002 | Create backend FastAPI baseline | ⬜ Not Started | Jesse + AI | Health endpoint, app config module, test harness |
| P1-003 | Create frontend React + TypeScript baseline | ⬜ Not Started | Jesse + AI | Vite app shell matching future dashboard direction |
| P1-004 | Add local PostgreSQL Docker service | ⬜ Not Started | Jesse + AI | Initial database service only; migrations can follow |
| P1-005 | Add versioned S&P 500 seed file | ⬜ Not Started | Jesse + AI | Local universe seed for MVP scans |
| P1-006 | Define normalized market-data/provider models | ⬜ Not Started | Jesse + AI | DTOs for symbols, daily bars, profiles, earnings, provider call status |
| P1-007 | Define Tier 1 provider interfaces | ⬜ Not Started | Jesse + AI | Provider abstraction before vendor-specific adapter |
| P1-008 | Prototype first provider with sample symbols | ⬜ Not Started | Jesse + AI | Validate response shape, adjusted data, limits, error behavior |
| P1-009 | Ingest and store daily OHLCV sample data | ⬜ Not Started | Jesse + AI | First real data foundation milestone |

---

## 4. Current Phase Acceptance Criteria

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Pass` | `⛔ Blocked`

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P0-001 | Project vision is documented | ✅ Pass | Covered in `/docs/00-project-plan-v0.3.md` |
| AC-P0-002 | MVP scope is documented | ✅ Pass | MVP defaults agreed |
| AC-P0-003 | Non-goals are documented | ✅ Pass | Automated trading excluded from MVP |
| AC-P0-004 | High-level product phases are documented | ✅ Pass | Roadmap lives in project plan |
| AC-P0-005 | Execution tracking process is documented | ✅ Pass | This file |
| AC-P0-006 | Decision logging process is documented | ✅ Pass | `/docs/09-decision-log-v1.1.md` |
| AC-P0-007 | AI working process is documented | ✅ Pass | `/docs/10-ai-working-guidelines.md` |
| AC-P0-008 | Product requirements are documented | ✅ Pass | `/docs/01-product-requirements.md` created |
| AC-P0-009 | Cost and operations requirements are documented | ✅ Pass | `/docs/07-cost-and-operations.md` created |
| AC-P0-010 | Trading strategy requirements are documented | ✅ Pass | `/docs/02-trading-strategy-requirements.md` created |
| AC-P0-011 | Trading concepts glossary is documented | ✅ Pass | `/docs/02a-trading-concepts-glossary.md` created |
| AC-P0-012 | Technical architecture is documented | ✅ Pass | `/docs/03-technical-architecture-v0.2.md` created |
| AC-P0-013 | Data sources are documented | ✅ Pass | `/docs/04-data-sources-v0.2.md` created |
| AC-P0-014 | Dashboard design is documented | ✅ Pass | `/docs/05-dashboard-design.md` created |
| AC-P0-015 | Risk and backtesting are documented | ✅ Pass | `/docs/06-risk-and-backtesting.md` created |
| AC-P0-016 | Phase 0 planning package is complete | ✅ Pass | Ready to move into Phase 1 data foundation |
| AC-P1-001 | Local development skeleton exists | 🟨 In Progress | Backend/frontend/Docker structure is the active first implementation work item |
| AC-P1-002 | S&P 500 seed file exists | ⬜ Not Started | Versioned local seed for MVP universe |
| AC-P1-003 | Tier 1 provider interface exists | ⬜ Not Started | Provider-backed MVP data source only |
| AC-P1-004 | Tier 1 provider prototype is tested with sample symbols | ⬜ Not Started | Validate response shape, limits, adjusted data, and errors |
| AC-P1-005 | Daily OHLCV can be ingested and stored | ⬜ Not Started | First real data foundation milestone |

---

## 5. Test Tracking

Testing begins with implementation. Use this section once code exists.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Backend health endpoint smoke test | Unit/API | TBD | ⬜ Not Started | Add with backend FastAPI baseline |
| T-002 | Backend provider model validation tests | Unit | TBD | ⬜ Not Started | Add with normalized DTOs/provider interfaces |
| T-003 | Frontend app shell smoke test | Unit | TBD | ⬜ Not Started | Add with frontend baseline |
| T-004 | Docker Compose startup check | Integration | TBD | ⬜ Not Started | Add after backend/frontend/Postgres services exist |
| T-005 | Sample OHLCV ingestion test | Integration | TBD | ⬜ Not Started | Add after provider prototype and database storage exist |

---

## 6. Open Questions / Clarifications

| ID | Question | Owner | Status | Blocker | Notes |
| --- | --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first? | Jesse + AI | 🟨 Partially Resolved | No | MVP will use Tier 1 provider-backed data only. Specific provider remains TBD; likely prototype FMP-style provider first and compare practical limits before final selection. |
| Q-002 | Should the MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | Jesse | ⬜ Open | No | Current default: S&P 500 only |
| Q-003 | Should the first dashboard be built before backtesting? | Jesse + AI | ⬜ Open | No | Current default: dashboard MVP before full backtesting |
| Q-004 | Should alerts be dashboard-only at first? | Jesse | ⬜ Open | No | Current default: dashboard-only |
| Q-005 | Should deployment be local-only for MVP? | Jesse | 🟨 Partially Resolved | No | Current default: local Docker Compose for development and MVP validation |
| Q-006 | What is the first acceptable monthly operating budget? | Jesse | ⬜ Open | No | Current recommendation: hosted MVP under $50/month if possible, hard review before exceeding $100/month |
| Q-007 | Which AI features, if any, should be allowed in MVP? | Jesse + AI | 🟨 Partially Resolved | No | Current default: none for trade decisions; AI summaries are post-MVP and disabled by default |

---

## 7. Decisions Log Snapshot

The canonical decision log is `/docs/09-decision-log-v1.1.md`.

| Date | Decision | Impact |
| --- | --- | --- |
| 2026-04-29 | Project name is PoorToPour | Sets repo identity and documentation tone |
| 2026-04-29 | Roadmap stays inside `/docs/00-project-plan-v0.3.md` | Avoids duplicate roadmap docs |
| 2026-04-29 | Add execution tracker | Creates living work tracker |
| 2026-04-29 | Add decision log | Creates durable decision memory |
| 2026-04-29 | Add AI working guidelines | Creates future-session AI instructions |
| 2026-04-29 | MVP starts as long-only daily/weekly swing scanner | Keeps first build manageable and testable |
| 2026-04-29 | No automated trading in MVP | Avoids unsafe execution before validation |
| 2026-04-30 | Create product requirements | Defines MVP product workflows and scope |
| 2026-04-30 | Create cost and operations requirements | Defines cost targets, operating modes, hosting/data/AI controls |
| 2026-04-30 | Create trading strategy requirements | Defines MVP setup families, indicators, scoring, risk/reward, and validation requirements |
| 2026-04-30 | Create trading concepts glossary | Adds beginner-friendly explanations of trading concepts used by the strategy document |
| 2026-04-30 | Create technical architecture | Defines MVP system architecture, modules, data flow, jobs, APIs, database boundaries, and future automation path |
| 2026-04-30 | Create data sources document | Defines MVP data needs, provider abstraction, freshness rules, provider candidates, and data-quality controls |
| 2026-04-30 | Create dashboard design | Defines MVP dashboard screens, candidate review flow, chart requirements, score/risk display, and UI states |
| 2026-04-30 | Create risk and backtesting requirements | Defines risk model, caution flags, backtesting metrics, paper-trading gates, and automation prerequisites |

---

## 8. Risks / Issues

Legend: `⬜ Open` | `🟨 Watching` | `✅ Closed` | `⛔ Blocked`

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-001 | Scope creep from scanner MVP into full autonomous trading too early | High | 🟨 Watching | Keep MVP focused on data, scanner, and dashboard |
| R-002 | Using unreliable or stale market data | High | 🟨 Watching | Data freshness must be shown in dashboard and required stale price data must block candidates |
| R-003 | False confidence from untested signals | High | 🟨 Watching | Explainability and backtesting required before automation |
| R-004 | Overbuilding architecture before proving scanner value | Medium | 🟨 Watching | Keep stack simple: FastAPI, React, PostgreSQL, Docker Compose |
| R-005 | Mixing research output with trade execution too early | High | 🟨 Watching | Broker integration is post-paper-trading only |
| R-006 | Choosing a market-data provider before validating practical limits | Medium | 🟨 Watching | Prototype with sample symbols before committing to one provider |
| R-007 | Documentation filename drift between versioned docs and unversioned references | Low | 🟨 Watching | Keep active tracker references accurate; broader doc link cleanup can be a separate task |

---

## 9. Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-04-29 | Created initial execution tracker with Phase 0 status and current decisions | Jesse + AI |
| 2026-04-30 | Marked product requirements complete and added cost/operations as next active document | Jesse + AI |
| 2026-04-30 | Marked cost/operations complete and set trading strategy requirements as next recommended document | Jesse + AI |
| 2026-04-30 | Marked trading strategy requirements complete and set technical architecture as next recommended document | Jesse + AI |
| 2026-04-30 | Added trading glossary to support strategy review and learning | Jesse + AI |
| 2026-04-30 | Marked technical architecture complete and set data sources as next recommended document | Jesse + AI |
| 2026-04-30 | Marked data sources complete and set dashboard design as next recommended document | Jesse + AI |
| 2026-04-30 | Marked dashboard design complete and set risk/backtesting as next recommended document | Jesse + AI |
| 2026-04-30 | Marked risk/backtesting complete; Phase 0 planning docs are now broadly complete | Jesse + AI |
| 2026-04-30 | Updated Phase 0 as complete, moved Phase 1 data foundation into active focus, and clarified Q-001 Tier 1 MVP data-provider decision | Jesse + AI |
| 2026-05-05 | Refreshed tracker for Phase 1 execution, corrected completed Phase 0 task statuses, added Phase 1 engineering tasks, and marked local development skeleton as the active first work item | Jesse + AI |
