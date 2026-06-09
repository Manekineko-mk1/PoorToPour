# Repo-Level Health Check — Code & Security Review

**Project:** PoorToPour
**Scope:** Whole repository (cross-phase), not a single feature/PR
**Reviewer:** Staff-level engineering pass (AI), against `/docs/10-ai-working-guidelines.md`
**Branch reviewed:** `feature/phase_3_dashboard_mvp`
**Date:** 2026-06-04
**Overall status:** 🟩 Healthy for local research MVP — no critical defects. A small set of Medium/Low items should be cleared before any hosted/MVP+ exposure.

---

## 1. Method

Reviewed against the guideline checklists in `10-ai-working-guidelines.md`:
§5 engineering principles, §5.9 coding-standards, §5.10 complexity triggers, §6 trading-safety, §7 testing, §8 security (OWASP ASVS L1 / NIST SSDF / CIS Docker references).

Surfaces examined:

- Backend: API routes (`scans`, `market_data`, `configuration`, `health`), services (`scanner`, `setup_detectors`, `indicators`, `scoring`, `risk_reward`, `status_rules`, `chart_data`, `market_data_refresh`), providers (`yfinance`, `alpha_vantage`, `mock`, `validation`), repositories, `core/config`, `core/security`, `db` models/base, `main`.
- Frontend: `api.ts` (typed API boundary), `App.tsx` surface.
- Deployment/config: `docker-compose.yml`, `backend/Dockerfile`, `.env.example`, `.gitignore`, `backend/requirements.txt`, `frontend/package.json`.

Grounding checks run:

```powershell
git status --short              # clean working tree
git diff --check               # ✅ no whitespace/conflict markers
git grep -nE "(BEGIN RSA|BEGIN OPENSSH|sk-[A-Za-z0-9]{20}|AKIA[0-9A-Z]{16})"   # ✅ no real secrets (only doc references to the scan command)
```

Backend pytest and `npm audit` were last run green in the Phase 3 review (83 passed, 0 vulns) and the tree is unchanged for that scope; this pass focuses on cross-cutting structure, not re-running gates.

---

## 2. Summary of Findings

| ID | Severity | Area | Finding | Status |
| --- | --- | --- | --- | --- |
| C1 | 🟧 Medium | Efficiency (§5.10) | Indicator snapshot recomputed 3× per symbol (once per detector) + per-symbol bar query in `run_manual_scan` (N+1). | 🟦 Open |
| C2 | 🟦 Low | Defensive (§5.5) | `GET /api/scans?limit=` is unbounded/unvalidated; negative value can 500, huge value is an unbounded fetch. | 🟦 Open |
| C3 | 🟦 Low | Maintainability (§6.1) | Candidate status is derived by string-matching human-readable caution-flag text; trading-sensitive logic is coupled to copy. | 🟦 Open |
| C4 | 🟦 Low | DRY (§5.4) | `MomentumScanner` (Phase 1 bootstrap) duplicates scoring/reason logic with magic-number thresholds now superseded by `scoring.py`/`setup_detectors.py`. | 🟦 Open |
| S1 | 🟧 Medium | Supply chain (§8.1 SSDF) | `frontend/package.json` pins almost every dependency to `"latest"` → non-reproducible builds, unreviewed major upgrades. | 🟦 Open |
| S2 | 🟦 Low | AuthN (§8.1 OWASP) | Manual-scan API key compared with `!=` (non-constant-time); use `secrets.compare_digest`. | 🟦 Open |
| S3 | 🟦 Low | Container (§8.1 CIS) | Backend image runs as root (no `USER`); `adminer` DB UI shipped in compose. | 🟧 Watching |
| S4 | ℹ️ Info | AuthN | No auth layer on read endpoints (known/accepted for local MVP). | 🟧 Watching |
| T1 | 🟧 Medium | Trading data (§6.4) | yfinance is unofficial, non-trading-grade (known, labelled). | 🟧 Watching |
| T2 | 🟦 Low | Trading logic (§6.1) | Relative-strength uses a price-leadership proxy, not true benchmark-relative strength (documented). | 🟧 Watching |
| P1 | 🟦 Low | Tooling (§5.2) | No linter/formatter/type-check or CI gate wired yet (ruff/black/eslint referenced as future). No frontend test runner. | 🟦 Open |

