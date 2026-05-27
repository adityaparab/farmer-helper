"""Add auth and RBAC schema.

Revision ID: 20260527_0007
Revises: 20260527_0006
Create Date: 2026-05-27 00:00:07
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0007"
down_revision = "20260527_0006"
branch_labels = None
depends_on = None

DEFAULT_ADMIN_PASSWORD_HASH = (
    "pbkdf2_sha256$310000$ZmFybWVyLWhlbHBlci1kZWZhdWx0LWFkbWluLXYx$"
    "sVHLdCuNSngooVlVDdkAn-oN0aLSL7uWBzJBQ_8tuvk"
)


def upgrade() -> None:
    op.create_table(
        "user_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_user_accounts_id", "user_accounts", ["id"], unique=False)
    op.create_index("ix_user_accounts_is_active", "user_accounts", ["is_active"], unique=False)
    op.create_index("ix_user_accounts_role", "user_accounts", ["role"], unique=False)
    op.create_index("ix_user_accounts_username", "user_accounts", ["username"], unique=True)

    op.create_table(
        "refresh_token_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        "ix_refresh_token_records_expires_at",
        "refresh_token_records",
        ["expires_at"],
        unique=False,
    )
    op.create_index("ix_refresh_token_records_id", "refresh_token_records", ["id"], unique=False)
    op.create_index(
        "ix_refresh_token_records_token_hash",
        "refresh_token_records",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_refresh_token_records_user_id",
        "refresh_token_records",
        ["user_id"],
        unique=False,
    )

    user_accounts = sa.table(
        "user_accounts",
        sa.column("username", sa.String),
        sa.column("password_hash", sa.String),
        sa.column("role", sa.String),
        sa.column("is_active", sa.Boolean),
    )
    op.bulk_insert(
        user_accounts,
        [
            {
                "username": "admin",
                "password_hash": DEFAULT_ADMIN_PASSWORD_HASH,
                "role": "admin",
                "is_active": True,
            }
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_refresh_token_records_user_id", table_name="refresh_token_records")
    op.drop_index("ix_refresh_token_records_token_hash", table_name="refresh_token_records")
    op.drop_index("ix_refresh_token_records_id", table_name="refresh_token_records")
    op.drop_index("ix_refresh_token_records_expires_at", table_name="refresh_token_records")
    op.drop_table("refresh_token_records")
    op.drop_index("ix_user_accounts_username", table_name="user_accounts")
    op.drop_index("ix_user_accounts_role", table_name="user_accounts")
    op.drop_index("ix_user_accounts_is_active", table_name="user_accounts")
    op.drop_index("ix_user_accounts_id", table_name="user_accounts")
    op.drop_table("user_accounts")
