import logging


class IngestionTraceLogger:
    def __init__(self) -> None:
        """Init for ingestion workflows.

        Initialize IngestionTraceLogger for ingestion workflows. This operation does not require
        explicit caller-supplied arguments. It runs synchronously and returns when local
        processing is complete. The operation is executed for its side effects and does not
        return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger = logging.getLogger(__name__)

    def job_started(self, job_id: int, document_id: int) -> None:
        """Job started for ingestion workflows.

        This IngestionTraceLogger method belongs to the ingestion service layer. Inputs are
        job_id, document_id. It runs synchronously and returns when local processing is
        complete. The operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.info(
            "ingestion.job.started",
            extra={
                "job_id": job_id,
                "document_id": document_id,
                "ingestion_stage": "ingestion",
                "ingestion_status": "pending",
            },
        )

    def processing_started(self, job_id: int, document_id: int) -> None:
        """Processing started for ingestion workflows.

        This IngestionTraceLogger method belongs to the ingestion service layer. Inputs are
        job_id, document_id. It runs synchronously and returns when local processing is
        complete. The operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.info(
            "ingestion.job.processing",
            extra={
                "job_id": job_id,
                "document_id": document_id,
                "ingestion_stage": "ingestion",
                "ingestion_status": "processing",
            },
        )

    def job_succeeded(self, job_id: int, document_id: int) -> None:
        """Job succeeded for ingestion workflows.

        This IngestionTraceLogger method belongs to the ingestion service layer. Inputs are
        job_id, document_id. It runs synchronously and returns when local processing is
        complete. The operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.info(
            "ingestion.job.succeeded",
            extra={
                "job_id": job_id,
                "document_id": document_id,
                "ingestion_stage": "ingestion",
                "ingestion_status": "succeeded",
            },
        )

    def job_failed(
        self,
        job_id: int,
        document_id: int,
        error_code: str,
        error_message: str,
    ) -> None:
        """Job failed for ingestion workflows.

        This IngestionTraceLogger method belongs to the ingestion service layer. Inputs are
        job_id, document_id, error_code, error_message. It runs synchronously and returns when
        local processing is complete. The operation is executed for its side effects and does
        not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._logger.error(
            "ingestion.job.failed",
            extra={
                "job_id": job_id,
                "document_id": document_id,
                "ingestion_stage": "ingestion",
                "ingestion_status": "failed",
                "error_code": error_code,
                "error_message": error_message,
            },
        )
