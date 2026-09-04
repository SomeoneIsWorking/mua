# Marvel: Ultimate Alliance port guidance

The repository-wide rules in `../../AGENTS.md` apply. Start with
`docs/project-state.md`, then `docs/codemap.md` and `docs/re-frontier.md`. Query
the registries through `../../shared/re-harness/tools/info.py brief <terms>`
before re-deriving a binary or behavioral fact.

## Product boundary

This repository owns the Xbox 360 Gold Edition title layer for a native/dynarec
PC port. It is deferred until X-Men 2's complete project-goals list is verified.
Do not begin MUA implementation merely because an initial X-Men 2 JIT milestone
passes. When MUA resumes, gameplay combines MUA-owned native behavior with guest
PPC execution through the shared `xenonport` integration of Xenia's runtime
dynarec.

- No gameplay target links or selects a PPC interpreter.
- Do not generate, compile, or run an offline-translated guest module.
- Do not resume the removed switch-target, generated-function-map, or static
  recompiler-input workflows.
- The primary source is the user-owned Gold disc. The PS2 disc is an auxiliary
  Alchemy/behavior reference, not another shipping target.
- Preserve exact disc/XEX/image identity and the validated provisioning path.
  Game bytes and extracted assets remain ignored and outside packages.

The dependency direction is:

```text
MUA title adapter -> shared xenonport -> Xenia dynarec
                  -> shared alchemy   -> native Alchemy engine services
```

MUA never depends on Gears. Shared code contains no MUA addresses or behavior.
`xenonport` owns the authenticated XEX image, PPC CPU/thread contexts, imports,
device-memory callbacks, dynarec dispatch, and native/original-call boundary.
MUA owns exact identity, title addresses, native overrides, save namespace,
input meaning, title-specific Alchemy policy, and conformance evidence.
`shared/alchemy` is the intended engine owner for both X-Men 2 and MUA, but it is
not a shared runtime engine today and MUA does not currently consume one. X-Men
2 establishes and verifies the first common engine contracts. After MUA's
deferral lifts, MUA must reuse and extend those contracts rather than building a
second title-local Alchemy engine.

## First implementation discriminator after deferral lifts

Load the authenticated Gold image and execute entry `0x824806D8` through
Xenia's dynarec until the first named missing service. The report must show
nonzero translated blocks and a complete refusal for the missing service. This
is wiring evidence, not permission to declare gameplay or delete remaining
static product code; retirement requires representative interactive gameplay.

## Structure and diagnostics

The codemap is the structure authority. C++ stateful owners use focused RAII
classes with explicit constructor dependencies and composition. The app entry
point only composes owners. Product modules do not write directly to stderr or
platform debug output; they use the configurable Lucent logger. Only the config
owner reads environment/CLI/file inputs and passes validated typed configuration
to consumers. The normal verifier must reject direct stderr writes, stray
`getenv`, forbidden dependency edges, and source-file growth beyond the project
limits.

Agent runs are headless and bounded. Capture and stop only the exact process PID;
never use `pkill`.
