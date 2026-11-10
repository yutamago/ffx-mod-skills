---
name: ffx-mod-review
description: Review a Fahrenheit mod for Final Fantasy X, X-2 or X-2 Last Mission (Final Fantasy X/X-2 HD Remaster, Steam/PC), its code, a pull request or a diff, before release or when someone asks "is this mod done right". Checks that it uses what Fahrenheit provides instead of rebuilding it, hooks and calls game functions safely, declares and supports the right games (FFX.exe vs FFX-2.exe), leaves the game folder and saves alone, and works next to other mods. Use for "review my FFX mod" or "review my X-2 mod", "check this Fahrenheit module", "what's wrong with this hook", or any review of C# code that derives from FhModule.
---

# Reviewing a Fahrenheit mod

This skill reviews mods built on
[Fahrenheit](https://github.com/fahrenheit-crew/fahrenheit). The rules it
checks are in the `ffx-mod` skill
([`ffx-mod/SKILL.md`](../ffx-mod/SKILL.md)); this skill turns
them into a list to go through. When this skill and the Fahrenheit wiki or the
source of the SDK version in use disagree, the wiki and source win.

## Steps

1. **Find the scope.** A whole mod, a pull request or a diff. For a diff,
   still read the module classes and the `.csproj` it touches, because most
   findings depend on context.
2. **Find the Fahrenheit version** in `<Project Sdk="Fahrenheit.Sdk/…">`. Read
   the Fahrenheit source at that tag when a finding depends on an API.
3. **Read the mod**: `.csproj`, every class deriving from `FhModule`, every
   `FhCallHandle` and hook, anything shared between modules or mods, the
   `efl` folder, and any install or packaging script.
4. **Go through [references/checklist.md](references/checklist.md)** section
   by section. Start with section 1 (rebuilding what Fahrenheit has): it is
   the most common problem in mods written with AI help, and fixing it often
   removes code that other findings were about.
5. **Build it** if you can (`dotnet build -c Debug`). Report build warnings
   that point at a checklist item.
6. **Report** (format below). Do not change code unless the user asks.

## Judging findings

- Report what you can point to: a file, a line, the rule, and the Fahrenheit
  source or wiki page that shows the rule. If you could not confirm something
  (a signature, an address, whether a hook chains at runtime), say "unconfirmed"
  and say what would confirm it.
- Do not report style preferences as problems. Fahrenheit's own code uses
  `snake_case` methods and `_underscore` fields; a mod may follow it or not.
- Removing code is a fine fix. Prefer "delete this wrapper and use `_logger`"
  over "improve this wrapper".
- A signature you cannot confirm is a finding, not a pass. Use the
  `ffx-find-game-function` skill to check it if the user wants.

## Report format

Group findings by severity, most severe first:

- **Must fix**: crashes, corrupts saves or game files, breaks other mods,
  or breaks a Fahrenheit rule players depend on (load order, IDs, the game
  folder).
- **Should fix**: rebuilds a Fahrenheit feature, fragile across game builds
  or SDK versions, misleading to players.
- **Consider**: smaller simplifications.

For each: `path:line`, one sentence on what is wrong, what happens because of
it, the fix, and the source link. End with what you did not check (for
example "did not run the game", "signatures of `h_foo` not confirmed").

Finish with one verdict line:

- `Verdict: approve`: no "must fix" or "should fix" findings remain. Open
  "consider" items and unchecked things may remain; list them.
- `Verdict: changes needed`: at least one "must fix" or "should fix".

If you were given findings the author declined, with reasons, judge each
reason. Accept it if it holds up against the source and do not report the
finding again; if it does not, report the finding again and say why the
reason does not hold. Mark findings that were not in the previous round as
new.

## Fahrenheit's own repositories

Never open issues or pull requests on `fahrenheit-crew` repositories, and do
not post review results there. If a finding is really a gap in Fahrenheit,
tell the user they can raise it on the Discord, Cid's Salvage Ship
(https://discord.gg/AGx2grw9nD), in their own words.

## Other skills of this plugin

This skill belongs to the `ffx-mod-skills` plugin, with `ffx-mod` and `ffx-find-game-function`. Links to
their files read `<skill>/<path>` and assume the skills sit side by side. If
such a file is missing, the skill was installed on its own: look for the
other skill where your agent keeps skills (for example `.agents/skills/`,
`.github/skills/`, `.claude/skills/` or the user's home equivalents), or ask
the user to install the whole plugin
(https://github.com/yutamago/ffx-mod-skills).
