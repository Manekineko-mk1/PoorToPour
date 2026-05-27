# Phase 2 Implementation Plan: Technical Scanner

**Project:** PoorToPour
**Phase:** Phase 2 - Technical Scanner MVP
**Status:** 🟨 Active
**Branch:** `feature/phase_2_technical_scanner`
**Last updated:** 2026-05-27

---

## 1. Purpose

This plan breaks Phase 2 into small implementation steps.

The goal is to expand the Phase 1 bootstrap scanner into a deterministic technical scanner with explainable setup detection, scoring, caution flags, risk/reward estimates, persisted output, and a small frontend inspection path.

This plan preserves MVP scope:

- no broker automation;
- no AI trade decisions;
- no intraday scanner;
- no full backtesting UI;
- no full dashboard redesign;
- no notification-based alerts.

---

## 2. Implementation Sequence

### Step 1: Phase 2 Scope And Data Inputs

Outcome:

- Phase 2 tracker and implementation plan are current.
- Scanner setup families and first implementation order are explicit.
- Alpha Vantage and Nasdaq 100 are captured as supporting work, not scope expansion.

Tasks:

- Confirm breakout as the first setup detector.
- Keep pullback continuation and relative strength leader as follow-on detectors.
- Define the minimum indicator/input set needed by all three detectors.
- Confirm candidate payload shape for reasons, warnings, score breakdown, and risk/reward fields.

Exit criteria:

- `P2-A` is marked `✅ Done`.
- The scanner can be implemented without guessing the Phase 2 order of operations.

---

### Step 2: Universe And Provider Support

Outcome:

- The project can seed S&P 500 plus Nasdaq 100 without duplicate symbols.
- Alpha Vantage exists as the first real provider adapter target.

Tasks:

- Add a Nasdaq 100 seed source or curated seed file.
- Add import/dedupe behavior for overlapping S&P 500 and Nasdaq 100 symbols.
- Add Alpha Vantage config through environment variables only.
- Add Alpha Vantage daily OHLCV adapter mapping into normalized internal bar models.
- Add fixture-based tests for provider response mapping.
- Avoid live API calls in automated tests.

Exit criteria:

- Seed/import tests pass.
- Alpha Vantage mapping tests pass with fixtures.
- No API key is committed or exposed to frontend code.

Notes:

- This work should be rate-limit-aware.
- Full-universe live refresh can remain manual or conservative during Phase 2.

---

### Step 3: Indicator Expansion

Outcome:

- `IndicatorService` exposes the scanner inputs required by Phase 2 setup detectors.

Likely inputs:

- SMA/EMA trend state;
- 20-day and 50-day highs;
- 52-week high distance;
- average volume and relative volume;
- ATR or ATR-like volatility estimate;
- recent range/consolidation measures;
- relative strength proxy versus SPY or another benchmark if available;
- insufficient-history warnings.

Exit criteria:

- Indicator tests cover normal, insufficient-history, missing-data, and zero/invalid-value cases.
- Indicator output remains provider-independent.

---

### Step 4: Setup Detectors

Outcome:

- Scanner can identify three deterministic setup families.

Implementation order:

1. Breakout.
2. Pullback continuation.
3. Relative strength leader.

Detector requirements:

- deterministic boolean/rule outputs;
- setup type;
- reasons;
- caution flags;
- score component hints;
- no AI-generated judgment;
- no direct database writes from detector functions.

Exit criteria:

- Each detector has unit tests.
- Each detector can return zero candidates without error.
- Reasons and warnings are stable enough for UI display.

---

### Step 5: Scoring And Candidate Status Rules

Outcome:

- Candidate output includes explainable scores and conservative status labels.

Score components should remain transparent, for example:

- trend quality;
- setup quality;
- volume confirmation;
- relative strength;
- risk/reward quality;
- data quality / caution penalties.

Candidate status rules:

- `Blocked`: required price data is missing, stale, invalid, or insufficient.
- `Avoid`: setup exists but caution/risk conditions are too weak.
- `Watch`: setup is promising but confirmation or risk/reward is not strong enough.
- `Actionable`: only allowed when risk/reward exists, required price data is fresh, setup confirmation is present, and blocking caution flags are absent.

