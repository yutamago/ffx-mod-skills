# Where to look

## 1. Fahrenheit

Use the source at the tag of the SDK version the mod builds against
(https://github.com/fahrenheit-crew/fahrenheit/tree/main/src/core, switch to
the tag). Fahrenheit's names and signatures are what other mods use, so prefer
them.

| Path | What |
|---|---|
| `src/core/call.cs` | `Fahrenheit.FhCall`: functions identical in both games |
| `src/core/ffx/call.cs` | `Fahrenheit.FFX.FhCall`: FFX functions with checked signatures |
| `src/core/ffx/call_N.g.cs` | generated handles for every other FFX function, named `FUN_<offset>`, typed `d_UnknownFn` (no signature) |
| `src/core/ffx/call_atel.cs` | the ATEL script engine's native functions (`AtelFn_*`) |
| `src/core/ffx/*.cs`, `ffx/battle/`, `ffx/ids/` | game structs, enums and IDs |
| `src/core/ffx/gstate.cs` | `Globals`: fixed addresses of game objects |
| `src/core/ffx2/call.cs`, `ffx2/call_N.g.cs` | `Fahrenheit.FFX2.FhCall`: the same for `FFX-2.exe` (X-2 and Last Mission) |
| `src/core/ffx2/atel/` | X-2's ATEL calls |
| `src/core/ffx2/*.cs`, `ffx2/battle/` | X-2 structs and data tables (including Last Mission ones, `Lm*`) |

A `FUN_…` handle tells you a function starts there and nothing else. Treat it
as unknown until you confirm a signature
([signatures.md](signatures.md)).

Search by behaviour words as well as by C++-style names: the hand-written
entries use the game's own class and method names where known
(`PhyreScene_doDeleteMeshInstances`).

## 2. ffx-rust (FFX only)

Nothing below covers `FFX-2.exe`. For X-2 and Last Mission go from
Fahrenheit (section 1) to a disassembler (section 3). A function that both
games share (engine, PhyreEngine, the C runtime) can be looked up in
ffx-rust for FFX and then matched in `FFX-2.exe` by its code, strings or
callers; Fahrenheit's shared `FhCall` entries show many such pairs.

[ffx-rust](https://github.com/yutamago/ffx-rust) is a separate project that
reverse-engineers `FFX.exe` to reimplement it. It is not part of Fahrenheit
and the Fahrenheit team does not support it. It is useful because it names
far more of the executable.

- **`symbols/ffx.sym`**: one line per function or label,
  `<address> <function|label> <name> # comment`. The header gives the
  SHA-256 of the `FFX.exe` it describes; compare it with the user's file
  before using any address. The comments often give the calling convention,
  arguments and callers.
  - Comments starting `fh v4`, `fh v3`, `fh switch` or `fh … call.cs` are
    names from the Fahrenheit team's database, merged with their permission;
    `call.cs` ones are their hand-checked signatures.
  - `BSim` matches and comments starting `guess:` are the least certain:
    confirm before relying on them.
  - Some functions use conventions a C# delegate cannot express (the
    comments say for example `fastcall-caller-pops` or `ecx = … (no stack
    words)`); see [signatures.md](signatures.md#conventions-a-delegate-cannot-express).
- **`docs/formats/*.md`**: one page per area (`battle.md`, `field.md`,
  `menu.md`, `save.md`, `script.md`, `text.md`, `sound.md`, `render.md`, …)
  with structs, globals and which functions read them.
- **`ffx script disasm`**: disassembles ATEL scripts with native calls
  resolved to their `FFX.exe` handlers, useful when an in-game event is the
  entry point.

Addresses in `ffx.sym` are absolute `FFX.exe` addresses. Subtract
`0x400000` for `FhCallLocation`.

## 3. A disassembler

- The Fahrenheit team runs a Ghidra server with their database of the game,
  free for modders: ask on the Discord (https://discord.gg/AGx2grw9nD).
- Otherwise open the user's own `FFX.exe` or `FFX-2.exe` in Ghidra, IDA,
  Binary Ninja or rizin. Do not share the executables.

## 4. Community data references

[FFXDataParser](https://github.com/Karifean/FFXDataParser) documents FFX's
data file formats (kernel tables, monsters, scripts), which tells you what a
function reads even when it does not name the function. For X-2's data,
start from the tables Fahrenheit already models in `src/core/ffx2`.

## Finding it yourself

When no source names the function, pick an entry point and follow
references:

| Start from | Then |
|---|---|
| A string the behaviour shows or logs | find the string, then the code that references it |
| A known function nearby (a caller or callee in `FhCall` or `ffx.sym`) | walk the call graph |
| A value that changes (HP, gil, a flag) | find its address with a memory search while playing, then the code that writes it |
| An in-game event or a monster's action | disassemble its ATEL script, find the native call, then its handler (`AtelFn_*` in Fahrenheit, resolved handlers in ffx-rust) |
| A data file the behaviour depends on | its format (ffx-rust `docs/formats`, FFXDataParser), then the code that parses it |

Prefer hooking the narrowest function that does the job: a function called
once per action is easier to reason about than the main loop, and less likely
to be hooked by other mods.
