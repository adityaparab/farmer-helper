import json
from collections.abc import Callable
from datetime import UTC, datetime

from farmer_helper.schemas.evaluation import (
    EvalOfflineReport,
    EvalOfflineReportItem,
    EvalOfflineReportSummary,
    EvalRunResult,
)


class EvalOfflineReportBuilder:
    def __init__(self, now_fn: Callable[[], datetime] | None = None) -> None:
        self._now_fn = now_fn or (lambda: datetime.now(UTC))

    def build(self, run_result: EvalRunResult) -> EvalOfflineReport:
        generated_at_utc = self._now_fn().astimezone(UTC).isoformat()

        items = [
            EvalOfflineReportItem(
                id=item.id,
                question=item.question,
                difficulty=item.difficulty,
                must_cite_source=item.must_cite_source,
                total_score=item.total_score,
                max_score=item.max_score,
                passed=item.passed,
                score_breakdown=item.score_breakdown,
            )
            for item in run_result.item_results
        ]

        return EvalOfflineReport(
            generated_at_utc=generated_at_utc,
            dataset_version=run_result.dataset_version,
            summary=EvalOfflineReportSummary(
                total_items=run_result.total_items,
                passed_items=run_result.passed_items,
                failed_items=run_result.failed_items,
                average_score=run_result.average_score,
            ),
            items=items,
        )

    @staticmethod
    def to_json(report: EvalOfflineReport, indent: int = 2) -> str:
        return json.dumps(report.model_dump(mode="json"), indent=indent, sort_keys=True)
