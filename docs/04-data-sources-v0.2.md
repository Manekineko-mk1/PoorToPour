# PoorToPour Data Sources

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/04-data-sources.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.2

---

## 1. Purpose

This document defines PoorToPour's data-source strategy.

It answers:

- What data does the MVP need?
- Which data can be deferred?
- Which provider categories should be considered?
- How should provider abstraction work?
- What data freshness rules should apply?
- What are the major provider risks?
- What should we avoid overcommitting to too early?

This document does not make a final vendor selection. The MVP should keep provider choices flexible until implementation reveals actual usage, rate limits, reliability needs, and cost tolerance.

---

## 2. Data Source Philosophy

PoorToPour should be **provider-flexible, cost-aware, and data-honest**.

Core principles:

1. **Start with minimum useful data**
   - MVP needs daily OHLCV, symbol universe, basic company profile, and earnings context.
   - MVP does not need tick data, Level 2 data, options chains, or full real-time firehose.

2. **Provider abstraction from day one**
   - External provider response shapes must not leak into strategy or dashboard logic.
   - All provider data should be normalized into PoorToPour-owned models.

3. **Cache and reuse**
   - Avoid repeated provider calls when data has not changed.
   - Respect rate limits and cost constraints.

4. **Label freshness**
   - Every important data point should expose source and freshness state.
   - Stale data should produce warning or blocked status.

5. **Do not let alternative data drive MVP**
   - News, social media, prediction markets, and politician trades are post-MVP context layers.
   - They should not be used as primary trade triggers in the first version.

6. **Official and free where practical**
   - Use official public data where it fits, especially SEC EDGAR for filings/fundamental context later.
   - Do not let raw public data normalization delay the MVP.

7. **Tier 1 only for MVP**
   - MVP should use one primary provider-backed data source for core scanner inputs.
   - Tier 2 official public APIs and Tier 3 scraping are deferred to MVP+ or later.
   - Re-evaluate provider upgrades or hybrid sourcing only after the MVP scanner proves useful.

---

## 3. MVP Data Requirements

## 3.1 Required for MVP

| Data Category | Required | Purpose |
| --- | --- | --- |
| Symbol universe | Yes | Know which tickers to scan |
| Daily OHLCV | Yes | Candles, indicators, setup detection |
| Adjusted close | Preferred | More accurate historical analysis around splits/dividends |
| Company name | Yes | Dashboard display |
| Sector | Yes | Context and later sector analysis |
| Industry | Preferred | Better company context |
| Market cap | Preferred | Filtering and context |
| Average volume | Yes | Liquidity filtering |
| Earnings dates | Preferred | Earnings caution flags |
| Exchange | Preferred | Symbol metadata |

---

## 3.2 Not Required for MVP

| Data Category | MVP Status | Reason |
| --- | --- | --- |
| Real-time quotes | Not required | Daily/weekly scans first |
| Intraday candles | Not required | Day-trading engine is post-MVP |
| Tick data | Not required | Too expensive/noisy for MVP |
| Level 2/order book | Not required | Not needed for swing scanner |
| Options chains | Not required | Options are out of MVP scope |
| News headlines | Post-MVP | Useful later for context |
| Full article text | Post-MVP | Licensing and AI-cost concerns |
| Social-media firehose | Post-MVP | Noisy and potentially expensive |
| Polymarket/event markets | Post-MVP | Context only, not trade trigger |
| Politician trades | Post-MVP | Delayed context only |
| Broker account data | Future only | Requires security/risk controls |

---

## 4. Data Source Tier Strategy

## 4.1 Tier Definitions

PoorToPour should classify data sources into three tiers.

| Tier | Source Type | Examples | MVP Usage |
| --- | --- | --- | --- |
| Tier 1 | Proper provider/API | FMP-style provider, Finnhub, Twelve Data, Polygon-style market data provider | Yes |
| Tier 2 | Official public APIs/datasets | SEC EDGAR, government/public disclosure datasets | Deferred to MVP+ |
| Tier 3 | Web scraping/manual research helpers | Public webpages, investor relations pages, non-API pages | Deferred to MVP+ or experimental use only |

---

## 4.2 MVP Data Strategy

