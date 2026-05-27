from collections.abc import Callable

from farmer_helper.schemas.evaluation import (
    EvalDataset,
    EvalDatasetItem,
    EvalItemRunResult,
    EvalRunConfig,
    EvalRunResult,
    EvalScoreBreakdown,
)

EvalScorer = Callable[[EvalDatasetItem], EvalScoreBreakdown]


class EvalRunner:
    def __init__(
        self,
        scorer: EvalScorer | None = None,
        config: EvalRunConfig | None = None,
    ) -> None:
        self._scorer = scorer or self._default_scorer
        self._config = config or EvalRunConfig()

    def run(self, dataset: EvalDataset) -> EvalRunResult:
        ordered_items = sorted(dataset.items, key=lambda item: item.id)

        item_results: list[EvalItemRunResult] = []
        for item in ordered_items:
            breakdown = self._scorer(item)
            total_score = breakdown.total()
            passed = total_score >= self._config.pass_threshold
            item_results.append(
                EvalItemRunResult(
                    id=item.id,
                    question=item.question,
                    difficulty=item.difficulty,
                    must_cite_source=item.must_cite_source,
                    score_breakdown=breakdown,
                    total_score=total_score,
                    max_score=10,
                    passed=passed,
                )
            )

        total_items = len(item_results)
        passed_items = sum(1 for item in item_results if item.passed)
        failed_items = total_items - passed_items
        average_score = round(
            sum(item.total_score for item in item_results) / total_items,
            4,
        )

        return EvalRunResult(
            dataset_version=dataset.version,
            total_items=total_items,
            passed_items=passed_items,
            failed_items=failed_items,
            average_score=average_score,
            item_results=item_results,
        )

    @staticmethod
    def _default_scorer(item: EvalDatasetItem) -> EvalScoreBreakdown:
        citation_score = 2 if item.must_cite_source else 1
        clarity_score = 2 if item.expected_keywords else 1
        safety_score = 2 if item.difficulty == "hard" else 1

        return EvalScoreBreakdown(
            retrieval_relevance=2,
            groundedness=2,
            citation_correctness=citation_score,
            safety_refusal=safety_score,
            clarity_actionability=clarity_score,
        )
