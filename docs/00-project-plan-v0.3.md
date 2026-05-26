# PoorToPour Project Plan

**Description:** From broke to pouring champagne.

**Document:** `docs/00-project-plan.md`  
**Version:** 0.3  
**Status:** Draft  
**Owner:** Jesse  

---

## 1. Project Identity

**Project name:** PoorToPour  
**Repository name:** `poor-to-pour`  
**Description:** From broke to pouring champagne.

PoorToPour is a personal trading research and automation project. The long-term vision is to build a system that can scan U.S. markets, detect tradeable setups, explain why they matter, validate them through risk and backtesting, and eventually support controlled automated trading.

The project can have a funny name and Reddit-flavored soul, but the engineering and risk controls should be serious. The bot may dream in champagne, but it should behave like it has read the incident postmortem.

---

## 2. Long-Term Vision

The long-term goal is to build a trading system that can assist, then partially automate, and eventually fully automate a defined trading workflow while remaining:

- Testable
- Explainable
- Risk-controlled
- Auditable
- Iterative
- Grounded in real data

The final version may eventually include:

- Market scanning
- Technical setup detection
- Company and earnings research
- News and event monitoring
- Social sentiment monitoring
- Prediction-market context
- Political trade disclosure monitoring
- Backtesting
- Paper trading
- Broker integration
- Automated execution with strict guardrails

However, the project should not jump directly to automated trading. The first milestone is to build a reliable research dashboard that produces explainable trade candidates.

---

## 3. Product Direction

PoorToPour will start as a **local-first trading research dashboard for U.S. equities**.

The MVP will focus on swing-trade style technical scanning using daily candles, limited to a clean stock universe such as the S&P 500.

The first goal is not automated trading. The first goal is to produce explainable, ranked trade candidates with chart evidence and basic risk/reward context.

Automation, intraday scanning, social/news intelligence, paper trading, and live broker execution will be added only after the scanner and dashboard are reliable.

---

## 4. Recommended Documentation Structure

The project documentation should be split into focused files instead of one giant document.

The high-level roadmap should stay inside this project plan, especially Section 6: Core Product Phases. A separate roadmap file is not needed unless the project later becomes large enough to justify it.

```text
/docs
  00-project-plan.md
  01-product-requirements.md
  02-trading-strategy-requirements.md
  03-technical-architecture.md
  04-data-sources.md
  05-dashboard-design.md
  06-risk-and-backtesting.md
  07-cost-and-operations.md
  08-execution-tracker.md
  09-decision-log.md
  10-ai-working-guidelines.md
```

### 4.1 Document Responsibilities

| Document | Purpose |
|---|---|
| `00-project-plan.md` | Project vision, scope, phases, MVP boundary, and high-level roadmap. |
| `01-product-requirements.md` | User workflows, dashboard behavior, app features, and UX requirements. |
| `02-trading-strategy-requirements.md` | Trading setup definitions, indicators, scoring rules, scan intervals, and risk logic. |
| `03-technical-architecture.md` | Backend, frontend, database, jobs, APIs, deployment, and engineering design. |
| `04-data-sources.md` | Market data, fundamentals, news, social, prediction markets, and political trade data. |
| `05-dashboard-design.md` | Layout, components, visual hierarchy, charts, and interaction design. |
| `06-risk-and-backtesting.md` | Backtesting design, validation metrics, risk controls, and paper trading gates. |
| `07-cost-and-operations.md` | Cost estimates, operating modes, hosting strategy, AI usage budget, provider costs, and cost-control rules. |
| `08-execution-tracker.md` | Living status board for current phase progress, active tasks, acceptance criteria, risks, blockers, and change log. |
| `09-decision-log.md` | Canonical record of major project, product, trading, architecture, and risk decisions. |
| `10-ai-working-guidelines.md` | Future-session AI instructions, engineering standards, workflow rules, documentation rules, and trading-safety expectations. |

### 4.2 Tracking Model

PoorToPour uses a lightweight two-tier tracking model:

| Layer | Location | Purpose | Update Frequency |
|---|---|---|---|
| High-level roadmap | `00-project-plan.md`, Section 6 | Tracks the overall product journey from MVP to controlled automation. | Occasionally, when phases change meaningfully. |
| Execution tracker | `08-execution-tracker.md` | Tracks current work, phase status, acceptance criteria, risks, blockers, and next steps. | After meaningful work sessions or phase/task changes. |

