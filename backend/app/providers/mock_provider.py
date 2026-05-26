import json
from functools import cached_property
from pathlib import Path
from typing import Any

from app.models.market_data import (
    CompanyProfile,
    DailyBar,
    EarningsEvent,
    ProviderStatus,
    SymbolProfile,
)


class MockProvider:
    """Fixture-backed provider for deterministic local development."""

    def __init__(self, fixture_dir: Path | None = None) -> None:
        self.fixture_dir = fixture_dir or Path(__file__).resolve().parents[1] / "fixtures"

    def get_status(self) -> ProviderStatus:
        return ProviderStatus(
            provider="Mock Provider",
            mode="fixture",
            status="ok",
            message="Using deterministic local fixture data. Not real market data.",
            data_date="2025-05-20",
        )

    def list_symbols(self) -> list[SymbolProfile]:
        return [SymbolProfile(**item) for item in self._symbols]

    def get_daily_bars(self, symbol: str) -> list[DailyBar]:
        rows = self._daily_bars.get(symbol.upper(), [])
        return [DailyBar(symbol=symbol.upper(), **row) for row in rows]

    def get_company_profile(self, symbol: str) -> CompanyProfile | None:
        row = self._company_profiles.get(symbol.upper())
        return CompanyProfile(**row) if row else None

    def get_earnings_event(self, symbol: str) -> EarningsEvent | None:
        row = self._earnings.get(symbol.upper())
        return EarningsEvent(symbol=symbol.upper(), **row) if row else None

    def get_latest_scan(self) -> dict[str, Any]:
        return self._load_json("scan_latest_sample.json")

    @cached_property
    def _symbols(self) -> list[dict[str, Any]]:
        return self._load_json("symbols_sample.json")

    @cached_property
    def _daily_bars(self) -> dict[str, list[dict[str, Any]]]:
        return self._load_json("daily_bars_sample.json")

    @cached_property
    def _company_profiles(self) -> dict[str, dict[str, Any]]:
        return self._load_json("company_profiles_sample.json")

    @cached_property
    def _earnings(self) -> dict[str, dict[str, Any]]:
        return self._load_json("earnings_sample.json")

    def _load_json(self, filename: str) -> Any:
        path = self.fixture_dir / filename
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
