# What Fahrenheit already gives you

A mod is meant to be small: inherit `FhModule`, use what the framework hands
you, and write only the part that is new. Agents tend to wrap a framework in
their own "host", "context", "manager" or base class before writing anything
else. In a Fahrenheit mod, don't. The Fahrenheit developers have asked mods
not to invent such layers for things that already exist.

Before you write a helper, a wrapper or a shared base class, look for the need
in this table. If it is there, use the built-in directly from the module.

| You need | Use | Not |
|---|---|---|
| A log | `_logger` on your module (`Debug`, `Info`, `Warning`, `Error`, `Fatal`); one log file per module | your own logger, or passing a logger around |
| The mod's folder and subfolders | `mod_context.Paths` in `init`: `ModDir`, `ResourcesDir`, `EflDir`, `LangDir`, `ManifestPath` | `Assembly.Location`, `AppContext.BaseDirectory`, working-directory guesses |
| The mod's ID, name, version, authors | `mod_context.Manifest` (`Id`, `Name`, `Version`, `Authors`, `Dependencies`, …) | assembly attributes, a version constant |
| Settings players can change | an `FhSettingProvider<YourModule>` with `FhSettingToggle`, `FhSettingNumber<T>`, `FhSettingText`, `FhSettingsCategory` ([runtime.md](runtime.md#settings)) | your own TOML/JSON/INI config file and its loader |
| Data kept between sessions | the global state stream `init` receives | a file of your own next to the DLL |
| Data kept per save game | `save_local_state` / `load_local_state` | writing into the game's saves, or side files keyed by slot |
| Another mod's module | `FhModuleHandle<T>` (`try_get_module`), or `FhApi.Mods` to list loaded mods and modules | static singletons, a registry of your own, reflection |
| Running code every frame | `FhApi.Events.Common.GameLoop.PreUpdate` / `PostUpdate` (subscribe in `init`), or `render_imgui` for drawing | hooking the main loop yourself |
| Reacting to new game, title, game over, save, load, save menu | the other events on `FhApi.Events.Common.GameLoop`: `PostNewGame`, `PostReturnToTitle`, `PostGameOver`, `PreSaveGame`, `PostLoadGame`, `PostOpenSaveMenu`, `PostCloseSaveMenu` | hooking those game functions yourself |
| A window, overlay or menu | ImGui in `render_imgui`, with helpers in `FhApi.Gui` | another UI library, or a window of your own shared by "all my mods" |
| Keys and buttons | `FhApi.Input` (controller actions), `FhApi.Gui.is_any_pressed` and ImGui for keys | polling `GetAsyncKeyState` |
| Images in the UI | `FhApi.Resources` loads textures from disk or from the game | your own image loader; shipping game images |
| A game sound | `FhApi.Audio.play_sound` | |
| Translated strings | `lang/<Module.Type.Name>/<locale>.json` and `FhApi.Localization` ([runtime.md](runtime.md#localization)) | a string table of your own |
| Game text (FFX encoding) | the encoders in `src/core/encoding.cs` | your own character table |
| A game function | the `FhCall` entry, if its signature is real ([calls.md](calls.md)) | a second declaration of the same function |
| Game memory at a fixed offset | `FhUtil.ptr_at<T>`, `get_at<T>`, `set_at<T>`; the structs and `Globals` in `src/core/ffx` and `src/core/ffx2` | your own base-address arithmetic and struct copies |
| Which game is running | `FhGlobal.game_id` (`FFX`, `FFX2`, `FFX2LM`); better, separate modules with `[FhLoad]` | checking the process name or command line |
| A value that differs per game | `FhUtil.select(ffx, ffx2, ffx2lm)` | `if` chains on the process name |
| The game's language | `FhGlobal.lang_id` | reading the game's INI yourself |

Sources, all in the Fahrenheit repository: `src/core/api.cs` (`FhApi`),
`src/core/module.cs` (`FhModule`, `FhModContext`), `src/core/paths.cs`
(`FhModPaths`), `src/core/log.cs`, `src/core/settings.cs`,
`src/core/handles.cs`, `src/core/events/`, `src/core/input.cs`,
`src/core/resources.cs`, `src/core/util.cs`, `src/core/gstate.cs` (`FhGlobal`). Browse them at
https://github.com/fahrenheit-crew/fahrenheit/tree/main/src/core, and check
the tag of the SDK version in use: names change during the alpha (for
example, `FhResources`' texture loading methods differ between `alpha12` and
later builds).

## Shared code across several mods

A library shared by a family of mods is fine when it holds things Fahrenheit
does not have: game logic, file formats, structs not yet in Fahrenheit. It
should not re-wrap Fahrenheit's own pieces (logger, paths, manifest, settings,
state, UI) behind a common start-up method. Each mod's module should still be
a plain `FhModule` that uses `_logger`, `mod_context` and the settings
provider itself.

## When something is missing

If Fahrenheit lacks what the mod needs, write the smallest thing that does the
job inside the mod, and tell the user it is a gap they could raise on the
Discord in their own words. Do not reach into Fahrenheit's `internal` types
with reflection: `src/core/api.cs` says to ask the developers instead.
