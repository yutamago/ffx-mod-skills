# Submitting findings to ffx-rust

Research findings about FFX go to [ffx-rust](https://github.com/yutamago/ffx-rust)
as new pull requests, so the next modder (or agent) finds them in
`symbols/ffx.sym` and `docs/formats/` instead of researching them again.
ffx-rust is a separate project, not part of Fahrenheit.

## What counts as a finding

Anything about `FFX.exe` or FFX's data that ffx-rust does not have yet, or
has wrong:

- a function's name, purpose, calling convention or arguments;
- a global, a struct field, a table, a constant;
- a file format detail, or what a field in a data file does;
- a correction to an existing line or page.

ffx-rust covers FFX only. Findings about `FFX-2.exe` (X-2, Last Mission)
have no home there; suggest the user share them on the Fahrenheit Discord
instead.

## Where each finding goes

| Finding | File |
|---|---|
| A name, signature or note for an address | `symbols/ffx.sym`: one line `<address> <function\|label> <name> # <comment>`, kept sorted by address, absolute address (offset + `0x400000`), the evidence in the comment |
| How a format, table or subsystem works | the matching `docs/formats/<area>.md` page, citing the `FFX.exe` functions it comes from |

Before adding a name, search `ffx.sym` for the address. Lines whose comment
starts with `fh` come from Fahrenheit and are rewritten by ffx-rust's import
script: add your note after them or in a separate comment, and keep
Fahrenheit's name when it has one.

## Every pull request includes

- **The model that did the research**, by the exact name and ID it runs as,
  whatever the vendor or agent tool, for example "Claude Opus 5.5
  (`claude-opus-5-5`)". Don't guess an ID: if you don't know yours, ask the
  user. If several models worked on it, name each and what it found. Put it in the PR description and in the commit
  message.
- **The evidence for each finding**:
  - the game build (SHA-256 of `FFX.exe`);
  - how it was found: the disassembly or decompiled code it rests on (function
    and instruction addresses, what the instructions do, in your own words),
    callers, data read back from memory, or a format check across files;
  - how it was confirmed: an in-game test hook and what it showed, a
    round-trip, or "static only, not run in the game";
  - how certain it is. Mark guesses as guesses (`guess:` in `ffx.sym`).
- **What the finding was for**: the mod or question that led to it.

Never include game files, extracted data, executables or long copied
disassembly: ffx-rust keeps those out of git. Short instruction excerpts to
make a point are fine.

## How

1. Collect the findings while researching (the record in
   [SKILL.md](../SKILL.md#record) has most of it).
2. Tell the user what you would submit, and open the pull request once they
   agree: it is public and goes out under their GitHub account.
3. Fork or branch ffx-rust, add the lines and doc changes, and open one pull
   request per research topic against `main`. Never push to `main` directly.
4. Give the user the pull request link.

Example description:

```text
Findings from building <mod> (<what it needed>).
Research: <model name> (<model ID>).
Build: FFX.exe sha256 0537b2a1…

- symbols/ffx.sym 0x0065a620 PhyreScene_doDeleteMeshInstances: thiscall(scene),
  no stack arguments (plain ret, ECX read first). Evidence: the three callers set
  only ECX; test hook in game ran on each map change with the scene pointer.
- docs/formats/render.md: ...
```
