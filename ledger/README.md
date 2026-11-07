# The findings ledger

Every error, bug, glitch and process miss found in any project, one JSON object per line in `findings.jsonl`. Every project in it is registered in `projects.json`.

It's the database the instinct reviewer (`agent/instinct-reviewer.md`) learns from:
- `tools/stats.py` turns it into `STATS.md`;
- STATS.md's check order is the order the agent checks a change in;
- the most costly kinds of miss get looked at first, and the order shifts as findings accumulate.

## Rules
- **Append, don't rewrite.** A new finding is a new line. Changing a finding's status, severity or fields is an in-place edit of that line, and the reason goes in the commit message.
- **IDs are permanent:** `<project code>-<local id>`, e.g. `PA-S-V07`. Project codes are in `projects.json`.
- **Instinct numbers are permanent.** New instincts are added at the end of `DEV-INSTINCTS.md`, never renumbered.
- **Synthetic data only.** No organization names, no real record data, no secrets, no absolute paths from anyone's machine.
- **Run `python3 tools/stats.py` after every change.** It refuses if the ledger cites an instinct that doesn't exist.

## Fields

| Field | Values | Meaning |
|---|---|---|
| `id` | `PA-S-02` | project code + local id |
| `project` | `PrivateApp` | |
| `round` | `1.0.0-review`, `pass1-verify`, `2026-10-31-ccabf0b-review` … | which pass found it; the instinct reviewer uses `<date>-<head sha>-<mode>` |
| `local_id` | `S-02` | the id used in that project's own reports/logs |
| `title` | one line | what's wrong, in plain words |
| `severity` | `data-loss` `security` `wrong-result` `crash` `stuck` `process` `cosmetic` | worst real consequence |
| `area` | `server` `front` `ui` `offline` `process` `docs` | |
| `instincts` | `[6, 28]` | the instincts that should have caught it (DEV-INSTINCTS.md numbers); `[]` = none fits yet, so propose one |
| `tags` | free | e.g. `fidelity`, `money`, `a11y`, `value-high`. `proposed:<slug>` (e.g. `proposed:traces-to-the-ask`, `proposed:idle-is-a-state`; each draft in `proposals/` shows its tag) marks a finding that fits a draft instinct in `proposals/` not yet approved; `STATS.md` counts them. When the draft is approved, put its new number in `instincts` and drop the tag. |
| `where` | `file:line` / route / screen | |
| `smell` | one line, optional | the visible code pattern an experienced reader would notice, e.g. "save() then log() with no atomic block". This is the instinct itself, so fill it in for every new finding. |
| `repro` | short, optional | steps or the test that proves it |
| `caught_by` | `independent-review` `verification` `domain-testing` `coding-agent` `oversight-review` `instinct-reviewer` `senior-coder` `user` `maintainer` `human-review` | who found it (`maintainer` = the project's own team, after merge; `human-review` = a reviewer on a pull request, before merge; `user` = reported after release; `senior-coder` = a break case in the senior coder's design note, re-run by the instinct reviewer) |
| `evidence` | `reproduced` or `reading` | reproduced means a script or test really ran |
| `status` | `open` `fixed-claimed` `fixed-verified` `fixed-with-problem` `partly-fixed` `not-fixed` `decision` `cant-verify` `rejected` | `fixed-claimed` = the author says so; only an independent re-run makes it `fixed-verified`; `rejected` = the developer judged it not a defect (a false positive) |
| `origin` | `new` `regression` `pre-existing` `carry-over` `escaped` `external` | regression = caused by a fix in the reviewed scope; pre-existing = there before the scope, no earlier review covered it; carry-over = known and left unfixed; escaped = in code a review already covered and that review missed it (the reviewer's own miss); external = another project's own escape, imported from its history as calibration data |
| `escaped_from` | round, optional | which earlier review missed it |
| `source` | path | where the full write-up is; the instinct reviewer's are `reviews/<project>/<round>.md` |
| `duplicate_of` | id, optional | |
| `filed` | `<owner>/<repo>#<n>`, optional | the upstream issue the bug was filed as (`testing/FILING.md` §6 and §8, `testing/CONTROL.md` §15), set as the row's last key on every row of the filed group. `status` stays `open`: filing changes nothing about the bug, and only a merged fix makes it `fixed-claimed`. |
| `fixed_in` | `<reference> (<sha>)`, optional | the change that fixed it and its commit: the project's own log entry (`RTIRR-149 (0ef7ee9)`) or, on a filed row, the upstream pull request and its merge commit (`<owner>/<repo>#<pr> (<sha>)`); several joined by commas where more than one change fixed it. Ferrite's imported rows hold the release that shipped the fix (`0.2.5`), or `open` or `unrecorded` |
| `note` | free text, optional | what the other fields can't hold, in sentences: the plan entry or decision that settles the finding; why its severity, origin or `caught_by` is what it is, an escape included; why it isn't a duplicate of a row it names; how it was scored against a design note; and its later fixes, re-checks and verifications, each with its round or commit |
| `authorship` | `ai` `human` `mixed`, optional | who wrote the code. Defaults to the project's authorship in `projects.json`; set it on a finding only when that change's own record says otherwise |
| `design_note` | `{"verdict": "predicted", "note": "reviews/<project>/<round>-design.md"}`, optional | the reviewer's score of the senior coder's design note for the rule this finding broke: `predicted` (a break case in the note matches), `partly` (the mechanism, not the consequence; counts half), `missed`. `tools/stats.py` turns these into the senior coder's severity-weighted hit rate. It scores predictions, not finds (Garrett, 2026-11-01): a finding with `caught_by: senior-coder` came from a note's own break cases and can't be missed, so it isn't scored (counted apart). Score only findings caught by someone else on a rule a note covered; a note's own find that someone later records (e.g. one the plan accepted) stays unscored. |

## Tags with a fixed meaning
`tags` is free (above), but these are set by rule. The control tags come from the judge's groups in a blinded control round (`testing/CONTROL.md` §15), never from a run's own claim list.

| Tag | Meaning |
|---|---|
| `control:A` | found by arm A (the instinct reviewer) only: the judge's group holds a confirmed arm A claim and no confirmed arm B claim. |
| `control:A+B` | found by both arms: the judge confirmed an arm B claim in the same group as arm A's row. The arm A row keeps the bug and arm B's claims add no row (one row per bug, not per claim). |
| `control:B` | found by arm B (the plain session) only: a judge-confirmed group with no arm A claim gets one row, round `<date>-<sha>-control`, source arm B's public report. |

Where arm A's two runs each logged the same bug (Monize groups 7 and 10), both rows stay with their tags and neither is `duplicate_of` the other: the record is append-only, and the tags already say two runs found it.

## Projects
`projects.json` lists every project in the ledger: its code, its kind (web app, desktop app…), its authorship, whether it's one of the developer's own (`own`), and for outside projects the source, license and what was mined. `tools/stats.py` refuses a finding whose project isn't registered.

**What feeds the check order:** the developer's own projects, plus outside projects whose code is AI-written (Ferrite). Human-written and mixed outside projects, mined with `testing/MINING.md`, are reference data. `STATS.md` ranks them separately and shows how much of each the instincts cover, but they never move the check order. What experienced human teams miss isn't the same as what AI-written code gets wrong, and a few large repos would otherwise bury the developer's own record. While the control's five-repo block is open, the rows tagged `control:B` (above) are left out of the check order too, though still counted everywhere else, and `STATS.md`'s header says how many (`testing/CONTROL.md` §5.2).

## What the ledger measures over time
- **Check order:** which instincts cost the most (`STATS.md`).
- **Escapes:** findings marked `escaped` show where the reviewer's instincts are weakest. Falling escapes is the real sign of progress.
- **Precision:** `rejected` ÷ everything the agent reported. Too many rejections means it's crying wolf.
- **Regressions:** fixes that broke something. If one instinct keeps producing regressions, that class needs a shared guard, not more instance fixes.

## Project kinds
`tools/stats.py` keeps a check order per kind of software, from each project's `kind` in `projects.json`. Register a new project there when it's first reviewed or mined.

## Seeded from
A one-off script (not published) parsed the private app case study: 1.0.0 review, fidelity audit, pass-1 verification, the developer's own testing, pass-2 oversight. That's 216 findings. Ferrite's 154 historical bugs and 14 latent ones were added from `case-study-ferrite/`. The instinct mapping in that script is a reviewer's judgment, so correct it where it's wrong. S-N01, S-N03, S-N04 and S-N06 still need their detail filled in from PrivateApp's rtirr-log on the agent's first run there.
