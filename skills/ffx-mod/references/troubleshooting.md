# Troubleshooting

Read the wiki's
[Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide)
first for problems with the game version, running as administrator, Linux,
and other tools (Special K, RivaTuner, Malwarebytes, older file loaders).
The [Installation guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Installation-guide)
covers prerequisites and launching, and the
[SDK](https://github.com/fahrenheit-crew/fahrenheit/wiki/SDK) page covers a local SDK that is ignored after a rebuild, and
the [Build and deployment guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Build-and-deployment-guide) warns about
build errors when the folder path has special characters. The symptoms below are not on
those pages ([how to read the wiki offline](../SKILL.md#getting-help)).

## Build

| Symptom | Cause and fix |
|---|---|
| `The SDK 'Fahrenheit.Sdk/x' specified could not be found` | That version is not on NuGet (yet). Use a published version, or a local SDK ([versions.md](versions.md)). |
| Fahrenheit DLLs appear in the mod's output | A reference to Fahrenheit or another mod is missing `Private=false` / `ExcludeAssets=runtime;native`. |

## Launch

| Symptom | Cause and fix |
|---|---|
| Fahrenheit exits at once | A line in `loadorder` names a folder that has no `<line>.manifest.json`, or that manifest is not valid JSON. Each line is used exactly as written, so a blank line or a stray space counts too. Fahrenheit reads `mods/<line>/<line>.manifest.json` for each line and stops if it cannot ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs), `_init_manifests`). |
| Crashes at boot or early in the game | Game build and Fahrenheit version do not match ([versions.md](versions.md)); or a hook has the wrong signature. |
| On the main menu, the top-left corner shows `1 mods loaded` and only *Fahrenheit Runtime* | `mods/loadorder` is missing, unreadable or empty. Fahrenheit loads only its own runtime; when the file is missing or unreadable it also writes a warning to the framework log in `logs/<session>/` ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs), `_init_load_order`). |
| One mod is not listed in the top-left corner of the main menu | Its ID is not in `loadorder`. |
| A mod is listed but its code never runs | The manifest's `Id` differs from the folder and DLL name, so Fahrenheit looks for a DLL that does not exist; or no module's `[FhLoad]` includes the running game, or the module class is not public or has no `[FhLoad]` (the framework log says `Loader ignored module type …`). |
| Hook never runs | It was registered after `init` on a function that some mod hooked during `init` (the framework log says `Late insertion rejected`), or a mod later in `loadorder` hooks the same function and does not chain ([calls.md](calls.md#which-hook-runs-first)). |

## Crashes

The wiki's
[Install structure](https://github.com/fahrenheit-crew/fahrenheit/wiki/Install-structure)
page says where dumps (`crash/`) and logs (`logs/<session>/`) are and what
to send with a report. In addition, the launcher prints a stack trace with
both .NET and native frames; open the dump in WinDbg or Visual Studio.

Before blaming Fahrenheit, disable all other mods and check again.
