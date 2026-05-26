"""Create foundational schema tables.

Revision ID: 20260526_0001
Revises:
Create Date: 2026-05-26 00:00:01
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260526_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_path", sa.String(length=512), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_path"),
    )
    op.create_index("ix_documents_id", "documents", ["id"], unique=False)
    op.create_index("ix_documents_content_hash", "documents", ["content_hash"], unique=False)

    op.create_table(
        "ingestion_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ingestion_jobs_id", "ingestion_jobs", ["id"], unique=False)
    op.create_index("ix_ingestion_jobs_document_id", "ingestion_jobs", ["document_id"], unique=False)
    op.create_index("ix_ingestion_jobs_status", "ingestion_jobs", ["status"], unique=False)

    op.create_table(
        "api_request_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("path", sa.String(length=256), nullable=False),
        sa.Column("method", sa.String(length=16), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_api_request_logs_id", "api_request_logs", ["id"], unique=False)
    op.create_index("ix_api_request_logs_request_id", "api_request_logs", ["request_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_api_request_logs_request_id", table_name="api_request_logs")
    op.drop_index("ix_api_request_logs_id", table_name="api_request_logs")
    op.drop_table("api_request_logs")

    op.drop_index("ix_ingestion_jobs_status", table_name="ingestion_jobs")
    op.drop_index("ix_ingestion_jobs_document_id", table_name="ingestion_jobs")
    op.drop_index("ix_ingestion_jobs_id", table_name="ingestion_jobs")
    op.drop_table("ingestion_jobs")

    op.drop_index("ix_documents_content_hash", table_name="documents")
    op.drop_index("ix_documents_id", table_name="documents")
    op.drop_table("documents")
