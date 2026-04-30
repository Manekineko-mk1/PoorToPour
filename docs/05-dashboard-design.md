# PoorToPour Dashboard Design

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/05-dashboard-design.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.1

---

## 1. Purpose

This document defines the initial dashboard design requirements for PoorToPour.

It answers:

- What should the MVP dashboard show?
- What screens are required?
- What information should be visible on each screen?
- How should trade candidates be ranked and reviewed?
- How should charts, scores, caution flags, and risk/reward be displayed?
- How should data freshness and scan status be communicated?
- What should be deferred to MVP+ or later?

This document focuses on user interface, dashboard flow, and visual information design. It does not define detailed trading formulas, backend architecture, or provider choices.

Related documents:

| File | Purpose |
| --- | --- |
| `/docs/00-project-plan.md` | Project vision, MVP boundary, and roadmap |
| `/docs/01-product-requirements.md` | Product workflows, screens, and user-facing requirements |
| `/docs/02-trading-strategy-requirements.md` | Strategy rules, indicators, scoring, and risk logic |
| `/docs/02a-trading-concepts-glossary.md` | Trading concepts used by the strategy document |
| `/docs/03-technical-architecture.md` | System design, modules, services, and data flow |
| `/docs/04-data-sources.md` | Data providers, limits, and freshness rules |
| `/docs/06-risk-and-backtesting.md` | Risk controls and validation methods |
| `/docs/07-cost-and-operations.md` | Cost estimates and operating constraints |
| `/docs/08-execution-tracker.md` | Current project progress |
| `/docs/09-decision-log.md` | Accepted project decisions |
| `/docs/10-ai-working-guidelines.md` | AI workflow and engineering standards |

---

## 2. Dashboard Design Goals

The dashboard should feel like a compact personal trading research terminal.

It should not feel like:

- a generic admin dashboard;
- a toy stock screener;
- a crypto casino;
- a beautiful but vague AI-generated horoscope machine.

The dashboard should help the user answer:

1. Did the latest scan run successfully?
2. Are there any interesting candidates?
3. Why did each candidate appear?
4. Is the data fresh?
5. Is the candidate technically strong?
6. Is risk/reward reasonable?
7. Are there caution flags?
8. Should I inspect, watch, avoid, or manually research further?

Design principle:

> The dashboard should make evidence easier to inspect, not make weak signals look fancy.

---

## 3. Visual Style Direction

## 3.1 Overall Style

Recommended style:

| Attribute | Direction |
| --- | --- |
| Theme | Dark mode first |
| Density | Compact but readable |
| Mood | Professional trading terminal with personal-project charm |
| Layout | Card + table + chart driven |
| Typography | Clean, legible, not overly decorative |
| Motion | Minimal, useful only |
| Color | Functional and consistent |
| Data display | Timestamped, traceable, and honest |

---

## 3.2 Dark Mode First

MVP should prioritize dark mode.

Reason:

- trading dashboards often show dense data;
- charts are easier to inspect for long sessions;
- visual contrast helps status/caution indicators;
- aligns with the “research cockpit” feel.

MVP does not need light mode.

Future:

- add light mode only if trivial or genuinely desired.

---

## 3.3 Layout Philosophy

Use a three-level information hierarchy:

| Level | Purpose |
| --- | --- |
| Overview | Show scan health and top candidates |
| Ranking | Compare candidates quickly |
| Detail | Inspect chart, score, explanation, and risk |

Avoid cramming everything into one screen.

---

## 4. MVP Screens

MVP requires four screens:

| Screen | MVP | Purpose |
| --- | --- | --- |
| Dashboard Home | Yes | Latest scan summary and ranked candidates |
| Candidate Detail | Yes | Deep review of one ticker |
| Scan History | Yes | Prior scan runs and status |
| Settings | Yes | Basic scan configuration |

MVP+ screens:

| Screen | Purpose |
| --- | --- |
| Watchlist | Save and monitor selected tickers |
| Backtesting | Review strategy performance |
| Alerts | Configure notifications |
| Cost/Usage | View provider/AI usage and estimated cost |
| News/Catalyst Feed | Review post-MVP context layer |
| Paper Trading | Simulated trade tracking |
| Automation Control | Future broker guardrails |

---

## 5. Navigation Design

## 5.1 Primary Navigation

Recommended left sidebar or top navigation:

