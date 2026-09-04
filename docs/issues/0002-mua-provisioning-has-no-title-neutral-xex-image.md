---
id: 2
title: MUA provisioning has no title-neutral XEX image inspector
status: open
symptom: The MUA launcher cannot verify decrypted image SHA-256, base, size, and entry without reaching into the Gears checkout
tags: provisioning,xex,architecture,dry,x360port
created: 2026-08-22
updated: 2026-09-04
---

## Root cause

MUA has a validated machine-readable XEX inspection contract, but the retired
static toolchain was its implementation owner. The product cannot depend on
Gears, retain that toolchain, or copy the AES/LZX/XEX parser into title-local
Python. The new title-neutral owner, `x360port`, does not yet provide the
`x360-xex-inspect` command required by provisioning.

## Proper fix

Implement `x360-xex-inspect` in `x360port`. Its machine-readable output must
cover the raw XEX digest, execution metadata (title/media IDs), decrypted image
digest, base, size, entry, sections, logical imports, and ABI helpers. MUA
provisioning owns input resolution and exact-profile comparison while delegating
all XEX interpretation to that platform tool.

## Ruled out

- Reusing `x360/gears1/tools/title_identity.py`: it embeds its own partial XEX header parser and Gears-specific environment/cache vocabulary.
- Reusing `x360/gears1/tools/gdf_extract.py` through the Gears path: creates a runtime dependency on another title repo.
- Verifying only the disc and raw XEX hashes: cannot verify `config/mua.toml`'s decrypted `image_sha256`, so it is not the requested exact disc/XEX/image gate.

## Exit condition

A MUA-owned provisioning command resolves explicit CLI input, then `MUA_X360_ISO`/`.env`, then exactly one ignored drop-in; uses the shared disc/XEX tools; and has positive plus wrong-disc, wrong-XEX, wrong-metadata, and wrong-decrypted-image discriminator tests.

## Current discriminator

`tools/provision.py` and its synthetic tests already consume the intended
command/schema and refuse every independently mutated identity layer. The issue
closes only when `x360port` implements that command and the real Gold disc again
matches every recorded identity.
