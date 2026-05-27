import {
  Activity,
  AlertTriangle,
  Database,
  PanelLeftClose,
  PanelLeftOpen,
  Play,
  Search,
  Settings,
  TrendingUp,
} from "lucide-react";
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

  return (
    <main className={`app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""}`}>
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
        <div className="brand">
          <span className="brand-icon">PT</span>
          <div className="brand-copy">
            <h1>PoorToPour</h1>
            <p>From broke to pouring champagne.</p>
          </div>
        </div>
        <nav>
          <a className="active">Dashboard</a>
          <a>Scan History</a>
          <a>Settings</a>
          <a className="muted">Watchlist MVP+</a>
          <a className="muted">Sector Scanner MVP+</a>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Local MVP</span>
            <h2>Dashboard</h2>
          </div>
          <div className="topbar-actions">
            <div className="search"><Search size={16} /> Search tickers...</div>
            <button><Play size={16} /> Run Manual Scan</button>
          </div>
        </header>

        {error && <section className="panel warning"><AlertTriangle /> {error}</section>}

        <section className="summary-grid">
          <div className="panel metric"><Activity /><span>Scan Status</span><strong>{scan?.status ?? "Loading"}</strong></div>
          <div className="panel metric"><Database /><span>Provider</span><strong>{formatProvider(scan?.provider)}</strong></div>
          <div className="panel metric"><TrendingUp /><span>Candidates</span><strong>{scan?.candidates_found ?? "--"}</strong></div>
          <div className="panel metric"><Settings /><span>Universe</span><strong>{scan?.universe ?? "S&P 500"}</strong></div>
        </section>

        <section className="content-grid">
          <section className="panel table-panel">
            <div className="panel-header">
              <div>
                <h3>Top Candidates</h3>
                <p>{scan?.warning ?? "Fixture data only."}</p>
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
