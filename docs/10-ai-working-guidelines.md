# PoorToPour AI Working Guidelines

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Date created:** 2026-04-29  
**Last updated:** 2026-04-29

---

## 1. Purpose

This document defines how AI assistance should work on the PoorToPour project.

Future AI sessions should read this file before proposing architecture, writing code, changing documentation, or making trading-system recommendations.

The goal is to keep the project consistent, traceable, practical, and safe as it evolves from a personal research dashboard into a possible automated trading system.

---

## 2. Project Context

PoorToPour is a personal trading research and automation project.

The long-term vision is to build a system that can:

1. Scan U.S. equities for tradeable setups.
2. Rank and explain trade candidates.
3. Display evidence on a professional dashboard.
4. Add company, earnings, news, social, prediction-market, and political-trade context over time.
5. Validate strategies through backtesting and paper trading.
6. Eventually support controlled broker automation with strict risk controls.

The MVP is intentionally smaller:

- S&P 500 universe by default.
- Long-only.
- Daily and weekly swing-trade scans.
- Deterministic technical setup detection.
- Dashboard with charts, scores, and risk/reward context.
- No automated trading.
- No AI-generated trade decisions.

---

## 3. Required Documentation to Check First

Before meaningful work, review the relevant docs:

| File | Purpose |
| --- | --- |
| `/docs/00-project-plan.md` | Project vision, MVP boundary, roadmap |
| `/docs/08-execution-tracker-v1.0.md` | Current work status and active tasks |
| `/docs/09-decision-log.md` | Accepted project decisions |
| `/docs/10-ai-working-guidelines.md` | AI workflow and engineering rules |

When available, also check:

| File | Purpose |
| --- | --- |
| `/docs/01-product-requirements.md` | Product behavior and user workflows |
| `/docs/02-trading-strategy-requirements.md` | Indicators, setups, scoring rules |
| `/docs/03-technical-architecture.md` | Stack, modules, services, data flow |
| `/docs/04-data-sources.md` | Data vendors, source limits, freshness |
| `/docs/05-dashboard-design.md` | UI/UX expectations |
| `/docs/06-risk-and-backtesting.md` | Risk controls and validation methods |

---

## 4. AI Workflow for New Work Items

For any meaningful feature, bug, refactor, or design task, follow this process.

### Step 1: Understand the Work

Clarify:

- What problem are we solving?
- Which phase does this belong to?
- Which docs or decisions already constrain this work?
- Is this MVP scope or post-MVP scope?
- Is this research-only, dashboard-only, backend-only, or trading-risk-sensitive?

Do not jump into code before the approach is discussed.

### Step 2: Propose the Approach

Before coding, provide:

- Recommended approach.
- Rationale.
- Pros and cons.
- Scope boundaries.
- Risks.
- Files likely to be touched.
- Tests to add or update.

For larger multi-module work, create or update a Markdown implementation plan before coding.

### Step 3: Implement in Small Safe Steps

When implementation begins:

- Keep changes focused.
- Avoid unrelated refactors.
- Follow existing project patterns.
- Prefer simple designs over clever abstractions.
- Add tests close to the logic being changed.
- Keep commits or change sets small when possible.

### Step 4: Review the Change

Before considering work complete, perform:

- Code review.
- Security review.
- Trading safety review.
- Test review.
- Documentation update review.

### Step 5: Update Project Tracking

After meaningful progress:

- Update `/docs/08-execution-tracker-v1.0.md`.
- Add important decisions to `/docs/09-decision-log.md`.
- Update any affected specification docs.
- Record unresolved questions and risks.

---

## 5. Engineering Principles

### 5.1 Core Principles

- Prefer maintainable code over clever code.
- Keep solutions simple, readable, and easy to change.
- Respect separation of concerns.
- Avoid duplication.
- Do not reinvent the wheel when an existing library, project pattern, or shared utility solves the problem.
- Analyze requirements before coding.
- Keep scope tight to the current work item.
- Avoid unrelated reformatting or drive-by refactors.

### 5.2 Separation of Concerns

Put code in the right place.

Suggested boundaries:

| Layer | Responsibility |
| --- | --- |
| Frontend component | View rendering and user interaction |
| Frontend hook/service | Client-side orchestration and API calls |
| Backend API route | HTTP boundary and request/response handling |
| Service | Business or domain logic |
| Repository/connector | Data access and external integration |
| Model/schema | Data representation and validation |
| Mapper | Transformation between external and internal models |
| Job/worker | Scheduled or background processing |
| Strategy module | Trading setup detection and scoring logic |

### 5.3 SOLID, DRY, and KISS

Apply SOLID pragmatically.

- One module should have one clear reason to change.
- Prefer small targeted interfaces over giant catch-all contracts.
- Depend on abstractions where it improves maintainability.
- Centralize repeated logic.
- Do not over-engineer speculative future flexibility.

### 5.4 Defensive Programming

- Validate inputs early.
- Fail loudly for invalid internal assumptions.
- Handle external data quality issues gracefully.
- Do not partially mutate state and then fail midway.
- Treat third-party data as unreliable until validated.
- Always label stale or delayed data clearly.

### 5.5 Naming

- Use clear descriptive names.
- Avoid unexplained abbreviations.
- Use consistent financial and technical terms.
- Boolean names should generally start with `is`, `has`, `can`, or `should`.
- File names should use `kebab-case`.

### 5.6 Function Design

- Keep functions focused.
- Separate validation, transformation, side effects, and formatting when practical.
- Avoid giant functions.
- Prefer guard clauses and early returns over deep nesting.
- Avoid hidden side effects.
- Do not mutate input parameters unless clearly intentional and documented.

### 5.7 Comments

Use comments sparingly.

Prefer self-documenting code through naming and structure.

When comments are helpful, keep them short. For this project, include concise English comments where useful, especially around non-obvious trading logic, data assumptions, or risk controls.

Example style:

```python
# EN: Guard against stale market data before scoring.
```

---

## 6. Trading-System Safety Rules

PoorToPour is not just a normal dashboard. It may eventually influence real trades.

Any feature that affects signals, scoring, risk, alerts, paper trades, or live execution must be treated as trading-risk-sensitive.

### 6.1 Required Safety Questions

Ask:

- Could this feature create misleading trade signals?
- Could stale data be mistaken as fresh data?
- Could a calculation bug affect risk sizing?
- Could this produce false confidence?
- Could this hide downside risk?
- Could this break backtesting validity?
- Could this become dangerous if broker automation is added later?
- Does the dashboard clearly distinguish evidence from opinion?
- Are source timestamps visible?
- Are assumptions documented?

### 6.2 No Black-Box Trade Decisions in MVP

The MVP must use deterministic, explainable rules.

AI may assist with:

- Documentation.
- Code generation.
- Summaries.
- Research explanation.
- Developer productivity.

AI must not be the source of final trade decisions in MVP.

### 6.3 Data Freshness

Every important market or context record should eventually expose:

- Source.
- Retrieved timestamp.
- Market timestamp.
- Freshness/staleness status.
- Provider limitations.

### 6.4 Risk Controls Before Automation

Broker automation must not be added until the system has:

- Historical backtesting.
- Paper trading.
- Risk limits.
- Kill switch.
- Position sizing controls.
- Trade logs.
- Error handling.
- Manual override path.
- Clear audit trail.

---

## 7. Testing Expectations

### 7.1 General Testing

Prefer tests early for:

- Indicator calculations.
- Strategy rule logic.
- Risk/reward calculations.
- Position sizing.
- Data normalization.
- Backtesting logic.
- API contracts.
- Dashboard rendering of critical values.

### 7.2 Test Style

- Test names should describe behavior.
- Prefer arrange / act / assert.
- Keep each test focused on one behavior.
- Use deterministic fixtures.
- Avoid tests that depend on live external market data.
- Mock third-party providers.

### 7.3 Financial Calculation Tests

For financial and trading calculations:

- Include known input/output fixtures.
- Test edge cases.
- Test missing data.
- Test stale data.
- Test zero volume, zero price, and division-by-zero cases.
- Test rounding behavior where relevant.
- Compare selected indicators against trusted reference calculations.

---

## 8. Security Expectations

Review security risks for features involving:

- API keys.
- External providers.
- User configuration.
- Broker credentials.
- Webhooks.
- Scheduled jobs.
- File exports.
- Authentication, if added later.

Rules:

- Never commit secrets.
- Use environment variables or secret managers.
- Do not expose provider keys to the frontend.
- Validate and sanitize external data.
- Avoid logging secrets or sensitive account details.
- Treat future broker integration as high-risk.

