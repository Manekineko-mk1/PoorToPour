# Phase 3 Implementation Plan: Dashboard MVP

**Project:** PoorToPour
**Phase:** Phase 3 - Dashboard MVP
**Status:** 🟨 Active
**Branch:** `feature/phase_3_dashboard_mvp`
**Last updated:** 2026-06-04

---

## 1. Purpose

This plan breaks Phase 3 into small implementation steps.

The goal is to turn persisted deterministic scanner output into the first complete user-facing dashboard MVP:

- view latest scan health;
- compare ranked candidates;
- inspect candidate chart evidence;
- review deterministic explanations, score breakdown, cautions, and risk/reward;
- review scan history;
- view or adjust basic settings safely.

This plan preserves MVP scope:

- no broker automation;
- no AI trade decisions;
- no alert notifications;
- no sector/theme scanner;
- no watchlist persistence;
- no full backtesting UI;
- no intraday scanner.

Phase 3 should use the v0.2 mock renders as the visual target wherever they do not conflict with MVP scope:

- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_01_MainScreen_v0.2.png`
- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_02_ScanHistory_v0.2.png`
- `/docs/references/Mock_UI_Renders/Mock_UI_PoorToPour_03_Settings_v0.2.png`

The implementation does not need to be pixel-perfect, but the first impression, layout hierarchy, spacing density, dark terminal style, header/sidebar/main structure, champagne branding, summary cards, ranked table, chart evidence area, and detail panels should feel recognizably close to the mocks.

Visible MVP+ panels from the mock may be represented as disabled, labelled, or omitted placeholders only when that helps preserve the intended layout. They should not create functional scope expansion.

Resolved implementation choices:

- Chart library: use TradingView Lightweight Charts.
- Candidate detail: use a real route for MVP traceability; the dashboard may still keep a selected-candidate preview panel.
- Settings: start with read-only system/admin scan options plus safe user preferences. MVP is single-user, but the UI should avoid implying all users can edit system-level provider or scan settings.
- Scan data source: use yfinance pragmatically for MVP scan data because Alpha Vantage's free API-call limit is too restrictive for S&P 500 plus Nasdaq 100 iteration. Keep Alpha Vantage as an implemented provider adapter and a future stable-source candidate after scanner/strategy value is proven.
- Hosted manual scan: local/dev can run yfinance-backed scans; hosted manual scans must be rate-limit-aware, secret-safe, and may be disabled or constrained if data-source behavior is unsuitable.
- Chart risk lines: show entry/invalidation/target lines if simple from existing risk/reward payload; otherwise defer to MVP+.

---

## 2. Implementation Sequence

### Step 1: Scope, Routes, and App Shell

Outcome:

- Phase 3 scope is explicit.
- The frontend shell follows the v0.2 mock direction within MVP boundaries.

Tasks:

- Confirm primary MVP routes: Dashboard, Candidate Detail, Scan History, Settings.
- Keep MVP+ navigation labels disabled or clearly marked if they remain visible.
- Align shell toward the v0.2 mock's three-part structure: compact header, left sidebar, and main content.
- Preserve sidebar collapse behavior and tall/narrow viewport safety.
- Keep the champagne icon/favicon work.
- Use the v0.2 dark theme, card density, typography scale, and status colors as the baseline visual language.

Exit criteria:

- `P3-A` is `✅ Done`.
- `P3-B` is ready for implementation or complete.
- Dashboard shell does not imply MVP+ features are available.
- Dashboard first viewport looks recognizably close to `Mock_UI_PoorToPour_01_MainScreen_v0.2.png` within MVP scope.

---

### Step 2: Latest Scan Dashboard

Outcome:

- Dashboard Home clearly summarizes the latest scan.

Tasks:

- Normalize frontend data mapping for latest scan metadata.
- Show scan status, provider, universe, symbols processed, candidates found, latest scan time, data date, and warning count.
- Show global failed/partial/stale states prominently.
- Keep research-only wording visible.
- Avoid crowding the top area on narrow/tall screens.
- Follow the MainScreen v0.2 placement pattern for header controls, scan summary cards, and dashboard status.

Exit criteria:

- Latest scan summary can be understood without opening candidate detail.
- Empty, loading, failed, and partial states are visible.

---

### Step 3: Candidate Ranking Table

Outcome:

