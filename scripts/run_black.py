from __future__ import annotations

import os
import subprocess
import sys
import tempfile


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-cache-") as cache_dir:
        env = os.environ.copy()
        env["BLACK_CACHE_DIR"] = cache_dir
        result = subprocess.run(
            [sys.executable, "-m", "black", *sys.argv[1:]],
            env=env,
        )
        return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
