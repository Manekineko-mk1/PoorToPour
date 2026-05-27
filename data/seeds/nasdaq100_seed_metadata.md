# Nasdaq 100 Seed Metadata

**File:** `data/seeds/nasdaq100_seed.csv`
**Downloaded:** 2026-05-26
**Rows:** 101
**Purpose:** Versioned local Nasdaq 100 universe seed for PoorToPour MVP development.

## Source

Downloaded from the current components table at:

```text
https://en.wikipedia.org/wiki/Nasdaq-100
```

Cross-reference source:

```text
https://www.nasdaq.com/solutions/global-indexes/nasdaq-100/companies
```

## Usage

This seed extends the MVP universe from S&P 500 only to S&P 500 plus Nasdaq 100. It is for bootstrapping local development and should not be treated as a licensed Nasdaq index-membership feed.

The combined MVP universe seed keeps S&P 500 metadata for overlapping symbols and adds Nasdaq 100-only symbols after deduping by normalized ticker.

The seed should be refreshed intentionally and reviewed before committing changes.

## Field Mapping

| Source Column | PoorToPour Field |
| --- | --- |
| `Symbol` | `symbol` |
| `Security` | `company_name` |
| `ICB Industry` | `sector` |
| `ICB Subsector` | `industry` |

PoorToPour imports Nasdaq 100-only symbols with `exchange = NASDAQ` until a provider supplies normalized listing metadata.
