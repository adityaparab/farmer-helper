"""Add embedding vector persistence schema.

Revision ID: 20260527_0002
Revises: 20260526_0001
Create Date: 2026-05-27 00:00:02
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0002"
down_revision = "20260526_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chunk_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("vector_json", sa.JSON(), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "document_id",
            "chunk_index",
            "provider",
            "model",
            "version",
            name="uq_chunk_embeddings_identity",
        ),
    )
    op.create_index("ix_chunk_embeddings_id", "chunk_embeddings", ["id"], unique=False)
    op.create_index(
        "ix_chunk_embeddings_document_id",
        "chunk_embeddings",
        ["document_id"],
        unique=False,
    )
    op.create_index(
        "ix_chunk_embeddings_content_hash",
        "chunk_embeddings",
        ["content_hash"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_chunk_embeddings_content_hash", table_name="chunk_embeddings")
    op.drop_index("ix_chunk_embeddings_document_id", table_name="chunk_embeddings")
    op.drop_index("ix_chunk_embeddings_id", table_name="chunk_embeddings")
    op.drop_table("chunk_embeddings")
