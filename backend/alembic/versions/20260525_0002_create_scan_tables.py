"""create scan tables

Revision ID: 20260525_0002
Revises: 20260525_0001
Create Date: 2026-05-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260525_0002"
down_revision: Union[str, None] = "20260525_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan_runs",
        sa.Column("id", sa.String(length=96), nullable=False),
        sa.Column("scan_type", sa.String(length=128), nullable=False),
        sa.Column("universe", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("provider", sa.String(length=128), nullable=False),
        sa.Column("data_date", sa.Date(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("symbols_processed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("candidates_found", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("warning", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scan_runs_completed_at", "scan_runs", ["completed_at"])
    op.create_index("ix_scan_runs_status", "scan_runs", ["status"])

    op.create_table(
        "scan_candidates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("scan_run_id", sa.String(length=96), nullable=False),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("setup", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("relative_volume", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("rsi", sa.Numeric(precision=8, scale=4), nullable=True),
        sa.Column("risk_reward", sa.String(length=32), nullable=True),
        sa.Column("indicator_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("score_breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("reasons", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("caution_flags", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["scan_run_id"], ["scan_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["symbol"], ["symbol_profiles.symbol"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("scan_run_id", "rank", name="uq_scan_candidates_run_rank"),
        sa.UniqueConstraint("scan_run_id", "symbol", "setup", name="uq_scan_candidates_run_symbol_setup"),
    )
    op.create_index("ix_scan_candidates_scan_run_id", "scan_candidates", ["scan_run_id"])
    op.create_index("ix_scan_candidates_status", "scan_candidates", ["status"])
    op.create_index("ix_scan_candidates_symbol", "scan_candidates", ["symbol"])


def downgrade() -> None:
    op.drop_index("ix_scan_candidates_symbol", table_name="scan_candidates")
    op.drop_index("ix_scan_candidates_status", table_name="scan_candidates")
    op.drop_index("ix_scan_candidates_scan_run_id", table_name="scan_candidates")
    op.drop_table("scan_candidates")
    op.drop_index("ix_scan_runs_status", table_name="scan_runs")
    op.drop_index("ix_scan_runs_completed_at", table_name="scan_runs")
    op.drop_table("scan_runs")
