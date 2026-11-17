# Confirming a signature

Both games are 32-bit x86 programs built with MSVC. A Fahrenheit hook or call
needs the calling convention, the number and size of the arguments, and the
return type exactly right. Read them from the machine code: the function's
own prologue and `ret`, and two or three of its callers.

## Calling convention

| What you see | Convention | C# |
|---|---|---|
| Callee takes no register argument; ends with plain `ret`; callers clean up with `add esp, N`, or `pop ecx` for one word, somewhere after the call (no arguments: nothing to clean up) | `cdecl` | `CallingConvention.Cdecl` / `CallConvCdecl` |
| Callee takes no register argument; ends with `ret N` | `stdcall` | `CallingConvention.StdCall` / `CallConvStdcall` |
| Callee takes an argument in `ECX` and in no other register, usually an object pointer; ends with `ret N`, or with plain `ret` only when it reads no stack arguments (for a thunk or tail call, judge by the target) | `thiscall` | `CallingConvention.ThisCall` / `CallConvThiscall`; `ECX` is the first parameter |
| Callee takes an argument in `EDX`, `EAX`, `EBX`, `ESI`, `EDI` or any other register besides `ECX`; or takes one in `ECX` plus stack arguments, ends with plain `ret`, and its callers clean up the stack | a register convention the compiler chose | none; see below |

A function **takes an argument in a register** when it uses the register's
incoming value as data: it copies it (`mov edi, ecx`), compares it
(`cmp edx, 0x20`) or dereferences it (`[ecx+0x10]`), and its callers set
that register just before the `call`. These do not count:

- a register pushed in the prologue and popped before `ret` (`push esi`,
  `push edi`, `push ebx`): the function only preserves it;
- `push ecx` at the start that only makes room for a local variable; for
  example Fahrenheit's `Cdecl` entry `graphicVFXCreate` (`FFX.exe+0x244DE0`)
  starts `push ebp; mov ebp, esp; push ecx; push esi`.

Check the last row first: a function that matches it is not `cdecl`,
`stdcall` or `thiscall`, even if it also fits one of those rows.

### How many stack words

The callee decides. `ret N` means it removes N bytes: N / 4 stack words.
Otherwise, find the highest stack slot it reads: `[ebp+0x8]` is the first
word after `push ebp; mov ebp, esp`, `[ebp+0xc]` the second, and so on
(without that frame, `[esp+4]` at entry is the first). Check every path
through the function, not only the first few instructions.

If the function ends by jumping to another function instead of returning (a
thunk such as a lone `jmp`, or a tail call), follow the jump: the target's
`ret N` and stack reads count, and so do its register arguments. For
example, `0x00431170` is a lone `jmp 0x0044ce10`, and the target reads one
stack word.

The callers only confirm it, and are easy to miscount:

- MSVC often merges the cleanup of several calls into one later
  `add esp, N`, or puts it behind a jump, so the size of `add esp` is not
  the argument count.
- `pop ecx` right after a call removes one word; it is cleanup, not an
  argument.
- A caller may push `f`'s later arguments (`x`), then `g`'s argument (`y`),
  call `g` to compute `f`'s first argument, and push its result: `push x; push y; call g; add esp, 4;
  push eax; call f` gives `f` two words, not one.
- `sub esp, 8` followed by `fstp qword ptr [esp]` passes a `double`.

If the callers and the callee (or the function it jumps to) disagree, the
callee's reads win.

Fahrenheit's own hand-checked `FhCall` entries use only `Cdecl`, `StdCall`
and `ThisCall` in both games (see
[`src/core/call.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/call.cs),
[`src/core/ffx/call.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/ffx/call.cs) and
[`src/core/ffx2/call.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/ffx2/call.cs)). Its generated call
files have one `FastCall` delegate, shared by both games:
`FUN_0054923A_0047D890` in
[`src/core/call_1.g.cs`](https://github.com/fahrenheit-crew/fahrenheit/blob/main/src/core/call_1.g.cs), which is
`__security_check_cookie`, a compiler helper, not a function to hook.

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

Fahrenheit's function lists
([`src/step/data`](https://github.com/fahrenheit-crew/fahrenheit/tree/main/src/step/data))
record a calling convention for only 155 of 56,260 functions in FFX and 163
of 59,141 in X-2; the rest are `unknown`. Among the recorded ones, the only `__fastcall`
is the compiler helper `__security_check_cookie`.

MSVC's whole-program optimisation still passes the arguments of some
internal functions in registers. ffx-rust's `symbols/ffx.sym` (not a
Fahrenheit project) marks these in its comments with wording such as
`fastcall(a, b)` or `fastcall-caller-pops`. In the `FFX.exe` with SHA-256
`0537b2a1…686d` (the build ffx.sym's header names):

- `0x0042e840` takes two arguments in `ECX` and `EDX` and none on the stack,
  the fastcall layout;
- `0x00401690` takes two in `ECX` and `EDX` and a third on the stack that
  the caller removes, which no standard convention describes;
- `0x0041e980` takes one argument in `ECX` and two 64-bit ones on the stack
  (four words, `add esp, 0x10` at the caller) that the caller removes, so it
  is not `thiscall` although its only register argument is `ECX`.

Some of these are in bundled library code (libogg, libwebm, the C++ standard
library); others are in the PC port's own engine code (scene, renderer,
settings). A comment that names a single argument in `ECX` and no stack
arguments that the caller removes describes what a `ThisCall` delegate
already expresses.

No delegate can express an argument in `EDX` or another register (.NET does
not support `CallingConvention.FastCall`:
[CallingConvention](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.callingconvention)).
Then:

1. Hook a caller or callee with a standard convention that sees the same
   data; or
2. tell the user they can ask on the Fahrenheit Discord whether there is a
   supported way, or raise an issue themselves, in their own words.

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
