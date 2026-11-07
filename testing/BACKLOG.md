# Backlog: held for the next block

Improvements to the control's reviewer under test, and measures proposed for a later block, held while a block runs (Garrett's decision, 2026-11-05; `testing/CONTROL.md` §5.2).

**The rule.** Append-only: each entry is dated and is never edited, shortened or removed, and a later word on one, a decision included, is a new dated entry at the end that names the one it concerns. Nothing here is acted on during a block: while `testing/CONTROL.md` §5.2 reads that the block is open (`Block 1: open.` for the first), the reviewer under test, `agent/instinct-reviewer.md` and `DEV-INSTINCTS.md`, doesn't change, and no measure is added (`testing/CONTROL.md` §14). Between blocks, Garrett decides which entries become pre-registered measures or rule changes; a rule so made goes in `RULES.md`, as every rule does. What comes here: an improvement to either frozen file, found during a block, and a measure proposed for a later block (the scope is the architect's reading of Garrett's decision, 2026-11-05; Garrett may change it). Cost: one entry per improvement, minutes to write; an improvement waits for the block's close, however good, and the frozen files serve every project, so it waits there too (the architect's estimate).

## Entries

### 2026-11-05: an instinct-yield measure
- **Status:** a candidate for the next block's pre-registration, not this block's (Garrett, 2026-11-05).
- **What it counts,** in Garrett's words, "bugs found by arm A and missed by every plain run": per repo, the judge's confirmed groups that hold a confirmed arm A claim and no confirmed claim from any arm B run on that repo.
- **How it would be computed:** from the final `verdicts.md` and `key.json` in the repo's control folder: for each confirmed group, the arms of its confirmed claims; the count is the groups whose only arm is A. It is arm A's *unique to the arm* (`testing/CONTROL.md` §12) over the arm's runs together, where `tools/control.py score` prints it for each run on its own (`testing/CONTROL.md` §11.1). Monize's four, groups 2, 3, 16 and 18, are in the round report's §8 table (`reviews/monize/2026-11-02-93f4e68-review.md`), descriptive only.
- **Open, for the pre-registration:** the first repo has two arm B runs and the others one, so "missed by every plain run" means missed by two runs there and by one elsewhere; the pre-registration would fix how the repos compare, and whether the measure is a count, a share of arm A's confirmed groups, or a rate per hour.
- **Why:** H1 and H2 measure a rate and a precision (`testing/CONTROL.md` §1); neither counts the bugs that only the run with the instincts found.
- **Cost if adopted:** none at run time: it is counted from files every round already has, by hand or by one more line of `score` (the architect's estimate).

The definition and the open points are the architect's, 2026-11-05, from Garrett's words; the pre-registration fixes them.

### 2026-11-05: a completeness proxy
- **Status:** a candidate for the next block's pre-registration, not this block's (Garrett, 2026-11-05).
- **What it counts,** in Garrett's words, the "share of the union of arms plus maintainer-confirmed": per repo, each arm's confirmed groups over the union of both arms' confirmed groups and the bugs a maintainer has confirmed.
- **How it would be computed:** the denominator is the judge's confirmed groups, every run of both arms, less any group whose filed issue a maintainer rejects as not a bug (`testing/CONTROL.md` §12), plus each bug a maintainer confirms (`acknowledged` or `fixed`, `testing/FILING.md` §7) that is present at the reviewed sha and that no claim names; the numerator is the arm's confirmed groups, over its runs together.
- **Open, for the pre-registration:** which maintainer-confirmed bugs are looked for (issues others file against code present at the sha, bugs found outside the arms and filed, or both) and until when, since maintainers answer over months and the denominator grows with each answer; and whether it is read per run or per arm.
- **Why:** confirmed per hour rewards speed and refuted per finding precision; neither says what share of the bugs there to find an arm found. It is a proxy: the true count is unknown, and the union is a floor for it.
- **Cost if adopted:** a read-only search of the repo's issues for maintainer-confirmed bugs that no claim names, dated, minutes at each re-check, and a count from the judge's groups (the architect's estimate).

The definition and the open points are the architect's, 2026-11-05, from Garrett's words; the pre-registration fixes them.
