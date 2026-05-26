# PoorToPour Session Handoff to Codex

**Project:** PoorToPour  
**Description:** From broke to pouring champagne.  
**Document:** `/docs/99-session-handoff-to-codex.md`  
**Date created:** 2026-05-14  
**Status:** Temporary handoff document  
**Audience:** IDE Codex / local development assistant

---

## 1. Purpose

This document summarizes the latest planning decisions and follow-up changes discussed outside the local IDE session.

Use this file as a context bridge for Codex so it can update the local repository documents without needing the full chat history.

This is a temporary coordination document. Once the relevant updates are applied to the main docs, this file can either remain as a session note or be archived.

---

## 2. Important Instruction for Codex

Do **not** expand the MVP just because new good ideas were found.

The user explicitly wants to avoid MVP scope drift.

The current MVP remains focused on:

```text
scan -> rank -> inspect -> learn
```

The MVP should continue to prioritize:

- local-first development;
- daily/weekly swing-trade scanner;
- S&P 500 first;
- long-only setups;
- deterministic rules;
- explainable candidate scoring;
- chart evidence;
- risk/reward research estimates;
- caution flags;
- scan history;
- Tier 1 provider-backed data only;
- no broker automation;
- no AI-generated trade decisions.

---

## 3. Latest External References Reviewed

Two external projects/screenshots were reviewed for inspiration.

### 3.1 OpenStock

Repository reviewed:

```text
https://github.com/Open-Dev-Society/OpenStock
```

Summary:

OpenStock appears to be a broad open-source market portal similar to a lightweight TradingView/Yahoo Finance style product.

It focuses on:

- stock search;
- watchlists;
- alerts;
- stock detail pages;
- TradingView widgets;
- market overview;
- news/AI email workflows;
- authentication;
- public-user product polish.

Useful lessons for PoorToPour:

- polished UI component discipline;
- command palette / global search;
- watchlist and alerts as later product features;
- scheduled workflow mindset;
- good README and environment documentation;
- clear non-broker / non-financial-advice boundary.

Do **not** copy OpenStock code.

Reason:

- OpenStock is AGPL-3.0 licensed.
- Use it for inspiration only.
- Do not import or directly copy implementation.

PoorToPour should not use OpenStock as a data source.

Reason:

- OpenStock is an app, not a market-data provider.
- It depends on Finnhub and TradingView widgets.
- It does not solve PoorToPour's provider constraints.

### 3.2 Spring Duck / 春江鴨

Screenshots reviewed from Threads.

Summary:

Spring Duck appears closer to PoorToPour's product direction than OpenStock.

It looks like:

```text
technical signal scanner + annotated chart dashboard + AI insight layer
```

Visible ideas from screenshots:

- candlestick chart with signal markers;
- moving averages;
- volume bars;
- detected signals panel;
- market signal cards;
- sector/theme scanner grid;
- scanner-aware watchlist;
- ticker chips/search;
- AI insight panel;
- tabs such as Overview, Scanner, Tasks.

Useful ideas:

- chart signal markers;
- structured detected-signal cards;
- sector/theme scanner grid;
- scanner-aware watchlist;
- AI insight panel after deterministic scanner exists;
- visual signal taxonomy.

Important constraint:

These should **not** be added to MVP unless already aligned with existing MVP scope or trivial.

Most of these belong to MVP+ or final vision.

---

## 4. Decisions to Apply to Main Docs

## 4.1 Keep MVP Scope Stable

Decision:

```text
Do not add new MVP features based only on external project inspiration.
```

Rationale:

External references are useful, but adding every attractive feature would create endless MVP drift.

Apply this to:

- `/docs/00-project-plan.md`
- `/docs/01-product-requirements.md`
- `/docs/05-dashboard-design.md`
- `/docs/08-execution-tracker.md`
- `/docs/09-decision-log.md`

Suggested decision-log entry:

```md
| D-056 | 2026-05-14 | Accepted | Keep external-project inspiration out of MVP unless it supports the existing scan-rank-inspect-learn flow | Prevents MVP scope drift after reviewing OpenStock and Spring Duck references | Some attractive features are delayed | Preserves Phase 1 focus on data foundation and core scanner |
```

---

## 4.2 Add OpenStock-Inspired Ideas to MVP+ / Later Roadmap

Potential additions to MVP+ / later:

| Feature | Suggested Phase | Reason |
| --- | --- | --- |
| Command palette / global ticker search | MVP+ | Useful navigation and search workflow |
| Scanner-aware watchlist | MVP+ | More useful than generic ticker list |
| External TradingView chart link | MVP or MVP+ | Low-cost manual research helper |
| Market regime panel | MVP+ | Adds SPY/QQQ/sector context |
| Alert engine | Post-MVP | Useful after scanner quality is proven |
| Daily/weekly scan briefing email | Post-MVP | Useful after scanner output is stable |
| Durable job/event system | Post-MVP | Useful when APScheduler becomes insufficient |