MVP should use **Tier 1 provider-backed data only** for core scanner inputs.

MVP core scanner inputs include:

- daily OHLCV;
- adjusted close if available;
- company name;
- sector;
- industry if available;
- market cap if available;
- average volume;
- earnings date if available.

Reasons:

- simpler implementation;
- fewer provider adapters;
- fewer legal/terms concerns;
- clearer data lineage;
- easier debugging;
- lower risk of mixing inconsistent sources;
- enough to answer whether the scanner can produce useful candidates.

MVP rule:

> If data affects candidate selection, scoring, risk/reward, or future execution readiness, it should come from a proper provider/API or a versioned local seed file, not scraping.

---

## 4.3 MVP+ Re-Evaluation

After the MVP scanner proves useful, re-evaluate whether to:

1. upgrade to a higher-quality paid provider;
2. add Tier 2 official public sources such as SEC EDGAR;
3. add limited Tier 3 scraping for supplemental context;
4. use a hybrid model combining paid market data with official public data;
5. add richer company, filings, news, social, or event data.

Evaluation criteria:

| Criterion | Question |
| --- | --- |
| Cost | Does the benefit justify monthly cost? |
| Reliability | Is the source stable enough for scheduled jobs? |
| Data quality | Does it improve scanner or research quality? |
| Legal/terms risk | Is usage allowed for the intended purpose? |
| Complexity | Does it add too much normalization or maintenance work? |
| Trading safety | Could stale or noisy data create false confidence? |

---

## 4.4 Web Scraping Policy

Web scraping is not part of the MVP.

Post-MVP, scraping may be considered only for supplemental, non-critical context or manual research helpers.

Allowed later:

- investor relations page discovery;
- public page monitoring for research context;
- one-off manual research helpers;
- non-critical supplemental metadata.

Not allowed:

- primary OHLCV source;
- candidate scoring input;
- risk/reward calculation input;
- future broker automation input;
- anything that must be highly reliable or legally clean.

Scraping rules if introduced later:

- respect website terms and robots guidance;
- use low request rates;
- cache results;
- store source URL and retrieval timestamp;
- treat scraped data as lower-confidence context;
- never let scraped data override Tier 1 provider data.

---

## 5. Data Source Categories

## 5.1 Market Data

Needed for:

- daily candles;
- indicator calculations;
- setup detection;
- chart rendering;
- scan history.

Minimum fields:

| Field | Notes |
| --- | --- |
| symbol | Ticker |
| date | Trading date |
| open | Daily open |
| high | Daily high |
| low | Daily low |
| close | Daily close |
| adjusted_close | Preferred |
| volume | Required |

MVP priority:

> Reliable daily OHLCV is the most important data source.

---

## 5.2 Symbol Universe Data

Needed for:

- S&P 500 universe;
- future Nasdaq 100 / Russell 1000 support;
- filtering inactive symbols;
- exchange and company metadata.

Possible sources:

- provider symbol list endpoint;
- public index constituent source;
- manually maintained seed file for MVP;
- later automated universe refresh.

MVP recommendation:

> Start with a versioned local S&P 500 symbol seed file, then automate refresh later.

Reason:

- avoids early provider dependency;
- easier reproducibility;
- enough for first scanner;
- can be validated manually.

---

## 5.3 Company Profile Data

Needed for:

- company name;
- sector;
- industry;
- exchange;
- market cap;
- business description.

MVP recommendation:

> Use provider profile data if available through the chosen market/fundamentals provider. Keep company profile optional enough that missing profile data warns but does not block price-based scans.

---

## 5.4 Earnings Data

Needed for:

- next earnings date caution flag;
- last earnings date context;
- basic earnings surprise later.

MVP recommendation:

> Include earnings date if available, but do not block the scanner if earnings data is missing. Show a warning instead.

Reason:

- earnings dates are useful but can vary by provider;
- missing earnings data should not break technical scanning;
- caution flags are still valuable when available.

---

## 5.5 Fundamentals and SEC Filings

Needed later for:

- financial statements;
- revenue/EPS growth;
- company background;
- earnings quality;
- filings-based research.

Possible source:

- SEC EDGAR APIs;
- paid fundamentals provider;
- Financial Modeling Prep / Finnhub / Twelve Data / similar.