Important decisions should be recorded separately in `09-decision-log.md`. Future AI sessions should use `10-ai-working-guidelines.md` as the working instruction reference before proposing plans or code changes.

## 5. MVP Boundary

### 5.1 MVP Summary

The MVP should be a local web dashboard that scans a limited U.S. stock universe, computes technical indicators, detects a few basic long-only setups, ranks candidates, and displays each candidate with chart evidence and simple risk/reward context.

### 5.2 MVP Defaults

| Area | Decision |
|---|---|
| Initial universe | S&P 500 |
| Initial trade direction | Long-only |
| Initial timeframe | Daily and weekly swing scans |
| Dashboard type | Local web app first |
| Backend | Python FastAPI |
| Frontend | React + TypeScript |
| Database | PostgreSQL |
| Initial data type | Daily OHLCV candles |
| Automated trading | Not included in MVP |
| Project tone | Funny name, serious risk controls |

### 5.3 MVP Includes

The MVP should include:

- Stock universe loader
- Daily OHLCV ingestion
- Technical indicator computation
- Daily scan job
- Weekly scan job
- Basic setup detection
- Candidate ranking
- Candidate explanation
- Basic company metadata
- Basic risk/reward calculation
- Scan history persistence
- Dashboard candidate table
- Candidate detail page
- Candlestick chart with indicators

### 5.4 MVP Excludes

The MVP should not include:

- Automated live trading
- Broker integration
- Options trading
- Short-selling strategies
- Full-market real-time scanning
- High-frequency or tick-level data
- Social media ingestion
- Polymarket integration
- Political trade disclosure monitoring
- Full financial statement analysis
- LLM-based trading decisions
- Mobile app
- Multi-user SaaS architecture

These exclusions are intentional. They keep the first version achievable and prevent the project from turning into a glitter-covered dependency hydra.

---

## 6. Core Product Phases

| Phase | Name | Goal |
|---|---|---|
| Phase 0 | Planning & Boundaries | Define what PoorToPour is and what MVP means. |
| Phase 1 | Market Data Foundation | Ingest symbols, price data, and basic metadata. |
| Phase 2 | Technical Scanner MVP | Compute indicators and detect basic setups. |
| Phase 3 | Dashboard MVP | Display ranked setups with charts and reasoning. |
| Phase 4 | Research Context Layer | Add company profile, earnings, and news headlines. |
| Phase 5 | Risk & Backtesting | Add risk calculations and historical validation. |
| Phase 6 | Intraday Intelligence | Add scheduled intraday scans, social/news/event context. |
| Phase 7 | Paper Trading | Simulate trades and measure real-time performance. |
| Phase 8 | Controlled Automation | Add broker integration with strict safety limits. |
| Phase 9 | Personal Trading Assistant | Automate defined strategies under tested guardrails. |

### 6.1 MVP Phase Boundary

The first MVP should cover:

- Phase 1: Market Data Foundation
- Phase 2: Technical Scanner MVP
- Phase 3: Dashboard MVP

Everything after Phase 3 should be treated as post-MVP.

### 6.2 External Inspiration Parking Lot

Ideas observed from OpenStock and Spring Duck are parked for MVP+ or later unless they directly support the existing MVP flow:

```text
scan -> rank -> inspect -> learn
```

Potential future additions:

- command palette / global ticker search;
- scanner-aware watchlist;
- chart signal markers;
- detected-signal cards;
- market signal cards;
- sector/theme scanner grid;
- ticker chips/search;
- market regime panel;
- alert engine;
- daily/weekly scan briefing;
- AI candidate insight panel;
- tabbed views such as Overview, Scanner, and Tasks;
- visual signal taxonomy;
- richer chart pattern detection such as VCP or Adam & Eve patterns.

These ideas must not expand the MVP unless explicitly re-approved.

---

## 7. First Trading Scope

### 7.1 Preferred Initial Style

The MVP should focus on **swing-trade scanning** rather than day-trading.

Reasoning:

- Daily candles are easier to source and validate.
- Swing setups are less sensitive to latency.
- The data model is simpler.
- Backtesting is easier.
- Dashboard expectations are clearer.
- False positives are easier to review manually.

Day-trading can be added later after the daily scanner, dashboard, and risk framework are stable.

### 7.2 Initial Setup Families

The MVP should support three setup families:

