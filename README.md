# Marvel Ultimate Alliance — native Xbox 360 recompilation port

This repository is the title layer for a native PC port of **Marvel Ultimate
Alliance: Gold Edition**. It consumes two peer shared projects:

- `xenon-host` for the Xbox 360 ABI, loader, services, input, audio, and Xenos
  presentation;
- `alchemy` for the game's engine formats and platform-neutral semantics.

It does not contain or download game code or assets. Supply your own disc image
through `.env` (`MUA_X360_ISO`) or place one unambiguous ISO under ignored
`roms/` once the launcher lands.

## Current milestone

The exact supplied build has been inventoried and observed reaching its retail
main menu in a bounded headless Xenia run. Its title profile now compiles from
`config/mua.toml` into the title-neutral `xenon-host` identity contract, without
copying a second set of hashes or addresses into C++. The XEX decrypts and
analyses through the existing Xenon toolchain. The next executable milestone is
a locally generated module entering through `xenon-host` and trapping at the
first real missing service.

The current contract milestone builds with:

```sh
CXX=clang++ cmake -S . -B scratch/build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build scratch/build -j$(nproc)
ctest --test-dir scratch/build --output-on-failure
```

This is not playable yet. `docs/codemap.md` names the implemented surface and
the remaining gaps without treating recognition or compilation as support.
