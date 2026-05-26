# Phase 2 Execution Tracker: Technical Scanner

**Project:** PoorToPour  
**Phase:** Phase 2 - Technical Scanner MVP  
**Status:** Active  
**Branch:** `feature/phase_2_technical_scanner`  
**Last updated:** 2026-05-26

---

## 1. Phase Goal

Turn the Phase 1 data foundation into a more complete deterministic technical scanner.

Phase 2 should produce scanner output that is still research-only, explainable, and safe for manual review.

MVP boundaries remain:

- long-only;
- daily/weekly swing research;
- no broker automation;
- no AI-generated trade decisions;
- no `Actionable` status until risk/reward and safety checks exist.

---

## 2. Detailed Checklist

Legend: `Not Started` | `In Progress` | `Done` | `Blocked`

| ID | Work Item | Status | Verification / Exit Criteria |
| --- | --- | --- | --- |
| P2-A | Define Phase 2 scanner scope | Not Started | Confirm first setup families and minimum viable scoring inputs |
| P2-B | Expand indicator coverage | Not Started | Add required indicators beyond Phase 1 snapshot if needed |
| P2-C | Implement breakout detector | Not Started | Deterministic rules with reasons and tests |
| P2-D | Implement pullback continuation detector | Not Started | Deterministic rules with reasons and tests |
| P2-E | Implement relative strength leader detector | Not Started | Deterministic rules with reasons and tests |
| P2-F | Add scanner scoring components | Not Started | Score breakdown is explainable and covered by tests |
| P2-G | Add risk/reward estimate scaffold | Not Started | Candidates can show entry, invalidation, target, and risk/reward estimate |
| P2-H | Add candidate status rules | Not Started | `Actionable`, `Watch`, `Avoid`, and `Blocked` rules are explicit |
| P2-I | Persist generated scan output | Not Started | Generated candidates write to existing `scan_runs` and `scan_candidates` tables |
| P2-J | Add scanner command/API flow | Not Started | Manual command or endpoint can run deterministic scanner locally |
| P2-K | Add focused frontend inspection hook | Not Started | Dashboard can surface score reasons/caution flags from generated candidates |
| P2-L | Phase 2 review checkpoint | Not Started | Code review, security review, and trading-safety review completed |

---

## 3. Acceptance Criteria

| ID | Acceptance Criterion | Status | Notes |
| --- | --- | --- | --- |
| AC-P2-001 | Scanner setup families are documented for implementation | Not Started | Breakout, pullback continuation, relative strength leader |
| AC-P2-002 | Scanner rules are deterministic and explainable | Not Started | No AI-generated trade decisions |
| AC-P2-003 | Scanner output includes reasons and score breakdown | Not Started | Candidate detail must show why it appeared |
| AC-P2-004 | Scanner output includes caution flags | Not Started | Missing data and weak confirmations should be visible |
| AC-P2-005 | Risk/reward estimate exists before `Actionable` status | Not Started | Trading-safety requirement |
| AC-P2-006 | Generated candidates persist to database | Not Started | Uses Phase 1 `scan_runs` and `scan_candidates` |
| AC-P2-007 | Tests cover indicator/scanner behavior | Not Started | Unit tests for setup detectors and scoring |
| AC-P2-008 | Phase 2 review is complete before merge | Not Started | Dedicated review artifact required |

---

## 4. Test Tracking

| Test ID | Description | Type | File / Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-P2-001 | Setup detector tests | Unit | TBD | Not Started | One test group per setup family |
| T-P2-002 | Score breakdown tests | Unit | TBD | Not Started | Verify component contributions and thresholds |
| T-P2-003 | Risk/reward estimate tests | Unit | TBD | Not Started | Required before `Actionable` status |
| T-P2-004 | Scanner persistence tests | Unit/Integration | TBD | Not Started | Verify generated scan writes cleanly |
| T-P2-005 | Backend test suite | Regression | `docker compose run --rm backend pytest` | Not Started | Must pass before Phase 2 review |
| T-P2-006 | Frontend build | Build | `npm.cmd run build` | Not Started | Must pass before Phase 2 review |

---

## 5. Open Questions

| ID | Question | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| Q-P2-001 | Which setup detector should be implemented first? | Jesse + AI | Open | Suggested first: breakout, because it maps well to chart evidence |
| Q-P2-002 | How conservative should `Actionable` be in first scanner MVP? | Jesse + AI | Open | Should require risk/reward and multiple confirmations |
| Q-P2-003 | Should Phase 2 include frontend candidate-detail improvements? | Jesse + AI | Open | Keep small unless needed for scanner review |

---

## 6. Phase Risks

| ID | Risk | Severity | Status | Notes |
| --- | --- | --- | --- | --- |
| R-P2-001 | False confidence from early scanner output | High | Watching | Keep explanations, warnings, and manual-review language visible |
| R-P2-002 | Overfitting setup rules too early | Medium | Watching | Keep first rules simple and testable |
| R-P2-003 | Letting UI polish outrun scanner correctness | Medium | Watching | Scanner correctness comes first in Phase 2 |

---

## 7. Review Artifacts

| Artifact | Path |
| --- | --- |
| Code/security/trading review | `/docs/phases/phase-2-technical-scanner/phase-2-code-security-trading-review.md` |
| Pull request draft | `/docs/phases/phase-2-technical-scanner/phase-2-pull-request-draft.md` |
