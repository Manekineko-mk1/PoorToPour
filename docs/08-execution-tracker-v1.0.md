# PoorToPour Execution Tracker

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-04-30  
**Status:** ✅ Phase 0 Complete — Ready for Phase 1 data foundation

---

## 1. Current Focus

**Current phase:** Phase 0 — Project Definition

Current objective:

Phase 0 planning documents are broadly complete. The next project focus is Phase 1 — Data Foundation, starting with repo setup, local development environment, S&P 500 seed data, provider interfaces, and MVP Tier 1 data-provider experiments.

---

## 2. Phase Progress

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| Phase | Description | Status | Notes |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | ✅ | Main planning docs created: project plan, PRD, strategy, glossary, architecture, data sources, dashboard design, risk/backtesting, cost/ops, tracker, decision log, AI guidelines |
| Phase 1 | Data foundation | 🟨 | Recommended next phase: repo setup, local Docker environment, S&P 500 seed file, provider interfaces, initial OHLCV ingestion |
| Phase 2 | Technical scanner MVP | ⬜ | Indicators, setup detection, scoring |
| Phase 3 | Dashboard MVP | ⬜ | Ranked candidates, chart views, score breakdown |
| Phase 4 | Research context layer | ⬜ | Company profile, earnings, news headlines |
| Phase 5 | Risk and backtesting | ⬜ | Historical validation and risk calculations |
| Phase 6 | Intraday intelligence | ⬜ | Intraday scans, social/news/event context |
| Phase 7 | Paper trading | ⬜ | Simulated real-time trade tracking |
| Phase 8 | Controlled broker automation | ⬜ | Broker integration with strict guardrails |
| Phase 9 | Personal trading assistant | ⬜ | Semi/fully automated trading system under tested rules |

---

## 3. Active Tasks

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| ID | Task | Status | Owner | Notes |
| --- | --- | --- | --- | --- |
| P0-001 | Create GitHub repository | ✅ | Jesse | Repo created as PoorToPour |
| P0-002 | Create project plan | ✅ | Jesse + AI | Saved as `/docs/00-project-plan.md` |
| P0-003 | Create execution tracker | ✅ | Jesse + AI | Saved as `/docs/08-execution-tracker.md` |
| P0-004 | Create decision log | ✅ | Jesse + AI | Saved as `/docs/09-decision-log.md` |
| P0-005 | Create AI working guidelines | ✅ | Jesse + AI | Saved as `/docs/10-ai-working-guidelines.md` |
| P0-006 | Create product requirements document | ✅ | Jesse + AI | Saved as `/docs/01-product-requirements.md` |
| P0-007 | Create cost and operations document | ✅ | Jesse + AI | Saved as `/docs/07-cost-and-operations.md` |
| P0-008 | Create trading strategy requirements document | ✅ | Jesse + AI | Saved as `/docs/02-trading-strategy-requirements.md` |
| P0-009 | Create trading concepts glossary | ✅ | Jesse + AI | Saved as `/docs/02a-trading-concepts-glossary.md` |
| P0-010 | Create technical architecture document | ✅ | Jesse + AI | Saved as `/docs/03-technical-architecture.md` |
| P0-010 | Create data sources document | ⬜ | Jesse + AI | Planned as `/docs/04-data-sources.md` |
| P0-011 | Create dashboard design document | ⬜ | Jesse + AI | Planned as `/docs/05-dashboard-design.md` |
| P0-012 | Create risk and backtesting document | ⬜ | Jesse + AI | Planned as `/docs/06-risk-and-backtesting.md` |

---

