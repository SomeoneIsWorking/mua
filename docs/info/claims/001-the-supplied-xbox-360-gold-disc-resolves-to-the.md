---
id: C001
kind: claim
status: holds
created: 2026-08-22
tags:
depends: config/mua.toml
---

## Claim

The supplied Xbox 360 Gold disc resolves to the exact MUA title profile in config/mua.toml

## Evidence

Streaming SHA-256 measured the 5952126976-byte disc, extracted XEX, and parsed image; XEX metadata independently reported title 415607DA, media 5A20A6D4, base 0x82000000, size 0x00D00000, and entry 0x824806D8.

## What would falsify it

Any digest or XEX execution field differing when the same local disc is reprovisioned, or config/mua.toml changing without remeasurement.
