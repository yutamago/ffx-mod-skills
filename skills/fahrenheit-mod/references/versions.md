# Fahrenheit versions and game builds

Fahrenheit relies on the exact layout of one game executable. It does not
check the game version itself, so a mismatch shows up as crashes, not as an
error message. Always confirm the pair before debugging anything else.

| Fahrenheit | Game build it supports | Steam manifest ID |
|---|---|---|
| `1.0.0-alpha11` and older | March 27, 2019 | `5168047039601173807` |
| `1.0.0-alpha12` and newer | October 1, 2026 (current Steam build) | `1235377778411650212` |

Source: the wiki's
[Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide).
Check it again; this table may be out of date.

Only genuine Steam copies are supported. Modified executables are not.

## Choosing a version

1. Find which game build the user has (Steam updates to the newest build
   unless they downgraded on purpose).
2. Look up the published SDK versions:
   https://www.nuget.org/packages/Fahrenheit.Sdk (and the
   [releases page](https://github.com/fahrenheit-crew/fahrenheit/releases) for
   the matching player download).
3. Use the newest Fahrenheit that supports the user's game build, and put that
   version in the project's `Sdk` attribute.

## When the matching version is not released yet

If the user's game build needs a Fahrenheit version that has no release and no
SDK on NuGet yet, there are two options. Explain both and let the user choose:

- **Wait for the release.** Simplest, and the only sensible choice for
  players.
- **Build Fahrenheit from source and use a local SDK** (developers only). The
  managed parts build on any system with the .NET 10 SDK; the native Stage 0
  and Stage 1 loaders need Visual Studio's C++ workload on Windows, or can be
  taken from the latest release. Building produces a local SDK package in
  `artifacts/pkg/{dbg,rel}`; add that folder as a NuGet source. Follow the
  wiki's
  [Build and deployment guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Build-and-deployment-guide)
  and [SDK](https://github.com/fahrenheit-crew/fahrenheit/wiki/SDK) pages
  exactly. Mods built against a local SDK are for testing: rebuild them against
  the official SDK before distributing, and disable the local NuGet source
  when doing so.

## Upgrading a mod

Change the version in the `Sdk` attribute, rebuild, and fix what breaks: the
API is not stable during the alpha. Read the release notes of every version in
between. Tell the user that players must update Fahrenheit and the mod
together.