## 4. Current Phase Acceptance Criteria

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Pass` | `⛔ Blocked`

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P0-001 | Project vision is documented | ✅ Pass | Covered in `/docs/00-project-plan.md` |
| AC-P0-002 | MVP scope is documented | ✅ Pass | MVP defaults agreed |
| AC-P0-003 | Non-goals are documented | ✅ Pass | Automated trading excluded from MVP |
| AC-P0-004 | High-level product phases are documented | ✅ Pass | Roadmap lives in project plan |
| AC-P0-005 | Execution tracking process is documented | ✅ Pass | This file |
| AC-P0-006 | Decision logging process is documented | ✅ Pass | `/docs/09-decision-log.md` |
| AC-P0-007 | AI working process is documented | ✅ Pass | `/docs/10-ai-working-guidelines.md` |
| AC-P0-008 | Product requirements are documented | ✅ Pass | `/docs/01-product-requirements.md` created |
| AC-P0-009 | Cost and operations requirements are documented | ✅ Pass | `/docs/07-cost-and-operations.md` created |
| AC-P0-010 | Trading strategy requirements are documented | ✅ Pass | `/docs/02-trading-strategy-requirements.md` created |
| AC-P0-011 | Trading concepts glossary is documented | ✅ Pass | `/docs/02a-trading-concepts-glossary.md` created |
| AC-P0-012 | Technical architecture is documented | ✅ Pass | `/docs/03-technical-architecture.md` created |
| AC-P0-013 | Data sources are documented | ✅ Pass | `/docs/04-data-sources.md` created |
| AC-P0-014 | Dashboard design is documented | ✅ Pass | `/docs/05-dashboard-design.md` created |
| AC-P0-015 | Risk and backtesting are documented | ✅ Pass | `/docs/06-risk-and-backtesting.md` created |
| AC-P0-016 | Phase 0 planning package is complete | ✅ Pass | Ready to move into Phase 1 data foundation |
| AC-P1-001 | Local development skeleton exists | ⬜ Not Started | Backend/frontend/Docker structure |
| AC-P1-002 | S&P 500 seed file exists | ⬜ Not Started | Versioned local seed for MVP universe |
| AC-P1-003 | Tier 1 provider interface exists | ⬜ Not Started | Provider-backed MVP data source only |
| AC-P1-004 | Tier 1 provider prototype is tested with sample symbols | ⬜ Not Started | Validate response shape, limits, adjusted data, and errors |
| AC-P1-005 | Daily OHLCV can be ingested and stored | ⬜ Not Started | First real data foundation milestone |

---

## 5. Test Tracking

Testing is not applicable until implementation begins. Use this section once code exists.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Placeholder for first backend test | Unit | TBD | ⬜ | Add after backend skeleton exists |
| T-002 | Placeholder for first frontend test | Unit | TBD | ⬜ | Add after dashboard skeleton exists |
| T-003 | Placeholder for first scanner validation | Integration | TBD | ⬜ | Add after indicator engine exists |

---

## 6. Open Questions / Clarifications

| ID | Question | Owner | Status | Blocker | Notes |
| --- | --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first? | Jesse + AI | 🟨 Partially Resolved | No | MVP will use Tier 1 provider-backed data only. Specific provider remains TBD; likely prototype FMP-style provider first and consider Tier 2/hybrid or higher-quality paid provider later after MVP scanner proves useful. |
| Q-002 | Should the MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | Jesse | ⬜ Open | No | Current default: S&P 500 only |
| Q-003 | Should the first dashboard be built before backtesting? | Jesse + AI | ⬜ Open | No | Current default: dashboard MVP before full backtesting |
| Q-004 | Should alerts be dashboard-only at first? | Jesse | ⬜ Open | No | Current default: dashboard-only |
| Q-005 | Should deployment be local-only for MVP? | Jesse | ⬜ Open | No | Current default: local Docker Compose |
| Q-006 | What is the first acceptable monthly operating budget? | Jesse | ⬜ Open | No | Current recommendation: hosted MVP under $50/month if possible, hard review before exceeding $100/month |
| Q-007 | Which AI features, if any, should be allowed in MVP? | Jesse + AI | ⬜ Open | No | Current default: none for trade decisions; summaries post-MVP |

---

## 7. Decisions Log Snapshot

The canonical decision log is `/docs/09-decision-log.md`.

| Date | Decision | Impact |
| --- | --- | --- |
| 2026-04-29 | Project name is PoorToPour | Sets repo identity and documentation tone |
| 2026-04-29 | Roadmap stays inside `/docs/00-project-plan.md` | Avoids duplicate roadmap docs |
| 2026-04-29 | Add `/docs/08-execution-tracker.md` | Creates living work tracker |
| 2026-04-29 | Add `/docs/09-decision-log.md` | Creates durable decision memory |
| 2026-04-29 | Add `/docs/10-ai-working-guidelines.md` | Creates future-session AI instructions |
| 2026-04-29 | MVP starts as long-only daily/weekly swing scanner | Keeps first build manageable and testable |
| 2026-04-29 | No automated trading in MVP | Avoids unsafe execution before validation |
| 2026-04-30 | Create `/docs/01-product-requirements.md` | Defines MVP product workflows and scope |
| 2026-04-30 | Add `/docs/07-cost-and-operations.md` | Tracks hosting, data, AI, and operating cost controls |
| 2026-04-30 | Create `/docs/07-cost-and-operations.md` | Defines cost targets, operating modes, hosting/data/AI controls |
| 2026-04-30 | Create `/docs/02-trading-strategy-requirements.md` | Defines MVP setup families, indicators, scoring, risk/reward, and validation requirements |
| 2026-04-30 | Create `/docs/02a-trading-concepts-glossary.md` | Adds beginner-friendly explanations of trading concepts used by the strategy document |
| 2026-04-30 | Create `/docs/03-technical-architecture.md` | Defines MVP system architecture, modules, data flow, jobs, APIs, database boundaries, and future automation path |
| 2026-04-30 | Create `/docs/04-data-sources.md` | Defines MVP data needs, provider abstraction, freshness rules, provider candidates, and data-quality controls |
| 2026-04-30 | Create `/docs/05-dashboard-design.md` | Defines MVP dashboard screens, candidate review flow, chart requirements, score/risk display, and UI states |
| 2026-04-30 | Create `/docs/06-risk-and-backtesting.md` | Defines risk model, caution flags, backtesting metrics, paper-trading gates, and automation prerequisites |

---

## 8. Risks / Issues

Legend: `⬜ Open` | `🟨 Watching` | `✅ Closed` | `⛔ Blocked`

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-001 | Scope creep from scanner MVP into full autonomous trading too early | High | 🟨 Watching | Keep MVP focused on data, scanner, and dashboard |
| R-002 | Using unreliable or stale market data | High | 🟨 Watching | Data freshness must be shown in dashboard |
| R-003 | False confidence from untested signals | High | 🟨 Watching | Explainability and backtesting required before automation |
| R-004 | Overbuilding architecture before proving scanner value | Medium | 🟨 Watching | Keep stack simple: FastAPI, React, PostgreSQL, Docker Compose |
| R-005 | Mixing research output with trade execution too early | High | 🟨 Watching | Broker integration is post-paper-trading only |

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
