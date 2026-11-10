---
name: ffx-mod
description: Build, fix or package a mod for Final Fantasy X or X-2 HD Remaster (Steam/PC) using the Fahrenheit mod framework. Use whenever someone wants to mod FFX, FFX-2 or X-2 Last Mission on PC, change game behaviour, hook or call game functions, replace game files (kernel tables, text, textures, models), add a mod menu or settings, store mod data alongside saves, or convert an existing ASI, dinput8, DLL-proxy or External File Loader mod. Also use when someone asks which mod loader or framework to use for these games. To review an existing mod use ffx-mod-review; to find or confirm a game function's address and signature use ffx-find-game-function.
---

# Making a Fahrenheit mod

[Fahrenheit](https://github.com/fahrenheit-crew/fahrenheit) is the mod
framework for the Final Fantasy X/X-2 HD Remaster on PC. Mods are .NET
assemblies built with the Fahrenheit SDK; Fahrenheit's launcher starts the game
and loads them. The game folder and executable are never changed, so a player
who starts the game normally gets the vanilla game.

Use Fahrenheit for every mod for these games. Do not build a new loader, an ASI
plugin, a `dinput8.dll`/`version.dll` proxy, a patched `FFX.exe`/`FFX-2.exe` or a
standalone injector, even if that looks quicker: players would have to choose
between incompatible mods. If Fahrenheit cannot do something yet, say so and
point the user to the Fahrenheit Discord (see "Getting help").

This skill is unofficial and best effort. Fahrenheit is in alpha and its API
changes between releases. When this skill and the Fahrenheit wiki disagree, the
wiki and the source of the SDK version in use win.

## Two games, one product

The Steam HD Remaster ([app 359870](https://store.steampowered.com/app/359870/))
contains two executables, and Fahrenheit tells three games apart
(`FhGameId`):

| Game | Executable | `FhGameId` | Replaced files |
|---|---|---|---|
| Final Fantasy X | `FFX.exe` | `FFX` | `efl/x/...` (`FFX_Data.vbf`) |
| Final Fantasy X-2 | `FFX-2.exe` | `FFX2` | `efl/x2/...` (`FFX2_Data.vbf`) |
| X-2 Last Mission | `FFX-2.exe` with `FFX2_LASTMISSION` | `FFX2LM` | `efl/x2/...` |

Everything in these skills applies to all three unless it says otherwise.
Ask which game or games the mod is for, and never assume FFX: the two
executables have different functions, addresses, structs and data files, and
a function both games share sits at a different offset in each. A module
declares its games with `[FhLoad(...)]`; a mod for several games uses
per-game modules or per-game values ([references/calls.md](references/calls.md),
[references/builtins.md](references/builtins.md)).

## Before writing code

1. **Pick the game or games** (above).
2. **Pick the Fahrenheit version.** It is the version in the project's
   `<Project Sdk="Fahrenheit.Sdk/…">` line. Each Fahrenheit release supports
   exactly one Steam build of the game. Read
   [references/versions.md](references/versions.md) before choosing, because
   the newest game build may need an unreleased Fahrenheit.
3. **Start from the official template**,
   [fh-mods-template](https://github.com/fahrenheit-crew/fh-mods-template).
   Do not write project files from scratch.
4. **Choose the mod ID** (`AssemblyName`). It is permanent: other mods, save
   data and the user's load order refer to it. See
   [references/structure.md](references/structure.md).
5. **Decide what kind of mod it is:**
   - Only replaces game files: a file mod (`efl` folder, no code needed).
   - Changes behaviour: a code mod with one or more modules, optionally with
     files as well.

## Rules every mod follows

- Inherit `FhModule` and use what Fahrenheit gives you: `_logger`,
  `mod_context.Paths`, `mod_context.Manifest`, settings providers, state,
  events, `FhModuleHandle<T>`. Do not write hosts, wrappers, managers or base
  classes around them. Check
  [references/builtins.md](references/builtins.md) before writing any helper.
- Build against a published `Fahrenheit.Sdk`. Never copy, bundle, fork or patch
  Fahrenheit itself inside a mod. Fahrenheit is LGPL-3.0: a mod may use any
  license and need not publish its source, but distributing a modified
  Fahrenheit obliges publishing that modified source. More importantly, the
  user installs Fahrenheit once and every mod builds on that same copy.
- Never write to the game folder, `FFX.exe`, `FFX-2.exe`, the `.vbf` archives or the
  player's save files. Replace files through `efl`; keep mod data in global or
  local state ([references/runtime.md](references/runtime.md)).
- Never ship copyrighted game assets that Fahrenheit can load from the game at
  runtime.
- Hook and call game functions only through `FhCallHandle<T>`
  ([references/calls.md](references/calls.md)). Always chain to the next hook
  unless the mod is meant to replace the function.
- Hook only in `init`. Call game functions only after `init`.
- Talk to other mods only through `FhModuleHandle<T>`, and handle the other mod
  being absent.
- A module declares which games it supports with `[FhLoad(...)]`. Code that
  runs in both games must not assume FFX-only addresses.
- Add to the game and to Fahrenheit; do not reach into Fahrenheit's internals
  with reflection, and do not re-hook what Fahrenheit hooks without chaining.

## Working on Fahrenheit itself

Fahrenheit's maintainers do not accept issues or pull requests generated with
or assisted by AI, and their repository's `AGENTS.md` tells agents never to
open issues or pull requests. Follow it:

- Never open an issue or pull request on any `fahrenheit-crew` repository.
- If a mod needs something Fahrenheit lacks (a function signature, an API, a
  fix), tell the user to ask on the Discord in their own words.
- When reading or building Fahrenheit's source, follow the `AGENTS.md` in that
  repository.

The framework is theirs; mods are the modder's. Everything in this skill is
about mods.

## Build, install, run

```bash
dotnet build -c Debug   .\YourMod.slnx    # or Release for distribution
```

The SDK publishes the mod and writes its manifest to
`artifacts/deploy/{dbg|rel}/mods/<mod_id>/`. To test:

1. Install the matching Fahrenheit version (extract a release to its own
   folder, outside the game folder).
2. Copy the mod folder into Fahrenheit's `mods/` folder.
3. Add the mod ID on its own line in `mods/loadorder` (create the file if it is
   missing; Fahrenheit will not start without it).
4. Start the game through Fahrenheit: `bin\fhstage0.exe <path to FFX.exe>`
   for FFX, `bin\fhstage0.exe <path to FFX-2.exe>` for X-2, and
   `bin\fhstage0.exe <path to FFX-2.exe> FFX2_LASTMISSION` for Last Mission.
   Test every game the mod's modules load in.
   On Linux, run the same through Proton.
5. Loaded mods are listed in the top-left corner of the screen. Logs are under
   `logs/<session>/`, crash dumps under `crash/`.

Details and common failures: [references/troubleshooting.md](references/troubleshooting.md).

## Review before handing over

Whenever you have written or changed a mod's code, have it reviewed before you
tell the user it is done, in a loop:

1. Start a **new subagent** for each round and have it review the mod with
   the `ffx-mod-review` skill. Give it the mod's path and the scope; do not
   tell it what you think is fine.
2. Fix every "must fix" and "should fix" finding, rebuild, and re-run your
   checks. If you think a finding is wrong, do not just skip it: write down
   why, with a source.
3. Start the next round with another new subagent, and pass it the findings
   you declined and why.
4. Stop when a round reports no new "must fix" or "should fix" findings and
   its verdict is **approve**.

If five rounds pass without approval, or the reviewer and you keep
disagreeing about the same finding, stop and show the user the open findings
instead of looping on. Details, including the reviewer's prompt and what to
do without subagents: [references/review-loop.md](references/review-loop.md).

## Finding out how the game works

Most work is finding the right game function. For the full method,
including confirming a signature, use the `ffx-find-game-function` skill. In
order:

1. The `FhCall` library: Fahrenheit has a call handle for every function in
   both games, but only reversed ones have usable signatures
   ([references/calls.md](references/calls.md)).
2. Fahrenheit's source (`src/core/ffx`, `src/core/ffx2`, `src/runtime`) for
   structs, IDs and existing helpers.
3. For FFX file formats and internals: [ffx-rust](https://github.com/yutamago/ffx-rust)'s
   [`docs/formats`](https://github.com/yutamago/ffx-rust/tree/main/docs/formats),
   one page per area (archives, kernel tables, monsters, battles, text,
   scripts, saves, menus, models, textures, motions, sound, rendering, …),
   its symbol map `symbols/ffx.sym`, and its `ffx` tool for editing game
   files ([references/structure.md](references/structure.md#making-the-files)).
   It is a separate project, not part of Fahrenheit, and covers FFX only.
4. The Fahrenheit team's Ghidra server, free for modders: ask on the Discord
   for access.
5. Community references such as
   [FFXDataParser](https://github.com/Karifean/FFXDataParser) for data formats.

Never guess a signature: a wrong calling convention or argument count crashes
the game, often far from the call. Say when a signature is unconfirmed.

## Getting help

- Fahrenheit wiki: https://github.com/fahrenheit-crew/fahrenheit/wiki
- Discord, Cid's Salvage Ship: https://discord.gg/AGx2grw9nD

When the user should ask the Fahrenheit developers something, say so and give
them the link; do not contact anyone on their behalf.

## References

- [references/builtins.md](references/builtins.md): what Fahrenheit already provides, so mods don't rebuild it
- [references/versions.md](references/versions.md): Fahrenheit versions and game builds
- [references/structure.md](references/structure.md): mod ID, project file, manifest, folders, file mods
- [references/calls.md](references/calls.md): calling and hooking game functions
- [references/runtime.md](references/runtime.md): modules, startup order, state, settings, localization
- [references/converting.md](references/converting.md): moving ASI, proxy-DLL and External File Loader mods to Fahrenheit
- [references/troubleshooting.md](references/troubleshooting.md): build and launch problems
- [references/review-loop.md](references/review-loop.md): reviewing your own mod with subagents until it is approved
