import {
  Activity,
  AlertTriangle,
  ArrowLeft,
  BarChart3,
  Bell,
  CalendarDays,
  CheckCircle2,
  Clock,
  Cloud,
  Database,
  FileText,
  Maximize2,
  Grid2X2,
  History,
  SlidersHorizontal,
  PanelLeftClose,
  PanelLeftOpen,
  Play,
  Rocket,
  Search,
  Settings,
  Star,
  TrendingUp,
} from "lucide-react";
import {
  CandlestickSeries,
  createChart,
  HistogramSeries,
  LineSeries,
  LineStyle,
} from "lightweight-charts";
import type { CandlestickData, HistogramData, IChartApi, ISeriesApi, LineData, Time } from "lightweight-charts";
import type { Dispatch, PointerEvent as ReactPointerEvent, ReactNode, SetStateAction } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import {
  Candidate,
  DisplaySettings,
  LatestScan,
  SymbolChartPayload,
  fetchDisplaySettings,
  fetchLatestScan,
  fetchScanRuns,
  fetchSymbolChart,
  runManualScan,
} from "./api";

type SortKey = "rank" | "score" | "riskReward";
type SortDirection = "asc" | "desc";
type NoticeTone = "success" | "info" | "warning" | "error";
type DashboardState = "loading" | "error" | "empty" | "filtered-empty" | "ready";
type ChartTimeframe = "1D" | "5D" | "1M" | "3M" | "6M" | "YTD" | "1Y" | "2Y" | "5Y";

type CandidateRoute = {
  symbol: string;
  setupSlug: string;
};

type RouteCandidateContext = {
  candidate: Candidate;
  scan: LatestScan | null;
};

function StatusPill({ status }: { status: Candidate["status"] }) {
  return <span className={`status status-${status.toLowerCase()}`}>{status}</span>;
}

function formatRelativeVolume(value: number | null) {
  return value == null ? "--" : `${value.toFixed(2)}x`;
}

function formatPrice(value: number | null) {
  return value == null ? "--" : `$${value.toFixed(2)}`;
}

function formatProvider(value: string | undefined) {
  return value?.replace("TechnicalScanner", "Technical Scanner") ?? "Mock";
}

