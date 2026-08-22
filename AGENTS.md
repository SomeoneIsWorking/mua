# Marvel Ultimate Alliance port guidance

The repository-wide rules in `../../AGENTS.md` apply here. Consult
`docs/codemap.md`, then run
`python3 ../../shared/re-harness/info.py brief <words>` before changing a
subsystem. Update the map and registries in the same commit.

## Product target

This is a native PC port of the Xbox 360 Gold Edition of Marvel Ultimate
Alliance, built as a static-recompilation plus measured native overrides. The
supplied exact build is the first conformance target, not permission to bake
its addresses into shared code.

The dependency direction is:

```text
MUA title adapter -> shared xenon-host
                  -> shared alchemy
```

MUA never depends on the GearsUE3 repository. `xenon-host` owns reusable Xbox
360 ABI, services, and presentation. `alchemy` owns engine formats and abstract
engine semantics. This repository owns the exact image identity, generated PPC
module, title addresses, overrides, scripts, probes, save namespace, and MUA
conformance evidence.

## Source and oracle

- The primary source is the user-owned Xbox 360 Gold disc. The PS2 disc is an
  auxiliary little-endian Alchemy/behavior cross-check, not a second shipping
  target.
- Generated recompiler output and extracted game data live only under ignored
  `scratch/titles/<disc-sha256>/`. Never edit or commit generated bodies.
- Xenia currently boots this build to its retail main menu headlessly. That is
  a positive compatibility observation, not yet a trusted differential oracle.
  Validate the oracle with positive/negative controls before citing absence or
  pixel agreement.
- Agent runs are headless and bounded. Capture the exact PID and terminate only
  that PID; never use `pkill`.

## Native boundary

The local generated bridge exports one immutable guest-module descriptor to
`xenon-host`; shared code must not include title `ppc_config.h`, `_xstart`,
`PPCFuncMappings`, `sub_*`, or `__imp__sub_*` names. Native overrides keep the
retained recomp body callable for A/B verification.

Every unsupported instruction traps by name. Every unresolved import traps by
symbol. Outside-function branch targets are classified as switch cases, real
functions, or data before being admitted; never seed all targets as functions.

`config/mua.toml` is the single title-profile authority. The build generates its
C++ constants through `tools/generate_profile.py`; do not duplicate disc/XEX/
image identities or layout constants in source or tests.

## Launcher

When the first executable target lands, `./run.sh` with no arguments launches
the native MUA product. It resolves explicit CLI input before `.env` before one
unambiguous ignored drop-in ISO and refuses missing or wrong media by exact
identity. Emulator and diagnostic paths remain explicit named modes.
