# PoorToPour Cost and Operations

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/07-cost-and-operations.md`  
**Date created:** 2026-04-30  
**Last updated:** 2026-04-30  
**Status:** Draft v0.1  
**Currency:** USD unless otherwise stated

---

## 1. Purpose

This document defines the cost and operating strategy for PoorToPour.

PoorToPour is a personal project with a large long-term ambition. That means the system must be built with cost discipline from the beginning.

This document answers:

- How much should the MVP cost to run?
- Which costs are acceptable now versus later?
- How should hosting, data, and AI usage be controlled?
- Which features are expensive and should be delayed?
- How do we prevent an AI-agent system from quietly becoming a money furnace?
- What operating modes should the project support?

This document is not the final vendor decision document. Detailed provider comparisons belong in `/docs/04-data-sources.md` and `/docs/03-technical-architecture.md`.

---

## 2. Cost Philosophy

PoorToPour should be **cheap by default and scalable by choice**.

The project should not require expensive cloud infrastructure, premium market data, or always-on AI agents to produce its first useful result.

Core principles:

1. **Local-first MVP**
   - The first usable version should run locally.
   - Hosting should be optional until the dashboard is worth keeping online.

2. **Deterministic before AI**
   - Technical indicators, setup detection, scoring, and risk estimates should be computed with deterministic code.
   - AI should not be required to produce MVP scan candidates.

3. **Batch before realtime**
   - Daily and weekly scans are cheaper and easier to validate than intraday scans.
   - Intraday scanning should be introduced only after the daily scanner is reliable.

4. **Cache before refetch**
   - Market data, company metadata, earnings dates, and AI summaries should be cached where safe.

5. **Budget caps before agents**
   - Any AI or agent workflow must have usage logging, monthly limits, and kill switches.

6. **No always-on AI swarm**
   - AI agents should not run continuously in MVP.
   - AI should be invoked for specific bounded tasks.

---

## 3. Cost Targets

## 3.1 MVP Cost Target

Recommended target:

| Mode | Monthly Target | Description |
| --- | ---: | --- |
| Local development | $0–$10 | Runs on local machine; optional API costs only |
| Low-cost hosted MVP | $10–$40 | Simple web app + small database |
| Comfortable hosted MVP | $40–$80 | More reliable app/database, limited AI usage |
| Post-MVP research mode | $80–$200 | Paid market data, light AI summaries, better hosting |
| Automation preparation mode | $200+ | Better data, monitoring, paper trading, broker sandbox |

Recommended MVP ceiling:

> The first serious MVP should aim to stay under **$50/month**.

Recommended personal comfort ceiling before paper trading:

> Avoid exceeding **$100/month** until the scanner produces useful candidates consistently for several weeks.

---

## 4. Recommended Operating Modes

## 4.1 Mode A — Local Research Mode

Purpose:

Build and test the MVP with minimum cost.

Typical cost:

| Category | Estimated Monthly Cost |
| --- | ---: |
| Hosting | $0 |
| Database | $0 |
| Market data | $0–$30 |
| AI | $0–$10 |
| Monitoring | $0 |
| Total | **$0–$40** |

Recommended for:

- Phase 0 planning.
- Phase 1 data foundation.
- Phase 2 scanner engine.
- Early dashboard development.
- Local-only manual scans.

Pros:

- Cheapest.
- Fastest development loop.
- No cloud deployment complexity.
- Easy to experiment.

Cons:

- Not always available remotely.
- Scheduled jobs only run when local machine is on.
- Less realistic operational environment.

Recommendation:

> Use Local Research Mode until the scanner and dashboard feel useful.

---

## 4.2 Mode B — Low-Cost Hosted MVP

Purpose:

Host the dashboard so it can run scheduled scans and be accessed remotely.

Typical cost:

| Category | Estimated Monthly Cost |
| --- | ---: |
| App hosting | $5–$25 |
| Database | $0–$25 |
| Market data | $0–$50 |
| AI | $0–$20 |
| Monitoring/logging | $0–$10 |
| Total | **$10–$80** |

Recommended for:

- Dashboard MVP.
- Scheduled daily/weekly scans.
- Remote review from laptop/tablet.
- Lightweight personal use.

Pros:

- Always available.
- Scheduled scans can run automatically.
- More realistic than local-only mode.

Cons:

- Requires basic deployment/security setup.
- Costs can creep if jobs are not controlled.
- Database and provider limits matter.

Recommendation:

> Use this after the local MVP can produce useful scan results.

---

## 4.3 Mode C — Research Desk Mode

Purpose:

Run a more serious personal research system with better data, richer context, and limited AI.

Typical cost:

| Category | Estimated Monthly Cost |
| --- | ---: |
| App hosting | $25–$85 |
| Database | $19–$55 |
| Market data | $50–$200 |
| AI | $20–$100 |
| Monitoring/logging | $0–$25 |
| Total | **$100–$400** |

Recommended for:

- Post-MVP research.
- News and earnings enrichment.
- More reliable data.
- Limited AI-generated candidate summaries.
- Backtesting and paper-trading preparation.

Pros:

- More reliable.
- Better data quality.
- Supports richer workflows.

Cons:

- Costs become meaningful.
- More vendor lock-in risk.
- Requires stricter budgeting and logging.

Recommendation:

> Do not move here until the MVP proves the scanner is worth improving.

---

## 4.4 Mode D — Automation Preparation Mode

Purpose:

Prepare for controlled broker integration and paper trading.

Typical cost:

| Category | Estimated Monthly Cost |
| --- | ---: |
| Hosting/database | $50–$150 |
| Market data | $100–$500+ |
| AI | $50–$200+ |
| Monitoring/logging | $25–$100 |
| Broker/data tools | TBD |
| Total | **$225–$950+** |

Recommended for:

- Paper trading.
- Strategy validation.
- Automated alerting.
- Broker sandbox integration.
- Serious uptime and audit needs.

Pros:

- More realistic trading-system operation.
- Better observability.
- Safer path to automation.

Cons:

- Much more expensive.
- Requires stricter security.
- Requires operational discipline.
- Must not be attempted before validation.

Recommendation:

> This mode is post-MVP only. Do not connect broker automation until backtesting, paper trading, kill switch, and risk controls are mature.

---

## 5. Hosting Cost Options

## 5.1 Local Docker Compose

Use:

- FastAPI backend.
- React frontend.
- PostgreSQL.
- Optional Redis later.

Estimated cost:

| Item | Cost |
| --- | ---: |
| Local machine | $0 incremental |
| Docker Desktop / Docker Engine | $0 |
| PostgreSQL container | $0 |
| Redis container | $0 |
| Total | **$0** |

Recommendation:

> Use this for MVP development.

---

## 5.2 Railway

Railway is convenient for small apps and side projects.

Current pricing anchor:

- Hobby includes $5 of monthly usage credit.
- Usage above included credit is billed based on actual resource usage.
- Pro has a higher baseline and larger included usage.

Reference:

- https://railway.com/pricing
- https://docs.railway.com/pricing/plans

Estimated PoorToPour use:

| Setup | Estimated Monthly Cost |
| --- | ---: |
| Small backend + database | $5–$25 |
| Backend + worker + database | $10–$50 |

Pros:

- Developer-friendly.
- Fast deployment.
- Good for side projects.
- Usage-based pricing can stay low.

Cons:

- Usage can climb if jobs are inefficient.
- Requires monitoring resource usage.
- Less predictable than fixed VPS.

Recommendation:

> Good candidate for early hosted MVP if simplicity matters.

---

## 5.3 Render

Render supports static sites, web services, background workers, cron jobs, Postgres, and Redis-like key-value services.

Current pricing anchors:

- Hobby workspace is $0/month plus compute.
- Starter web service is listed at $7/month.
- Standard web service is listed at $25/month.
- Basic Render Postgres starts at $6/month, with a 1 GB option at $19/month.
- Cron jobs are available from $1/month, with per-minute compute pricing.

Reference:

- https://render.com/pricing

Estimated PoorToPour use:

| Setup | Estimated Monthly Cost |
| --- | ---: |
| Static frontend + starter backend + basic Postgres | $13–$30 |
| Standard backend + 1 GB Postgres | $44+ |
| Add cron/worker jobs | +$1–$20 depending on runtime |

Pros:

- Clear app hosting model.
- Native cron/background services.
- Managed Postgres available.
- Good deployment experience.

Cons:

- More expensive than bare VPS at higher tiers.
- Free Postgres has limits and time constraints.
- Multiple services can add up.

Recommendation:

> Good candidate for a more polished hosted MVP.

---

## 5.4 DigitalOcean Droplet

DigitalOcean provides simple VPS hosting.

Current pricing anchor:

- Droplets start as low as $4/month.
- Droplets include outbound transfer starting at 500 GiB/month.
- Droplets use granular billing with per-second billing and minimums.

Reference:

- https://www.digitalocean.com/pricing/droplets
- https://www.digitalocean.com/products/droplets

Estimated PoorToPour use:

| Setup | Estimated Monthly Cost |
| --- | ---: |
| Small VPS running Docker Compose | $4–$12 |
| More comfortable VPS | $12–$24 |
| Managed database added later | Additional cost |

Pros:

- Cheapest reliable hosted option.
- Predictable.
- Full control.
- Good for Docker Compose deployment.

Cons:

- More DevOps responsibility.
- Need to manage updates, backups, firewall, and deployment.
- Less convenient than platform-as-a-service.

Recommendation:

> Best low-cost option if we are comfortable with basic server operations.

---

## 5.5 Supabase

Supabase can provide managed PostgreSQL and related backend services.

Current pricing anchor:

- Free plan exists.
- Pro plan is listed at $25/month per project.
- Supabase Edge Functions charge for invocations beyond included quota.

Reference:

- https://supabase.com/pricing
- https://supabase.com/docs/guides/functions/pricing

Estimated PoorToPour use:

| Setup | Estimated Monthly Cost |
| --- | ---: |
| Free tier development database | $0 |
| Pro project | $25+ |
| Edge function overages | Usage-based |

Pros:

- Managed Postgres.
- Easy dashboard.
- Useful if we want managed auth/storage later.

Cons:

- Might be unnecessary if the backend already uses FastAPI.
- Pro tier may be overkill for personal MVP.
- Additional features can create scattered architecture.

Recommendation:

> Consider only if managed Postgres convenience is worth it. Otherwise local PostgreSQL first.

---

## 6. Market Data Cost Strategy

## 6.1 MVP Data Requirements

MVP requires:

- Symbol universe.
- Daily OHLCV data.
- Basic company profile.
- Basic earnings dates.
- Optional basic fundamentals.

MVP does not require:

- Tick data.
- Level 2 order book.
- Full real-time quotes.
- Options chains.
- Intraday full-market firehose.
- Institutional-grade historical database.

## 6.2 Recommended MVP Approach

Use provider abstraction from day one.

The code should define interfaces such as:

- `MarketDataProvider`
- `CompanyProfileProvider`
- `EarningsProvider`
- `NewsProvider`
- `FundamentalsProvider`

This lets us start cheap and swap providers later.

Recommended data strategy:

| Phase | Data Strategy |
| --- | --- |
| MVP local | Free/cheap data provider; daily bars only |
| MVP hosted | Same provider with caching and rate limits |
| Post-MVP | Evaluate paid provider for reliability |
| Paper trading | Use more reliable paid data |
| Automation | Use data provider suitable for execution-sensitive workflows |

## 6.3 Provider Notes

### Alpha Vantage

Current pricing anchor:

- Offers free stock APIs.
- Majority of endpoints can be accessed for free.
- Standard free limit is listed as 25 API requests per day.
- Premium membership exists for higher usage and premium functions.

Reference:

- https://www.alphavantage.co/
- https://www.alphavantage.co/premium/

Assessment:

| Pros | Cons |
| --- | --- |
| Easy to start | Free limit may be too low for S&P 500 scans |
| Broad asset coverage | Premium may be needed quickly |
| Good for prototypes | Rate limits require caching and batching |

Recommendation:

> Useful for experiments, but the free tier may be too constrained for scanning S&P 500 regularly.

---

### Finnhub

Current pricing anchor:

- Offers market data, company fundamentals, economic data, and alternative data.
- Pricing page lists paid stock API tiers such as Basic, Standard, and Professional.
- Some plans describe high API call limits for market data and fundamentals.

Reference:

- https://finnhub.io/
- https://finnhub.io/pricing
- https://finnhub.io/pricing-stock-api-market-data

Assessment:

| Pros | Cons |
| --- | --- |
| Broad API surface | Paid tiers may be needed |
| Market data + fundamentals | Need to verify data licensing and limits |
| Useful for MVP enrichment | Costs can rise with breadth |

Recommendation:

> Candidate for MVP+ or post-MVP if we want one provider for market data and company context.

---

### Massive / Polygon-style Market Data

Current pricing anchor:

- Offers a free basic stock API option with limited calls.
- Paid stock plans can start around low monthly tiers, depending on package.
- Real-time or advanced market data generally costs more.

Reference:

- https://massive.com/pricing
- https://massive.com/

Assessment:

| Pros | Cons |
| --- | --- |
| Good market-data developer experience | Real-time data can get expensive |
| Useful historical aggregates | Asset classes may be packaged separately |
| Stronger path for serious trading app | Might be unnecessary for MVP |

Recommendation:

> Consider after the MVP proves useful. Avoid expensive real-time plans at the beginning.

---

### Twelve Data

Current pricing anchor:

- Offers stock, forex, crypto, ETF, fundamentals, and technical indicator APIs.
- Offers free access and paid individual/business plans.
- Pricing and rate limits should be checked again before selection.

Reference:

- https://twelvedata.com/
- https://twelvedata.com/pricing
- https://twelvedata.com/stocks

Assessment:

| Pros | Cons |
| --- | --- |
| Broad coverage | Need to confirm rate limits and plan fit |
| Useful technical indicators | Provider-specific limits can shape architecture |
| Could reduce custom computation early | We still prefer computing indicators ourselves for traceability |

Recommendation:

> Candidate for provider comparison in `/docs/04-data-sources.md`.

---

### SEC EDGAR APIs

Current pricing anchor:

- SEC provides RESTful APIs for company submissions and extracted XBRL data on data.sec.gov.
- APIs return JSON formatted data.

Reference:

- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/about/developer-resources

Assessment:

| Pros | Cons |
| --- | --- |
| Official public source | Raw data requires normalization |
| Free | Not designed as a polished fundamentals API |
| Good for filings and fundamentals | Requires careful mapping and caching |

Recommendation:

> Use as a strong candidate for free company/fundamental context later, but do not let XBRL normalization delay the MVP.

---

## 7. AI Cost Strategy

## 7.1 AI Should Not Be Required for MVP

MVP candidate generation should not depend on AI.

MVP scanner logic should be deterministic:

- technical indicator calculation;
- setup rule matching;
- score calculation;
- risk/reward estimation;
- caution flags.

AI can be introduced later for:

- candidate summary generation;
- headline clustering;
- earnings-call summary;
- bull/bear research notes;
- natural-language explanations;
- code/developer assistance.

## 7.2 Current AI Pricing Anchors

Pricing changes often. These are planning anchors as of this document date.

### OpenAI

Current pricing anchors:

| Model | Input / 1M tokens | Cached Input / 1M tokens | Output / 1M tokens |
| --- | ---: | ---: | ---: |
| GPT-5.5 | $5.00 | $0.50 | $30.00 |
| GPT-5.4 | $2.50 | $0.25 | $15.00 |
| GPT-5.4 mini | $0.75 | $0.075 | $4.50 |

OpenAI web search is listed at $10 per 1,000 calls.

OpenAI Batch API can save 50% on inputs and outputs for asynchronous work.

Reference:

- https://openai.com/api/pricing/

### Anthropic

Current pricing anchors:

| Model | Input / 1M tokens | Output / 1M tokens |
| --- | ---: | ---: |
| Claude Opus 4.7 | $5.00 | $25.00 |
| Claude Sonnet 4.6 | Approximately $3.00 | Approximately $15.00 |

Anthropic pricing pages also describe web search pricing at $10 per 1,000 searches plus standard token costs.

Reference:

- https://platform.claude.com/docs/en/about-claude/pricing
- https://www.anthropic.com/claude/opus
- https://www.anthropic.com/news/claude-opus-4-7

---

## 7.3 AI Cost Formula

Use this formula for AI calls:

```text
AI cost =
  input_tokens_millions * input_price