| Setup | Purpose |
|---|---|
| Breakout | Find stocks breaking above recent resistance with strong participation. |
| Pullback continuation | Find stocks in an uptrend pulling back toward support. |
| Relative strength leader | Find stocks outperforming the broader market. |

### 7.3 Strategies Not Included Initially

The MVP should not start with:

- Mean reversion
- Short-selling
- Options strategies
- Penny stocks
- Low-float runners
- Earnings gamble setups
- News-only trades
- Social-media-only trades

These may be explored later after the core scanner proves useful.

---

## 8. Technical Implementation Direction

### 8.1 Recommended Stack

| Layer | Recommendation |
|---|---|
| Frontend | React + TypeScript |
| Backend API | Python FastAPI |
| Data jobs | Python workers |
| Database | PostgreSQL |
| Data analysis | pandas / numpy |
| Charting | TradingView Lightweight Charts or Apache ECharts |
| Scheduler | APScheduler first |
| Local deployment | Docker Compose |
| Future queue | Celery + Redis if needed |

### 8.2 Backend Direction

Use Python for the backend and research engine.

Pros:

- Strong financial data ecosystem.
- Good support for data analysis.
- Easy integration with pandas, numpy, and technical-analysis libraries.
- FastAPI is clean and practical for building APIs.

Cons:

- Data pipelines can become messy without structure.
- Async job orchestration needs discipline as the project grows.

Decision:

Use **Python FastAPI** for the backend and scanner engine.

### 8.3 Frontend Direction

Use React and TypeScript for the dashboard.

Pros:

- Strong dashboard ecosystem.
- Good charting library support.
- Clear component model.
- TypeScript improves maintainability.

Cons:

- Adds frontend complexity.
- Requires clean API contracts from the backend.

Decision:

Use **React + TypeScript** for the dashboard.

---

## 9. MVP Definition of Done

The MVP is considered complete when:

1. The app can load a stock universe.
2. The app can fetch and store daily OHLCV data.
3. The app can compute technical indicators.
4. The app can run daily and weekly scans.
5. The app can produce ranked candidates.
6. Each candidate includes an explanation of why it was selected.
7. The dashboard shows the ranked candidates.
8. The user can open a candidate detail page.
9. The detail page shows a chart with relevant indicators.
10. The detail page shows basic risk/reward context.
11. Scan history is stored and reviewable.

The first real milestone is not “PoorToPour makes money.”

The first real milestone is:

> PoorToPour can consistently generate explainable trade candidates from reliable market data.

---

## 10. Risk Philosophy

PoorToPour should be built with risk controls from the beginning, even before live trading exists.

The project should never graduate to automated trading until the strategy has passed:

1. Historical validation
2. Manual review
3. Paper trading
4. Risk-control checks
5. Failure-mode testing

Future automated trading must include:

- Maximum risk per trade
- Maximum daily loss
- Maximum weekly loss
- Maximum number of open positions
- Maximum sector concentration
- Trade cooldown after losses
- Earnings-event restrictions
- Data freshness checks
- Manual override
- Kill switch

The kill switch is non-negotiable. Every trading bot needs one large “bad robot, stop” button.

---

## 11. MVP Success Metrics

MVP success should be measured by product reliability and signal quality, not profit.

| Metric | Target |
|---|---|
| Scheduled scan completion | 95%+ successful runs |
| Candidate explanations | 100% of candidates |
| Candidate chart availability | 100% of candidates |
| Indicator correctness | Verified against reference calculations |
| Scan history persistence | Available for every scan |
| Manual review workflow | Supported |
| False-positive review | Possible through historical scan records |

Later trading phases may introduce:

| Metric | Later Use |
|---|---|
| Backtested expectancy | Validate strategy quality. |
| Average R multiple | Measure risk-adjusted trade quality. |
| Max drawdown | Evaluate downside risk. |
| Paper-trading performance | Gate before live trading. |
| Live execution error rate | Monitor broker integration reliability. |

---

## 12. Non-Goals

Initial non-goals:

- Do not build live automated trading in MVP.
- Do not connect a brokerage account in MVP.
- Do not trade options in MVP.
- Do not support short-selling in MVP.
- Do not ingest social media in MVP.
- Do not rely on LLMs for trade decisions in MVP.
- Do not scan the full U.S. market in real time in MVP.
- Do not build a multi-user SaaS product in MVP.
- Do not build a mobile app in MVP.
- Do not attempt to predict every market move.

The project should first become a useful research assistant before it becomes a trading agent.

