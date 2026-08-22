# RE Frontier — the ordered RE dependency chain toward a faithful port

Tracked by the shared `re-harness/re_frontier.py` tool (consult it FIRST; update
it in the SAME commit that changes a step). This is the fine-grained companion to `docs/codemap.md`:
the codemap says *what subsystem exists*, this says *which ordered RE step is
real reverse-engineering vs a hack that jumped ahead*.

**Hard rule (no hacks / no fallbacks):** a `⛔ hack` status is DEBT, never an
acceptable resting state. It marks a shortcut standing in for absent RE and MUST
be removed as its real mechanism lands. `re_frontier.py hacks` is the debt list;
`re_frontier.py next` tells you the next RE-ready step.

**`re-verified` MEANS FAITHFUL to the real target — not "the mechanism runs."** A
step is `re-verified` only when its OUTPUT matches the real game/binary (look /
sound / behavior) on real data. An internal trace ("bytecode reached the call
site", "N rows attached") is a mechanism check, NOT faithfulness — if it runs but
the result doesn't match the real target, it is `re-partial` with the
faithfulness gap named. The user observes the running system; that observation
overrides any internal trace.

**Fail fast & loud:** a failure must surface loudly, never silently fall back —
unless the fallback IS intended behavior of the real target being reproduced.

Statuses: ✅ re-verified · 🟡 re-partial (honest gap) · 🔬 in-progress ·
⛔ hack (debt, must remove) · ⬜ todo · ➖ skip-by-design · ⏸ blocked (computed).

<!-- Entries are `## <area>` sections holding `### <id> — <title>` headings, each
     followed by `- <field>: <value>` lines. Prose ANYWHERE in this file — before,
     between or inside entries — is yours: tools/re_frontier.py edits only the
     field lines it is told to change and copies everything else through byte for
     byte, refusing the write if anything else would be lost. -->

## boot

### media-identity — Exact Gold disc and XEX identity
- status: re-verified
- deps:
- evidence: Supplied disc, XEX, and parsed-image SHA-256 values plus XEX execution metadata agree with config/mua.toml.
- where: config/mua.toml; docs/RE/platform-selection.md
- gap:
- notes: Unknown revisions refuse rather than inheriting this profile.

### xenia-menu-observation — Headless Xenia reaches the retail main menu
- status: re-partial
- deps: media-identity
- evidence: A bounded 90-second run produced 1210 1280x720 presents and 6/6 nonuniform captures, accepted Start/A input, and reached the full retail menu without a guest crash.
- where: docs/RE/platform-selection.md
- gap: Xenia output is not yet validated against hardware as a correctness oracle.
- notes: Compatibility observation only.

### xex-analysis — Decrypt, decompress, and strictly analyse the XEX
- status: re-partial
- deps: media-identity
- evidence: Current Xenon tools recover the 0x82000000 image, 51015 functions, eight save/restore helpers, and 365 jump tables while naming 13 unsupported instructions and 82 outside-function targets.
- where: docs/RE/platform-selection.md
- gap: Move the generic path into xenon-host and add MUA-owned reproducibility evidence.
- notes:

### module-abi — Shared guest-module ABI and descriptor validation
- status: re-partial
- deps: media-identity
- evidence: The shared xenon-host now builds an address-free GuestModule/TitleAdapter contract with exact image, mapping, import, capability, and entry validation; MUA compiles its exact Gold profile from config through that API.
- where: peer shared/xenon-host; include/mua/title_profile.hpp; src/title/title_profile.cpp
- gap: The real generated MUA function map and import manifest are not yet connected, so the module contract is synthetic plus exact-profile only.
- notes:

### instruction-coverage — Implement the 13 missing PPC instruction cases
- status: todo
- deps: xex-analysis, module-abi
- evidence: Strict recompilation names six lhbrx and seven bso sites instead of emitting fallbacks.
- where: shared xenon-host XenonRecomp fork
- gap: Implement from Xenon ISA semantics with positive and negative decoder tests.
- notes:

### switch-targets — Classify 82 outside-function switch targets
- status: todo
- deps: xex-analysis
- evidence: Strict analysis reports 82 targets across ten tables.
- where: MUA generated analysis inputs; shared switch validator
- gap: Classify each as owning-function case label, missed function, or code/data false positive before generation.
- notes: Never seed all targets as functions.

### generated-module — Generate and link the exact MUA PPC module
- status: todo
- deps: instruction-coverage, switch-targets, module-abi
- evidence:
- where: ignored scratch/titles/<disc-sha256>/ppc; local title bridge
- gap: Generate every body without hand edits and link one exact module descriptor.
- notes:

### guest-entry — Enter the real MUA image through xenon-host
- status: todo
- deps: generated-module
- evidence:
- where: src/app; src/title; shared xenon-host
- gap: Run the exact entry thunk and stop at the first real missing service.
- notes:

### import-frontier — Implement required Xbox services in first-use order
- status: todo
- deps: guest-entry
- evidence: Current inventory finds 30 of 196 imports without reusable implementations; every one is a loud trap until measured.
- where: shared xenon-host; MUA title import manifest
- gap: Drive from the first reached trap; do not bulk-return success.
- notes:

### native-menu — Reach the retail main menu in the native host
- status: todo
- deps: import-frontier, xenia-menu-observation
- evidence:
- where: MUA native executable and differential harness
- gap: Compare synchronized state and frames against a validated oracle before calling it faithful.
- notes:
