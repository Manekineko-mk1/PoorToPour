# Phase 2 Execution Tracker: Technical Scanner

**Project:** PoorToPour
**Phase:** Phase 2 - Technical Scanner MVP
**Status:** ✅ Review Complete
**Branch:** `feature/phase_2_technical_scanner`
**Last updated:** 2026-05-27

---

## 1. Phase Goal

Turn the Phase 1 data foundation into a more complete deterministic technical scanner.

Phase 2 should produce scanner output that is still research-only, explainable, persisted, and safe for manual review.

MVP boundaries remain:

- long-only;
- daily/weekly swing research;
- deterministic scanner rules;
- no broker automation;
- no AI-generated trade decisions;
- no `Actionable` status until risk/reward and safety checks exist.

Supporting decisions now in force:

- first real provider adapter target: Alpha Vantage;
- MVP universe: S&P 500 plus Nasdaq 100, with duplicate symbols merged;
- first setup detector: breakout;
- dashboard MVP comes before full backtesting;
- alerts remain dashboard-only at first.

Implementation plan:

`/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md`

---

## 2. Detailed Checklist

Legend: `⬜ Not Started` | `🟨 In Progress` | `✅ Done` | `⛔ Blocked`

| ID | Work Item | Status | Verification / Exit Criteria |
| --- | --- | --- | --- |
| P2-A | Define Phase 2 scanner scope | ✅ Done | Scope and sequence documented in `phase-2-implementation-plan.md` |
| P2-B | Add Nasdaq 100 universe support | ✅ Done | `seed_mvp_universe` imports 516 unique symbols; duplicate S&P 500 symbols keep primary metadata |
| P2-C | Add Alpha Vantage provider adapter | ✅ Done | Env-only API key config, daily OHLCV adapter, ingest command, and fixture tests exist |
| P2-D | Expand indicator coverage | ✅ Done | Breakout-ready highs, prior highs, ATR, range position, and distance fields exist |
| P2-E | Implement breakout detector | ✅ Done | Deterministic breakout rules return Watch/Blocked only, with reasons, warnings, and unit tests |
| P2-F | Implement pullback continuation detector | ✅ Done | Deterministic rules, pullback scoring, pullback risk/reward, reasons, cautions, and unit tests exist |
| P2-G | Implement relative strength leader detector | ✅ Done | Deterministic price-leadership proxy rules, scoring, reasons, cautions, and unit tests exist |
| P2-G.1 | Add benchmark-relative strength inputs | ⬜ Not Started | Later MVP/MVP+ work should compare candidate returns against SPY/QQQ once benchmark bars are part of scanner input |
| P2-H | Add scanner scoring components | ✅ Done | Breakout score breakdown is explainable, clamped, caution-aware, and covered by tests |
| P2-I | Add risk/reward estimate scaffold | ✅ Done | Breakout candidates show entry, invalidation, 2R target, and risk/reward estimate |
| P2-I.1 | Make risk/reward parameters configurable | ✅ Done | ATR buffer and target multiple are configurable through reviewed app settings/env defaults |
| P2-J | Add candidate status rules | ✅ Done | Shared status rules cover `Actionable`, `Watch`, `Avoid`, and `Blocked`; breakout detector uses them |
| P2-K | Persist generated scan output | ✅ Done | Phase 2 scanner output writes to existing `scan_runs` and `scan_candidates` tables |
| P2-L | Add scanner command/API flow | ✅ Done | `run_technical_scan` command runs deterministic scanner locally and persists output |
| P2-M | Add focused frontend inspection hook | ✅ Done | Dashboard surfaces setup type, score components, reasons, risk/reward details, and caution flags from generated candidates |
| P2-N | Phase 2 review checkpoint | ✅ Done | Code review, security review, and trading-safety review completed in `phase-2-code-security-trading-review.md` |

---