function formatLabel(value: string) {
  return value.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function numericEntries(value: Record<string, unknown> | null | undefined) {
  return Object.entries(value ?? {})
    .filter(([, entry]) => typeof entry === "number")
    .sort(([, a], [, b]) => Math.abs(Number(b)) - Math.abs(Number(a)));
}

function riskRewardDetails(candidate: Candidate) {
  const riskReward = candidate.score_breakdown?.risk_reward;
  return riskReward && typeof riskReward === "object" ? riskReward as Record<string, unknown> : null;
}

function App() {
  const [scan, setScan] = useState<LatestScan | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [setupFilter, setSetupFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [sortKey, setSortKey] = useState<SortKey>("score");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [path, setPath] = useState(() => window.location.pathname);
  const [routeCandidateContext, setRouteCandidateContext] = useState<RouteCandidateContext | null>(null);
  const [manualScanState, setManualScanState] = useState<"idle" | "running" | "success" | "error">("idle");
  const [manualScanMessage, setManualScanMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchLatestScan()
      .then((latestScan) => {
        setScan(latestScan);
        setError(null);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  useEffect(() => {
    function handlePopState() {
      setPath(window.location.pathname);
    }

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const candidates = scan?.candidates ?? [];
  const routeCandidate = parseCandidateRoute(path);
  const carriedRouteCandidate = routeCandidateContext && routeCandidateMatches(routeCandidateContext.candidate, routeCandidate)
    ? routeCandidateContext
    : null;
  const detailCandidate = routeCandidate
    ? candidates.find((candidate) => (
      candidate.symbol.toUpperCase() === routeCandidate.symbol
      && slugify(candidate.setup) === routeCandidate.setupSlug
    )) ?? carriedRouteCandidate?.candidate ?? null
    : null;
  const detailScan = carriedRouteCandidate?.scan ?? scan;
  const setupOptions = useMemo(() => uniqueOptions(candidates.map((candidate) => candidate.setup)), [candidates]);
  const statusOptions = useMemo(() => uniqueOptions(candidates.map((candidate) => candidate.status)), [candidates]);
  const displayedCandidates = useMemo(
    () => sortCandidates(
      candidates.filter((candidate) => setupFilter === "all" || candidate.setup === setupFilter)
        .filter((candidate) => statusFilter === "all" || candidate.status === statusFilter),
      sortKey,
      sortDirection,
    ),
    [candidates, setupFilter, statusFilter, sortDirection, sortKey],
  );
  const selected =
    displayedCandidates.find((candidate) => candidateKey(candidate) === selectedKey)
    ?? displayedCandidates[0]
    ?? candidates.find((candidate) => candidateKey(candidate) === selectedKey)
    ?? candidates[0];
  const riskDetails = selected ? riskRewardDetails(selected) : null;
  const scoreEntries = selected ? numericEntries(selected.score_breakdown) : [];
  const visibleScanWarning = getVisibleScanWarning(scan);
  const freshness = getFreshnessState(scan);
  const health = getDataHealth(scan, error, visibleScanWarning, freshness);
  const isDetailRoute = routeCandidate !== null;
  const isScanHistoryRoute = path === "/scans";
  const isSettingsRoute = path === "/settings";
  const isDashboardRoute = !isDetailRoute && !isScanHistoryRoute && !isSettingsRoute;
  const dashboardState = getDashboardState(scan, error, displayedCandidates.length, candidates.length);
  const showManualScanNotice = manualScanMessage && (manualScanState !== "success" || isDashboardRoute);

  function navigateTo(nextPath: string) {
    window.history.pushState({}, "", nextPath);
    setPath(nextPath);
  }

  function openCandidateDetail(candidate: Candidate, sourceScan: LatestScan | null = scan) {
    setSelectedKey(candidateKey(candidate));
    setRouteCandidateContext({ candidate, scan: sourceScan });
    navigateTo(candidatePath(candidate));
  }

  function toggleSort(nextSortKey: SortKey) {
    if (sortKey === nextSortKey) {
      setSortDirection((direction) => direction === "asc" ? "desc" : "asc");
      return;
    }

    setSortKey(nextSortKey);
    setSortDirection(nextSortKey === "rank" ? "asc" : "desc");
  }

  function handleManualScan() {
    setManualScanState("running");
    setManualScanMessage("Refreshing market data and running deterministic scan...");
    runManualScan()
      .then((nextScan) => {
        setScan(nextScan);
        setError(null);
        setSelectedKey(null);
        setManualScanState("success");
        setManualScanMessage(manualScanSuccessMessage(nextScan));
      })
      .catch((err: Error) => {
        setManualScanState("error");
        setManualScanMessage(err.message);
      });
  }

  return (
    <main className={`app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""} ${isDetailRoute ? "detail-route" : ""}`}>
      <header className="global-header">
        <div className="brand">
          <span className="brand-icon" aria-hidden="true">
            <img src="/poortopour-champagne-icon.png" alt="" />
          </span>
          <div className="brand-copy">
            <h1>PoorToPour</h1>
            <p>From broke to pouring champagne.</p>
          </div>
          <span className="environment-pill">Local</span>
        </div>

        <div className="header-status">
          <HeaderStatus icon={<Clock size={18} />} label="Last Successful Scan" value={formatTimestamp(scan?.completed_at ?? scan?.started_at)} />
          <HeaderStatus icon={<CalendarDays size={18} />} label="Data Date" value={scan?.data_date ?? "--"} />
          <HeaderStatus icon={<Cloud size={18} />} label="Provider Status" value={`${formatProvider(scan?.provider)} - ${health.label}`} accent={health.tone === "healthy"} />
        </div>

        <div className="header-actions">
          <button disabled={manualScanState === "running"} onClick={handleManualScan} type="button">
            <Play size={16} /> {manualScanState === "running" ? "Running Scan" : "Run Manual Scan"}
          </button>
        </div>
      </header>

      <aside className="sidebar">
        <button
          aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="sidebar-toggle"
          onClick={() => setSidebarCollapsed((collapsed) => !collapsed)}
          title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          type="button"
        >
          {sidebarCollapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
        </button>
        <nav>
          <a className={isDashboardRoute ? "active" : ""} href="/" onClick={(event) => { event.preventDefault(); navigateTo("/"); }}><Grid2X2 size={18} /> <span>Dashboard</span></a>
          <a className={isScanHistoryRoute ? "active" : ""} href="/scans" onClick={(event) => { event.preventDefault(); navigateTo("/scans"); }}><History size={18} /> <span>Scan History</span></a>
          <a className="muted"><Star size={18} /> <span>Watchlist</span><em>42</em></a>
          <a className="muted"><TrendingUp size={18} /> <span>Backtesting</span><em>Soon</em></a>
          <a className="muted"><Bell size={18} /> <span>Alerts</span><em>7</em></a>
          <a className="muted"><FileText size={18} /> <span>Reports</span><em>Soon</em></a>
          <a className={isSettingsRoute ? "active" : ""} href="/settings" onClick={(event) => { event.preventDefault(); navigateTo("/settings"); }}><Settings size={18} /> <span>Settings</span></a>
        </nav>

        <section className="scanner-status-card">
          <div>
            <span>Scanner Status</span>
            <strong><CheckCircle2 size={13} /> Real-time</strong>
          </div>
          <div>
            <span>Next scan in</span>
            <strong>04:17:38</strong>
          </div>
          <div className="progress-track"><span /></div>
          <div>
            <span>Auto scan (Daily)</span>
            <strong>On</strong>
          </div>
        </section>

        <section className="sidebar-note">
          <Rocket size={22} />
          <strong>Keep scanning.</strong>
          <span>Stay disciplined.</span>
          <b>Focus compound.</b>
        </section>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Local MVP</span>
            <h2>{pageTitle(isDetailRoute, isScanHistoryRoute, isSettingsRoute)}</h2>
          </div>
          <div className="topbar-actions">
            {isDetailRoute && (
              <button className="secondary-button" onClick={() => navigateTo("/")} type="button">
                <ArrowLeft size={16} /> Dashboard
              </button>
            )}
            <div className="search"><Search size={16} /> Search tickers, companies, or press Ctrl+K</div>
          </div>
        </header>

        {error && <StatusNotice tone="error" title="Latest scan unavailable" message={error} />}
        {showManualScanNotice && (
          <StatusNotice
            tone={manualScanState === "error" ? "error" : manualScanState === "running" ? "info" : "success"}
            title={manualScanState === "running" ? "Manual scan running" : manualScanState === "error" ? "Manual scan failed" : "Manual scan complete"}
            message={manualScanMessage}
          />
        )}
        {visibleScanWarning && !error && isDashboardRoute && (
          <StatusNotice tone="warning" title="Partial scan context" message={visibleScanWarning} />
        )}
        {freshness.isStale && !error && isDashboardRoute && (
          <StatusNotice tone="warning" title="Stale data" message={freshness.detail} />
        )}

        {isDetailRoute ? (
          <CandidateDetailPage
            candidate={detailCandidate}
            onBack={() => navigateTo("/")}
            requestedRoute={routeCandidate}
            scan={detailScan}
          />
        ) : isScanHistoryRoute ? (
          <ScanHistoryPage
            latestScan={scan}
            onOpenCandidate={openCandidateDetail}
          />
        ) : isSettingsRoute ? (
          <SettingsPage latestScan={scan} />
        ) : (
          <>
            <section className="summary-grid">
              <MetricCard icon={<Activity />} label="Scan Status" value={formatStatus(scan?.status)} detail={formatTimestamp(scan?.completed_at ?? scan?.started_at)} tone={scanStatusTone(scan, error)} />
              <MetricCard icon={<Database />} label="Scan Type" value={formatScanType(scan?.scan_type)} detail={`Provider: ${formatProvider(scan?.provider)}`} />
              <MetricCard icon={<Settings />} label="Universe" value={scan?.universe ?? "--"} detail="Active scan scope" />
              <MetricCard icon={<Grid2X2 />} label="Symbols Processed" value={formatCount(scan?.symbols_processed)} detail={scan?.symbols_processed ? "Coverage recorded" : "Waiting for scan"} />
              <MetricCard icon={<TrendingUp />} label="Candidates Found" value={formatCount(scan?.candidates_found)} detail={candidateCountDetail(scan)} tone={scan && scan.candidates_found === 0 ? "neutral" : "healthy"} />
              <MetricCard icon={<CheckCircle2 />} label="Data Health" value={health.label} detail={health.detail} tone={health.tone} />
            </section>

            <section className="content-grid">
              <section className="panel table-panel">
            <div className="panel-header">
              <div>
                <h3>Top Candidates</h3>
                {visibleScanWarning && <p>{visibleScanWarning}</p>}
              </div>
              <span>{scan?.data_date ?? ""}</span>
            </div>
            <div className="table-toolbar">
              <label>
                <span>Setup</span>
                <select value={setupFilter} onChange={(event) => setSetupFilter(event.target.value)}>
                  <option value="all">All setups</option>
                  {setupOptions.map((setup) => <option key={setup} value={setup}>{setup}</option>)}
                </select>
              </label>
              <label>
                <span>Status</span>
                <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
                  <option value="all">All statuses</option>
                  {statusOptions.map((status) => <option key={status} value={status}>{status}</option>)}
                </select>
              </label>
              <div className="table-count">
                Showing {displayedCandidates.length.toLocaleString()} of {candidates.length.toLocaleString()}
              </div>
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th><SortButton active={sortKey === "rank"} direction={sortDirection} onClick={() => toggleSort("rank")}>Rank</SortButton></th>
                    <th>Ticker</th>
                    <th>Company</th>
                    <th>Setup</th>
                    <th>Status</th>
                    <th><SortButton active={sortKey === "score"} direction={sortDirection} onClick={() => toggleSort("score")}>Score</SortButton></th>
                    <th>Price</th>
                    <th>Rel Vol</th>
                    <th>RSI</th>
                    <th><SortButton active={sortKey === "riskReward"} direction={sortDirection} onClick={() => toggleSort("riskReward")}>R/R</SortButton></th>
                    <th>Cautions</th>
                    <th>Last Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {displayedCandidates.length ? (
                    displayedCandidates.map((candidate) => (
                      <tr
                        className={selected && candidateKey(candidate) === candidateKey(selected) ? "selected-row" : ""}
                        key={candidateKey(candidate)}
                        onClick={() => openCandidateDetail(candidate)}
                        onKeyDown={(event) => {
                          if (event.key === "Enter" || event.key === " ") {
                            event.preventDefault();
                            openCandidateDetail(candidate);
                          }
                        }}
                        role="button"
                        tabIndex={0}
                      >
                        <td>{candidate.rank}</td>
                        <td className="ticker">{candidate.symbol}</td>
                        <td>{candidate.company_name}</td>
                        <td>{candidate.setup}</td>
                        <td><StatusPill status={candidate.status} /></td>
                        <td className="score">{candidate.score}</td>
                        <td>{formatPrice(candidate.price)}</td>
                        <td>{formatRelativeVolume(candidate.relative_volume)}</td>
                        <td>{formatNumber(candidate.rsi)}</td>
                        <td>{candidate.risk_reward ?? "--"}</td>
                        <td><CautionSummary flags={candidate.caution_flags} /></td>
                        <td>{formatTimestamp(candidate.last_updated)}</td>
                      </tr>
                    ))
                  ) : (
                    <tr className="empty-row">
                      <td colSpan={12}>
                        <TableEmptyState state={dashboardState} />
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
              </section>

              <aside className="panel insight-panel">
            <h3>Selected Candidate</h3>
            {selected ? (
              <>
                <div className="selected-symbol">{selected.symbol}</div>
                <p>{selected.company_name}</p>
                <button className="secondary-button detail-link-button" onClick={() => openCandidateDetail(selected)} type="button">
                  Open Detail
                </button>
                <dl className="candidate-facts">
                  <dt>Setup</dt>
                  <dd>{selected.setup}</dd>
                  <dt>Status</dt>
                  <dd><StatusPill status={selected.status} /></dd>
                  <dt>Price</dt>
                  <dd>{formatPrice(selected.price)}</dd>
                  <dt>Score</dt>
                  <dd>{selected.score}</dd>
                  <dt>Risk / Reward</dt>
                  <dd>{selected.risk_reward ?? "Not estimated yet"}</dd>
                </dl>

                {riskDetails && (
                  <div className="evidence-block">
                    <h4>Risk Context</h4>
                    <div className="risk-grid">
                      <span>Entry</span><strong>{formatRiskNumber(riskDetails.entry)}</strong>
                      <span>Invalidation</span><strong>{formatRiskNumber(riskDetails.invalidation)}</strong>
                      <span>Target</span><strong>{formatRiskNumber(riskDetails.target)}</strong>
                      <span>Risk / Share</span><strong>{formatRiskNumber(riskDetails.risk_per_share)}</strong>
                    </div>
                  </div>
                )}

                <EvidenceList title="Reasons" items={selected.reasons ?? []} empty="No reasons recorded" />
                <EvidenceList title="Caution Flags" items={selected.caution_flags} empty="No caution flags" />

                <div className="evidence-block">
                  <h4>Score Components</h4>
                  {scoreEntries.length ? (
                    <ul className="component-list">
                      {scoreEntries.map(([key, value]) => (
                        <li key={key}>
                          <span>{formatLabel(key)}</span>
                          <strong>{Number(value)}</strong>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No score breakdown recorded</p>
                  )}
                </div>
              </>
            ) : (
              <DashboardEmptyAside state={dashboardState} />
            )}
              </aside>
            </section>
          </>
        )}
      </section>
    </main>
  );
}

export default App;

function HeaderStatus({
  icon,
  label,
  value,
  accent = false,
}: {
  icon: ReactNode;
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <div className="header-status-item">
      {icon}
      <div>
        <span>{label}</span>
        <strong className={accent ? "accent" : ""}>{value}</strong>
      </div>
    </div>
  );
}

function MetricCard({
  icon,
  label,
  value,
  detail,
  tone = "neutral",
}: {
  icon: ReactNode;
  label: string;
  value: string;
  detail: string;
  tone?: "healthy" | "warning" | "error" | "neutral";
}) {
  return (
    <div className={`panel metric metric-${tone}`}>
      {icon}
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function StatusNotice({
  message,
  title,
  tone,
}: {
  message: string;
  title: string;
  tone: NoticeTone;
}) {
  const icon = tone === "error" || tone === "warning"
    ? <AlertTriangle size={18} />
    : <CheckCircle2 size={18} />;

  return (
    <section className={`panel status-notice status-notice-${tone}`}>
      {icon}
      <div>
        <strong>{title}</strong>
        <span>{message}</span>
      </div>
    </section>
  );
}

function TableEmptyState({ state }: { state: DashboardState }) {
  const copy = dashboardStateCopy(state);

  return (
    <div className="table-empty-state">
      <strong>{copy.title}</strong>
      <span>{copy.detail}</span>
    </div>
  );
}

function DashboardEmptyAside({ state }: { state: DashboardState }) {
  const copy = dashboardStateCopy(state);

  return (
    <div className="aside-empty-state">
      <AlertTriangle size={20} />
      <strong>{copy.title}</strong>
      <span>{copy.detail}</span>
    </div>
  );
}

function ScanHistoryPage({
  latestScan,
  onOpenCandidate,
}: {
  latestScan: LatestScan | null;
  onOpenCandidate: (candidate: Candidate, sourceScan: LatestScan | null) => void;
}) {
  const [scanRuns, setScanRuns] = useState<LatestScan[]>([]);
  const [selectedScanId, setSelectedScanId] = useState<string | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);

  useEffect(() => {
    let isCurrent = true;
    fetchScanRuns()
      .then((runs) => {
        if (!isCurrent) {
          return;
        }

        setScanRuns(runs);
        setSelectedScanId((current) => current ?? runs[0]?.scan_id ?? null);
      })
      .catch((err: Error) => {
        if (isCurrent) {
          setHistoryError(err.message);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  const selectedRun =
    scanRuns.find((run) => run.scan_id === selectedScanId)
    ?? scanRuns[0]
    ?? latestScan;
  const selectedCandidates = selectedRun?.candidates ?? [];
  const selectedWarning = getVisibleScanWarning(selectedRun ?? null);
  const selectedFreshness = getFreshnessState(selectedRun ?? null);
  const selectedHealth = getDataHealth(selectedRun ?? null, historyError, selectedWarning, selectedFreshness);

  return (
    <section className="scan-history-page">
      {historyError && <StatusNotice tone="error" title="Scan history unavailable" message={historyError} />}
      {selectedWarning && !historyError && <StatusNotice tone="warning" title="Selected scan warning" message={selectedWarning} />}
      {selectedFreshness.isStale && !historyError && <StatusNotice tone="warning" title="Selected scan may be stale" message={selectedFreshness.detail} />}

      <section className="summary-grid scan-history-summary">
        <MetricCard icon={<History />} label="Runs Loaded" value={formatCount(scanRuns.length)} detail="Recent persisted scans" />
        <MetricCard icon={<CheckCircle2 />} label="Selected Status" value={formatStatus(selectedRun?.status)} detail={formatTimestamp(selectedRun?.completed_at ?? selectedRun?.started_at)} tone={selectedHealth.tone} />
        <MetricCard icon={<CalendarDays />} label="Selected Data Date" value={selectedRun?.data_date ?? "--"} detail={selectedRun?.scan_type ?? "No run selected"} />
        <MetricCard icon={<TrendingUp />} label="Candidates" value={formatCount(selectedRun?.candidates_found)} detail="Found in selected run" />
      </section>

      <section className="scan-history-grid">
        <section className="panel run-list-panel">
          <div className="panel-header">
            <div>
              <h3>Scan Runs</h3>
              <p>Recent persisted scanner runs</p>
            </div>
          </div>
          <div className="run-list">
            {scanRuns.length ? (
              scanRuns.map((run) => (
                <button
                  className={`run-list-item ${run.scan_id === selectedRun?.scan_id ? "active" : ""}`}
                  key={run.scan_id}
                  onClick={() => setSelectedScanId(run.scan_id)}
                  type="button"
                >
                  <span>
                    <strong>{formatTimestamp(run.completed_at ?? run.started_at)}</strong>
                    <small>{run.scan_type}</small>
                  </span>
                  <span>
                    <StatusText status={run.status} />
                    <small>{run.candidates_found} candidates</small>
                  </span>
                </button>
              ))
            ) : (
              <p className="empty-copy">No scan runs loaded yet.</p>
            )}
          </div>
        </section>

        <section className="panel scan-run-detail-panel">
          <div className="panel-header">
            <div>
              <h3>Selected Run</h3>
              <p>{selectedRun?.scan_id ?? "No scan selected"}</p>
            </div>
            <span>{selectedRun?.data_date ?? ""}</span>
          </div>

          {selectedRun && (
            <dl className="scan-run-facts">
              <dt>Provider</dt>
              <dd>{formatProvider(selectedRun.provider)}</dd>
              <dt>Universe</dt>
              <dd>{selectedRun.universe}</dd>
              <dt>Symbols Processed</dt>
              <dd>{selectedRun.symbols_processed.toLocaleString()}</dd>
              <dt>Status</dt>
              <dd>{formatStatus(selectedRun.status)}</dd>
            </dl>
          )}

          <div className="table-scroll scan-history-candidates">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Ticker</th>
                  <th>Company</th>
                  <th>Setup</th>
                  <th>Status</th>
                  <th>Score</th>
                  <th>R/R</th>
                  <th>Cautions</th>
                </tr>
              </thead>
              <tbody>
                {selectedCandidates.length ? (
                  selectedCandidates.map((candidate) => (
                    <tr
                      key={candidateKey(candidate)}
                      onClick={() => onOpenCandidate(candidate, selectedRun)}
                      onKeyDown={(event) => {
                        if (event.key === "Enter" || event.key === " ") {
                          event.preventDefault();
                          onOpenCandidate(candidate, selectedRun);
                        }
                      }}
                      role="button"
                      tabIndex={0}
                    >
                      <td>{candidate.rank}</td>
                      <td className="ticker">{candidate.symbol}</td>
                      <td>{candidate.company_name}</td>
                      <td>{candidate.setup}</td>
                      <td><StatusPill status={candidate.status} /></td>
                      <td className="score">{candidate.score}</td>
                      <td>{candidate.risk_reward ?? "--"}</td>
                      <td><CautionSummary flags={candidate.caution_flags} /></td>
                    </tr>
                  ))
                ) : (
                  <tr className="empty-row">
                    <td colSpan={8}>No candidates recorded for this scan.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </section>
    </section>
  );
}

function SettingsPage({ latestScan }: { latestScan: LatestScan | null }) {
  const [settings, setSettings] = useState<DisplaySettings | null>(null);
  const [settingsError, setSettingsError] = useState<string | null>(null);

  useEffect(() => {
    let isCurrent = true;
    fetchDisplaySettings()
      .then((payload) => {
        if (isCurrent) {
          setSettings(payload);
        }
      })
      .catch((err: Error) => {
        if (isCurrent) {
          setSettingsError(err.message);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  if (settingsError) {
    return <section className="panel warning"><AlertTriangle /> {settingsError}</section>;
  }

  if (!settings) {
    return (
      <section className="panel detail-empty-state">
        <h3>Loading settings...</h3>
        <p>Loading display-safe configuration.</p>
      </section>
    );
  }

  return (
    <section className="settings-page">
      <section className="summary-grid settings-summary">
        <MetricCard icon={<Settings />} label="Environment" value={settings.environment} detail="Runtime mode" />
        <MetricCard icon={<Database />} label="Provider" value={formatProvider(settings.provider)} detail={settings.data_source_note} />
        <MetricCard icon={<Grid2X2 />} label="Universe" value={settings.universe} detail={latestScan?.universe ?? "From persisted scan data"} />
        <MetricCard icon={<CheckCircle2 />} label="Secrets" value="Redacted" detail="API keys and DB URLs are not displayed" tone="healthy" />
      </section>

      <section className="settings-grid">
        <section className="panel settings-panel">
          <h3>Scanner Configuration</h3>
          <dl className="settings-list">
            <dt>Schedule</dt>
            <dd>{settings.scanner.schedule}</dd>
            <dt>Risk ATR Buffer</dt>
            <dd>{settings.scanner.risk_reward_atr_buffer_multiplier}</dd>
            <dt>Target Multiple</dt>
            <dd>{settings.scanner.risk_reward_target_multiple}</dd>
            <dt>Latest Scan Type</dt>
            <dd>{latestScan?.scan_type ?? "--"}</dd>
          </dl>
        </section>

        <section className="panel settings-panel">
          <h3>Enabled Setups</h3>
          <div className="settings-chip-list">
            {settings.enabled_setups.map((setup) => <span key={setup}>{setup}</span>)}
          </div>
        </section>

        <section className="panel settings-panel">
          <h3>Safe User Preferences</h3>
          <SettingsDictionary values={settings.safe_user_preferences} />
        </section>

        <section className="panel settings-panel">
          <h3>Admin/System Options</h3>
          <SettingsDictionary values={settings.admin_controls} />
        </section>

        <section className="panel settings-panel">
          <h3>AI Controls</h3>
          <SettingsDictionary values={settings.ai} />
        </section>

        <section className="panel settings-panel">
          <h3>Secret Safety</h3>
          <dl className="settings-list">
            <dt>API Keys Visible</dt>
            <dd>{settings.secrets.api_keys_visible ? "Yes" : "No"}</dd>
            <dt>Database URLs Visible</dt>
            <dd>{settings.secrets.database_urls_visible ? "Yes" : "No"}</dd>
          </dl>
        </section>
      </section>
    </section>
  );
}

function CandidateDetailPage({
  candidate,
  onBack,
  requestedRoute,
  scan,
}: {
  candidate: Candidate | null;
  onBack: () => void;
  requestedRoute: CandidateRoute | null;
  scan: LatestScan | null;
}) {
  const [chartPayload, setChartPayload] = useState<SymbolChartPayload | null>(null);
  const [chartError, setChartError] = useState<string | null>(null);

  useEffect(() => {
    if (!candidate) {
      setChartPayload(null);
      return;
    }

    let isCurrent = true;
    setChartError(null);
    setChartPayload(null);
    fetchSymbolChart(candidate.symbol, candidate.setup, scan?.scan_id)
      .then((payload) => {
        if (isCurrent) {
          setChartPayload(payload);
        }
      })
      .catch((err: Error) => {
        if (isCurrent) {
          setChartError(err.message);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [candidate, scan?.scan_id]);

  if (!scan) {
    return (
      <section className="panel detail-empty-state">
        <h3>Loading candidate detail...</h3>
        <p>Waiting for latest scan data.</p>
      </section>
    );
  }

  if (!candidate) {
    return (
      <section className="panel detail-empty-state">
        <h3>Candidate not found</h3>
        <p>
          {requestedRoute
            ? `${requestedRoute.symbol} is not present in the latest scan output.`
            : "No candidate route was selected."}
        </p>
        <button className="secondary-button" onClick={onBack} type="button">
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
      </section>
    );
  }

  const riskDetails = riskRewardDetails(candidate);
  const scoreEntries = numericEntries(candidate.score_breakdown);
  const chartOverlay = chartPayload?.candidate?.risk_reward_overlay ?? null;
  const tradePlan = {
    entry: chartOverlay?.entry ?? riskDetails?.entry,
    invalidation: chartOverlay?.invalidation ?? riskDetails?.invalidation,
    target: chartOverlay?.target ?? riskDetails?.target,
    riskPerShare: chartOverlay?.risk_per_share ?? riskDetails?.risk_per_share,
  };

  return (
    <section className="candidate-detail">
      <section className="candidate-detail-header">
        <div className="candidate-identity">
          <button className="text-button" onClick={onBack} type="button">
            <ArrowLeft size={16} /> Back to Dashboard
          </button>
          <div className="candidate-title-line">
            <div className="selected-symbol">{candidate.symbol}</div>
            <p>{candidate.company_name}</p>
            <span className="exchange-badge">{chartPayload?.exchange ?? "Listed"}</span>
          </div>
        </div>
        <dl className="candidate-header-stats">
          <div><dt>Setup</dt><dd><span className={`setup-badge setup-${slugify(candidate.setup)}`}>{candidate.setup}</span></dd></div>
          <div><dt>Status</dt><dd><StatusPill status={candidate.status} /></dd></div>
          <div className="score-stat"><dt>Score</dt><dd>{candidate.score}</dd></div>
        </dl>
      </section>

      <section className="detail-grid">
        <CandidateChart payload={chartPayload} error={chartError} symbol={candidate.symbol} />

        <aside className="detail-side-panel research-context-panel">
          <section className="side-card research-summary-card">
            <div className="side-card-header">
              <h3>Research Context</h3>
              <StatusPill status={candidate.status} />
            </div>
            <dl className="side-facts">
              <dt>Setup</dt>
              <dd>{candidate.setup}</dd>
              <dt>Risk / Reward</dt>
              <dd>{candidate.risk_reward ?? "Not estimated yet"}</dd>
              <dt>Universe</dt>
              <dd>{scan.universe}</dd>
              <dt>Data Date</dt>
              <dd>{scan.data_date ?? "--"}</dd>
            </dl>
          </section>

          <section className="side-card trade-plan-card">
            <h3>Trade Plan</h3>
            {riskDetails ? (
              <div className="trade-plan-grid">
                <span>Entry</span><strong className="trade-entry">{formatRiskNumber(tradePlan.entry)}</strong>
                <span>Stop / Invalidation</span><strong className="trade-stop">{formatRiskNumber(tradePlan.invalidation)}</strong>
                <span>Target</span><strong className="trade-target">{formatRiskNumber(tradePlan.target)}</strong>
                <span>Risk / Share</span><strong>{formatRiskNumber(tradePlan.riskPerShare)}</strong>
                <span>Risk / Reward</span><strong>{candidate.risk_reward ?? "--"}</strong>
              </div>
            ) : (
              <p className="research-note">No risk/reward estimate is available for this candidate.</p>
            )}
          </section>

          <section className="side-card signal-card">
            <h3>Key Reasons / Signals</h3>
            <SignalList items={candidate.reasons ?? []} empty="No reasons recorded" tone="positive" />
          </section>

          <section className="side-card caution-card">
            <h3><AlertTriangle size={18} /> Validation / Caution</h3>
            <SignalList items={candidate.caution_flags} empty="No caution flags" tone="caution" />
          </section>

          <section className="side-card score-card">
            <h3>Score Components</h3>
            {scoreEntries.length ? (
              <ul className="component-list">
                {scoreEntries.map(([key, value]) => (
                  <li key={key}>
                    <span>{formatLabel(key)}</span>
                    <strong>{Number(value)}</strong>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No score breakdown recorded</p>
            )}
          </section>
        </aside>
      </section>
    </section>
  );
}

function CandidateChart({
  error,
  payload,
  symbol,
}: {
  error: string | null;
  payload: SymbolChartPayload | null;
  symbol: string;
}) {
  const chartPanelRef = useRef<HTMLElement | null>(null);
  const priceChartRef = useRef<HTMLDivElement | null>(null);
  const rsiChartRef = useRef<HTMLDivElement | null>(null);
  const [rsiHeight, setRsiHeight] = useState(108);
  const [timeframe, setTimeframe] = useState<ChartTimeframe>("1Y");
  const [showChartOptions, setShowChartOptions] = useState(false);
  const [showRsiPanel, setShowRsiPanel] = useState(true);
  const [showVolumePanel, setShowVolumePanel] = useState(true);
  const visibleBars = useMemo(
    () => sliceBarsByTimeframe(payload?.bars ?? [], timeframe),
    [payload?.bars, timeframe],
  );

  useEffect(() => {
    if (!visibleBars.length || !priceChartRef.current || !rsiChartRef.current) {
      return;
    }

    const priceContainer = priceChartRef.current;
    const rsiContainer = rsiChartRef.current;
    const priceChart = createChart(priceContainer, {
      autoSize: true,
      grid: {
        horzLines: { color: "rgba(147, 163, 181, 0.12)" },
        vertLines: { color: "rgba(147, 163, 181, 0.08)" },
      },
      layout: {
        background: { color: "transparent" },
        textColor: "#93a3b5",
      },
      rightPriceScale: {
        borderColor: "#1d3042",
        scaleMargins: { top: 0.08, bottom: 0.24 },
      },
      timeScale: {
        borderColor: "#1d3042",
        timeVisible: false,
      },
    });
    const rsiChart = createChart(rsiContainer, {
      autoSize: true,
      grid: {
        horzLines: { color: "rgba(147, 163, 181, 0.12)" },
        vertLines: { color: "rgba(147, 163, 181, 0.08)" },
      },
      layout: {
        background: { color: "transparent" },
        textColor: "#93a3b5",
      },
      rightPriceScale: {
        borderColor: "#1d3042",
      },
      timeScale: {
        borderColor: "#1d3042",
      },
    });

    const candles = priceChart.addSeries(CandlestickSeries, {
      borderVisible: false,
      downColor: "#ef5350",
      upColor: "#48df63",
      wickDownColor: "#ef5350",
      wickUpColor: "#48df63",
    });
    candles.setData(visibleBars.map(toCandleData));

    if (showVolumePanel) {
      const volume = priceChart.addSeries(HistogramSeries, {
        priceFormat: { type: "volume" },
        priceScaleId: "",
      });
      volume.priceScale().applyOptions({ scaleMargins: { top: 0.78, bottom: 0 } });
      volume.setData(visibleBars.map(toVolumeData));
    }

    addLineSeries(priceChart, visibleBars, "sma_20", "#f2a900", "SMA 20");
    addLineSeries(priceChart, visibleBars, "sma_50", "#5b62ff", "SMA 50");
    addLineSeries(priceChart, visibleBars, "sma_200", "#93a3b5", "SMA 200");
    addRiskPriceLines(candles, payload?.candidate?.risk_reward_overlay ?? null);

    const rsi = rsiChart.addSeries(LineSeries, {
      color: "#f2a900",
      lineWidth: 2,
      priceLineVisible: false,
    });
    rsi.setData(visibleBars.filter((bar) => bar.rsi_14 !== null).map((bar) => ({
      time: bar.date as Time,
      value: Number(bar.rsi_14),
    })));
    rsi.createPriceLine({ color: "#48df63", lineStyle: LineStyle.Dashed, lineWidth: 1, price: 70, title: "70" });
    rsi.createPriceLine({ color: "#ef5350", lineStyle: LineStyle.Dashed, lineWidth: 1, price: 30, title: "30" });

    priceChart.timeScale().fitContent();
    rsiChart.timeScale().fitContent();

    return () => {
      priceChart.remove();
      rsiChart.remove();
    };
  }, [payload, showVolumePanel, visibleBars]);

  function toggleFullscreen() {
    if (document.fullscreenElement) {
      void document.exitFullscreen();
      return;
    }

    void chartPanelRef.current?.requestFullscreen();
  }

  return (
    <section className="panel chart-panel" ref={chartPanelRef}>
      <div className="chart-toolbar">
        <div className="chart-tabs">
          <button className="active" type="button"><TrendingUp size={16} /> Chart Evidence</button>
          <button disabled type="button"><Database size={16} /> Company Overview</button>
          <button disabled type="button"><FileText size={16} /> News & Events</button>
        </div>
        <div className="chart-actions">
          {(["1D", "5D", "1M", "3M", "6M", "YTD", "1Y", "2Y", "5Y"] as ChartTimeframe[]).map((value) => (
            <button
              className={timeframe === value ? "active" : ""}
              key={value}
              onClick={() => setTimeframe(value)}
              type="button"
            >
              {value}
            </button>
          ))}
          <button
            aria-expanded={showChartOptions}
            aria-label="Chart options"
            className={showChartOptions ? "active" : ""}
            onClick={() => setShowChartOptions((isOpen) => !isOpen)}
            title="Chart options"
            type="button"
          >
            <SlidersHorizontal size={16} />
          </button>
          <button
            aria-label={document.fullscreenElement ? "Exit chart fullscreen" : "Open chart fullscreen"}
            onClick={toggleFullscreen}
            title={document.fullscreenElement ? "Exit chart fullscreen" : "Open chart fullscreen"}
            type="button"
          >
            <Maximize2 size={16} />
          </button>
        </div>
      </div>
      {showChartOptions && (
        <div className="chart-options-panel">
          <label>
            <input checked={showVolumePanel} onChange={(event) => setShowVolumePanel(event.target.checked)} type="checkbox" />
            Volume
          </label>
          <label>
            <input checked={showRsiPanel} onChange={(event) => setShowRsiPanel(event.target.checked)} type="checkbox" />
            RSI panel
          </label>
          <span>{visibleBars.length.toLocaleString()} bars visible</span>
        </div>
      )}
      <div className="chart-header">
        <div>
          <h3>{symbol} Chart Evidence</h3>
          <p>Candles, volume, SMA 20/50/200, RSI 14, and research estimate lines.</p>
        </div>
        <span>{payload?.data_date ?? "Loading"}</span>
      </div>

      {error && <div className="chart-state"><AlertTriangle size={18} /> {error}</div>}
      {!error && !payload && <div className="chart-state"><BarChart3 size={18} /> Loading chart evidence...</div>}
      {!error && payload && !payload.bars.length && <div className="chart-state"><AlertTriangle size={18} /> No chart bars available.</div>}

      <div className="chart-surface" aria-label={`${symbol} candlestick chart with moving averages and volume`} ref={priceChartRef} />
      {showRsiPanel ? (
        <>
          <button
            aria-label="Resize RSI chart"
            className="chart-resize-handle"
            onPointerDown={(event) => startRsiResize(event, setRsiHeight)}
            title="Drag to resize RSI chart"
            type="button"
          />
          <div
            className="rsi-surface"
            aria-label={`${symbol} RSI 14 chart`}
            ref={rsiChartRef}
            style={{ height: rsiHeight }}
          />
        </>
      ) : (
        <div className="rsi-surface-hidden" ref={rsiChartRef} />
      )}

      {payload?.warnings.length ? (
        <div className="chart-warning-list">
          {payload.warnings.map((warning) => <span key={warning}>{warning}</span>)}
        </div>
      ) : null}

      <div className="chart-legend">
        <span><i className="legend-sma-20" /> SMA 20</span>
        <span><i className="legend-sma-50" /> SMA 50</span>
        <span><i className="legend-sma-200" /> SMA 200</span>
        <span><i className="legend-volume" /> Volume</span>
        <span>Charting by TradingView Lightweight Charts</span>
      </div>
    </section>
  );
}

function SortButton({
  active,
  children,
  direction,
  onClick,
}: {
  active: boolean;
  children: ReactNode;
  direction: SortDirection;
  onClick: () => void;
}) {
  return (
    <button className={`sort-button ${active ? "active" : ""}`} onClick={onClick} type="button">
      {children}
      <span>{active ? (direction === "asc" ? "ASC" : "DESC") : "SORT"}</span>
    </button>
  );
}

function CautionSummary({ flags }: { flags: string[] }) {
  if (!flags.length) {
    return <span className="caution-empty">--</span>;
  }

  return <span className="caution-badge" title={flags.join("; ")}>{flags.length} flag{flags.length === 1 ? "" : "s"}</span>;
}

function StatusText({ status }: { status: string }) {
  return <strong className={`run-status run-status-${status.toLowerCase()}`}>{formatStatus(status)}</strong>;
}

function SettingsDictionary({ values }: { values: Record<string, string> }) {
  return (
    <dl className="settings-list">
      {Object.entries(values).map(([key, value]) => (
        <div key={key}>
          <dt>{formatLabel(key)}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function toCandleData(bar: SymbolChartPayload["bars"][number]): CandlestickData<Time> {
  return {
    time: bar.date,
    open: bar.open,
    high: bar.high,
    low: bar.low,
    close: bar.close,
  };
}

function toVolumeData(bar: SymbolChartPayload["bars"][number]): HistogramData<Time> {
  return {
    time: bar.date,
    value: bar.volume,
    color: bar.close >= bar.open ? "rgba(72, 223, 99, 0.36)" : "rgba(239, 83, 80, 0.36)",
  };
}

function sliceBarsByTimeframe(
  bars: SymbolChartPayload["bars"],
  timeframe: ChartTimeframe,
): SymbolChartPayload["bars"] {
  if (!bars.length) {
    return [];
  }

  if (timeframe === "1D") {
    return bars.slice(-1);
  }

  if (timeframe === "5D") {
    return bars.slice(-5);
  }

  const latestDate = new Date(`${bars[bars.length - 1].date}T00:00:00`);
  const startDate = new Date(latestDate);

  if (timeframe === "YTD") {
    startDate.setMonth(0, 1);
  } else {
    startDate.setDate(latestDate.getDate() - timeframeDays(timeframe));
  }

  return bars.filter((bar) => new Date(`${bar.date}T00:00:00`) >= startDate);
}

function timeframeDays(timeframe: Exclude<ChartTimeframe, "1D" | "5D" | "YTD">) {
  const daysByTimeframe = {
    "1M": 31,
    "3M": 93,
    "6M": 186,
    "1Y": 366,
    "2Y": 366 * 2,
    "5Y": 366 * 5,
  };
  return daysByTimeframe[timeframe];
}

function addLineSeries(
  chart: IChartApi,
  bars: SymbolChartPayload["bars"],
  field: "sma_20" | "sma_50" | "sma_200",
  color: string,
  title: string,
) {
  const data: LineData<Time>[] = bars
    .filter((bar) => bar[field] !== null)
    .map((bar) => ({ time: bar.date, value: Number(bar[field]) }));
  if (!data.length) {
    return;
  }

  const series = chart.addSeries(LineSeries, {
    color,
    lineWidth: 2,
    priceLineVisible: false,
    title,
  });
  series.setData(data);
}

function addRiskPriceLines(
  candles: ISeriesApi<"Candlestick", Time>,
  overlay: NonNullable<SymbolChartPayload["candidate"]>["risk_reward_overlay"] | null,
) {
  if (!overlay) {
    return;
  }

  addRiskPriceLine(candles, overlay.entry, "#f2a900", "Entry");
  addRiskPriceLine(candles, overlay.invalidation, "#ef5350", "Invalidation");
  addRiskPriceLine(candles, overlay.target, "#48df63", "Target");
}

function addRiskPriceLine(
  candles: ISeriesApi<"Candlestick", Time>,
  price: number | null,
  color: string,
  title: string,
) {
  if (price === null) {
    return;
  }

  candles.createPriceLine({
    color,
    lineStyle: LineStyle.Dashed,
    lineWidth: 1,
    price,
    title,
  });
}

function startRsiResize(
  event: ReactPointerEvent<HTMLButtonElement>,
  setRsiHeight: Dispatch<SetStateAction<number>>,
) {
  event.preventDefault();
  const startY = event.clientY;
  const rsiPanel = event.currentTarget.nextElementSibling;
  const startHeight = rsiPanel instanceof HTMLElement
    ? rsiPanel.getBoundingClientRect().height
    : 108;

  function handlePointerMove(moveEvent: PointerEvent) {
    const nextHeight = startHeight - (moveEvent.clientY - startY);
    setRsiHeight(clamp(nextHeight, 80, 220));
  }

  function handlePointerUp() {
    window.removeEventListener("pointermove", handlePointerMove);
    window.removeEventListener("pointerup", handlePointerUp);
  }

  window.addEventListener("pointermove", handlePointerMove);
  window.addEventListener("pointerup", handlePointerUp);
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

function EvidenceList({ title, items, empty }: { title: string; items: string[]; empty: string }) {
  return (
    <div className="evidence-block">
      <h4>{title}</h4>
      <EvidenceListItems items={items} empty={empty} />
    </div>
  );
}

function EvidenceListItems({ items, empty }: { items: string[]; empty: string }) {
  return items.length ? (
    <ul>
      {items.map((item) => <li key={item}>{item}</li>)}
    </ul>
  ) : (
    <p>{empty}</p>
  );
}

function SignalList({
  empty,
  items,
  tone,
}: {
  empty: string;
  items: string[];
  tone: "positive" | "caution";
}) {
  if (!items.length) {
    return <p className="research-note">{empty}</p>;
  }

  return (
    <ul className={`signal-list signal-list-${tone}`}>
      {items.map((item) => (
        <li key={item}>
          {tone === "positive" ? <CheckCircle2 size={15} /> : <AlertTriangle size={15} />}
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

function candidateKey(candidate: Candidate) {
  return `${candidate.symbol}:${candidate.setup}`;
}

function candidatePath(candidate: Candidate) {
  return `/candidates/${candidate.symbol.toUpperCase()}/${slugify(candidate.setup)}`;
}

function routeCandidateMatches(candidate: Candidate, route: CandidateRoute | null) {
  return Boolean(
    route
    && candidate.symbol.toUpperCase() === route.symbol
    && slugify(candidate.setup) === route.setupSlug,
  );
}

function parseCandidateRoute(path: string): CandidateRoute | null {
  const match = path.match(/^\/candidates\/([^/]+)\/([^/]+)$/);
  if (!match) {
    return null;
  }

  return {
    symbol: decodeURIComponent(match[1]).toUpperCase(),
    setupSlug: decodeURIComponent(match[2]),
  };
}

function slugify(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function formatRiskNumber(value: unknown) {
  return typeof value === "number" ? value.toFixed(2) : "--";
}

function formatNumber(value: number | null) {
  return value == null ? "--" : value.toFixed(1);
}

function formatTimestamp(value: string | null | undefined) {
  if (!value) {
    return "Loading";
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(parsed);
}

function formatStatus(value: string | undefined) {
  return value ? formatLabel(value) : "Loading";
}

function formatScanType(value: string | undefined) {
  return value ? formatLabel(value) : "--";
}

function formatCount(value: number | null | undefined) {
  return value == null ? "--" : value.toLocaleString();
}

function uniqueOptions(values: string[]) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
}

function sortCandidates(candidates: Candidate[], sortKey: SortKey, direction: SortDirection) {
  const sorted = [...candidates].sort((a, b) => {
    if (sortKey === "rank") {
      return a.rank - b.rank;
    }

    if (sortKey === "riskReward") {
      return parseRiskReward(a.risk_reward) - parseRiskReward(b.risk_reward);
    }

    return a.score - b.score;
  });

  return direction === "asc" ? sorted : sorted.reverse();
}

function parseRiskReward(value: string | null) {
  if (!value) {
    return Number.NEGATIVE_INFINITY;
  }

  const [firstNumber] = value.match(/\d+(\.\d+)?/) ?? [];
  return firstNumber ? Number(firstNumber) : Number.NEGATIVE_INFINITY;
}

function pageTitle(isDetailRoute: boolean, isScanHistoryRoute: boolean, isSettingsRoute: boolean) {
  if (isDetailRoute) {
    return "Candidate Detail";
  }

  if (isScanHistoryRoute) {
    return "Scan History";
  }

  if (isSettingsRoute) {
    return "Settings";
  }

  return "Dashboard";
}

function isResearchOnlyWarning(value: string | null | undefined) {
  return value?.toLowerCase().includes("research-only deterministic scanner output") ?? false;
}

function getVisibleScanWarning(scan: LatestScan | null): string | null {
  if (!scan?.warning || isResearchOnlyWarning(scan.warning)) {
    return null;
  }

  return scan.warning;
}

function getDashboardState(
  scan: LatestScan | null,
  error: string | null,
  displayedCandidateCount: number,
  candidateCount: number,
): DashboardState {
  if (error) {
    return "error";
  }

  if (!scan) {
    return "loading";
  }

  if (candidateCount === 0) {
    return "empty";
  }

  if (displayedCandidateCount === 0) {
    return "filtered-empty";
  }

  return "ready";
}

function dashboardStateCopy(state: DashboardState) {
  if (state === "error") {
    return {
      title: "Latest scan unavailable",
      detail: "Check the backend service or run a manual scan after the API is healthy.",
    };
  }

  if (state === "loading") {
    return {
      title: "Loading latest scan",
      detail: "Waiting for persisted scanner output.",
    };
  }

  if (state === "empty") {
    return {
      title: "No candidates in this scan",
      detail: "The scanner ran successfully, but no symbols passed the current deterministic filters.",
    };
  }

  if (state === "filtered-empty") {
    return {
      title: "No candidates match the current filters",
      detail: "Adjust setup or status filters to review the full scan output.",
    };
  }

  return {
    title: "Candidate selected",
    detail: "Review deterministic evidence before making any decision.",
  };
}

function scanStatusTone(scan: LatestScan | null, error: string | null): "healthy" | "warning" | "error" | "neutral" {
  if (error) {
    return "error";
  }

  if (!scan) {
    return "neutral";
  }

  const normalizedStatus = scan.status.toLowerCase();
  if (normalizedStatus.includes("fail")) {
    return "error";
  }

  if (normalizedStatus.includes("partial")) {
    return "warning";
  }

  return "healthy";
}

function candidateCountDetail(scan: LatestScan | null) {
  if (!scan) {
    return "Waiting for scan";
  }

  if (scan.candidates_found === 0) {
    return "No symbols passed filters";
  }

  return "Pass filters";
}

function manualScanSuccessMessage(scan: LatestScan) {
  const refresh = scan.market_data_refresh;
  if (!refresh) {
    return `Manual scan completed: ${scan.candidates_found} candidates found.`;
  }

  const failedCopy = refresh.symbols_failed
    ? ` ${refresh.symbols_failed} symbols failed refresh.`
    : "";
  return (
    `Market data refreshed for ${refresh.symbols_refreshed}/${refresh.symbols_requested} symbols; `
    + `${refresh.bars_persisted.toLocaleString()} bars persisted. `
    + `Manual scan completed: ${scan.candidates_found} candidates found.`
    + failedCopy
  );
}

function getFreshnessState(scan: LatestScan | null): { detail: string; isStale: boolean } {
  if (!scan) {
    return { detail: "Waiting for scan data", isStale: false };
  }

  const staleReasons: string[] = [];
  const dataDateAge = getAgeInDays(scan.data_date);
  const completedAge = getAgeInHours(scan.completed_at ?? scan.started_at);

  if (dataDateAge !== null && dataDateAge > 5) {
    staleReasons.push(`data date is ${dataDateAge} days old`);
  }

  if (completedAge !== null && completedAge > 36) {
    staleReasons.push(`latest scan completed ${Math.floor(completedAge)} hours ago`);
  }

  if (!staleReasons.length) {
    return { detail: "Latest scan freshness looks acceptable", isStale: false };
  }

  return {
    detail: `Review freshness before acting: ${staleReasons.join("; ")}.`,
    isStale: true,
  };
}

function getAgeInDays(value: string | null | undefined) {
  const timestamp = parseDateMs(value);
  if (timestamp === null) {
    return null;
  }

  return Math.floor((Date.now() - timestamp) / 86_400_000);
}

function getAgeInHours(value: string | null | undefined) {
  const timestamp = parseDateMs(value);
  if (timestamp === null) {
    return null;
  }

  return (Date.now() - timestamp) / 3_600_000;
}

function parseDateMs(value: string | null | undefined) {
  if (!value) {
    return null;
  }

  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed.getTime();
}

function getDataHealth(
  scan: LatestScan | null,
  error: string | null,
  visibleScanWarning: string | null,
  freshness: { detail: string; isStale: boolean },
): {
  label: string;
  detail: string;
  tone: "healthy" | "warning" | "error" | "neutral";
} {
  if (error) {
    return { label: "Failed", detail: "Latest scan unavailable", tone: "error" };
  }

  if (!scan) {
    return { label: "Loading", detail: "Waiting for scan data", tone: "neutral" };
  }

  const normalizedStatus = scan.status.toLowerCase();
  if (normalizedStatus.includes("fail")) {
    return { label: "Failed", detail: "Review scan errors", tone: "error" };
  }

  if (normalizedStatus.includes("partial") || visibleScanWarning) {
    return { label: "Warning", detail: visibleScanWarning ?? "Partial scan output", tone: "warning" };
  }

  if (freshness.isStale) {
    return { label: "Stale", detail: freshness.detail, tone: "warning" };
  }

  return { label: "Healthy", detail: "All systems operational", tone: "healthy" };
}
