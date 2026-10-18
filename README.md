# ffx-mod-skills

Instructions for AI coding agents (Claude Code, Codex, Cursor and others) that
help people make mods for the **Final Fantasy X/X-2 HD Remaster** on PC.

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

```text
skills/fahrenheit-mod/
  SKILL.md                    the skill: when to use Fahrenheit, rules, workflow
  references/versions.md      Fahrenheit versions and the game builds they support
  references/structure.md     mod ID, project file, manifest, folders, file mods
  references/calls.md         calling and hooking game functions
  references/runtime.md       modules, startup order, state, settings, localization
  references/converting.md    moving ASI, proxy-DLL and EFL mods to Fahrenheit
  references/troubleshooting.md
```

## Install

**Claude Code**, as a plugin:

```text
/plugin marketplace add yutamago/ffx-mod-skills
/plugin install ffx-mod-skills@ffx-mod-skills
```

or copy `skills/fahrenheit-mod` into `~/.claude/skills/` (all projects) or
`.claude/skills/` (one project).

**Other agents:** copy `skills/fahrenheit-mod` into your mod project and point
your agent's instruction file (`AGENTS.md`, `.cursorrules`, …) at
`skills/fahrenheit-mod/SKILL.md`.

## Contributing

Corrections are welcome. Every statement should be checkable against the
Fahrenheit wiki or source; link the page it comes from, and write it in your
own words.

Do not use this repository to contact or file anything with the Fahrenheit
team. Questions about Fahrenheit belong in their Discord,
[Cid's Salvage Ship](https://discord.gg/AGx2grw9nD).

## License

MIT OR Apache-2.0, at your option. Fahrenheit itself is LGPL-3.0-or-later and
is not included here.
