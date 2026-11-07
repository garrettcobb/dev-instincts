# Sync: where everything lives, and how copies stay true

Every file has one source. Anything else is a copy, made by a script and checked by a script, never by hand.

## The map

| What | Source (edit here) | Copies | How a copy is made | How it's checked |
|---|---|---|---|---|
| Agent definitions | `agent/*.md` in this repo | `~/.claude/agents/` | `agent/sync-agents.ps1` | the script hashes each copy; every agent runs `tools/sync-check.sh` first and refuses to work if its copy differs |
| Where Dev Instincts is | the user environment variable `DEV_INSTINCTS_HOME` | none: agents read the variable | set once (`agent/INSTALL.md`) | `sync-check.sh` stops if it's unset or wrong; `sync-agents.ps1` flags memory naming any other folder |
| Where the control folder is | the user environment variable `DEV_CONTROL_HOME` | none: `testing/CONTROL.md`'s commands read the variable | set once (`testing/CONTROL.md` §6, the way `agent/INSTALL.md` sets `DEV_INSTINCTS_HOME`) | arm B's three windows in `testing/CONTROL.md` §7 and the judge's three in §10 each open with a guard that stops the window where it isn't set, since there every path would start at the drive's root (§6); `tests/test_sync_map.py`, in `sh tools/check.sh`, fails if a guard is gone. The export gate in `sh tools/check.sh` fails on any drive path left in a tracked file |
| Instincts, ledger, reviews, plans | this repo | the public repo | the export script (kept outside this repo; it names what it hides) | the export's scan fails on any private string; a stale exception also fails |
| The commit each export took | the tag `export/<date>` in this repo, on that commit | the mirror's bundle (`--all`) | `git tag export/<date> <commit>` at each export (`WORKFLOW.md`, *Mirror, tag, export*, 4); the next mirror run carries it | *After every round*, 5: `git tag -l 'round/*' 'export/*'` lists it; `tests/test_sync_map.py`, in `sh tools/check.sh`, fails unless the latest *Public repo* line in `metrics/FILED.md` names the latest export tag; `tests/test_mirror.py` shows the bundle holds every tag on its commit |
| The public repo's lag | the latest `export/<date>` tag and this repo's history | the dated *Public repo* line in `metrics/FILED.md` | counted when the line is written, with `git rev-list --count <tag>..HEAD` plus one for the commit that writes it (*Mirror, tag, export*, 4) | `tests/test_sync_map.py`, in `sh tools/check.sh`, fails unless the latest line names the latest `export/<date>` tag, or, while there is none, says it is counted by date; anyone can count it again from the tag |
| STATS.md | `tools/stats.py` from the ledger | none | the reviewer runs it after every ledger change | it's generated; never edited by hand |
| This repo and the work folder, with their whole histories | the two repos | one bundle each, `<folder name>.bundle`, in `~/dev/mirrors` | `sh tools/mirror.sh` after every commit batch (*Mirror, tag, export*, 1): the new bundle is written under a temporary name and renamed over the old one only once it verifies | `git bundle verify`, and the bundle's HEAD against the repo's, before the rename; the run prints both HEADs |
| Each round's closing commit | the tag `round/<round-name>` in this repo | the mirror's bundle (`--all`) | `git tag round/<round-name>` at the round's close (*Mirror, tag, export*, 2); the next mirror run carries it | *After every round*, 5: `git tag -l 'round/*' 'export/*'` lists it, read by eye; `tests/test_mirror.py` shows the bundle holds every tag on its commit |
| The project's code | the project repo | the project's backup mirror | the project's mirror script, at the close of a round | the close compares the mirror's HEAD with the repo's |
| The round's plan and decisions | `reviews/<project>/<round>-plan.md` | none | written by the architect under the lock | the builder checks each acceptance file's SHA-256 against the plan |

## Rules

1. **Edit only the source.** A change to an installed agent file is lost at the next sync, and until then the agent refuses to run.
2. **After any change to `agent/`, run `sync-agents.ps1` and restart Claude Code.** A running session keeps the agent files it started with.
3. **One writer at a time in each repo.** In this repo, whoever holds `.instinct-lock/`. In a project repo, only the builder.
4. **Memory is never the source of a path.** If an agent's memory and `DEV_INSTINCTS_HOME` disagree, the variable wins and the agent fixes its memory.
5. **Calibration is the one allowed difference:** a calibration run installs the blind senior-coder copy on purpose, and `sync-check.sh` lets that through. Re-run `sync-agents.ps1` right after.

## Before every round (two minutes)

```
powershell -ExecutionPolicy Bypass -File "$env:DEV_INSTINCTS_HOME\agent\sync-agents.ps1"
```

It must end with "In sync". Then restart Claude Code, and confirm `/agents` lists instinct-reviewer, dev-architect and senior-coder.

## After every round

1. The reviewer's verify round is committed and the lock is released.
2. `tools/stats.py` has run (the Targets section in `ledger/STATS.md` shows this round's escape rate).
3. `metrics/CONVERGENCE.md` has the round's row.
4. Tag the round's closing commit `round/<round-name>`; export to the public repo, read the change list, push; tag the exported commit `export/<date>`; and write the dated *Public repo* line in `metrics/FILED.md`, naming that tag (`WORKFLOW.md`, *Mirror, tag, export*, 2 to 4).
5. `git tag -l 'round/*' 'export/*'` lists both new tags; `sh tools/check.sh` passes, its FILED test reading the line against the latest export tag; and `sh tools/mirror.sh` carries both tags into the bundle.
