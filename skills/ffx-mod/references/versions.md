# Fahrenheit versions and game builds

Read the wiki's
[Compatibility guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Compatibility-guide)
first: it says which Fahrenheit versions support which Steam build of the
game, with the Steam manifest IDs. The table is not repeated here, because it
changes with each release. For local SDKs and building Fahrenheit, read the
[SDK](https://github.com/fahrenheit-crew/fahrenheit/wiki/SDK) and
[Build and deployment guide](https://github.com/fahrenheit-crew/fahrenheit/wiki/Build-and-deployment-guide)
pages. This file holds only what those pages do not say
([how to read the wiki offline](../SKILL.md#getting-help)).

- Fahrenheit does not check the game version, so a mismatch shows up as
  crashes, not as an error message. Confirm the pair before debugging
  anything else.
- The game build is the build of the whole Steam product, so one Fahrenheit
  version covers `FFX.exe` and `FFX-2.exe` of the same build.

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
- **Build Fahrenheit from source and use a local SDK** (developers only).
  Follow the wiki's Build and deployment guide and SDK pages exactly. Mods
  built against a local SDK are for testing: rebuild them against the
  official SDK before distributing.

## Upgrading a mod

Change the version in the `Sdk` attribute, rebuild, and fix what breaks: the
API is not stable during the alpha. Read the release notes of every version in
between. Tell the user that players must update Fahrenheit and the mod
together.
