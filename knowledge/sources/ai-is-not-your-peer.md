# AI Is Not Your Peer
- **Source:** notyourpeer.com, subtitled "A manifesto on engineering in the age of AI". The author names aren't legible in the OCR. The credits list several people, plus "Claude Opus 4.7" and "GPT-5.5". No date is shown (the page was captured 10/30/26). https://www.notyourpeer.com
- **Type:** opinion/essay
- **Evidence strength:** anecdotal. A manifesto with no data; the argument is structural, not empirical.

## Claims
No numbers. All asserted without evidence:
- Peer review had two purposes: catching mistakes before production, and making both the author and the reviewer better over time.
- With an AI author, the learning half is gone. The agent doesn't carry feedback from one PR into the next, and is "exactly as good, and exactly as bad, tomorrow."
- An AI PR fuses two things: the human's decisions about what to build, and the agent's rote guesses about how to build it. From inside the diff you can't tell which line is which.
- The hard part of engineering is understanding the problem and planning the solution. The agent took over the expression, not the understanding.
- Proposal: move human peer review to the plan given to the agent. Hand the diff to an agent that checks for bugs and for faithful implementation of the plan, the way a compiler or test suite is trusted.

## What humans catch that AI misses (per this source)
- Disagreement on substance. A peer pushes back because they think you're wrong; a model doesn't.
- Whether the plan is right: what to build, and the shape of the system.

## Checks for the reviewer
- **A written plan governs the change.** Detect: the change refers to a plan or spec file committed in the repo before the code; flag code with no governing document. Maps to #41 and #34.
- **The diff matches the plan in both directions.** Every plan item has code and a test, and every diff hunk maps to a plan item. Detect: build a plan-item-to-hunk table, then list orphan hunks and unimplemented items. Maps to NEW: Diff traces to the ask/plan.
- **The agent's unchosen guesses are surfaced.** List each implementation choice the plan didn't make: defaults, overwrite vs. append, behaviour on error, rounding, time zone, sort order, what gets deleted. Report them to the developer as decisions to confirm. Maps to NEW: Unstated defaults are decisions.
- **Recurring findings become rules.** The agent doesn't learn from review, so a finding that recurs across rounds must become a written rule (the project's CLAUDE.md or the checklist) or a guard test. Detect: the same smell appears in the ledger in two or more rounds with no matching rule or test in the project. Maps to #27.

## Over-engineering signals (if relevant)
- Not discussed.

## Process lessons for a non-coder directing AI
- The plan is the human work. Make it explicit enough that another person could review it.
- Improve the instructions rather than expecting the agent to learn from review comments.
- Treat the agent's diff check as a mechanical audit against the plan, not as peer review.

## Quotes
- "the parts that were so obvious we didn't bother to specify, the parts nobody chose."
- "People review people's work. Machines check machines'."

## Caveats
- No evidence.
- "Machines check machines'" conflicts with the CSA article ("Engineers must review every line of AI code") and with DEV-INSTINCTS #38 (a second human reviews the risky parts).
- Alenezi's synthesis (human-ai-collaboration-se-work.md) warns that agent output reviewed by a bot from the same provider risks correlated blind spots.
- The page credits AI models as contributors.
