---
id: I003
kind: instrument
status: untrusted
created: 2026-08-22
---

## Instrument

x360port `x360-xex-inspect`

## Validated by

The command and schema have positive and independent negative consumers in
`tests/test_provision.py`. A previous implementation matched the real Gold XEX:
ten sections, 206 unique logical imports (196 functions and ten variables),
zero duplicate library/ordinal identities, eight unique helper addresses, and
the independently recorded raw/image SHA-256 values.

## Known failure modes

No implementation currently exists in `x360port`, so the instrument cannot be
trusted until it produces both the recorded positive result and every named
negative refusal through its new shipping owner.
