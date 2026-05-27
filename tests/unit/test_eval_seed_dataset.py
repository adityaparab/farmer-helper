from pathlib import Path

from farmer_helper.services.evaluation.dataset_loader import EvalDatasetLoader


def test_seed_dataset_has_stable_id_order_and_unique_items() -> None:
    dataset_path = (
        Path(__file__).resolve().parents[2] / "docs" / "evaluation" / "EVAL_DATASET_SEED.jsonl"
    )

    dataset = EvalDatasetLoader().load(str(dataset_path))
    ids = [item.id for item in dataset.items]

    assert len(ids) >= 15
    assert ids == sorted(ids)
    assert len(set(ids)) == len(ids)


def test_seed_dataset_covers_refusal_and_high_confidence_cases() -> None:
    dataset_path = (
        Path(__file__).resolve().parents[2] / "docs" / "evaluation" / "EVAL_DATASET_SEED.jsonl"
    )

    dataset = EvalDatasetLoader().load(str(dataset_path))

    assert any(not item.must_cite_source for item in dataset.items)
    assert any(item.must_cite_source for item in dataset.items)
    assert any(item.difficulty == "hard" for item in dataset.items)
    assert any(item.difficulty == "easy" for item in dataset.items)
