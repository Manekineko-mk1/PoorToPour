from typing import Protocol

from app.models.market_data import (
    CompanyProfile,
    DailyBar,
    EarningsEvent,
    ProviderStatus,
    SymbolProfile,
)


class MarketDataProvider(Protocol):
    def get_status(self) -> ProviderStatus:
        ...

    def list_symbols(self) -> list[SymbolProfile]:
        ...

    def get_daily_bars(self, symbol: str) -> list[DailyBar]:
        ...


class CompanyProfileProvider(Protocol):
    def get_company_profile(self, symbol: str) -> CompanyProfile | None:
        ...


class EarningsProvider(Protocol):
    def get_earnings_event(self, symbol: str) -> EarningsEvent | None:
        ...
