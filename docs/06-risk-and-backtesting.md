# PoorToPour Risk and Backtesting

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/06-risk-and-backtesting.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.1

---

## 1. Purpose

This document defines the risk-management and backtesting requirements for PoorToPour.

It answers:

- How should trade risk be represented?
- What risk fields should the MVP calculate?
- What caution flags should protect the user from weak or unsafe candidates?
- How should the strategy be backtested later?
- What does “scanner quality” mean?
- What gates must be passed before paper trading?
- What gates must be passed before broker automation?
- How do we avoid false confidence from attractive but untested signals?

This document does not define the exact implementation architecture. Architecture is covered in `/docs/03-technical-architecture.md`.

---

## 2. Risk Philosophy

PoorToPour should be built around this principle:

> A trade idea is not useful unless the system can explain where it is wrong.

PoorToPour must never present a candidate as “safe,” “guaranteed,” or “certain.” All scanner output is research output.

The MVP should focus on:

- identifying technically interesting candidates;
- showing why they appeared;
- showing caution flags;
- estimating risk/reward;
- making data quality visible;
- supporting manual review only.

The long-term system may eventually support paper trading and controlled automation, but only after validation gates are passed.

---

## 3. Core Risk Principles

## 3.1 Risk First, Signal Second

The scanner should not promote a candidate simply because it has a high technical score.

A candidate should be penalized or downgraded if:

- risk/reward is poor;
- stop distance is too wide;
- data is stale;
- volume is weak;
- earnings are too close;
- price is overextended;
- trend structure is damaged.

---

## 3.2 No Hidden Uncertainty

If data is missing, stale, partial, or invalid, the dashboard must say so.

PoorToPour should prefer:

```text
Blocked: required data is stale
```

over:

```text
Score: 87
```

when the score is not reliable.

---

## 3.3 Research Estimate, Not Instruction

Entry, stop, target, position size, and risk/reward outputs are research estimates.

They must not be displayed as direct trading instructions.

Preferred UI wording:

```text
Research estimate
```

Avoid UI wording:

```text
Buy here
Sell here
Guaranteed target
Safe trade
```

---

## 3.4 Survival Over Optimization

The system should prioritize avoiding catastrophic mistakes over maximizing theoretical returns.

This means:

- conservative defaults;
- no live trading in MVP;
- no broker integration before paper trading;
- strict future kill switch;
- strict max-risk limits before automation.

---

## 4. MVP Risk Scope

## 4.1 Included in MVP

MVP should include:

| Risk Feature | MVP | Notes |
| --- | --- | --- |
| Entry zone estimate | Yes | Research estimate |
| Invalidation level | Yes | Where thesis weakens/fails |
| Stop-loss estimate | Yes | Research estimate |
| Target estimate | Yes | Simple 2R target first |
| Risk/reward ratio | Yes | Prefer at least 2:1 |
| ATR context | Yes | Volatility-aware risk |
| Caution flags | Yes | Visible in dashboard/table/detail |
| Data freshness blocking | Yes | Required for trading safety |
| Candidate status labels | Yes | Actionable / Watch / Avoid / Blocked |
| Position sizing | Maybe | Only if account-size config is simple |
| Portfolio-level risk | No | Post-MVP |
| Paper trading | No | Later |
| Broker execution | No | Future only |

---

## 4.2 Excluded from MVP

MVP does not include:

- live trading;
- broker connection;
- real order placement;
- portfolio optimization;
- options risk;
- short-selling risk;
- intraday scalping risk;
- automated alerts that imply urgency;
- AI-generated risk decisions;
- fully automated position sizing;
- tax-aware trading;
- multi-account risk management.

---

## 5. Candidate Risk Model

Each candidate should have a structured risk model.

Suggested fields:

| Field | Purpose |
| --- | --- |
| `entry_zone_low` | Lower bound of estimated entry zone |
| `entry_zone_high` | Upper bound of estimated entry zone |
| `invalidation_level` | Level where setup thesis weakens |
| `stop_loss_estimate` | Estimated protective stop |
| `target_1` | First upside estimate, default 2R |
| `target_2` | Optional extended target |
| `risk_per_share` | Entry minus stop estimate |
| `reward_per_share` | Target minus entry estimate |
| `risk_reward_ratio` | Reward divided by risk |
| `atr_14` | Volatility context |
| `stop_distance_pct` | Stop distance as percentage |
| `risk_label` | Acceptable / Wide / Poor / Unknown |
| `risk_notes` | Human-readable explanation |

---

## 6. Entry Zone Requirements

## 6.1 Purpose

