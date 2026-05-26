# PoorToPour Execution Tracker

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-05-26
**Status:** 🟨 Phase 1 Active — Data foundation started

---

## 1. Current Focus

**Current phase:** Phase 1 - Data Foundation

Current objective:

Continue the first engineering phase from the new local development skeleton: FastAPI backend, React/Vite frontend, Docker Compose/Postgres, fixture-backed mock provider, Alembic migrations, persisted mock market data, versioned S&P 500 universe seed, yfinance OHLCV bootstrap ingestion, deterministic indicator snapshots, scan-run/candidate persistence, and the first generated scanner pass are online. Next focus is the Phase 1 review checkpoint.

Phase 1 should stay local-first, deterministic, and provider-flexible. No broker automation, AI trade decisions, intraday scanning, or post-MVP context sources belong in this phase.

---

## 2. Phase Progress

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| Phase | Description | Status | Notes |
| --- | --- | --- | --- |
| Phase 0 | Project definition, MVP boundary, documentation setup | ✅ Done | Main planning docs created: project plan, PRD, strategy, glossary, architecture, data sources, dashboard design, risk/backtesting, cost/ops, tracker, decision log, AI guidelines |
| Phase 1 | Data foundation | 🟨 In Progress | Phase 1 implementation and review are complete; next step is commit/push |
| Phase 2 | Technical scanner MVP | ⬜ Not Started | Indicators, setup detection, scoring |
| Phase 3 | Dashboard MVP | ⬜ Not Started | Ranked candidates, chart views, score breakdown |
| Phase 4 | Research context layer | ⬜ Not Started | Company profile, earnings, news headlines |
| Phase 5 | Risk and backtesting | ⬜ Not Started | Historical validation and risk calculations |
| Phase 6 | Intraday intelligence | ⬜ Not Started | Intraday scans, social/news/event context |
| Phase 7 | Paper trading | ⬜ Not Started | Simulated real-time trade tracking |
| Phase 8 | Controlled broker automation | ⬜ Not Started | Broker integration with strict guardrails |
| Phase 9 | Personal trading assistant | ⬜ Not Started | Semi/fully automated trading system under tested rules |

---

## 3. Phase 1 Detailed Checklist

This is the working checklist for the Phase 1 baseline before commit and push.

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| ID | Work Item | Status | Verification / Exit Criteria |
| --- | --- | --- | --- |
| P1-A | Local Docker development environment | ✅ Done | `docker compose up -d --build`; frontend, backend, db, and Adminer reachable |
| P1-B | Backend FastAPI baseline | ✅ Done | Health, market-data, scan, and indicator routes registered |
| P1-C | Frontend Vite/React baseline | ✅ Done | Frontend shell loads latest scan API; buttons are placeholder-only for now |
| P1-D | PostgreSQL and migrations | ✅ Done | Alembic migrations create market-data and scan tables |
| P1-E | Mock provider and deterministic fixtures | ✅ Done | Mock symbols, bars, profiles, earnings, and latest scan fixture exist |
| P1-F | Persist mock market data | ✅ Done | `symbol_profiles`, `daily_bars`, `company_profiles`, and `earnings_events` seed idempotently |
| P1-G | S&P 500 universe seed | ✅ Done | `data/seeds/sp500_seed.csv` imports 503 symbols |
| P1-H | Browser DB inspection | ✅ Done | Adminer available at `http://localhost:8080` |
| P1-I | yfinance bootstrap OHLCV adapter | ✅ Done | `AAPL`, `MSFT`, and `NVDA` sample bars ingested with `source = yfinance` |
| P1-J | IndicatorService | ✅ Done | `/api/symbols/{symbol}/indicators` returns deterministic scanner inputs and warnings |
| P1-K | Scan-run and candidate persistence | ✅ Done | `scan_runs` and `scan_candidates` tables exist; mock scan persists and reads through `/api/scans/latest` |
| P1-L | First deterministic setup detector | ✅ Done | Bootstrap trend/momentum scanner uses stored bars and indicator snapshots |
| P1-M | Persist generated scanner output | ✅ Done | Scanner writes a new `scan_run` and ranked `scan_candidates` |
| P1-N | Scanner API handoff | ✅ Done | Latest scan endpoint returns generated scanner output after scanner run |
| P1-O | Phase 1 review checkpoint | ✅ Done | Code review, security review, and trading-safety review completed in `/docs/11-phase-1-review.md`; fixes applied before commit/push |

