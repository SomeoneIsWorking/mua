#!/usr/bin/env python3
"""Discriminator tests for MUA's exact-media provisioning policy."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mua_provision", ROOT / "tools" / "provision.py")
assert SPEC is not None and SPEC.loader is not None
provision = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = provision
SPEC.loader.exec_module(provision)


def exact_profile() -> dict[str, object]:
    return {
        "disc_sha256": "11" * 32,
        "xex_sha256": "22" * 32,
        "image_sha256": "33" * 32,
        "title_id": "415607da",
        "media_id": "5a20a6d4",
        "image_base": "82000000",
        "image_size": 0xD00000,
        "image_entry": "824806d8",
    }


def exact_inspection() -> dict[str, object]:
    return {
        "schema": 1,
        "format": "XEX2",
        "xex": {"sha256": "22" * 32, "size": 100},
        "execution": {"title_id": "415607da", "media_id": "5a20a6d4"},
        "image": {
            "sha256": "33" * 32,
            "base": "82000000",
            "size": 0xD00000,
            "entry": "824806d8",
        },
        "sections": [{"name": ".text", "base": "82000000", "size": 4, "code": True}],
        "imports": [
            {
                "kind": "function",
                "library": "xam.xex",
                "ordinal": 1,
                "name": "__imp__Function",
                "address": "82000010",
                "record_address": "82000000",
            },
            {
                "kind": "variable",
                "library": "xboxkrnl.exe",
                "ordinal": 2,
                "name": "__imp__Variable",
                "address": "82000020",
                "record_address": "82000020",
            },
        ],
        "helpers": {name: ["82000000"] for name in provision.HELPER_NAMES},
    }


class ProvisionTests(unittest.TestCase):
    def setUp(self) -> None:
        scratch = ROOT / "scratch"
        scratch.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="provision_test_", dir=scratch)
        self.root = Path(self.temporary.name)
        (self.root / "roms").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def image(self, relative: str, content: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_resolution_priority_and_no_fallback(self) -> None:
        explicit = self.image("explicit.iso", b"explicit")
        environment = self.image("environment.iso", b"environment")
        dotenv = self.image("dotenv.iso", b"dotenv")
        self.image("roms/drop.iso", b"drop")
        (self.root / ".env").write_text(f'{provision.ENV_DISC}="{dotenv}"\n')

        selected = provision.resolve_disc(
            explicit, self.root, {provision.ENV_DISC: str(environment)}, self.root
        )
        self.assertEqual((selected.path, selected.source), (explicit.resolve(), "explicit"))
        selected = provision.resolve_disc(
            None, self.root, {provision.ENV_DISC: str(environment)}, self.root
        )
        self.assertEqual((selected.path, selected.source), (environment.resolve(), "environment"))
        selected = provision.resolve_disc(None, self.root, {}, self.root)
        self.assertEqual((selected.path, selected.source), (dotenv.resolve(), "dotenv"))

        (self.root / ".env").write_text(f"{provision.ENV_DISC}=\n", encoding="utf-8")
        selected = provision.resolve_disc(None, self.root, {}, self.root)
        self.assertEqual(
            (selected.path, selected.source), ((self.root / "roms/drop.iso").resolve(), "drop-in")
        )

        with self.assertRaisesRegex(provision.ProvisionError, "does not exist"):
            provision.resolve_disc("missing.iso", self.root, {}, self.root)

    def test_ambiguous_drop_in_is_refused(self) -> None:
        self.image("roms/a.iso", b"a")
        self.image("roms/b.xiso", b"b")
        with self.assertRaisesRegex(provision.ProvisionError, "ambiguous"):
            provision.resolve_disc(None, self.root, {}, self.root)

    def test_tool_resolution_uses_cli_environment_then_dotenv(self) -> None:
        explicit = self.image("explicit-tool", b"")
        environment = self.image("environment-tool", b"")
        dotenv = self.image("dotenv-tool", b"")
        (self.root / ".env").write_text(f'{provision.ENV_INSPECTOR}="{dotenv}"\n', encoding="utf-8")

        selected = provision._tool(
            explicit,
            provision.ENV_INSPECTOR,
            "missing-test-tool",
            self.root,
            {provision.ENV_INSPECTOR: str(environment)},
            self.root,
        )
        self.assertEqual(selected, explicit.resolve())
        selected = provision._tool(
            None,
            provision.ENV_INSPECTOR,
            "missing-test-tool",
            self.root,
            {provision.ENV_INSPECTOR: str(environment)},
            self.root,
        )
        self.assertEqual(selected, environment.resolve())
        selected = provision._tool(
            None, provision.ENV_INSPECTOR, "missing-test-tool", self.root, {}, self.root
        )
        self.assertEqual(selected, dotenv.resolve())

        with self.assertRaisesRegex(provision.ProvisionError, "does not exist"):
            provision._tool(
                Path("missing-tool"),
                provision.ENV_INSPECTOR,
                "missing-test-tool",
                self.root,
                {provision.ENV_INSPECTOR: str(environment)},
                self.root,
            )

    def test_wrong_disc_digest_is_refused_before_extraction(self) -> None:
        disc = self.image("wrong.iso", b"wrong disc")
        profile = self.root / "mua.toml"
        profile.write_text(
            """[title]
