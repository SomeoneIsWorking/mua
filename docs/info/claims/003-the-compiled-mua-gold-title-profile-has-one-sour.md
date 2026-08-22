---
id: C003
kind: claim
status: holds
created: 2026-08-22
tags: mua,profile,xenon
depends: config/mua.toml, tools/generate_profile.py, src/title/title_profile.cpp, tests/title_profile_tests.cpp
---

## Claim

The compiled MUA Gold title profile has one source of truth in config/mua.toml and enters xenon-host types with exact disc, XEX, parsed-image, base, size, entry, title, and media identity.

## Evidence

Clang build generated mua_profile_data.hpp from config/mua.toml; title_profile and profile_generator tests passed, including a malformed-digest refusal

## What would falsify it

config/mua.toml, the generator, compiled profile composition, or title contract changes without rerunning Clang build, generator discriminator, format, clang-tidy, and structure gates