Current simple mental model:

1. Data foundation is built enough for Phase 1.
2. The first scanner can turn indicators into persisted candidates.
3. Phase 1 review is complete; next step is commit/push after Jesse's final local inspection.

---

## 4. Active Tasks

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
| P1-001 | Create local development skeleton | ✅ Done | Jesse + AI | Backend/frontend folders, Docker Compose, env example, and README run notes exist |
| P1-002 | Create backend FastAPI baseline | ✅ Done | Jesse + AI | Health endpoint, app config module, persisted-data APIs, and test harness exist |
| P1-003 | Create frontend React + TypeScript baseline | ✅ Done | Jesse + AI | Vite app shell loads latest mock scan API |
| P1-004 | Add local PostgreSQL Docker service | ✅ Done | Jesse + AI | PostgreSQL service, health check, Alembic migration, and startup seed are in place |
| P1-005 | Add versioned S&P 500 seed file | ✅ Done | Jesse + AI | `data/seeds/sp500_seed.csv` has 503 rows with metadata and seed command |
| P1-006 | Define normalized market-data/provider models | 🟨 In Progress | Jesse + AI | Symbol, bar, profile, earnings, and provider status models exist; scan-run/candidate models still pending |
| P1-007 | Define Tier 1 provider interfaces | 🟨 In Progress | Jesse + AI | Basic provider protocol exists; final paid/provider-backed adapter still pending |
| P1-008 | Prototype first provider with sample symbols | ✅ Done | Jesse + AI | yfinance bootstrap adapter tested with `AAPL`, `MSFT`, and `NVDA` |
| P1-009 | Ingest and store daily OHLCV sample data | ✅ Done | Jesse + AI | 192 yfinance daily bars stored for 3 sample symbols |
| P1-010 | Add deterministic indicator service | ✅ Done | Jesse + AI | Latest indicator snapshots available from persisted bars |
| P1-011 | Add scan-run and candidate persistence | ✅ Done | Jesse + AI | `scan_runs` and `scan_candidates` tables store mock scan output |
| P1-012 | Add first deterministic setup detector | ✅ Done | Jesse + AI | Bootstrap trend/momentum scanner produces persisted candidates |

---

## 5. Current Phase Acceptance Criteria

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
| AC-P1-001 | Local development skeleton exists | ✅ Pass | Backend/frontend/Docker structure is runnable locally |
| AC-P1-002 | S&P 500 seed file exists | ✅ Pass | `data/seeds/sp500_seed.csv` imported 503 symbols into PostgreSQL |
| AC-P1-003 | Tier 1 provider interface exists | 🟨 In Progress | Protocol exists; final Tier 1 provider adapter remains pending |
| AC-P1-004 | Provider prototype is tested with sample symbols | ✅ Pass | yfinance bootstrap adapter ingested `AAPL`, `MSFT`, and `NVDA` |
| AC-P1-005 | Daily OHLCV can be ingested and stored | ✅ Pass | 192 daily bars stored with `source = yfinance` |
| AC-P1-006 | Stored bars can produce scanner-ready indicators | ✅ Pass | `/api/symbols/{symbol}/indicators` returns latest deterministic snapshot |
| AC-P1-007 | Scan runs and candidates can be persisted | ✅ Pass | Mock scan persists to `scan_runs` and `scan_candidates` |
| AC-P1-008 | First generated scanner output can be persisted | ✅ Pass | Momentum scanner wrote a generated scan run and candidate |

---

## 6. Test Tracking

