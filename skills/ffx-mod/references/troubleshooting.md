# Troubleshooting

Read the wiki's
[Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide)
first for problems with the game version, running as administrator, Linux,
and other tools (Special K, RivaTuner, Malwarebytes, older file loaders).
The [Installation guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Installation-guide)
covers prerequisites and launching, and the
[SDK](https://github.com/fahrenheit-crew/fahrenheit/wiki/SDK) page covers a
local SDK that is ignored after a rebuild. The symptoms below are not on
those pages ([how to read the wiki offline](../SKILL.md#getting-help)).

## Build

| Symptom | Cause and fix |
|---|---|
| `The SDK 'Fahrenheit.Sdk/x' specified could not be found` | That version is not on NuGet (yet). Use a published version, or a local SDK ([versions.md](versions.md)). |
| Fahrenheit DLLs appear in the mod's output | A reference to Fahrenheit or another mod is missing `Private=false` / `ExcludeAssets=runtime;native`. |

## Launch

| Symptom | Cause and fix |
|---|---|
| Fahrenheit exits at once | A mod listed in `loadorder` has no valid manifest whose `Id` equals its folder name. |
| Crashes at boot or early in the game | Game build and Fahrenheit version do not match ([versions.md](versions.md)); or a hook has the wrong signature. |
| No mods are listed in the top-left corner | `mods/loadorder` is missing or unreadable. Fahrenheit logs a warning and loads only its own runtime ([`src/core/bootloader.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/bootloader.cs)). |
| One mod is not listed in the top-left corner | Its ID is not in `loadorder`, its folder name differs from the ID, or no module's `[FhLoad]` includes the running game. |
| Hook never runs | It was registered outside `init`, or an earlier mod's hook does not chain. |

## Crashes

The wiki's
[Install structure](https://github.com/fahrenheit-crew/fahrenheit/wiki/Install-structure)
page says where dumps (`crash/`) and logs (`logs/<session>/`) are and what
to send with a report. In addition, the launcher prints a stack trace with
both .NET and native frames; open the dump in WinDbg or Visual Studio.

Before blaming Fahrenheit, disable all other mods and check again.
