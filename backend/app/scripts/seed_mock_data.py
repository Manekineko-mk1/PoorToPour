from app.db.base import SessionLocal
from app.providers.mock_provider import MockProvider
from app.repositories.market_data import (
    upsert_company_profile,
    upsert_daily_bar,
    upsert_earnings_event,
    upsert_symbol,
)
from app.repositories.scans import scan_run_from_payload, upsert_scan_run


def seed_mock_data() -> None:
    provider = MockProvider()
    db = SessionLocal()
    try:
        symbols = provider.list_symbols()
        for symbol in symbols:
            upsert_symbol(db, symbol)

        for symbol in symbols:
            profile = provider.get_company_profile(symbol.symbol)
            if profile is not None:
                upsert_company_profile(db, profile)

            earnings = provider.get_earnings_event(symbol.symbol)
            if earnings is not None:
                upsert_earnings_event(db, earnings)

            for bar in provider.get_daily_bars(symbol.symbol):
                upsert_daily_bar(db, bar, source="mock")

        upsert_scan_run(db, scan_run_from_payload(provider.get_latest_scan()))

        db.commit()
        print(f"Seeded mock provider data for {len(symbols)} symbols.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_mock_data()
