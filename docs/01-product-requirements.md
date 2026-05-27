# PoorToPour Product Requirements

**Project:** PoorToPour
**Description:** From broke to pouring champagne.
**Document:** `/docs/01-product-requirements.md`
**Date created:** 2026-04-30
**Last updated:** 2026-05-27
**Status:** Draft v0.6

---

## 1. Purpose

This document defines PoorToPour from a product and user-experience perspective.

It answers:

- What does the user need to do?
- What does the app display?
- What workflows must the MVP support?
- What is in scope for the first usable version?
- What is intentionally deferred?
- What product constraints should guide implementation?

This document does **not** define detailed trading formulas, database schema, provider selection, or implementation architecture. Those belong in separate documents.

Related documents:

| File | Purpose |
| --- | --- |
| `/docs/00-project-plan.md` | Project vision, MVP boundary, and roadmap |
| `/docs/02-trading-strategy-requirements.md` | Trading setups, indicators, scoring, and risk logic |
| `/docs/03-technical-architecture.md` | System design, modules, services, and data flow |
| `/docs/04-data-sources.md` | Data providers, source limits, and freshness rules |
| `/docs/05-dashboard-design.md` | Dashboard layout and UI behavior |
| `/docs/06-risk-and-backtesting.md` | Risk controls and validation methods |
| `/docs/07-cost-and-operations.md` | Cost estimates, operating modes, hosting, and budget controls |
| `/docs/08-execution-tracker-v1.0.md` | Current project progress |
| `/docs/09-decision-log.md` | Accepted project decisions |
| `/docs/10-ai-working-guidelines.md` | AI workflow and engineering standards |

---

## 2. Product Overview

PoorToPour is a personal trading research dashboard that scans a defined U.S. equity universe, identifies explainable technical trade setups, ranks candidates, and presents the evidence in a clean dashboard.

The MVP is designed to help the user manually review potential swing-trade candidates.

The MVP does **not** execute trades automatically.

Product role by phase:

| Stage | Product Role |
| --- | --- |
| MVP | Research assistant |
| MVP+ | Research assistant with watchlist and convenience features |
| Post-MVP | Research and monitoring assistant |
| Later | Paper-trading system |
| Final vision | Controlled automated trading assistant |

---

## 3. Target User

Primary user:

> A technically capable individual trader/developer who wants a personal research system for U.S. equities.

The first user is Jesse.

The product should assume the user is comfortable with trading concepts, charts, and technical indicators, but the app should still explain why a candidate was selected.

User goals:

| Goal | Product Implication |
| --- | --- |
| Find trade ideas faster | Provide ranked scan results |
| Avoid random chart browsing | Use setup-based filtering |
| Understand why a ticker appears | Show explanations and score breakdowns |
| Review visual evidence | Show candlestick chart, volume, and indicators |
| Avoid obvious risk traps | Show caution flags and earnings context |
| Manage trade risk | Show entry zone, invalidation, stop estimate, target estimate, and risk/reward |
| Track whether setups were useful | Store scan history for later review and validation |

---

## 4. MVP Product Scope

The MVP should deliver a local-first web dashboard that allows the user to run or view daily and weekly stock scans, review ranked long-only swing-trade candidates, inspect chart evidence, and understand why each candidate was selected.

MVP summary:

> PoorToPour MVP is a local-first trading research dashboard for reviewing explainable long-only swing-trade setups from a limited U.S. equity universe.

### 4.1 In Scope for MVP

