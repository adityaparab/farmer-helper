from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
VERSION_PATTERN = re.compile(r'^__version__ = "(?P<version>[^"]+)"$', re.MULTILINE)

REPO_ROOT = Path(__file__).resolve().parents[1]
ABOUT_FILE = REPO_ROOT / "src" / "farmer_helper" / "__about__.py"
FRONTEND_PACKAGE_FILE = REPO_ROOT / "frontend" / "package.json"
FRONTEND_LOCK_FILE = REPO_ROOT / "frontend" / "package-lock.json"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read and update Farmer Helper semver release versions."
    )
    parser.add_argument(
        "--release-type",
        choices=("major", "minor", "patch"),
        help="Semver bump to apply from the current version.",
    )
    parser.add_argument(
        "--set-version",
        help="Explicit semver version to set. Must be greater than the current version.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the resolved version to tracked version files.",
    )
    parser.add_argument(
        "--check-sync",
        action="store_true",
        help="Validate that backend and frontend version files are in sync.",
    )
    return parser.parse_args()


def _parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError(f"Invalid semantic version: {value}")
    return tuple(int(group) for group in match.groups())


def _read_about_version() -> str:
    content = ABOUT_FILE.read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(content)
    if match is None:
        raise ValueError(f"Could not find __version__ in {ABOUT_FILE}")
    return match.group("version")


def _read_frontend_versions() -> dict[str, str]:
    package_json = json.loads(FRONTEND_PACKAGE_FILE.read_text(encoding="utf-8"))
    package_lock = json.loads(FRONTEND_LOCK_FILE.read_text(encoding="utf-8"))
    root_package = package_lock.get("packages", {}).get("", {})
    return {
        "frontend/package.json": str(package_json["version"]),
        "frontend/package-lock.json": str(package_lock["version"]),
        "frontend/package-lock.json#packages['']": str(root_package.get("version", "")),
    }


def _assert_versions_match(expected_version: str) -> None:
    mismatches = [
        f"{path}={value}"
        for path, value in _read_frontend_versions().items()
        if value != expected_version
    ]
    if mismatches:
        mismatch_summary = ", ".join(mismatches)
        raise ValueError(
            "Version files are out of sync with src/farmer_helper/__about__.py: "
            f"{mismatch_summary}"
        )


def _resolve_target_version(current_version: str, args: argparse.Namespace) -> str:
    explicit_version = args.set_version
    if explicit_version:
        _parse_semver(explicit_version)
        if _parse_semver(explicit_version) <= _parse_semver(current_version):
            raise ValueError(
                "Explicit version "
                f"{explicit_version} must be greater than current version {current_version}"
            )
        return explicit_version

    release_type = args.release_type
    if release_type is None:
        return current_version

    major, minor, patch = _parse_semver(current_version)
    if release_type == "major":
        return f"{major + 1}.0.0"
    if release_type == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def _write_versions(target_version: str) -> None:
    about_content = ABOUT_FILE.read_text(encoding="utf-8")
    updated_about = VERSION_PATTERN.sub(f'__version__ = "{target_version}"', about_content, count=1)
    ABOUT_FILE.write_text(updated_about, encoding="utf-8")

    package_json = json.loads(FRONTEND_PACKAGE_FILE.read_text(encoding="utf-8"))
    package_json["version"] = target_version
    FRONTEND_PACKAGE_FILE.write_text(json.dumps(package_json, indent=2) + "\n", encoding="utf-8")

    package_lock = json.loads(FRONTEND_LOCK_FILE.read_text(encoding="utf-8"))
    package_lock["version"] = target_version
    package_lock.setdefault("packages", {}).setdefault("", {})["version"] = target_version
    FRONTEND_LOCK_FILE.write_text(json.dumps(package_lock, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = _parse_args()
    current_version = _read_about_version()
    _parse_semver(current_version)

    if args.check_sync:
        _assert_versions_match(current_version)

    target_version = _resolve_target_version(current_version, args)
    if args.apply and target_version != current_version:
        _write_versions(target_version)

    if args.apply or args.check_sync:
        _assert_versions_match(target_version)

    print(target_version)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
