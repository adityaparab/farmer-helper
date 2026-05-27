from farmer_helper.schemas.evaluation import EvalRunResult


class EvalRegressionError(Exception):
    pass


class EvalCIGate:
    def __init__(self, min_average_score: float) -> None:
        if min_average_score < 0.0 or min_average_score > 10.0:
            raise ValueError("min_average_score must be between 0 and 10")
        self._min_average_score = min_average_score

    def assert_passes(self, run_result: EvalRunResult) -> None:
        if run_result.average_score < self._min_average_score:
            raise EvalRegressionError(
                "Evaluation average score below threshold: "
                f"{run_result.average_score} < {self._min_average_score}"
            )
