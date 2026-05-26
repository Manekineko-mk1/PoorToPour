from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SymbolProfileRow(Base):
    __tablename__ = "symbol_profiles"

    symbol: Mapped[str] = mapped_column(String(16), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255))
    sector: Mapped[str] = mapped_column(String(128))
    industry: Mapped[str] = mapped_column(String(128))
    exchange: Mapped[str] = mapped_column(String(32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    bars: Mapped[list["DailyBarRow"]] = relationship(back_populates="symbol_profile", cascade="all, delete-orphan")
    company_profile: Mapped["CompanyProfileRow | None"] = relationship(back_populates="symbol_profile", cascade="all, delete-orphan")
    earnings_event: Mapped["EarningsEventRow | None"] = relationship(back_populates="symbol_profile", cascade="all, delete-orphan")
    scan_candidates: Mapped[list["ScanCandidateRow"]] = relationship(back_populates="symbol_profile")


class CompanyProfileRow(Base):
    __tablename__ = "company_profiles"

    symbol: Mapped[str] = mapped_column(ForeignKey("symbol_profiles.symbol", ondelete="CASCADE"), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255))
    sector: Mapped[str] = mapped_column(String(128))
    industry: Mapped[str] = mapped_column(String(128))
    market_cap: Mapped[int] = mapped_column(BigInteger)
    average_volume: Mapped[int] = mapped_column(BigInteger)
    exchange: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    symbol_profile: Mapped[SymbolProfileRow] = relationship(back_populates="company_profile")


class EarningsEventRow(Base):
    __tablename__ = "earnings_events"

    symbol: Mapped[str] = mapped_column(ForeignKey("symbol_profiles.symbol", ondelete="CASCADE"), primary_key=True)
    last_earnings_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_earnings_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    source: Mapped[str] = mapped_column(String(64), default="mock")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    symbol_profile: Mapped[SymbolProfileRow] = relationship(back_populates="earnings_event")


class DailyBarRow(Base):
    __tablename__ = "daily_bars"
    __table_args__ = (UniqueConstraint("symbol", "date", name="uq_daily_bars_symbol_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(ForeignKey("symbol_profiles.symbol", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    open: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    high: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    low: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    close: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    adjusted_close: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    volume: Mapped[int] = mapped_column(BigInteger)
    source: Mapped[str] = mapped_column(String(64), default="mock")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    symbol_profile: Mapped[SymbolProfileRow] = relationship(back_populates="bars")


class ScanRunRow(Base):
    __tablename__ = "scan_runs"

    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    scan_type: Mapped[str] = mapped_column(String(128))
    universe: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), index=True)
    provider: Mapped[str] = mapped_column(String(128))
    data_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    symbols_processed: Mapped[int] = mapped_column(Integer, default=0)
    candidates_found: Mapped[int] = mapped_column(Integer, default=0)
    warning: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    candidates: Mapped[list["ScanCandidateRow"]] = relationship(
        back_populates="scan_run",
        cascade="all, delete-orphan",
        order_by="ScanCandidateRow.rank",
    )


class ScanCandidateRow(Base):
    __tablename__ = "scan_candidates"
    __table_args__ = (
        UniqueConstraint("scan_run_id", "rank", name="uq_scan_candidates_run_rank"),
        UniqueConstraint("scan_run_id", "symbol", "setup", name="uq_scan_candidates_run_symbol_setup"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_run_id: Mapped[str] = mapped_column(ForeignKey("scan_runs.id", ondelete="CASCADE"), index=True)
    symbol: Mapped[str] = mapped_column(ForeignKey("symbol_profiles.symbol", ondelete="CASCADE"), index=True)
    rank: Mapped[int] = mapped_column(Integer)
    company_name: Mapped[str] = mapped_column(String(255))
    setup: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), index=True)
    score: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    relative_volume: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    rsi: Mapped[Decimal | None] = mapped_column(Numeric(8, 4), nullable=True)
    risk_reward: Mapped[str | None] = mapped_column(String(32), nullable=True)
    indicator_snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    score_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    reasons: Mapped[list] = mapped_column(JSONB, default=list)
    caution_flags: Mapped[list] = mapped_column(JSONB, default=list)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    scan_run: Mapped[ScanRunRow] = relationship(back_populates="candidates")
    symbol_profile: Mapped[SymbolProfileRow] = relationship(back_populates="scan_candidates")
