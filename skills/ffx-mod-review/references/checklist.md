# Review checklist

Each item names what to look for and where the rule comes from. "ffx-mod"
links point to the `ffx-mod` skill's references, which link on to the
Fahrenheit wiki and source.

## 1. Rebuilding what Fahrenheit has

Full table: [builtins.md](../../ffx-mod/references/builtins.md).
Search the mod for these patterns:

| Look for | Problem | Fix |
|---|---|---|
| A class named `*Host`, `*Context`, `*Manager`, `*Base`, `ModCore` that every module calls from `init`, or a base class between `FhModule` and the mod's modules | a layer over the framework the Fahrenheit developers asked mods not to add | move what each module needs into the module; delete the layer |
| `new FhLogger(...)`, a logger field passed in, `Console.WriteLine`, a log file of the mod's own | the module already has `_logger` | use `_logger` |
| `Assembly.Location`, `AppContext.BaseDirectory`, `Environment.CurrentDirectory`, hard-coded `mods/<id>` paths | `mod_context.Paths` has the mod's folders | use `mod_context.Paths.ModDir`, `ResourcesDir`, `EflDir`, `LangDir` |
| `AssemblyInformationalVersionAttribute`, a `Version` constant | the manifest is in `mod_context.Manifest` | use `mod_context.Manifest.Version` |
| A config file (`.toml`, `.json`, `.ini`) the mod reads itself, and code to create or merge it | Fahrenheit settings show in the F7 panel and are saved for the player | an `FhSettingProvider<T>` ([runtime.md](../../ffx-mod/references/runtime.md#settings)) |
| Files the mod writes to keep data | global and local state exist for this | the `init` state stream, `save_local_state` / `load_local_state` |
| Static singletons or a registry so modules or mods can find each other | `FhModuleHandle<T>` does this and handles absent mods | `FhModuleHandle<T>.try_get_module` |
| A hook on the main loop, new game, save or load | `FhApi.Events.Common.GameLoop` has these events | subscribe in `init` |
| `GetAsyncKeyState`, a second input layer | `FhApi.Input` and ImGui | use those |
| Its own base address arithmetic, memory read helpers | `FhUtil.ptr_at` / `get_at` / `set_at` | use those |
| A delegate and `FhCallHandle` for a function `FhCall` already declares with a real signature | two declarations to keep in step | use the `FhCall` entry ([calls.md](../../ffx-mod/references/calls.md#the-call-library)) |
| Interfaces, factories or option objects with one implementation and one caller | more code than the mod needs | inline it |

Shared libraries across a family of mods are fine for game logic and file
formats; flag them when they wrap Fahrenheit's own pieces.

## 2. Start-up and lifecycle

Source: [runtime.md](../../ffx-mod/references/runtime.md#startup-order).

- The constructor only sets fields and creates the settings provider and
  module handles. No game calls, no file reading that could fail silently.
- Every hook is registered in `init`, and `init` returns the result of the
  hook calls (or `false` when the module cannot work).
- No game function is called from the constructor or from `init`.
- `init` does not assume another mod's `init` has run, unless that mod is
  earlier in `loadorder` and the README says so.
- Exactly one public parameterless constructor per module; modules are never
  constructed by the mod itself.

## 3. Hooks and calls

Source: [calls.md](../../ffx-mod/references/calls.md).

- Each hook's delegate, `[UnmanagedCallConv]`, parameters and return type
  match each other and the game function. Mark any signature without a
  source (Fahrenheit's `FhCall`, ffx-rust's `symbols/ffx.sym`, a disassembly)
  as unconfirmed.
- No hook or call on a handle whose delegate is `d_UnknownFn`.
- Each hook calls `chain_from(this_hook)` unless it replaces the function on
  purpose, and the code or README says so.
- Calls use `fnptr?.Invoke` or check for null where the target can be
  missing (another module, an export).
- Offsets are `FhCallLocation` offsets in the module (`0x25A620`), not
  absolute addresses copied from a disassembler (`0x0065A620`). The difference
  is the image base `0x400000`.
- Addresses match the game build the SDK version supports
  ([versions.md](../../ffx-mod/references/versions.md)). Addresses from
  the 2019 build do not work with `alpha12` and newer.

## 4. Which games

The product holds FFX (`FFX.exe`), X-2 and Last Mission (both `FFX-2.exe`).
Source: [ffx-mod SKILL.md](../../ffx-mod/SKILL.md#two-games-one-product).

- Every module has `[FhLoad(...)]` listing only the games it works in, and
  the README says which games the mod supports.
- A module that loads in more than one game uses no `Fahrenheit.FFX.FhCall`
  or `Fahrenheit.FFX2.FhCall` entries, offsets or structs of only one game;
  per-game values go through `FhUtil.select`, `FhGlobal.game_id`, or
  separate modules.
- `FhCallLocation` names the right executable (`"FFX.exe"` or
  `"FFX-2.exe"`); a function in both games has both offsets.
- An X-2 module also loads in Last Mission only if it was meant to: they
  share `FFX-2.exe` but are different games (`FFX2` and `FFX2LM`).
- Replaced files for X-2 are under `efl/x2`, not `efl/x`.
- The author tested in every game the modules load in.

## 5. Game folder, saves and assets

Source: [SKILL.md rules](../../ffx-mod/SKILL.md#rules-every-mod-follows),
[structure.md](../../ffx-mod/references/structure.md).

- Nothing writes to the game folder, `FFX.exe`, `FFX-2.exe`, the `.vbf` archives or the
  player's save files.
- Replaced files are under `efl/x/...` or `efl/x2/...`, mirroring the path
  inside the archive.
- The mod ships no game assets that Fahrenheit or the player's own copy can
  provide (textures through `FhApi.Resources`, text through the encoders).
- Local state handlers catch their own exceptions, do not keep the stream,
  and use the version passed to `load_local_state` to handle old data.
- `SEPARATE_SAVES` is set if saves made with the mod would break the vanilla
  game.

## 6. Project and packaging

Source: [structure.md](../../ffx-mod/references/structure.md),
[troubleshooting.md](../../ffx-mod/references/troubleshooting.md).

- `AssemblyName` (the mod ID) is a valid file name, has an author prefix, and
  has not changed since a release.
- The `.csproj` follows the template and does not override properties the SDK
  sets.
- References to Fahrenheit or other mods have `Private=false` and
  `ExcludeAssets=runtime;native`; no Fahrenheit DLL is in the output.
- No copy, fork or patched build of Fahrenheit inside the mod. No reflection
  into Fahrenheit's `internal` types and no `InternalsVisibleTo` tricks.
- The README names the Fahrenheit version and the game build, and tells
  players to add the ID to `mods/loadorder`.
- Install scripts do not touch the game folder or other mods' folders.

## 7. Living with other mods

- The mod works when modules it looks up with `FhModuleHandle<T>` are
  missing.
- Hooks chain, so other mods' hooks on the same function still run.
- No assumption about its position in `loadorder` that the README does not
  state.
