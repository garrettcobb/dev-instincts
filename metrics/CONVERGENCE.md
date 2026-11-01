# Convergence tracking

The question: does refining after a result iron out the bugs, or do they become uncontrollable?

## Data so far

| Round | Battery depth | New defects (functional) | Not fully fixed from before | Regressions from fixes | Severity mix |
|---|---|---|---|---|---|
| 1.0.0 review | review + repro scripts | ~91 (42 + server 25 + front 24) | n/a | n/a | crashes, stuck Recycle Bin/Undo, white screens, lost prices |
| Pass 1 verify | **deeper**: + 40k fuzz, forced-failure atomicity, races, perf, full browser walk, offline namespace | 32 (server 16, front 16) | 22 server/front (11 + 9 "fixed with a problem", 5 + 6 partly), 1 not fixed | at least 3 traced (FV-01, S-V01, NF-01) | edge cases: double-submit, races, stale/partial forms, plus 4 data loss |
| Pass 1 fidelity | re-measured | 16 cosmetic or confusing | 14 of 64 gaps | at least 1 (NF-01) | cosmetic |
| Pass 1 offline | first isolation run | 9 (OFF-01..09) | 2 (S-22, S-23 with problems) | 0 | 1 real outbound attempt |
| Pass 2 (in progress, Oct 30) | coding agent's own workflow mapping; the end-of-pass battery not run yet | 6 found while mapping (S-N01..06), all fixed | section 2 crashes/stops all fixed; data loss and atomicity fixed by class (one transaction per request; 46-route forced-failure test, checked by turning the fix off) | not measured yet | n/a until the battery re-runs |

**Caveat:** the pass-1 battery was deeper than round 1, so the drop can't be called convergence yet. From pass 2 on, keep the battery fixed.

## 2026-10-31 fix round (plan 59ae532): uncontrolled, then closed

Not a pass with a fixed battery, so it is not a point in the trend above. It is recorded as its own case. Every finding from the uncontrolled stretch carries the tag `uncontrolled-round` in the ledger, so the stats can split it out.

| Stretch | What ran | Log entries | Findings | Regressions from fixes | Escaped an earlier review | Data loss |
|---|---|---|---|---|---|---|
| Uncontrolled: 2ce008c to 6166f51, 14 per-commit reviews | Architect planned 12 entries, then dropped out. The builder wrote its own fixes and tests and asked the developer design questions directly. | 34 (RTIRR-210 to 243) | 44 | 15 (44% of entries) | 13 | 7 |
| Closed: 3157477 and 844e811, then the verify round | Architect back in the loop; builder built to the reviewer's tests only | 3 (RTIRR-244 to 246) | 4 (1 crash, 3 process) | 0 | 0 | 0 |

**Read:** by the decision rule above (regressions under about 10% of fixes), the uncontrolled stretch did not converge. Two clusters drove it:
- **Version-restore Undo:** the rule went through four versions (RTIRR-210 to 215), each one decided on an assumption about the data that the code could have answered first.
- **scripts/mirror.sh:** an unplanned backup script that took 17 findings, 3 of them data loss.

The lock group is the counter-example inside the same day. Its rule was decided before the code and built to it, and 6166f51 closed five findings at once with no regression.

**Limits of today's data:**
- Reviews before 6166f51 quoted pass counts, not coverage (`instinct-tests.sh` runs no coverage). Their verified fixes stand, because each was proven by its own test or probe, but "the suite is green" was only partly checked. PA-IR-069 and 070 sat unseen from 59a26f7 to 3157477.
- One reviewer caught 68 of the 70 PA-IR findings. Nothing checked the checker.
- Of the plan's 12 entries, the lock group finished; rows 9 to 16 moved to the next round (plan section 13).

## What to record each pass
- Battery version (and what changed, if anything).
- New defects by severity: crash / data loss / wrong result / security / stuck / cosmetic.
- Regressions caused by the previous pass's fixes.
- Claimed fixed but not.
- Recurring root-cause classes, i.e. the same class showing up in a new place.
- Features added during the pass (should be zero while stabilizing).

## Decision rule
- **Converging:** functional defects roughly halve each pass, regressions stay under ~10% of fixes, severity keeps falling, and no recurring class survives a "fixed by class" pass. Keep refining.
- **Not converging:** counts go flat, regressions climb, or the same classes keep reappearing after class-level fixes. Stop patching. Restructure, or rebuild from the baseline with the shared guards in from the start.

## Pass 2 notes so far
- Fixed by class: one transaction per request, one-time submit tokens plus status checks, prices change only where sent, stale saves refused.
- Watch: test totals changed after the AFP amount rule (each needs a reason); files on disk aren't covered by the transaction; D16 (new feature) is in the pass.

## Read after pass 1
Converging, conditionally. The decisive test is pass 2: fix by class, freeze features, run the same battery.
