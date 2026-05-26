from app.providers.mock_provider import MockProvider


def test_mock_provider_lists_sample_symbols() -> None:
    provider = MockProvider()

    symbols = provider.list_symbols()

    assert [symbol.symbol for symbol in symbols] == ["NVDA", "MSFT", "AAPL", "META", "AMD", "AMZN"]


def test_mock_provider_returns_daily_bars() -> None:
    provider = MockProvider()

    bars = provider.get_daily_bars("NVDA")

    assert len(bars) == 10
    assert bars[-1].close == 938.70


def test_mock_provider_returns_latest_scan_fixture() -> None:
    provider = MockProvider()

    scan = provider.get_latest_scan()

    assert scan["status"] == "completed"
    assert scan["candidates"][0]["symbol"] == "NVDA"
