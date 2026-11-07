# The workflow

How a change goes from request to done with four agents and one writer at a time. Before any of it, the agents must be in sync (`SYNC.md`).

## Roles

| Role | Who | Model | Writes |
|---|---|---|---|
| Architect and decision-maker | the developer | — | decisions, approvals |
| devArchitect | `agent/dev-architect.md` | Opus, max effort | the plan file, acceptance tests (never app code) |
| Builder | the main Claude Code session in the project | Opus, high effort | application code; commits |
| senior-coder | `agent/senior-coder.md` | Opus, max effort | one design note per rule change, beside the plan; never code, tests or the ledger |
| instinct-reviewer | `agent/instinct-reviewer.md` | inherits the session's model | nothing in the project; findings in Dev Instincts |
| Search helper (optional) | Claude Code's built-in Explore agent | a smaller model | nothing |

**Why it isn't a manager, a lead and a junior.**
- Writing code isn't the bottleneck; checking it is. More writers means more to check.
- Every handoff down a chain loses detail.
- The main session already coordinates.

The split that pays is by **independence**:
- the tests are written by someone who hasn't seen the code;
- the review is done by someone who didn't write it.

## The sequence
0. **Design note (any change to a rule).** *"Use the senior-coder agent: design note for `<rule or finding>`."* It reads the code and data model and writes where each candidate rule breaks. The architect doesn't offer options until the note exists.
1. **Plan.** In the project's session: *"Use the dev-architect agent. Plan: `<what you want>`."* It writes the plan file and comes back with decisions.
2. **Decide.** Answer each decision in a line. This is where the expensive bugs are prevented: every unanswered question becomes a default the code invents.
3. **Tests.** *"Use the dev-architect agent. Tests. My answers: 1 = `<…>`, 2 = `<…>`."* It records your answers, writes acceptance tests that fail now, and gives the builder a handoff block.
4. **Build.** Paste the handoff block into the main session. The builder makes the acceptance tests pass without changing them, runs the project's gates, and commits.
5. **Review.** *"Use the instinct-reviewer: review since `<commit>`."* It checks the change against the instincts and the plan's scope, checks that the acceptance tests are unchanged, quotes the pass count and the coverage total line, and scores the senior coder's note on every finding that touches its rule.
6. **Fix.** Paste the reviewer's block into the builder. Re-run step 5 on the fix commits until it's clean or you've decided on what's left.
7. **When you find a bug yourself:** *"Use the instinct-reviewer: learn. I found: `<…>`."*

**Skip steps by size, not mood:**
- **A typo, a label, a one-line obvious fix:** build, then review.
- **Anything that touches money, saved data, permissions, migrations or more than one screen:** all steps.
- **Max effort is slow and costly,** so don't spend it on what a sentence settles.

## One writer at a time
Two agents writing the same repo at once can overwrite each other's work, and either one's commit can sweep up the other's half-done changes.
- **In a project:** the devArchitect writes only in steps 1–3, the builder only in steps 4 and 6. Never run them at the same time.
- **In Dev Instincts:** only one instinct-reviewer run at a time, in any mode. The reviewer enforces this with a lock folder, `.instinct-lock/`. A second run that finds the lock stops and says which run holds it. If a run crashed and left the lock behind, delete the folder by hand after checking nothing is running.
- **Mining** runs in its own session opened in the Dev Instincts folder, never alongside a review or verify.

## Tests and new rules (Garrett, 2026-11-03)
Every test is red before its fix and green after, with hand-worked expected values, and every new rule carries its cost beside it. Red means the test is run before its fix and fails; green, that it passes once the fix is in. Its expected values are worked out by hand and written beside it, never taken from the output of the code under test. A rule's cost goes beside the rule, as `PRINCIPLES.md` §2 asks. *Cost:* each new test run twice, before its fix and after; its expected values worked out by hand; and a cost line for each new rule.

## Mirror, tag, export (Garrett, 2026-11-03)
1. **Mirror after every commit batch:** `sh tools/mirror.sh`. It keeps a git bundle of this repo and one of the private work folder in the mirrors folder (`~/dev/mirrors`), under one fixed name each, `<folder name>.bundle`. Each run writes the new bundle under a temporary name, checks it with `git bundle verify` and its HEAD against the repo's, and only then renames it over the old one, so the old one is never removed before the new one verifies. It prints each bundle's HEAD beside its repo's HEAD. While either repo has anything not committed, it stops and writes nothing. *Cost:* one run a batch, and disk for one bundle per repo, about the size of its history (164 MiB for the work folder and 1.6 MiB for this repo on 2026-11-03), with room for a second of each while a run writes its new one.
2. **Tag each round at its close:** `git tag round/<round-name>` in this repo, on the commit that closes the round. *Cost:* one command a round.
3. **Export to the public repo after every round close** (the export script, `SYNC.md`). The public repo's lag is a dated line in `metrics/FILED.md`. *Cost:* an export run and a read of its change list each round, and one line.
4. **Tag every export:** each export to the public repo tags the commit it exported `export/<date>` in this repo (`git tag export/<date> <commit>`), and the lag line in `metrics/FILED.md` counts from the latest export tag. The 2026-10-31 export recorded no commit, so its lag can only be counted by date. The architect's (2026-11-03; Garrett may change them): the count is the commits after the tag, the one that writes the line included, as the 3fb715a line counted; a second export on one day is tagged `export/<date>-2`. *Cost:* one command an export, and one count for each lag line: `git rev-list --count <tag>..HEAD`, plus one for the commit that writes the line.

## Line for each project's `CLAUDE.md`

> Before building a feature or a fix that touches money, saved data, permissions, migrations or more than one screen, run the dev-architect agent and build to its plan. Never edit acceptance test files without my written OK. Before reporting a pass done, run the instinct-reviewer in review mode on everything since the last review, and include its report.