No 🟥 Critical or 🟥 High-severity defects found. The deterministic scanner, risk/reward guards, secret handling, and persistence transaction boundaries are sound.

---

## 3. Code Review

### C1 — Indicator snapshot recomputed per detector + N+1 bar load 🟧 Medium (efficiency)

`TechnicalScanner.scan` runs every detector for every symbol, and each detector
independently calls `self.indicator_service.build_snapshot(...)`:

- `backend/app/services/scanner.py:45-50`
- `backend/app/services/setup_detectors.py:47, 158, 274`

With three detectors that means the full SMA/EMA/ATR/rolling-high snapshot is
computed **three times per symbol**. Separately, `run_manual_scan` builds
`bars_by_symbol` with one DB round-trip per symbol:

- `backend/app/api/routes/scans.py:80`

For the MVP universe (~600 symbols) that is ~1,800 snapshot computations and
~600 queries per scan. Negligible today on small local data, but it scales with
the universe and is exactly the kind of "tangled responsibility / repeated work"
§5.10 flags. **Recommendation:** compute the snapshot once per symbol (in the
scanner) and pass it into the detectors; batch-load bars for all run symbols in
one query (`WHERE symbol IN (...)` grouped in Python). Low-risk, deterministic,
covered by existing tests.

### C2 — Unbounded `limit` on scan-history endpoint 🟦 Low (defensive)

`backend/app/api/routes/scans.py:27`

```python
def list_scan_runs(db: Session = Depends(get_db), limit: int = 20) -> list[dict]:
```

Unlike `refresh_limit` (correctly `Query(default=None, ge=1)`), `limit` has no
bounds. `?limit=-1` flows into SQLAlchemy `.limit(-1)` → Postgres rejects a
negative LIMIT → 500; `?limit=99999999` is an unbounded fetch + serialize.
**Recommendation:** `limit: int = Query(default=20, ge=1, le=100)`. Mirror the
guard in `repositories/scans.list_scan_runs`.

### C3 — Status inferred from caution-flag prose 🟦 Low (trading-sensitive maintainability)

`backend/app/services/status_rules.py:47-53`

```python
def _is_blocking_caution(flag: str) -> bool:
    normalized = flag.casefold()
    return (
        normalized.startswith("missing required")
        or normalized.startswith("at least ")
        or "price data is stale" in normalized
    )
```

Whether a candidate becomes **Blocked** depends on matching the wording of
human-readable warning strings produced elsewhere. Per §5.10/§6.1 trading logic
should be explainable and decoupled from copy: reword a warning (e.g. for UX) and
a candidate could silently flip status. The structured inputs already exist on
`CandidateStatusInput` (`missing_required_fields`, `price_data_fresh`), so the
text match is partly redundant. **Recommendation:** drive blocking purely from
structured fields / an enum of caution *kinds*; keep the display text separate.

### C4 — Legacy MomentumScanner duplicates scoring with magic numbers 🟦 Low (DRY)

`backend/app/services/scanner.py:170-203` (`_score_snapshot`, `_reasons`,
`_status_for_score`) re-implement scoring/reason/threshold logic (45, 25, 20, 15…)
that the Phase 2 `scoring.py` + `setup_detectors.py` now own in a more structured
way. It's an intentional Phase 1 bootstrap, but two parallel scoring styles invite
drift (§5.4). **Recommendation:** if `MomentumScanner` is still used only by
`scripts/run_momentum_scan.py`, mark it explicitly as deprecated/bootstrap in the
docstring and exclude it from the dashboard path; otherwise migrate it onto the
shared `scoring`/`status_rules` helpers.

