# PR Draft: Phase 2 Technical Scanner MVP

## Summary

Phase 2 expands PoorToPour from the Phase 1 data foundation into a deterministic technical scanner MVP.

This adds the first real provider adapter path, a combined S&P 500 plus Nasdaq 100 universe, scanner-ready indicators, setup detectors, explainable scoring, configurable risk/reward estimates, conservative candidate status rules, persisted technical scan output, and a focused frontend evidence panel for manual review.

## Branch

- `feature/phase_2_technical_scanner`

## Scope of Change

- Add Nasdaq 100 seed support and combined MVP universe seeding with duplicate symbol handling.
- Add Alpha Vantage daily OHLCV provider adapter, env-only API key config, and ingest command.
- Expand indicator snapshots with prior highs, 20/50/52-week context, ATR, range position, and distance fields.
- Add deterministic setup detectors:
  - breakout;
  - pullback continuation;
  - relative strength leader price-leadership proxy.
- Add explainable score breakdowns, caution flags, and configurable risk/reward assumptions.
- Add shared candidate status rules for `Actionable`, `Watch`, `Avoid`, and `Blocked`.
- Persist generated technical scans to existing `scan_runs` and `scan_candidates` tables.
- Add `run_technical_scan` command for local deterministic scan generation.
- Surface scanner evidence in the frontend: selected candidate details, risk context, reasons, caution flags, and score components.
- Add responsive UI polish for the Phase 2 dashboard view, including sidebar collapse and safer narrow/tall viewport behavior.

Implementation plan:

- `/docs/phases/phase-2-technical-scanner/phase-2-implementation-plan.md`

Review artifact:

- `/docs/phases/phase-2-technical-scanner/phase-2-code-security-trading-review.md`

## Verification Performed

```powershell
docker compose run --rm backend pytest
npm.cmd run build
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
```

Observed results:

- `docker compose run --rm backend pytest`: 69 passed.
- `npm.cmd run build`: passed.
- `docker compose config --quiet`: passed.
- `docker compose run --rm backend python -m pip check`: no broken requirements.
- `npm.cmd audit --audit-level=moderate`: 0 vulnerabilities.
- Secret scan found no real Alpha Vantage API key in tracked files; expected hits were placeholders, local dev database values, provider parameter names, docs, and test fixtures.

Manual/user-confirmed checks:

- `run_technical_scan --limit 10` persisted `technical_scan_20260527_044237_959bb63a` with 2 candidates.
- Frontend returned 200 locally and `/api/scans/latest` returned `Technical Scanner MVP`.
- Candidate row selection works.
- Sidebar collapse toggle works.
- Provider metric wrapping works.
- Summary cards/table overflow behavior works on the tall/narrow viewport.

## Review Outcomes

Phase 2 code/security/trading review completed on 2026-05-27.

Finding fixed during review:

- Stale price-data checks were declared in shared status rules but were not wired into detectors. Detectors now compute freshness from `latest_date`, add a stale-data caution flag, pass `price_data_fresh`, and regression tests confirm stale detected candidates are blocked.
- Coding-standards follow-up centralized ingest script symbol resolution, removed repeated risk/reward warning literals, and extracted relative-strength helper logic from `detect()`.
- Second guideline-based review added shared provider daily-bar validation so malformed Alpha Vantage/yfinance rows are skipped before persistence.

## Known Limitations

- No broker automation.
- No AI-generated trade decisions.
- No intraday scanner.
- No full backtesting UI.
- No notification-based alerts.
- Relative strength leader detection currently uses a deterministic price-leadership proxy; SPY/QQQ-relative returns remain follow-up work once benchmark bars are part of scanner input.
- Candidate chart visuals, signal markers, sector/theme scanner grid, and AI insight panels remain MVP+ or later.
- Alpha Vantage rate limits may constrain full-universe refresh cadence.
- Local Docker Compose database credentials are development-only and must be replaced before hosted deployment.

## Reviewer Checklist

- [ ] Confirm backend tests pass.
- [ ] Confirm frontend build passes.
- [ ] Confirm code/security/trading review has been read.
- [ ] Confirm scanner output remains deterministic, explainable, and research-only.
- [ ] Confirm no real API keys or production secrets are committed.
