# Codemap

This map owns subsystem placement only. Status belongs in
`docs/project-state.md`; execution order belongs in `docs/re-frontier.md`.

| Responsibility | Owner | Current or intended location | New work belongs |
| --- | --- | --- | --- |
| Exact Gold identity and title policy | MUA title profile | `config/mua.toml`, `include/mua/`, `src/title/` | Same title-profile owner |
| Exact disc/XEX provisioning | MUA provisioning boundary | `tools/provision.py` | Same tool until title-neutral XEX inspection moves to `xenonport` |
| XEX mapping, PPC CPU/threads, imports, memory/device callbacks, Xenia dynarec dispatch | Shared Xbox 360 framework | Intended peer `shared/xenonport` | `xenonport`, never MUA or Gears |
| Runtime native override and original-guest call mechanics | Shared Xbox 360 framework | Intended peer `shared/xenonport` | Its executor/dispatch module |
| MUA native behavior, addresses, save namespace, and input meaning | MUA game layer | Planned game modules | The smallest cohesive MUA owner |
| Title-neutral Alchemy engine services and asset semantics | Intended shared Alchemy engine | Peer `../../shared/alchemy` after X-Men 2 establishes its first runtime contracts | Extend the shared engine; do not create an MUA-local duplicate |
| MUA-specific Alchemy policy | MUA game layer | Planned MUA modules | Keep title behavior here and call narrow shared-engine interfaces |
| Application lifetime and composition | MUA app | Planned app module | Composition only |
| Rendering/presentation | MUA/Xbox presentation owner | Planned video modules | Renderer modules, separate from app and game policy |
| Audio device/mix ownership | MUA audio owner | Planned audio modules | Audio modules |
| Device discovery and action mapping | MUA input owner | Planned input modules | Input modules; title action meaning remains MUA-owned |
| Configuration ingestion and typed immutable settings | MUA config owner | Planned config module | Only this owner may read environment/CLI/config files |
| Product diagnostics | Lucent-backed logging owner | Planned logging adapter | One adapter; product modules do not write stderr directly |
| Differential and conformance evidence | Test harness | `tests/`, `docs/re-frontier.md` | Tests using shipping owners plus independent oracle |