disc_sha256 = "00"
xex_sha256 = "22"
image_sha256 = "33"
title_id = "415607da"
media_id = "5a20a6d4"
[image]
base = 0x82000000
size = 0x00d00000
entry = 0x824806d8
""",
            encoding="utf-8",
        )
        observed = hashlib.sha256(disc.read_bytes()).hexdigest()
        with self.assertRaisesRegex(provision.ProvisionError, f"disc.sha256 mismatch.*{observed}"):
            provision.provision(
                provision.ResolvedDisc(disc, "explicit"), profile, disc, disc, self.root
            )

    def test_exact_inspection_is_accepted(self) -> None:
        provision.validate_inspection(exact_profile(), exact_inspection())

    def test_each_identity_layer_has_a_named_refusal(self) -> None:
        mutations = {
            "xex.sha256": ("xex", "sha256", "44" * 32),
            "execution.title_id": ("execution", "title_id", "00000000"),
            "execution.media_id": ("execution", "media_id", "00000000"),
            "image.sha256": ("image", "sha256", "55" * 32),
            "image.base": ("image", "base", "83000000"),
            "image.size": ("image", "size", 1),
            "image.entry": ("image", "entry", "82000000"),
        }
        for label, (section, field, value) in mutations.items():
            with self.subTest(label=label):
                inspection = exact_inspection()
                inspection[section][field] = value
                with self.assertRaisesRegex(provision.ProvisionError, label.replace(".", r"\.")):
                    provision.validate_inspection(exact_profile(), inspection)

    def test_helper_ambiguity_and_missing_code_range_are_refused(self) -> None:
        inspection = exact_inspection()
        inspection["helpers"]["restgprlr_14"] = []
        with self.assertRaisesRegex(provision.ProvisionError, "helpers.restgprlr_14"):
            provision.validate_inspection(exact_profile(), inspection)
        inspection = exact_inspection()
        inspection["sections"] = []
        with self.assertRaisesRegex(provision.ProvisionError, "code range"):
            provision.validate_inspection(exact_profile(), inspection)

    def test_old_descriptor_rows_and_missing_record_address_are_refused(self) -> None:
        inspection = exact_inspection()
        inspection["imports"][1]["library"] = "xam.xex"
        inspection["imports"][1]["ordinal"] = 1
        with self.assertRaisesRegex(provision.ProvisionError, "duplicate identity"):
            provision.validate_inspection(exact_profile(), inspection)
        inspection = exact_inspection()
        del inspection["imports"][0]["record_address"]
        with self.assertRaisesRegex(provision.ProvisionError, "logical-import schema"):
            provision.validate_inspection(exact_profile(), inspection)


if __name__ == "__main__":
    unittest.main()
