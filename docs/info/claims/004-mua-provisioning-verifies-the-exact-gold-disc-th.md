---
id: C004
kind: claim
status: holds
created: 2026-08-22
tags:
depends: tools/provision.py, tests/test_provision.py, config/mua.toml
---

## Claim

MUA provisioning verifies the exact Gold disc through the raw XEX and decrypted image without a Gears runtime dependency

## Evidence

tools/provision.py streamed 5,952,126,976 disc bytes to SHA-256 a994..., used
xdvdfs for default.xex, invoked the then-available title-neutral XEX inspection
implementation, and matched config/mua.toml: XEX 06d1..., title 415607da, media
5a20a6d4, image fbf7... at 82000000 size 13631488 entry 824806d8, ten
sections, 206 unique logical imports (196 functions and ten variables), zero
duplicate identities, and eight unique helpers. tests/test_provision.py exercises
a wrong-disc discriminator before extraction, seven downstream identity
mutations, old descriptor-row ambiguity, missing record addresses, exact
input/tool priority, and policy refusals. The implementation owner is now
required to be `x360port`'s `x360-xex-inspect`; the real-disc discriminator must
be rerun after that command lands.

## What would falsify it

A supplied Gold disc no longer produces these identities through tools/provision.py, any discriminator is accepted, or provisioning resolves/executes code from the Gears title repository.