## 3. Acceptance Criteria

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P2-001 | Scanner setup families are documented for implementation | ✅ Done | Breakout first, then pullback continuation and relative strength leader |
| AC-P2-002 | Scanner rules are deterministic and explainable | ✅ Done | Breakout, pullback continuation, and relative strength leader detectors use explicit rules only |
| AC-P2-003 | Scanner output includes reasons and score breakdown | ✅ Done | Scanner candidates include reasons and structured score breakdowns visible in the frontend evidence panel |
| AC-P2-004 | Scanner output includes caution flags | ✅ Done | Detectors emit missing-data, weak-confirmation, and setup-specific caution flags |
| AC-P2-005 | Risk/reward estimate exists before `Actionable` status | ✅ Done | Breakout risk/reward scaffold, configurable assumptions, and shared status rules exist |
| AC-P2-006 | Generated candidates persist to database | ✅ Done | `run_technical_scan` persisted Phase 2 candidates to existing scan tables |
| AC-P2-007 | Alpha Vantage adapter does not expose secrets | ✅ Done | API key is read from env/config; `.env.example` contains only an empty placeholder |
| AC-P2-008 | S&P 500 plus Nasdaq 100 universe can be seeded without duplicates | ✅ Done | `AAPL` keeps S&P metadata; Nasdaq-only symbols such as `ARM` are added |
| AC-P2-009 | Tests cover indicator/scanner/provider behavior | ✅ Done | Unit tests cover provider mapping, indicators, setup detectors, scoring, risk/reward, and status rules |
| AC-P2-010 | Phase 2 review is complete before merge | ✅ Done | Code/security/trading review completed on 2026-05-27 |

---

## 4. Test Tracking

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P2-001 | Nasdaq 100 seed/import tests | Unit/Data | `backend/tests/test_sp500_seed.py` | ✅ Pass | Verifies required columns, symbol normalization, and dedupe behavior |
| T-P2-002 | Alpha Vantage adapter mapping tests | Unit | `backend/tests/test_alpha_vantage_provider.py` | ✅ Pass | Uses fixtures, not live API calls; malformed dates/OHLC rows are skipped |
| T-P2-003 | Indicator expansion tests | Unit | `backend/tests/test_indicator_service.py` | ✅ Pass | Verifies breakout inputs, ATR, range position, prior highs, and insufficient-history warnings |
| T-P2-004 | Breakout detector tests | Unit | `backend/tests/test_breakout_detector.py` | ✅ Pass | Covers confirmed, near, blocked, and weak non-breakout cases |
| T-P2-004A | Pullback continuation detector tests | Unit | `backend/tests/test_pullback_detector.py` | ✅ Pass | Covers confirmed, developing, blocked, and broken-trend cases |
| T-P2-004B | Relative strength leader detector tests | Unit | `backend/tests/test_relative_strength_detector.py` | ✅ Pass | Covers confirmed leader, shorter-term proxy, blocked, and lagging cases |
| T-P2-005 | Score breakdown tests | Unit | `backend/tests/test_scoring.py` | ✅ Pass | Verifies component contributions, caution penalty, and score clamping |
| T-P2-006 | Risk/reward estimate tests | Unit | `backend/tests/test_risk_reward.py` | ✅ Pass | Verifies ATR-buffered invalidation, 2R target, missing inputs, and invalid risk |
| T-P2-006A | Risk/reward config tests | Unit | `backend/tests/test_scanner_config.py` | ✅ Pass | Verifies configurable ATR buffer and target multiple defaults and validation |
| T-P2-007 | Candidate status rule tests | Unit | `backend/tests/test_status_rules.py` | ✅ Pass | Confirms conservative `Actionable`, `Watch`, `Avoid`, and `Blocked` behavior |
| T-P2-008 | Scanner persistence tests | Unit/Integration | `backend/tests/test_technical_scanner.py`; `python -m app.scripts.run_technical_scan --limit 10` | ✅ Pass | Unit tests cover composed scan output; local command persisted 10-symbol scan with 2 candidates |
| T-P2-009 | Backend test suite | Regression | `docker compose run --rm backend pytest` | ✅ Pass | 69 passed after review freshness, symbol-resolution, and provider-validation coverage |
| T-P2-011 | Technical scanner command | Manual/Integration | `docker compose run --rm backend python -m app.scripts.run_technical_scan --limit 10` | ✅ Pass | Persisted `technical_scan_20260527_044237_959bb63a` with 2 candidates |
| T-P2-010 | Frontend build | Build | `npm.cmd run build` | ✅ Pass | Build passed after focused scanner evidence display |
| T-P2-012 | Frontend local smoke check | Manual | `Invoke-WebRequest http://localhost:5173`; `GET /api/scans/latest` | ✅ Pass | Frontend returned 200; latest scan returned `Technical Scanner MVP` with 2 candidates |
| T-P2-013 | Review security/dependency checks | Review | `docker compose config --quiet`; `pip check`; `npm audit`; secret scan | ✅ Pass | No real API key found in tracked files; dependency checks passed |

