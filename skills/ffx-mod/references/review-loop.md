# Reviewing your own mod in a loop

An agent that reviews code it just wrote tends to find it fine. A fresh
subagent has not seen your reasoning, so it reads the code as it is. Each
round therefore uses a **new** subagent, never one that saw an earlier round
or your conversation.

## When

After any change to a mod's code or project files, before telling the user
the work is done. A change to a comment or README alone does not need it.

## One round

1. Build the mod (`dotnet build -c Debug`) and fix build errors first; a
   reviewer's time is wasted on code that does not compile.
2. Start a new subagent with the prompt below.
3. Read its report. For each "must fix" and "should fix" finding:
   - fix it, or
   - decline it, with a reason backed by a source (a Fahrenheit source file,
     a wiki page, a confirmed disassembly). "I prefer it this way" is not a
     reason.
4. Rebuild and re-run whatever checks you ran before (tests, the game).
5. "Consider" items are optional. Apply the ones that remove code.

## Reviewer prompt

Give the subagent the facts it needs and nothing that tells it what to
conclude:

```text
Review the Fahrenheit mod at <path> using the ffx-mod-review skill
(skills/ffx-mod-review/SKILL.md and its checklist). Scope: <whole mod |
these files: …>. Fahrenheit SDK version: <version>. Target game(s): <FFX, X-2,
Last Mission: list each one>.

<Round 2 and later:>
Findings the author declined last round, with reasons:
- <finding>: <reason and source>

Do not change any files. Report findings in the skill's format and end with
the verdict line.
```

Do not pass your own summary of the mod, the earlier reviews or your fixes
beyond the declined findings. The reviewer should read the code.

## When to stop

- **Done:** the round reports no new "must fix" or "should fix" findings and
  ends with `Verdict: approve`. Tell the user how many rounds it took and
  list any open "consider" items and things the reviewer could not check.
- **Stop and ask the user:**
  - after five rounds without approval;
  - when the same finding comes back after you declined it twice;
  - when a fix needs a decision only the user can make (changing the mod ID,
    dropping a feature, a signature nobody can confirm).

  Show the open findings, what you tried, and your recommendation.

## Without subagents

If your environment cannot start subagents, review the mod yourself with the
`ffx-mod-review` checklist in a separate pass after the code is finished,
reading the files again rather than relying on memory. Tell the user that
the review was not independent.
