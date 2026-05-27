from app.scripts import symbol_resolution


def test_resolve_symbols_normalizes_requested_symbols_and_applies_limit() -> None:
    symbols = symbol_resolution.resolve_symbols(["aapl", "msft", "nvda"], limit=2)

    assert symbols == ["AAPL", "MSFT"]


def test_resolve_symbols_prefers_persisted_symbols(monkeypatch) -> None:
    monkeypatch.setattr(symbol_resolution, "_persisted_symbols", lambda: ["AAPL", "MSFT", "NVDA"])

    symbols = symbol_resolution.resolve_symbols(requested_symbols=None, limit=2)

    assert symbols == ["AAPL", "MSFT"]


def test_resolve_symbols_falls_back_to_development_symbols(monkeypatch) -> None:
    monkeypatch.setattr(symbol_resolution, "_persisted_symbols", lambda: [])

    symbols = symbol_resolution.resolve_symbols(requested_symbols=None, limit=3)

    assert symbols == ["AAPL", "MSFT", "NVDA"]
