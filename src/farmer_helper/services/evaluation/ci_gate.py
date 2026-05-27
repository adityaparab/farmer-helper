from farmer_helper.schemas.evaluation import EvalRunResult


class EvalRegressionError(Exception):
    pass


class EvalCIGate:
    def __init__(self, min_average_score: float) -> None:
        """Init for evaluation workflows.

        Initialize EvalCIGate for evaluation workflows. Inputs are min_average_score. It runs
        synchronously and returns when local processing is complete. The operation is executed
        for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if min_average_score < 0.0 or min_average_score > 10.0:
            raise ValueError("min_average_score must be between 0 and 10")
        self._min_average_score = min_average_score

    def assert_passes(self, run_result: EvalRunResult) -> None:
        """Assert passes for evaluation workflows.

        This EvalCIGate method belongs to the evaluation service layer. Inputs are run_result.
        It runs synchronously and returns when local processing is complete. The operation is
        executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        if run_result.average_score < self._min_average_score:
            raise EvalRegressionError(
                "Evaluation average score below threshold: "
                f"{run_result.average_score} < {self._min_average_score}"
            )
