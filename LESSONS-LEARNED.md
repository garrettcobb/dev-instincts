# Lessons learned: the PrivateApp trial

## What the trial was

PrivateApp is an construction-procurement app, built in a week with Claude Code: a Django + PostgreSQL backend, a React/Fluent UI front end that copies Windows File Explorer, and an offline Windows installer. The developer has the baseline code and does the real job himself.

The trial had two purposes:
1. Find out how deep the development process needs to go.
2. Test whether repeated refinement after a result irons out the bugs, or whether they become uncontrollable.

## Timeline

| Date (2026) | What happened |
|---|---|
| Oct 23 | First commit of the PrivateApp line |
| Oct 28 | 1.0.0: the Explorer front end replaces the old pages (657 pytest, 100% coverage) |
| Oct 28 | First review: 42 findings. The developer's own testing adds 2 workflow bugs ($0 prices, AFP dead end) and 1 request (Ctrl/Shift multi-select) |
| Oct 28 | Three independent reviews: server 25, front end 24, Explorer fidelity 64 gaps |
| Oct 28–30 | Pass 1 (Claude Code): 1.0.1 → 1.0.2 (ADR-026) → 1.1.0/1.1.1 (ADR-027) → fix-1.1.2 (ADR-028 new features). 813 pytest at 100%, 328 Vitest |
| Oct 30 | Pass-1 verification: four independent checks (server + atomicity, browser workflow, fidelity, offline isolation) |

Active development time, measured from commit timestamps: about 39 hours over 11 sessions (more counting testing time).

## What worked
- **The process scaffolding:** an ADR per step, an error log (rtirr), a changes register, 100% branch coverage, small commits. Every decision and bug is traceable.
- **Domain testing.** The two worst workflow problems ($0 prices after moving to a contract, the AFP greyed out with no reason) came from doing the real job, not from any test or review.
- **Independent report-only reviewers** with their own copies and their own databases. They found 91 defects that a fully green suite missed, then 57 more after pass 1.
- **Proving instead of reading.** Reproduction scripts, forced-failure tests, fuzzing, races, a real browser, a real network cut.
- **Money math held:** the full workflow matched hand math to the cent after pass 1.
- **Most fixes held:** 38/59 server and 34/53 front-end items verified fixed, and 50/64 fidelity gaps closed.

## What didn't
- **Green ≠ correct.** 813 tests and 100% coverage still shipped a white-screen crash, data loss and double-billing. Coverage proves the code ran, not that it behaves.
- **Instance fixes.** Atomicity, double-submits, bad input and stale data were fixed route by route, and each new route brought them back.
- **Fixes made bugs.** The Ctrl+Z white screen came from a pass-1 fix. A new rule (contracts need a price) had four ways around it.
- **"Claimed fixed" wasn't.** Tab separators never drew, and change-order Print printed blank, both logged as fixed.
- **Features during stabilization.** ADR-028 landed mid-fix and muddied the signal.
- **Direction churn.** The UI was rebuilt four times. Each rebuild reset the bug count.
- **AI reviewing AI.** Without a human who reads the code, the subtle classes (concurrency, idempotency, stale state) slipped through until a targeted battery went looking.
- **The front door went stale.** The README still described an older project name, ADR statuses were wrong, and there were no user or IT guides.

## Answers so far to the trial's two questions

**How deep does the process need to go?** Deeper than unit tests and coverage, in a specific way. The fixed battery in `testing/TEST-BATTERY.md` is the depth that found real bugs:
- full workflow with money assertions;
- fuzz;
- forced-failure atomicity;
- double-submit;
- races;
- stale and partial;
- browser failure paths;
- real size;
- layout at the user's screen;
- offline isolation;
- migrations.

Beyond that, more review depth found mostly cosmetic items.

**Does refinement converge?** Tentatively yes, with conditions. Defects fell from about 91 to about 32 new, plus 22 not fully fixed. Severity moved from crashes and stuck states to edge cases. But regressions from fixes, and the same root-cause classes recurring, are the warning signs. See `metrics/CONVERGENCE.md` for the rule to call it either way after pass 2.

## 2026-10-31: the round that got away

The plan was 12 entries with the architect planning, the builder building and the reviewer checking each commit. After planning, the architect dropped out. The builder wrote its own fixes and tests, asked the developer design questions directly, and kept going. By midday one planned entry was done and 27 unplanned ones had been logged, most of them fixes for bugs the previous fix caused.

What brought it back: putting the architect back between the reviewer and the builder, acceptance tests written from the decided rule before the code, a scope cap, one writer at a time, and a stop when the same rule regresses twice. The close that followed had no regressions.

What it showed:
- The human gate isn't at the end. A gate on how the code is built has to sit before the rule is chosen, which is why the senior coder exists (`agent/senior-coder.md`, uncalibrated).
- A reviewer's "passed" needs the coverage line next to it, or the checks can quietly stop meaning what they say.
- Speed hid the loss of control. Thirty commits in a day looked like progress.

## Carry forward
1. Use the checklist in `DEV-INSTINCTS.md` on every feature, before the first review.
2. Build the shared guards early: one transaction-plus-event path, idempotent actions, input cleaning, stale-save refusal, error boundaries. Back each with a test that every route must pass.
3. Run the fixed battery every pass, and score it.
4. Freeze features while stabilizing.
5. Settle the UI direction with mock-ups before building.
6. Keep doing the real job as testing, and script each session.
7. Learn to read the risky code: money, saving, concurrency, permissions.
