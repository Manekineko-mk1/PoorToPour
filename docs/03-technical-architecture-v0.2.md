# PoorToPour Technical Architecture

**Project:** PoorToPour
**Description:** From broke to pouring champagne.
**Document:** `/docs/03-technical-architecture.md`
**Date created:** 2026-04-30
**Last updated:** 2026-04-30
**Status:** Draft v0.2

---

## 1. Purpose

This document defines the initial technical architecture for PoorToPour.

It answers:

- What system are we building for MVP?
- What are the main services and modules?
- How does market data flow through the system?
- Where do indicators, scanners, scoring, and risk estimates live?
- What database boundaries should exist?
- What API endpoints are needed?
- How should scheduled jobs run?
- How should the dashboard consume data?
- How do we keep the MVP simple while leaving a safe path toward paper trading and automation later?

This document is architecture-focused. It does not define detailed trading formulas, UI visual design, or vendor-specific data-provider decisions.

Related documents:

| File | Purpose |
| --- | --- |
| `/docs/00-project-plan.md` | Project vision, MVP boundary, and roadmap |
| `/docs/01-product-requirements.md` | Product workflows, screens, and user-facing requirements |
| `/docs/02-trading-strategy-requirements.md` | Strategy rules, indicators, scoring, and risk logic |
| `/docs/02a-trading-concepts-glossary.md` | Trading concepts used by the strategy document |
| `/docs/04-data-sources.md` | Data providers, limits, and freshness rules |
| `/docs/05-dashboard-design.md` | Dashboard layout and UI behavior |
| `/docs/06-risk-and-backtesting.md` | Risk controls and validation methods |
| `/docs/07-cost-and-operations.md` | Cost estimates and operating constraints |
| `/docs/08-execution-tracker-v1.0.md` | Current project progress |
| `/docs/09-decision-log.md` | Accepted project decisions |
| `/docs/10-ai-working-guidelines.md` | AI workflow and engineering standards |

---

## 2. Architecture Summary

PoorToPour MVP should use a simple local-first web architecture:

```text
React Dashboard
      |
      v
FastAPI Backend
      |
      +--> Scanner / Strategy Services
      +--> Market Data Services
      +--> Indicator Services
      +--> Risk/Reward Services
      +--> Job Scheduler
      |
      v
PostgreSQL Database
```

MVP principle:

> Use a modular monolith before splitting into multiple services.

The MVP should not start with microservices, complex event streaming, distributed workers, or agent orchestration. Those may become useful later, but they add unnecessary complexity before the scanner proves useful.

---

## 3. Recommended Stack

## 3.1 MVP Stack

| Layer | Recommendation | Reason |
| --- | --- | --- |
| Frontend | React + TypeScript | Strong dashboard ecosystem and type safety |
| Backend API | Python FastAPI | Clean API development and strong Python data ecosystem |
| Database | PostgreSQL | Reliable relational store for scans, symbols, candles, and results |
| Data analysis | pandas / numpy | Mature financial/time-series computation support |
| Technical indicators | Internal `IndicatorService` with optional open-source libraries | Avoids reinventing standard indicator math while preserving PoorToPour-owned outputs |
| Scheduling | APScheduler first | Simple local scheduled jobs |
| Charting | TradingView Lightweight Charts or similar | Candlestick charts and overlays |
| Local runtime | Docker Compose | Repeatable local setup |
| Testing | pytest + frontend test tools | Backend logic and UI confidence |
| Formatting/linting | Ruff/Black for Python, ESLint/Prettier for frontend | Consistency and maintainability |

---

## 3.2 Post-MVP Additions

| Need | Possible Addition | When |
| --- | --- | --- |
| Background job scaling | Celery + Redis or RQ | When jobs become slow or need retries |
| Time-series optimization | TimescaleDB | When candle/indicator storage grows |
| Auth | Simple password/OAuth/proxy auth | If hosted beyond private local network |
| Observability | Structured logs + metrics | Before paper trading |
| Alerts | Email/Telegram/Discord | MVP+ or post-MVP |
| AI summaries | LLM provider service | After scanner proves useful |
| Paper trading | Trade simulation module | After backtesting design |
| Broker integration | Broker connector | After paper trading and risk gates |

---

## 4. Architectural Principles

## 4.1 Modular Monolith First

Use one backend application with clear module boundaries.

Pros:

- simpler deployment;
- easier local development;
- easier refactoring;
- fewer network boundaries;
- enough for personal MVP.

Cons:

- requires discipline to keep modules separated;
- can become messy if boundaries are ignored.