| Navigation Item | Route | MVP |
| --- | --- | --- |
| Dashboard | `/` or `/dashboard` | Yes |
| Candidates | `/candidates` | Maybe, if separate from Dashboard |
| Scan History | `/scans` | Yes |
| Settings | `/settings` | Yes |
| Watchlist | `/watchlist` | MVP+ |
| Backtesting | `/backtesting` | Later |
| Alerts | `/alerts` | Later |
| Cost / Usage | `/usage` | MVP+ |
| Paper Trading | `/paper-trading` | Later |

MVP recommendation:

> Keep navigation minimal: Dashboard, Scan History, Settings.

Candidate details can be accessed from the dashboard table.

---

## 5.2 Header Bar

The dashboard header should show:

| Item | Purpose |
| --- | --- |
| App name | PoorToPour |
| Environment | Local / Hosted / Paper / Live later |
| Current data mode | MVP data provider / fixture mode |
| Last successful scan | Freshness |
| Global warnings | Stale data, failed job, provider error |
| Manual scan action | Trigger scan |

Future:

- show monthly cost estimate;
- show paper/live mode indicator;
- show kill switch if automation exists.

---

## 6. Dashboard Home

## 6.1 Purpose

The Dashboard Home is the main command center.

It should answer:

- What happened in the latest scan?
- How many candidates appeared?
- Which candidates deserve attention?
- Is anything stale, broken, or risky?

---

## 6.2 Dashboard Home Sections

Recommended MVP layout:

```text
Header / Global Status
  |
  +-- Latest Scan Summary Cards
  |
  +-- Candidate Ranking Table
  |
  +-- Caution / Data Health Panel
```

Optional MVP+ layout:

```text
Header / Global Status
  |
  +-- Latest Scan Summary Cards
  |
  +-- Market Snapshot
  |
  +-- Candidate Ranking Table
  |
  +-- Caution / Data Health Panel
  |
  +-- Recent Scan History
```

---

## 6.3 Latest Scan Summary Cards

Required cards:

| Card | Example | Purpose |
| --- | --- | --- |
| Scan Status | Succeeded | Did it run? |
| Scan Type | Daily | Daily or weekly |
| Universe | S&P 500 | What was scanned |
| Symbols Processed | 497 / 503 | Coverage |
| Candidates Found | 18 | Signal density |
| Last Scan Time | 2026-04-30 16:30 | Freshness |
| Data Date | 2026-04-30 | Market data date |
| Provider Status | Healthy / Partial | Data reliability |

Optional cards:

| Card | Purpose |
| --- | --- |
| Top Setup Type | Shows which setup dominated |
| Average Candidate Score | Quality signal |
| Failed Symbols | Troubleshooting |
| Estimated Cost MTD | MVP+ cost visibility |

---

## 6.4 Candidate Ranking Table

The candidate table is the MVP's most important UI element.

Default behavior:

- sort by score descending;
- show latest scan candidates;
- allow setup/status filtering;
- show warning badges clearly;
- clicking ticker opens Candidate Detail page.

Recommended columns:

| Column | Required | Notes |
| --- | --- | --- |
| Rank | Yes | Numeric rank |
| Ticker | Yes | Link to detail |
| Company | Yes | Human-readable name |
| Setup | Yes | Breakout / Pullback / Relative Strength |
| Status | Yes | Actionable / Watch / Avoid / Blocked |
| Score | Yes | 0–100 or N/A |
| Price | Yes | Latest close used |
| Change % | Preferred | Daily move |
| Relative Volume | Yes | Participation |
| RSI | Yes | Momentum |
| Distance from High / Support | Yes | Setup context |
| Risk/Reward | Yes | Research estimate |
| Caution Flags | Yes | Badges |
| Last Updated | Yes | Freshness |

MVP table actions:

| Action | MVP |
| --- | --- |
| Open detail | Yes |
| Filter by setup | Yes |
| Filter by status | Yes |
| Sort by score | Yes |
| Sort by risk/reward | Preferred |
| Export | MVP+ |
| Add to watchlist | MVP+ unless trivial |

---

## 6.5 Candidate Table Status Badges

Status should be visually distinct.

| Status | Meaning | UI Treatment |
| --- | --- | --- |
| Actionable | Worth manual review now | Strong positive badge |
| Watch | Interesting but not clean yet | Neutral/attention badge |
| Avoid | Poor risk or weak setup | Negative badge |
| Blocked | Cannot judge due to data issue | Disabled/error badge |

Important:

- `Actionable` must not mean “buy.”
- `Blocked` must be visually obvious.
- Data issues should never be hidden behind a score.

---

## 6.6 Caution Flag Badges

Common caution flags:

| Flag | Example Badge Text |
| --- | --- |
| Earnings soon | Earnings in 2D |
| Stale data | Stale OHLCV |
| Missing data | Missing earnings |
| Overextended | Extended |
| Low volume | Low volume |
| Weak relative strength | Weak vs SPY |
| Poor risk/reward | < 2R |
| High volatility | High ATR |
| Broken trend | Trend damaged |

Badge design:

- short text;
- consistent severity color;
- tooltip/hover detail later;
- candidate detail page shows full explanation.

---

## 7. Candidate Detail Page

## 7.1 Purpose

The Candidate Detail page is the deep review screen.

It should answer:

- Why did this ticker appear?
- What does the chart show?
- Which rules passed or failed?
- Is the score justified?
- What are the risks?
- Is the candidate worth manual research?

---

## 7.2 Candidate Detail Layout

Recommended MVP layout:

```text
Candidate Header
  |
  +-- Chart Panel
  |
  +-- Setup Explanation + Score Breakdown
  |
  +-- Risk/Reward Card + Caution Flags
  |
  +-- Company / Earnings Snapshot
```

For desktop:

```text
[Chart Panel - Wide]
[Explanation / Score] [Risk / Context]
```

For smaller screens:

```text
Chart
Explanation
Risk
Company Context
```

---

## 7.3 Candidate Header

Required fields:

| Field | Example |
| --- | --- |
| Ticker | MSFT |
| Company | Microsoft Corp. |
| Setup | Pullback continuation |
| Status | Watch |
| Overall Score | 78 |
| Last Scan | 2026-04-30 16:30 |
| Data Date | 2026-04-30 |
| Data Status | Fresh |

Header actions:

| Action | MVP |
| --- | --- |
| Back to dashboard | Yes |
| Open external chart | Maybe |
| Add to watchlist | MVP+ |
| Export note | MVP+ |

---

## 7.4 Chart Panel

MVP chart requirements:

| Chart Element | MVP | Notes |
| --- | --- | --- |
| Candlestick chart | Yes | Main visual |
| Volume bars | Yes | Participation |
| SMA 20 | Yes | Short-term trend |
| SMA 50 | Yes | Medium-term trend |
| SMA 200 | Yes | Long-term trend |
| RSI panel | Yes | Momentum |
| Breakout/support marker | Preferred | Helpful if simple |
| Entry/stop/target lines | Preferred | Research estimates only |
| MACD panel | Maybe | Optional |
| EMA 8/21 | Maybe | Optional |
| VWAP | No | Intraday/post-MVP |

Chart time ranges:

| Range | MVP |
| --- | --- |
| 3 months | Yes |
| 6 months | Yes |
| 1 year | Yes |
| 2 years | Maybe |
| Intraday | No |

Default chart range:

> 6 months.

Reason:

- enough to see swing structure;
- not too zoomed out;
- works well for daily/weekly setup review.

---

## 7.5 Chart Interaction

MVP interactions:

| Interaction | MVP |
| --- | --- |
| Hover candle values | Yes if chart library supports |
| Switch range | Yes |
| Toggle moving averages | Preferred |
| Zoom/pan | Chart library default |
| Tooltip with OHLCV | Preferred |
| Draw trendlines manually | No |
| Save chart annotations | No |
| Compare with SPY | MVP+ |

---

## 7.6 Setup Explanation Panel

The explanation panel should be generated from structured rule outputs.

Required content:

| Content | Purpose |
| --- | --- |
| Setup summary | Plain-English reason ticker appeared |
| Passed required rules | Evidence |
| Failed required rules | Explain why not Actionable |
| Passed preferred rules | Confidence context |
| Failed preferred rules | Weakness context |
| Caution flags | Risk context |

Example:

```text
MSFT matched the pullback continuation setup.

Passed:
- Price remains above SMA 50 and SMA 200.
- Price pulled back near SMA 20.
- 20-day relative strength versus SPY is positive.

Warnings:
- Earnings are in 3 trading days.
- Risk/reward is below 2R at current price.
```

Rule display requirement:

- Rules should use human-readable text.
- Stable rule IDs may be shown in advanced/details view.
- Avoid unexplained jargon in the main explanation.

---

## 7.7 Score Breakdown Panel

The score breakdown should show major components.

Recommended UI:

| Component | Value |
| --- | ---: |
| Setup Match | 34 / 40 |
| Volume | 11 / 15 |
| Relative Strength | 13 / 15 |
| Risk/Reward | 8 / 15 |
| Context/Caution | 9 / 15 |
| Total | 75 / 100 |