Exit criteria:

- Status rule tests cover all status labels.
- `Actionable` cannot appear without risk/reward data.

---

### Step 6: Risk/Reward Scaffold

Outcome:

- Candidate output includes first-pass entry, invalidation, target, and risk/reward estimate.

MVP constraints:

- values are research estimates, not instructions;
- stop/target logic must be deterministic;
- missing volatility or price structure should downgrade or block status;
- no position sizing is required unless trivial and explicitly accepted later.

Exit criteria:

- Risk/reward tests cover normal cases, invalid prices, zero risk, missing ATR/volatility, and low reward/risk.

---

### Step 7: Scanner Run Flow And Persistence

Outcome:

- A scanner command or backend flow runs the Phase 2 deterministic scanner and writes generated candidates to existing Phase 1 tables.

Tasks:

- Reuse `scan_runs` and `scan_candidates`.
- Version or label Phase 2 scanner runs clearly.
- Persist reasons, score breakdown, warnings, setup type, and risk/reward fields.
- Ensure latest scan API can return the generated Phase 2 output.

Exit criteria:

- Scanner persistence tests pass.
- Latest scan API returns generated scanner output without frontend contract breakage.

---

### Step 8: Focused Frontend Inspection Hook

Outcome:

- The frontend can inspect Phase 2 generated scanner evidence.

Scope:

- surface setup type;
- show score/reason breakdown;
- show caution flags;
- show risk/reward fields if present;
- keep current frontend shell modest.

Out of scope:

- full chart signal markers;
- sector/theme scanner grid;
- AI insight panel;
- full dashboard redesign.

Exit criteria:

- Frontend build passes.
- UI copy remains research-oriented and does not imply trading advice.

---

### Step 9: Phase 2 Review And Closeout

Outcome:

- Phase 2 is ready to merge.

Required review:

- code review;
- security review;
- trading-safety review;
- test review;
- documentation review.

Required commands before closeout:

```powershell
docker compose config
docker compose run --rm backend pytest
npm.cmd run build
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH)" -S .
```

Exit criteria:

- `phase-2-code-security-trading-review.md` is completed.
- `phase-2-pull-request-draft.md` is updated.
- Phase 2 tracker statuses reflect actual completion.

---

## 3. Build Order Recommendation

Recommended first coding order:

1. Add Nasdaq 100 seed/dedupe support.
2. Add Alpha Vantage adapter with fixture tests. ✅ Done
3. Expand indicator snapshots. ✅ Done
4. Implement breakout detector. ✅ Done
5. Add scoring and risk/reward scaffold. ✅ Done
5.1. Make risk/reward assumptions configurable. ✅ Done
6. Add conservative candidate status rules. ✅ Done
7. Add pullback and relative strength detectors. ✅ Done
8. Persist Phase 2 generated scanner output. ✅ Done
9. Add focused frontend evidence display. ✅ Done
10. Run review and closeout.

This order keeps the system testable at each step and avoids letting UI polish outrun scanner correctness.

---

## 4. Known Risks

| Risk | Mitigation |
| --- | --- |
| Alpha Vantage rate limits constrain full-universe refreshes | Use fixture tests, manual ingestion, caching, and conservative refresh flows |
| Nasdaq 100 overlaps with S&P 500 | Dedupe by normalized symbol during seed/import |
| Early detector rules overfit | Keep rules simple and document assumptions |
| `Actionable` creates false confidence | Require risk/reward, fresh data, and no blocking caution flags |
| Relative strength proxy is mistaken for true benchmark-relative strength | Current Phase 2 detector uses price leadership only; add SPY/QQQ-relative returns once benchmark bars are in scanner input |
| Frontend implies advice | Use research-oriented labels and keep evidence visible |

---

## 5. Status Legend

| Status | Meaning |
| --- | --- |
| ⬜ Not Started | Work has not begun |
| 🟨 In Progress | Work is actively underway |
| ✅ Done | Work is complete |
| ⛔ Blocked | Work cannot continue until a blocker is resolved |
