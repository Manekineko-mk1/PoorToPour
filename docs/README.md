# PoorToPour Docs

This folder holds project planning, execution tracking, phase artifacts, and reference material.

## Current Structure

| Path | Purpose |
| --- | --- |
| `/docs/*.md` | Core planning and execution documents. These remain at the top level for Phase 1 to avoid pre-commit link churn. |
| `/docs/phases/` | Phase-specific artifacts such as reviews, PR drafts, release notes, and closeout summaries. |
| `/docs/phases/phase-1-data-foundation/` | Phase 1 tracker, review, and pull request draft. |
| `/docs/phases/phase-2-technical-scanner/` | Phase 2 tracker, implementation plan, review, and pull request draft. |
| `/docs/phases/phase-3-dashboard-mvp/` | Phase 3 tracker, implementation plan, review, and pull request draft. |
| `/docs/references/` | Supporting visual and research references. |
| `/docs/references/Mock_UI_Renders/` | PoorToPour mock UI renders. |
| `/docs/references/Research_Docs/` | External inspiration screenshots and research references. |

## Phase Artifact Pattern

Use this structure for future phases:

```text
docs/phases/phase-N-short-name/
  phase-N-execution-tracker.md
  phase-N-implementation-plan.md
  phase-N-code-security-trading-review.md
  phase-N-pull-request-draft.md
```

Keep durable product, architecture, strategy, cost, and execution documents linked from the root `README.md`.

## Future Feature Parking

Use these durable docs for features that should survive across phase trackers:

| Feature Type | Canonical Home |
| --- | --- |
| MVP/MVP+ product features | `/docs/01-product-requirements.md`, Section 14 |
| High-level phase roadmap and external inspiration parking lot | `/docs/00-project-plan-v0.3.md`, Section 6 |
| Trading-rule or indicator follow-ups | `/docs/02-trading-strategy-requirements.md` |

Phase trackers can link or mirror these items, but future MVP/MVP+ features should not live only inside one phase folder.
