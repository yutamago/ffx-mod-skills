# Modules, startup, state, settings, localization

Read the wiki pages first:
[Modules](https://github.com/fahrenheit-crew/fahrenheit/wiki/Modules),
[Startup](https://github.com/fahrenheit-crew/fahrenheit/wiki/Startup),
[State](https://github.com/fahrenheit-crew/fahrenheit/wiki/State),
[Settings](https://github.com/fahrenheit-crew/fahrenheit/wiki/Settings),
[Localization](https://github.com/fahrenheit-crew/fahrenheit/wiki/Localization).
They give the rules for a module, what is allowed in the constructor, in
`init` and afterwards, module handles, global and local state, setting
providers and the `lang` folder. This file holds only what those pages do not
say ([how to read the wiki offline](../SKILL.md#getting-help)).

## Modules

- `init` receives the mod's `FhModContext`: its folders (`Paths`) and its
  manifest (`Manifest`, including the version). The wiki's examples show the
  parameter but not what it holds. Use it and `_logger` directly;
  [builtins.md](builtins.md) lists what else not to rebuild.
- Split a mod into several modules when parts are independent or
  game-specific.

## Startup order

The wiki gives the rules per stage but not the order across mods:

1. Every module of every mod is constructed.
2. Every module's `init` runs, mod by mod in load order.
3. The game starts.

So a module can fetch another module with `FhModuleHandle<T>` in `init`
regardless of load order, but it can rely on the other module's `init` having
run only if that mod is listed earlier in `loadorder`.

Return `false` from `init` only if the module cannot work. Fahrenheit logs a
warning and carries on with the other modules
([`src/core/mods.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/mods.cs)).

## State

Set `SEPARATE_SAVES` in `FhManifestFlags` when the mod changes the game so
much that its saves should not mix with vanilla saves. The wiki's State and
Manifests pages do not describe the flag
([`FhManifestFlags`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/module.cs)).

## Settings

The wiki page lists `FhSettingToggle` and `FhSettingNumber<T>`. Check
`src/core/settings.cs` of the Fahrenheit version in use for the other
built-in types before writing one ([builtins.md](builtins.md)).

## Game text

Not on the wiki. Fahrenheit can encode and decode the games' text format at
runtime, so mods can create or change in-game strings without shipping game
files. Look for the encoding helpers in `src/core/encoding.cs` of the
Fahrenheit version in use.

## User interface

Not on the wiki. Fahrenheit bundles ImGui for custom interfaces and can load
game textures for use in them, so mods need not ship copyrighted images.
