#!/usr/bin/env python3
"""Provision and verify the exact user-owned MUA Gold Xbox 360 disc."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV_DISC = "MUA_X360_ISO"
ENV_INSPECTOR = "X360PORT_XEX_INSPECT"
ENV_XDVDFS = "XDVDFS"
DROP_IN_SUFFIXES = frozenset({".img", ".iso", ".xgd", ".xiso"})
HASH_CHUNK_SIZE = 1024 * 1024
HEX_8 = re.compile(r"[0-9a-f]{8}\Z")
HELPER_NAMES = (
    "restgprlr_14",
    "savegprlr_14",
    "restfpr_14",
    "savefpr_14",
    "restvmx_14",
    "savevmx_14",
    "restvmx_64",
    "savevmx_64",
)


class ProvisionError(RuntimeError):
    """Provisioning cannot prove the exact requested title profile."""


@dataclass(frozen=True)
class ResolvedDisc:
    path: pathlib.Path
    source: str


def _absolute(path: pathlib.Path, base: pathlib.Path) -> pathlib.Path:
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _regular_file(path: pathlib.Path, label: str) -> pathlib.Path:
    if not path.exists():
        raise ProvisionError(f"{label} does not exist: {path}")
    if not path.is_file():
        raise ProvisionError(f"{label} is not a regular file: {path}")
    return path


def _dotenv_value(path: pathlib.Path, key: str) -> str | None:
    if not path.exists():
        return None
    _regular_file(path, "environment file")
    matches: list[str] = []
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        name, separator, raw_value = line.partition("=")
        if not separator or name.strip() != key:
            continue
        value = raw_value.strip()
        if value[:1] in {"'", '"'}:
            quote = value[0]
            if len(value) < 2 or value[-1] != quote:
                raise ProvisionError(f"{path}:{number}: unterminated quoted {key} value")
            value = value[1:-1]
        if not value:
            continue
        matches.append(value)
    if len(matches) > 1:
        raise ProvisionError(f"{path} defines {key} more than once")
    return matches[0] if matches else None


def resolve_disc(
    explicit: str | os.PathLike[str] | None,
    repo_root: pathlib.Path = ROOT,
    environ: Mapping[str, str] | None = None,
    current_directory: pathlib.Path | None = None,
) -> ResolvedDisc:
    """Resolve explicit CLI input, then environment/.env, then one drop-in."""

    root = repo_root.resolve()
    environment = os.environ if environ is None else environ
    cwd = pathlib.Path.cwd() if current_directory is None else current_directory
    if explicit is not None:
        selected = _absolute(pathlib.Path(explicit), cwd)
        return ResolvedDisc(_regular_file(selected, "explicit disc image"), "explicit")
    if value := environment.get(ENV_DISC):
        selected = _absolute(pathlib.Path(value), root)
        return ResolvedDisc(_regular_file(selected, f"{ENV_DISC} disc image"), "environment")
    if value := _dotenv_value(root / ".env", ENV_DISC):
        selected = _absolute(pathlib.Path(value), root)
        return ResolvedDisc(_regular_file(selected, f"{ENV_DISC} disc image from .env"), "dotenv")

    drop_in = root / "roms"
    if not drop_in.is_dir():
        raise ProvisionError(f"no disc selected and drop-in directory is missing: {drop_in}")
    candidates = sorted(
        path.resolve()
        for path in drop_in.iterdir()
        if path.is_file() and path.suffix.lower() in DROP_IN_SUFFIXES
    )
    if not candidates:
        raise ProvisionError(f"no supported Xbox 360 disc image found in {drop_in}")
    if len(candidates) != 1:
        names = ", ".join(path.name for path in candidates)
        raise ProvisionError(f"ambiguous drop-in disc images: {names}; select one explicitly")
    return ResolvedDisc(candidates[0], "drop-in")


def sha256_file(path: pathlib.Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with _regular_file(path, "SHA-256 input").open("rb") as source:
        while chunk := source.read(HASH_CHUNK_SIZE):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def load_profile(path: pathlib.Path) -> dict[str, object]:
    try:
        with path.open("rb") as source:
            profile = tomllib.load(source)
        title = profile["title"]
        image = profile["image"]
        return {
            "disc_sha256": str(title["disc_sha256"]).lower(),
            "xex_sha256": str(title["xex_sha256"]).lower(),
            "image_sha256": str(title["image_sha256"]).lower(),
            "title_id": str(title["title_id"]).lower(),
            "media_id": str(title["media_id"]).lower(),
            "image_base": f"{int(image['base']):08x}",
            "image_size": int(image["size"]),
            "image_entry": f"{int(image['entry']):08x}",
        }
    except (KeyError, OSError, TypeError, ValueError, tomllib.TOMLDecodeError) as error:
        raise ProvisionError(f"invalid title profile {path}: {error}") from error


def _field(document: object, path: str) -> object:
    current = document
    for component in path.split("."):
        if not isinstance(current, dict) or component not in current:
            raise ProvisionError(f"x360-xex-inspect output is missing {path}")
        current = current[component]
    return current


def _expect(document: object, path: str, expected: object) -> None:
    observed = _field(document, path)
    if observed != expected:
        raise ProvisionError(f"{path} mismatch: expected {expected!r}, observed {observed!r}")


def validate_inspection(profile: Mapping[str, object], inspection: object) -> None:
    _expect(inspection, "schema", 1)
    _expect(inspection, "format", "XEX2")
    _expect(inspection, "xex.sha256", profile["xex_sha256"])
    _expect(inspection, "execution.title_id", profile["title_id"])
    _expect(inspection, "execution.media_id", profile["media_id"])
    _expect(inspection, "image.sha256", profile["image_sha256"])
    _expect(inspection, "image.base", profile["image_base"])
    _expect(inspection, "image.size", profile["image_size"])
    _expect(inspection, "image.entry", profile["image_entry"])

    sections = _field(inspection, "sections")
    imports = _field(inspection, "imports")
    helpers = _field(inspection, "helpers")
    if not isinstance(sections, list) or not sections:
        raise ProvisionError("sections must be a nonempty code range list")
    for index, section in enumerate(sections):
        if (
            not isinstance(section, dict)
            or not isinstance(section.get("name"), str)
            or not isinstance(section.get("base"), str)
            or HEX_8.fullmatch(section["base"]) is None
            or not isinstance(section.get("size"), int)
            or isinstance(section["size"], bool)
            or section["size"] <= 0
            or not isinstance(section.get("code"), bool)
        ):
            raise ProvisionError(f"sections[{index}] has invalid schema")
    if not any(section["code"] for section in sections):
        raise ProvisionError("sections must contain at least one explicit code range")
    if not isinstance(imports, list) or not imports:
        raise ProvisionError("imports must be a nonempty list")
    identities: set[tuple[str, int]] = set()
    for index, imported in enumerate(imports):
        if not isinstance(imported, dict):
            raise ProvisionError(f"imports[{index}] must be an object")
        kind = imported.get("kind")
        library = imported.get("library")
        ordinal = imported.get("ordinal")
        name = imported.get("name")
        address = imported.get("address")
        record_address = imported.get("record_address")
        if (
            kind not in {"function", "variable"}
            or not isinstance(library, str)
            or not library
            or not isinstance(ordinal, int)
            or isinstance(ordinal, bool)
            or not isinstance(name, str)
            or not name
            or not isinstance(address, str)
            or HEX_8.fullmatch(address) is None
            or not isinstance(record_address, str)
            or HEX_8.fullmatch(record_address) is None
        ):
            raise ProvisionError(f"imports[{index}] has invalid logical-import schema")
        identity = (library, ordinal)
        if identity in identities:
            raise ProvisionError(f"imports contains duplicate identity {library} ordinal {ordinal}")
        identities.add(identity)
    if not isinstance(helpers, dict):
        raise ProvisionError("helpers must be an object")
    for name in HELPER_NAMES:
        addresses = helpers.get(name)
        if (
            not isinstance(addresses, list)
            or len(addresses) != 1
            or not isinstance(addresses[0], str)
            or HEX_8.fullmatch(addresses[0]) is None
        ):
            raise ProvisionError(f"helpers.{name} must contain exactly one address")


def _tool(
    explicit: pathlib.Path | None,
    environment_key: str,
    command: str,
    repo_root: pathlib.Path = ROOT,
    environ: Mapping[str, str] | None = None,
    current_directory: pathlib.Path | None = None,
) -> pathlib.Path:
    root = repo_root.resolve()
    environment = os.environ if environ is None else environ
    cwd = pathlib.Path.cwd() if current_directory is None else current_directory
    if explicit is not None:
        return _regular_file(_absolute(explicit, cwd), f"explicit {command} executable")
    if value := environment.get(environment_key):
        selected = _absolute(pathlib.Path(value), root)
        return _regular_file(selected, f"{environment_key} executable")
    if value := _dotenv_value(root / ".env", environment_key):
        selected = _absolute(pathlib.Path(value), root)
        return _regular_file(selected, f"{environment_key} executable from .env")
    found = shutil.which(command)
    if found is None:
        raise ProvisionError(f"{command} is unavailable; pass its path or set {environment_key}")
    return pathlib.Path(found).resolve()


def _run(command: Sequence[str], label: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise ProvisionError(f"{label} failed: {detail}")
    return result


def _provision_directory(root: pathlib.Path, digest: str) -> pathlib.Path:
    ignore = root / ".gitignore"
    if not ignore.is_file() or "scratch/" not in ignore.read_text(encoding="utf-8").splitlines():
        raise ProvisionError(".gitignore must ignore scratch/ before provisioning assets")
    directory = root / "scratch" / "titles" / digest / "provision"
    for path in (root / "scratch", root / "scratch" / "titles", directory):
        if path.is_symlink():
            raise ProvisionError(f"refusing provision output through symlink: {path}")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def provision(
    disc: ResolvedDisc,
    profile_path: pathlib.Path,
    inspector: pathlib.Path,
    xdvdfs: pathlib.Path,
    repo_root: pathlib.Path = ROOT,
) -> pathlib.Path:
    profile = load_profile(profile_path)
    disc_digest, disc_size = sha256_file(disc.path)
    if disc_digest != profile["disc_sha256"]:
        raise ProvisionError(
            f"disc.sha256 mismatch: expected {profile['disc_sha256']!r}, observed {disc_digest!r}"
        )

    output = _provision_directory(repo_root.resolve(), disc_digest)
    nonce = str(os.getpid())
    temporary_xex = output / f".default.xex.{nonce}.tmp"
    temporary_image = output / f".image.bin.{nonce}.tmp"
    temporary_inspection = output / f".inspection.json.{nonce}.tmp"
    temporary_paths = (temporary_xex, temporary_image, temporary_inspection)
    try:
        _run(
            [str(xdvdfs), "copy-out", str(disc.path), "default.xex", str(temporary_xex)],
            "default.xex extraction",
        )
        inspected = _run(
            [str(inspector), str(temporary_xex), "--image-out", str(temporary_image)],
            "x360-xex-inspect",
        )
        try:
            inspection = json.loads(inspected.stdout)
        except json.JSONDecodeError as error:
            raise ProvisionError(f"x360-xex-inspect returned invalid JSON: {error}") from error
        validate_inspection(profile, inspection)
        temporary_inspection.write_text(
            json.dumps(inspection, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        os.replace(temporary_xex, output / "default.xex")
        os.replace(temporary_image, output / "image.bin")
        os.replace(temporary_inspection, output / "inspection.json")
    finally:
        for temporary in temporary_paths:
            if temporary.exists() and temporary.is_file() and temporary.parent == output:
                temporary.unlink()

    print(f"verified {disc.source} disc: {disc_digest} ({disc_size} bytes)", file=sys.stderr)
    return output / "inspection.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc", nargs="?", help="explicit user-owned Xbox 360 disc image")
    parser.add_argument("--profile", type=pathlib.Path, default=ROOT / "config" / "mua.toml")
    parser.add_argument("--xex-inspect", type=pathlib.Path)
    parser.add_argument("--xdvdfs", type=pathlib.Path)
    parser.add_argument("--repo-root", type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        root = arguments.repo_root.resolve()
        disc = resolve_disc(arguments.disc, root)
        inspector = _tool(arguments.xex_inspect, ENV_INSPECTOR, "x360-xex-inspect", root)
        xdvdfs = _tool(arguments.xdvdfs, ENV_XDVDFS, "xdvdfs", root)
        manifest = provision(disc, arguments.profile.resolve(), inspector, xdvdfs, root)
    except (OSError, ProvisionError) as error:
        print(f"provision: REFUSING: {error}", file=sys.stderr)
        return 2
    print(manifest.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