Apply to:

- `/docs/01-product-requirements.md`
- `/docs/03-technical-architecture.md`
- `/docs/05-dashboard-design.md`
- `/docs/07-cost-and-operations.md`
- `/docs/09-decision-log.md`

Do not add these as required MVP items.

---

## 4.3 Add Spring Duck-Inspired Ideas to MVP+ / Final Vision

Potential additions to MVP+ / later:

| Feature | Suggested Phase | Reason |
| --- | --- | --- |
| Chart signal markers | MVP preferred if simple, otherwise MVP+ | Makes setup evidence visual |
| Detected Signals panel | MVP+ | More structured than plain text explanations |
| Signal taxonomy expansion | MVP+ / later | Supports richer pattern detection |
| Sector/theme scanner grid | MVP+ / later | Helps identify where market strength is concentrated |
| Scanner-aware watchlist | MVP+ | Tracks tickers with source scan and recent signal |
| AI candidate insight panel | MVP+ / later | AI explains scanner output after deterministic rules exist |
| VCP pattern detection | Later | Needs formal rule definition and validation |
| Adam & Eve pattern detection | Later | Pattern is subjective and needs careful testing |
| Divergence detection | Later | Useful but easy to overfit |
| Real-time signal detection | Later | Requires intraday data and higher cost |

Apply to:

- `/docs/00-project-plan.md`
- `/docs/01-product-requirements.md`
- `/docs/02-trading-strategy-requirements.md`
- `/docs/03-technical-architecture.md`
- `/docs/05-dashboard-design.md`
- `/docs/06-risk-and-backtesting.md`
- `/docs/09-decision-log.md`

Do not add these as required MVP items.

---

## 5. Suggested Main Doc Updates

## 5.1 `/docs/00-project-plan.md`

Add a short subsection under roadmap or post-MVP phases:

```md
### External Inspiration Parking Lot

Ideas observed from OpenStock and Spring Duck are parked for MVP+ or later unless they directly support the existing MVP flow.

Potential future additions:

- command palette / global ticker search;
- scanner-aware watchlist;
- chart signal markers;
- detected-signal cards;
- sector/theme scanner grid;
- market regime panel;
- alert engine;
- daily/weekly scan briefing;
- AI candidate insight panel;
- richer chart pattern detection such as VCP or Adam & Eve patterns.

These ideas must not expand the MVP unless explicitly re-approved.
```

---

## 5.2 `/docs/01-product-requirements.md`

Add to MVP+ or future product phasing:

```md
### MVP+ Candidate Features from External Review

- Command palette / global ticker search.
- Scanner-aware watchlist.
- External TradingView chart link.
- Chart signal markers.
- Detected Signals panel.
- Sector/theme scanner grid.
- Market regime panel.

These are not required for MVP.
```

---

## 5.3 `/docs/02-trading-strategy-requirements.md`

Add to future setup expansion:

```md
### Future Signal Taxonomy

Future versions may expand beyond the first three MVP setup families into a structured signal taxonomy:

- trend signals;
- breakout signals;
- pullback/support signals;
- volume confirmation signals;
- pattern signals;
- caution/divergence signals;
- risk-quality signals.

Examples to evaluate later:

- volume breakout;
- resistance breakout;
- support breakdown;
- VCP pattern;
- Adam & Eve bottom/top;
- bearish divergence;
- bullish/bearish trend markers.

Each future signal must have deterministic rules, test fixtures, and validation before being trusted.
```

---

## 5.4 `/docs/03-technical-architecture.md`

Add to future architecture path:

```md
### Future Job System Upgrade

APScheduler remains the MVP scheduler.

If PoorToPour adds alerts, AI summaries, paper-trading checks, scan briefings, or more frequent provider refreshes, migrate to a more durable job system such as Celery + Redis, RQ + Redis, Temporal, or another workflow engine.

The upgrade should happen only when APScheduler becomes a real limitation.
```

Add to UI/frontend architecture:

```md
### Future Command Palette

MVP+ may include a command palette for:

- ticker search;
- opening candidate details;
- navigating to scans/settings;
- opening manual scan modal;
- jumping to watchlist items.

This is a UX enhancement, not an MVP dependency.
```

---

## 5.5 `/docs/05-dashboard-design.md`

Add to MVP+ features:

```md
### External-Inspired MVP+ UI Ideas

From OpenStock-style product references:

- command palette / global search;
- scanner-aware watchlist;
- external TradingView chart link;
- market regime panel.

From Spring Duck-style signal dashboard references:

- chart signal markers;
- detected-signal cards;
- sector/theme scanner grid;
- AI candidate insight panel after deterministic scanner output exists.

These are visual/product references only and should not expand MVP scope.
```

Add to Candidate Detail future section:

```md
### Future Chart Signal Markers

Candidate Detail may eventually show signal markers directly on the chart, such as:

- breakout level;
- volume breakout;
- pullback support;
- trend warning;
- invalidation marker;
- caution marker.

Each marker must be generated from structured rule output.
```

---

## 5.6 `/docs/06-risk-and-backtesting.md`

Add to future signal expansion / validation:

```md
### Validation Requirement for Future Pattern Signals

Future pattern signals such as VCP, Adam & Eve, or divergence must not be trusted based on visual appeal alone.

Before promotion into scanner scoring, each signal requires:

- deterministic definition;
- test fixtures;
- false-positive review;
- historical backtesting;
- forward testing or manual review;
- documented caution flags;
- clear explanation output.
```

---

## 5.7 `/docs/08-execution-tracker.md`

Current tracker should remain mostly unchanged.

Optional addition only if desired:

```md
| P1-009 | Review external inspiration parking lot before MVP+ planning | ⬜ | Jesse + AI | OpenStock and Spring Duck ideas are parked, not MVP scope |
```

Recommended:

Do not add this unless the user wants it tracked as an active task.

---

## 5.8 `/docs/09-decision-log.md`

Add decisions:

```md
| D-056 | 2026-05-14 | Accepted | Keep external-project inspiration out of MVP unless it supports the existing scan-rank-inspect-learn flow | Prevents MVP scope drift after reviewing OpenStock and Spring Duck references | Some attractive features are delayed | Preserves Phase 1 focus on data foundation and core scanner |
| D-057 | 2026-05-14 | Accepted | Add OpenStock-inspired ideas such as command palette, scanner-aware watchlist, alerts, and scan briefings to MVP+ or later roadmap | These are useful product patterns but not required for MVP scanner validation | Delays convenience features | Keeps MVP focused while preserving good ideas |
| D-058 | 2026-05-14 | Accepted | Add Spring Duck-inspired ideas such as chart signal markers, detected-signal cards, sector scanner grid, and AI insight panel to MVP+ or later roadmap | These strengthen the future signal UX but could create scope drift if added now | Delays visually attractive features | Preserves MVP simplicity while improving final vision |
| D-059 | 2026-05-14 | Accepted | Future pattern signals require deterministic rules and validation before entering scoring | Visual chart patterns can be subjective and overfit-prone | Slower feature expansion | Protects scanner credibility and backtesting quality |
```

---

## 6. Recommended Codex Task Prompt

Use this prompt in the IDE Codex session:

```text
You are working in the PoorToPour repository.

Read `/docs/99-session-handoff-to-codex.md` first. Then update the existing project documents according to the handoff instructions.

Important constraints:
- Do not expand the MVP scope.
- Keep MVP focused on scan -> rank -> inspect -> learn.
- Add OpenStock and Spring Duck ideas only to MVP+, post-MVP, final vision, or external inspiration sections.
- Update `/docs/09-decision-log.md` with the new decisions.
- Update `/docs/00-project-plan.md`, `/docs/01-product-requirements.md`, `/docs/02-trading-strategy-requirements.md`, `/docs/03-technical-architecture.md`, `/docs/05-dashboard-design.md`, and `/docs/06-risk-and-backtesting.md` where relevant.
- Do not update `/docs/08-execution-tracker.md` unless you add an optional parking-lot review task.
- Preserve existing tone and formatting.
- Do not copy code or text from OpenStock. Treat it as inspiration only.
- Keep all additions concise and clearly marked as MVP+ or later unless already part of the existing MVP.

After making changes, summarize:
1. files changed;
2. key additions;
3. anything intentionally not changed;
4. any questions or risks.
```

---

## 7. Expected Outcome

After Codex applies this handoff, the repo should clearly reflect that:

- external projects were reviewed;
- useful ideas were captured;
- MVP scope did not expand;
- OpenStock is treated as a product/UX reference only;
- Spring Duck is treated as a signal-UX reference only;
- chart markers, detected-signal cards, command palette, sector grid, and richer pattern detection are parked for MVP+ or later;
- future pattern signals require deterministic definitions and validation.

---

## 8. Change Log

| Date | Version | Update | Author |
| --- | --- | --- | --- |
| 2026-05-14 | v0.1 | Created IDE Codex handoff for external-reference updates | Jesse + AI |
