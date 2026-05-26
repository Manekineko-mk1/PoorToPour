import { Activity, AlertTriangle, Database, Play, Search, Settings, TrendingUp } from "lucide-react";
import { useEffect, useState } from "react";

import { Candidate, LatestScan, fetchLatestScan } from "./api";

function StatusPill({ status }: { status: Candidate["status"] }) {
  return <span className={`status status-${status.toLowerCase()}`}>{status}</span>;
}

function formatRelativeVolume(value: number | null) {
  return value == null ? "--" : `${value.toFixed(2)}x`;
}

function App() {
  const [scan, setScan] = useState<LatestScan | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLatestScan().then(setScan).catch((err: Error) => setError(err.message));
  }, []);

  const candidates = scan?.candidates ?? [];
  const selected = candidates[0];

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">PT</span>
          <div>
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
          <div className="panel metric"><Database /><span>Provider</span><strong>{scan?.provider ?? "Mock"}</strong></div>
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
                  <tr key={candidate.symbol}>
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
          </section>

          <aside className="panel insight-panel">
            <h3>Selected Candidate</h3>
            {selected ? (
              <>
                <div className="selected-symbol">{selected.symbol}</div>
                <p>{selected.company_name}</p>
                <dl>
                  <dt>Setup</dt>
                  <dd>{selected.setup}</dd>
                  <dt>Score</dt>
                  <dd>{selected.score}</dd>
                  <dt>Risk / Reward</dt>
                  <dd>{selected.risk_reward ?? "Not estimated yet"}</dd>
                  <dt>Reasons</dt>
                  <dd>{selected.reasons?.length ? selected.reasons.join(", ") : "None"}</dd>
                  <dt>Caution</dt>
                  <dd>{selected.caution_flags.length ? selected.caution_flags.join(", ") : "None"}</dd>
                </dl>
              </>
            ) : (
              <p>Loading fixture candidate...</p>
            )}
          </aside>
        </section>
      </section>
    </main>
  );
}

export default App;
