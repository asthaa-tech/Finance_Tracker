
"""add families financial accounts and analytics

Revision ID: 1a992f8cb305
Revises: 0c483c38e8e6
Create Date: 2026-09-26 15:37:23.369351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1a992f8cb305"
down_revision: Union[str, Sequence[str], None] = "0c483c38e8e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "families",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "family_memberships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("family_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["family_id"], ["families.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "family_id",
            "user_id",
            name="uq_family_user",
        ),
    )

    op.create_index(
        op.f("ix_family_memberships_family_id"),
        "family_memberships",
        ["family_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_family_memberships_user_id"),
        "family_memberships",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "financial_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("account_type", sa.String(length=30), nullable=False),
        sa.Column("provider_name", sa.String(length=100), nullable=True),
        sa.Column("identifier", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_financial_accounts_user_id"),
        "financial_accounts",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "financial_connections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("provider_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("external_account_id", sa.String(length=255), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_financial_connections_account_id"),
        "financial_connections",
        ["account_id"],
        unique=False,
    )

    op.add_column(
        "transactions",
        sa.Column("account_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "transactions",
        sa.Column("merchant_name", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "transactions",
        sa.Column(
            "categorization_source",
            sa.String(length=30),
            server_default="manual",
            nullable=False,
        ),
    )

    op.add_column(
        "transactions",
        sa.Column(
            "categorization_confidence",
            sa.Numeric(precision=5, scale=4),
            nullable=True,
        ),
    )

    op.add_column(
        "transactions",
        sa.Column(
            "external_transaction_id",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_transactions_account_id"),
        "transactions",
        ["account_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_transactions_external_transaction_id"),
        "transactions",
        ["external_transaction_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_transactions_account_id",
        "transactions",
        "financial_accounts",
        ["account_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_transactions_account_id",
        "transactions",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_transactions_external_transaction_id"),
        table_name="transactions",
    )

    op.drop_index(
        op.f("ix_transactions_account_id"),
        table_name="transactions",
    )

    op.drop_column(
        "transactions",
        "external_transaction_id",
    )

    op.drop_column(
        "transactions",
        "categorization_confidence",
    )

    op.drop_column(
        "transactions",
        "categorization_source",
    )

    op.drop_column(
        "transactions",
        "merchant_name",
    )

    op.drop_column(
        "transactions",
        "account_id",
    )

    op.drop_index(
        op.f("ix_financial_connections_account_id"),
        table_name="financial_connections",
    )

    op.drop_table("financial_connections")

    op.drop_index(
        op.f("ix_financial_accounts_user_id"),
        table_name="financial_accounts",
    )

    op.drop_table("financial_accounts")

    op.drop_index(
        op.f("ix_family_memberships_user_id"),
        table_name="family_memberships",
    )

    op.drop_index(
        op.f("ix_family_memberships_family_id"),
        table_name="family_memberships",
    )

    op.drop_table("family_memberships")

    op.drop_table("families")