- Candidate comparison becomes the central dashboard surface.

Tasks:

- Display rank, ticker, company, setup, status, score, price, relative volume, risk/reward, caution count, and last/data date where available.
- Sort by score descending by default.
- Add setup and status filters.
- Add sortable score and risk/reward columns if simple.
- Keep horizontal overflow usable without clipping important text.
- Clicking a row opens or updates candidate detail.
- Match the MainScreen v0.2 table density and status-badge style as closely as practical.

Exit criteria:

- User can compare candidates quickly.
- Table behavior remains usable with more than the six mock candidates.

---

### Step 4: Backend Chart and Candidate Evidence APIs

Outcome:

- Frontend can render candidate evidence without reimplementing trading logic.

Tasks:

- Add API endpoint for candidate detail by scan/candidate or symbol.
- Add API endpoint for chart bars and indicators for a selected symbol.
- Include daily OHLCV, volume, SMA 20/50/200, RSI, and risk/reward overlay values where available.
- Ensure responses include data date/freshness metadata.
- Return clear 404/empty states for missing symbols or missing bars.

Exit criteria:

- Backend tests cover normal, missing, and insufficient-history responses.
- Frontend does not recompute scanner indicators.

---

### Step 5: Candidate Detail Page

Outcome:

- One ticker can be deeply inspected.

Tasks:

- Add a dedicated candidate detail route or route-compatible view.
- Use `Mock_UI_PoorToPour_01_CandidateDetail.png` as the visual guide for the MVP detail page.
- Show a compact identity strip: ticker, company, exchange badge, setup badge, status, score, and dashboard/back navigation.
- Do not use top hero cards for price, relative volume, RSI, or data date; preserve chart real estate.
- Show chart evidence as the primary center panel: candlesticks, volume, SMA 20/50/200, RSI, and optional research estimate lines.
- Add chart toolbar controls for MVP review: timeframe slicing, simple display options, and chart-panel fullscreen.
- Show setup explanation, reasons, cautions, score components, and rule-derived labels in right-side research panels.
- Show risk/reward estimate with entry, invalidation, target, risk/share, and risk/reward ratio in a color-coded right-side trade plan panel.
- Show company context available from symbol metadata, including exchange/listing context where available.
- Keep Company Overview and News & Events as disabled/placeholder tabs unless Phase 3 explicitly expands their data scope.

Exit criteria:

- User can understand why the ticker appeared and what the chart evidence shows.
- Copy clearly states risk/reward is a research estimate.

---

### Step 6: Scan History

Outcome:

- Previous scan runs are inspectable.

Tasks:

- Add `GET /api/scans` or equivalent if missing.
- Add Scan History page with run table.
- Show status, started/completed time, scan type, universe, data date, candidate count, and warnings/errors where available.
- Allow selecting/opening a prior scan and seeing its candidates.
- Use `Mock_UI_PoorToPour_02_ScanHistory_v0.2.png` as the visual guide for layout, summary cards, run table, and selected scan detail.

Exit criteria:

- User can trace a candidate back to a scan run.
- Prior scan output is not confused with the latest scan.

---

### Step 7: Settings MVP

Outcome:

- Basic configuration is visible and safe.

Tasks:

- Add Settings page.
- Show environment, provider name, universe, enabled setup families, max candidates, minimum price, minimum volume, and AI disabled status where available.
- Do not expose API keys, database URLs, or secrets.
- Keep system/admin scan options read-only first.
- Support only safe user preferences if editing is simple, with validation and explicit save.
- Keep broker and AI trade-decision controls absent from MVP.
- Use `Mock_UI_PoorToPour_03_Settings_v0.2.png` as the visual guide while keeping MVP+ controls disabled, labelled, or omitted.

Exit criteria:

- User can understand current scan configuration without opening source files.
- No secret values appear in frontend output.

---

### Step 8: Manual Scan Flow

Outcome:

- Manual scan can refresh market data, persist updated bars, and then trigger the deterministic scanner safely.

Tasks:

