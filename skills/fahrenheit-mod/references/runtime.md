# Modules, startup, state, settings, localization

Wiki pages: [Modules](https://github.com/fahrenheit-crew/fahrenheit/wiki/Modules),
[Startup](https://github.com/fahrenheit-crew/fahrenheit/wiki/Startup),
[State](https://github.com/fahrenheit-crew/fahrenheit/wiki/State),
[Settings](https://github.com/fahrenheit-crew/fahrenheit/wiki/Settings),
[Localization](https://github.com/fahrenheit-crew/fahrenheit/wiki/Localization).

## Modules

A code mod contains one or more modules: public classes deriving from
`FhModule`. Each module:

- has exactly one public parameterless constructor;
- overrides `init`;
- carries `[FhLoad(FhGameId.FFX | FhGameId.FFX2 | FhGameId.FFX2LM)]` (or a
  subset) naming the games it loads in;
- gets its own log (`_logger`), global state and local state.

Never construct a module yourself; Fahrenheit does. Split a mod into several
modules when parts are independent or game-specific.

## Startup order

1. Every module of every mod is constructed.
2. Every module's `init` runs, mod by mod in load order.
3. Hooks are committed and the game starts.

| Phase | Allowed | Not allowed |
|---|---|---|
| Constructor | set fields; create the settings provider | module handles, call handles, `FhApi` |
| `init` | subscribe to events, hook functions, module handles, `FhApi`, global state | calling game functions |
| After `init` | calling game functions, module handles, `FhApi` | new hooks on already hooked functions |

Return `false` from `init` only if the module cannot work; Fahrenheit logs a
warning and continues.

Because all modules exist before any `init` runs, a module can fetch another
module with `FhModuleHandle<T>` in `init` regardless of load order. It cannot
rely on the other module's `init` having run already, unless the other module
is listed earlier in `loadorder`.

## Talking to other modules

```cs
private readonly FhModuleHandle<OtherModule> _other;
public MyModule() { _other = new(this); }

public override bool init(FhModContext mod_context, FileStream global_state_file) {
    if (_other.try_get_module(out OtherModule? other)) { /* use it */ }
    return true;
}
```

Always handle the module being missing: the user may not have the mod, or the
module may not load for the current game.

## State

Never store mod data in the game's save files or in files of your own choosing.

- **Global state**: `init` receives a `FileStream`. Keep it if you need it;
  Fahrenheit never closes it. The format is up to the mod.
- **Local state** (per save game): override `save_local_state` and
  `load_local_state`. Both must catch their own exceptions and must not keep
  the stream. `load_local_state` receives the version of the mod that wrote
  the file; use it to migrate or reject old data.

Set `SEPARATE_SAVES` in `FhManifestFlags` when the mod changes the game so
much that its saves should not mix with vanilla saves.

## Settings

Create one class deriving from `FhSettingProvider<YourModule>`, instantiate it
in the module's constructor, and return the settings in display order from
`get()`. Built-in setting types include `FhSettingToggle` (bool) and
`FhSettingNumber<T>`. Players change them in the mod configuration panel
(F7).

## Localization

Put strings in `lang/<Full.Type.Name.Of.Module>/<locale>.json`, for example
`lang/Author.Mod.MyModule/en-US.json`, and look them up with
`FhApi.Localization.localize("string_id", this)`. The folder name must match
the module's full type name exactly.

## Game text

Fahrenheit can encode and decode the games' text format at runtime, so mods
can create or change in-game strings without shipping game files. Look for the
encoding helpers in `src/core/encoding.cs` of the Fahrenheit version in use.

## User interface

Fahrenheit bundles ImGui for custom interfaces and can load game textures for
use in them, so mods need not ship copyrighted images.
