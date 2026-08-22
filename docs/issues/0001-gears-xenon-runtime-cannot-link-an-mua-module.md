---
id: 1
title: Gears Xenon runtime cannot link an MUA module
status: investigating
symptom: A valid MUA XenonRecomp output fails to link against the existing host despite sharing the Xbox 360 platform
tags: architecture,xenon,title-boundary,link
created: 2026-08-22
updated: 2026-08-22
---

## Root cause


## What was tried / dead ends


## Resolution

### Note (2026-08-22)
Inventory found 91 exact __imp__sub_* title references in the current Gears host; MUA emits only two coincident addresses and lacks 89. Address coincidence is not semantic compatibility. Proper fix: shared xenon-host owns only address-free module ABI and console services; each title adapter owns every guest address, override, probe, and save namespace.

### Note (2026-08-22)
The title-neutral xenon-host contract is now a separate compiled peer, and MUA compiles its exact Gold ImageIdentity through it without Gears addresses. The issue remains investigating until a real generated MUA function/import manifest links and enters, which is the test that will prove the old linker failure is gone.