Visual treatment:

- horizontal bars or compact score rows;
- clear max score;
- show penalties;
- show score version.

Required fields:

| Field | Purpose |
| --- | --- |
| Component score | Explain ranking |
| Component max | Show weighting |
| Score version | Traceability |
| Computed timestamp | Freshness |

---

## 7.8 Risk/Reward Card

Required fields:

| Field | Example |
| --- | --- |
| Entry Zone | $100–$102 |
| Invalidation Level | Below $98 |
| Stop Estimate | $97.50 |
| Target Estimate | $110 |
| Risk/Reward | 2.4R |
| ATR 14 | $2.10 |
| Stop Distance | 3.8% |
| Risk Label | Acceptable / Wide / Poor |

Important wording:

> Risk/reward is a research estimate, not a trading instruction.

UI requirements:

- show estimates clearly;
- show uncertainty/caution;
- do not visually imply guaranteed profit;
- show warning if risk/reward is unavailable.

---

## 7.9 Company and Earnings Snapshot

Required MVP fields where available:

| Field | Example |
| --- | --- |
| Company Name | Microsoft Corp. |
| Sector | Technology |
| Industry | Software |
| Market Cap | $3.1T |
| Exchange | NASDAQ |
| Next Earnings | 2026-07-24 |
| Last Earnings | 2026-04-24 |
| Earnings Warning | None / Earnings soon |

Optional:

| Field | MVP |
| --- | --- |
| Business summary | Preferred |
| Revenue growth | Post-MVP |
| EPS surprise | Post-MVP |
| Analyst rating | Post-MVP |
| News headlines | Post-MVP |

---

## 8. Scan History Page

## 8.1 Purpose

The Scan History page shows previous scan runs.

It supports:

- traceability;
- debugging;
- reviewing past candidates;
- future backtesting workflow.

---

## 8.2 Scan History Table

Recommended columns:

| Column | Required | Notes |
| --- | --- | --- |
| Scan ID | Yes | Internal link |
| Scan Type | Yes | Daily / weekly / manual |
| Status | Yes | Succeeded / failed / partial |
| Started At | Yes | Job timestamp |
| Completed At | Yes | Job timestamp |
| Market Date | Yes | Data date |
| Universe | Yes | S&P 500 |
| Symbols Processed | Yes | Coverage |
| Candidates Found | Yes | Signal density |
| Provider Errors | Preferred | Troubleshooting |
| Estimated Cost | MVP+ | Later cost tracking |

Actions:

| Action | MVP |
| --- | --- |
| Open scan details | Yes |
| Re-run scan | Maybe |
| Delete scan | No |
| Export scan | MVP+ |

---

## 8.3 Scan Details View

Required information:

| Section | Purpose |
| --- | --- |
| Scan metadata | When, what type, what universe |
| Candidate table | Results from that scan |
| Job errors/warnings | Reliability |
| Provider call summary | Troubleshooting |
| Data freshness summary | Trust |

---

## 9. Settings Page

## 9.1 Purpose

Settings should allow basic scan configuration without requiring code changes.

MVP settings should stay simple.

---

## 9.2 MVP Settings

| Setting | Default | MVP |
| --- | --- | --- |
| Universe | S&P 500 | Yes |
| Scan types | Daily + weekly | Yes |
| Max candidates | 25 | Yes |
| Minimum price | $5 | Yes |
| Minimum average dollar volume | $20M | Yes |
| Enabled setups | Breakout, pullback, relative strength | Yes |
| Manual scan enabled | true | Yes |
| Data provider display | Current provider name | Yes |
| AI enabled | false | Display only |
| AI budget | $0 | Display only |

Avoid in MVP:

- too many strategy knobs;
- advanced indicator thresholds;
- broker settings;
- AI agent controls;
- options/intraday settings.

---

## 9.3 Settings UX Rules

Settings should:

- show defaults clearly;
- validate input;
- explain risky changes;
- avoid exposing secrets;
- separate display settings from backend secrets;
- require confirmation for expensive scan changes later.

---

## 10. Data Freshness and Reliability Design

## 10.1 Freshness Indicators

Every screen should expose freshness.

Examples:

| UI Area | Freshness Display |
| --- | --- |
| Dashboard header | Last successful scan |
| Candidate row | Last updated |
| Candidate detail | Data date and computed timestamp |
| Scan history | Started/completed timestamps |
| Provider status | Healthy / partial / failed |

