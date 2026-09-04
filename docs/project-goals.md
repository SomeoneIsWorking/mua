# Project goals

## G001 — Ship the Gold Edition as a native/dynarec port

Execute the user's exact Xbox 360 Gold Edition image through Xenia's dynarec,
replacing selected behavior with verified MUA-native owners.

Success conditions:

- The gameplay product contains no offline-translated guest code and no PPC
  interpreter in its build, link, selector, or fallback surfaces.
- `xenonport` authenticates and maps the exact image, executes all non-native
  guest paths through Xenia, and provides image-aware native/original calls.
- Native Alchemy engine services consume the contracts established in
  `shared/alchemy` by X-Men 2; MUA does not create a parallel title-local engine.
- A fresh checkout provisions from the user's disc and zero-argument `run.sh`
  launches the intended product.
- Representative interactive gameplay passes CPU/memory/timing/device and
  frame-time gates on every released host.

## G002 — Preserve exact title identity and fail-closed service ownership

Keep one MUA-owned profile for disc/XEX/image identity and title policy while
placing title-neutral Xbox 360 execution and services in `xenonport` and shared
Alchemy engine behavior in `shared/alchemy`.

Success conditions:

- Wrong or ambiguous media refuses without changing the last valid selection.
- Unknown imports, device accesses, and guest failures name their complete
  identity; no service returns success merely to advance boot.
- Shared code contains no MUA addresses, hashes, or game policy.
- `shared/alchemy` exposes only title-neutral contracts proven by both games;
  MUA-specific behavior remains in this repository.

## G003 — Deliver the intended native product surface

Preserve Gold Edition gameplay and content while adding native presentation,
audio, input, saves/settings, packaging, and platform integration through
cohesive owners.

Success conditions:

- Gameplay, rendering, audio, input, save/load, and configuration are verified
  against independent Xenia/hardware/binary evidence.
- User-visible enhancements are separately gated from faithful behavior.
- Desktop/mobile releases contain no game assets and provide a no-terminal first
  run setup flow.

## Priority constraint

USER 2026-09-04: "MUA is also deferred until xmen2 is done"

MUA implementation remains deferred until every success condition in X-Men 2's
project-goals authority is verified. An intermediate X-Men 2 executor, boot, or
gameplay milestone does not lift this constraint.
