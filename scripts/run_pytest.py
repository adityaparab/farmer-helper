from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    suite = sys.argv[1] if len(sys.argv) == 2 else "all"
    if suite == "unit":
        args = ["-q", "tests/unit"]
    elif suite == "integration":
        args = ["-q", "tests/integration"]
    elif suite == "all":
        args = ["-q"]
    else:
        print("Suite must be 'unit', 'integration', or 'all'", file=sys.stderr)
        return 2

    src_path = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src_path))

    import pytest

    return pytest.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