Freshness states:

| State | Display |
| --- | --- |
| Fresh | Normal |
| Stale | Warning |
| Missing | Warning/error |
| Invalid | Error |
| Unknown | Neutral warning |

---

## 10.2 Partial Failure Design

If a scan partially fails, the dashboard should not pretend everything is fine.

Example:

```text
Scan completed with warnings.
497 / 503 symbols processed.
6 symbols failed due to provider errors.
```

Candidate table should:

- exclude invalid candidates;
- show data warnings where relevant;
- show scan status in header.

---

## 11. Empty and Error States

## 11.1 Empty Candidate State

If no candidates are found:

```text
No candidates matched the current scan rules.
This can be normal. The scanner should not force low-quality ideas.
```

Optional details:

- symbols scanned;
- scan type;
- filters used;
- last successful scan time.

---

## 11.2 Failed Scan State

If scan fails:

```text
Latest scan failed.
Review job details or retry manually.
```

Show:

- failure time;
- job ID;
- error summary;
- retry action if safe;
- link to scan/job detail.

---

## 11.3 Stale Data State

If data is stale:

```text
Latest market data is stale.
Candidates may not reflect current market conditions.
```

Show:

- expected latest market date;
- actual latest market date;
- affected symbols;
- provider status.

---

## 12. MVP+ Features

The following should be deferred unless trivial.

## 12.1 Watchlist

Purpose:

Save interesting tickers for monitoring.

Features:

- add/remove ticker;
- notes;
- source scan;
- current status;
- last seen setup;
- watchlist filter on dashboard.

Reason to defer:

- adds persistence and UX decisions;
- not required for first scan-review workflow.

---

## 12.2 Exports

Possible exports:

- Markdown scan report;
- CSV candidate table;
- PDF research note;
- screenshot-style chart export.

Reason to defer:

- not needed for first interactive dashboard;
- useful after workflows stabilize.

---

## 12.3 Alerts

Possible alert types:

- new Actionable candidate;
- watched ticker status change;
- failed scan;
- stale data;
- budget threshold.

Reason to defer:

- requires notification provider;
- can create noise;
- should wait until scanner quality is known.

---

## 12.4 Cost / Usage Dashboard

Possible metrics:

- provider calls;
- estimated monthly data cost;
- AI usage;
- failed/retried calls;
- most expensive jobs.

Reason to defer:

- backend should log usage first;
- UI can come later.

---

## 12.5 News / Catalyst Feed

Post-MVP context layer.

Features:

- headlines;
- catalyst categories;
- ticker mapping;
- freshness/source labels.

Reason to defer:

- licensing/terms concerns;
- noisy mapping;
- not required for technical scanner MVP.

---

## 13. Accessibility and Usability

MVP should still follow basic accessibility practices.

Requirements:

| Requirement | Notes |
| --- | --- |
| Color not only signal | Use text labels and icons, not color alone |
| Keyboard navigation | Basic table/detail navigation should work |
| Contrast | Dark mode must remain readable |
| Tooltips | Helpful for glossary-like terms later |
| Responsive layout | Desktop-first, but avoid broken small screens |
| Clear language | Avoid unexplained jargon in main UI |

Future:

- add inline glossary links or help tooltips for concepts like RSI, ATR, R/R.

---

## 14. Performance Expectations

MVP dashboard should feel fast for S&P 500 scans.

Targets:

| Area | Target |
| --- | --- |
| Dashboard initial load | Fast enough for local use |
| Candidate table | Smooth with up to 100 rows |
| Candidate detail chart | Loads without noticeable lag |
| Scan history | Paginated if needed |
| API calls | Cached by frontend where practical |

Frontend should avoid:

- recomputing indicators;
- loading all historical candles for all symbols at once;
- rendering unnecessary huge tables;
- blocking UI during manual scan.

---

## 15. Component Recommendations

Suggested component groups:

```text
components/
  layout/
    AppShell
    HeaderBar
    SidebarNav
  cards/
    ScanSummaryCard
    ScoreCard
    RiskRewardCard
    DataHealthCard
  tables/
    CandidateRankingTable
    ScanHistoryTable
  charts/
    CandidateCandlestickChart
    VolumePanel
    RsiPanel
  status/
    StatusBadge
    CautionFlagBadge
    FreshnessBadge
  forms/
    SettingsForm
```

Feature-level components:

```text
features/
  dashboard/
  candidates/
  scans/
  settings/
```

---

