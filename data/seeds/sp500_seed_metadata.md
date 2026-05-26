# S&P 500 Seed Metadata

**File:** `data/seeds/sp500_seed.csv`  
**Downloaded:** 2026-05-25  
**Rows:** 503  
**Purpose:** Versioned local universe seed for PoorToPour MVP development.

## Source

Downloaded from:

```text
https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv
```

Repository:

```text
https://github.com/datasets/s-and-p-500-companies
```

The dataset is based on the Wikipedia S&P 500 constituents table.

## Usage

This seed is for bootstrapping the MVP stock universe. It is not a licensed S&P Global constituent feed and should not be treated as trading-grade index membership data.

The seed should be refreshed intentionally and reviewed before committing changes.

## Field Mapping

| Source Column | PoorToPour Field |
| --- | --- |
| `Symbol` | `symbol` |
| `Security` | `company_name` |
| `GICS Sector` | `sector` |
| `GICS Sub-Industry` | `industry` |

The source file does not include exchange. PoorToPour imports this seed with `exchange = UNKNOWN` until a provider supplies normalized listing metadata.
