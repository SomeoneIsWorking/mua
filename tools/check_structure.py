#!/usr/bin/env python3
"""Reject monolith growth and shared/title boundary leaks."""

from __future__ import annotations

import argparse
import pathlib
import re
import tempfile

MAX_LINES = 500
SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".h", ".hpp"}
CHECKED_SUFFIXES = SOURCE_SUFFIXES | {".py"}
FORBIDDEN_PRODUCT_NAMES = re.compile(
    r"\b(?:gears|ppc_config|PPCFuncMappings|XenonRecomp|sub_[0-9A-Fa-f]+)\b"
)
DIRECT_DIAGNOSTICS = re.compile(
    r"(?:fprintf\s*\(\s*stderr|std::c(?:err|log)\b|OutputDebugString|SDL_Log)"
)
DIRECT_ENVIRONMENT = re.compile(r"\b(?:std::)?getenv\s*\(")


def violations(root: pathlib.Path) -> list[str]:
    found: list[str] = []
    for top in ("include", "src", "tests", "tools"):
        directory = root / top
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.suffix not in CHECKED_SUFFIXES:
                continue
            relative = path.relative_to(root)
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > MAX_LINES:
                found.append(f"{relative}: {len(lines)} lines; limit is {MAX_LINES}")
            if top in ("include", "src"):
                for number, line in enumerate(lines, 1):
                    if FORBIDDEN_PRODUCT_NAMES.search(line):
                        found.append(f"{relative}:{number}: forbidden product/static dependency")
                    if path.suffix in SOURCE_SUFFIXES and DIRECT_DIAGNOSTICS.search(line):
                        found.append(f"{relative}:{number}: bypasses the configurable logger")
                    if path.suffix in SOURCE_SUFFIXES and DIRECT_ENVIRONMENT.search(line):
                        found.append(f"{relative}:{number}: bypasses the configuration owner")
    for path in sorted(root.rglob("*.sh")):
        if path.is_file() and path.relative_to(root) != pathlib.Path("run.sh"):
            found.append(f"{path.relative_to(root)}: project automation must be Python")
    return found


def selftest() -> int:
    scratch = pathlib.Path(__file__).resolve().parents[1] / "scratch"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="structure_", dir=scratch) as temporary:
        root = pathlib.Path(temporary)
        source = root / "src"
        source.mkdir()
        (source / "too_large.cpp").write_text("line\n" * 501, encoding="utf-8")
        (source / "leak.cpp").write_text(
            "void sub_82000000();\n"
            'void log() { fprintf(stderr, "bad"); }\n'
            'void config() { getenv("BAD"); }\n',
            encoding="utf-8",
        )
        (root / "probe.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        found = violations(root)
        if len(found) != 5:
            print(f"structure selftest: expected 5 refusals, observed {found}")
            return 1
    print("structure selftest: all ownership and tooling violations refused")
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
    print("structure: source, diagnostics, configuration, and tooling boundaries hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