Testing begins with implementation. Use this section once code exists.

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Backend health endpoint smoke test | Unit/API | TBD | ⬜ Not Started | Add with backend FastAPI baseline |
| T-002 | Backend provider model validation tests | Unit | TBD | ⬜ Not Started | Add with normalized DTOs/provider interfaces |
| T-003 | Frontend app shell smoke test | Unit | TBD | ⬜ Not Started | Add with frontend baseline |
| T-004 | Docker Compose startup check | Integration | TBD | ⬜ Not Started | Add after backend/frontend/Postgres services exist |
| T-005 | Sample OHLCV ingestion test | Integration | TBD | ⬜ Not Started | Add after provider prototype and database storage exist |
| T-006 | S&P 500 seed file smoke test | Unit/Data | `docker compose run --rm backend pytest` | ✅ Pass | Confirms required seed columns and expected 503-row range |
| T-007 | yfinance adapter normalization tests | Unit | `docker compose run --rm backend pytest` | ✅ Pass | Covers share-class symbol conversion, single-level frames, and MultiIndex frames |
| T-008 | Indicator service tests | Unit | `docker compose run --rm backend pytest` | ✅ Pass | Covers SMA, EMA, 52-week high, relative volume, trend flags, and insufficient-history warnings |
| T-009 | Scan repository payload test | Unit | `docker compose run --rm backend pytest` | ✅ Pass | Confirms scan fixture payload maps into scan-run/candidate models |
| T-010 | Momentum scanner tests | Unit | `docker compose run --rm backend pytest` | ✅ Pass | Confirms ranked candidates, score ordering, reasons, warnings, and zero-candidate behavior |

---

## 7. Open Questions / Clarifications

| ID | Question | Owner | Status | Blocker | Notes |
| --- | --- | --- | --- | --- | --- |
| Q-001 | Which market data provider should be used first? | Jesse + AI | 🟨 Partially Resolved | No | yfinance is accepted as a Phase 1 bootstrap OHLCV source. Final MVP trading-grade/provider-backed source remains TBD. |
| Q-002 | Should the MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | Jesse | ⬜ Open | No | Current default: S&P 500 only |
| Q-003 | Should the first dashboard be built before backtesting? | Jesse + AI | ⬜ Open | No | Current default: dashboard MVP before full backtesting |
| Q-004 | Should alerts be dashboard-only at first? | Jesse | ⬜ Open | No | Current default: dashboard-only |
| Q-005 | Should deployment be local-only for MVP? | Jesse | 🟨 Partially Resolved | No | Current default: local Docker Compose for development and MVP validation |
| Q-006 | What is the first acceptable monthly operating budget? | Jesse | ⬜ Open | No | Current recommendation: hosted MVP under $50/month if possible, hard review before exceeding $100/month |
| Q-007 | Which AI features, if any, should be allowed in MVP? | Jesse + AI | 🟨 Partially Resolved | No | Current default: none for trade decisions; AI summaries are post-MVP and disabled by default |

---

## 8. Decisions Log Snapshot

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

## 9. Risks / Issues

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

## 10. Phase 1 Scaffold Update - 2026-05-25

Completed in this pass:

- Created FastAPI backend baseline with `/api/health`, provider status, symbol, bar, profile, earnings, and latest-scan endpoints.
- Created fixture-backed mock provider for `NVDA`, `MSFT`, `AAPL`, `META`, `AMD`, and `AMZN`.
- Added deterministic sample daily OHLCV, company profile, earnings, and latest scan fixtures.
- Created React + TypeScript + Vite frontend shell using the mock latest-scan API.
- Added Docker Compose services for backend, frontend, and PostgreSQL.
- Added `.env.example`, Dockerfiles, and Docker ignore files.
- Added backend smoke tests for health and mock provider behavior.
- Added Alembic migration for symbol, company profile, earnings, and daily bar tables.
- Added idempotent seed command that persists mock fixtures into PostgreSQL.
- Updated symbol, bar, profile, and earnings API endpoints to read from persisted tables.
- Added versioned S&P 500 universe seed from `datasets/s-and-p-500-companies`.
- Added idempotent S&P 500 seed command for `symbol_profiles`.
- Added yfinance bootstrap provider and manual OHLCV ingestion command.
- Added deterministic indicator service and `/api/symbols/{symbol}/indicators` endpoint.
- Added scan-run and scan-candidate persistence tables, repository methods, and scan APIs.
- Added first deterministic bootstrap trend/momentum scanner and persistence runner.

Verified:

