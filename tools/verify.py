#!/usr/bin/env python3
"""Run MUA's source, provisioning, and structure gates."""

from __future__ import annotations

import pathlib
import subprocess
import sys
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(label: str, command: Sequence[str]) -> bool:
    print(f"verify: {label}")
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode == 0:
        return True
    print(f"verify: {label} failed with exit {result.returncode}", file=sys.stderr)
    return False


def main() -> int:
    commands = (
        ("Python format", ("ruff", "format", "--check", "tools", "tests")),
        ("Python lint", ("ruff", "check", "tools", "tests")),
        ("provisioning tests", (sys.executable, "-m", "unittest", "tests/test_provision.py")),
        ("structure", (sys.executable, "tools/check_structure.py")),
        ("structure discriminator", (sys.executable, "tools/check_structure.py", "--selftest")),
    )
    failures = sum(not run(label, command) for label, command in commands)
    if failures:
        print(f"verify: FAILED ({failures} gate(s))", file=sys.stderr)
        return 1
    print("verify: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
