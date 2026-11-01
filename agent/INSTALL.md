# Installing the instinct reviewer

The reviewer is a Claude Code custom agent (a "subagent"). It runs in its own context, separate from the agent writing the code, so it isn't anchored on the author's reasoning.

## 1. Put the Dev Instincts repo somewhere permanent
Clone it somewhere the agent can write to, for example `<path-to>\dev-instincts`. Keep any copyrighted originals behind `knowledge/` outside the repo. It's a git repo. Every review commits its findings there, so it needs to be writable, and reachable when the reviewer runs.

If Git says the folder has "dubious ownership" (common on network drives), run the `git config --global --add safe.directory …` command it prints, once.

## 2. Install the agents for every project
Copy `agent\instinct-reviewer.md` and `agent\dev-architect.md` to `C:\Users\<you>\.claude\agents\`. This is the user-level folder, so the agents are available in all projects. Re-copy them whenever they change in the repo:

```
Copy-Item "<path-to>\dev-instincts\agent\instinct-reviewer.md","<path-to>\dev-instincts\agent\dev-architect.md" "$env:USERPROFILE\.claude\agents\"
```

How the two agents and the coding session work together is in `WORKFLOW.md`.

`agent\senior-coder.md` is not installed yet. It stays out of `.claude\agents\` until it passes its calibration replay (see the file).

Check that it loaded: in Claude Code, run `/agents`. `instinct-reviewer` should be listed.

The agent's `memory: user` setting gives it a notes folder at `C:\Users\<you>\.claude\agent-memory\instinct-reviewer\`. Auto memory has to be on in Claude Code for that to work.

## 3. First run
In Claude Code, in the PrivateApp folder:

```
Use the instinct-reviewer agent. Dev Instincts is at <path-to>\dev-instincts — save
that in your memory. Mode: verify. Re-check every PrivateApp finding marked fixed-claimed,
fixed-with-problem or partly-fixed against the current code, and fill in the detail for
PA-S-N01, S-N03, S-N04 and S-N06 from PrivateApp's rtirr-log.
```

That turns the 45 fixed-but-unverified findings into verified ones, or shows they aren't fixed.

## 4. Everyday use

| You want | Say |
|---|---|
| Plan a change before any code | "Use the dev-architect agent. Plan: `<what you want>`." |
| Turn your answers into acceptance tests | "Use the dev-architect agent. Tests. My answers: 1 = `<…>`, 2 = `<…>`." |
| Check a pass or feature before calling it done | "Use the instinct-reviewer: review since `<commit>`." |
| Re-check what's claimed fixed | "Use the instinct-reviewer: verify." |
| You found a bug by hand | "Use the instinct-reviewer: learn. I found: `<what you saw, where, steps>`." |
| A full test-battery run before a release | "Use the instinct-reviewer: audit." |
| Grow the database from an open-source repo | In a Claude Code session opened in the Dev Instincts folder: "Use the instinct-reviewer: mine django/django." |

Its report ends with a paste-ready block for the coding agent. Every report is also saved in Dev Instincts under `reviews/<project>/`, with its proofs.

**For mine mode, set up the GitHub CLI once:** install it, then run `gh auth login`. Without it the reviewer can still mine release notes and history, but it can't read what reviewers asked for on pull requests, which is the most valuable part. One repo per session; each run takes a while.

## 5. Make it part of done (optional, recommended)
Add one line to each project's `CLAUDE.md`:

> Before building a feature or a fix that touches money, saved data, permissions, migrations or more than one screen, run the dev-architect agent and build to its plan. Never edit acceptance test files without my written OK. Before reporting a pass done, run the instinct-reviewer in review mode on everything since the last review, and include its report.

The coding agent then calls both agents itself. The reviewer still can't change project code, so it stays independent.

## The first run already happened
A smoke test on the private app found 7 real problems, including a regression in the activity dates. It also showed 15 ways the instructions were unclear, and all 15 are fixed in this version. Its memory notes for PrivateApp are reflected in `testing/PROBE-RECIPES.md`.

## Updating the instincts
- The reviewer proposes new instincts in `proposals/`. You approve one by asking for it to be added to the end of `DEV-INSTINCTS.md`, never renumbering.
- When you approve a draft, its findings move with it: the ledger lines tagged with its `proposed:<slug>` get the new number in `instincts`, and the tag is dropped. Ask the reviewer (or any agent) to do that in the same commit.
- `STATS.md` has a table of how many findings each draft has collected. Use it to decide: a draft that keeps catching things has earned its number.
- After any change to the ledger, run `python tools/stats.py`.

## Adding to the knowledge base
Drop new articles or papers in `a local folder of originals` and ask for them to be added. `knowledge/README.md` says how: one note per source, rated for evidence, and the synthesis updated only if the source is measured or changes a conclusion.

## Later (not built yet)
- **A hook that enforces report-only:** a `PreToolUse` hook that blocks the agent's Write and Edit outside `.instinct-scratch/` and the Dev Instincts repo. For now the rule is in its instructions.