MVP recommendation:

> Do not make full fundamental normalization part of the first MVP. Use minimal company/earnings context first.

---

## 5.6 News Headlines

Post-MVP context layer.

Needed later for:

- catalyst detection;
- earnings/news reaction context;
- analyst upgrades/downgrades;
- legal/regulatory events;
- M&A headlines.

MVP recommendation:

> Do not include news ingestion in MVP. Add headline-only ingestion later before full article processing.

Reasons:

- licensing concerns;
- article text can be expensive to process with AI;
- headline-to-ticker mapping can be noisy;
- not required for first technical scanner.

---

## 5.7 Social Media

Post-MVP context layer.

Possible sources:

- Reddit;
- X/Twitter;
- StockTwits;
- other finance communities.

MVP recommendation:

> Do not include social media in MVP.

Later approach:

- track mention count;
- track mention velocity;
- apply lightweight sentiment labels;
- avoid firehose ingestion;
- use strict cost/rate limits.

---

## 5.8 Polymarket / Prediction Markets

Post-MVP context layer.

Use cases:

- macro event probabilities;
- election/policy odds;
- Fed decision odds;
- sector/event context.

MVP recommendation:

> Do not include Polymarket in MVP. Later, treat it as event context only, not as a direct stock signal.

---

## 5.9 Politician Trade Records

Post-MVP context layer.

Use cases:

- delayed disclosure context;
- ticker-level political trade awareness;
- exploratory alternative-data research.

MVP recommendation:

> Do not include politician trades in MVP. Later, show as delayed context only.

Important:

Political trade records are not real-time institutional flow. They should never be treated as same-day trading triggers.

---

## 5.10 Broker Data

Future only.

Use cases:

- paper/live account status;
- positions;
- orders;
- fills;
- buying power;
- trade logs.

MVP recommendation:

> No broker integration in MVP.

Broker data requires:

- security design;
- token management;
- live/paper environment separation;
- kill switch;
- audit logs;
- risk limits;
- manual override.

---

## 6. Provider Abstraction Requirements

## 6.1 Provider Interfaces

Create internal provider interfaces.

Suggested interfaces:

```text
MarketDataProvider
CompanyProfileProvider
EarningsProvider
FundamentalsProvider
NewsProvider
SocialProvider
PredictionMarketProvider
PoliticalTradeProvider
BrokerProvider
```

MVP interfaces:

```text
MarketDataProvider
CompanyProfileProvider
EarningsProvider
```

Post-MVP interfaces:

```text
NewsProvider
SocialProvider
PredictionMarketProvider
PoliticalTradeProvider
BrokerProvider
```

---

## 6.2 Normalized Internal Models

Provider responses should map into PoorToPour-owned models.

Example models:

```text
DailyBar
SymbolProfile
CompanyProfile
EarningsEvent
ProviderCallLog
DataFreshnessStatus
```

Rules:

- Do not store provider response shape as strategy input.
- Do not expose provider-specific fields directly to frontend unless intentionally mapped.
- Keep raw provider payloads optional and short-retention.
- Store provider name and retrieval timestamp for traceability.

---

## 6.3 Provider Selection Must Be Deferrable

Architecture should allow changing providers later.

Reason:

- pricing changes;
- free tiers may be too limited;
- provider quality may vary;
- data coverage may differ;
- implementation needs are not fully known yet.

Provider choice should be treated as a configuration and adapter decision, not a strategy-engine decision.

---

## 7. Data Freshness Requirements

## 7.1 Freshness States

Use consistent freshness states.

| State | Meaning |
| --- | --- |
| Fresh | Data is recent enough for intended use |
| Stale | Data is older than expected but may still be displayed with warning |
| Missing | Required data is unavailable |
| Invalid | Data exists but failed validation |
| Unknown | Freshness cannot be determined |

---

## 7.2 MVP Freshness Rules

Suggested defaults:

| Data Type | Freshness Expectation | Candidate Impact |
| --- | --- | --- |
| Daily OHLCV | Latest completed trading day | Block if missing/stale |
| Indicator snapshot | Same scan run or same market date | Block if missing |
| Company profile | Within 30 days | Warn if stale/missing |
| Earnings date | Within 7 days during earnings season, otherwise 30 days | Warn if stale/missing |
| Market cap | Within 7 days if used for filter | Warn or skip filter if missing |
| Symbol universe | Within 30 days | Warn if stale |

