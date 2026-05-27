from __future__ import annotations

import os
import subprocess
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
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{src_path}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else str(src_path)
    )
    result = subprocess.run([sys.executable, "-m", "pytest", *args], env=env, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
