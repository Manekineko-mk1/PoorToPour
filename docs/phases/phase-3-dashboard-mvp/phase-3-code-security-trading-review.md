# Phase 3 Code, Security, Trading, and UX Review

**Project:** PoorToPour
**Phase:** Phase 3 - Dashboard MVP
**Status:** ⬜ Not Started
**Last updated:** 2026-05-28

---

## 1. Review Scope

To be completed before Phase 3 merge.

Expected review areas:

- dashboard shell, routing, and responsive layout;
- latest scan summary and data-health states;
- candidate ranking table;
- candidate detail page and chart evidence;
- backend chart/candidate/scan/settings APIs;
- manual scan flow;
- scan history;
- settings page and secret redaction;
- yfinance-first MVP scan-data labelling and provider abstraction preservation;
- accessibility and UX polish;
- trading-safety wording and deterministic evidence display.

---

## 2. Code Review

**Status:** ⬜ Not Started.

Findings:

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| TBD | TBD | TBD | ⬜ Not Started |

---

## 3. Security Review

**Status:** ⬜ Not Started.

Required checks:

```powershell
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH|DATABASE_URL)" -S --glob '!.env' --glob '!.env.*' --glob '!frontend/node_modules/**' --glob '!frontend/dist/**' --glob '!backend/.venv/**' .
```

Security focus:

- no API keys, database URLs, or provider secrets exposed in frontend responses;
- settings page displays only safe configuration;
- manual scan flow does not leak provider errors containing secrets;
- hosted/manual scan behavior is constrained enough to avoid accidental full-universe paid or rate-limited provider calls;
- hosted/demo behavior is safe for public access.

---

## 4. Trading-Safety Review

**Status:** ⬜ Not Started.

Required checks:

- candidate visuals remain research evidence, not trade instructions;
- risk/reward copy is clearly labelled as an estimate;
- stale, missing, failed, and partial data states are visible;
- chart overlays come from deterministic backend/scanner output;
- yfinance-backed output is labelled as unofficial MVP data with source/freshness visible;
- no broker automation or AI-generated trade decisions are introduced.

---

## 5. UX and Accessibility Review

**Status:** ⬜ Not Started.

Required checks:

- desktop layout follows MVP dashboard flow;
- tall/narrow 1080x2560 layout remains usable;
- table overflow is intentional and readable;
- chart area renders nonblank and does not overlap text;
- status is communicated with text plus color;
- navigation, filters, table rows, and buttons are keyboard accessible enough for MVP.

---

## 6. Final Verification

To be completed before closeout:

```powershell
docker compose run --rm backend pytest
npm.cmd run build
```

Manual checks:

- Dashboard loads.
- Candidate detail opens.
- Chart evidence renders.
- Scan History loads.
- Settings loads without secrets.
- Manual scan flow handles success and failure.

---

## 7. Remaining Risks / Follow-Ups

To be completed during review.