Entry zone estimates help the user understand where the setup becomes interesting.

They are not execution instructions.

---

## 6.2 Setup-Specific Entry Logic

| Setup | MVP Entry Zone Idea |
| --- | --- |
| Breakout | Near breakout level or close above resistance |
| Pullback continuation | Near SMA 20/SMA 50 or recent support |
| Relative strength leader | Usually watch-only unless paired with breakout/pullback |

---

## 6.3 Entry Zone Display Rules

UI should show:

- entry zone range;
- source logic;
- whether current price is inside, above, or below the zone;
- warning if price is chasing too far above the zone.

Example:

```text
Entry Zone: $100.00–$102.00
Current Price: $105.20
Status: Above preferred zone / extended
```

---

## 7. Invalidation and Stop-Loss Requirements

## 7.1 Invalidation Level

The invalidation level should represent the price area where the setup story is likely wrong.

Examples:

| Setup | Invalidation Idea |
| --- | --- |
| Breakout | Close back below breakout level or recent swing low |
| Pullback continuation | Close below recent swing low or key moving average |
| Relative strength leader | Close below SMA 50 or recent swing low |

---

## 7.2 Stop-Loss Estimate

Stop-loss estimate should be based on invalidation plus volatility buffer.

Suggested inputs:

- recent swing low;
- breakout level;
- SMA 20/SMA 50 support;
- ATR buffer;
- setup type.

MVP rule:

> Use simple, explainable stop logic before complex optimization.

---

## 7.3 Stop Distance Quality

Stop distance should be evaluated.

| Risk Label | Meaning |
| --- | --- |
| Acceptable | Stop distance is reasonable versus ATR and expected reward |
| Wide | Stop is far away; position size would need to be smaller |
| Poor | Stop is too wide or reward is too small |
| Unknown | Missing data prevents estimate |

---

## 8. Target and Risk/Reward Requirements

## 8.1 Target Estimate

MVP default target:

> Target 1 = 2R from entry estimate.

Reason:

- simple;
- consistent;
- easy to validate;
- avoids pretending to predict exact future price.

Optional later target methods:

- measured move;
- prior resistance;
- ATR multiple;
- trailing exit;
- moving average violation;
- partial profit target.

---

## 8.2 Risk/Reward Ratio

Formula:

```text
risk_reward_ratio = potential_reward / potential_risk
```

Example:

```text
Entry: $100
Stop: $95
Target: $110

Risk: $5
Reward: $10
Risk/Reward: 2:1
```

MVP preference:

> Swing-trade candidates should generally require at least 2:1 to be labelled Actionable.

---

## 8.3 Risk/Reward Labeling

| Risk/Reward | Suggested Label |
| --- | --- |
| 3R or above | Strong |
| 2R to 2.99R | Acceptable |
| 1R to 1.99R | Weak |
| Below 1R | Poor |
| Unknown | Blocked or Watch |

---

## 9. ATR and Volatility Requirements

## 9.1 ATR Usage

ATR 14 should be used for volatility context.

Use cases:

- stop buffer;
- overextension warning;
- high-volatility caution;
- position sizing later;
- risk normalization across stocks.

---

## 9.2 High Volatility Warning

Flag high volatility when:

- ATR as percentage of price is above configured threshold;
- recent daily range is unusually large;
- price is far from support;
- stop distance becomes too wide.

Exact thresholds should be refined during implementation and backtesting.

---

## 10. Position Sizing Requirements

## 10.1 MVP Position Sizing

Position sizing is optional in MVP.

If account size is not configured, the dashboard should show risk/reward without share quantity.

If account size is configured later:

```text
risk_dollars = account_equity * risk_per_trade_pct
position_size = risk_dollars / risk_per_share
```

Example:

```text
Account equity: $50,000
Risk per trade: 1%
Risk dollars: $500
Entry: $100
Stop: $95
Risk per share: $5
Position size: 100 shares
```

---

## 10.2 Default Risk Per Trade

Suggested defaults:

| Setting | Default |
| --- | --- |
| Conservative risk | 0.5% |
| Standard risk | 1.0% |
| Aggressive risk | 2.0% max, later only |

MVP recommendation:

> If position sizing is shown, default to 0.5% or 1.0% risk per trade.

---

## 10.3 Position Sizing Warnings

Warn when:

- stop distance is too small and share count becomes unrealistic;
- stop distance is too wide;
- estimated position value exceeds configured account limit;
- liquidity is too low;
- data is stale;
- account size is missing.

---

## 11. Caution Flags

MVP caution flags must be generated and visible.

