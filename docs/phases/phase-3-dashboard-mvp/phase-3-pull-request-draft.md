# PR Draft: Phase 3 Dashboard MVP

## Summary

Phase 3 turns the deterministic scanner foundation into the first complete Dashboard MVP workflow.

The goal is to let the user view latest scan health, compare ranked candidates, inspect candidate chart evidence, review explanations and risk context, inspect scan history, and view safe dashboard settings.

Phase 3 should look recognizably close to the v0.2 mock render direction while preserving MVP scope.

## Branch

- `feature/phase_3_dashboard_mvp`

## Scope of Change

Planned scope:

- Align the app shell with the v0.2 dashboard direction while preserving MVP boundaries.
- Match the v0.2 mock render hierarchy for the Dashboard, Scan History, and Settings screens as closely as practical.
- Improve latest scan summary cards and data health states.
- Upgrade the candidate ranking table with practical filtering/sorting and visible caution context.
- Add candidate detail route/page.
- Add backend chart/candidate evidence API payloads.
- Render candidate chart evidence with candles, volume, SMA 20/50/200, RSI, and optional research estimate overlays.
- Add deterministic explanation, score breakdown, caution flag, and risk/reward panels.
- Add Scan History page.
- Add Settings page with read-only system/admin config display, safe user preferences, and no secret exposure.
- Wire manual scan action with loading/success/error states, defaulting local/dev scan data to yfinance while keeping hosted behavior constrained.
- Add responsive, accessibility, and empty/error state polish.

Implementation plan:

- `/docs/phases/phase-3-dashboard-mvp/phase-3-implementation-plan.md`

Review artifact:

- `/docs/phases/phase-3-dashboard-mvp/phase-3-code-security-trading-review.md`

## Verification Performed

To be completed before PR:

```powershell
docker compose run --rm backend pytest
npm.cmd run build
docker compose config --quiet
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
```

Manual checks to complete:

- Dashboard loads latest scan summary.
- Dashboard first viewport is visually close to `Mock_UI_PoorToPour_01_MainScreen_v0.2.png` within MVP scope.
- Candidate table filters/sorts and opens detail.
- Candidate detail chart renders nonblank candles, volume, moving averages, and RSI.
- Scan History route loads previous runs and follows `Mock_UI_PoorToPour_02_ScanHistory_v0.2.png` direction.
- Settings route follows `Mock_UI_PoorToPour_03_Settings_v0.2.png` direction and does not expose secrets.
- Manual scan flow shows loading/error/success clearly and labels active data source/freshness.
- Tall/narrow 1080x2560 layout remains usable.
- Hosted/demo mode does not expose secrets or imply live trading.

## Review Outcomes

To be completed in:

- `/docs/phases/phase-3-dashboard-mvp/phase-3-code-security-trading-review.md`

## Known Limitations

Expected MVP boundaries:

- No broker automation.
- No AI-generated trade decisions.
- No watchlist persistence.
- No alert notifications.
- No sector/theme scanner grid.
- No full backtesting UI.
- No intraday scanner.
- yfinance-backed MVP scan data is not trading-grade and must be labelled with source/freshness.
- Chart signal taxonomy, detected-signal panels, watchlist, sector scanner, and AI insight panels remain MVP+ unless trivial and explicitly approved.

## Reviewer Checklist

- [ ] Confirm backend tests pass.
- [ ] Confirm frontend build passes.
- [ ] Confirm dashboard UX matches MVP scope.
- [ ] Confirm candidate chart evidence is deterministic and backend-derived.
- [ ] Confirm copy remains research-only, not trade-instructional.
- [ ] Confirm no secrets are exposed in frontend, logs, docs, or committed files.
- [ ] Confirm Phase 3 code/security/trading/UX review has been read.