| Feature | MVP | Notes |
| --- | --- | --- |
| Dashboard home | Yes | Main command center |
| Latest scan results | Yes | Ranked list of trade candidates |
| Candidate detail page | Yes | Chart, indicators, score, explanation, risk/reward |
| Manual scan trigger | Yes | Useful for development and manual refresh |
| Scheduled scans | Yes | Daily and weekly |
| Scan history | Yes | Required for traceability |
| Basic scan settings | Yes | Universe, scan type, max candidates, basic filters |
| Basic company profile | Yes | Name, sector, industry, market cap |
| Basic earnings context | Yes | Last/next earnings date if available |
| Technical setup explanations | Yes | Explain why a ticker matched |
| Risk/reward estimate | Yes | Research estimate only |
| Data freshness labels | Yes | Show timestamps and stale/missing data states |
| Watchlist | No | MVP+ unless trivial |
| Sector scanner / market regime page | No | MVP+ unless explicitly re-approved |
| Alerts | No | Post-MVP |
| Intraday social/news scanning | No | Post-MVP |
| Broker execution | No | Later only after validation |
| AI summaries | No | Post-MVP |
| Multi-user support | No | Not required for personal MVP |

### 4.2 Out of Scope for MVP

The MVP should not include:

- Automated live trading.
- Broker integration.
- Options strategy generation.
- Short-selling setup detection.
- Full intraday day-trading engine.
- Social-media firehose ingestion.
- Polymarket/event-market trading logic.
- Politician-trade-based live signals.
- AI-generated trade decisions.
- Multi-user authentication.
- Mobile application.
- SaaS deployment architecture.

---

## 5. Product Principles

### 5.1 Evidence First

Every candidate must show why it appeared.

The product should avoid unexplained “buy this” style outputs. A candidate is only useful if the dashboard shows the evidence behind it.

### 5.2 Risk First

Every candidate should include basic risk context.

The MVP does not need perfect trade planning, but it should show:

- possible entry zone;
- invalidation area;
- stop-loss estimate;
- target estimate;
- estimated risk/reward;
- caution flags.

### 5.3 Explainability Over Magic

PoorToPour should behave like a research workstation, not a fortune cookie with candlesticks.

The user should be able to inspect:

- which setup matched;
- which rules passed;
- which rules failed;
- what data was used;
- when the scan was run.

### 5.4 Local-First and Cost-Conscious

PoorToPour is a personal project. The MVP should be able to run locally and should avoid expensive always-on services.

Detailed cost modeling belongs in `/docs/07-cost-and-operations.md`.

### 5.5 Manual Review Before Automation

The MVP must support human review only.

Automated trade execution belongs to a later phase after:

- data quality is proven;
- scanner logic is tested;
- backtesting exists;
- paper trading exists;
- strict risk controls exist;
- a kill switch exists.

---

## 6. MVP User Workflows

## 6.1 Workflow 1 — View Latest Market Scan

User opens the dashboard and sees the latest scan results.

Required information:

| Element | Purpose |
| --- | --- |
| Last scan timestamp | Know data freshness |
| Scan type | Daily or weekly |
| Universe scanned | Know scope |
| Number of symbols scanned | Confirm scan coverage |
| Number of candidates found | Understand signal density |
| Top-ranked candidates | Main output |
| Setup type labels | Breakout, pullback continuation, relative strength |
| Candidate scores | Ranking signal |
| Caution flags | Surface obvious risks |
| Data status | Show success, partial, failed, stale, or missing data |

Success criteria:

- User can quickly understand whether the latest scan produced interesting candidates.
- User can see when the scan ran.
- User can click a candidate for deeper review.

---

## 6.2 Workflow 2 — Review One Candidate

User clicks a ticker from the ranked scan table and opens its detail page.

Required information:

| Element | Purpose |
| --- | --- |
| Ticker and company name | Identify candidate |
| Setup type | Explain category |
| Overall score | Summarize ranking |
| Status label | Actionable, Watch, Avoid, or Blocked |
| Candlestick chart | Review price action |
| Moving averages | Understand trend context |
| Volume | Confirm participation |
| RSI | Review momentum |
| Setup explanation | Explain why ticker appeared |
| Score breakdown | Show ranking components |
| Risk/reward card | Show basic trade planning context |
| Company snapshot | Provide business context |
| Earnings context | Avoid blind earnings risk |
| Data freshness | Show when values were calculated |

Success criteria:

- User can understand why the ticker appeared.
- User can decide whether to keep watching, reject, or manually research further.
- User can see whether data is fresh enough to trust.

---

## 6.3 Workflow 3 — Review Scan History

User can review previous scan runs.

Required information:

| Field | Purpose |
| --- | --- |
| Scan date/time | Historical reference |
| Scan type | Daily or weekly |
| Universe | What was scanned |
| Status | Successful, failed, partial |
| Symbols processed | Scan coverage |
| Candidates found | Signal density |
| Top candidates | Review past outputs |
| Error summary | Troubleshooting |

Success criteria:

- User can inspect previous results.
- User can compare signal frequency over time.
- User can later use historical scan output for validation and backtesting workflows.

---

## 6.4 Workflow 4 — Configure Basic Scan Settings

User can configure the basic scan behavior.

MVP settings:

| Setting | Default |
| --- | --- |
| Universe | S&P 500 |
| Scan interval | Daily and weekly |
| Max candidates shown | 25 |
| Minimum price | 5 USD |
| Minimum average daily dollar volume | 20 million USD |
| Setup types enabled | Breakout, pullback continuation, relative strength |
| Data freshness warning threshold | TBD |
| Manual scan allowed | Yes |

Success criteria:

- User can adjust basic scan behavior without code changes.
- Configuration remains simple enough to avoid dashboard clutter.

---

## 7. MVP Screens

## 7.1 Dashboard Home

Purpose:

Main command center for the latest scan.

Required sections:

| Section | MVP | Notes |
| --- | --- | --- |
| Latest scan summary | Yes | Timestamp, scan type, universe, status |
| Top candidate ranking table | Yes | Core MVP feature |
| Market snapshot | Maybe | Optional if easy |
| Caution summary | Yes | Earnings soon, stale data, failed providers |
| Manual scan button | Yes | Useful for development and manual refresh |
| Link to scan history | Yes | Traceability |

---

## 7.2 Candidate Detail Page

Purpose:

Deep review of one ticker.

Required sections:

| Section | MVP | Notes |
| --- | --- | --- |
| Candidate summary card | Yes | Ticker, company, setup, score, status |
| Chart section | Yes | Candles, volume, SMA, RSI |
| Setup explanation | Yes | Rule-level explanation |
| Score breakdown | Yes | Component scores |
| Risk/reward card | Yes | Entry, stop, target, R/R |
| Company snapshot | Yes | Sector, industry, market cap |
| Earnings context | Yes | Last/next earnings date where available |
| Recent headlines | No | Post-MVP |
| Social/event context | No | Post-MVP |
| Watchlist action | No | MVP+ unless trivial |

---

## 7.3 Scan History Page

Purpose:

Review prior scan runs.

Required sections:

| Section | MVP | Notes |
| --- | --- | --- |
| Scan run table | Yes | Date, type, universe, status |
| Candidate count | Yes | Signal density |
| Error/partial status | Yes | Troubleshooting |
| Link to scan results | Yes | Inspect past results |
| Performance outcome | No | Later with backtesting |

---

## 7.4 Settings Page

Purpose:

Control basic scan behavior.

Required sections:

| Section | MVP | Notes |
| --- | --- | --- |
| Universe settings | Yes | S&P 500 first |
| Scan schedule settings | Yes | Daily and weekly |
| Candidate filters | Yes | Price, volume, max results |
| Setup toggles | Yes | Enable/disable setup families |
| Provider configuration display | Maybe | Actual secrets should not be shown |
| AI settings | No | Post-MVP |
| Broker settings | No | Not allowed in MVP |

---

## 8. Candidate Ranking Table Requirements

The ranking table is the core MVP product surface.

Recommended columns:

| Column | Example | Purpose |
| --- | --- | --- |
| Rank | 1 | Candidate order |
| Ticker | NVDA | Symbol |
| Company | NVIDIA Corp. | Human-readable name |
| Setup | Breakout | Setup family |
| Status | Watch | Product-facing classification |
| Score | 86 | Ranking score |
| Price | 124.50 | Latest price used |
| Change % | +2.4% | Price movement |
| Relative volume | 2.1x | Participation strength |
| RSI | 64 | Momentum context |
| Distance from 20D high | +1.2% | Breakout context |
| Risk/reward | 2.4R | Basic attractiveness estimate |
| Caution flags | Earnings in 3 days | Risk context |
| Last updated | 2026-04-30 16:15 | Data freshness |

Table behavior:

- Sort by score by default.
- Allow filtering by setup type.
- Allow filtering by status.
- Show stale or missing data clearly.
- Link each ticker to its detail page.

---

## 9. Candidate Detail Requirements

## 9.1 Summary Card

Required fields:

| Field | Example |
| --- | --- |
| Ticker | MSFT |
| Company | Microsoft Corp. |
| Sector | Technology |
| Industry | Software |
| Setup | Pullback continuation |
| Overall score | 78 |
| Status | Watch |
| Last scan | 2026-04-30 16:15 |
| Data status | Fresh |

---

## 9.2 Chart Section

MVP chart requirements:

| Chart Item | MVP | Notes |
| --- | --- | --- |
| Candlestick chart | Yes | Main visual |
| Volume bars | Yes | Confirm participation |
| SMA 20 | Yes | Short-term trend |
| SMA 50 | Yes | Medium trend |
| SMA 200 | Yes | Long-term trend |
| RSI panel | Yes | Momentum |
| EMA 8/21 | Maybe | Add if simple |
| MACD panel | Maybe | Not required for first MVP |
| VWAP | No | Intraday feature |
| ATR overlay | No | Show ATR in risk card instead |

---

## 9.3 Setup Explanation

Each candidate must explain why it appeared.

Example format:

> MSFT appeared because it matched the pullback continuation setup:
>
> - Price remains above the 50-day and 200-day moving averages.
> - The 20-day moving average is above the 50-day moving average.
> - Price pulled back near the 20-day moving average.
> - RSI is neutral-positive, suggesting the stock is not extremely overbought.

Requirements:

- Explanation must be generated from actual rule outputs.
- Passed rules and failed rules should both be visible where useful.
- Avoid vague explanations such as “strong technicals.”
- Avoid AI-generated certainty language in MVP.

---

## 9.4 Score Breakdown

The score breakdown should show major components.

Suggested product-level components:

| Component | Purpose |
| --- | --- |
| Technical setup score | How strongly setup rules matched |
| Volume score | Whether participation supports the move |
| Relative strength score | Whether ticker outperforms market |
| Risk/reward score | Whether trade structure is reasonable |
| Context score | Basic company/earnings caution context |

Detailed formula belongs in `/docs/02-trading-strategy-requirements.md`.

---

## 9.5 Risk/Reward Card

Required fields:

| Field | Purpose |
| --- | --- |
| Suggested entry zone | Where setup becomes interesting |
| Invalidation level | Where the setup thesis weakens or fails |
| Stop-loss estimate | Risk reference |
| Target estimate | Upside reference |
| Risk/reward ratio | Compare estimated upside to downside |
| ATR | Volatility context |
| Caution note | Warn if estimate is weak or data is stale |

Important wording:

Risk/reward output must be labelled as a **research estimate**, not a trading instruction.

---

## 9.6 Company and Earnings Context

Required fields where available:

| Field | Purpose |
| --- | --- |
| Company name | Identify business |
| Sector | Sector context |
| Industry | More specific context |
| Market cap | Size/liquidity context |
| Exchange | Listing context |
| Business summary | Brief background |
| Last earnings date | Recent catalyst awareness |
| Next earnings date | Avoid blind earnings risk |
| EPS actual vs estimate | Basic earnings surprise context |
| Revenue actual vs estimate | Basic earnings surprise context |

---

## 10. Product Status Labels

Each candidate should receive one product-facing status.