Decision:

> Start with a modular monolith. Split services only when there is real pressure.

---

## 4.2 Provider Abstraction

All external data providers must sit behind provider interfaces.

Do not let the strategy engine directly depend on vendor-specific response shapes.

Example provider boundaries:

```text
MarketDataProvider
CompanyProfileProvider
EarningsProvider
NewsProvider
PredictionMarketProvider
PoliticalTradeProvider
```

Benefits:

- easier to switch vendors;
- easier testing with fixtures;
- clearer data normalization;
- lower vendor lock-in.

---

## 4.3 Deterministic Strategy Core

The scanner should be deterministic.

Same inputs should produce same outputs.

The strategy core should not call LLMs, web APIs, or UI code directly.

Benefits:

- explainable;
- backtestable;
- testable;
- safer before automation.

---

## 4.4 Traceability Everywhere

Every scan result should be traceable to:

- scan run ID;
- data provider;
- source data timestamp;
- indicator calculation timestamp;
- strategy version;
- rule pass/fail output;
- score breakdown;
- caution flags.

This is essential for debugging and future backtesting.

---

## 4.5 Cost-Aware Operations

Architecture must support:

- local-first development;
- configurable universe size;
- configurable scan frequency;
- provider call logging;
- AI feature toggles;
- cache reuse;
- job run history;
- future cost dashboard.

---

## 4.6 Indicator Build-vs-Buy Boundary

PoorToPour should not reinvent standard technical indicator math unless the calculation is trivial or project-specific.

Decision:

> Use open-source technical-analysis libraries where practical for standard indicator calculations, but keep setup detection, scoring, risk/reward, caution flags, and strategy decisions in-house.

Recommended boundary:

| Area | Ownership | Reason |
| --- | --- | --- |
| SMA, rolling highs/lows, relative volume | In-house or pandas-native | Simple, transparent calculations |
| RSI, ATR, MACD, Bollinger Bands | Library-assisted through internal wrapper | Avoids subtle formula and edge-case bugs |
| Setup detection | In-house | Core PoorToPour strategy logic |
| Candidate scoring | In-house | Must be explainable and versioned |
| Risk/reward estimates | In-house | Safety-critical and project-specific |
| Caution flags | In-house | Must match project risk philosophy |
| Rule pass/fail outputs | In-house | Required for dashboard explanations |
| Provider normalization | In-house | Avoids vendor lock-in |

The practical rule:

> Libraries can calculate RSI. They should not decide whether PoorToPour labels a candidate as Actionable.

## 4.7 Safety Before Automation

Broker execution must not exist in MVP.

Architecture should leave a safe path toward automation later, but live execution must require:

- validated strategy rules;
- backtesting;
- paper trading;
- risk controls;
- kill switch;
- audit logs;
- manual override.

---

## 5. System Context

## 5.1 MVP System Context

```text
User
 |
 | opens dashboard / triggers scan
 v
React Frontend
 |
 | REST API calls
 v
FastAPI Backend
 |
 | reads/writes
 v
PostgreSQL
 |
 | background jobs fetch data
 v
External Data Providers
```

MVP external providers:

- market data provider;
- company profile provider;
- earnings provider.

Post-MVP providers:

- news provider;
- social provider;
- Polymarket/prediction-market provider;
- political-trade disclosure provider;
- broker provider;
- LLM provider.

---

## 5.2 High-Level Data Flow

```text
1. Load symbol universe
2. Fetch/update OHLCV data
3. Normalize and store price data
4. Compute indicators
5. Run setup detectors
6. Calculate scores
7. Estimate risk/reward
8. Attach caution flags
9. Store scan run and candidates
10. Display results in dashboard
```

Important:

> The dashboard should read stored scan results. It should not recompute strategy logic in the browser.

---

## 6. Backend Architecture

## 6.1 Backend Responsibilities

The FastAPI backend should handle:

- API endpoints;
- input validation;
- database access;
- market data ingestion;
- indicator calculations;
- scanner execution;
- score generation;
- risk/reward calculations;
- scheduled jobs;
- job status tracking;
- provider abstraction;
- configuration management.

---

## 6.2 Suggested Backend Module Structure

Suggested initial backend structure:

```text
backend/
  app/
    main.py
    api/
      routes/
        health.py
        symbols.py
        scans.py
        candidates.py
        config.py
    core/
      config.py
      logging.py
      errors.py
      time.py
    db/
      session.py
      models/
      repositories/
      migrations/
    providers/
      base.py
      market_data/
      company_profile/
      earnings/
    services/
      universe_service.py
      market_data_service.py
      indicator_service.py
      scanner_service.py
      scoring_service.py
      risk_service.py
      scan_run_service.py
      config_service.py
    strategy/
      indicators/
      setups/
        breakout.py
        pullback_continuation.py
        relative_strength.py
      scoring.py
      caution_flags.py
      risk_reward.py
    jobs/
      scheduler.py
      daily_scan_job.py
      weekly_scan_job.py
      data_refresh_job.py
    schemas/
      symbols.py
      scans.py
      candidates.py
      config.py
    tests/
```

Notes:

- `strategy/` should contain deterministic trading logic.
- `services/` should orchestrate application workflows.
- `providers/` should isolate external APIs.
- `repositories/` should isolate database access.
- `api/routes/` should stay thin.

---

## 6.3 Backend Layering Rule

Recommended dependency direction:

```text
API routes
  -> services
    -> strategy modules
    -> repositories
    -> providers
      -> external APIs
```

Avoid:

- strategy code calling API routes;
- strategy code reading from database directly;
- frontend reimplementing strategy logic;
- provider-specific data leaking into strategy logic.

---

## 7. Frontend Architecture

## 7.1 Frontend Responsibilities

The React dashboard should handle:

- dashboard layout;
- latest scan summary;
- candidate ranking table;
- candidate detail page;
- chart visualization;
- scan history page;
- settings page;
- API integration;
- loading/error states.

The frontend should not handle:

- indicator calculations;
- strategy scoring;
- data-provider calls;
- secret management;
- broker logic;
- AI prompt orchestration.

---

## 7.2 Suggested Frontend Structure

Suggested initial frontend structure:

```text
frontend/
  src/
    app/
      App.tsx
      routes.tsx
    components/
      layout/
      charts/
      tables/
      cards/
      status/
    features/
      dashboard/
      candidates/
      scans/
      settings/
    api/
      client.ts
      scans.api.ts
      candidates.api.ts
      symbols.api.ts
      config.api.ts
    models/
      scan.ts
      candidate.ts
      symbol.ts
      config.ts
    hooks/
      useLatestScan.ts
      useCandidateDetail.ts
      useScanHistory.ts
    utils/
      formatting.ts
      dates.ts
    tests/
```

---

## 7.3 Frontend State Management

MVP recommendation:

> Use React Query / TanStack Query or simple fetch hooks before adding global state management.

Reason:

Most MVP frontend state is server state:

- latest scan;
- candidate list;
- candidate detail;
- scan history;
- settings.

Avoid Redux/Zustand unless there is a real need.

Pros:

- simpler;
- better caching;
- fewer custom state bugs.

Cons:

- may need more structure later if dashboard interactions become complex.

---

## 7.4 Frontend Data Freshness

Every major screen should show data freshness.

Examples:

| Screen | Freshness Display |
| --- | --- |
| Dashboard Home | Last scan timestamp, data date |
| Candidate Detail | Last indicator calculation timestamp |
| Scan History | Scan run status and completion time |
| Settings | Last config update if applicable |

## 7.5 Future Command Palette

MVP+ may include a command palette for:

- ticker search;
- opening candidate details;
- navigating to scans/settings;
- opening manual scan modal;
- jumping to watchlist items.

This is a UX enhancement, not an MVP dependency.

---

## 8. Database Architecture

## 8.1 Database Choice

Use PostgreSQL for MVP.

Reasons:

- reliable;
- familiar;
- supports relational scan metadata;
- supports JSON fields where useful;
- can evolve toward TimescaleDB if time-series volume grows.

---

## 8.2 Core Tables

Suggested MVP tables:

| Table | Purpose |
| --- | --- |
| `symbols` | Stock universe and symbol metadata |
| `daily_bars` | Daily OHLCV data |
| `company_profiles` | Basic company context |
| `earnings_events` | Last/next earnings context |
| `indicator_snapshots` | Computed indicators for scan dates |
| `scan_runs` | Each scan execution |
| `scan_candidates` | Candidate tickers produced by scans |
| `candidate_rule_results` | Rule pass/fail details |
| `candidate_scores` | Score breakdowns |
| `candidate_risk_estimates` | Entry, stop, target, R/R estimates |
| `job_runs` | Scheduled/manual job history |
| `app_config` | Basic configurable settings |

---

## 8.3 Post-MVP Tables

Possible later tables:

| Table | Purpose |
| --- | --- |
| `watchlist_items` | Saved user watchlist |
| `news_headlines` | Headlines and ticker mappings |
| `social_mentions` | Mention counts and source summaries |
| `prediction_market_events` | Polymarket/event context |
| `political_trades` | Public political disclosure data |
| `backtest_runs` | Historical validation runs |
| `backtest_results` | Backtest output |
| `paper_trades` | Simulated trade records |
| `alerts` | Notification rules |
| `ai_usage_logs` | Token/cost tracking |
| `ai_summaries` | Cached AI-generated summaries |
| `broker_accounts` | Future only, encrypted/safe design required |
| `trade_orders` | Future only, not MVP |

---

## 8.4 Data Modeling Guidelines

Use normalized relational tables for core data.

Use JSON columns selectively for:

- provider raw payload snapshots;
- rule output details;
- score breakdown metadata;
- experimental context fields.

Rules:

- Do not store secrets in normal config tables.
- Do not store giant raw payloads indefinitely.
- Keep provider-specific fields isolated.
- Store timestamps carefully.
- Distinguish market data date from scan run timestamp.

---

## 8.5 Timestamp Requirements

Important timestamps:

| Timestamp | Meaning |
| --- | --- |
| `market_date` | Date of the market data candle |
| `retrieved_at` | When data was fetched from provider |
| `computed_at` | When indicators/scores were calculated |
| `scan_started_at` | When scan job began |
| `scan_completed_at` | When scan job ended |
| `created_at` | Record creation time |
| `updated_at` | Record update time |

Use timezone-aware timestamps for application events.

Market dates can be date-only for daily bars.

---

## 9. Data Provider Architecture

## 9.1 Provider Interface Pattern

All provider modules should return normalized internal DTOs.

Example conceptual interface:

```text
MarketDataProvider
  get_daily_bars(symbol, start_date, end_date) -> list[DailyBar]
  get_latest_daily_bar(symbol) -> DailyBar
```

Provider output should be mapped before storage.

Do not store provider response shapes directly as application models.

---

## 9.2 Provider Error Handling

Providers can fail.

The system must handle:

- rate limits;
- missing symbols;
- stale responses;
- malformed data;
- network errors;
- partial failures.

Provider errors should:

- be logged;
- be linked to job runs;
- not crash the entire scan if avoidable;
- create `Blocked` or warning states when required data is unavailable.

---

## 9.3 Provider Call Logging

MVP should log provider usage at job level.

Suggested fields:

| Field | Purpose |
| --- | --- |
| provider_name | Which provider was used |
| endpoint_name | Which endpoint/function |
| symbol | Optional ticker |
| job_run_id | Link to job |
| status | success/failure |
| started_at | timing |
| completed_at | timing |
| error_message | troubleshooting |
| estimated_cost | optional future field |

---

## 10. Strategy Engine Architecture

## 10.1 Strategy Engine Responsibility

The strategy engine should:

- receive normalized market data and indicators;
- evaluate setup rules;
- produce rule results;
- calculate candidate scores;
- generate caution flags;
- estimate risk/reward;
- return explainable candidate objects.

It should not:

- call external providers;
- read directly from the database;
- generate UI components;
- call LLMs;
- place trades.

---

## 10.2 Indicator Service Boundary

Indicator calculations should be wrapped behind an internal `IndicatorService`.

The service may use third-party libraries internally, but all outputs must be normalized into PoorToPour-owned models before they reach scanner, scoring, risk, or dashboard logic.

Conceptual boundary:

```text
IndicatorService
  -> may use pandas / numpy / ta / TA-Lib / other vetted libraries internally
  -> returns PoorToPour-owned IndicatorSnapshot objects
```

Rules:

- Do not let third-party library-specific objects leak into strategy modules.
- Pin dependency versions.
- Keep dependency usage isolated to the indicator layer.
- Add fixtures and tests for indicator outputs.
- Compare critical indicator outputs against trusted sample data.
- Allow library replacement without rewriting setup detectors.
- Prefer simple in-house/pandas calculations for trivial rolling metrics.
- Use libraries for indicators with formula nuances, warm-up periods, and edge cases.

Initial recommendation:

| Indicator | Preferred Implementation |
| --- | --- |
| SMA 20/50/200 | pandas-native or in-house |
| EMA 8/21 | pandas-native or library |
| RSI 14 | library-assisted |
| ATR 14 | library-assisted |
| MACD 12/26/9 | library-assisted if included |
| Bollinger Bands | library-assisted if included |
| Relative volume | in-house |
| 20-day / 50-day highs and lows | pandas-native or in-house |
| 52-week high/low | pandas-native or in-house |
| Relative strength vs SPY | in-house |

