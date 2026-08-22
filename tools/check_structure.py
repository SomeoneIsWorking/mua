#!/usr/bin/env python3
"""Reject monolith growth and shared/title boundary leaks."""

from __future__ import annotations

import argparse
import pathlib
import re
import tempfile

MAX_LINES = 500
SUFFIXES = {".cpp", ".hpp", ".py"}
FORBIDDEN_SHARED_NAMES = re.compile(r"\b(?:gears|ppc_config|PPCFuncMappings|sub_[0-9A-Fa-f]+)\b")


def violations(root: pathlib.Path):
    found = []
    for top in ("include", "src", "tests", "tools"):
        directory = root / top
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.suffix not in SUFFIXES:
                continue
            relative = path.relative_to(root)
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > MAX_LINES:
                found.append(f"{relative}: {len(lines)} lines; limit is {MAX_LINES}")
            if top in ("include", "src"):
                for number, line in enumerate(lines, 1):
                    if FORBIDDEN_SHARED_NAMES.search(line):
                        found.append(f"{relative}:{number}: forbidden shared/generated title name")
    return found


def selftest() -> int:
    scratch = pathlib.Path(__file__).resolve().parents[1] / "scratch"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="structure_", dir=scratch) as temporary:
        root = pathlib.Path(temporary)
        source = root / "src"
        source.mkdir()
        (source / "too_large.cpp").write_text("line\n" * 501, encoding="utf-8")
        (source / "leak.cpp").write_text("void sub_82000000();\n", encoding="utf-8")
        found = violations(root)
        if len(found) != 2:
            print(f"structure selftest: expected 2 refusals, observed {found}")
            return 1
    print("structure selftest: oversized source and generated title leak refused")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    root = pathlib.Path(__file__).resolve().parents[1]
    found = violations(root)
    for violation in found:
        print(f"structure: {violation}")
    if found:
        return 1
    print("structure: source ownership and title/shared boundaries hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
