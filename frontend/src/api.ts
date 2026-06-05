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
  market_data_refresh?: MarketDataRefreshSummary;
};

export type MarketDataRefreshSummary = {
  provider: string;
  period: string;
  symbols_requested: number;
  symbols_refreshed: number;
  symbols_failed: number;
  bars_persisted: number;
  failure_messages: string[];
};

export type ChartIndicatorBar = {
  symbol: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  adjusted_close: number;
  volume: number;
  sma_20: number | null;
  sma_50: number | null;
  sma_200: number | null;
  rsi_14: number | null;
};

export type RiskRewardOverlay = {
  entry: number | null;
  invalidation: number | null;
  target: number | null;
  risk_per_share: number | null;
  ratio: string | null;
};

export type ChartCandidateContext = {
  scan_id: string;
  setup: string;
  status: Candidate["status"];
  score: number;
  risk_reward: string | null;
  reasons: string[];
  caution_flags: string[];
  risk_reward_overlay: RiskRewardOverlay | null;
};

export type SymbolChartPayload = {
  symbol: string;
  company_name: string | null;
  exchange: string | null;
  data_date: string | null;
  bars: ChartIndicatorBar[];
  candidate: ChartCandidateContext | null;
  warnings: string[];
};

export type DisplaySettings = {
  environment: string;
  provider: string;
  data_source_note: string;
  universe: string;
  enabled_setups: string[];
  scanner?: {
    risk_reward_atr_buffer_multiplier: number;
    risk_reward_target_multiple: number;
    schedule: string;
  };
  ui_feature_notes: Record<string, string>;
  admin_controls?: Record<string, string>;
  ai_notes: Record<string, string>;
};

export async function fetchLatestScan(): Promise<LatestScan | null> {
  const response = await fetch(`${API_BASE_URL}/api/scans/latest`);
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error(await responseErrorMessage(response, "Unable to load latest scan"));
  }
  return response.json();
}

export async function runManualScan(): Promise<LatestScan> {
  const response = await fetch(`${API_BASE_URL}/api/scans/manual`, { method: "POST" });
  if (!response.ok) {
    throw new Error(await responseErrorMessage(response, "Unable to run manual scan"));
  }
  return response.json();
}

export async function fetchScanRuns(limit = 20): Promise<LatestScan[]> {
  const response = await fetch(`${API_BASE_URL}/api/scans?limit=${limit}`);
  if (!response.ok) {
    throw new Error(await responseErrorMessage(response, "Unable to load scan history"));
  }
  return response.json();
}

export async function fetchSymbolChart(
  symbol: string,
  setup?: string,
  scanId?: string | null,
): Promise<SymbolChartPayload> {
  const params = new URLSearchParams();
  if (setup) {
    params.set("setup", setup);
  }
  if (scanId) {
    params.set("scan_id", scanId);
  }
  const query = params.size ? `?${params.toString()}` : "";
  const response = await fetch(`${API_BASE_URL}/api/symbols/${encodeURIComponent(symbol)}/chart${query}`);
  if (!response.ok) {
    throw new Error(await responseErrorMessage(response, "Unable to load symbol chart"));
  }
  return response.json();
}

export async function fetchDisplaySettings(): Promise<DisplaySettings> {
  const response = await fetch(`${API_BASE_URL}/api/settings/display`);
  if (!response.ok) {
    throw new Error(await responseErrorMessage(response, "Unable to load settings"));
  }
  return response.json();
}

async function responseErrorMessage(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.json();
    if (typeof payload.detail === "string") {
      return payload.detail;
    }
  } catch {
    // Use the user-facing fallback when the API returns a non-JSON error.
  }
  return fallback;
}