Preferred MVP library direction:

| Option | Position |
| --- | --- |
| `ta` | Practical first choice because it is pandas/numpy-based and simple to install |
| TA-Lib | Mature classic choice, but C dependency may complicate local/Docker setup |
| vectorbt | Better suited for later research/backtesting than first scanner MVP |
| talipp | Interesting later for incremental/intraday indicators |

## 10.3 Strategy Flow

```text
Input:
  Symbol data
  Daily bars
  Indicator values
  Company/earnings context

Process:
  Apply universe filters
  Compute or load indicators
  Evaluate setup detectors
  Calculate score
  Generate caution flags
  Estimate risk/reward
  Assign candidate status

Output:
  Candidate result
  Rule pass/fail details
  Score breakdown
  Risk estimate
  Warnings
```

---

## 10.4 Setup Detector Interface

Each setup detector should follow the same conceptual pattern:

```text
SetupDetector
  name
  evaluate(input) -> SetupEvaluation
```

Example setup detectors:

- `BreakoutDetector`
- `PullbackContinuationDetector`
- `RelativeStrengthLeaderDetector`

Each detector should output:

| Field | Purpose |
| --- | --- |
| setup_type | Breakout, pullback, relative strength |
| passed | Whether setup matched |
| required_rule_results | Required rule outputs |
| preferred_rule_results | Preferred rule outputs |
| explanation_facts | Facts used for dashboard explanation |
| raw_score | Setup-specific score |

---

## 10.5 Rule Result Model

Each rule should produce structured output.

Example fields:

| Field | Purpose |
| --- | --- |
| rule_id | Stable identifier such as `BO-001` |
| name | Human-readable rule |
| passed | true/false |
| severity | required/preferred/info |
| actual_value | Observed value |
| expected_value | Threshold or expectation |
| message | Explanation-ready text |

This makes the dashboard explanation data-driven.

---

## 10.6 Scoring Service

The scoring service should combine:

- setup match score;
- volume score;
- relative strength score;
- risk/reward score;
- context/caution score.

Scoring should be versioned.

Example:

```text
score_version = "mvp-v1"
```

This matters because future score changes should not make old scan results impossible to interpret.

---

## 10.7 Risk Service

The risk service should estimate:

- entry zone;
- invalidation level;
- stop estimate;
- target estimate;
- risk/reward ratio;
- ATR context;
- position sizing if account settings are configured later.

Risk estimates are research estimates.

They must not be treated as execution instructions.

---

## 11. Job Architecture

## 11.1 MVP Jobs

Required MVP jobs:

| Job | Purpose |
| --- | --- |
| `daily_scan_job` | Run daily scan after market close |
| `weekly_scan_job` | Run weekly scan |
| `symbol_universe_refresh_job` | Refresh S&P 500 universe when needed |
| `market_data_refresh_job` | Fetch/update OHLCV data |
| `company_profile_refresh_job` | Refresh company profile context |
| `earnings_refresh_job` | Refresh earnings context |
| `manual_scan_job` | Run scan on user request |

---

## 11.2 Job Execution Model

MVP recommendation:

> Use APScheduler inside the backend process for local-first MVP.

Pros:

- simple;
- low cost;
- easy to run locally;
- good enough for daily/weekly jobs.

Cons:

- less robust than a separate worker system;
- jobs stop if backend is down;
- not ideal for high-volume parallel work.

Post-MVP:

Move to Celery/RQ + Redis if jobs become slow, require retries, or need stronger isolation.

### 11.2.1 Future Job System Upgrade

APScheduler remains the MVP scheduler.

If PoorToPour adds alerts, AI summaries, paper-trading checks, scan briefings, or more frequent provider refreshes, migrate to a more durable job system such as Celery + Redis, RQ + Redis, Temporal, or another workflow engine.

The upgrade should happen only when APScheduler becomes a real limitation.

---

## 11.3 Job Run Tracking

Every job must write a `job_runs` record.

Suggested fields:

| Field | Purpose |
| --- | --- |
| job_run_id | Unique ID |
| job_type | Daily scan, market data refresh, etc. |
| status | pending/running/succeeded/failed/partial |
| started_at | Start timestamp |
| completed_at | End timestamp |
| symbols_requested | Requested symbols |
| symbols_processed | Processed symbols |
| candidates_found | Scan output count |
| provider_calls | Usage tracking |
| estimated_cost | Future cost tracking |
| error_summary | Troubleshooting |
| logs_ref | Optional future link |

---

## 11.4 Failure Handling

Jobs should support partial success.

Example:

If 500 symbols are scanned and 7 fail provider fetch, the job can complete as `partial` with warnings rather than failing everything.

Rules:

- Do not silently ignore failures.
- Store failed symbol details.
- Surface partial scan status on dashboard.
- Block candidates with missing required data.
- Allow manual retry.

---

## 12. API Architecture

## 12.1 API Style

Use REST API for MVP.

Reason:

- simple;
- clear;
- easy for React dashboard;
- no need for GraphQL yet.

---

## 12.2 MVP API Endpoints

Suggested endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| GET | `/api/config` | Read app settings |
| PUT | `/api/config` | Update basic settings |
| GET | `/api/symbols` | List symbols/universe |
| GET | `/api/scans/latest` | Latest scan summary |
| GET | `/api/scans` | Scan history |
| GET | `/api/scans/{scan_id}` | Scan details |
| POST | `/api/scans/run` | Trigger manual scan |
| GET | `/api/candidates` | Candidate list, usually latest scan |
| GET | `/api/candidates/{symbol}` | Latest candidate detail |
| GET | `/api/candidates/{symbol}/chart` | Chart data |
| GET | `/api/jobs` | Job history |
| GET | `/api/jobs/{job_run_id}` | Job detail |

---

## 12.3 API Design Rules

API responses should:

- include timestamps;
- include data status;
- include stable IDs;
- avoid exposing secrets;
- avoid exposing raw provider payloads by default;
- return structured errors;
- support pagination for scan history;
- support filtering candidate list by setup/status.

---

## 13. Configuration Architecture

## 13.1 MVP Config

Config should include:

| Config | Default |
| --- | --- |
| stock universe | S&P 500 |
| scan interval | daily and weekly |
| max candidates | 25 |
| minimum price | $5 |
| minimum average dollar volume | $20M |
| enabled setup types | breakout, pullback, relative strength |
| AI enabled | false |
| monthly AI budget | $0 |
| manual scan enabled | true |

---

## 13.2 Config Storage

MVP options:

1. Environment variables for technical settings.
2. Database `app_config` table for product settings.
3. Local config file for early development.

Recommendation:

> Use environment variables for secrets and infrastructure settings. Use database-backed app config for user-facing scan settings once the dashboard settings page exists.

---

## 13.3 Secrets Management

Secrets include:

- provider API keys;
- database credentials;
- future LLM keys;
- future broker credentials.

Rules:

- never commit secrets;
- do not expose secrets to frontend;
- use `.env` locally;
- use hosting provider secrets when deployed;
- broker secrets require stricter future design.

---

## 14. AI Architecture

## 14.1 MVP AI Decision

AI is off in MVP.

No AI is required for:

- indicator calculations;
- setup detection;
- candidate scoring;
- risk/reward estimates;
- candidate status.

---

## 14.2 Post-MVP AI Service

When introduced, AI should be isolated behind an `AiResearchService`.

Possible responsibilities:

- summarize candidate evidence;
- summarize company background;
- summarize recent headlines;
- generate bull/bear notes;
- produce human-readable briefings.

AI service must:

- log model usage;
- estimate cost;
- respect budget caps;
- cache outputs;
- avoid changing deterministic strategy scores.

---

## 14.3 AI Usage Logging

Future table:

`ai_usage_logs`

Suggested fields:

| Field | Purpose |
| --- | --- |
| model | Model used |
| prompt_type | Candidate summary, news summary, etc. |
| input_tokens | Cost tracking |
| output_tokens | Cost tracking |
| estimated_cost | Budget control |
| scan_run_id | Traceability |
| symbol | Optional ticker |
| created_at | Timestamp |

---

## 15. Security Architecture

## 15.1 MVP Security

Local MVP:

- no public internet exposure required;
- environment variables for secrets;
- local database;
- no broker credentials;
- no user authentication required if purely local.

Hosted MVP:

- HTTPS required;
- dashboard access should be restricted;
- secrets must be managed by hosting environment;
- logs must not expose secrets;
- CORS must be restricted;
- database should not be publicly open.

---

## 15.2 Future Broker Security

Broker integration is not MVP.

Before broker integration:

- define broker threat model;
- encrypt sensitive tokens;
- separate paper/live environments;
- require kill switch;
- require max position/risk limits;
- require audit logs;
- require manual disable switch;
- require clear account status display.

---

## 16. Testing Architecture

## 16.1 Backend Testing

Backend tests should cover:

| Area | Test Type |
| --- | --- |
| Indicator calculations | Unit |
| Setup detectors | Unit |
| Scoring | Unit |
| Risk/reward estimates | Unit |
| Provider normalization | Unit |
| Repository queries | Integration |
| API endpoints | Integration |
| Job execution | Integration |
| Failure handling | Unit/integration |

---

## 16.2 Indicator and Dependency Testing

Indicator-related tests should include:

| Test Area | Purpose |
| --- | --- |
| Known-value fixtures | Confirm indicators match expected outputs |
| Warm-up periods | Confirm early rows with insufficient data are handled consistently |
| Missing data | Confirm null/NaN behavior does not create false signals |
| Zero volume / zero price edge cases | Prevent divide-by-zero and invalid calculations |
| Library wrapper tests | Ensure third-party outputs are normalized correctly |
| Regression fixtures | Prevent accidental strategy drift after dependency updates |

Dependency rules:

- Pin versions for indicator libraries.
- Avoid large dependency trees unless justified.
- Review maintenance activity and license before adoption.
- Keep wrappers small and replaceable.
- Do not couple strategy rules directly to third-party APIs.

## 16.3 Frontend Testing

Frontend tests should cover:

| Area | Test Type |
| --- | --- |
| Candidate ranking table | Component |
| Candidate detail display | Component |
| Status/caution rendering | Component |
| API error states | Component |
| Loading states | Component |
| Settings form | Component |
| Chart rendering smoke test | Component/e2e later |

---

## 16.4 Golden Fixtures

For strategy logic, use fixed sample data fixtures.

Examples:

| Fixture | Purpose |
| --- | --- |
| clean breakout stock | Should trigger breakout |
| failed breakout stock | Should not trigger breakout |
| healthy pullback stock | Should trigger pullback |
| broken trend stock | Should avoid |
| stale data stock | Should block |
| low volume stock | Should filter or warn |

Golden fixtures help prevent accidental strategy drift.

---

## 17. Observability and Operations

## 17.1 MVP Observability

MVP should include:

- structured application logs;
- job run records;
- provider call records;
- scan status;
- error summaries;
- data freshness labels.

---

## 17.2 Post-MVP Observability

Later add:

- cost dashboard;
- alerting on failed scans;
- provider outage alerts;
- AI budget alerts;
- dashboard uptime monitoring;
- database backup status;
- paper-trading performance monitoring.

---

## 18. Development Environment

## 18.1 Local Development

Recommended local services:

```text
docker-compose.yml
  postgres
  backend
  frontend
```

Optional later:

```text
redis
worker
scheduler
```

---

## 18.2 Environment Files

Example local files:

```text
.env.example
.env.local
```

Rules:

- commit `.env.example`;
- never commit real `.env`;
- document required variables;
- use safe placeholder values.

---

## 18.3 Recommended Root Repo Structure

Suggested repo structure:

```text
poor-to-pour/
  docs/
  backend/
  frontend/
  docker-compose.yml
  .env.example
  README.md
  Makefile
```

Optional later:

```text
scripts/
infra/
notebooks/
```

---

## 19. Deployment Architecture

## 19.1 MVP Deployment

Initial deployment:

> Local only.

Reason:

- cheapest;
- simplest;
- no public security risk;
- enough for first development.

---

## 19.2 Hosted MVP Deployment

When ready:

Option A: VPS with Docker Compose.

```text
DigitalOcean Droplet / equivalent VPS
  -> Docker Compose
    -> frontend static server
    -> FastAPI backend
    -> PostgreSQL
```

Option B: Platform-as-a-service.

```text
Render / Railway
  -> frontend service
  -> backend service
  -> managed Postgres
```

Provider choice is deferred until implementation needs are clearer.

---

## 19.3 Deployment Rules

- No public hosted dashboard without access control.
- No secrets in code.
- Database backups required before important schema changes.
- Use HTTPS if hosted.
- Use provider logs carefully and avoid secret leakage.

---

## 20. Future Architecture Path

## 20.1 MVP

```text
React + FastAPI + PostgreSQL + APScheduler
```

Focus:

- local dashboard;
- daily data;
- deterministic scanner;
- scan history.

---

## 20.2 MVP+

Add:

- watchlist;
- exports;
- better filters;
- command palette / global ticker search;
- scanner-aware watchlist;
- chart signal markers and detected-signal cards;
- market regime panel;
- limited AI summaries;
- cost logging;
- improved job UI.

---

## 20.3 Post-MVP Research Desk

Add:

- news headlines;
- earnings enrichment;
- backtesting UI;
- improved provider abstraction;
- possible Redis/job queue or workflow engine;
- alerting;
- daily/weekly scan briefings;
- sector/theme scanner grid.