---

## 7.3 Timestamp Requirements

Data records should include:

| Field | Purpose |
| --- | --- |
| `source` | Provider/source name |
| `market_date` | Date the market data represents |
| `retrieved_at` | When PoorToPour fetched the data |
| `as_of` | Provider's stated data timestamp if available |
| `computed_at` | When indicators/scores were computed |
| `freshness_status` | Fresh, stale, missing, invalid, unknown |

---

## 8. Provider Candidate Review

## 8.1 Alpha Vantage

Use cases:

- daily OHLCV;
- technical indicators;
- fundamentals in some endpoints;
- prototyping.

Current known constraints:

- Free stock API access is available.
- Standard free limit is very low at 25 API requests per day.
- Premium plans exist for higher usage.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Easy to start | Free rate limit likely too low for S&P 500 scans |
| Broad API catalog | Premium may be needed quickly |
| Useful for experiments | May not be ideal for automated universe-wide scans |

Recommendation:

> Consider for quick experiments, but avoid relying on the free tier for regular S&P 500 scans.

---

## 8.2 Financial Modeling Prep

Use cases:

- historical prices;
- company profiles;
- financial statements;
- earnings;
- reference data.

Current known constraints:

- Pricing page lists a free Basic tier with 250 calls/day.
- Provides many endpoints across historical prices, profile/reference data, and fundamentals.

MVP assessment:

| Pros | Cons |
| --- | --- |
| More generous free tier than some alternatives | Need to validate data quality and endpoint limits |
| Covers both prices and fundamentals | Plan limits may constrain full-universe scans |
| Good candidate for early MVP research | Must verify licensing/terms for intended use |

Recommendation:

> Preferred first MVP provider candidate for experimentation because it may cover multiple MVP needs with a manageable free tier.

MVP note:

> FMP-style provider-backed data fits the Tier 1-only MVP strategy better than scraping or hybrid sourcing.

---

## 8.3 Finnhub

Use cases:

- stock market data;
- company fundamentals;
- earnings/calendar data;
- alternative data;
- news/social-style data in some offerings.

Current known constraints:

- Offers a broad API surface.
- Pricing and included limits vary by plan.
- Some alternative/fundamental datasets may require paid access.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Broad data categories | Paid tier may be needed |
| Useful for company and context data | Need to verify exact limits before selection |
| Can support future alternative data | More provider complexity than MVP may need |

Recommendation:

> Good candidate for MVP+ or post-MVP if we want one provider for market, company, earnings, and context data.

---

## 8.4 Twelve Data

Use cases:

- stock data;
- ETFs;
- forex/crypto;
- technical indicators;
- fundamentals in some offerings.

Current known constraints:

- Offers free access and paid plans.
- Provides stock APIs and 100+ technical indicators.
- Need to verify plan limits before final selection.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Broad product coverage | Exact limits/plan fit must be checked |
| Useful technical indicator endpoints | We prefer computing indicators internally for traceability |
| Global market coverage | May be more than MVP needs |

Recommendation:

> Candidate for provider comparison. Avoid relying on provider-computed indicators as the primary strategy source.

---

## 8.5 Polygon / Massive-style Market Data

Use cases:

- professional market data;
- historical aggregates;
- real-time/intraday data;
- future serious trading workflows.

Current known constraints:

- End-of-day and delayed tiers may be affordable.
- Real-time data generally costs more.
- Pricing and brand/provider structure should be rechecked before selection.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Strong market-data focus | May be more expensive than MVP needs |
| Better future path for intraday/real-time | Overkill for local-first scanner |
| Good developer experience | Paid plans likely needed for serious usage |

Recommendation:

> Keep as a serious post-MVP candidate. Do not start with expensive real-time data.

---

## 8.6 SEC EDGAR APIs

Use cases:

- company submissions;
- XBRL facts;
- filings and financial statement data;
- official public source.

Current known constraints:

- SEC provides RESTful APIs for company submissions and extracted XBRL data.
- Data is official and JSON-formatted.
- Raw data requires normalization.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Official public data | Requires mapping/normalization work |
| Free | Not a polished financial-data product |
| Strong source for filings/fundamentals | Can slow development if tackled too early |

Recommendation:

> Use later for official fundamentals/filings context. Do not let XBRL normalization block the MVP scanner.

---

## 8.7 Polymarket APIs

Use cases:

- event market context;
- macro/political probability changes;
- post-MVP event intelligence.

Current known constraints:

- Public market data APIs are available.
- Trading/order endpoints require authentication.
- PoorToPour should use only public market/event data if added.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Interesting event probability source | Mapping events to stocks is subjective |
| Public market data available | Should not drive direct trade decisions |
| Useful for macro context later | Not needed for MVP scanner |

Recommendation:

> Add post-MVP as event context only.

---

## 8.8 Quiver Quantitative / Political Trade Data

Use cases:

- U.S. Congress trading disclosures;
- lobbying/government-contract style alternative data;
- delayed political trade context.

Current known constraints:

- Political trade datasets exist through providers such as Quiver.
- Some access may require premium/API subscription.
- Public disclosures are delayed and should be treated cautiously.

MVP assessment:

| Pros | Cons |
| --- | --- |
| Interesting alternative context | Delayed and noisy |
| Can enrich candidate pages later | Not useful for real-time MVP signals |
| May support future research ideas | Access/pricing may matter |

Recommendation:

> Add later only as delayed context. Do not treat as intraday signal.

---

## 9. Recommended MVP Data Plan

## 9.1 MVP Phase 1 Data Plan

Recommended first implementation:

| Need | Approach |
| --- | --- |
| S&P 500 universe | Versioned local seed file |
| Daily OHLCV | One Tier 1 provider through `MarketDataProvider` |
| Company name/sector | Same Tier 1 provider if available, otherwise local seed/minimal profile |
| Earnings date | Same Tier 1 provider if available; warn if missing |
| Indicators | Compute internally via `IndicatorService` |
| Scan results | Store in PostgreSQL |
| Provider call logs | Store in job/provider logs |

---

## 9.2 Why Local Universe Seed First

Pros:

- avoids early provider dependency;
- reproducible scans;
- easy to inspect;
- good enough for S&P 500 MVP.

Cons:

- universe can become stale;
- requires manual update until automated;
- not ideal for historical backtesting with constituent changes.

Decision:

> Use a local S&P 500 seed file for MVP, then automate universe updates later.

---

## 9.3 Why Daily OHLCV First

Pros:

- enough for MVP swing scans;
- cheaper than intraday data;
- easier to backtest;
- less noisy;
- compatible with daily/weekly product direction.

Cons:

- cannot support true day-trading scans;
- misses intraday setup timing;
- delayed compared with real-time workflows.

Decision:

> Use daily OHLCV first. Add intraday candles only after the daily scanner proves useful.

---

## 10. Data Quality Validation

## 10.1 Required Validations

Daily bars should be validated before use.

Validation checks:

| Check | Rule |
| --- | --- |
| Required fields | open/high/low/close/volume/date must exist |
| Price sanity | high >= low |
| OHLC sanity | high >= open/close and low <= open/close |
| Volume sanity | volume >= 0 |
| Date sanity | market date is not in the future |
| Duplicate bars | one bar per symbol/date |
| Split adjustment awareness | adjusted close handled consistently |
| Missing recent bars | freshness warning/block |
| Extreme outliers | warn if suspicious |

---

## 10.2 Candidate Blocking Rules

Block a candidate when:

- required OHLCV is missing;
- recent daily bar is stale;
- required indicators cannot be computed;
- volume is missing or invalid;
- provider data failed validation;
- scan did not complete for the symbol.

Warn, but do not necessarily block, when:

- company profile is stale;
- earnings date is missing;
- market cap is missing;
- business summary is missing.

---

## 11. Caching and Retention

## 11.1 Caching Rules

Cache data where safe.

| Data Type | Cache Strategy |
| --- | --- |
| Historical daily bars | Store indefinitely for selected universe |
| Latest daily bar | Refresh once after market close |
| Company profile | Refresh weekly/monthly |
| Earnings calendar | Refresh daily during earnings season, otherwise weekly |
| Provider raw payloads | Optional short-retention only |
| AI summaries | Post-MVP, cache until source data changes |

