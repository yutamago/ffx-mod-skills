# Mod structure

## Mod ID

The mod ID is the project's `AssemblyName`. It names the DLL, the manifest,
the mod's folder, its line in `loadorder` and its saved state.

- It must be unique across all mods and must never change after release.
- It must be a valid file name: no spaces and no characters that are invalid
  in a Windows path. Dots and dashes are fine. (The template's comment asking
  for alphanumeric IDs only is out of date; the wiki's rule applies.)
- Prefix it with something of the author's to avoid collisions, for example
  `authorname.modname`.

## Project file

Copy the template's `.csproj` and keep its structure. The properties that
matter:

| Property | Becomes | Notes |
|---|---|---|
| `AssemblyName` | manifest `Id`, DLL name | the mod ID; required |
| `AssemblyTitle` | manifest `Name` | display name; may change |
| `Product` | Windows file properties | usually the same as `AssemblyTitle` |
| `Description` | manifest `Desc` | |
| `Version` | manifest `Version` | NuGet version string; the SDK appends the commit hash under git |
| `Authors` | manifest `Authors` | comma-separated |
| `RepositoryUrl` | manifest `Link` | takes precedence over `FhManifestHomePage` |
| `FhManifestHomePage` | manifest `Link` | used when there is no `RepositoryUrl` |
| `FhManifestFlags` | manifest `Flags` | required; `NONE` or a comma-separated list |

Do not override properties the SDK sets (target framework, runtime identifier,
unsafe code and so on).

Flags in current versions: `NONE`, and `SEPARATE_SAVES` (the mod gets its own
save set). Check `FhManifestFlags` in the Fahrenheit source for the version in
use.

## Manifest

Every mod folder needs `<mod_id>.manifest.json` with `Id` equal to the folder
name, or Fahrenheit refuses to start. Code mods get it generated at build
time; never edit the generated file. File mods without code write it by hand:

```json
{
    "Id": "authorname.modname",
    "Name": "Readable name",
    "Desc": "What it changes.",
    "Authors": "Author",
    "Version": "1.0.0",
    "Link": "https://example.com/where-to-get-it",
    "Dependencies": [],
    "Flags": "NONE"
}
```

`Dependencies` lists the mod IDs this mod needs. Load order no longer has to
follow dependencies for DLLs to resolve; the field is meant for the upcoming
mod manager. The SDK currently writes it as empty.

## Folder layout

```text
mods/
  loadorder                     one mod ID per line
  <mod_id>/
    <mod_id>.manifest.json
    <mod_id>.dll                code mods only, with .deps.json, .runtimeconfig.json, .pdb
    efl/x/...                   files replacing FFX_Data.vbf contents
    efl/x2/...                  files replacing FFX2_Data.vbf contents
    lang/<Module.Full.TypeName>/<locale>.json
    resources/...               anything the mod wants
```

Players must not edit or delete files inside a mod folder.

## File mods (`efl`)

`efl/x` and `efl/x2` each stand for the root of the respective archive. Mirror
the path inside the archive exactly:

```text
ffx_ps2/ffx/master/jppc/battle/kernel/takara.bin
  -> efl/x/ffx_ps2/ffx/master/jppc/battle/kernel/takara.bin
```

In a code mod, put the `efl` folder in the project; the SDK copies
`efl/x/**` and `efl/x2/**` into the build output.

## Sharing code between mods

A mod can build against another mod's types:

```xml
<ProjectReference Include="../othermod/othermod.csproj">
    <Private>false</Private>
    <ExcludeAssets>runtime;native</ExcludeAssets>
</ProjectReference>
```

`Private=false` and `ExcludeAssets` keep the other mod's DLL out of this
mod's output, so only one copy is loaded and shared at runtime. The other mod
must still be installed and listed in `loadorder`. Get its modules through
`FhModuleHandle<T>` and handle it being missing.