| Check | Command | Result |
| --- | --- | --- |
| Compose config | `docker compose config` | Pass |
| Backend tests | `docker compose run --rm backend pytest` | 16 passed |
| Frontend build | `npm.cmd run build` from `frontend/` | Pass |
| Compose startup | `docker compose up -d --build` | Pass |
| Backend health | `GET http://localhost:8000/api/health` | Pass |
| Latest scan API | `GET http://localhost:8000/api/scans/latest` | Pass |
| Persisted symbols API | `GET http://localhost:8000/api/symbols` | Pass |
| Persisted bars API | `GET http://localhost:8000/api/symbols/NVDA/bars` | Pass |
| Postgres seed counts | `select count(*) from symbol_profiles; select count(*) from daily_bars;` | 6 symbols, 60 bars |
| S&P 500 universe seed | `docker compose run --rm backend python -m app.scripts.seed_sp500_universe` | 503 symbols imported |
| Postgres after S&P seed | `select count(*) from symbol_profiles; select count(*) from daily_bars;` | 503 symbols, 60 bars |
| yfinance sample ingestion | `docker compose run --rm backend python -m app.scripts.ingest_yfinance_bars --symbols AAPL MSFT NVDA --period 3mo` | 192 bars imported |
| yfinance Postgres counts | `select source, count(*) from daily_bars group by source;` | 60 mock bars, 192 yfinance bars |
| Indicator API | `GET http://localhost:8000/api/symbols/AAPL/indicators` | Pass |
| Scan table migration | `docker compose run --rm backend alembic upgrade head` | Pass |
| Persisted scan counts | `select count(*) from scan_runs; select count(*) from scan_candidates;` | 1 scan run, 6 candidates |
| Persisted latest scan API | `GET http://localhost:8000/api/scans/latest` | Pass |
| Generated scanner run | `docker compose run --rm backend python -m app.scripts.run_momentum_scan --limit 25` | 1 generated candidate persisted |
| Latest generated scan API | `GET http://localhost:8000/api/scans/latest` | Returns generated `Bootstrap Trend Momentum` scan |
| Frontend page | `GET http://localhost:5173` | Pass |

Next recommended Phase 1 work:

1. Jesse performs final local inspection in browser/Adminer if desired.
2. Commit and push Phase 1 baseline.
3. Begin Phase 2 technical scanner MVP.

Review checkpoint completed:

Full review notes are saved in `/docs/11-phase-1-review.md`.

| Review | Status | Notes |
| --- | --- | --- |
| Code review | ✅ Done | Fixed frontend nullable-field handling for generated scanner output |
| Security review | ✅ Done | Bound local dev ports to `127.0.0.1`; no committed API keys found; npm audit found 0 vulnerabilities; `pip check` passed |
| Trading-safety review | ✅ Done | Bootstrap scanner can no longer label candidates `Actionable` before risk/reward exists |

---

## 11. Change Log

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
| 2026-05-25 | Added local FastAPI/React/Docker scaffold, fixture-backed mock provider, sample scan API, frontend shell, and smoke-test tracking | Jesse + AI |
| 2026-05-25 | Added Alembic migration, PostgreSQL persistence for mock market data, idempotent seed command, and persisted-data API verification | Jesse + AI |
| 2026-05-25 | Added versioned S&P 500 seed CSV, metadata, seed command, seed smoke test, and PostgreSQL verification for 503 symbols | Jesse + AI |
| 2026-05-25 | Added yfinance bootstrap provider, OHLCV ingestion command, normalization tests, and sample ingestion verification for AAPL/MSFT/NVDA | Jesse + AI |
| 2026-05-25 | Added deterministic indicator snapshots for persisted bars and verified the AAPL indicator API | Jesse + AI |
| 2026-05-25 | Added detailed Phase 1 checklist plus scan-run/candidate persistence and persisted scan API verification | Jesse + AI |
| 2026-05-26 | Added first deterministic bootstrap trend/momentum scanner, persisted generated output, and updated Phase 1 checklist for review readiness | Jesse + AI |
| 2026-05-26 | Completed Phase 1 code/security/trading-safety review, applied safety fixes, and deleted stale handoff document | Jesse + AI |
| 2026-05-26 | Added dedicated Phase 1 review document and moved visual/reference assets under `/docs` | Jesse + AI |
