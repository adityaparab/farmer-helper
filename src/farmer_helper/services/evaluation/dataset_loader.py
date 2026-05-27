import json
from pathlib import Path
from typing import Any

from farmer_helper.schemas.evaluation import EvalDataset, EvalDatasetItem


class EvalDatasetLoaderError(Exception):
    pass


class EvalDatasetLoader:
    def load(self, file_path: str | Path) -> EvalDataset:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise EvalDatasetLoaderError(f"Dataset file not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".jsonl":
            payload = self._load_jsonl(path)
        elif suffix == ".json":
            payload = self._load_json(path)
        else:
            raise EvalDatasetLoaderError(
                f"Unsupported dataset format '{suffix}'. Expected .json or .jsonl"
            )

        dataset = EvalDataset.model_validate(payload)
        self._validate_unique_ids(dataset.items)
        return dataset

    def _load_jsonl(self, path: Path) -> dict[str, Any]:
        items: list[dict[str, Any]] = []
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
            for line_number, raw_line in enumerate(lines, 1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise EvalDatasetLoaderError(
                        f"Invalid JSON at line {line_number} in {path.name}"
                    ) from exc
                if not isinstance(parsed, dict):
                    raise EvalDatasetLoaderError(
                        f"Line {line_number} in {path.name} must be a JSON object"
                    )
                items.append(parsed)
        except OSError as exc:
            raise EvalDatasetLoaderError(f"Failed to read dataset file: {path}") from exc

        if not items:
            raise EvalDatasetLoaderError(f"Dataset file is empty: {path}")

        return {"version": "v1", "items": items}

    def _load_json(self, path: Path) -> dict[str, Any]:
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvalDatasetLoaderError(f"Failed to read dataset file: {path}") from exc
        except json.JSONDecodeError as exc:
            raise EvalDatasetLoaderError(f"Invalid JSON in {path.name}") from exc

        if isinstance(parsed, dict):
            if "items" not in parsed:
                raise EvalDatasetLoaderError(
                    f"JSON dataset object must contain 'items' key: {path.name}"
                )
            return parsed

        if isinstance(parsed, list):
            return {"version": "v1", "items": parsed}

        raise EvalDatasetLoaderError(
            f"Unsupported JSON dataset shape in {path.name}; expected object or array"
        )

    def _validate_unique_ids(self, items: list[EvalDatasetItem]) -> None:
        seen: set[str] = set()
        for item in items:
            if item.id in seen:
                raise EvalDatasetLoaderError(f"Duplicate eval item id: {item.id}")
            seen.add(item.id)