---

## 11.2 Retention Rules

| Data Type | Suggested Retention |
| --- | --- |
| Daily OHLCV | Indefinite |
| Indicator snapshots | Keep scan-time snapshots |
| Scan runs | Indefinite initially |
| Job logs | 30–90 days |
| Provider call logs | 90 days |
| Raw provider payloads | 7–30 days if stored |
| Company profiles | Latest plus optional history |
| Earnings events | Keep historical earnings dates |

---

## 12. Cost and Rate Limit Controls

Data ingestion must respect cost constraints.

Required controls:

| Control | Requirement |
| --- | --- |
| Provider call logging | Track provider, endpoint, symbol, status |
| Rate limit handling | Backoff or stop when limits are reached |
| Batch requests | Use batch endpoints if available |
| Universe limits | MVP scans S&P 500 only |
| Manual scan guard | Prevent repeated expensive manual scans |
| Cache reuse | Do not refetch unchanged data unnecessarily |
| Feature toggles | Disable expensive providers/context layers |
| Cost estimates | Track estimated provider cost later |

---

## 13. Data Source Testing

Testing should cover provider normalization and data quality.

Test areas:

| Test | Purpose |
| --- | --- |
| Provider response fixture | Ensure API response maps correctly |
| Missing field fixture | Ensure invalid data is caught |
| Stale data fixture | Ensure freshness warning/block works |
| Rate limit error fixture | Ensure graceful failure |
| Partial universe failure | Ensure scan can continue as partial |
| Split/adjusted data fixture | Ensure adjusted close handling is consistent |
| Duplicate bars fixture | Ensure dedupe logic works |

---

## 14. Security and Compliance Notes

Rules:

- Never commit API keys.
- Store keys in environment variables or hosting secrets.
- Do not expose provider keys to frontend.
- Do not log API keys.
- Respect provider terms of service.
- Be careful with redistribution/display rights if the app is ever shared.
- Treat broker data as future high-risk data.
- Treat full news/article text as licensing-sensitive.

Important:

> PoorToPour is a personal project, but data-provider terms still matter.

---

## 15. Data Source Architecture Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| DATA-D-001 | MVP requires daily OHLCV first | Daily/weekly scanner depends on candles |
| DATA-D-002 | Use local S&P 500 seed file first | Keeps MVP reproducible and avoids early provider dependency |
| DATA-D-003 | Use provider abstraction from day one | Keeps vendor choice flexible |
| DATA-D-004 | Compute indicators internally through `IndicatorService` | Ensures traceability and avoids provider-computed black boxes |
| DATA-D-005 | Do not include real-time/intraday data in MVP | Reduces cost and complexity |
| DATA-D-006 | Do not include news/social/Polymarket/politician trades in MVP | Keeps scanner focused and cheaper |
| DATA-D-007 | Treat SEC EDGAR as a later official fundamentals source | Useful but normalization-heavy |
| DATA-D-008 | Missing price data blocks candidates; missing context data warns | Keeps trading safety high without blocking technical scans unnecessarily |
| DATA-D-009 | Final provider selection is deferred | Implementation needs and provider limits must be tested first |
| DATA-D-010 | Provider raw payloads should be optional and short-retention | Avoids database bloat and provider-shape coupling |
| DATA-D-011 | MVP uses Tier 1 provider-backed data only for core scanner inputs | Keeps implementation simple, reliable, and easier to validate |
| DATA-D-012 | Tier 2 official public APIs are deferred to MVP+ or later | Avoids normalization-heavy sources before scanner value is proven |
| DATA-D-013 | Tier 3 web scraping is deferred to MVP+ or later and only for supplemental non-critical context | Avoids fragile, legally ambiguous, or unreliable data in core scanner logic |
| DATA-D-014 | Re-evaluate provider upgrade versus hybrid sourcing after MVP scanner proves useful | Data cost and quality trade-offs need evidence before committing |

---