### Code notes — confirmed sound (no action)

- ✅ Risk/reward guards: `risk_per_share <= 0 → None`, ATR/target multiplier `> 0`
  guards, and "estimate unavailable" caution are correct (`risk_reward.py`,
  `setup_detectors._append_risk_reward_caution`). No division-by-zero paths.
- ✅ Indicator math handles short history (returns `None` + warnings) and avoids
  div-by-zero in `relative_volume`, `_range_position_pct`, `_percent_distance`.
- ✅ Chart RSI is incremental Wilder's smoothing in O(n) and SMA is O(n) rolling
  (the earlier O(n²) note from the Phase 3 secondary review is resolved).
- ✅ Persistence: `run_manual_scan` wraps refresh + scan upsert in one transaction
  with `db.rollback()` on failure; no partial-mutate-then-fail (§5.5).
- ✅ All DB access is via SQLAlchemy ORM with bound parameters — no SQL injection
  surface; path params are upper-cased, not interpolated into SQL.
- ✅ yfinance multi-symbol frame de-multiplexing (`_frame_for_downloaded_symbol`)
  fails loud (logs + empty frame) rather than silently dropping data.

---

## 4. Security Review

**Status:** 🟩 Passed for local MVP scope. Items below are hardening for hosted/MVP+.

Confirmed good:

- ✅ No real secrets tracked; `.env` and `.env.*` gitignored with `!.env.example`.
- ✅ Provider keys are backend-only; `GET /api/settings/display` returns no secret
  values and only exposes scanner config when `is_local` (`configuration.py:29`).
- ✅ External provider payloads validated before use (`providers/validation.py`,
  Alpha Vantage / yfinance NaN + OHLC sanity checks).
- ✅ Refresh failures are redacted to clients with a trace id; full exception stays
  in logs only (`market_data_refresh.py:42-53`) — good secret-leak hygiene (§8).
- ✅ Hosted manual scan is disabled by default, gated by `allow_hosted_manual_scan`,
  symbol-capped, rate-limited, and API-key-guarded (`scans.py`, `core/security.py`).
- ✅ Ports bound to `127.0.0.1` in compose; CORS uses explicit origins (not `*`).

### S1 — Frontend dependencies pinned to `"latest"` 🟧 Medium (supply chain)

`frontend/package.json` declares `react`, `react-dom`, `vite`, `typescript`,
`@vitejs/plugin-react`, `lucide-react`, `@types/*` all as `"latest"`. This
violates NIST SSDF dependency-review intent (§8.1): builds are non-reproducible
and a fresh `npm install` can pull an unreviewed major version at any time.
There is no committed `package-lock.json` to pin transitively either.
**Recommendation:** pin to caret ranges of known-good versions and commit the
lockfile; make `npm ci` (not `npm install`) the build/CI command.

### S2 — Non-constant-time API key comparison 🟦 Low

`backend/app/core/security.py:23`

```python
if not configured_key or api_key != configured_key:
```

Plain `!=` on the secret is a timing side-channel. **Recommendation:**
`secrets.compare_digest(api_key or "", configured_key)` after the empty-key guard.
Minor in practice (key is long, network jitter dominates) but trivial to fix and
called for by the OWASP reference in §8.1.

### S3 — Container hardening before hosting 🟧 Watching (Low)

- `backend/Dockerfile` installs/runs as root with no `USER` directive — CIS Docker
  Benchmark (§8.1) wants a non-root runtime user before cloud deployment.
- `docker-compose.yml` ships an `adminer` DB admin UI. It is bound to
  `127.0.0.1:8080` (safe locally) but must never reach a hosted compose file.
- `pip install` is unhashed (acceptable for MVP; revisit with hashes for SSDF).

