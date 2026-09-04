# Project state

## Comparison baseline

The comparison baseline is the exact Gold Edition running under Xenia. This
project intends a native/dynarec product with title-native owners and the user's
same original disc, not an offline-generated guest-code executable.

## Current focus

S003 is the current focus: connect the authenticated Gold image to the shared
`x360port` executor after the static product path was removed.

## Capability inventory

| ID | Capability or outcome | State | Factual dependency | Goals |
| --- | --- | --- | --- | --- |
| S001 | Exact Gold disc, raw XEX, decrypted image, section, import, and helper identity are known | verified | — | G001, G002 |
| S002 | Exact media provisioning validates and preserves the runtime image without static generation | partial | S001 | G001, G002 |
| S003 | `x360port` maps the image and executes entry `0x824806D8` through Xenia's dynarec | missing | S001, S009 | G001, G002 |
| S004 | Runtime imports and Xbox services advance from the first named missing service | missing | S003 | G001, G002 |
| S005 | MUA-native override and original-call dispatch works through the dynarec | missing | S003 | G001, G002 |
| S006 | MUA consumes Alchemy's neutral contracts through its x360 adapter over `x360port` | missing | X-Men 2 complete goals | G001, G002, G003 |
| S007 | Native rendering, audio, input, configuration, saves, and platform composition are implemented | missing | S004, S006 | G003 |
| S008 | Representative interactive gameplay is conformant and within the host performance budget | missing | S005, S007 | G001, G003 |
| S009 | The offline generated-PPC pipeline and remaining static product surfaces are absent | verified | — | G001 |
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
`x360port`, execute entry `0x824806D8`, count nonzero Xenia JIT blocks, and stop
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
contracts. MUA then links Alchemy's x360 adapter over `x360port`, reuses and
extends the neutral contracts, and keeps title identity, addresses, and policy
in this repository. The neutral core never depends on a platform runtime.

### S007 — native host surface

Missing capability: compose cohesive renderer, audio, input, configuration,
save, UI, and platform owners without Gears or title-specific shared code.

### S008 — representative gameplay

Missing capability: verify a bounded interactive gameplay scenario against an
independent oracle with CPU/memory/timing/device and frame-time evidence on each
released host.

### S009 — static path removal

Evidence: the generated title-profile header/body, profile generator, generated
source ignore path, static title library/tests, old shared-host dependency, and
obsolete cleanup tool were deleted. CMake now exposes one product target that
fails only at the named missing `x360port` title-adapter boundary. The remaining
profile is runtime identity data consumed by provisioning, not generated guest
code.

### S010 — player delivery

Missing capability: provide the zero-argument launcher, no-terminal first-run
selection, OS user-data storage, and asset-free signed packages.
