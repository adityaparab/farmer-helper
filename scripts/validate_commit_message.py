from __future__ import annotations

import re
import sys
from pathlib import Path

COMMIT_MESSAGE_PATTERN = re.compile(
    r"^(?P<type>feat|fix|docs|refactor|test|chore|ci|build|perf|style|revert)"
    r"(\([a-z0-9._-]+\))?"
    r"(!)?: [^\s].*$"
)


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage: validate_commit_message.py <commit-message-file>",
            file=sys.stderr,
        )
        return 2

    message_path = Path(sys.argv[1])
    message = message_path.read_text(encoding="utf-8").strip().splitlines()[0].strip()

    if COMMIT_MESSAGE_PATTERN.match(message):
        return 0

    print(
        "Commit message must use conventional commit format like "
        "feat(scope): summary, fix: summary, or chore: summary.",
        file=sys.stderr,
    )
    print(f"Invalid commit message: {message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