**Recommendation:** add a non-root `USER` to the backend image and keep
`adminer` in a `local`-only compose override before any hosted deployment.

### S4 — No authentication on read endpoints ℹ️ Info / 🟧 Watching

All `GET` endpoints are unauthenticated. Accepted for local single-user MVP and
already tracked in the Phase 3 review. Keep hosted/demo deployments read-only and
set `POORTOPOUR_ENVIRONMENT=production` so the non-local guards engage. Add auth
before exposing any non-local dashboard (§8 "before hosted MVP").

---

## 5. Trading-Safety Review

**Status:** 🟩 Passed for research-only MVP. No buy/sell/execution language, no
broker automation, no AI-driven decisions. Evidence is distinguished from
recommendation, statuses stay `Actionable/Watch/Avoid/Blocked`, and source /
freshness / partial-refresh state is surfaced.

- 🟧 **T1 (known):** yfinance is unofficial and not trading-grade; freshness and
  provider labels are present. Revisit a paid/official provider before trusting
  setups for alerts or paper trading (§6.4).
- 🟦 **T2 (known):** `RelativeStrengthLeaderDetector` is a price-leadership proxy,
  not benchmark-relative strength; this is documented in the class docstring and
  flagged as an MVP+ follow-up when SPY/QQQ bars enter scanner input.
- ✅ Stale price data (`> MAX_PRICE_DATA_AGE_DAYS = 7`) forces **Blocked** status,
  so the dashboard cannot present stale bars as fresh evidence (§6.2).
- ✅ `Actionable` requires confirmed setup, score ≥ 80, no caution flags, and
  realized R/R ≥ 2 — appropriately conservative (`status_rules._is_actionable`).
- ⚠️ Reinforces guideline §6.5: **no alerts/paper-trading/automation** until
  backtesting exists (still the highest-priority open risk, carried from Phase 3).

---

## 6. Tests & Process

- ✅ Backend test coverage is strong: 35 test files covering indicators, each
  detector, scoring, status rules, risk/reward, repositories, providers, manual
  scan security, and config — matching the §7 expectations for financial logic.
- 🟦 **P1:** No linter/formatter/type-checker is wired yet (ruff/black/eslint are
  referenced in §5.2 as "when added"); there is no CI gate and no frontend test
  runner. **Recommendation:** add `ruff` + `black --check` + `tsc -b` as a CI
  step, and introduce Vitest/Testing Library for the dashboard once `App.tsx` is
  split. Record the commands in README + trackers per §5.2.

---

## 7. Recommended Next Actions (priority order)

1. **S1** — Pin frontend deps + commit lockfile + `npm ci` in build. (Medium, cheap)
2. **C1** — Compute the indicator snapshot once per symbol and batch-load bars. (Medium)
3. **C2 / S2** — Bound `limit`; use `secrets.compare_digest`. (Low, quick wins)
4. **C3** — Decouple Blocked status from caution-flag text. (Low, trading-sensitive)
5. **S3** — Non-root backend image + local-only `adminer` before hosting. (Pre-hosting)
6. **P1** — Wire ruff/black/tsc into a CI gate. (Process)
7. Carry forward the standing **backtesting-before-automation** gate (§6.5).

None of the above blocks continued local MVP development. Items S1–S3 and S4 are
the gate before any hosted/MVP+ exposure.

---

## 8. Doc Drift Notes

- `10-ai-working-guidelines.md §3` links `/docs/00-project-plan.md`,
  `/docs/03-technical-architecture.md`, `/docs/09-decision-log.md` without the
  versioned suffixes that exist on disk (`-v0.3`, `-v0.2`, `-v1.1`). Minor; worth
  normalizing so the startup checklist resolves cleanly.
- This health check is filed under a new `/docs/reviews/` folder for cross-phase
  reviews (the existing `/docs/phases/...` pattern is per-phase). Consider adding a
  `reviews/` row to `docs/README.md` "Current Structure" if this becomes recurring.
