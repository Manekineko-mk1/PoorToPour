# PoorToPour Trading Strategy Requirements

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/02-trading-strategy-requirements.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.1

---

## 1. Purpose

This document defines the first trading strategy requirements for PoorToPour.

It answers:

- What trading style does the MVP support?
- What stock universe does the scanner analyze?
- Which technical indicators are required?
- Which setup types should the MVP detect?
- How should candidates be scored?
- How should risk/reward be estimated?
- What makes a candidate actionable, watch-only, avoided, or blocked?
- What validation is required before strategies are trusted?

This document focuses on strategy behavior and trading logic. It does not define database schema, UI layout, provider selection, or deployment architecture.

Related documents:

| File | Purpose |
| --- | --- |
| `/docs/00-project-plan.md` | Project vision, MVP boundary, and roadmap |
| `/docs/01-product-requirements.md` | Product workflows, screens, and user-facing requirements |
| `/docs/03-technical-architecture.md` | System design, modules, services, and data flow |
| `/docs/04-data-sources.md` | Data providers, limits, and freshness rules |
| `/docs/05-dashboard-design.md` | Dashboard layout and UI behavior |
| `/docs/06-risk-and-backtesting.md` | Detailed risk controls and validation methodology |
| `/docs/07-cost-and-operations.md` | Cost estimates and operating constraints |
| `/docs/08-execution-tracker.md` | Current project progress |
| `/docs/09-decision-log.md` | Accepted project decisions |
| `/docs/10-ai-working-guidelines.md` | AI workflow and engineering standards |

---

## 2. Strategy Scope

## 2.1 MVP Strategy Summary

The MVP strategy is a **long-only, swing-trade technical scanner** for a limited U.S. equity universe.

The goal is not to generate automatic buy/sell orders. The goal is to surface technically interesting candidates that deserve manual review.

MVP strategy statement:

> PoorToPour MVP scans a liquid U.S. equity universe for explainable long-only swing-trade setups using daily and weekly market data. It ranks candidates based on technical structure, volume confirmation, relative strength, and basic risk/reward quality.

---

## 2.2 MVP Trading Style

| Dimension | MVP Decision |
| --- | --- |
| Direction | Long-only |
| Holding period | Swing-trade oriented |
| Scan interval | Daily and weekly |
| Data granularity | Daily candles first |
| Intraday usage | Not required for MVP |
| Universe | S&P 500 by default |
| Execution | Manual review only |
| AI role | No AI-generated trade decisions |
| Strategy type | Rule-based and explainable |

---

## 2.3 Out of Scope for MVP

The MVP strategy should not include:

- Short-selling setups.
- Options strategies.
- Intraday scalping.
- Premarket gap trading.
- News-only catalyst trading.
- Earnings gamble trades.
- Penny stocks.
- Low-float runners.
- Automated live trading.
- AI-generated buy/sell decisions.
- Reinforcement learning.
- Portfolio optimization.
- Position execution.

These can be revisited later after the deterministic scanner proves useful.

---

## 3. Strategy Principles

## 3.1 Evidence Before Opinion

Every candidate must be selected because it matched explicit rules.

A ticker should not appear because it “feels strong” or because an AI summary sounds convincing.

Required evidence types:

- price structure;
- trend context;
- volume participation;
- relative strength;
- volatility/risk context;
- data freshness.

---

## 3.2 Risk Before Excitement

A setup is not useful unless risk can be described.

Every candidate should include:

- entry zone estimate;
- invalidation level;
- stop-loss estimate;
- initial target estimate;
- risk/reward ratio;
- ATR-based volatility context;
- caution flags.

---

## 3.3 Explainable Scores

Composite scores must be decomposable.

The user should be able to inspect:

- which setup rules passed;
- which setup rules failed;
- which score components contributed;
- which data was missing or stale;
- why a candidate was labelled Actionable, Watch, Avoid, or Blocked.

---

## 3.4 Conservative First Version

The MVP should favor fewer, higher-quality candidates over noisy signal spam.

Default behavior:

- Prefer liquid large-cap stocks.
- Avoid overextended moves.
- Avoid candidates with missing data.
- Warn around earnings.
- Do not force a candidate count.
- It is acceptable for a scan to produce zero strong candidates.

---

## 4. Market Universe Requirements

## 4.1 MVP Universe

Default universe:

> S&P 500 constituents.

Reason:

- liquid;
- widely followed;
- easier to validate;
- less exposed to extreme low-float behavior;
- manageable number of tickers for early scans.

---

## 4.2 Universe Filters

The scanner should apply basic liquidity and quality filters before setup detection.

Suggested defaults:

| Filter | Default | Reason |
| --- | ---: | --- |
| Minimum price | $5 | Avoid penny-stock behavior |
| Minimum average daily dollar volume | $20 million | Avoid illiquid candidates |
| Minimum market cap | $1 billion | Keep MVP focused on established names |
| Minimum trading history | 252 trading days | Needed for 52-week and 200-day indicators |
| Exclude OTC/pink sheets | Yes | Avoid unreliable data/liquidity |
| Exclude symbols with missing recent price data | Yes | Avoid stale candidates |

These defaults should be configurable later.

---

## 4.3 Future Universe Expansion

Potential later universes:

| Universe | When to Add |
| --- | --- |
| Nasdaq 100 | After S&P 500 scanner works |
| Russell 1000 | After performance and rate limits are understood |
| Custom watchlist | MVP+ if easy |
| Sector-specific lists | Post-MVP |
| ETFs | Post-MVP |
| Full U.S. equities | Much later, with stronger filters |

---

## 5. Required Market Data

## 5.1 Daily OHLCV

Required for MVP:

| Field | Required | Notes |
| --- | --- | --- |
| Open | Yes | Daily candle |
| High | Yes | Daily candle |
| Low | Yes | Daily candle |
| Close | Yes | Daily candle |
| Adjusted close | Preferred | Useful for split/dividend adjustment |
| Volume | Yes | Volume confirmation |
| Date | Yes | Time series key |

---

## 5.2 Company and Context Data

Strategy layer needs limited context:

| Field | Required for MVP | Purpose |
| --- | --- | --- |
| Company name | Yes | Display |
| Sector | Yes | Context |
| Industry | Preferred | Context |
| Market cap | Preferred | Filter/context |
| Next earnings date | Preferred | Caution flag |
| Last earnings date | Preferred | Context |
| Exchange | Preferred | Display/filter |

Detailed provider decisions belong in `/docs/04-data-sources.md`.

---

## 5.3 Data Freshness Rules

A candidate should be marked `Blocked` if required price data is missing or stale.

Suggested freshness rules:

| Data Type | Freshness Expectation | If Violated |
| --- | --- | --- |
| Daily OHLCV after market close | Latest completed trading day | Block or warn |
| Company profile | Within 30 days | Warn |
| Earnings date | Within 7 days during earnings season | Warn |
| Market cap | Within 7 days | Warn |
| Indicator calculation | Same timestamp as scan run | Block if unavailable |

The dashboard should display freshness labels.

---

## 6. Required Technical Indicators

## 6.1 MVP Indicators

The MVP scanner should compute the following indicators internally.

| Indicator | Parameters | Purpose |
| --- | --- | --- |
| SMA | 20, 50, 200 | Trend and support/resistance context |
| EMA | 8, 21 | Short-term momentum context, optional in first UI |
| RSI | 14 | Momentum and overbought/oversold context |
| ATR | 14 | Volatility and stop-distance context |
| Volume moving average | 20 | Relative volume calculation |
| Relative volume | Current volume / 20-day average volume | Participation confirmation |
| 20-day high/low | 20 trading days | Breakout/pullback context |
| 50-day high/low | 50 trading days | Breakout/pullback context |
| 52-week high/low | 252 trading days | Long-term strength context |
| Relative strength vs SPY | 20-day and 60-day | Market outperformance |

---

## 6.2 Optional MVP Indicators

These may be computed if simple, but should not block MVP:

| Indicator | Parameters | Reason to Add |
| --- | --- | --- |
| MACD | 12, 26, 9 | Momentum confirmation |
| Bollinger Bands | 20, 2 std dev | Volatility/extension context |
| Distance from moving averages | % from SMA 20/50/200 | Overextension warning |
| Average dollar volume | 20-day | Liquidity filter |

---

## 6.3 Post-MVP Indicators

Add later only if useful:

- VWAP.
- Anchored VWAP.
- ADX.
- Donchian channels.
- Keltner channels.
- OBV.
- Accumulation/distribution line.
- Market breadth.
- Sector relative strength.
- Beta.
- Implied volatility.
- Short interest.
- Options flow.

---

## 7. MVP Setup Families

The MVP should detect three setup families:

1. Breakout.
2. Pullback continuation.
3. Relative strength leader.

These are simple enough to implement, explain, visualize, and validate.

---

## 8. Setup 1 — Breakout

## 8.1 Goal

Find stocks breaking above recent resistance with meaningful volume participation.

Breakout candidates should show:

- price strength;
- clean resistance break;
- volume expansion;
- positive relative strength;
- manageable overextension.

---

## 8.2 Candidate Rules

Required base rules:

| Rule ID | Rule | Default |
| --- | --- | --- |
| BO-001 | Close is above previous 20-day high | Required |
| BO-002 | Close is above SMA 20 | Required |
| BO-003 | Close is above SMA 50 | Required |
| BO-004 | SMA 20 is above or rising toward SMA 50 | Preferred |
| BO-005 | Relative volume is at least 1.5x | Required |
| BO-006 | RSI is between 50 and 75 | Preferred |
| BO-007 | 20-day relative strength vs SPY is positive | Preferred |
| BO-008 | Distance from SMA 20 is not excessively extended | Required |
| BO-009 | Required data is fresh | Required |

Optional stronger confirmation:

| Rule ID | Rule | Notes |
| --- | --- | --- |
| BO-010 | Close is above previous 50-day high | Stronger breakout |
| BO-011 | Stock is within 10% of 52-week high | Long-term strength |
| BO-012 | Sector is outperforming SPY | Post-MVP |

---

## 8.3 Breakout Caution Flags

| Flag | Trigger |
| --- | --- |
| Overextended | Close is too far above SMA 20 or ATR-based range |
| Low participation | Relative volume below threshold |
| Weak market confirmation | Relative strength vs SPY is negative |
| Earnings soon | Next earnings within configured warning window |
| Stale data | Price or indicator data is stale |
| Gap risk | Large move without enough volume confirmation |

---

## 8.4 Breakout Status Guidance

| Status | Conditions |
| --- | --- |
| Actionable | Required rules pass, volume strong, risk/reward acceptable, no major caution |
| Watch | Setup forming but needs confirmation or cleaner entry |
| Avoid | Overextended, weak volume, poor risk/reward, or major caution |
| Blocked | Required data missing or stale |

---

## 9. Setup 2 — Pullback Continuation

## 9.1 Goal

Find stocks in established uptrends that are pulling back toward support without breaking trend structure.

Pullback continuation candidates should show:

- existing uptrend;
- controlled pullback;
- price near support;
- momentum reset;
- acceptable downside risk.

---

## 9.2 Candidate Rules

Required base rules:

| Rule ID | Rule | Default |
| --- | --- | --- |
| PB-001 | Close is above SMA 50 | Required |
| PB-002 | Close is above SMA 200 | Required |
| PB-003 | SMA 20 is above SMA 50 | Preferred |
| PB-004 | SMA 50 is above SMA 200 | Preferred |
| PB-005 | Close is near SMA 20 or SMA 50 | Required |
| PB-006 | RSI is between 40 and 60 | Preferred |
| PB-007 | 20-day or 60-day relative strength vs SPY is positive | Preferred |
| PB-008 | Pullback has not broken recent swing low | Required |
| PB-009 | Required data is fresh | Required |

Suggested “near moving average” definition:

| Support | Default Zone |
| --- | --- |
| Near SMA 20 | Within 0% to 3% above SMA 20 |
| Near SMA 50 | Within 0% to 5% above SMA 50 |

These thresholds should be configurable.

---

## 9.3 Pullback Caution Flags

| Flag | Trigger |
| --- | --- |
| Trend damage | Close below SMA 50 |
| Deep pullback | Pullback exceeds configured ATR or percentage threshold |
| Weak relative strength | Stock underperforming SPY |
| Momentum too weak | RSI below 40 |
| Still overbought | RSI above 65 during pullback |
| Earnings soon | Next earnings within configured warning window |
| Stale data | Price or indicator data is stale |

---

## 9.4 Pullback Status Guidance

| Status | Conditions |
| --- | --- |
| Actionable | Uptrend intact, pullback near support, risk/reward acceptable |
| Watch | Trend good but entry area not clean yet |
| Avoid | Trend damaged, weak relative strength, or poor risk/reward |
| Blocked | Required data missing or stale |

---

## 10. Setup 3 — Relative Strength Leader

## 10.1 Goal

Find stocks outperforming the market and trading near important highs.

