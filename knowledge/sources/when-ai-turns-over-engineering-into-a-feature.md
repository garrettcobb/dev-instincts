# When AI Turns Over-Engineering into a Feature
- **Source:** DEV Community, posted by Clear Data Labs on May 1, originally published at cleardatalabs.com. The account joined May 1, 2026; no named author. https://dev.to/cleardatalabs/when-ai-turns-over-engineering-into-a-feature-3mm6
- **Type:** opinion/essay
- **Evidence strength:** anecdotal. One code-review anecdote and argument, no data.

## Claims
- **Anecdote.** In a code review, the author found a new AI "Skill" file that used hooks and scripts to keep configuration variables in sync across several places in a project. The fix was to move the config into one shared module. In the author's framing, "fifty lines of automation rather than moving five lines of configuration."
- Asserted without evidence:
  - LLMs have made refactoring cheap. Paradoxically, teams now defer technical debt and build AI workarounds instead.
  - "When the cost of adding complexity drops, the volume of complexity tends to rise."
  - AI optimises locally for the prompt it's given unless it gets architectural context. Its answers are correct within the frame even when the frame is wrong.
  - A developer who doesn't know a principle (e.g., single source of truth) won't ask the AI for it, and will ask the AI to maintain the current approach instead.
  - The pattern spreads because automation looks like progress, teams are rewarded for visible tooling, and treating symptoms is easier.
- "Comprehension debt": the system works, but the team no longer understands its complexity.
- Exception: in distributed, multi-environment or cross-service systems, some duplication and syncing is unavoidable and automation is justified.

## What humans catch that AI misses (per this source)
- That the requested automation shouldn't exist: the real fix is structural (one source of truth).
- The question behind the prompt: "how do I fix the architecture?" instead of "how do I automate this annoyance?"

## Checks for the reviewer
- **One source of truth.** The same configuration value, constant or business rule defined in more than one file. Detect:
  - identical literal assignments or keys across `.env`, settings, JS constants and templates;
  - the same magic number in several modules;
  - the same validation rule written twice.

  Maps to NEW: One source of truth; don't automate around duplication (related to #6 and #27).
- **Sync automation is a symptom.** Scripts, hooks, AI skills or pre-commit steps whose job is to copy, propagate or check that values stay equal across files. Detect: names like `sync_*`, `propagate*`, `*_mirror`; hooks under `.claude/` or `.git/hooks` that rewrite tracked files; tests asserting two copies are equal. Maps to NEW: One source of truth; don't automate around duplication.
- **Comprehension debt.** For each new piece of tooling or automation in a change, ask: "Does this exist because of real system complexity, or a preventable design issue?" Report it to the developer if it's the second. Maps to #38 and NEW: One source of truth; don't automate around duplication.

## Over-engineering signals (if relevant)
- **Automation that compensates for duplication.** Detect as above.
- **Tooling that grows faster than features.** Count lines in scripts, hooks and skills against lines of app code across recent changes.
- **"Agents" or "Skills" that manage drift between parts of one repo.**

## Process lessons for a non-coder directing AI
- Before asking the AI to automate a repetitive chore in the codebase, ask it whether the chore exists because of a design flaw, and what the structural fix would be.
- Give the AI architectural context. Without it, the AI solves the problem inside your current (possibly wrong) frame.
- The developer has to know the principles to ask for them. Where he doesn't, the reviewer must supply them.

## Quotes
- "If you multiply a mess, you simply get a faster, more automated mess."
- "Does this task exist because of genuine system complexity, or because of a preventable design issue?"

## Caveats
- A single anecdote, with no measurement of how common this is.
- It doesn't say whether the Skill file was written by a person or by the AI. The point is the design choice, not AI authorship.
- Consistent with TheBitForge's "DRY is about knowledge": a duplicated config value is duplicated knowledge.
