---
name: ffx-find-game-function
description: Find, name and confirm a function, global or struct in FFX.exe or FFX-2.exe (Final Fantasy X, X-2 and X-2 Last Mission in the Final Fantasy X/X-2 HD Remaster on Steam) for a Fahrenheit mod to hook or call. Use when a mod needs "the function that does X", when someone has an address from an old mod or a forum post, when an FhCall entry is d_UnknownFn, when a hook crashes and the signature is in doubt, or when converting addresses between game builds.
---

# Finding and confirming a game function

Almost every code mod starts by finding the game function behind a behaviour.
A wrong address or signature crashes the game, often somewhere else and later,
so the work is not done when you have a name: it is done when the signature
is confirmed and a test hook has run in the game.

The mod itself follows the `ffx-mod` skill
([../ffx-mod/SKILL.md](../ffx-mod/SKILL.md)); hooking and calling
are in its [calls.md](../ffx-mod/references/calls.md).

## Steps

1. **Pin the game and the build.** Which game: FFX (`FFX.exe`), X-2 or
   Last Mission (both `FFX-2.exe`); see
   [two games, one product](../ffx-mod/SKILL.md#two-games-one-product). Get
   the SHA-256 of that executable and the Fahrenheit version of the mod.
   Every address below is only valid for one executable of one build
   ([versions.md](../ffx-mod/references/versions.md)). Never use an FFX
   address in X-2 or the other way round, and never mix builds. If the mod
   needs the function in both games, find and confirm it in each.
2. **Look it up, in this order**, and stop at the first source with a real
   signature ([references/sources.md](references/sources.md)):
   1. Fahrenheit's `FhCall` library, structs and `Globals` for the SDK version
      in use: the shared, FFX and X-2 parts.
   2. For FFX only: ffx-rust's symbol map `symbols/ffx.sym` and
      `docs/formats/*.md` (not part of Fahrenheit). There is no equivalent for
      `FFX-2.exe`; for X-2, a function shared with FFX can be found in
      ffx-rust and then matched in `FFX-2.exe` by its code.
   3. The Fahrenheit team's Ghidra server (ask on the Discord), or a
      disassembler on the user's own executable.
3. **Find it yourself** if no source has it: start from a string, a known
   neighbour, a piece of data the behaviour changes, or the ATEL native call
   that triggers it ([references/sources.md](references/sources.md#finding-it-yourself)).
4. **Confirm the signature** from the machine code, not from a name or a
   guess: calling convention, argument count and types, return value
   ([references/signatures.md](references/signatures.md)).
5. **Test with a do-nothing hook.** Hook it in `init`, log the arguments
   with `_logger`, chain to the original, and trigger the behaviour in the
   game. The hook should run when expected, with sensible arguments, and the
   game should behave as without the mod. Only then write the real change.
6. **Write it down** (format below) and tell the user what is confirmed and
   what is not.

## Converting addresses

Disassemblers and `ffx.sym` show absolute addresses (image base plus
offset). `FhCallLocation` takes the offset inside the executable:
`offset = address - image base`. Read the image base from the disassembler
or the PE header of the executable you are working on. For `FFX.exe` it is
`0x400000`: `PhyreScene_doDeleteMeshInstances` is `0x0065a620` in `ffx.sym`
and `0x25A620` in Fahrenheit's `FhCall`.

| Function is in | Declare it as |
|---|---|
| FFX only | `new FhCallLocation("FFX.exe", ffx_offset)` |
| X-2 and Last Mission only | `new FhCallLocation("FFX-2.exe", x2_offset)` |
| both games | `new FhCallLocation(ffx_offset, x2_offset)`, for example Fahrenheit's shared `FUN_0048e750_0034c250` at `(0x48E750, 0x34C250)` |

The same function is almost never at the same offset in both executables.

An address from another game build (for example the 2019 build that
Fahrenheit `alpha11` and older target) is a hint, not an address. Find the same
function in the current build by its code, strings or callers, and confirm it
again.

## Record

For each function, keep this next to the declaration in the mod (a comment
is enough):

```text
name        PhyreScene_doDeleteMeshInstances
game        FFX
offset      0x25A620 in FFX.exe (sha256 0537b2a1…)
signature   thiscall void (PhyreScene* this)
source      Fahrenheit FhCall (call.cs) / ffx.sym / own disassembly
confirmed   yes: test hook ran on map change, this matched the scene pointer
```

Say plainly when a signature is unconfirmed. Do not present a guess as a
fact.

## Sharing what you find

Names and signatures help everyone. Suggest the user share new findings on
the Fahrenheit Discord, Cid's Salvage Ship (https://discord.gg/AGx2grw9nD), in
their own words. Never open issues or pull requests on `fahrenheit-crew`
repositories.