Relative strength leaders may not always be immediate entries. They are high-quality watchlist candidates for future breakouts or pullbacks.

---

## 10.2 Candidate Rules

Required base rules:

| Rule ID | Rule | Default |
| --- | --- | --- |
| RS-001 | 20-day relative strength vs SPY is positive | Required |
| RS-002 | 60-day relative strength vs SPY is positive | Preferred |
| RS-003 | Close is above SMA 50 | Required |
| RS-004 | Close is above SMA 200 | Required |
| RS-005 | Close is within 10% of 52-week high | Preferred |
| RS-006 | Volume trend is stable or improving | Preferred |
| RS-007 | RSI is between 50 and 75 | Preferred |
| RS-008 | Required data is fresh | Required |

---

## 10.3 Relative Strength Caution Flags

| Flag | Trigger |
| --- | --- |
| Too extended | Price far above SMA 20 or ATR range |
| Late-stage move | RSI above 75 with large recent price advance |
| Weak volume | Relative volume consistently weak |
| Market divergence | Stock rising while broader market weakens sharply |
| Earnings soon | Next earnings within configured warning window |
| Stale data | Price or indicator data is stale |

---

## 10.4 Relative Strength Status Guidance

| Status | Conditions |
| --- | --- |
| Actionable | Strong relative strength plus clean setup and risk/reward |
| Watch | Strong stock but no clean entry yet |
| Avoid | Too extended or weakening |
| Blocked | Required data missing or stale |

---

## 11. Composite Scoring Requirements

## 11.1 Score Purpose

The score ranks candidates for manual review.

The score is not a buy signal.

Score range:

| Score | Meaning |
| --- | --- |
| 80–100 | Strong candidate |
| 65–79 | Interesting candidate |
| 50–64 | Weak/watch-only candidate |
| Below 50 | Usually avoid or filter out |
| N/A | Blocked due to missing/stale data |

---

## 11.2 MVP Score Components

Suggested default weighting:

| Component | Weight | Purpose |
| --- | ---: | --- |
| Setup match score | 40% | How strongly setup rules pass |
| Volume/participation score | 15% | Confirms market interest |
| Relative strength score | 15% | Measures outperformance |
| Risk/reward score | 15% | Estimates whether structure is worth attention |
| Context/caution score | 15% | Penalizes earnings risk, stale data, overextension |

Total:

> 100%

---

## 11.3 Setup Match Score

The setup match score should consider:

- required rule pass/fail;
- preferred rule pass/fail;
- strength of the condition;
- severity of failed conditions.

Rule requirement:

- If any required rule fails, the candidate should usually not become `Actionable`.
- Missing required data should produce `Blocked`.

---

## 11.4 Volume Score

Volume score should consider:

| Metric | Interpretation |
| --- | --- |
| Relative volume above 1.5x | Positive for breakout |
| Relative volume above 2.0x | Strong breakout participation |
| Stable volume during pullback | Healthy pullback |
| Very weak volume | Penalize |
| Abnormal volume with poor price action | Warning |

---

## 11.5 Relative Strength Score

Relative strength should compare stock performance against SPY.

Suggested calculations:

| Metric | Purpose |
| --- | --- |
| 20-day return minus SPY 20-day return | Short-term outperformance |
| 60-day return minus SPY 60-day return | Intermediate outperformance |
| Distance from 52-week high | Leadership context |

Future version:

- Compare against sector ETF as well as SPY.

---

## 11.6 Risk/Reward Score

Risk/reward score should consider:

| Metric | Positive |
| --- | --- |
| Clear invalidation level | Yes |
| Stop distance reasonable vs ATR | Yes |
| Upside target at least 2R | Yes |
| Price not too extended | Yes |
| Stop distance too wide | Penalize |
| Target unclear | Penalize |

Default minimum preferred risk/reward:

> 2:1 for swing-trade candidates.

---

## 11.7 Context/Caution Score

This component should penalize candidates with caution flags.

Examples:

| Caution | Suggested Effect |
| --- | --- |
| Earnings within 1–3 trading days | Strong penalty or Watch/Avoid |
| Stale price data | Block |
| Missing company profile | Small penalty/warn |
| Missing earnings date | Warn |
| Overextended price | Penalize |
| Low liquidity | Exclude or penalize |
| Abnormal volatility | Penalize |

---

## 12. Candidate Status Requirements

Every candidate should have one status.

