# PoorToPour Decision Log

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-05-26

---

## Purpose

This document records important product, trading, architecture, workflow, and risk decisions for PoorToPour.

Use this file to preserve why decisions were made, not just what was chosen. Future sessions should check this file before revisiting major direction, architecture, or trading-safety choices.

---

## Decision Status Legend

| Status | Meaning |
| --- | --- |
| Proposed | Suggested but not yet accepted |
| Accepted | Current project direction |
| Replaced | No longer current because a newer decision superseded it |
| Rejected | Considered and intentionally not chosen |

---

## Decision Log

| ID | Date | Status | Decision | Reason | Trade-off | Impact |
| --- | --- | --- | --- | --- | --- | --- |
| D-001 | 2026-04-29 | Accepted | Project name is **PoorToPour** | Memorable personal-project identity with humorous ambition | Less professional than a fintech-style name | Sets README, repo, and documentation tone |
| D-002 | 2026-04-29 | Accepted | Project description is **From broke to pouring champagne.** | Captures the long-term dream in a funny, concise way | Not suitable as formal investment product language | Used as repo/project tagline |
| D-003 | 2026-04-29 | Accepted | Keep the high-level roadmap inside `/docs/00-project-plan.md` | Avoids duplicating roadmap information across docs | Roadmap is less isolated than a standalone file | Section 6 of project plan is the canonical roadmap |
| D-004 | 2026-04-29 | Accepted | Add `/docs/08-execution-tracker-v1.0.md` | Provides a living tracker for current work and phase status | Requires periodic maintenance | Future sessions should update it after meaningful progress |
| D-005 | 2026-04-29 | Accepted | Add `/docs/09-decision-log.md` | Keeps durable memory of important project choices | Requires discipline to update | Prevents repeated debates and context loss |
| D-006 | 2026-04-29 | Accepted | Add `/docs/10-ai-working-guidelines.md` | Gives future AI sessions a project-specific workflow and engineering standard | Another doc to keep current | Improves continuity and implementation quality |
| D-007 | 2026-04-29 | Replaced | MVP starts with **S&P 500** universe by default | Clean, liquid, manageable starting universe | Misses small-cap momentum and broader market opportunities | Replaced by D-071: MVP universe is S&P 500 plus Nasdaq 100 |
| D-008 | 2026-04-29 | Accepted | MVP is **long-only** | Lower complexity and risk than supporting shorts immediately | No short-side setups in first version | Simplifies scoring, risk, and backtesting |
| D-009 | 2026-04-29 | Accepted | MVP focuses on **daily and weekly swing scans** | Easier to validate than intraday/day-trading scans | Delays real-time day-trading features | Reduces data, latency, and false-positive complexity |
| D-010 | 2026-04-29 | Accepted | Automated trading is excluded from MVP | Avoids unsafe execution before strategy validation | Slower path to final automation dream | Broker integration requires backtesting and paper-trading evidence first |
| D-011 | 2026-04-29 | Accepted | First technical setup families are breakout, pullback continuation, and relative strength | These are explainable, chart-friendly, and testable | Excludes mean reversion, shorting, options, and event gambles initially | Defines first scanner requirements |
| D-012 | 2026-04-29 | Accepted | Preferred backend stack is Python FastAPI | Strong financial-data and analytics ecosystem | Requires discipline to avoid messy pipelines | Guides backend architecture document |
| D-013 | 2026-04-29 | Accepted | Preferred frontend stack is React + TypeScript | Strong dashboard ecosystem and type safety | Requires separate frontend/backend coordination | Guides dashboard and architecture documents |
| D-014 | 2026-04-29 | Accepted | Preferred database is PostgreSQL | Reliable relational storage with future TimescaleDB path | More setup than flat files | Supports scan history, symbols, indicators, and candidates |
| D-015 | 2026-04-29 | Accepted | Local-first Docker Compose deployment for MVP | Fast personal development loop | Not production-grade deployment | Simplifies early implementation |
| D-016 | 2026-04-29 | Accepted | Use deterministic rules before AI-generated trade reasoning | Keeps signals explainable and testable | Delays flashy AI summaries | Reduces black-box trading risk |
| D-017 | 2026-04-29 | Accepted | AI summaries can be added later, but AI should not make trade decisions in MVP | Prevents false confidence from generated explanations | Less magical MVP | Keeps decision logic auditable |
| D-018 | 2026-04-29 | Accepted | Add trading safety review beside normal code/security review | Trading bugs can create misleading or unsafe outputs | Adds review overhead | Required before risk, backtesting, paper trading, and automation features |
| D-019 | 2026-04-29 | Accepted | Keep documentation modular under `/docs` | Easier to maintain and use across sessions | More files than one mega-spec | Enables focused docs by product, strategy, architecture, data, dashboard, and risk |
| D-020 | 2026-04-29 | Accepted | Do not use GitHub Issues immediately unless the Markdown tracker becomes crowded | Markdown is enough for early personal project planning | Less formal task management | Avoids Jira cosplay and keeps flow lightweight |
| D-021 | 2026-04-30 | Accepted | Create `/docs/01-product-requirements.md` as the product-facing requirements document | Separates user workflows, screens, scope, and product constraints from trading formulas and architecture | Adds another document to maintain | Provides the product contract for the MVP dashboard and scan-review experience |
| D-022 | 2026-04-30 | Accepted | Add `/docs/07-cost-and-operations.md` as a separate cost and operating model document | Cost discipline is important enough to deserve detailed tracking outside the product requirements doc | More documentation overhead | Enables explicit budgeting for hosting, data providers, AI usage, jobs, and operating modes |
| D-023 | 2026-04-30 | Accepted | Keep detailed cost estimates out of `/docs/01-product-requirements.md` | Product requirements should state cost constraints, while vendor prices and operating estimates need a dedicated, changeable document | Requires cross-reference between docs | Keeps the PRD readable while preserving cost visibility |
| D-024 | 2026-04-30 | Accepted | MVP should run locally first and should not require AI | Avoids recurring cost and keeps signal generation deterministic while the scanner is unproven | Hosted access and AI summaries are delayed | Keeps early development cheap, explainable, and testable |
| D-025 | 2026-04-30 | Accepted | Hosted MVP should aim to stay under $50/month where possible | Personal project costs must stay sustainable before scanner value is proven | May require simpler hosting/data choices | Sets a practical operating budget for early deployment |
| D-026 | 2026-04-30 | Accepted | AI usage must be disabled by default and capped before enablement | Prevents runaway agent/token spending | AI summaries and research features arrive later | Requires usage logging, feature toggles, and budget controls before AI workflows |
| D-027 | 2026-04-30 | Accepted | Create `/docs/02-trading-strategy-requirements.md` to define MVP scanner logic | Strategy rules need a separate contract before architecture and implementation | Adds another document to maintain | Defines setup families, indicators, scoring, risk/reward, status labels, and validation requirements |
| D-028 | 2026-04-30 | Accepted | MVP strategy uses breakout, pullback continuation, and relative strength leader setup families | These setup types are explainable, visual, and practical for daily/weekly swing scanning | Excludes mean reversion, shorting, options, and intraday setups initially | Gives the first scanner a narrow and testable scope |
| D-029 | 2026-04-30 | Accepted | Strategy output must remain deterministic and explainable in MVP | Enables dashboard explanations and future backtesting | AI-generated trade reasoning is delayed | Prevents black-box trading signals |
| D-030 | 2026-04-30 | Accepted | Create `/docs/02a-trading-concepts-glossary.md` beside the strategy requirements | Trading terminology is a learning dependency for reviewing and implementing strategy logic | Adds one supporting documentation file | Improves shared understanding before architecture and implementation |
| D-031 | 2026-04-30 | Accepted | Create `/docs/03-technical-architecture.md` to define the MVP system shape | Product and strategy requirements need implementation boundaries before coding | Adds another planning document | Defines services, modules, data flow, database boundaries, jobs, APIs, and deployment path |
| D-032 | 2026-04-30 | Accepted | Use a modular monolith for MVP | Simpler and cheaper than microservices while still allowing clean internal boundaries | Requires discipline to keep modules separated | Keeps local-first development practical |
| D-033 | 2026-04-30 | Accepted | Use provider abstraction for external data integrations | Avoids vendor lock-in and improves testability | Adds mapping/interface work | Allows data provider choice to be deferred until implementation needs are clearer |
| D-034 | 2026-04-30 | Accepted | Use APScheduler initially for local-first scheduled jobs | Daily/weekly MVP jobs do not need a full distributed queue | Less robust than Celery/RQ for heavy workloads | Keeps MVP job architecture simple |
| D-035 | 2026-04-30 | Accepted | Keep broker integration outside the MVP architecture | Trading execution requires validation, paper trading, risk controls, and kill switch first | Delays automation features | Preserves safety boundary |
| D-036 | 2026-04-30 | Accepted | Use open-source technical-analysis libraries for standard indicator calculations where practical | Avoids subtle formula, warm-up-period, and edge-case bugs in common indicators | Adds dependency-management and supply-chain review responsibilities | Speeds up MVP indicator implementation while preserving testability |
| D-037 | 2026-04-30 | Accepted | Keep setup detection, candidate scoring, risk/reward estimates, caution flags, and strategy decisions in-house | These are the core PoorToPour strategy and safety logic and must remain explainable, versioned, and auditable | Requires more custom implementation for the strategy layer | Ensures the scanner's trading brain remains project-owned |
| D-038 | 2026-04-30 | Accepted | Wrap indicator libraries behind an internal `IndicatorService` | Prevents third-party APIs and objects from leaking into strategy, scoring, API, or dashboard layers | Adds a small abstraction layer | Allows swapping indicator libraries later without rewriting core strategy logic |
| D-039 | 2026-04-30 | Accepted | Create `/docs/04-data-sources.md` to define data-source strategy before implementation | Data quality, provider limits, freshness, and cost shape the scanner architecture | Adds another planning document | Establishes MVP data needs and provider abstraction rules |
| D-040 | 2026-04-30 | Accepted | Use a local S&P 500 seed file for MVP universe bootstrapping | Keeps the MVP reproducible and avoids early provider dependency | Manual updates needed until automated refresh exists | Simplifies Phase 1 data foundation |
| D-041 | 2026-04-30 | Accepted | Use daily OHLCV as the first required market data layer | Supports daily/weekly swing scans while keeping cost and complexity low | Intraday/day-trading features are delayed | Aligns data needs with MVP trading scope |
| D-042 | 2026-04-30 | Replaced | Defer final market data provider selection until implementation testing | Provider pricing, rate limits, adjusted data quality, and endpoint behavior need hands-on validation | Requires a provider experiment step before full implementation | Replaced by D-070: use Alpha Vantage as the first real provider adapter |
| D-043 | 2026-04-30 | Accepted | Treat missing required price data as candidate-blocking and missing context data as warning-only | Price data is essential for strategy safety, while company/earnings context is useful but not always available | Some candidates may appear with incomplete context | Balances scanner reliability with practical MVP provider limits |
| D-044 | 2026-04-30 | Accepted | MVP data sourcing will use Tier 1 provider-backed data only for core scanner inputs | Keeps MVP implementation simple, reliable, and easier to validate before adding hybrid data complexity | Tier 2 official public APIs and Tier 3 scraping are delayed | Reduces early data-quality, terms, normalization, and maintenance risks |
| D-045 | 2026-04-30 | Accepted | Tier 2 official public APIs and Tier 3 scraping are deferred to MVP+ or later | The scanner should first prove useful on clean provider-backed data before adding supplemental context sources | Delays richer fundamentals/filings/scraped context | Creates a clear re-evaluation point after MVP |
| D-046 | 2026-04-30 | Accepted | Re-evaluate higher-quality paid provider versus hybrid sourcing after MVP scanner quality is demonstrated | Data costs can become meaningful, so provider upgrades should be justified by evidence | Final provider architecture remains flexible | Prevents premature spending and premature complexity |
| D-047 | 2026-04-30 | Accepted | Create `/docs/05-dashboard-design.md` to define the MVP dashboard experience before implementation | Dashboard behavior must align with product, strategy, architecture, and data-source requirements | Adds another planning document | Defines the scan-review cockpit, candidate detail view, score/risk display, freshness states, and UI scope |
| D-048 | 2026-04-30 | Accepted | MVP dashboard uses dark mode first | Dense chart and market-data review benefits from strong contrast and terminal-like focus | Light mode is delayed | Keeps first UI direction simple and cohesive |
| D-049 | 2026-04-30 | Accepted | Candidate ranking table is the central MVP dashboard surface | The main product value is ranked, explainable scan results | Fancy cards/visuals are secondary | Prioritizes the workflow that proves scanner usefulness |
| D-050 | 2026-04-30 | Accepted | Watchlist, alerts, cost dashboard, and news/catalyst feed are MVP+ or later | These features add persistence, notifications, cost UI, or data complexity before scanner value is proven | Delays convenience and context features | Keeps MVP focused on scan, rank, inspect, and learn |
| D-051 | 2026-04-30 | Accepted | Create `/docs/06-risk-and-backtesting.md` as the final major Phase 0 planning document | Risk and validation gates must be explicit before implementation and any future automation | Adds another planning document | Defines candidate risk model, caution flags, backtesting metrics, paper-trading gates, and automation prerequisites |
| D-052 | 2026-04-30 | Accepted | Treat all MVP risk outputs as research estimates, not trading instructions | Prevents overstating scanner authority and keeps manual review central | UI must be careful with wording | Reduces risk of false confidence |
| D-053 | 2026-04-30 | Accepted | Use 2:1 as the initial preferred minimum risk/reward for Actionable swing candidates | Simple conservative starting point for manual review | May reject some valid lower-R opportunities | Gives scoring and status labels a clear first threshold |
| D-054 | 2026-04-30 | Accepted | Paper trading is required before any broker automation | Real-time simulated validation is safer than jumping from backtest to live trading | Slower path to automation | Creates a necessary safety gate |
| D-055 | 2026-04-30 | Accepted | Live automation requires kill switch, risk limits, audit logs, monitoring, and live/paper separation | Automation without safety controls is unacceptable | Significant implementation overhead later | Protects against runaway or unsafe trading behavior |
| D-056 | 2026-05-14 | Accepted | Keep external-project inspiration out of MVP unless it supports the existing scan-rank-inspect-learn flow | Prevents MVP scope drift after reviewing OpenStock and Spring Duck references | Some attractive features are delayed | Preserves Phase 1 focus on data foundation and core scanner |
| D-057 | 2026-05-14 | Accepted | Add OpenStock-inspired ideas such as command palette, scanner-aware watchlist, alerts, and scan briefings to MVP+ or later roadmap | These are useful product patterns but not required for MVP scanner validation | Delays convenience features | Keeps MVP focused while preserving good ideas |
| D-058 | 2026-05-14 | Accepted | Add Spring Duck-inspired ideas such as chart signal markers, detected-signal cards, sector scanner grid, and AI insight panel to MVP+ or later roadmap | These strengthen the future signal UX but could create scope drift if added now | Delays visually attractive features | Preserves MVP simplicity while improving final vision |
| D-059 | 2026-05-14 | Accepted | Future pattern signals require deterministic rules and validation before entering scoring | Visual chart patterns can be subjective and overfit-prone | Slower feature expansion | Protects scanner credibility and backtesting quality |
| D-060 | 2026-05-25 | Accepted | Treat v0.2 mock UI renders as visual direction, not MVP scope expansion | The renders clarify the desired product feel while showing several MVP+ ideas | Some visible panels may not be built immediately | Keeps implementation focused on scan-rank-inspect-learn |
| D-061 | 2026-05-25 | Accepted | Treat Spring Duck-inspired signal UX as a deliberate MVP+ feature cluster | The reference aligns well with PoorToPour's future scanner experience after deterministic rules exist | Adds a visible backlog of attractive UI ideas | Captures the desired direction while preserving MVP scope |
| D-062 | 2026-05-25 | Accepted | Start Phase 1 implementation with a fixture-backed mock provider before wiring a real market-data provider | Mock data keeps backend, frontend, Docker, and provider interfaces testable without API keys or rate limits | First data is not real market data | Enables deterministic development while preserving the provider abstraction |
| D-063 | 2026-05-25 | Accepted | Use Alembic migrations and PostgreSQL persistence before adding a real provider adapter | Persisted normalized data gives future provider adapters a stable target schema | Adds migration and repository maintenance | Keeps real-provider integration clean and testable |
| D-064 | 2026-05-25 | Accepted | Use the `datasets/s-and-p-500-companies` CSV as the versioned local S&P 500 universe seed for MVP bootstrapping | It is simple, reviewable, and adequate for local universe setup before provider-backed listing metadata exists | It is Wikipedia-derived and not a licensed trading-grade index membership feed | Keeps Phase 1 moving while making the data-source caveat explicit |
| D-065 | 2026-05-25 | Accepted | Use yfinance as a Phase 1 OHLCV bootstrap adapter only | It lets the project validate ingestion, normalization, and storage with real daily bars before choosing a paid/provider-backed source | yfinance is unofficial and should not be treated as final trading-grade data | Speeds up local development while preserving the final provider decision |
| D-066 | 2026-05-25 | Accepted | Build scanner inputs through a deterministic internal `IndicatorService` | Scanner inputs need to be explainable, testable, and independent from provider-specific objects | Adds project-owned calculation code and tests to maintain | Creates a stable bridge from stored bars to setup detection and scoring |
| D-067 | 2026-05-25 | Accepted | Persist scan runs and candidates before building the first generated scanner pass | Scanner output needs a durable target before setup-detection logic starts producing candidates | Requires flexible JSON fields while the score schema is still evolving | Lets mock, bootstrap, and future generated scans share one API shape |
| D-068 | 2026-05-26 | Accepted | Make the first generated scanner a narrow bootstrap trend/momentum detector | It proves the end-to-end path from stored bars to indicators to persisted candidates without pretending to be the full strategy | The first generated candidate logic is intentionally simple and may produce few candidates | Marks Phase 1 ready for review before expanding scanner sophistication |
| D-069 | 2026-05-26 | Accepted | Keep mock UI renders and research screenshots under `/docs` | Visual references are project documentation and should live beside the planning docs | Asset paths need updates when references move | Keeps the repository root focused on runnable application code and top-level setup files |
| D-070 | 2026-05-26 | Accepted | Use Alpha Vantage as the first real market-data provider adapter | Jesse already has an Alpha Vantage key, and it is good enough to test the provider abstraction after yfinance bootstrap | API limits may constrain full-universe refreshes and require batching, caching, and rate-limit handling | Gives Phase 2/Phase 3 a concrete provider target without committing to it forever |
| D-071 | 2026-05-26 | Accepted | MVP universe is S&P 500 plus Nasdaq 100 | Adds major liquid growth/technology names while staying manageable | Larger universe increases provider calls, deduping work, and scan runtime | Requires universe seeding to merge duplicate symbols across indexes |
| D-072 | 2026-05-26 | Accepted | Build the Dashboard MVP before full backtesting | The scanner needs an inspectable user workflow before deeper validation tools | Full statistical validation comes later | Keeps near-term work focused on scan, rank, inspect, and learn |
| D-073 | 2026-05-26 | Accepted | Alerts are dashboard-only at first | Keeps early alerts visible but non-intrusive and avoids urgency-inducing notifications | No email, push, SMS, or broker-triggered alert actions initially | Preserves manual review and trading-safety boundaries |
| D-074 | 2026-05-26 | Accepted | MVP development runs on local Docker Compose; MVP+ and later should support cloud deployment | Local development keeps iteration cheap, while the project should eventually be reachable beyond one machine | Cloud deployment work is deferred until the scanner/dashboard prove useful | Sets a local-to-cloud path without adding cloud complexity to the current phase |
| D-075 | 2026-05-26 | Accepted | Hosted MVP should stay under $50/month if possible, with hard review before exceeding $100/month | Keeps the personal project financially sustainable | May limit hosting, provider, and AI choices | Creates a budget gate before paid infrastructure grows |
| D-076 | 2026-05-26 | Accepted | AI must not make trade decisions; AI summaries are post-MVP, disabled by default, and reviewed again after MVP+ | Preserves deterministic and auditable scanner behavior | Delays AI insight panels until the deterministic scanner exists | Keeps AI as an explanation layer, not a trading brain |

