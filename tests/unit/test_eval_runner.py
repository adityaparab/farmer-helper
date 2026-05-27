from farmer_helper.schemas.evaluation import (
    EvalDataset,
    EvalDatasetItem,
    EvalRunConfig,
    EvalScoreBreakdown,
)
from farmer_helper.services.evaluation.runner import EvalRunner


def _dataset() -> EvalDataset:
    return EvalDataset(
        version="v1",
        items=[
            EvalDatasetItem(
                id="Q002",
                question="Question 2",
                expected_topics=["topic-2"],
                expected_keywords=["kw-2"],
                must_cite_source=True,
                difficulty="medium",
            ),
            EvalDatasetItem(
                id="Q001",
                question="Question 1",
                expected_topics=["topic-1"],
                expected_keywords=[],
                must_cite_source=False,
                difficulty="hard",
            ),
        ],
    )


def test_eval_runner_sorts_by_id_and_aggregates_counts() -> None:
    score_map = {
        "Q001": EvalScoreBreakdown(
            retrieval_relevance=2,
            groundedness=2,
            citation_correctness=1,
            safety_refusal=2,
            clarity_actionability=1,
        ),
        "Q002": EvalScoreBreakdown(
            retrieval_relevance=1,
            groundedness=1,
            citation_correctness=1,
            safety_refusal=1,
            clarity_actionability=1,
        ),
    }

    def scorer(item: EvalDatasetItem) -> EvalScoreBreakdown:
        return score_map[item.id]

    runner = EvalRunner(scorer=scorer, config=EvalRunConfig(pass_threshold=7))
    result = runner.run(_dataset())

    assert [item.id for item in result.item_results] == ["Q001", "Q002"]
    assert result.total_items == 2
    assert result.passed_items == 1
    assert result.failed_items == 1
    assert result.average_score == 6.5


def test_eval_runner_default_scorer_produces_stable_results() -> None:
    runner = EvalRunner(config=EvalRunConfig(pass_threshold=6))
    result = runner.run(_dataset())

    assert result.total_items == 2
    assert result.passed_items == 2
    assert result.failed_items == 0
    assert all(item.total_score >= 6 for item in result.item_results)
