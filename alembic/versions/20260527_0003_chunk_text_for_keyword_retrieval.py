"""Add chunk text column for keyword retrieval.

Revision ID: 20260527_0003
Revises: 20260527_0002
Create Date: 2026-05-27 00:00:03
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0003"
down_revision = "20260527_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "chunk_embeddings",
        sa.Column("chunk_text", sa.Text(), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("chunk_embeddings", "chunk_text")