---

## Replaced Decisions

| ID | Date Replaced | Replaced By | Reason |
| --- | --- | --- | --- |
| D-007 | 2026-05-26 | D-071 | MVP universe expanded from S&P 500 only to S&P 500 plus Nasdaq 100 |
| D-042 | 2026-05-26 | D-070 | First real provider adapter selected as Alpha Vantage |

---

## Rejected Decisions

| ID | Date | Rejected Option | Reason |
| --- | --- | --- | --- |
| R-001 | 2026-04-29 | Start MVP with automated broker trading | Too risky before data validation, backtesting, and paper trading |
| R-002 | 2026-04-29 | Start MVP with full intraday social/news/political/Polymarket intelligence | Too much noisy alternative data before core scanner reliability |
| R-003 | 2026-04-29 | Create separate `/docs/07-project-roadmap.md` immediately | Roadmap already exists inside `/docs/00-project-plan.md`; separate file would duplicate it for now |

---

## How to Add a Decision

When adding a new decision, include:

1. Decision date.
2. Status.
3. Clear decision statement.
4. Reason.
5. Trade-off.
6. Impact on future work.

Use the next available `D-###` ID.

---

## Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-04-29 | Created initial decision log from project planning discussion | Jesse + AI |
| 2026-04-30 | Added decisions for product requirements and cost/operations documentation | Jesse + AI |
| 2026-04-30 | Added decisions from cost and operations planning | Jesse + AI |
| 2026-04-30 | Added decisions from trading strategy requirements planning | Jesse + AI |
| 2026-04-30 | Added decision to create trading concepts glossary | Jesse + AI |
| 2026-04-30 | Added decisions from technical architecture planning | Jesse + AI |
| 2026-04-30 | Added build-vs-buy decisions for technical indicator calculations | Jesse + AI |
| 2026-04-30 | Added decisions from data-source planning | Jesse + AI |
| 2026-04-30 | Added Tier 1-only MVP data-source decision and MVP+ re-evaluation path | Jesse + AI |
| 2026-04-30 | Added decisions from dashboard design planning | Jesse + AI |
| 2026-04-30 | Added decisions from risk and backtesting planning | Jesse + AI |
| 2026-05-14 | Added external-reference scope decisions for OpenStock and Spring Duck ideas | Jesse + AI |
| 2026-05-25 | Added decision for v0.2 mock UI render scope | Jesse + AI |
| 2026-05-25 | Added decision for Spring Duck-inspired MVP+ signal UX cluster | Jesse + AI |
| 2026-05-25 | Added decision to start Phase 1 with a fixture-backed mock provider | Jesse + AI |
| 2026-05-25 | Added decision to use Alembic/PostgreSQL persistence before real provider adapter | Jesse + AI |
| 2026-05-25 | Added decision to use the datasets S&P 500 CSV as the local MVP universe seed | Jesse + AI |
| 2026-05-25 | Added decision to use yfinance only as a Phase 1 OHLCV bootstrap adapter | Jesse + AI |
| 2026-05-25 | Added decision to build scanner inputs through a deterministic internal IndicatorService | Jesse + AI |
| 2026-05-25 | Added decision to persist scan runs and candidates before building generated scanner output | Jesse + AI |
| 2026-05-26 | Added decision for the first generated scanner to remain a narrow bootstrap trend/momentum detector | Jesse + AI |
| 2026-05-26 | Added decision to keep visual/research reference assets under `/docs` | Jesse + AI |
| 2026-05-26 | Resolved standing MVP direction questions for provider, universe, dashboard/backtesting order, alerts, deployment path, budget, and AI boundaries | Jesse + AI |
