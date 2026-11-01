# The workflow

How a change goes from request to done with three agents and one writer at a time.

## Roles

| Role | Who | Model | Writes |
|---|---|---|---|
| Architect and decision-maker | the developer | — | decisions, approvals |
| devArchitect | `agent/dev-architect.md` | Opus, max effort | the plan file, acceptance tests (never app code) |
| Builder | the main Claude Code session in the project | Opus, high effort | application code; commits |
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
1. **Plan.** In the project's session: *"Use the dev-architect agent. Plan: `<what you want>`."* It writes the plan file and comes back with decisions.
2. **Decide.** Answer each decision in a line. This is where the expensive bugs are prevented: every unanswered question becomes a default the code invents.
3. **Tests.** *"Use the dev-architect agent. Tests. My answers: 1 = `<…>`, 2 = `<…>`."* It records your answers, writes acceptance tests that fail now, and gives the builder a handoff block.
4. **Build.** Paste the handoff block into the main session. The builder makes the acceptance tests pass without changing them, runs the project's gates, and commits.
5. **Review.** *"Use the instinct-reviewer: review since `<commit>`."* It checks the change against the instincts and the plan's scope, and checks that the acceptance tests are unchanged.
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

## Line for each project's `CLAUDE.md`

> Before building a feature or a fix that touches money, saved data, permissions, migrations or more than one screen, run the dev-architect agent and build to its plan. Never edit acceptance test files without my written OK. Before reporting a pass done, run the instinct-reviewer in review mode on everything since the last review, and include its report.