---

## 20.4 Paper Trading

Add:

- simulated trades;
- position tracking;
- performance metrics;
- slippage assumptions;
- strategy validation dashboard.

---

## 20.5 Controlled Automation

Only after validation:

- broker connector;
- order preview;
- strict risk limits;
- kill switch;
- audit logs;
- live/paper environment separation.

---

## 21. Architecture Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| ARCH-D-001 | Use modular monolith for MVP | Simpler than microservices and enough for personal MVP |
| ARCH-D-002 | Use FastAPI backend | Strong Python data ecosystem and clean API framework |
| ARCH-D-003 | Use React + TypeScript frontend | Strong dashboard stack and type safety |
| ARCH-D-004 | Use PostgreSQL | Reliable store for symbols, candles, scans, and results |
| ARCH-D-005 | Use APScheduler initially | Simple scheduled jobs for local-first MVP |
| ARCH-D-006 | Use provider abstraction | Avoid vendor lock-in and simplify testing |
| ARCH-D-007 | Keep strategy engine deterministic | Required for explainability and backtesting |
| ARCH-D-008 | Dashboard reads stored results, not recomputed logic | Keeps UI simple and traceable |
| ARCH-D-009 | AI is isolated and off in MVP | Prevents black-box strategy and cost creep |
| ARCH-D-010 | Broker integration is excluded from MVP architecture | Avoids unsafe execution before validation |
| ARCH-D-011 | Use open-source libraries for standard indicator calculations where practical | Avoids subtle formula and edge-case bugs |
| ARCH-D-012 | Keep PoorToPour setup detection, scoring, risk/reward, and caution flags in-house | These are core strategy and safety logic |
| ARCH-D-013 | Wrap indicator libraries behind an internal `IndicatorService` | Allows dependency replacement without rewriting scanner logic |

---

## 22. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-ARCH-001 | Should backend and frontend live in one repo or separate repos? | One repo | 🟦 Open |
| Q-ARCH-002 | Should PostgreSQL run locally only at first? | Yes | 🟦 Open |
| Q-ARCH-003 | Should APScheduler run inside FastAPI or separate process? | Inside backend for MVP | 🟦 Open |
| Q-ARCH-004 | Should strategy outputs store full rule details or summaries only? | Full rule details | 🟦 Open |
| Q-ARCH-005 | Should indicator snapshots be stored or recomputed on demand? | Store scan-time snapshots | 🟦 Open |
| Q-ARCH-006 | Should scan settings be DB-backed in MVP or config-file based first? | DB-backed if easy, config file acceptable first | 🟦 Open |
| Q-ARCH-007 | Should frontend use TanStack Query? | Yes, likely | 🟦 Open |
| Q-ARCH-008 | Should we include Redis in MVP? | No | 🟦 Open |
| Q-ARCH-009 | Should we include auth in local MVP? | No | 🟦 Open |
| Q-ARCH-010 | Should hosted MVP require simple auth immediately? | Yes | 🟦 Open |
| Q-ARCH-011 | Which indicator library should be used first? | Leaning `ta`, confirm during implementation | 🟦 Open |

---

## 23. MVP Architecture Definition of Done

The architecture is MVP-ready when:

| ID | Requirement | Status |
| --- | --- | --- |
| ARCH-001 | Repo structure is defined | Required |
| ARCH-002 | Backend module boundaries are defined | Required |
| ARCH-003 | Frontend module boundaries are defined | Required |
| ARCH-004 | Database core tables are identified | Required |
| ARCH-005 | Data flow from provider to dashboard is defined | Required |
| ARCH-006 | Strategy engine boundary is defined | Required |
| ARCH-007 | Job scheduling approach is defined | Required |
| ARCH-008 | API endpoint list is drafted | Required |
| ARCH-009 | Config and secrets approach is defined | Required |
| ARCH-010 | Testing architecture is defined | Required |
| ARCH-011 | Deployment path is defined | Required |
| ARCH-012 | Future automation boundaries are clearly excluded from MVP | Required |
| ARCH-013 | Indicator calculation boundary is defined | Required |
| ARCH-014 | Third-party indicator dependency rules are defined | Required |

---

## 24. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial technical architecture document | Jesse + AI |
| 2026-04-30 | v0.2 | Added indicator build-vs-buy decision, `IndicatorService` boundary, and dependency testing rules | Jesse + AI |
| 2026-05-14 | v0.3 | Added MVP+ command palette and future job-system upgrade path from external review | Jesse + AI |
