from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.db.models import CompanyProfileRow, DailyBarRow, EarningsEventRow, SymbolProfileRow
from app.models.market_data import CompanyProfile, DailyBar, EarningsEvent, SymbolProfile


def list_symbols(db: Session) -> list[SymbolProfile]:
    rows = db.scalars(select(SymbolProfileRow).order_by(SymbolProfileRow.symbol)).all()
    return [
        SymbolProfile(
            symbol=row.symbol,
            company_name=row.company_name,
            sector=row.sector,
            industry=row.industry,
            exchange=row.exchange,
            is_active=row.is_active,
        )
        for row in rows
    ]


def get_daily_bars(db: Session, symbol: str) -> list[DailyBar]:
    rows = db.scalars(
        select(DailyBarRow)
        .where(DailyBarRow.symbol == symbol.upper())
        .order_by(DailyBarRow.date)
    ).all()
    return [
        DailyBar(
            symbol=row.symbol,
            date=row.date,
            open=_to_float(row.open),
            high=_to_float(row.high),
            low=_to_float(row.low),
            close=_to_float(row.close),
            adjusted_close=_to_float(row.adjusted_close),
            volume=row.volume,
        )
        for row in rows
    ]


def get_company_profile(db: Session, symbol: str) -> CompanyProfile | None:
    row = db.get(CompanyProfileRow, symbol.upper())
    if row is None:
        return None
    return CompanyProfile(
        symbol=row.symbol,
        company_name=row.company_name,
        sector=row.sector,
        industry=row.industry,
        market_cap=row.market_cap,
        average_volume=row.average_volume,
        exchange=row.exchange,
    )


def get_earnings_event(db: Session, symbol: str) -> EarningsEvent | None:
    row = db.get(EarningsEventRow, symbol.upper())
    if row is None:
        return None
    return EarningsEvent(
        symbol=row.symbol,
        last_earnings_date=row.last_earnings_date.isoformat() if row.last_earnings_date else None,
        next_earnings_date=row.next_earnings_date.isoformat() if row.next_earnings_date else None,
        source=row.source,
    )


def upsert_symbol(db: Session, symbol: SymbolProfile) -> None:
    statement = pg_insert(SymbolProfileRow).values(**symbol.model_dump())
    statement = statement.on_conflict_do_update(
        index_elements=[SymbolProfileRow.symbol],
        set_={
            "company_name": statement.excluded.company_name,
            "sector": statement.excluded.sector,
            "industry": statement.excluded.industry,
            "exchange": statement.excluded.exchange,
            "is_active": statement.excluded.is_active,
        },
    )
    db.execute(statement)


def upsert_company_profile(db: Session, profile: CompanyProfile) -> None:
    statement = pg_insert(CompanyProfileRow).values(**profile.model_dump())
    statement = statement.on_conflict_do_update(
        index_elements=[CompanyProfileRow.symbol],
        set_={
            "company_name": statement.excluded.company_name,
            "sector": statement.excluded.sector,
            "industry": statement.excluded.industry,
            "market_cap": statement.excluded.market_cap,
            "average_volume": statement.excluded.average_volume,
            "exchange": statement.excluded.exchange,
        },
    )
    db.execute(statement)


def upsert_earnings_event(db: Session, event: EarningsEvent) -> None:
    values = event.model_dump()
    values["last_earnings_date"] = _parse_date(values["last_earnings_date"])
    values["next_earnings_date"] = _parse_date(values["next_earnings_date"])
    statement = pg_insert(EarningsEventRow).values(**values)
    statement = statement.on_conflict_do_update(
        index_elements=[EarningsEventRow.symbol],
        set_={
            "last_earnings_date": statement.excluded.last_earnings_date,
            "next_earnings_date": statement.excluded.next_earnings_date,
            "source": statement.excluded.source,
        },
    )
    db.execute(statement)


def upsert_daily_bar(db: Session, bar: DailyBar, source: str = "mock") -> None:
    values = bar.model_dump()
    values["source"] = source
    statement = pg_insert(DailyBarRow).values(**values)
    statement = statement.on_conflict_do_update(
        constraint="uq_daily_bars_symbol_date",
        set_={
            "open": statement.excluded.open,
            "high": statement.excluded.high,
            "low": statement.excluded.low,
            "close": statement.excluded.close,
            "adjusted_close": statement.excluded.adjusted_close,
            "volume": statement.excluded.volume,
            "source": statement.excluded.source,
        },
    )
    db.execute(statement)


def _to_float(value: Decimal) -> float:
    return float(value)


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None
