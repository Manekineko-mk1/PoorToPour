import {
  Activity,
  AlertTriangle,
  Bell,
  CalendarDays,
  CheckCircle2,
  Clock,
  Cloud,
  Database,
  FileText,
  Grid2X2,
  History,
  PanelLeftClose,
  PanelLeftOpen,
  Play,
  Rocket,
  Search,
  Settings,
  Star,
  TrendingUp,
} from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";

import { Candidate, LatestScan, fetchLatestScan } from "./api";

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

  useEffect(() => {
    fetchLatestScan().then(setScan).catch((err: Error) => setError(err.message));
  }, []);

  const candidates = scan?.candidates ?? [];
  const selected = candidates.find((candidate) => candidateKey(candidate) === selectedKey) ?? candidates[0];
  const riskDetails = selected ? riskRewardDetails(selected) : null;
  const scoreEntries = selected ? numericEntries(selected.score_breakdown) : [];
  const health = getDataHealth(scan, error);

  return (
    <main className={`app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""}`}>
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
          <button><Play size={16} /> Run Manual Scan</button>
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
          <a className="active"><Grid2X2 size={18} /> <span>Dashboard</span></a>
          <a><History size={18} /> <span>Scan History</span></a>
          <a className="muted"><Star size={18} /> <span>Watchlist</span><em>42</em></a>
          <a className="muted"><TrendingUp size={18} /> <span>Backtesting</span><em>Soon</em></a>
          <a className="muted"><Bell size={18} /> <span>Alerts</span><em>7</em></a>
          <a className="muted"><FileText size={18} /> <span>Reports</span><em>Soon</em></a>
          <a><Settings size={18} /> <span>Settings</span></a>
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
            <h2>Dashboard</h2>
          </div>
          <div className="topbar-actions">
            <div className="search"><Search size={16} /> Search tickers, companies, or press Ctrl+K</div>
          </div>
        </header>

        {error && <section className="panel warning"><AlertTriangle /> {error}</section>}
        {scan?.warning && !error && <section className="panel warning"><AlertTriangle /> {scan.warning}</section>}

        <section className="summary-grid">
          <MetricCard icon={<Activity />} label="Scan Status" value={formatStatus(scan?.status)} detail={formatTimestamp(scan?.completed_at ?? scan?.started_at)} />
          <MetricCard icon={<Database />} label="Scan Type" value={formatScanType(scan?.scan_type)} detail={`Provider: ${formatProvider(scan?.provider)}`} />
          <MetricCard icon={<Settings />} label="Universe" value={scan?.universe ?? "--"} detail="Active scan scope" />
          <MetricCard icon={<Grid2X2 />} label="Symbols Processed" value={formatCount(scan?.symbols_processed)} detail={scan?.symbols_processed ? "Coverage recorded" : "Waiting for scan"} />
          <MetricCard icon={<TrendingUp />} label="Candidates Found" value={formatCount(scan?.candidates_found)} detail="Pass filters" />
          <MetricCard icon={<CheckCircle2 />} label="Data Health" value={health.label} detail={health.detail} tone={health.tone} />
        </section>

        <section className="content-grid">
          <section className="panel table-panel">
            <div className="panel-header">
              <div>
                <h3>Top Candidates</h3>
                <p>{scan?.warning ?? "Research-only deterministic scanner output. Not a trading recommendation."}</p>
              </div>
              <span>{scan?.data_date ?? ""}</span>
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Ticker</th>
                    <th>Company</th>
                    <th>Setup</th>
                    <th>Status</th>
                    <th>Score</th>
                    <th>Rel Vol</th>
                    <th>R/R</th>
                  </tr>
                </thead>
                <tbody>
                  {candidates.map((candidate) => (
                    <tr
                      className={selected && candidateKey(candidate) === candidateKey(selected) ? "selected-row" : ""}
                      key={candidateKey(candidate)}
                      onClick={() => setSelectedKey(candidateKey(candidate))}
                    >
                      <td>{candidate.rank}</td>
                      <td className="ticker">{candidate.symbol}</td>
                      <td>{candidate.company_name}</td>
                      <td>{candidate.setup}</td>
                      <td><StatusPill status={candidate.status} /></td>
                      <td className="score">{candidate.score}</td>
                      <td>{formatRelativeVolume(candidate.relative_volume)}</td>
                      <td>{candidate.risk_reward ?? "--"}</td>
                    </tr>
                  ))}
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
              <p>Loading candidate evidence...</p>
            )}
          </aside>
        </section>
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

function EvidenceList({ title, items, empty }: { title: string; items: string[]; empty: string }) {
  return (
    <div className="evidence-block">
      <h4>{title}</h4>
      {items.length ? (
        <ul>
          {items.map((item) => <li key={item}>{item}</li>)}
        </ul>
      ) : (
        <p>{empty}</p>
      )}
    </div>
  );
}

function candidateKey(candidate: Candidate) {
  return `${candidate.symbol}:${candidate.setup}`;
}

function formatRiskNumber(value: unknown) {
  return typeof value === "number" ? value.toFixed(2) : "--";
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

function getDataHealth(scan: LatestScan | null, error: string | null): {
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

  if (normalizedStatus.includes("partial") || scan.warning) {
    return { label: "Warning", detail: scan.warning ?? "Partial scan output", tone: "warning" };
  }

  return { label: "Healthy", detail: "All systems operational", tone: "healthy" };
}
