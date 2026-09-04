# RE frontier — Gold Edition execution spine

Statuses: `re-verified`, `re-partial`, `in-progress`, `hack`, `authored`, `todo`,
and `skip-by-design`. This chain tracks ground-truth readiness, not general
project status.

## boot

### media-identity — Exact Gold disc and XEX identity
- status: re-verified
- deps:
- evidence: Provisioning streamed all 5,952,126,976 supplied disc bytes and matched the raw XEX, execution metadata, decrypted 13,631,488-byte image, ten sections, 206 logical imports, and eight ABI helpers to config/mua.toml.
- where: config/mua.toml; tools/provision.py; docs/RE/platform-selection.md
- gap:
- notes: Unknown revisions refuse rather than inheriting this profile.

### xenia-menu-observation — Xenia reaches the retail main menu
- status: re-partial
- deps: media-identity
- evidence: A bounded headless run produced nonuniform presents, accepted input, and reached the retail menu without a guest crash.
- where: docs/RE/platform-selection.md
- gap: Compatibility observation is not yet validated against hardware as a differential oracle and is not native-port gameplay evidence.
- notes:

### runtime-image — Reproduce the exact runtime XEX image
- status: re-verified
- deps: media-identity
- evidence: The current title-neutral inspector reproduces the exact decrypted image, base, entry, sections, imports, and ABI helpers consumed by provisioning.
- where: tools/provision.py; docs/info/instruments/003-xenonrecomp-xex-inspect.md
- gap:
- notes: Preserve this contract while moving its title-neutral owner into xenonport; it does not authorize static guest-code emission.

### dynarec-entry — Execute the Gold entry through Xenia
- status: todo
- deps: runtime-image
- evidence:
- where: intended shared xenonport executor; MUA app/title composition
- gap: Map the authenticated image and execute 0x824806D8 with nonzero Xenia JIT blocks until the first named missing service.
- notes: No PPC interpreter or offline-generated guest module participates.

### import-frontier — Implement reached Xbox services in first-use order
- status: todo
- deps: dynarec-entry
- evidence: The exact image contains 206 logical imports whose identity is known from provisioning.
- where: intended shared xenonport import/service owners; MUA title bindings
- gap: Begin at the first reached trap; unknown services remain complete fail-loud errors.
- notes:

### native-boundary — Prove native override and original guest execution
- status: todo
- deps: dynarec-entry
- evidence:
- where: intended shared xenonport dispatcher; MUA native game owner
- gap: Prove override disabled, enabled, and one-call-original paths through Xenia, including policy-change invalidation.
- notes:

### representative-gameplay — Reach and verify interactive Gold gameplay
- status: todo
- deps: import-frontier, native-boundary, xenia-menu-observation
- evidence:
- where: MUA gameplay product and differential harness
- gap: Compare a bounded interactive scenario on CPU, memory, timing, devices, frames, audio, input, and host frame-time budget.
- notes: Boot, menu, FMV, and nonzero JIT counters alone do not complete this step.