## 11.1 Required Flags

| Flag | Trigger | Candidate Impact |
| --- | --- | --- |
| Data stale | Required OHLCV or indicator data is stale | Block |
| Data missing | Required price/volume/indicator data missing | Block |
| Earnings soon | Earnings within warning window | Watch/Avoid penalty |
| Low volume | Below liquidity threshold | Exclude or Avoid |
| Weak relative strength | Underperforming SPY | Score penalty |
| Overextended | Price too far from support/ATR range | Watch/Avoid penalty |
| Poor risk/reward | Below threshold | Watch/Avoid |
| High volatility | ATR% unusually high | Warning/penalty |
| Trend damaged | Price below required trend support | Avoid |
| Provider partial failure | Some source data failed | Warning or Block per symbol |

---

## 11.2 Caution Flag Severity

Use severity levels.

| Severity | Meaning |
| --- | --- |
| Info | Useful context, not dangerous |
| Warning | Should reduce confidence |
| Severe | Should usually prevent Actionable status |
| Blocking | Candidate cannot be judged |

---

## 11.3 Earnings Warning Window

Initial default:

| Window | Impact |
| --- | --- |
| Earnings within 1 trading day | Severe warning or Avoid |
| Earnings within 2–3 trading days | Warning / Watch |
| Earnings within 4–7 trading days | Info or mild warning |
| No known upcoming earnings | No warning |
| Missing earnings data | Missing context warning |

Reason:

Earnings can invalidate technical setups quickly.

---

## 12. Candidate Status Rules

Candidate status should combine setup, score, risk, and data quality.

| Status | Conditions |
| --- | --- |
| Actionable | Strong setup, fresh data, acceptable risk/reward, no severe caution |
| Watch | Interesting but needs cleaner entry, confirmation, or lower risk |
| Avoid | Poor setup, damaged trend, overextension, weak volume, or poor risk/reward |
| Blocked | Missing/stale/invalid required data |

Important:

> Actionable means worth manual review now. It does not mean buy.

---

## 13. Backtesting Purpose

Backtesting tests strategy rules on historical data.

PoorToPour needs backtesting to answer:

- Did the setup historically produce useful candidates?
- Did candidates outperform SPY?
- How often did signals fail?
- What was the average forward return?
- What was the downside after signal?
- Which setup families performed best?
- Which caution flags predicted poor outcomes?
- Are we fooling ourselves with pretty charts?

Backtesting should be used to improve the scanner, not to guarantee future performance.

---

## 14. Backtesting Scope

## 14.1 MVP Readiness Requirement

MVP does not need a full backtesting UI, but strategy code should be designed so it can be backtested later.

Requirements from the beginning:

- deterministic strategy rules;
- stored rule pass/fail outputs;
- scan timestamp and market date separation;
- strategy versioning;
- score versioning;
- no future data leakage;
- reproducible inputs.

---

## 14.2 First Backtesting Version

The first backtesting version should be simple.

Inputs:

- historical daily OHLCV;
- selected universe;
- selected setup type;
- selected date range;
- strategy/scoring version.

Outputs:

- signal dates;
- candidates generated;
- forward returns;
- comparison to SPY;
- win rate;
- average/median return;
- max adverse excursion;
- max favorable excursion;
- simple R multiple if stop/target are simulated.

---

## 15. Backtesting Windows

Initial forward-return windows:

| Window | Purpose |
| --- | --- |
| 1 trading day | Very short follow-through |
| 5 trading days | One-week behavior |
| 10 trading days | Two-week behavior |
| 20 trading days | Swing-trade behavior |
| 60 trading days | Longer-term context, optional later |

MVP+ recommendation:

> Use 1D, 5D, 10D, and 20D windows first.

---

## 16. Backtesting Metrics

## 16.1 Core Metrics

| Metric | Purpose |
| --- | --- |
| Candidate count | Signal frequency |
| Win rate | Percent of positive outcomes |
| Average return | Mean forward return |
| Median return | Typical forward return |
| Max adverse excursion | Worst move against candidate during holding window |
| Max favorable excursion | Best move in favor during holding window |
| Average R multiple | Return normalized by initial risk |
| Hit target rate | How often target reached |
| Hit stop rate | How often stop reached |
| SPY-relative return | Did candidate beat market? |
| Setup family performance | Compare breakout/pullback/relative strength |

---

## 16.2 Quality Metrics

| Metric | Purpose |
| --- | --- |
| False positive rate | How many candidates looked good but failed quickly |
| Actionable vs Watch performance | Check label quality |
| Score bucket performance | Confirm high scores perform better |
| Caution flag impact | See if warnings predict weak outcomes |
| Sector concentration | Identify overdependence |
| Market regime sensitivity | See if strategy only works in bull markets |

---

## 17. Bias and Validation Risks

## 17.1 Lookahead Bias

Lookahead bias happens when backtesting uses information that would not have been available at signal time.

Examples:

- using full-day close to simulate an entry earlier that same day;
- using future earnings dates incorrectly;
- using current index membership for old dates without caution.

Rule:

> Backtests must only use data available at the simulated decision time.

---

## 17.2 Survivorship Bias

Survivorship bias happens when historical tests only include stocks that survived until today.

Example:

Testing on today’s S&P 500 constituents over the last 10 years ignores companies that were removed from the index.

MVP limitation:

> Early backtests may use current S&P 500 membership, but results must be labelled as survivorship-biased.

Later improvement:

- use historical index constituents;
- use broader survivorship-bias-aware dataset.

---

## 17.3 Overfitting

Overfitting happens when a strategy is tuned too closely to historical data.

Symptoms:

- many precise thresholds;
- great backtest, poor forward results;
- strategy only works on one period;
- small changes destroy performance.

Rule:

> Avoid threshold over-optimization until we have enough data and forward testing.

---

## 17.4 Data Snooping

Data snooping happens when many strategies are tested and only the best-looking result is reported.

Rule:

- record tested variants;
- preserve failed experiments;
- do not only document winners;
- use out-of-sample and forward testing later.

---

## 18. Backtesting Architecture Requirements

Detailed architecture belongs in `/docs/03-technical-architecture.md`, but the risk/backtesting layer requires these capabilities.

Backtest engine should:

- accept a strategy version;
- accept date range;
- accept universe;
- accept setup type(s);
- replay historical dates;
- generate signals using only past/current data;
- record generated candidates;
- calculate forward returns;
- compare to SPY;
- save results.

Suggested tables later:

| Table | Purpose |
| --- | --- |
| `backtest_runs` | Backtest metadata |
| `backtest_signals` | Signals generated during test |
| `backtest_outcomes` | Forward returns and metrics |
| `backtest_summary_metrics` | Aggregated performance |
| `strategy_versions` | Rule/scoring version history |

---

## 19. Paper Trading Requirements

## 19.1 Purpose

Paper trading tests strategy behavior in real time without real money.

It helps validate:

- scan reliability;
- signal usefulness;
- entry/exit assumptions;
- stop/target logic;
- risk metrics;
- user workflow;
- emotional realism.

---

## 19.2 Paper Trading Entry Gate

PoorToPour should not add paper trading until:

| Requirement | Gate |
| --- | --- |
| Scanner produces stable candidates | Required |
| Scan history works | Required |
| Candidate scoring is explainable | Required |
| Risk/reward estimates exist | Required |
| Basic backtesting exists | Preferred before paper trading |
| Data freshness logic works | Required |
| Candidate status rules work | Required |

---

## 19.3 Paper Trading Features

Future paper-trading module should include:

- simulated entry;
- simulated stop;
- simulated target;
- position status;
- exit reason;
- realized/unrealized R;
- trade notes;
- strategy version;
- source scan/candidate link.

---

## 19.4 Paper Trading Metrics

Track:

- win rate;
- average R;
- max drawdown;
- target hit rate;
- stop hit rate;
- average hold time;
- strategy performance by setup type;
- performance versus SPY;
- false positive review notes.

---

## 20. Live Automation Requirements

Live broker automation is future-only.

## 20.1 Automation Prerequisites

Before live broker automation, PoorToPour must have:

| Requirement | Status Needed |
| --- | --- |
| Historical backtesting | Required |
| Forward/paper trading | Required |
| Risk limits | Required |
| Kill switch | Required |
| Broker sandbox testing | Required |
| Manual override | Required |
| Audit logs | Required |
| Error handling | Required |
| Monitoring/alerts | Required |
| Secret management | Required |
| Live/paper mode separation | Required |

---

## 20.2 Hard Automation Rules

Future live automation must enforce:

- max risk per trade;
- max daily loss;
- max weekly loss;
- max open positions;
- max sector exposure;
- no trade if data stale;
- no trade if provider status unhealthy;
- no trade if strategy version unapproved;
- no trade during blocked state;
- no trade if kill switch active;
- no trade around earnings unless explicitly allowed.

---

## 20.3 Kill Switch Requirements

The kill switch must:

- immediately prevent new orders;
- optionally cancel pending orders;
- display active state clearly;
- be available from dashboard;
- be logged when activated/deactivated;
- default to safe state if system is uncertain.

MVP note:

No kill switch UI is needed until broker/paper automation exists, but the requirement should remain documented.

---

## 21. Risk Dashboard Requirements

MVP dashboard risk display:

| UI Element | Required |
| --- | --- |
| Caution flags in candidate table | Yes |
| Risk/reward card in candidate detail | Yes |
| Data freshness badges | Yes |
| Blocked status for missing/stale data | Yes |
| Scan partial failure warnings | Yes |

MVP+ / later:

| UI Element | Future |
| --- | --- |
| Portfolio risk panel | Later |
| Paper trade performance | Later |
| Drawdown chart | Later |
| Strategy backtest dashboard | Later |
| Automation kill switch | Future only |
| Max daily loss panel | Future only |

---

## 22. Scanner Quality Review

Before spending more on data/AI or moving toward paper trading, review scanner quality.

Suggested review period:

> 2–4 weeks of daily/weekly scan output.

Review questions:

- Are candidates understandable?
- Are high-scoring candidates visibly stronger?
- Are many candidates obviously junk?
- Are caution flags useful?
- Are false positives explainable?
- Is risk/reward often reasonable?
- Does the scanner produce too many or too few candidates?
- Do results look better than random browsing?
- Would better data or AI summaries improve the workflow?

---

## 23. MVP Risk and Backtesting Definition of Done

This planning area is complete when:

| ID | Requirement | Status |
| --- | --- | --- |
| RISK-001 | Candidate risk model is defined | Required |
| RISK-002 | Entry/invalidation/stop/target concepts are defined | Required |
| RISK-003 | Risk/reward labels are defined | Required |
| RISK-004 | Required caution flags are defined | Required |
| RISK-005 | Candidate status rules are tied to risk/data quality | Required |
| RISK-006 | Backtesting purpose is defined | Required |
| RISK-007 | Backtesting windows are defined | Required |
| RISK-008 | Core backtesting metrics are defined | Required |
| RISK-009 | Bias risks are documented | Required |
| RISK-010 | Paper trading gate is defined | Required |
| RISK-011 | Live automation prerequisites are defined | Required |
| RISK-012 | Kill switch requirements are documented | Required |
| RISK-013 | Scanner quality review criteria are defined | Required |

---

## 24. Risk and Backtesting Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| RISK-D-001 | MVP risk outputs are research estimates only | Avoids overstating scanner authority |
| RISK-D-002 | 2:1 risk/reward is the initial preferred minimum for Actionable swing candidates | Simple, conservative starting point |
| RISK-D-003 | Missing/stale required price data blocks candidates | Data quality is safety-critical |
| RISK-D-004 | Earnings soon should create caution or downgrade | Earnings can invalidate technical setups |
| RISK-D-005 | Backtesting UI is not required for MVP, but strategy logic must be backtestable | Avoids rewriting strategy later |
| RISK-D-006 | Early backtests may be survivorship-biased but must be labelled | Practical starting point with honest limitation |
| RISK-D-007 | Paper trading is required before broker automation | Safer validation path |
| RISK-D-008 | Broker automation requires kill switch, risk limits, audit logs, and monitoring | Prevents unsafe live execution |
| RISK-D-009 | AI must not make risk or trade decisions in MVP | Keeps output deterministic and explainable |
| RISK-D-010 | Scanner quality should be reviewed for 2–4 weeks before increasing data/AI spend | Spending should follow evidence |

---

## 25. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-RISK-001 | Should position sizing appear in MVP? | Maybe, only if account-size config is simple | Open |
| Q-RISK-002 | What exact ATR buffer should be used for stops? | TBD during implementation/testing | Open |
| Q-RISK-003 | What exact overextension threshold should be used? | TBD during implementation/testing | Open |
| Q-RISK-004 | Should earnings within 3 days force Watch/Avoid? | Likely yes | Open |
| Q-RISK-005 | Should Actionable require 2R minimum? | Yes by default | Open |
| Q-RISK-006 | Should first backtest use current S&P 500 membership? | Yes, with survivorship-bias warning | Open |
| Q-RISK-007 | Should scanner quality review be manual first? | Yes | Open |
| Q-RISK-008 | What is the minimum paper-trading period before automation? | TBD later, likely months not days | Open |
| Q-RISK-009 | What max daily loss should future automation use? | TBD much later | Open |
| Q-RISK-010 | Should future paper trading support partial exits? | Later | Open |

---

## 26. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial risk and backtesting document | Jesse + AI |