- Add backend route or frontend flow for manual scan if missing.
- Refresh yfinance daily bars before the default local/dev manual scan.
- Persist refreshed bars before running the deterministic scanner.
- Keep an explicit persisted-only scan mode for debugging and fallback.
- Return refresh metadata: symbols requested, symbols refreshed, symbols failed, bars persisted, provider, and period.
- Show loading, success, failure, and partial-success states.
- Refresh latest scan after completion.
- Default local/dev manual scans to the yfinance-backed data path while preserving the provider abstraction.
- Keep Alpha Vantage available as an adapter, but avoid making it the default full-universe MVP scan source because the free call limit is too restrictive.
- Respect provider mode, hosted mode, rate-limit constraints, and secret handling.
- Disable or constrain hosted manual scans if the active data source cannot safely support them.

Exit criteria:

- Manual scan is useful for local development and clear in hosted demo mode.
- The default local/dev manual scan does not silently scan stale persisted bars.
- Failures are visible and do not leave stale success UI behind.
- Data source and freshness are visible enough that yfinance-backed results are not mistaken for paid/trading-grade provider output.

---

### Step 9: UX Polish, Accessibility, and Responsive QA

Outcome:

- Dashboard MVP feels coherent and usable.

Tasks:

- Verify desktop, tall/narrow 1080x2560, and smaller responsive layouts.
- Compare desktop Dashboard, Scan History, and Settings against the v0.2 mocks for visual closeness before Phase 3 closeout.
- Ensure status uses text plus color, not color alone.
- Check keyboard focus for navigation, table rows, filters, and buttons.
- Keep text from overflowing buttons/cards.
- Keep palette functional and avoid one-note color drift.
- Make empty/error/loading states polished.

Exit criteria:

- UI is stable enough for a demo and internal MVP review.
- Known visual compromises are documented.

---

### Step 10: Review and Closeout

Outcome:

- Phase 3 is ready to merge.

Required review:

- code review;
- security review;
- trading-safety review;
- UX/accessibility review;
- test review;
- documentation review.

Required commands before closeout:

```powershell
docker compose config --quiet
docker compose run --rm backend pytest
npm.cmd run build
docker compose run --rm backend python -m pip check
npm.cmd audit --audit-level=moderate
rg -n "(API_KEY|apikey|api key|SECRET|TOKEN|PASSWORD|PRIVATE|BEGIN RSA|BEGIN OPENSSH|DATABASE_URL)" -S --glob '!.env' --glob '!.env.*' --glob '!frontend/node_modules/**' --glob '!frontend/dist/**' --glob '!backend/.venv/**' .
```

Exit criteria:

- `phase-3-code-security-trading-review.md` is completed.
- `phase-3-pull-request-draft.md` is updated.
- Phase 3 tracker statuses reflect actual completion.

---

## 3. Build Order Recommendation

Recommended first coding order:

1. App shell and route structure.
2. Latest scan summary and improved candidate table.
3. Backend chart/candidate evidence endpoints.
4. Candidate detail page and chart rendering.
5. Scan History page.
6. Settings page.
7. Manual scan flow with yfinance refresh-before-scan.
8. Mock-alignment pass for Dashboard, Scan History, and Settings.
9. UX/accessibility/responsive polish.
10. Tests, review, and PR draft.

This order keeps the product usable early while avoiding chart/UI work that has no stable data contract.

---

## 4. Known Risks

| Risk | Mitigation |
| --- | --- |
| Chart work expands into MVP+ signal dashboard | Ship basic evidence first: candles, volume, SMA, RSI, and simple risk lines only if available |
| Mock fidelity causes scope creep | Match layout and visual treatment first; keep non-MVP panels disabled, labelled, or omitted |
| React duplicates backend indicator logic | Backend owns indicators and chart-ready values |
| Manual scan causes expensive provider calls | Make provider mode visible and rate-limit hosted/manual scans |
| yfinance is convenient but not trading-grade | Use it as a cost-constrained MVP data source, label provider/freshness clearly, and preserve the path to Alpha Vantage or another stable source |
| UI suggests trade instruction | Keep research-only copy, caution flags, and explanation panels prominent |
| Settings exposes secrets | Return display-safe config only; never serialize keys or URLs |
| Narrow/tall layouts regress | Test against the user's 1080x2560 case before closeout |

---

## 5. Status Legend

| Status | Meaning |
| --- | --- |
| ⬜ Not Started | Work has not begun |
| 🟨 In Progress | Work is actively underway |
| ✅ Done | Work is complete |
| ⛔ Blocked | Work cannot continue until a blocker is resolved |
