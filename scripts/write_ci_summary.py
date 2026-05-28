from __future__ import annotations

import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _summary_path() -> Path:
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        raise RuntimeError("GITHUB_STEP_SUMMARY is not set")
    return Path(summary)


def _append_coverage_summary(report_path: Path, summary_path: Path, title: str) -> None:
    root = ET.parse(report_path).getroot()
    lines_valid = int(root.attrib.get("lines-valid", "0"))
    lines_covered = int(root.attrib.get("lines-covered", "0"))
    line_rate = float(root.attrib.get("line-rate", "0")) * 100

    classes: list[tuple[float, str]] = []
    for package in root.findall("./packages/package"):
        for class_node in package.findall("./classes/class"):
            filename = class_node.attrib.get("filename", "unknown")
            class_rate = float(class_node.attrib.get("line-rate", "0")) * 100
            classes.append((class_rate, filename))

    lowest_covered = sorted(classes, key=lambda item: item[0])[:5]

    with summary_path.open("a", encoding="utf-8") as handle:
        handle.write(f"## {title}\n\n")
        handle.write(f"- Lines covered: {lines_covered}/{lines_valid} ({line_rate:.2f}%)\n")
        if lowest_covered:
            handle.write("- Lowest covered files:\n")
            for class_rate, filename in lowest_covered:
                handle.write(f"  - {filename}: {class_rate:.2f}%\n")
        handle.write("\n")


def _append_eval_summary(report_path: Path, summary_path: Path, title: str) -> None:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    summary = payload["summary"]
    failed_items = [item for item in payload["items"] if not item["passed"]]

    with summary_path.open("a", encoding="utf-8") as handle:
        handle.write(f"## {title}\n\n")
        handle.write(f"- Dataset version: {payload['dataset_version']}\n")
        handle.write(f"- Average score: {summary['average_score']:.4f}\n")
        handle.write(f"- Passed items: {summary['passed_items']}/{summary['total_items']}\n")
        handle.write(f"- Failed items: {summary['failed_items']}\n")
        if failed_items:
            handle.write("\n| ID | Score | Question |\n")
            handle.write("| --- | ---: | --- |\n")
            for item in failed_items[:10]:
                question = item["question"].replace("|", "\\|")
                handle.write(
                    f"| {item['id']} | {item['total_score']}/{item['max_score']} | {question} |\n"
                )
        handle.write("\n")


def main() -> int:
    if len(sys.argv) not in {3, 4}:
        print(
            "Usage: python scripts/write_ci_summary.py <coverage|eval> <report_path> [title]",
            file=sys.stderr,
        )
        return 2

    report_kind = sys.argv[1]
    report_path = Path(sys.argv[2])
    title = (
        sys.argv[3]
        if len(sys.argv) == 4
        else ("Coverage Report" if report_kind == "coverage" else "Eval Report")
    )
    summary_path = _summary_path()

    if report_kind == "coverage":
        _append_coverage_summary(report_path, summary_path, title)
        return 0
    if report_kind == "eval":
        _append_eval_summary(report_path, summary_path, title)
        return 0

    print("Report kind must be 'coverage' or 'eval'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
