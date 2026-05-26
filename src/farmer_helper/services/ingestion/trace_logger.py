import logging


class IngestionTraceLogger:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def job_started(self, job_id: int, document_id: int) -> None:
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
