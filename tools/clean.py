#!/usr/bin/env python3
"""Remove only named MUA build trees below the repository scratch directory."""

from __future__ import annotations

import argparse
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWED = {"build", "build-sanitize"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+", choices=sorted(ALLOWED))
    args = parser.parse_args()
    scratch = (ROOT / "scratch").resolve()
    for name in args.targets:
        target = (scratch / name).resolve()
        if target.parent != scratch:
            parser.error(f"refusing target outside scratch: {target}")
        if target.exists():
            shutil.rmtree(target)
            print(f"removed {target.relative_to(ROOT)}")
        else:
            print(f"already absent: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
