"""create market data tables

Revision ID: 20260525_0001
Revises:
Create Date: 2026-05-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260525_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "symbol_profiles",
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("sector", sa.String(length=128), nullable=False),
        sa.Column("industry", sa.String(length=128), nullable=False),
        sa.Column("exchange", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("symbol"),
    )

    op.create_table(
        "company_profiles",
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("sector", sa.String(length=128), nullable=False),
        sa.Column("industry", sa.String(length=128), nullable=False),
        sa.Column("market_cap", sa.BigInteger(), nullable=False),
        sa.Column("average_volume", sa.BigInteger(), nullable=False),
        sa.Column("exchange", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["symbol"], ["symbol_profiles.symbol"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("symbol"),
    )

    op.create_table(
        "earnings_events",
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("last_earnings_date", sa.Date(), nullable=True),
        sa.Column("next_earnings_date", sa.Date(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["symbol"], ["symbol_profiles.symbol"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("symbol"),
    )

    op.create_table(
        "daily_bars",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("open", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("high", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("low", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("close", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("adjusted_close", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="mock"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["symbol"], ["symbol_profiles.symbol"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol", "date", name="uq_daily_bars_symbol_date"),
    )
    op.create_index("ix_daily_bars_symbol_date", "daily_bars", ["symbol", "date"])


def downgrade() -> None:
    op.drop_index("ix_daily_bars_symbol_date", table_name="daily_bars")
    op.drop_table("daily_bars")
    op.drop_table("earnings_events")
    op.drop_table("company_profiles")
    op.drop_table("symbol_profiles")
