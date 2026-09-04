# Marvel: Ultimate Alliance — native/dynarec port

This project targets the Xbox 360 Gold Edition of **Marvel: Ultimate Alliance**.
Its intended architecture is MUA-owned native behavior plus runtime guest PPC
execution through `x360port` and Xenia's dynarec, with native Alchemy engine
services shared through `shared/alchemy`. That common runtime engine does not
exist yet and MUA does not currently consume it. The project is not playable.
Its Xbox 360 dynarec migration is active; only shared-Alchemy adoption waits for
X-Men 2's complete project goals to be verified.

Alchemy remains one repository: `alchemy/shared` is platform-neutral and the
optional `alchemy/x360` adapter consumes `x360port`. MUA will link those two
components, not the x86 adapter, and keeps Gold-specific addresses and policy in
this repository. The title composes the sibling dependencies; Alchemy does not
vendor both platform runtimes as submodules.

The repository contains no game code or assets. Supply your own exact Gold disc
image through `.env` (`MUA_X360_ISO`) or one unambiguous ignored file under
`roms/`.

## Current state

The supplied disc, raw XEX, execution metadata, decrypted image, sections,
imports, and ABI helpers have been validated from one title profile. A bounded
headless Xenia observation reached the retail menu, but that is compatibility
evidence rather than native-port conformance. The gameplay product and
`x360port` executor do not exist yet.

The active implementation discriminator is to execute the exact Gold XEX entry
`0x824806D8` through Xenia's dynarec until the first named missing service. A
representative interactive gameplay gate follows before any migration is
complete.

See [project state](docs/project-state.md) for intended features and honest
coverage, [project goals](docs/project-goals.md) for completion conditions, and
the [codemap](docs/codemap.md) for subsystem ownership.

## Provision exact media

The in-flight `tools/provision.py` path resolves an explicit argument, then
`MUA_X360_ISO` from environment/`.env`, then one supported ignored disc image.
It validates the complete disc and XEX identity before preserving `default.xex`,
`image.bin`, and `inspection.json` under the content-addressed ignored
provisioning directory. These are runtime inputs for `x360port`; they are not
inputs to a static code generator.

The current CMake product target refuses at the explicit missing `x360port`
title-adapter boundary; it cannot build or silently select the retired static
path. No launcher or playable build is claimed yet. When it lands, zero-argument
`./run.sh` will provision and launch the native/dynarec product without running
tests or requiring maintainer-only RE tools.

Maintainers run `uv run --frozen python tools/verify.py`; verification is not a
launcher mode.
