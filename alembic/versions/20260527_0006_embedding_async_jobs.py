"""Add persistent embedding async jobs table.

Revision ID: 20260527_0006
Revises: 20260527_0005
Create Date: 2026-05-27 00:00:06
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0006"
down_revision = "20260527_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "embedding_async_jobs",
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("request_json", sa.JSON(), nullable=True),
        sa.Column("result_json", sa.JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("job_id"),
    )
    op.create_index(
        "ix_embedding_async_jobs_job_id", "embedding_async_jobs", ["job_id"], unique=False
    )
    op.create_index(
        "ix_embedding_async_jobs_status", "embedding_async_jobs", ["status"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_embedding_async_jobs_status", table_name="embedding_async_jobs")
    op.drop_index("ix_embedding_async_jobs_job_id", table_name="embedding_async_jobs")
    op.drop_table("embedding_async_jobs")
