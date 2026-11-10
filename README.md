# ffx-mod-skills

Instructions for AI coding agents (Claude Code, Codex, Cursor and others) that
help people make mods for the **Final Fantasy X/X-2 HD Remaster** on PC:
Final Fantasy X, X-2 and X-2 Last Mission.

They make agents build mods on [Fahrenheit](https://github.com/fahrenheit-crew/fahrenheit),
the mod framework for these games, instead of writing new loaders, ASI plugins
or DLL proxies. Mods built this way work together, install and uninstall
cleanly, and never touch the game folder.

This project is **unofficial** and not affiliated with the Fahrenheit team.
Fahrenheit is in alpha; when these instructions and the
[Fahrenheit wiki](https://github.com/fahrenheit-crew/fahrenheit/wiki) disagree,
the wiki is right. Please do not ask the Fahrenheit team for support with this
repository.

## What's inside

One plugin, `ffx-mod-skills`, with these skills:

| Skill | Use it to |
|---|---|
| `ffx-mod` | make, fix, package or convert a mod |
| `ffx-mod-review` | review a mod, a pull request or a diff before release |
| `ffx-find-game-function` | find a game function and confirm its signature before hooking it |

```text
skills/ffx-mod/
  SKILL.md                    when to use Fahrenheit, rules, workflow
  references/builtins.md      what Fahrenheit already provides, so mods don't rebuild it
  references/versions.md      Fahrenheit versions and the game builds they support
  references/structure.md     mod ID, project file, manifest, folders, file mods
  references/calls.md         calling and hooking game functions
  references/runtime.md       modules, startup order, state, settings, localization
  references/converting.md    moving ASI, proxy-DLL and EFL mods to Fahrenheit
  references/troubleshooting.md
  references/review-loop.md     reviewing your own mod with fresh subagents until approved
skills/ffx-mod-review/
  SKILL.md                    how to review and report
  references/checklist.md     what to check, section by section
skills/ffx-find-game-function/
  SKILL.md                    from "which function does X" to a confirmed hook
  references/sources.md       Fahrenheit, ffx-rust, disassemblers, finding it yourself
  references/signatures.md    reading the calling convention and arguments
  references/sharing.md       submitting findings to ffx-rust as pull requests
```

## Install

**Claude Code**, as a plugin:

```text
/plugin marketplace add yutamago/ffx-mod-skills
/plugin install ffx-mod-skills@ffx-mod-skills
```

or copy the folders under `skills/` into `~/.claude/skills/` (all projects)
or `.claude/skills/` (one project). Copy all of them: the skills link to each
other's references.

**Other agents:** copy the `skills` folder into your mod project and point
your agent's instruction file (`AGENTS.md`, `.cursorrules`, …) at
`skills/ffx-mod/SKILL.md`, and at the other skills for reviews and
reverse engineering.

## Contributing

Corrections are welcome. Every statement should be checkable against the
Fahrenheit wiki or source, or for game internals against another public
source (ffx-rust, Atel#, FFXDataParser); link the page it comes from, and
write it in your own words.

Do not use this repository to contact or file anything with the Fahrenheit
team. Questions about Fahrenheit belong in their Discord,
[Cid's Salvage Ship](https://discord.gg/AGx2grw9nD).

## License

MIT. Fahrenheit itself is LGPL-3.0-or-later and is not included here.
