from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from shutil import which

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_ROOT = REPO_ROOT / "frontend"
FRONTEND_PREFIX = "frontend/"


def _normalize_paths(paths: list[str]) -> list[str]:
    normalized_paths: list[str] = []
    for raw_path in paths:
        normalized_path = raw_path.replace("\\", "/")
        if not normalized_path.startswith(FRONTEND_PREFIX):
            continue
        normalized_paths.append(normalized_path.removeprefix(FRONTEND_PREFIX))
    return normalized_paths


def main() -> int:
    args = sys.argv[1:]
    fix_mode = False
    if args and args[0] == "--fix":
        fix_mode = True
        args = args[1:]

    target_paths = _normalize_paths(args)
    if not target_paths:
        return 0

    npm_executable = which("npm.cmd") or which("npm")
    if npm_executable is None:
        raise FileNotFoundError("npm executable was not found on PATH")

    command = [npm_executable, "exec", "eslint"]
    if fix_mode:
        command.append("--fix")
    command.extend(target_paths)
    result = subprocess.run(command, cwd=FRONTEND_ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
