# Project state

## Comparison baseline

The comparison baseline is the exact Gold Edition running under Xenia. This
project intends a native/dynarec product with title-native owners and the user's
same original disc, not an offline-generated guest-code executable.

## Current focus

None. MUA is deferred until X-Men 2's complete project-goals list is verified.

## Capability inventory

| ID | Capability or outcome | State | Factual dependency | Goals |
| --- | --- | --- | --- | --- |
| S001 | Exact Gold disc, raw XEX, decrypted image, section, import, and helper identity are known | verified | — | G001, G002 |
| S002 | Exact media provisioning validates and preserves the runtime image without static generation | partial | S001 | G001, G002 |
| S003 | `xenonport` maps the image and executes entry `0x824806D8` through Xenia's dynarec | missing | S001 | G001, G002 |
| S004 | Runtime imports and Xbox services advance from the first named missing service | missing | S003 | G001, G002 |
| S005 | MUA-native override and original-call dispatch works through the dynarec | missing | S003 | G001, G002 |
| S006 | MUA consumes the Alchemy engine contracts established in `shared/alchemy` by X-Men 2 | missing | X-Men 2 complete goals | G001, G002, G003 |
| S007 | Native rendering, audio, input, configuration, saves, and platform composition are implemented | missing | S004, S006 | G003 |
| S008 | Representative interactive gameplay is conformant and within the host performance budget | missing | S005, S007 | G001, G003 |
| S009 | The offline generated-PPC pipeline and remaining static product surfaces are absent | partial | S008 | G001 |
| S010 | Fresh-clone launcher and asset-free desktop/mobile packages provide player setup | missing | S007, S008 | G001, G003 |

## Capability details

### S001 — exact title identity

Evidence: provisioning measured the 5,952,126,976-byte supplied disc, raw XEX,
13,631,488-byte decrypted image, base/entry, ten sections, 206 logical imports,
and eight ABI helpers against `config/mua.toml`.

### S002 — media provisioning

The in-flight provisioner validates disc through image identity and preserves
content-addressed runtime inputs. Gap: the current dirty batch has not been
integrated, re-gated, committed, or connected to a launcher/runtime consumer.

### S003 — Xenia dynarec entry

Missing capability: consume the authenticated runtime image through
`xenonport`, execute entry `0x824806D8`, count nonzero Xenia JIT blocks, and stop
at the first complete missing-service identity.

### S004 — service frontier

Missing capability: implement reached imports, memory/device mappings, clock,
and guest-thread behavior in first-use order without fake-success stubs.

### S005 — native override boundary

Missing capability: prove disabled, enabled, and one-call-original paths through
the runtime address dispatcher, including translation invalidation when policy
changes.

### S006 — shared Alchemy engine consumption

Missing capability: `shared/alchemy` is not yet a proven runtime engine and MUA
does not consume it. X-Men 2 must first establish verified title-neutral engine
contracts; MUA then reuses and extends those contracts without moving
title-specific policy into the shared repository.

### S007 — native host surface

Missing capability: compose cohesive renderer, audio, input, configuration,
save, UI, and platform owners without Gears or title-specific shared code.

### S008 — representative gameplay

Missing capability: verify a bounded interactive gameplay scenario against an
independent oracle with CPU/memory/timing/device and frame-time evidence on each
released host.

### S009 — static path removal

Static-only untracked tools and generated scratch artifacts were removed. Gap:
tracked CMake/documentation and any retained source dependencies still need a
code-phase audit and deletion after S008; do not regenerate, build, or run them.

### S010 — player delivery

Missing capability: provide the zero-argument launcher, no-terminal first-run
selection, OS user-data storage, and asset-free signed packages.
