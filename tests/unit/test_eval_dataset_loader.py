import json
from pathlib import Path

import pytest

from farmer_helper.services.evaluation.dataset_loader import (
    EvalDatasetLoader,
    EvalDatasetLoaderError,
)


def test_eval_dataset_loader_reads_jsonl_file(tmp_path: Path) -> None:
    dataset_path = tmp_path / "eval.jsonl"
    dataset_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "Q001",
                        "question": "What causes low crop yield?",
                        "expected_topics": ["soil health", "water"],
                        "expected_keywords": ["yield", "rain-fed"],
                        "must_cite_source": True,
                        "difficulty": "easy",
                        "notes": "seed",
                    }
                ),
                json.dumps(
                    {
                        "id": "Q002",
                        "question": "How to improve retention?",
                        "expected_topics": ["mulching"],
                        "expected_keywords": ["water"],
                        "must_cite_source": True,
                        "difficulty": "medium",
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    loader = EvalDatasetLoader()
    dataset = loader.load(dataset_path)

    assert dataset.version == "v1"
    assert len(dataset.items) == 2
    assert dataset.items[0].id == "Q001"


def test_eval_dataset_loader_reads_json_object_file(tmp_path: Path) -> None:
    dataset_path = tmp_path / "eval.json"
    dataset_path.write_text(
        json.dumps(
            {
                "version": "v2",
                "items": [
                    {
                        "id": "Q003",
                        "question": "When to refuse unsupported recommendation?",
                        "expected_topics": ["safety"],
                        "expected_keywords": ["unsupported"],
                        "must_cite_source": False,
                        "difficulty": "hard",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    loader = EvalDatasetLoader()
    dataset = loader.load(dataset_path)

    assert dataset.version == "v2"
    assert dataset.items[0].id == "Q003"


def test_eval_dataset_loader_rejects_duplicate_ids(tmp_path: Path) -> None:
    dataset_path = tmp_path / "eval.jsonl"
    line = json.dumps(
        {
            "id": "Q001",
            "question": "What causes low crop yield?",
            "expected_topics": ["soil health"],
            "expected_keywords": ["yield"],
            "must_cite_source": True,
            "difficulty": "easy",
        }
    )
    dataset_path.write_text("\n".join([line, line]), encoding="utf-8")

    loader = EvalDatasetLoader()

    with pytest.raises(EvalDatasetLoaderError) as exc:
        loader.load(dataset_path)

    assert "Duplicate eval item id" in str(exc.value)


def test_eval_dataset_loader_rejects_invalid_jsonl_line(tmp_path: Path) -> None:
    dataset_path = tmp_path / "eval.jsonl"
    dataset_path.write_text("{not-json}\n", encoding="utf-8")

    loader = EvalDatasetLoader()

    with pytest.raises(EvalDatasetLoaderError) as exc:
        loader.load(dataset_path)

    assert "Invalid JSON at line" in str(exc.value)


def test_eval_dataset_loader_rejects_unsupported_extension(tmp_path: Path) -> None:
    dataset_path = tmp_path / "eval.txt"
    dataset_path.write_text("x", encoding="utf-8")

    loader = EvalDatasetLoader()

    with pytest.raises(EvalDatasetLoaderError) as exc:
        loader.load(dataset_path)

    assert "Unsupported dataset format" in str(exc.value)
