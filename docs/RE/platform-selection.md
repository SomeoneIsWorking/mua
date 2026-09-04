# Source-platform selection

## Decision

Use the Xbox 360 Gold Edition as the primary source and keep the PS2 build as a
cross-platform Alchemy reference.

## Xbox 360 evidence

The supplied 5,952,126,976-byte disc has SHA-256
`a994dbf1359686797671eb1e198d7e1124ec4ec3f220fc6a672daac68d6b54c7`.
Its retail AES/LZX XEX becomes a 13,631,488-byte PowerPCBE image at
`0x82000000`, entry `0x824806D8`.

Title-neutral XEX inspection identifies ten sections, 206 logical imports (196
functions and ten variables), and all eight save/restore helpers. Binary
comparison also found 89 of 91 Gears title-address references absent from this
image, proving that shared Xbox execution cannot contain Gears policy or
addresses. These are runtime-image and ownership facts for `x360port`; no
offline guest-code analysis or generation is part of the product plan.

A bounded, isolated, headless Xenia observation mounted `default.xex`, started
the main guest thread, issued 1,210 1280x720 presents, accepted scripted Start/A
input, initialized its XMA/audio client, and reached the full retail main menu.
Six of six captures succeeded. There was no guest crash, assertion, Vulkan
device loss, or fatal launch error during the 90-second title interval. The
known oracle teardown hang required terminating the exact process after capture
completion, so the shell's eventual status 137 is not a title failure.

This proves the local emulator can execute and observe this revision. It does
not yet establish hardware-faithful oracle output.

## Why PS2 is not the primary path

The PS2 executable is an 8,845,696-byte, stripped, static R5900 ELF with MMI
instructions, VU1 microcode, 22 IOP modules, direct VIF/GIF/DMA use, and
load-address overlays. A faithful first milestone therefore needs a new
R5900/MMI lifter plus a pinned PCSX2 fork exposing synchronous EE, IOP, VU, DMA,
GIF, and GS state. The installed PCSX2 PINE interface cannot provide that
lockstep state.

PS2 assets remain valuable: they expose Alchemy version-6 containers and
platform raster formats that the shared engine should decode independently of
the shipping Xenon target.
