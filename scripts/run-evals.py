from __future__ import annotations

import argparse
from pathlib import Path

from farmer_helper.services.evaluation.ci_gate import EvalCIGate, EvalRegressionError
from farmer_helper.services.evaluation.dataset_loader import EvalDatasetLoader
from farmer_helper.services.evaluation.reporting import EvalOfflineReportBuilder
from farmer_helper.services.evaluation.runner import EvalRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run offline evaluation dataset checks")
    parser.add_argument(
        "--dataset",
        default="docs/evaluation/EVAL_DATASET_SEED.jsonl",
        help="Path to eval dataset file (.json or .jsonl)",
    )
    parser.add_argument(
        "--min-average-score",
        type=float,
        default=6.0,
        help="Minimum average score required to pass the eval gate",
    )
    parser.add_argument(
        "--report-out",
        default="artifacts/eval-report.json",
        help="Output path for generated eval report JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    dataset = EvalDatasetLoader().load(args.dataset)
    run_result = EvalRunner().run(dataset)
    report = EvalOfflineReportBuilder().build(run_result)

    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(EvalOfflineReportBuilder.to_json(report), encoding="utf-8")

    print(
        "Eval completed:",
        f"items={run_result.total_items}",
        f"passed={run_result.passed_items}",
        f"failed={run_result.failed_items}",
        f"average={run_result.average_score}",
        f"report={report_path}",
    )

    try:
        EvalCIGate(min_average_score=args.min_average_score).assert_passes(run_result)
    except EvalRegressionError as exc:
        print(f"Eval gate failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
