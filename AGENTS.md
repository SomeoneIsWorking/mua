# Marvel: Ultimate Alliance port guidance

The repository-wide rules in `../../AGENTS.md` apply. Start with
`docs/project-state.md`, then `docs/codemap.md` and `docs/re-frontier.md`. Query
the registries through `../../shared/re-harness/tools/info.py brief <terms>`
before re-deriving a binary or behavioral fact.

## Product boundary

This repository owns the Xbox 360 Gold Edition title layer for a native/dynarec
PC port. Its break-first dynarec migration is active alongside Gears because
both consume the same `x360port` integration of Xenia's runtime dynarec. Only
MUA's adoption of `shared/alchemy` remains deferred until X-Men 2's complete
project-goals list is verified.

- No gameplay target links or selects a PPC interpreter.
- Do not resume the removed switch-target, generated-function-map, or static
  recompiler-input workflows.
- The primary source is the user-owned Gold disc. The PS2 disc is an auxiliary
  Alchemy/behavior reference, not another shipping target.
- Preserve exact disc/XEX/image identity and the validated provisioning path.
  Game bytes and extracted assets remain ignored and outside packages.

The dependency direction is:

```text
MUA title policy -> alchemy/x360 -> shared x360port -> Xenia dynarec
                 -> alchemy/shared
```

MUA never depends on Gears. Shared code contains no MUA addresses or behavior.
`x360port` owns the authenticated XEX image, PPC CPU/thread contexts, imports,
device-memory callbacks, dynarec dispatch, and native/original-call boundary.
MUA owns exact identity, title addresses, native overrides, save namespace,
input meaning, title-specific Alchemy policy, and conformance evidence.
`shared/alchemy` is one intended engine repository for both X-Men 2 and MUA: its
neutral `shared` component has no CPU-framework dependency, while its optional
`x86` and `x360` adapters consume `x86port` and `x360port` respectively. MUA
links only the x360 adapter and keeps exact addresses and policy here. X-Men 2
establishes and verifies the first common engine and x86-adapter contracts.
When that Alchemy-specific gate lifts, MUA adds the x360 adapter rather than a
second title-local engine. Alchemy does not own both platform frameworks as
submodules. MUA is not a UE3 title and never depends on `x360ue3` or
`GearsUE3`.

## Break-first migration and first discriminator

Preserve exact media/provisioning evidence and any independent native contract,
then delete every static translator, generated module/function map, switch
target, static selector/configuration/test, and stale methodology. The build may
fail only at the explicit missing `x360port` boundary. Then load the
authenticated Gold image and execute entry `0x824806D8` through Xenia's dynarec
until the first named missing service. The report must show nonzero translated
blocks and a complete refusal for the missing service. This is wiring evidence,
not representative-gameplay conformance.

Agent runs are headless and bounded.