---

## 9. Documentation Rules

### 9.1 Keep Docs Current

When work changes project direction, update the relevant doc.

Examples:

| Change | Update |
| --- | --- |
| New major decision | `/docs/09-decision-log.md` |
| Phase/task progress | `/docs/08-execution-tracker-v1.0.md` |
| Product behavior | `/docs/01-product-requirements.md` |
| Trading logic | `/docs/02-trading-strategy-requirements.md` |
| Architecture | `/docs/03-technical-architecture.md` |
| Data provider choice | `/docs/04-data-sources.md` |
| Dashboard behavior | `/docs/05-dashboard-design.md` |
| Risk/backtesting logic | `/docs/06-risk-and-backtesting.md` |

### 9.2 Avoid Documentation Drift

If the implementation differs from the documentation:

1. Call out the mismatch.
2. Recommend which side should change.
3. Update the affected doc after the decision is made.

---

## 10. Execution Tracker Rules

Use `/docs/08-execution-tracker-v1.0.md` as the living project status board.

Update it when:

- A task starts.
- A task completes.
- A task becomes blocked.
- A risk is discovered or closed.
- A decision affects active work.
- The current focus changes.

Do not update it for every tiny code edit. Keep it useful, not noisy.

---

## 11. Decision Log Rules

Use `/docs/09-decision-log.md` for durable decisions.

Add entries for:

- Stack choices.
- Data provider choices.
- Trading strategy choices.
- Risk policy choices.
- Scope changes.
- MVP boundary changes.
- Architecture changes.
- Automation-readiness criteria.

Each decision should include:

- Date.
- Status.
- Decision.
- Reason.
- Trade-off.
- Impact.

---

## 12. Pull Request / Change Summary Expectations

When preparing a PR or change summary, include:

- What changed.
- Why it changed.
- Scope in.
- Scope out.
- Tests run.
- Risks.
- Follow-ups.
- Screenshots, if UI changed.

Write implementation notes from the reviewer's perspective:

- Behavior-level changes first.
- File references second.
- Explain non-obvious choices.
- Avoid noisy file-by-file narration.

---

## 13. Preferred MVP Stack

Current accepted defaults:

| Layer | Choice |
| --- | --- |
| Frontend | React + TypeScript |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| Local deployment | Docker Compose |
| Data analysis | pandas / numpy |
| Charting | TradingView Lightweight Charts or similar |
| Scheduling | APScheduler initially |
| Later queue | Celery + Redis if needed |

Do not treat these as permanent if better evidence appears, but record any changes in the decision log.

---

## 14. Scope Discipline

Default rule:

Build the smallest correct version that moves PoorToPour toward the next project milestone.

Avoid:

- Full autonomous trading before validation.
- Complex AI agents before deterministic scanner reliability.
- Intraday firehose ingestion before daily scans work.
- Options strategy generation before equity scanner maturity.
- Premature SaaS/multi-user architecture.
- Broad refactors unrelated to the task.
- Fancy abstractions for future features that do not exist yet.

---

## 15. Current MVP Boundary

Current MVP:

- Local-first dashboard.
- S&P 500 by default.
- Long-only.
- Daily and weekly swing scans.
- Technical setup detection.
- Basic company and earnings context.
- Ranked candidates.
- Explainable score breakdown.
- Chart evidence.
- Basic risk/reward view.
- Historical scan storage.

Not MVP:

- Live broker execution.
- Full intraday day-trading engine.
- Options.
- Short selling.
- Social-media firehose.
- Political-trade-based live signals.
- AI-driven trading decisions.
- Multi-user SaaS.
- Mobile app.

---

## 16. Future AI Session Startup Checklist

At the start of a new meaningful PoorToPour session, AI should:

1. Identify the user's requested task.
2. Check the relevant docs.
3. Check `/docs/08-execution-tracker-v1.0.md` for current status.
4. Check `/docs/09-decision-log.md` for accepted decisions.
5. Confirm whether the work is MVP or post-MVP.
6. Propose an approach before coding.
7. Explain trade-offs.
8. Recommend a preferred option.
9. Update docs after meaningful progress.

---

## 17. Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-04-29 | Created initial AI working guidelines from project discussion and reusable engineering/workflow patterns | Jesse + AI |
