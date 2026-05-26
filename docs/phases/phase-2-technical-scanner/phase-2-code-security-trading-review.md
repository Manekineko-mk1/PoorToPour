# Phase 2 Code, Security, and Trading Review

**Project:** PoorToPour  
**Phase:** Phase 2 - Technical Scanner MVP  
**Status:** Not started  
**Last updated:** 2026-05-26

---

## 1. Review Scope

TBD during Phase 2.

Expected review areas:

- scanner setup detection logic;
- score breakdown correctness;
- risk/reward estimate behavior;
- generated candidate status rules;
- database persistence behavior;
- frontend display of scanner reasons and caution flags;
- security and dependency posture.

---

## 2. Code Review

**Status:** Not started.

Findings:

| Severity | Finding | File / Area | Status |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

---

## 3. Security Review

**Status:** Not started.

Checks to run:

```powershell
docker compose config
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH)" -S .
```

---

## 4. Trading-Safety Review

**Status:** Not started.

Required checks:

- Candidate statuses are conservative.
- `Actionable` requires risk/reward estimate.
- Missing required price data blocks candidates.
- Caution flags are visible.
- Scanner output is framed as research, not advice.
- No broker automation or order placement exists.

---

## 5. Final Verification

TBD.
