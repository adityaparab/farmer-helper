import pytest

from farmer_helper.schemas.evaluation import EvalItemRunResult, EvalRunResult, EvalScoreBreakdown
from farmer_helper.services.evaluation.ci_gate import EvalCIGate, EvalRegressionError


def _run_result(average_score: float) -> EvalRunResult:
    return EvalRunResult(
        dataset_version="v1",
        total_items=1,
        passed_items=1,
        failed_items=0,
        average_score=average_score,
        item_results=[
            EvalItemRunResult(
                id="Q001",
                question="Question",
                difficulty="easy",
                must_cite_source=True,
                score_breakdown=EvalScoreBreakdown(
                    retrieval_relevance=2,
                    groundedness=2,
                    citation_correctness=2,
                    safety_refusal=2,
                    clarity_actionability=2,
                ),
                total_score=10,
                max_score=10,
                passed=True,
            )
        ],
    )


def test_eval_ci_gate_passes_when_average_meets_threshold() -> None:
    gate = EvalCIGate(min_average_score=6.0)
    gate.assert_passes(_run_result(average_score=6.0))


def test_eval_ci_gate_raises_when_average_below_threshold() -> None:
    gate = EvalCIGate(min_average_score=6.0)

    with pytest.raises(EvalRegressionError):
        gate.assert_passes(_run_result(average_score=5.9))


def test_eval_ci_gate_rejects_invalid_threshold() -> None:
    with pytest.raises(ValueError):
        EvalCIGate(min_average_score=-0.1)

    with pytest.raises(ValueError):
        EvalCIGate(min_average_score=10.1)