| Status | Meaning |
| --- | --- |
| Actionable | Strong setup, fresh data, acceptable risk/reward, no major caution |
| Watch | Interesting but needs confirmation, cleaner entry, or less risk |
| Avoid | Poor structure, overextended, weak participation, or major caution |
| Blocked | Missing/stale/invalid data prevents judgment |

Important:

- `Actionable` means “worth manual review now.”
- It does not mean “automatically buy.”
- The UI must never present strategy output as guaranteed return.

---

## 13. Risk/Reward Estimation

## 13.1 Purpose

The MVP should produce a simple research estimate for each candidate.

It should help answer:

- Where does this setup become interesting?
- Where is the setup probably wrong?
- How much downside is implied?
- Is the upside meaningful enough?

---

## 13.2 Entry Zone

Entry zone depends on setup type.

| Setup | Entry Zone Idea |
| --- | --- |
| Breakout | Near breakout level or close above resistance |
| Pullback continuation | Near SMA 20/SMA 50 or recent support |
| Relative strength leader | Usually watch-only unless paired with breakout/pullback |

The MVP should label entry zones as estimates.

---

## 13.3 Invalidation Level

Suggested invalidation logic:

| Setup | Invalidation Level |
| --- | --- |
| Breakout | Below breakout level or recent swing low |
| Pullback continuation | Below recent swing low or support moving average |
| Relative strength leader | Below SMA 50 or recent swing low, depending on structure |

---

## 13.4 Stop-Loss Estimate

Stop estimate should consider:

- invalidation level;
- ATR buffer;
- recent swing low;
- moving average support.

Example:

> Stop estimate = min(recent swing low, breakout level) minus ATR buffer.

Exact formulas belong to implementation and later refinement.

---

## 13.5 Target Estimate

Target estimate can be simple in MVP.

Possible methods:

| Method | Notes |
| --- | --- |
| 2R target | Simple and consistent |
| Prior measured move | Useful for breakouts |
| Recent resistance | Useful when below highs |
| ATR-based target | Useful for volatility context |

MVP default:

> Use 2R target as the first target estimate.

---

## 13.6 Position Sizing

MVP should show risk context but does not need full portfolio integration.

Optional MVP calculation:

| Input | Default |
| --- | --- |
| Account size | User-configurable later |
| Risk per trade | 0.5% to 1.0% |
| Stop distance | From entry to stop estimate |
| Position size | Risk dollars / stop distance |

If account size is not configured, show risk/reward only.

---

## 14. Caution Flags

Caution flags must be visible in dashboard and candidate detail pages.

Required MVP flags:

| Flag | Trigger |
| --- | --- |
| Earnings soon | Next earnings date within warning window |
| Data stale | Latest required data is stale |
| Data missing | Required field unavailable |
| Low volume | Liquidity/volume below threshold |
| Overextended | Price too far from support or ATR range |
| Weak relative strength | Underperforming SPY |
| Poor risk/reward | Estimated reward below threshold |
| High volatility | ATR unusually high relative to price |
| Broken trend | Price below key moving average for trend setup |

---

## 15. Scan Types and Frequency

## 15.1 Daily Scan

Purpose:

Find swing-trade candidates after the market close.

Recommended schedule:

- Run once after daily OHLCV data is available.
- Store scan results.
- Produce ranked candidates.
- Mark scan with timestamp and data date.

---

## 15.2 Weekly Scan

Purpose:

Find broader breakout and relative-strength candidates.

Recommended schedule:

- Run once per week after the final trading day closes.
- Reuse daily data.
- Focus on stronger trend and leadership signals.

---

## 15.3 Manual Scan

Purpose:

Support development and manual refresh.

Requirements:

- User can trigger a scan manually.
- Manual scan should show status.
- Manual scan should not bypass cost/rate limits.
- Manual scan should record a normal scan run.

---

## 15.4 Intraday Scan

MVP status:

> Not required.

Future use:

- Gap-up momentum.
- VWAP hold.
- Headline reaction.
- Relative volume spikes.
- Day-trade setup discovery.

Reason to delay:

- Requires intraday data.
- More expensive.
- More noise.
- Harder validation.
- Greater risk of false confidence.

---

## 16. Backtesting Requirements Summary

Detailed backtesting belongs in `/docs/06-risk-and-backtesting.md`.

MVP strategy logic should still be built so it can later be backtested.

Requirements:

- Strategy rules must be deterministic.
- Signals must be reproducible from historical data.
- Scan result should store enough metadata to inspect why a candidate appeared.
- Avoid using future data in signal generation.
- Record the data date and scan timestamp separately.
- Store rule pass/fail outputs.

Initial validation windows:

| Window | Purpose |
| --- | --- |
| 1 trading day | Very short follow-through |
| 5 trading days | One-week behavior |
| 10 trading days | Two-week behavior |
| 20 trading days | Swing-trade behavior |

Initial metrics:

- win rate;
- average return;
- median return;
- max adverse excursion;
- max favorable excursion;
- average R multiple;
- comparison against SPY;
- number of candidates;
- false positive review notes.

---

## 17. AI Usage in Strategy

AI must not make MVP trade decisions.

Allowed later:

- summarize candidate evidence;
- summarize recent company context;
- generate bull/bear research notes;
- explain rule outputs in natural language;
- cluster headlines;
- assist with post-scan review.

Not allowed in MVP:

- AI says buy/sell;
- AI overrides deterministic setup status;
- AI changes score without explainable rules;
- AI generates targets without validated logic;
- AI creates trades for broker execution.

Strategy rule:

> AI can explain strategy output later, but it should not be the source of strategy output in MVP.

---

## 18. MVP Strategy Definition of Done

The strategy layer is MVP-complete when:

| ID | Requirement | Status |
| --- | --- | --- |
| STRAT-001 | S&P 500 universe can be filtered by liquidity and data availability | Required |
| STRAT-002 | Required daily indicators are computed | Required |
| STRAT-003 | Breakout setup detection exists | Required |
| STRAT-004 | Pullback continuation setup detection exists | Required |
| STRAT-005 | Relative strength leader detection exists | Required |
| STRAT-006 | Composite score is generated | Required |
| STRAT-007 | Candidate status is assigned | Required |
| STRAT-008 | Risk/reward estimate is generated | Required |
| STRAT-009 | Caution flags are generated | Required |
| STRAT-010 | Rule pass/fail explanations are stored | Required |
| STRAT-011 | Missing/stale data produces Blocked or warning states | Required |
| STRAT-012 | Strategy output can be displayed by dashboard | Required |
| STRAT-013 | Strategy logic can be backtested later without rewriting | Required |

---

## 19. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-STRAT-001 | Should MVP use S&P 500 only or include Nasdaq 100? | S&P 500 only | Open |
| Q-STRAT-002 | Should MACD be computed in MVP? | Optional, not required | Open |
| Q-STRAT-003 | Should Bollinger Bands be included in MVP? | Optional, not required | Open |
| Q-STRAT-004 | What exact overextension threshold should be used? | TBD during implementation/backtesting | Open |
| Q-STRAT-005 | What exact earnings warning window should be used? | 1–3 trading days | Open |
| Q-STRAT-006 | Should position sizing be shown in MVP? | Only if account size setting is simple | Open |
| Q-STRAT-007 | Should weekly scans use different thresholds than daily scans? | Likely yes later | Open |
| Q-STRAT-008 | Should sector relative strength be included in MVP? | Post-MVP | Open |
| Q-STRAT-009 | Should candidates below score 50 be stored or discarded? | Store scan metadata, hide by default | Open |
| Q-STRAT-010 | What minimum risk/reward should be required for Actionable? | 2:1 | Open |

---

## 20. Initial Strategy Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| STRAT-D-001 | MVP is long-only | Simpler and lower risk than long/short scanner |
| STRAT-D-002 | MVP uses daily/weekly swing scans | Easier and cheaper than intraday scanning |
| STRAT-D-003 | MVP starts with S&P 500 | Clean, liquid, manageable universe |
| STRAT-D-004 | MVP uses deterministic rules | Required for explainability and backtesting |
| STRAT-D-005 | MVP setup families are breakout, pullback continuation, and relative strength leader | Simple, visual, and testable setup types |
| STRAT-D-006 | AI does not make MVP trade decisions | Avoids black-box signals and expensive false confidence |
| STRAT-D-007 | Candidate scoring must be explainable | User must understand why a ticker appears |
| STRAT-D-008 | Missing or stale required data can block a candidate | Data honesty is required for trading safety |
| STRAT-D-009 | Risk/reward output is a research estimate, not instruction | Prevents overstating scanner authority |
| STRAT-D-010 | Backtesting compatibility is required from the beginning | Avoids rewriting strategy logic later |

---

## 21. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial trading strategy requirements document | Jesse + AI |