---

## 5. Resolved Questions

| ID | Question | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| Q-P2-001 | Which setup detector should be implemented first? | Jesse + AI | 🟩 Resolved | Breakout first, because it maps well to chart evidence and signal markers |
| Q-P2-002 | How conservative should `Actionable` be in first scanner MVP? | Jesse + AI | 🟩 Resolved | Require risk/reward, fresh required price data, setup confirmation, and no blocking caution flags |
| Q-P2-003 | Should Phase 2 include frontend candidate-detail improvements? | Jesse + AI | 🟩 Resolved | Yes, but only a focused inspection hook for generated scanner evidence; full dashboard polish remains Phase 3 |

---

## 6. Phase Risks

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-P2-001 | False confidence from early scanner output | High | 🟧 Watching | Keep explanations, warnings, and manual-review language visible |
| R-P2-002 | Overfitting setup rules too early | Medium | 🟧 Watching | Keep first rules simple, deterministic, and testable |
| R-P2-003 | Letting UI polish outrun scanner correctness | Medium | 🟧 Watching | Scanner correctness comes first in Phase 2 |
| R-P2-004 | Alpha Vantage rate limits slow full-universe refreshes | Medium | 🟧 Watching | Use fixture tests, caching, batching where available, and rate-limit-aware ingestion |
| R-P2-005 | Nasdaq 100 overlap creates duplicate candidates | Medium | 🟧 Watching | Universe seed/import must dedupe by normalized symbol |
| R-P2-006 | `Actionable` appears before risk/reward is trustworthy | High | 🟧 Watching | Shared status rules require setup confirmation, risk/reward, fresh price data, high score, and no caution flags |
| R-P2-007 | Hardcoded risk/reward assumptions become hidden strategy rules | Medium | ✅ Closed | ATR buffer and target multiple are now explicit configurable defaults |
| R-P2-008 | Relative strength proxy is mistaken for benchmark-relative strength | Medium | 🟦 Open | Current detector uses price leadership only; revisit SPY/QQQ-relative return once benchmark bars are available |

---

## 7. Review Artifacts

| Artifact | Path |
| --- | --- |
| Implementation plan | `/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md` |
| Code/security/trading review | `/docs/phases/phase-2-technical-scanner/phase-2-code-security-trading-review.md` |
| Pull request draft | `/docs/phases/phase-2-technical-scanner/phase-2-pull-request-draft.md` |

---

## 8. Change Log

| Date | Update | Author |
| --- | --- | --- |
| 2026-05-26 | Added Phase 2 implementation plan and marked scope definition complete | Jesse + AI |
| 2026-05-26 | Added Nasdaq 100 seed, combined MVP universe seeder, dedupe tests, and local database verification for 516 unique symbols | Jesse + AI |
| 2026-05-26 | Added Alpha Vantage daily OHLCV adapter, env-only config, ingest command, fixture tests, and Compose env wiring | Jesse + AI |
| 2026-05-26 | Expanded IndicatorService with breakout-ready highs, prior highs, ATR, range-position fields, and tests | Jesse + AI |
| 2026-05-26 | Added deterministic breakout detector returning conservative Watch/Blocked candidates with reasons, caution flags, and tests | Jesse + AI |
| 2026-05-26 | Added breakout score components, caution penalties, risk/reward scaffold, and focused tests | Jesse + AI |
| 2026-05-26 | Added shared candidate status rules and wired breakout detector through the conservative status gate | Jesse + AI |
| 2026-05-26 | Made breakout risk/reward ATR buffer and target multiple configurable through app settings/env defaults | Jesse + AI |
| 2026-05-27 | Added pullback continuation and relative strength leader detectors with scoring, risk/reward, cautions, and tests | Jesse + AI |
| 2026-05-27 | Added Phase 2 technical scanner run composition and persistence command using existing scan tables | Jesse + AI |
| 2026-05-27 | Added focused frontend scanner evidence display for selected generated candidates | Jesse + AI |
| 2026-05-27 | Completed Phase 2 code/security/trading-safety review and fixed stale price-data gating in setup detectors | Jesse + AI |
| 2026-05-27 | Completed coding-standards follow-up for shared symbol resolution, repeated risk/reward warning text, and relative-strength detector complexity | Jesse + AI |
| 2026-05-27 | Re-ran Phase 2 review against updated guidelines and added shared provider daily-bar validation | Jesse + AI |
