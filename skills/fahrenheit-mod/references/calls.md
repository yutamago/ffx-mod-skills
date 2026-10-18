# Calling and hooking game functions

Wiki page: [Calls](https://github.com/fahrenheit-crew/fahrenheit/wiki/Calls).

## The pieces

A call handle, `FhCallHandle<TDelegate>`, needs two things:

- **Signature**: a delegate type giving calling convention, return type and
  arguments.
- **Location**: an `FhCallLocation`.

```cs
[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
public delegate int d_SomeFunction(int a, nint b);

public static FhCallHandle<d_SomeFunction> SomeFunction
    => new(new FhCallLocation("FFX.exe", 0x123450));   // offset in the module
```

`FhCallLocation` forms:

| Constructor | Targets |
|---|---|
| `(nint ffx, nint ffx2)` | the same function in both games, by offset |
| `(string module, nint offset)` | a function at an offset in a module |
| `(string module, string export)` | an exported function |
| `(nint address)` | an absolute address, for example a vtable slot |

## The call library

`FhCall` already has a handle for every function in both games:

| Namespace | Functions |
|---|---|
| `Fahrenheit.FhCall` | identical in both games |
| `Fahrenheit.FFX.FhCall` | FFX only |
| `Fahrenheit.FFX2.FhCall` | X-2 and Last Mission only |

Only reversed functions have real signatures. A handle whose delegate is
`d_UnknownFn` has no known signature; calling or hooking it will almost
certainly crash. Then either:

- confirm the signature yourself in a disassembler and declare your own handle
  in the mod (as above), or
- ask the Fahrenheit developers on Discord to reverse it.

Prefer an existing `FhCall` entry over your own declaration when it has a real
signature.

## Calling

```cs
int r = FhCall.SomeFunction.fnptr!(1, ptr);   // crash if not found
FhCall.SomeFunction.fnptr?.Invoke(1, ptr);    // call only if found
```

`fnptr` is null when the module is not loaded or the export does not exist.
Call game functions only after `init` has returned.

## Hooking

Hook in the module's `init` and return the result:

```cs
public override bool init(FhModContext mod_context, FileStream global_state_file) {
    return FhCall.SomeFunction.hook(this, h_some_function);
}

[UnmanagedCallConv(CallConvs = [ typeof(CallConvCdecl) ])]
private int h_some_function(int a, nint b) {
    // before
    int r = FhCall.SomeFunction.chain_from(h_some_function).fnptr!(a, b);
    // after
    return r;
}
```

- The hook's `[UnmanagedCallConv]` must match the delegate's calling
  convention, and its parameters and return type must match exactly.
- Call `chain_from(this_hook)` to run the next hook or the original. Skip it
  only when the mod deliberately replaces the function, and say so: it also
  disables every later mod's hook on that function.
- Hooks registered during `init` run in load order.
- A function that nobody hooked during `init` may be hooked later; such late
  hooks run in the order they were added.

## Calling conventions in these games

The games are 32-bit x86. Expect `cdecl`, `stdcall`, `thiscall` (object
pointer in ECX) and `fastcall`. Compiler-generated functions sometimes pass
values in other registers, which a delegate cannot express. If a function's
convention is unclear, look at how its callers set up the stack and registers,
and at its `ret` instruction (`ret N` means the callee pops N bytes).
