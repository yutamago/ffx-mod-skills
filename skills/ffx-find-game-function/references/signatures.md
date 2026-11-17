# Confirming a signature

Both games are 32-bit x86 programs built with MSVC. A Fahrenheit hook or call
needs the calling convention, the number and size of the arguments, and the
return type exactly right. Read them from the machine code: the function's
own prologue and `ret`, and two or three of its callers.

## Calling convention

| What you see | Convention | C# |
|---|---|---|
| Callee ends with plain `ret`; callers `add esp, N` after the call | `cdecl` | `CallingConvention.Cdecl` / `CallConvCdecl` |
| Callee ends with `ret N`; nothing in `ECX` that the callee reads first | `stdcall` | `CallingConvention.StdCall` / `CallConvStdcall` |
| Callee reads `ECX` before writing it (usually as an object pointer), ends with `ret N` or `ret` | `thiscall` | `CallingConvention.ThisCall` / `CallConvThiscall`; `ECX` is the first parameter |
| Callee reads `EDX`, `EAX`, `ESI` or `EDI` as an argument before writing it | a register convention the compiler made up | none; see below |

`ret N` means the callee removes N bytes of arguments: N / 4 stack words.
With `cdecl`, count the words from the callers' `push`es or from the size of
their `add esp, N`, and check which `[esp+…]` / `[ebp+8+…]` slots the callee
reads.

Fahrenheit's own hand-checked `FhCall` entries use only `Cdecl`, `StdCall`
and `ThisCall` in both games (see `src/core/call.cs`, `src/core/ffx/call.cs` and
`src/core/ffx2/call.cs`).

## Arguments and return value

- Each argument takes one 4-byte stack word, except `double` and 64-bit
  integers (two). Pointers and handles are `nint`, `uint` or a typed pointer.
- A `float` argument is pushed as a 4-byte word, often with `fstp
  dword ptr [esp]` or `movss [esp], xmm0`.
- Return values: `EAX` for integers and pointers (only `AL` for a `bool`),
  `EDX:EAX` for 64-bit, the x87 stack `ST0` for `float` and `double`. If the
  callers ignore `EAX`, declare `void`.
- Structs passed by value are rare; check the callers' stack writes before
  assuming one.

## Conventions a delegate cannot express

Apart from compiler helpers such as `__security_check_cookie`, neither game
has a function declared `__fastcall`: that helper is the only entry with that
convention in Fahrenheit's function lists
([`src/step/data`](https://github.com/fahrenheit-crew/fahrenheit/tree/main/src/step/data)).

Whole-program optimisation still lets MSVC pass the arguments of internal
functions in registers. ffx-rust's `symbols/ffx.sym` (not a Fahrenheit
project) marks these in its comments with wording such as `fastcall(a, b)`
or `fastcall-caller-pops`. For example, in the October 2026 `FFX.exe`,
`0x0042e840` takes its two arguments in `ECX` and `EDX`, and `0x00401690`
takes a third on the stack that the caller removes. Most are in bundled
library code. A comment that names a single argument in `ECX` describes what
a `ThisCall` delegate already expresses.

No delegate can express an argument in `EDX` or another register. Then:

1. Hook a caller or callee with a standard convention that sees the same
   data; or
2. tell the user they can ask on the Fahrenheit Discord whether there is a
   supported way.

Do not hook such a function with a guessed delegate. It will corrupt
registers or the stack and crash later.

## Checking it in the game

A signature is confirmed when a do-nothing hook (log the arguments, chain to
the original, return its result) runs in the game:

- it runs when the behaviour happens, and not constantly when it shouldn't;
- the arguments make sense (pointers point into the game's memory, IDs are in
  range, a `this` matches across calls);
- the game behaves exactly as without the hook, including after the call
  returns.

If the game crashes later than the hook, suspect the convention or the
argument count first.
