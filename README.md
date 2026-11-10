# ffx-mod-skills

Instructions for AI coding agents (Claude Code, Codex, GitHub Copilot,
Google Antigravity and others) that
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
  references/review-loop.md   reviewing your own mod with fresh subagents until approved
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

The skills follow the [Agent Skills](https://agentskills.io) format, and the
repository is a plugin for each tool below. Install the whole plugin: the
skills link to each other's files.

**Claude Code**

```text
/plugin marketplace add yutamago/ffx-mod-skills
/plugin install ffx-mod-skills@ffx-mod-skills
```

**Codex**

```bash
codex plugin marketplace add yutamago/ffx-mod-skills
```

then install `ffx-mod-skills` from `/plugins` and start a new task.

**GitHub Copilot CLI**

```bash
copilot plugin marketplace add yutamago/ffx-mod-skills
copilot plugin install ffx-mod-skills@ffx-mod-skills
```

**Google Antigravity**

```bash
agy plugin install https://github.com/yutamago/ffx-mod-skills
```

or copy the repository into `.agents/plugins/ffx-mod-skills/` (one project)
or `~/.gemini/config/plugins/ffx-mod-skills/` (all projects).

**Any other agent, or without a plugin system:** copy the three folders under
`skills/` into your project's `.agents/skills/` (read by Codex, Copilot and
Antigravity) or `.claude/skills/` (Claude Code). Agents that read only an
instruction file (`AGENTS.md`, `.cursorrules`, …) can be pointed at
`skills/ffx-mod/SKILL.md`.

| File | Read by |
|---|---|
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Claude Code (Copilot CLI and Codex also read the marketplace) |
| `plugin.json` ([Agent Plugins](https://agent-plugins.org) 1.0) | Codex, Copilot CLI |
| `.agents/plugins/marketplace.json` | Codex |
| `.github/plugin/marketplace.json` | Copilot CLI |
| `.antigravity-plugin/plugin.json` | Antigravity |

## Contributing

Corrections are welcome. Every statement should be checkable against the
Fahrenheit wiki or source, or for game internals against another public
source (ffx-rust, Atel#, FFXDataParser); link the page it comes from, and
write it in your own words.

Before a pull request, run `python3 tools/check.py`. It checks that every
manifest has the same name, version and description, that each skill's
frontmatter is valid, and that every link resolves. When releasing, change
the version in all five manifests.

Do not use this repository to contact or file anything with the Fahrenheit
team. Questions about Fahrenheit belong in their Discord,
[Cid's Salvage Ship](https://discord.gg/AGx2grw9nD).

## License

MIT. Fahrenheit itself is LGPL-3.0-or-later and is not included here.