## 16. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-DATA-001 | Which market data provider should be used first? | Compare FMP, Twelve Data, Finnhub, Alpha Vantage, Polygon/Massive | Open |
| Q-DATA-002 | Should S&P 500 universe be manually seeded first? | Yes | Open |
| Q-DATA-003 | Should company profiles be required for MVP candidates? | Warn if missing, do not block | Open |
| Q-DATA-004 | Which provider has the best earnings-date coverage for MVP? | TBD | Open |
| Q-DATA-005 | Should adjusted close be required? | Preferred, but depends on provider | Open |
| Q-DATA-006 | Should we store raw provider payloads? | Short-retention only if useful | Open |
| Q-DATA-007 | Should provider call cost be estimated from day one? | Log calls first, estimate later | Open |
| Q-DATA-008 | Should SEC EDGAR be used in MVP? | No, post-MVP | Open |
| Q-DATA-009 | Should we use provider-computed indicators? | No for strategy source; okay for comparison/testing | Open |
| Q-DATA-010 | Should intraday data be added before backtesting? | No | Open |
| Q-DATA-011 | Should Tier 2 official public APIs be added in MVP+? | Re-evaluate after MVP scanner proves useful | Open |
| Q-DATA-012 | Should Tier 3 scraping be added later? | Only for supplemental non-critical context if justified | Open |
| Q-DATA-013 | Should we upgrade to a higher-quality paid provider instead of hybrid sourcing? | Re-evaluate after MVP | Open |

---

## 17. Recommended Provider Evaluation Checklist

Before selecting a provider, evaluate:

| Category | Questions |
| --- | --- |
| Coverage | Does it cover S&P 500 daily OHLCV reliably? |
| Adjustments | Does it provide adjusted close or split/dividend-adjusted data? |
| Rate limits | Can it scan 500 symbols daily without pain? |
| Batch support | Can multiple symbols be fetched efficiently? |
| Fundamentals | Does it include company profile and earnings dates? |
| Cost | Can MVP stay under target monthly budget? |
| Reliability | Is provider uptime acceptable? |
| Documentation | Is API behavior clear? |
| Licensing | Can data be displayed in a personal dashboard? |
| Historical depth | Is there enough history for SMA 200 and future backtests? |
| Error behavior | Are rate limits and missing data clear? |
| SDK quality | Is there a decent Python client or simple REST API? |

---

## 18. Recommended Next Steps

1. Keep provider selection deferred until implementation.
2. Treat Tier 1 provider-backed data as the only MVP source category for core scanner inputs.
3. Start implementation with provider interfaces and local fixtures.
4. Create a local S&P 500 seed file.
5. Prototype one or two Tier 1 providers with 5–10 symbols.
6. Measure rate limits, data quality, adjusted close behavior, and response shape.
7. Choose the first MVP provider after testing.
8. Document the final provider choice in `/docs/09-decision-log.md`.
9. Re-evaluate Tier 2 official public APIs, Tier 3 scraping, or higher-quality paid providers only after MVP scanner quality is demonstrated.
10. Update this file once provider experiments produce evidence.

---

## 19. Source Notes

Pricing, limits, and provider offerings change often. Re-check official pages before final vendor selection.

Initial references used for this draft:

- Alpha Vantage support / free limit: https://www.alphavantage.co/support/
- Alpha Vantage premium: https://www.alphavantage.co/premium/
- Financial Modeling Prep pricing: https://site.financialmodelingprep.com/pricing-plans
- Financial Modeling Prep developer docs: https://site.financialmodelingprep.com/developer/docs
- Finnhub: https://finnhub.io/
- Twelve Data: https://twelvedata.com/
- Twelve Data pricing: https://twelvedata.com/pricing
- Twelve Data stocks API: https://twelvedata.com/stocks
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC Developer Resources: https://www.sec.gov/about/developer-resources
- Polymarket API docs: https://docs.polymarket.com/api-reference/introduction
- Polymarket market data overview: https://docs.polymarket.com/market-data/overview
- Quiver Quantitative Congress trading: https://www.quiverquant.com/congresstrading/
- Quiver API page: https://www.quiverquant.com/congresstrading/stock/API

---

## 20. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-04-30 | v0.1 | Created initial data sources document | Jesse + AI |
| 2026-04-30 | v0.2 | Added Tier 1-only MVP data policy, MVP+ re-evaluation path, and web scraping policy | Jesse + AI |
