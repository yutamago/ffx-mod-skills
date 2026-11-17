# Mod structure

Read the wiki pages first:
[Mod structure](https://github.com/fahrenheit-crew/fahrenheit/wiki/Mod-structure),
[Manifests](https://github.com/fahrenheit-crew/fahrenheit/wiki/Manifests) and
[Install structure](https://github.com/fahrenheit-crew/fahrenheit/wiki/Install-structure).
They give the rules for a mod ID, the files and subfolders of a mod folder,
the manifest format, which project property becomes which manifest field,
and the layout of a Fahrenheit installation. This file holds only what those
pages do not say ([how to read the wiki offline](../SKILL.md#getting-help)).

## Mod ID

- The mod ID is the project's `AssemblyName`, and it is also the mod's line
  in `mods/loadorder` (one mod ID per line).
- Prefix it with something of the author's to avoid collisions, for example
  `authorname.modname`.
- The template's comment asking for alphanumeric IDs only is out of date;
  the wiki's rule applies (dots and dashes are fine).

## Project file

Copy the template's `.csproj` and keep its structure. Beyond the wiki's list
of properties:

- `Version` is a NuGet version string; the SDK appends the commit hash when
  the project is under git.
- If `RepositoryUrl` is set, it becomes the manifest's `Link` and
  `FhManifestHomePage` is ignored. The Manifests page states the opposite
  order; the SDK's
  [`Sdk.targets`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/sdk/Sdk/Sdk.targets)
  decides.
- `FhManifestFlags` is `NONE` or a comma-separated list. The only other flag
  in current versions is `SEPARATE_SAVES` (the mod gets its own save set);
  check `FhManifestFlags` in the Fahrenheit source for the version in use.
- Do not override properties the SDK sets (target framework, runtime
  identifier, unsafe code and so on).

## Manifest

- Never edit the manifest the SDK generates for a code mod.
- `Dependencies` lists the mod IDs this mod needs. The wiki does not describe
  the field. Load order no longer has to follow dependencies for DLLs to
  resolve; the field is meant for the upcoming mod manager, and the SDK
  currently writes it as empty.

## File mods (`efl`)

The Mod structure page explains how `efl/x` and `efl/x2` mirror the archive.
In a code mod, put the `efl` folder in the project; the SDK copies
`efl/x/**` and `efl/x2/**` into the build output
([`Sdk.props`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/sdk/Sdk/Sdk.props)).

### Making the files

For FFX, [ffx-rust](https://github.com/yutamago/ffx-rust) (a separate
project, not part of Fahrenheit) reads the player's own `FFX_Data.vbf` and
converts most game files to editable forms and back, byte for byte when
unchanged. Build it with `cargo` and run `ffx <command> --help`:

| Command | Files |
|---|---|
| `ffx vbf` | list and extract archive files |
| `ffx kernel` | battle kernel tables (items, commands, …) as TOML |
| `ffx monster` | monster stats and rewards as TOML |
| `ffx battle` | encounter table and formations as TOML |
| `ffx text` | event and battle dialogue as TOML |
| `ffx script` | disassemble and assemble event and monster AI scripts |
| `ffx texture` | textures to DDS and back |
| `ffx model` | models to glTF |
| `ffx motion` | motion groups as JSON |
| `ffx sound` | list sound banks, export samples as WAV |

Each format is described in its
[`docs/formats`](https://github.com/yutamago/ffx-rust/tree/main/docs/formats)
page. Put the result under the Fahrenheit mod's `efl/x/` at the file's path
inside the archive, and check the path before shipping. Use only the
converter: ffx-rust also has its own `dinput8.dll` loader and mod folder,
which a Fahrenheit mod must not use or depend on. It covers FFX only, not
X-2.

## Sharing code between mods

Not on the wiki. A mod can build against another mod's types:

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