+ cached_input_tokens_millions * cached_input_price
+ output_tokens_millions * output_price
+ tool_call_costs
```

For web search:

```text
Web search cost = number_of_search_calls * price_per_search_call
```

For OpenAI web search at $10 per 1,000 calls:

```text
price_per_search_call = $0.01
```

## 7.4 Example AI Cost Scenarios

These are rough planning scenarios. Actual costs depend on prompts, outputs, retry behavior, tools, caching, and model choice.

### Scenario A — No AI in MVP

| Item | Monthly Cost |
| --- | ---: |
| Candidate generation | $0 |
| Setup explanation from deterministic rules | $0 |
| Dashboard text | $0 |
| Total AI cost | **$0** |

Recommendation:

> This is the MVP default.

---

### Scenario B — Light AI Summaries

Assumption:

- Weekly summaries only.
- 25 candidates per week.
- Each candidate uses roughly 3,000 input tokens and 500 output tokens.
- 100 candidate summaries per month.
- Use a cheaper model.

Estimated monthly tokens:

| Token Type | Amount |
| --- | ---: |
| Input | 300,000 |
| Output | 50,000 |

Estimated monthly cost using GPT-5.4 mini:

| Token Type | Formula | Cost |
| --- | --- | ---: |
| Input | 0.3M * $0.75 | $0.23 |
| Output | 0.05M * $4.50 | $0.23 |
| Total |  | **~$0.46/month** |

This excludes web search and retries.

Recommendation:

> Cheap enough for MVP+ if summaries are generated only for top candidates and cached.

---

### Scenario C — Daily AI Summaries for Top Candidates

Assumption:

- Daily scan summaries.
- 25 candidates per trading day.
- 21 trading days/month.
- Each candidate uses roughly 3,000 input tokens and 500 output tokens.
- 525 candidate summaries/month.
- Use GPT-5.4 mini.

Estimated monthly tokens:

| Token Type | Amount |
| --- | ---: |
| Input | 1,575,000 |
| Output | 262,500 |

Estimated monthly cost using GPT-5.4 mini:

| Token Type | Formula | Cost |
| --- | --- | ---: |
| Input | 1.575M * $0.75 | $1.18 |
| Output | 0.2625M * $4.50 | $1.18 |
| Total |  | **~$2.36/month** |

This excludes web search, retries, and larger prompts.

Recommendation:

> Affordable if summaries are short, cached, and only run on top candidates.

---

### Scenario D — Expensive Agentic Research

Assumption:

- Multi-agent bull/bear/research debate.
- 25 candidates per day.
- 21 trading days/month.
- 20,000 input tokens and 4,000 output tokens per candidate.
- Use a frontier model.

Estimated monthly tokens:

| Token Type | Amount |
| --- | ---: |
| Input | 10,500,000 |
| Output | 2,100,000 |

Estimated monthly cost using GPT-5.5:

| Token Type | Formula | Cost |
| --- | --- | ---: |
| Input | 10.5M * $5.00 | $52.50 |
| Output | 2.1M * $30.00 | $63.00 |
| Total |  | **~$115.50/month** |

This excludes web search, retries, tool calls, and context expansion.

If each candidate also uses one web search call:

| Item | Formula | Cost |
| --- | --- | ---: |
| Web search | 525 calls * $0.01 | $5.25 |

Approximate total:

> **~$120.75/month before retries and provider overhead.**

Recommendation:

> Do not use this mode until deterministic scanner quality is proven.

---

## 8. AI Cost Controls

Required controls before AI features are added:

| Control | Requirement |
| --- | --- |
| Monthly AI budget | Configurable hard cap |
| Per-job budget | Each scan job has max AI spend |
| Per-candidate budget | Prevent runaway research on one ticker |
| Model tiering | Cheap model first; frontier model only on selected candidates |
| Caching | Do not regenerate summaries if source data has not changed |
| Batching | Use batch/async processing when not time-sensitive |
| Candidate limit | AI only runs on top N candidates |
| Feature toggle | AI summaries can be disabled |
| Usage logging | Store tokens, model, cost estimate, job ID |
| Alert threshold | Warn at 50%, 80%, 100% of monthly budget |
| Kill switch | Disable AI calls globally |

Recommended MVP settings:

| Setting | Default |
| --- | --- |
| AI enabled | false |
| Monthly AI budget | $0 |
| AI summaries | off |
| AI research agents | off |
| Web search by AI | off |
| Max AI candidates per scan | 0 |

Recommended MVP+ settings:

| Setting | Default |
| --- | --- |
| AI enabled | true |
| Monthly AI budget | $10 |
| Max AI candidates per scan | 5 |
| Model | Cheap/mini model |
| Cache summaries | true |
| Web search by AI | off unless explicitly enabled |

---

## 9. News, Social, Polymarket, and Political Data Costs

## 9.1 News

MVP:

- Not required.

Post-MVP:

- Start with free or low-cost headlines.
- Avoid paid full-text article ingestion at first.
- Store headline, source, timestamp, URL, ticker mapping, and catalyst label.

Cost risk:

- Paid news APIs can become expensive.
- Full article processing increases AI token costs.
- Licensing matters if redisplaying content.

Recommendation:

> Start with headlines only. Do not summarize full articles until provider rights and costs are clear.

---

## 9.2 Social Media

MVP:

- Not required.

Post-MVP:

- Start with limited sources.
- Track mention counts and simple velocity.
- Avoid full social firehose ingestion.

Cost risk:

- APIs can be expensive or restricted.
- Social data is noisy.
- AI sentiment processing can multiply token costs.

Recommendation:

> Add only after technical scanner and dashboard are useful.

---

## 9.3 Polymarket / Prediction Markets

MVP:

- Not required.

Post-MVP:

- Treat as event-risk context.
- Do not treat market probabilities as direct stock signals.

Cost risk:

- API cost may be low, but mapping events to stocks is noisy.
- AI event interpretation can add token costs.

Recommendation:

> Add only as contextual event cards, not trade triggers.

---

## 9.4 Politician Trade Records

MVP:

- Not required.

Post-MVP:

- Use as delayed context only.
- Show transaction date, disclosure date, ticker, transaction type, and value range.

Cost risk:

- Usually not expensive, but signal value is limited by reporting delays.
- Processing and cleaning data may cost developer time.

Recommendation:

> Add later as context, not intraday trading signal.

---

## 10. Storage and Database Cost Controls

MVP storage should be modest.

Data to store:

- Symbol universe.
- Daily OHLCV bars.
- Technical indicators.
- Scan runs.
- Scan candidates.
- Company profiles.
- Earnings context.
- Basic job logs.

Avoid storing in MVP:

- Tick data.
- Full article bodies.
- Full social-media firehose.
- High-frequency intraday bars for all symbols.
- Large unbounded AI transcripts.

Storage rules:

| Rule | Reason |
| --- | --- |
| Keep raw provider responses only when useful | Avoid database bloat |
| Compress or discard large JSON payloads | Control storage growth |
| Store normalized data for querying | Keep dashboard fast |
| Set retention policies for logs | Avoid unbounded growth |
| Separate cache from source-of-truth tables | Easier cleanup |

Recommended MVP retention:

| Data Type | Retention |
| --- | --- |
| Daily OHLCV | Indefinite for selected universe |
| Technical indicators | Recomputable; store if useful for performance |
| Scan runs | Indefinite initially |
| Job logs | 30–90 days |
| AI summaries | Until source data changes or 90 days |
| Provider raw payloads | 7–30 days, if stored at all |

---

## 11. Job Scheduling Cost Controls

MVP jobs:

| Job | Frequency | Cost Control |
| --- | --- | --- |
| Daily scan | Once after market close | Batch all symbols |
| Weekly scan | Once per week | Reuse daily data |
| Company profile refresh | Weekly or monthly | Cache aggressively |
| Earnings refresh | Daily during earnings season, otherwise weekly | Fetch only needed universe |
| Manual scan | User-triggered | Require confirmation if expensive |
| AI summary job | Off in MVP | Top N candidates only later |

Rules:

- Jobs must record start time, end time, status, symbols processed, provider calls, AI tokens, and estimated cost.
- Jobs should stop if cost or provider call limits are exceeded.
- Jobs should fail safely if data is stale or unavailable.
- Jobs should support dry-run mode.

MVP+ and post-MVP job ideas from external product review:

- alert engine after scanner quality is proven;
- daily/weekly scan briefing email after scan output is stable;
- AI candidate insight job only for top candidates, with caps and caching;
- durable job/event system only if APScheduler becomes insufficient.

These should not increase MVP job scope.

---

## 12. Monitoring and Alerts

MVP monitoring can be simple:

- Application logs.
- Job run history.
- Error table.
- Provider call counts.
- Estimated monthly cost table.

Post-MVP monitoring:

- Error alerts.
- Budget alerts.
- Provider outage alerts.
- Job failure notifications.
- Uptime monitoring.
- Database backup status.

Recommended MVP dashboard card:

| Metric | Purpose |
| --- | --- |
| Month-to-date estimated cost | Budget visibility |
| Provider calls today | Rate-limit visibility |
| AI tokens this month | AI budget visibility |
| Failed jobs | Reliability |
| Last successful scan | Freshness |
| Stale data warnings | Trading safety |

---

## 13. Security and Operations

Cost and security are connected.

Rules:

- Never commit API keys.
- Store secrets in environment variables or managed secret storage.
- Separate local, staging, and production credentials.
- Use read-only provider keys where possible.
- Do not expose provider keys to the frontend.
- Do not log secrets.
- Rotate keys if exposed.
- Back up the database before major schema migrations.
- Use HTTPS for hosted dashboard.
- Restrict dashboard access if hosted publicly.

Broker-related rules:

- No broker credentials in MVP.
- No broker API integration before paper trading requirements are documented.
- No live trading without kill switch and audit logs.

---

## 14. Cost Dashboard Requirements

Post-MVP, PoorToPour should include a simple cost visibility panel.

Suggested fields:

| Field | Description |
| --- | --- |
| Current month estimated total | Sum of provider, hosting, and AI estimates |
| Monthly budget | Configured budget |
| Budget used % | Current usage ratio |
| AI cost month-to-date | Estimated model/tool spend |
| Market data calls | Provider API calls |
| Most expensive job | Highest estimated job cost |
| Failed/retried calls | Retry cost risk |
| Upcoming paid services | Services enabled but not yet active |

MVP requirement:

- Track job counts and provider call counts in backend logs/tables.
- Full cost dashboard can wait until MVP+.

---

## 15. Recommended Cost-Control Roadmap

| Phase | Cost Strategy |
| --- | --- |
| Phase 0 | No recurring cost required |
| Phase 1 | Local Docker Compose; free/cheap data only |
| Phase 2 | Deterministic scanner; no AI required |
| Phase 3 | Optional low-cost hosting; dashboard only |
| Phase 4 | Add company/earnings context with cached provider calls |
| Phase 5 | Add backtesting; avoid expensive intraday data |
| Phase 6 | Add limited intraday intelligence with strict provider limits |
| Phase 7 | Add paper trading; improve monitoring |
| Phase 8 | Consider broker integration only with strict risk controls |
| Phase 9 | Expand AI and automation only after measured value |

---

## 16. Recommended MVP Cost Stack

Preferred MVP stack:

| Category | Recommendation |
| --- | --- |
| Development | Local Docker Compose |
| Backend | FastAPI local container |
| Frontend | React local dev server; static build later |
| Database | Local PostgreSQL |
| Market data | Free/cheap daily OHLCV provider with abstraction |
| Fundamentals | Start minimal; SEC EDGAR later if needed |
| AI | Off |
| Hosting | None until scanner is useful |
| Monitoring | Local logs + job history table |

Estimated MVP cost:

| Item | Monthly Cost |
| --- | ---: |
| Local hosting | $0 |
| Local database | $0 |
| AI | $0 |
| Market data | $0–$30 |
| Domain | Optional |
| Total | **$0–$30/month** |

Recommended next hosted stack:

| Category | Option |
| --- | --- |
| Cheapest hosted | DigitalOcean Droplet + Docker Compose |
| Easiest hosted | Railway or Render |
| Managed database | Render Postgres or Supabase only if convenience is worth cost |
| AI summaries | GPT-5.4 mini or equivalent cheap model, capped at $10/month |

Estimated hosted MVP cost:

| Item | Monthly Cost |
| --- | ---: |
| App hosting | $5–$25 |
| Database | $0–$25 |
| Market data | $0–$50 |
| AI | $0–$10 |
| Total | **$5–$110/month** |

Recommended ceiling:

> Keep hosted MVP under **$50/month** if possible. Accept up to **$100/month** only if the scanner is clearly useful.

---

## 17. Open Questions

| ID | Question | Default / Current Leaning | Status |
| --- | --- | --- | --- |
| Q-COST-001 | What is Jesse's preferred monthly MVP budget ceiling? | $50/month | Open |
| Q-COST-002 | Should the first hosted version use Railway, Render, or DigitalOcean? | Local first; decide later | Open |
| Q-COST-003 | Which market data provider should be used first? | TBD in `/docs/04-data-sources.md` | Open |
| Q-COST-004 | Should AI summaries be added in MVP+? | Yes, only if capped and cached | Open |
| Q-COST-005 | Should the dashboard include cost visibility in MVP? | Basic backend logging only | Open |
| Q-COST-006 | Should we pay for market data before the scanner proves useful? | No | Open |
| Q-COST-007 | What is the maximum acceptable AI budget before paper trading? | $10–$25/month | Open |
| Q-COST-008 | Should we use official SEC data for fundamentals? | Likely yes later | Open |

---

## 18. Initial Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| COST-D-001 | MVP should run locally first | Avoid recurring cost before product value is proven |
| COST-D-002 | MVP should not require AI | Deterministic scanner should be useful on its own |
| COST-D-003 | MVP should avoid premium market data | Daily/weekly scanner can start with cheaper data |
| COST-D-004 | Hosted MVP should aim to stay under $50/month | Keeps project sustainable |
| COST-D-005 | AI must have budget caps before use | Prevents runaway agent costs |
| COST-D-006 | Intraday intelligence is post-MVP | Reduces data and compute cost |
| COST-D-007 | Cost visibility should become a dashboard feature later | Helps prevent silent cost creep |

---

## 19. Source Notes

Pricing and provider details change often. Before committing to a provider, re-check the current official pricing pages.

Initial references used for this draft:

- OpenAI API pricing: https://openai.com/api/pricing/
- Anthropic Claude pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Claude Opus 4.7 pricing note: https://www.anthropic.com/news/claude-opus-4-7
- Railway pricing: https://railway.com/pricing
- Railway pricing docs: https://docs.railway.com/pricing/plans
- Render pricing: https://render.com/pricing
- DigitalOcean Droplet pricing: https://www.digitalocean.com/pricing/droplets
- DigitalOcean Droplets product page: https://www.digitalocean.com/products/droplets
- Supabase pricing: https://supabase.com/pricing
- Supabase Edge Functions pricing: https://supabase.com/docs/guides/functions/pricing
- Alpha Vantage: https://www.alphavantage.co/
- Alpha Vantage Premium: https://www.alphavantage.co/premium/
- Finnhub pricing: https://finnhub.io/pricing
- Finnhub stock API pricing: https://finnhub.io/pricing-stock-api-market-data
- Massive pricing: https://massive.com/pricing
- Twelve Data pricing: https://twelvedata.com/pricing
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC Developer Resources: https://www.sec.gov/about/developer-resources

---

## 20. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-05-14 | v0.2 | Added post-MVP job and briefing ideas from external review without expanding MVP costs | Jesse + AI |
| 2026-04-30 | v0.1 | Created initial cost and operations document | Jesse + AI |
