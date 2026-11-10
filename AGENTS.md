# Agent instructions

This repository holds instructions for AI coding agents that help people make
mods for the Final Fantasy X/X-2 HD Remaster with the Fahrenheit mod
framework. It is one plugin with several skills under `skills/`.

If you are helping someone make or fix such a mod, read
`skills/ffx-mod/SKILL.md` and the files it links, and follow them.
To review a mod, use `skills/ffx-mod-review/`; to find or confirm a game
function, use `skills/ffx-find-game-function/`.

When editing this repository:

- Keep every fact checkable against a public source, and link the page it
  comes from: the Fahrenheit wiki or source first; for game internals also
  [ffx-rust](https://github.com/yutamago/ffx-rust),
  [Atel#](https://github.com/yutamago/ffx-atel-sharp) or
  [FFXDataParser](https://github.com/Karifean/FFXDataParser). Say when a fact
  comes from a project that is not Fahrenheit, since the Fahrenheit team does
  not support those. Write in your own words; do not copy Fahrenheit's wiki or
  code.
- Keep each `SKILL.md` short; put detail in its `references/`.
- A skill may link to another skill's references with a relative path
  (`../ffx-mod/references/...`); all skills ship together.
- Never open issues or pull requests on `fahrenheit-crew` repositories.