## 16. API Data Needs by Screen

## 16.1 Dashboard Home

Needs:

| API | Purpose |
| --- | --- |
| `GET /api/scans/latest` | Latest scan summary |
| `GET /api/candidates` | Latest candidate list |
| `GET /api/jobs` | Optional latest job status |

---

## 16.2 Candidate Detail

Needs:

| API | Purpose |
| --- | --- |
| `GET /api/candidates/{symbol}` | Candidate summary and explanation |
| `GET /api/candidates/{symbol}/chart` | Candles and indicators |
| `GET /api/scans/{scan_id}` | Optional scan metadata |

---

## 16.3 Scan History

Needs:

| API | Purpose |
| --- | --- |
| `GET /api/scans` | Scan history table |
| `GET /api/scans/{scan_id}` | Scan detail |

---

## 16.4 Settings

Needs:

| API | Purpose |
| --- | --- |
| `GET /api/config` | Read settings |
| `PUT /api/config` | Update settings |
| `POST /api/scans/run` | Trigger manual scan |

---

## 17. Dashboard Design Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| UI-D-001 | MVP uses dark mode first | Better for dense chart/data review |
| UI-D-002 | MVP requires Dashboard, Candidate Detail, Scan History, and Settings | Covers scan-review workflow |
| UI-D-003 | Candidate ranking table is the central MVP surface | Main product value is ranked scan results |
| UI-D-004 | Candidate detail page must show chart, explanation, score, risk/reward, and context | Supports evidence-based manual review |
| UI-D-005 | Watchlist is MVP+ unless trivial | Avoids persistence/UX scope creep |
| UI-D-006 | Alerts are post-MVP | Avoid noise before scanner quality is known |
| UI-D-007 | Cost dashboard is MVP+ | Backend should log usage first; UI can follow |
| UI-D-008 | Data freshness must be visible throughout dashboard | Trading safety and trust |
| UI-D-009 | `Actionable` means worth manual review, not buy | Prevents overstating scanner authority |
| UI-D-010 | The dashboard must show partial/failed scans clearly | Avoids false confidence |

---

## 18. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-UI-001 | Should MVP use a left sidebar or top navigation? | Left sidebar for desktop | Open |
| Q-UI-002 | Which chart library should be used first? | TradingView Lightweight Charts or similar | Open |
| Q-UI-003 | Should MACD appear on candidate detail MVP? | Optional, not required | Open |
| Q-UI-004 | Should entry/stop/target lines appear on MVP chart? | Preferred if simple | Open |
| Q-UI-005 | Should user settings be UI-editable in first build? | Yes if simple; config file acceptable first | Open |
| Q-UI-006 | Should external TradingView chart links be included? | Maybe useful | Open |
| Q-UI-007 | Should glossary tooltips be included in MVP? | MVP+ unless trivial | Open |
| Q-UI-008 | Should Dashboard and Candidates be separate pages? | Not necessary for MVP | Open |
| Q-UI-009 | Should table support column customization? | No, later | Open |
| Q-UI-010 | Should scan results be exportable? | MVP+ | Open |

---

## 19. MVP Dashboard Definition of Done

The dashboard MVP is complete when:

| ID | Requirement | Status |
| --- | --- | --- |
| UI-001 | Dashboard Home shows latest scan summary | Required |
| UI-002 | Dashboard Home shows ranked candidate table | Required |
| UI-003 | Candidate rows show setup, status, score, flags, and freshness | Required |
| UI-004 | Candidate Detail page exists | Required |
| UI-005 | Candidate Detail shows candlestick chart and volume | Required |
| UI-006 | Candidate Detail shows SMA 20/50/200 | Required |
| UI-007 | Candidate Detail shows RSI | Required |
| UI-008 | Candidate Detail shows setup explanation | Required |
| UI-009 | Candidate Detail shows score breakdown | Required |
| UI-010 | Candidate Detail shows risk/reward card | Required |
| UI-011 | Candidate Detail shows company/earnings snapshot where available | Required |
| UI-012 | Scan History page exists | Required |
| UI-013 | Settings page exists or equivalent config flow exists | Required |
| UI-014 | Stale/missing/partial data states are visible | Required |
| UI-015 | Manual scan can be triggered from UI or development control | Required |
| UI-016 | Watchlist is implemented | MVP+ |
| UI-017 | Alerts are implemented | Post-MVP |
| UI-018 | Broker automation controls are implemented | Future only |

---

## 20. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial dashboard design document | Jesse + AI |
