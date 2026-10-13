# Prior art

External work on Marvel: Ultimate Alliance Gold Edition (Xbox 360, title `415607DA`, media `5A20A6D4`, image sha256 `fbf7a09b…117`, base `0x82000000`, entry `0x824806D8`). Addresses were checked with `../gears1/tools/ppcdis.py --image <provisioned image.bin> --base 0x82000000`; the image sha256 matches `config/mua.toml`.

| project | URL | kind | license | target build | build match (addresses checked) | what we may take | notes |
|---|---|---|---|---|---|---|---|
| Xenia Canary game patches, `415607DA - Marvel Ultimate Alliance (Special Edition).patch.toml` | https://github.com/xenia-canary/game-patches | Xenia memory patches (unlock FPS, 1080p) | none (no LICENSE file) | "Special Edition" XEX, Xenia module hash `3C79FD35938D985D` | matched: `0x82455C1C` `li r11,0x500` (width 1280), `0x82455C20` `li r10,0x2D0` (height 720), `0x82497F94` `li r10,1` (frame-interval byte `0x82497F97`), `0x8212145C` `stfs f0,0x18(r30)` (nop target) | evidence only | Its comment cites media `26848425`; ours is `5A20A6D4`, yet the bytes agree, so the Gold XEX is the build this file names "Special Edition". The plain and `(TU2)` files do not match: `0x8243DF94` is `lwz`, `0x8211144C` is `bdnzf`, `0x824982CC` is `li r9,0`, `0x82455F2C` is `lwz`. |
| sp00nznet/mua | https://github.com/sp00nznet/mua | PS3 static recompilation (`BLUS30010`) | MIT | PS3 EBOOT, not Xbox 360 | not checkable: other platform and binary; repo held only a README at 2026-09-05 | nothing | Watch only for engine-level names if it grows. |
| raven-formats | https://github.com/nikita488/raven-formats | XMLB/ZSND data-format tools (MarvelMods) | MIT | PC data formats | n/a (no code addresses) | names only (format field names) | Confirm against Gold disc files before relying on it. |
| OpenHeroSelect | https://github.com/TheRealPSV/OpenHeroSelect | PC herostat/roster modding tool | AGPL-3.0 | PC MUA/XML2 | n/a | nothing | Data-mod tool; AGPL. |
| igb-blender | https://github.com/KaikoClanworth1/igb-blender | IGB/IGZ Blender importer | none | PC XML2/MUA assets | n/a | evidence only | Alchemy format notes belong in `shared/alchemy` if used. |

Not found (searched 2026-10-13): an Xbox 360 MUA decompilation, recompilation or native port (GitHub, decomp.dev, recompiled-games lists), public symbol maps or IDA/Ghidra databases for any MUA XEX, an Alchemy engine decompilation.
