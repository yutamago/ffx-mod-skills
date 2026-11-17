# Calling and hooking game functions

Read the wiki's [Calls](https://github.com/fahrenheit-crew/fahrenheit/wiki/Calls)
page first. It explains call handles (`FhCallHandle<T>`), signatures and
locations, the `FhCall` library, calling through `fnptr`, hooking in `init`
and chaining with `chain_from`. This file holds only what that page does not
say ([how to read the wiki offline](../SKILL.md#getting-help)).

## Not on the wiki page

### X-2 and Last Mission

The wiki's examples target `FFX.exe`. An X-2 function names `FFX-2.exe`:

```cs
public static FhCallHandle<d_X2Function> X2Function
    => new(new FhCallLocation("FFX-2.exe", 0x134BD0));
```

X-2 and Last Mission run the same `FFX-2.exe`, so their offsets are the same.
A function both games share has a different offset in each; look up both for
the `(nint ffx, nint ffx2)` constructor.

### A function without a signature

The wiki says a `d_UnknownFn` handle will likely not work and to raise an
issue or contact the team. For an agent that means:

- confirm the signature yourself in a disassembler and declare your own
  handle in the mod (the `ffx-find-game-function` skill has the method), or
- tell the user they can ask the Fahrenheit developers on the Discord, or
  raise an issue themselves, in their own words. Never raise it for them
  ([why](../SKILL.md#working-on-fahrenheit-itself)).

Prefer an existing `FhCall` entry over your own declaration when it has a
real signature, so there is one declaration to keep right.

### Replacing a function

The wiki allows a hook to return without chaining. Do that only when the mod
is meant to replace the function, and say so in the code and the README: it
also switches off every later mod's hook on that function.

### Calling conventions in these games

The wiki shows where the convention goes but not how to find it. The games
are 32-bit x86. Fahrenheit's hand-checked `FhCall` entries use `cdecl`,
`stdcall` and `thiscall` (object pointer in `ECX`), and a delegate can
express all three. Its function lists
([`src/step/data`](https://github.com/fahrenheit-crew/fahrenheit/tree/main/src/step/data))
record a convention for only about 160 functions per game; most entries say
`unknown`, so work it out from the machine code.

If a function's convention is unclear, look at how its callers set up the
stack and registers, and at its `ret` instruction (`ret N` means the function
removes N bytes of arguments). A few internal functions take arguments in
other registers, which no delegate can express: do not guess one. The
`ffx-find-game-function` skill has the full method
([`ffx-find-game-function/references/signatures.md`](../../ffx-find-game-function/references/signatures.md)).