| Status | Meaning |
| --- | --- |
| Actionable | Setup is valid, data is fresh, and risk/reward appears acceptable |
| Watch | Interesting candidate but waiting for confirmation or cleaner structure |
| Avoid | Too extended, too weak, too risky, or contradicted by context |
| Blocked | Missing, stale, or invalid data prevents judgment |

Notes:

- `Actionable` does not mean “place trade automatically.”
- `Blocked` is required because the system must be honest when data is not reliable.
- Candidate status should be explainable from rule outputs and data state.

---

## 11. Cost and Operating Constraints

PoorToPour is a personal project and must be designed with cost discipline from the beginning.

The MVP should avoid expensive always-on services and should prioritize:

- local-first development;
- deterministic computations before AI calls;
- configurable scan intervals;
- configurable universe size;
- caching and reuse of fetched data;
- clear data-provider feature toggles;
- limited and logged AI usage;
- simple hosting options;
- no always-running AI agent swarm in MVP.

The product should allow the user to control operating cost through:

| Cost Lever | Product Requirement |
| --- | --- |
| Universe size | User can limit the scanned ticker universe |
| Scan frequency | User can configure daily/weekly scan behavior |
| AI usage | AI-generated summaries are off by default in MVP |
| Data providers | Expensive providers should be optional |
| Caching | Previously fetched data should be reused where safe |
| Feature toggles | Post-MVP context layers can be enabled/disabled |
| Job visibility | Scan job history should show frequency and failures |

MVP cost principle:

> The MVP should be useful without requiring expensive AI agents, premium market data, or complex cloud infrastructure.

Detailed cost estimation, hosting options, AI token budgeting, provider pricing, and operating modes belong in `/docs/07-cost-and-operations.md`.

---

## 12. Non-Functional Product Requirements

| Requirement | MVP Expectation |
| --- | --- |
| Freshness | Show scan timestamp and data freshness clearly |
| Explainability | Every candidate must show why it appeared |
| Traceability | Candidate results must link to a scan run |
| Responsiveness | Dashboard should feel fast for the MVP universe |
| Data honesty | Missing/stale data must be visible |
| Safety | No automated trading in MVP |
| Local-first | App can run locally |
| Cost control | No required always-on AI or premium infrastructure |
| Configurability | Basic scan settings can be changed without code edits |
| Maintainability | Product behavior should map cleanly to documented requirements |

---

## 13. MVP Definition of Done

The MVP is complete when:

> The user can open the dashboard, view the latest daily or weekly scan, inspect ranked long-only swing-trade candidates from the S&P 500, click into a candidate, see chart evidence and explanation, review basic risk/reward context, and view previous scan runs.

Checklist:

| ID | Requirement | MVP Status |
| --- | --- | --- |
| PRD-001 | Dashboard home displays latest scan | Required |
| PRD-002 | Candidate ranking table displays setup results | Required |
| PRD-003 | Candidate detail page displays chart evidence | Required |
| PRD-004 | Candidate detail page explains setup match | Required |
| PRD-005 | Candidate detail page shows score breakdown | Required |
| PRD-006 | Basic company context is displayed | Required |
| PRD-007 | Basic earnings context is displayed if available | Required |
| PRD-008 | Risk/reward card is displayed | Required |
| PRD-009 | Scan history is available | Required |
| PRD-010 | User can manually trigger scan | Required |
| PRD-011 | User can configure basic scan settings | Required |
| PRD-012 | No broker execution exists | Required |
| PRD-013 | Stale/missing data is clearly labelled | Required |
| PRD-014 | Watchlist is available | MVP+ |
| PRD-015 | AI-generated summaries are available | Post-MVP |
| PRD-016 | Alerts are available | Post-MVP |
| PRD-017 | Intraday intelligence is available | Post-MVP |
| PRD-018 | Paper trading is available | Later |
| PRD-019 | Broker automation is available | Later |

---

## 14. Product Phasing