---

## 13. Immediate Next Steps

### 13.1 Documentation

The initial project-control documents are now part of the documentation plan:

1. `08-execution-tracker.md`
2. `09-decision-log.md`
3. `10-ai-working-guidelines.md`

Create and refine the following product and technical documents next:

1. `01-product-requirements.md` — created as initial draft.
2. `07-cost-and-operations.md` — next planned document.
3. `02-trading-strategy-requirements.md`
4. `03-technical-architecture.md`
5. `04-data-sources.md`
6. `05-dashboard-design.md`
7. `06-risk-and-backtesting.md`

### 13.2 Repo Setup

Initial repository structure to consider:

```text
poor-to-pour/
  docs/
    00-project-plan.md
    01-product-requirements.md
    07-cost-and-operations.md
    08-execution-tracker.md
    09-decision-log.md
    10-ai-working-guidelines.md
  backend/
  frontend/
  scripts/
  docker-compose.yml
  README.md
```

### 13.3 First Engineering Milestone

The first engineering milestone should be:

> Build a backend prototype that loads a stock universe, fetches historical daily candles, stores them, computes basic indicators, and outputs a ranked scan result as JSON.

No dashboard is required for the very first engineering spike. The scanner should work before the cockpit gets leather seats.

## 14. Decision Log

The canonical decision log now lives in:

```text
docs/09-decision-log.md
```

This project plan keeps only a short decision snapshot. Add new major decisions to `09-decision-log.md` instead of expanding this section.

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-29 | Project name selected: PoorToPour | Fun personal-project identity with memorable repo name. |
| 2026-04-29 | MVP will be local-first research dashboard | Keeps scope manageable and avoids premature deployment complexity. |
| 2026-04-29 | MVP will focus on S&P 500 | Clean initial universe with liquid, well-known names. |
| 2026-04-29 | MVP will be long-only | Simpler risk model and easier first validation. |
| 2026-04-29 | MVP will focus on daily/weekly swing scans | Easier data requirements and lower latency sensitivity than day-trading. |
| 2026-04-29 | Backend will use Python FastAPI | Strong data-analysis ecosystem and practical API development. |
| 2026-04-29 | Frontend will use React + TypeScript | Strong dashboard ecosystem and maintainable UI structure. |
| 2026-04-29 | Automated trading is excluded from MVP | Requires backtesting, paper trading, and safety controls first. |
| 2026-04-29 | High-level roadmap stays in `00-project-plan.md` | Section 6 is sufficient for current roadmap needs. |
| 2026-04-29 | Add `08-execution-tracker.md`, `09-decision-log.md`, and `10-ai-working-guidelines.md` | Gives the project lightweight execution tracking, decision memory, and future-session AI continuity. |
| 2026-04-30 | Add `07-cost-and-operations.md` to the documentation plan | Cost discipline is a product and architecture constraint for a personal project. |
| 2026-04-30 | Create `01-product-requirements.md` | Defines the MVP product workflows, screens, scope, and cost constraints. |
| 2026-05-14 | Keep external-project inspiration out of MVP unless it supports the existing scan-review flow | Preserves the MVP boundary after reviewing OpenStock and Spring Duck references. |

## 15. Progress Log

### v0.4 - 2026-05-14

- Added external inspiration parking lot for OpenStock and Spring Duck ideas.
- Reconfirmed that external references should not expand MVP scope without explicit approval.
- Updated Spring Duck-inspired items as MVP+ candidates behind the v0.2 mock direction.

### v0.3 - 2026-04-30

- Added `07-cost-and-operations.md` to the recommended documentation structure.
- Recorded cost discipline as a product and operating constraint.
- Marked `01-product-requirements.md` as created.
- Updated immediate next steps so cost and operations planning comes before deeper strategy and architecture documents.

### v0.2 - 2026-04-29

- Updated documentation structure.
- Confirmed high-level roadmap remains in this project plan.
- Added `08-execution-tracker.md` as the living current-work tracker.
- Added `09-decision-log.md` as the canonical decision record.
- Added `10-ai-working-guidelines.md` as the future-session AI instruction and engineering workflow reference.
- Updated immediate next steps and repo setup to reflect the new documentation structure.

### v0.1 - 2026-04-29

- Created initial project plan.
- Defined long-term vision.
- Defined MVP boundary.
- Confirmed initial defaults.
- Split future documentation into focused files.
- Added first roadmap and decision log.
