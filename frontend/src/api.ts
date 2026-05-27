const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type Candidate = {
  rank: number;
  symbol: string;
  company_name: string;
  setup: string;
  status: "Actionable" | "Watch" | "Avoid" | "Blocked";
  score: number;
  price: number | null;
  relative_volume: number | null;
  rsi: number | null;
  risk_reward: string | null;
  indicator_snapshot?: Record<string, unknown> | null;
  score_breakdown?: Record<string, unknown> | null;
  reasons?: string[];
  caution_flags: string[];
  last_updated: string | null;
};

export type LatestScan = {
  scan_id: string;
  scan_type: string;
  universe: string;
  status: string;
  provider: string;
  data_date: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  symbols_processed: number;
  candidates_found: number;
  warning: string | null;
  candidates: Candidate[];
};

export async function fetchLatestScan(): Promise<LatestScan> {
  const response = await fetch(`${API_BASE_URL}/api/scans/latest`);
  if (!response.ok) {
    throw new Error("Unable to load latest scan");
  }
  return response.json();
}
