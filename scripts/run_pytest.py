from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: run_pytest.py <unit|integration>", file=sys.stderr)
        return 2

    suite = sys.argv[1]
    if suite == "unit":
        args = ["-q", "tests/unit"]
    elif suite == "integration":
        args = ["-q", "tests/integration"]
    else:
        print("Suite must be 'unit' or 'integration'", file=sys.stderr)
        return 2

    src_path = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src_path))

    import pytest

    return pytest.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
