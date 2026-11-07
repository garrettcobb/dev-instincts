# Principles

Garrett's decisions of 2026-11-02, in Garrett's words.

## 1. The markers
A result counts only when someone else can rerun it and get the same answer. That means:
- pre-registered measures;
- a control;
- blinding;
- negative results published;
- prompts and shas frozen, so a round can be rerun on a new model.

Rounds that lost are reported like rounds that won.

## 2. The test for every addition
A rule, check or step is added only if it comes from a logged failure or enables a measure, with its cost written beside it. Rigor that doesn't change what the data can say is not added.

**The record:** the 2026-11-01 PrivateApp round had five stop rules and no cost rule.
- The five stops are numbered in the round's batch 2 handoff, `reviews/PrivateApp/2026-11-01-0d6183f-plan.md` §9: the module's first regression; a second regression from one rule; regressions over 10% of fixes; the scope cap; a 3 hour time box.
- Garrett stopped entry 250's build on cost, 12 minutes in (`metrics/CONVERGENCE.md`, *2026-11-01 round*). `LESSONS-LEARNED.md` (*2026-11-02: the 2026-11-01 round, closed on paper*): "Cost had no rule. The round had stops for regressions, scope and build time, but none for spend, and spend is what ended it."

## 3. The record and the protocol
- **The record** is append-only: every rule ever written, with its origin, its rounds and its measured effect. It is never edited or shortened.
- **The protocol in force** is versioned. Each version is dated, with the record entries that put a rule in or took it out.
- A rule measured at no effect leaves the protocol and stays in the record.

## 4. The road, in order
1. The pre-registered multi-repo result, with a control.
2. One outside replication, on a repo Garrett didn't pick.
3. A cadence of one repo a month under the same protocol, with a public, dated scoreboard.
4. Reruns of frozen rounds against new models.
