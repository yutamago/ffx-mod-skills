# Troubleshooting

Wiki: [Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide),
[Installation guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Installation-guide).

## Build

| Symptom | Cause and fix |
|---|---|
| `The SDK 'Fahrenheit.Sdk/x' specified could not be found` | That version is not on NuGet (yet). Use a published version, or a local SDK ([versions.md](versions.md)). |
| A newly built local SDK is ignored | Clear the local NuGet caches after every rebuild of Fahrenheit. |
| Fahrenheit DLLs appear in the mod's output | A reference to Fahrenheit or another mod is missing `Private=false` / `ExcludeAssets=runtime;native`. |
| Build errors in a cloned path | The path contains special characters; move the clone. |

## Launch

| Symptom | Cause and fix |
|---|---|
| Fahrenheit exits at once | `mods/loadorder` is missing, or a listed mod has no valid manifest whose `Id` equals its folder name. |
| Crashes at boot or early in the game | Game build and Fahrenheit version do not match ([versions.md](versions.md)); or a hook has the wrong signature. |
| Mod not listed in the top-left corner | Its ID is not in `loadorder`, its folder name differs from the ID, or no module's `[FhLoad]` includes the running game. |
| Hook never runs | It was registered outside `init`, or an earlier mod's hook does not chain. |
| UAC shield on the game executable | "Run as administrator" is enabled; turn it off. Running as administrator is unsupported. |
| Special K deadlocks on boot | Pass `--extdbg` in the launch options. |
| Fahrenheit's interface does not show with RivaTuner | Enable "Use Microsoft Detours API hooking" in RTSS. |
| Linux graphics problems | Use DXVK; `PROTON_USE_WINED3D=1` is unsupported. |

## Crashes

The launcher prints a stack trace with both .NET and native frames and writes
a dump to `crash/`. Logs are in `logs/<session>/`, one file per module plus
the framework's. Open the dump in WinDbg or Visual Studio. When asking for
help, include the session's log folder zipped and the dump.

Before blaming Fahrenheit, disable all other mods and check again.
