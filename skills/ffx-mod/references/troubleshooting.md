# Troubleshooting

Read the wiki first:

- [Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide): the game version, running
  as administrator, Linux, and other tools (Special K, RivaTuner,
  Malwarebytes, older file loaders);
- [Installation guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Installation-guide): prerequisites and launching;
- [SDK](https://github.com/fahrenheit-crew/fahrenheit/wiki/SDK): a local SDK that is ignored after a rebuild;
- [Build and deployment guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Build-and-deployment-guide): build errors
  when the folder path has special characters.

The symptoms below are not on those pages ([how to read the wiki offline](../SKILL.md#getting-help)).

## Build

| Symptom | Cause and fix |
|---|---|
| `The SDK 'Fahrenheit.Sdk/x' specified could not be found` | That version is not on NuGet (yet). Use a published version, or a local SDK ([versions.md](versions.md)). |
| Fahrenheit DLLs appear in the mod's output | A reference to Fahrenheit or another mod is missing `Private=false` / `ExcludeAssets=runtime;native`. |

## Launch

| Symptom | Cause and fix |
|---|---|
| Fahrenheit exits at once | The wiki's [Manifests](https://github.com/fahrenheit-crew/fahrenheit/wiki/Manifests) page says a mod without a manifest stops the game. In detail: a line in `loadorder` names a folder that has no `<line>.manifest.json`, or that manifest is not valid JSON. Each line is used exactly as written, so a blank line or a stray space counts too. Fahrenheit reads `mods/<line>/<line>.manifest.json` for each line and stops if it cannot ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs), `_init_manifests`). |
| Fahrenheit exits at boot with `Constructor of module … threw or faulted` in the framework log | A module's constructor threw. Keep constructors to setting fields and creating the settings provider ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs)). |
| Crashes at boot or early in the game | Game build and Fahrenheit version do not match ([versions.md](versions.md)); or a hook has the wrong signature. |
| On the main menu, the top-left corner shows `1 mods loaded` and only *Fahrenheit Runtime* | `mods/loadorder` is missing, unreadable or empty. Fahrenheit loads only its own runtime; when the file is missing or unreadable it also writes a warning to the framework log in `logs/<session>/` ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs), `_init_load_order`). |
| One mod is not listed in the top-left corner of the main menu | Its ID is not in `loadorder`. |
| A mod is listed but its code never runs | The manifest's `Id` differs from the folder and DLL name, so Fahrenheit looks for a DLL that does not exist; or a module has no `[FhLoad]` or one without the running game (the framework log says `Loader ignored module type …`), or the module class is not public (skipped without a log line). See `load_mod` in [`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs). |
| Hook never runs: registered after `init` | The function was hooked by some mod during `init`, so later hooks are rejected; the framework log says `Late insertion rejected`. |
| Hook never runs: another mod | A mod later in `loadorder` hooks the same function and does not chain ([calls.md](calls.md#which-hook-runs-first)). |
| Hook never runs: `hook()` returned `false` | The target was not found ([runtime.md](runtime.md#startup-order)). Nothing is logged for an offset in a module that is not loaded; a missing export logs `No export`. |
| Hook never runs: installation failed | A queued hook failed to install. Fahrenheit stops there, so every hook of any mod not yet installed stays uninstalled. The framework log shows `MH_CreateHook() failed` or `MH_EnableHook() failed` (`chain_finalize` in [`src/core/handles.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/handles.cs)). |

## Crashes

The wiki's
[Install structure](https://github.com/fahrenheit-crew/fahrenheit/wiki/Install-structure)
page says where dumps (`crash/`) and logs (`logs/<session>/`) are and what
to send with a report. In addition, the launcher prints a stack trace with
both .NET and native frames; open the dump in WinDbg or Visual Studio.

Before blaming Fahrenheit, disable all other mods and check again.
