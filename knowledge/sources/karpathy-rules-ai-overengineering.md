# Why Your AI Coding Assistant Keeps Overengineering: 4 Rules That Actually Fix It
- **Source:** DEV Community, Evan-dong (CEO of EvoLink, which the post plugs at the end). No date shown; the author joined Mar 4, 2026. https://dev.to/evan-dong/why-your-ai-coding-assistant-keeps-overengineering-4-rules-that-actually-fix-it-d8a
- **Type:** practitioner article
- **Evidence strength:** anecdotal. Illustrative examples only, no measurement. It promotes an unrelated API gateway product, and the Karpathy post it builds on isn't linked.

## Claims
- Illustrative, not measured:
  - asked to add input validation, Claude Code writes an abstract class, three subclasses and a factory: 200 lines where 5 were needed;
  - asked to fix a bug, it refactors adjacent functions, adds type hints and changes quote style, so "half the diff" is unrelated;
  - a bug-fix diff runs 40 lines where it should be 4.
- In January 2026, Andrej Karpathy posted on X about four recurring failure modes in LLM-assisted coding. Asserted; no link given.
- Someone turned these into a single CLAUDE.md, repo `forrestchang/andrej-karpathy-skills`, "currently at 97.8k stars".
  - The OCR'd screenshot instead reads "multica-ai/andrej-karpathy-skills" with "227k" and "23k". The repo name and the counts are inconsistent or garbled; don't rely on them.
- **Rule 1, Think before coding.** State assumptions, list interpretations, stop when confused. Example: "write an export function" silently became CSV, all fields, overwrite existing file. "30 seconds" of questions vs. "30 minutes of debugging" (rhetorical).
- **Rule 2, Simplicity first.** No features beyond the request, no abstractions for single-use code, no speculative future-proofing; "If 200 lines could be 50, rewrite." Example: a discount calculation came back as a Strategy pattern with a factory and a config file. The OCR reads "4@ lines of Strategy pattern" (probably 40) against a one-line `apply_discount`.
- **Rule 3, Surgical changes.** Touch only what you must; every changed line traces to the request; mention unrelated dead code, don't delete it. Example: a time-zone fix also added type hints, a docstring and changed quotes.
- **Rule 4, Goal-driven execution.** Turn vague tasks into verifiable goals ("Write tests for invalid inputs, then make them pass") and loop until they pass. Claim: LLMs otherwise "write code and call it done. No tests, no verification."
- The author's take:
  - Surgical Changes gives the biggest day-to-day gain;
  - drive-by changes slip through review in large diffs where formatting mixes with logic;
  - over-engineering is easy to see by comparison.
- Stated limitation: the rules fix behavioural tendencies, not capability gaps. "If the model doesn't understand your architecture, four rules won't save it."

## What humans catch that AI misses (per this source)
- Unrequested choices made silently: format, fields, overwrite vs. append.
- Unrelated edits hidden inside a fix.
- An abstraction where a line would do.
- "Done" claimed with no test behind it.

## Checks for the reviewer
- **Every changed line traces to the request.** Flag:
  - hunks in functions the task doesn't involve;
  - whitespace, quote or type-hint-only hunks;
  - renames "for clarity";
  - added docstrings;
  - deleted "dead" code outside the task.

  Detect: compare `git diff --stat` with `git diff -w --stat`; map hunks to the task; list files touched but not named in the task. Maps to NEW: Diff traces to the ask/plan.
- **Silent defaults.** For file writes and exports, check the mode: overwrite without an existence check or confirmation. For each, ask whether the spec decided format, fields, encoding and time zone. Detect: `open(..., 'w')`, `to_csv(path)`, `writeFile` on user-visible paths with no prior check. Maps to NEW: Unstated defaults are decisions.
- **Naive datetimes.** The time-zone example is the classic case. Detect: `datetime.now()`/`datetime.utcnow()` without tz; `strftime` on naive values; mixed aware and naive comparisons. Maps to #11.
- **Single-use abstractions.** Detect: a Strategy, factory or ABC with one implementation; a config file read by one function for one value. Maps to NEW: Speculative generality and NEW: Options nobody uses.
- **Validation tasks proved by failing tests first.** Tests for invalid inputs exist and were seen failing before the fix. Maps to #9 and #39.
- **"Done" means a run.** The completion message names the tests run and their result. Maps to #26.

## Over-engineering signals (if relevant)
- **Strategy pattern + factory + config file for a single formula.** Detect: classes named `*Strategy`/`*Factory` with one product.
- **An abstract base + three subclasses + factory for simple validation.** Detect: class count in the change against the number of rules actually validated.
- **Speculative future-proofing.** Detect: parameters, hooks or extension points with no caller.

## Process lessons for a non-coder directing AI
- Put the four rules in the project's CLAUDE.md:
  - make the agent ask clarifying questions before coding;
  - forbid unrequested features and abstractions;
  - restrict edits to what the task needs, and have it list unrelated issues rather than fix them;
  - define done as passing tests the agent wrote for the goal.
- Rules don't fix missing architectural understanding. Give the agent the architecture as well.

## Quotes
- "Every changed line should trace directly to the user's request."
- "If you spot unrelated dead code, mention it — don't delete it."

## Caveats
- Promotional author, no data, unverifiable star counts.
- The over-engineering claim is broadly echoed by Ahmad, but it sits in tension with the AIDev data cited by Alenezi (agent PRs are structurally simpler). It's also in tension with Borg et al., where Claude Code was conservative on refactors (mostly renames and formatting).
- The code samples are partly garbled by OCR.
