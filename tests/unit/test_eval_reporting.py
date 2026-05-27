from datetime import UTC, datetime

from farmer_helper.schemas.evaluation import EvalDataset, EvalDatasetItem
from farmer_helper.services.evaluation.reporting import EvalOfflineReportBuilder
from farmer_helper.services.evaluation.runner import EvalRunner


def _run_result():
    dataset = EvalDataset(
        version="v1",
        items=[
            EvalDatasetItem(
                id="Q001",
                question="Question 1",
                expected_topics=["topic-1"],
                expected_keywords=["kw-1"],
                must_cite_source=True,
                difficulty="easy",
            ),
            EvalDatasetItem(
                id="Q002",
                question="Question 2",
                expected_topics=["topic-2"],
                expected_keywords=[],
                must_cite_source=False,
                difficulty="hard",
            ),
        ],
    )
    return EvalRunner().run(dataset)


def test_eval_offline_report_builder_produces_deterministic_payload() -> None:
    fixed_now = datetime(2026, 5, 27, 12, 0, 0, tzinfo=UTC)
    builder = EvalOfflineReportBuilder(now_fn=lambda: fixed_now)

    report = builder.build(_run_result())

    assert report.generated_at_utc == "2026-05-27T12:00:00+00:00"
    assert report.dataset_version == "v1"
    assert report.summary.total_items == 2
    assert len(report.items) == 2


def test_eval_offline_report_builder_json_is_stable() -> None:
    fixed_now = datetime(2026, 5, 27, 12, 0, 0, tzinfo=UTC)
    builder = EvalOfflineReportBuilder(now_fn=lambda: fixed_now)
    report = builder.build(_run_result())

    left = EvalOfflineReportBuilder.to_json(report)
    right = EvalOfflineReportBuilder.to_json(report)

    assert left == right
    assert '"dataset_version": "v1"' in left
