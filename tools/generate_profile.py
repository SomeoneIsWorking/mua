#!/usr/bin/env python3
"""Generate the C++ MUA title profile from its single TOML authority."""

from __future__ import annotations

import argparse
import pathlib
import tempfile
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ProfileError(ValueError):
    """The title profile cannot describe an exact Xenon image."""


def _hex_u32(value: object, label: str) -> int:
    if not isinstance(value, str) or len(value) != 8:
        raise ProfileError(f"{label} must be exactly eight hexadecimal digits")
    try:
        parsed = int(value, 16)
    except ValueError as error:
        raise ProfileError(f"{label} is not hexadecimal") from error
    return parsed


def _digest(value: object, label: str) -> bytes:
    if not isinstance(value, str) or len(value) != 64:
        raise ProfileError(f"{label} must be exactly 64 hexadecimal digits")
    try:
        parsed = bytes.fromhex(value)
    except ValueError as error:
        raise ProfileError(f"{label} is not hexadecimal") from error
    if not any(parsed):
        raise ProfileError(f"{label} cannot be the zero digest")
    return parsed


def _u32(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 0xFFFFFFFF:
        raise ProfileError(f"{label} must be a 32-bit unsigned integer")
    return value


def _array(data: bytes) -> str:
    return ", ".join(f"0x{byte:02x}" for byte in data)


def render(path: pathlib.Path) -> str:
    with path.open("rb") as source:
        document = tomllib.load(source)
    try:
        title = document["title"]
        image = document["image"]
        name = title["name"]
    except (KeyError, TypeError) as error:
        raise ProfileError(f"missing profile field: {error}") from error
    if not isinstance(name, str) or not name:
        raise ProfileError("title.name must be a non-empty string")
    title_id = _hex_u32(title.get("title_id"), "title.title_id")
    media_id = _hex_u32(title.get("media_id"), "title.media_id")
    disc_sha = _digest(title.get("disc_sha256"), "title.disc_sha256")
    xex_sha = _digest(title.get("xex_sha256"), "title.xex_sha256")
    image_sha = _digest(title.get("image_sha256"), "title.image_sha256")
    base = _u32(image.get("base"), "image.base")
    size = _u32(image.get("size"), "image.size")
    entry = _u32(image.get("entry"), "image.entry")
    end = base + size
    if size == 0 or end > 0x100000000 or base & 3 or entry & 3 or not base <= entry < end:
        raise ProfileError("image range must be aligned, non-empty, 32-bit, and contain entry")
    escaped_name = name.replace("\\", "\\\\").replace('"', '\\"')
    return f"""#ifndef MUA_GENERATED_PROFILE_DATA_HPP
#define MUA_GENERATED_PROFILE_DATA_HPP

#include "xenon_host/guest_module.hpp"

#include <cstdint>

namespace mua::generated
{{
inline constexpr char Name[] = "{escaped_name}";
inline constexpr std::uint32_t TitleId = 0x{title_id:08x}U;
inline constexpr std::uint32_t MediaId = 0x{media_id:08x}U;
inline constexpr xenon_host::Sha256Digest DiscSha256 = {{{_array(disc_sha)}}};
inline constexpr xenon_host::Sha256Digest XexSha256 = {{{_array(xex_sha)}}};
inline constexpr xenon_host::Sha256Digest ImageSha256 = {{{_array(image_sha)}}};
inline constexpr std::uint32_t ImageBase = 0x{base:08x}U;
inline constexpr std::uint32_t ImageSize = 0x{size:08x}U;
inline constexpr std::uint32_t EntryPoint = 0x{entry:08x}U;
}} // namespace mua::generated

#endif
"""


def selftest() -> int:
    scratch = ROOT / "scratch"
    scratch.mkdir(exist_ok=True)
    checks = []
    with tempfile.TemporaryDirectory(prefix="profile_", dir=scratch) as temporary:
        root = pathlib.Path(temporary)
        positive = root / "positive.toml"
        positive_text = f"""[title]
name = "Synthetic"
title_id = "00000001"
media_id = "00000002"
disc_sha256 = "{'01' * 32}"
xex_sha256 = "{'02' * 32}"
image_sha256 = "{'03' * 32}"
[image]
base = 0x82000000
size = 0x1000
entry = 0x82000004
"""
        positive.write_text(positive_text, encoding="utf-8")
        checks.append(("valid profile", "EntryPoint = 0x82000004U" in render(positive)))
        invalid = root / "invalid.toml"
        invalid.write_text(positive_text.replace("01" * 32, "zz" + "01" * 31, 1),
                           encoding="utf-8")
        try:
            render(invalid)
            refused = False
        except ProfileError:
            refused = True
        checks.append(("invalid digest refusal", refused))
    for label, passed in checks:
        print(f"{'ok  ' if passed else 'FAIL'} {label}")
    print(f"profile generator selftest: {sum(result for _, result in checks)} of {len(checks)}")
    return 0 if all(result for _, result in checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=pathlib.Path)
    parser.add_argument("output", nargs="?", type=pathlib.Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.input is None or args.output is None:
        parser.error("input and output are required unless --selftest is used")
    try:
        generated = render(args.input)
    except (OSError, ProfileError, tomllib.TOMLDecodeError) as error:
        parser.error(str(error))
    args.output.write_text(generated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