| Product Phase | Features |
| --- | --- |
| MVP | Daily/weekly scanner, dashboard, candidate detail, basic per-candidate visual evidence, scan history, settings |
| MVP+ | Watchlist, exports, improved filters, saved views, global ticker search, scanner-aware watchlist, benchmark-relative strength inputs, richer per-candidate visual presentation, chart signal markers, detected-signal panel, market regime panel, sector/theme scanner |
| Phase 2 | Company, earnings, and news/catalyst feed improvements |
| Phase 3 | Backtesting UI and strategy validation |
| Phase 4 | Alerts, notifications, and daily/weekly scan briefing |
| Phase 5 | Intraday monitoring |
| Phase 6 | Paper trading |
| Phase 7 | Controlled broker automation |
| Phase 8 | Personal trading assistant with strict guardrails |

### 14.1 MVP+ Candidate Features from External Review

The following ideas were captured from OpenStock-style market portal references and Spring Duck-style signal dashboard references. They are not required for MVP.

- Command palette / global ticker search.
- Scanner-aware watchlist.
- Benchmark-relative strength inputs using SPY/QQQ return comparison.
- Richer per-candidate visual presentation with annotated chart evidence.
- External TradingView chart link.
- Chart signal markers.
- Detected Signals panel.
- Sector/theme scanner grid.
- Market regime panel.
- AI candidate insight panel after deterministic scanner output exists.

The v0.2 mock renders in `/docs/references/Mock_UI_Renders` show these ideas as visual direction. They should not be treated as a commitment to implement every visible panel in MVP.

### 14.2 Spring Duck-Inspired MVP+ Feature Cluster

The Spring Duck screenshots in `/docs/references/Research_Docs/Screenshots` inspired the v0.2 mock render direction. These ideas should be treated as MVP+ candidates after the deterministic MVP scanner exists:

- candlestick chart signal markers;
- moving average and volume evidence around each signal;
- structured Detected Signals panel;
- market signal cards;
- sector/theme scanner grid;
- scanner-aware watchlist;
- ticker chips/search;
- AI insight panel that explains deterministic scanner output;
- tabbed views such as Overview, Scanner, and Tasks;
- visual signal taxonomy for richer future setup review.

AI insights and visual signal taxonomy must remain explainability layers over deterministic rule output, not independent trade-decision engines.

---

## 15. Open Product Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-PRD-001 | Should MVP universe be S&P 500 only or S&P 500 plus Nasdaq 100? | S&P 500 plus Nasdaq 100 | 🟩 Resolved |
| Q-PRD-002 | Should market snapshot cards appear on Dashboard Home MVP? | Maybe, if easy | 🟦 Open |
| Q-PRD-003 | Should MACD be shown on the first candidate detail page? | Maybe, not required | 🟦 Open |
| Q-PRD-004 | Should watchlist be included if trivial? | MVP+ unless trivial | 🟦 Open |
| Q-PRD-005 | Should scan results be exportable in MVP? | No | 🟦 Open |
| Q-PRD-006 | Should settings be editable from UI or config file first? | UI if simple, config file acceptable for first internal build | 🟦 Open |
| Q-PRD-007 | What is the first acceptable monthly operating budget? | TBD in `/docs/07-cost-and-operations.md` | 🟦 Open |

---

## 16. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-05-26 | v0.5 | Resolved MVP universe as S&P 500 plus Nasdaq 100 | Jesse + AI |
| 2026-05-27 | v0.6 | Added benchmark-relative strength inputs to durable MVP+ feature list | Jesse + AI |
| 2026-05-25 | v0.4 | Added Spring Duck-inspired MVP+ feature cluster from v0.2 mock direction | Jesse + AI |
| 2026-05-25 | v0.3 | Clarified v0.2 render scope and kept Sector Scanner / market regime as MVP+ | Jesse + AI |
| 2026-05-14 | v0.2 | Added MVP+ external-review candidate features without expanding MVP scope | Jesse + AI |
| 2026-04-30 | v0.1 | Created initial product requirements document | Jesse + AI |
