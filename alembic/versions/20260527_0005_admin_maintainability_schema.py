"""Add admin maintainability schema.

Revision ID: 20260527_0005
Revises: 20260527_0004
Create Date: 2026-05-27 00:00:05
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0005"
down_revision = "20260527_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "version_tracking_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_version", sa.String(length=64), nullable=False),
        sa.Column("model_version", sa.String(length=128), nullable=False),
        sa.Column("pipeline_version", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_version_tracking_records_id", "version_tracking_records", ["id"], unique=False
    )
    op.create_index(
        "ix_version_tracking_records_content_version",
        "version_tracking_records",
        ["content_version"],
        unique=False,
    )
    op.create_index(
        "ix_version_tracking_records_model_version",
        "version_tracking_records",
        ["model_version"],
        unique=False,
    )
    op.create_index(
        "ix_version_tracking_records_pipeline_version",
        "version_tracking_records",
        ["pipeline_version"],
        unique=False,
    )
    op.create_index(
        "ix_version_tracking_records_created_by",
        "version_tracking_records",
        ["created_by"],
        unique=False,
    )

    op.create_table(
        "gold_answer_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("editor_id", sa.String(length=128), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_gold_answer_records_id", "gold_answer_records", ["id"], unique=False)
    op.create_index(
        "ix_gold_answer_records_status", "gold_answer_records", ["status"], unique=False
    )
    op.create_index(
        "ix_gold_answer_records_editor_id", "gold_answer_records", ["editor_id"], unique=False
    )

    op.create_table(
        "qa_review_queue_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("source_path", sa.String(length=512), nullable=True),
        sa.Column("issue_type", sa.String(length=64), nullable=False),
        sa.Column("details", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("assigned_to", sa.String(length=128), nullable=True),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_qa_review_queue_items_id", "qa_review_queue_items", ["id"], unique=False)
    op.create_index(
        "ix_qa_review_queue_items_document_id",
        "qa_review_queue_items",
        ["document_id"],
        unique=False,
    )
    op.create_index(
        "ix_qa_review_queue_items_issue_type", "qa_review_queue_items", ["issue_type"], unique=False
    )
    op.create_index(
        "ix_qa_review_queue_items_status", "qa_review_queue_items", ["status"], unique=False
    )
    op.create_index(
        "ix_qa_review_queue_items_assigned_to",
        "qa_review_queue_items",
        ["assigned_to"],
        unique=False,
    )

    op.create_table(
        "access_audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=True),
        sa.Column("details_json", sa.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_access_audit_logs_id", "access_audit_logs", ["id"], unique=False)
    op.create_index(
        "ix_access_audit_logs_actor_id", "access_audit_logs", ["actor_id"], unique=False
    )
    op.create_index("ix_access_audit_logs_action", "access_audit_logs", ["action"], unique=False)
    op.create_index(
        "ix_access_audit_logs_target_type", "access_audit_logs", ["target_type"], unique=False
    )
    op.create_index(
        "ix_access_audit_logs_target_id", "access_audit_logs", ["target_id"], unique=False
    )
    op.create_index(
        "ix_access_audit_logs_request_id", "access_audit_logs", ["request_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_access_audit_logs_request_id", table_name="access_audit_logs")
    op.drop_index("ix_access_audit_logs_target_id", table_name="access_audit_logs")
    op.drop_index("ix_access_audit_logs_target_type", table_name="access_audit_logs")
    op.drop_index("ix_access_audit_logs_action", table_name="access_audit_logs")
    op.drop_index("ix_access_audit_logs_actor_id", table_name="access_audit_logs")
    op.drop_index("ix_access_audit_logs_id", table_name="access_audit_logs")
    op.drop_table("access_audit_logs")

    op.drop_index("ix_qa_review_queue_items_assigned_to", table_name="qa_review_queue_items")
    op.drop_index("ix_qa_review_queue_items_status", table_name="qa_review_queue_items")
    op.drop_index("ix_qa_review_queue_items_issue_type", table_name="qa_review_queue_items")
    op.drop_index("ix_qa_review_queue_items_document_id", table_name="qa_review_queue_items")
    op.drop_index("ix_qa_review_queue_items_id", table_name="qa_review_queue_items")
    op.drop_table("qa_review_queue_items")

    op.drop_index("ix_gold_answer_records_editor_id", table_name="gold_answer_records")
    op.drop_index("ix_gold_answer_records_status", table_name="gold_answer_records")
    op.drop_index("ix_gold_answer_records_id", table_name="gold_answer_records")
    op.drop_table("gold_answer_records")

    op.drop_index("ix_version_tracking_records_created_by", table_name="version_tracking_records")
    op.drop_index(
        "ix_version_tracking_records_pipeline_version", table_name="version_tracking_records"
    )
    op.drop_index(
        "ix_version_tracking_records_model_version", table_name="version_tracking_records"
    )
    op.drop_index(
        "ix_version_tracking_records_content_version", table_name="version_tracking_records"
    )
    op.drop_index("ix_version_tracking_records_id", table_name="version_tracking_records")
    op.drop_table("version_tracking_records")
