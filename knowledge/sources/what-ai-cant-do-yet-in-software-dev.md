# What AI Can't Do (Yet) in Software Development
- **Source:** UC Berkeley Extension, "Voices", Sarah Benzuly, Apr 14, 2026. https://voices.berkeley.edu/technology-and-information-management/what-ai-cant-do-yet-software-development
- **Type:** opinion/essay
- **Evidence strength:** weak. No data or examples. It ends in a promotion for the Extension's paid software development program.

## Claims
All asserted without evidence:
- AI doesn't decide what to build. It can't ask the right clarifying questions, challenge assumptions or align technical decisions with real-world constraints.
- AI doesn't understand trade-offs (performance vs. development speed, scalability vs. simplicity, security vs. usability, short-term fixes vs. maintainability) and can't own outcomes.
- AI is "surprisingly good" at simple bugs. Real debugging involves multiple services interacting, legacy code with hidden dependencies, edge cases that appear only under specific conditions, and performance problems spanning systems.
- AI can't handle team dynamics, stakeholder priorities or ambiguity in meetings.
- Without the fundamentals, AI is a liability. You need them to recognize incorrect or inefficient output and to integrate generated code into larger systems.

## What humans catch that AI misses (per this source)
- Hidden dependencies in legacy code.
- Edge cases that appear only under specific conditions.
- Problems that come from services interacting.
- Whether a trade-off (e.g. scalability over simplicity) suits the project.

## Checks for the reviewer
- **Hidden dependents.** For every changed function, table, field or setting, list all readers: callers, ORM queries, raw SQL, templates, exports, scheduled jobs. Confirm each still holds. Maps to #6 and #28.
- **Trade-off has a stated need.** Caching, denormalization, background jobs or other scalability mechanisms in a change come with a written reason or requirement. Without one, flag it. `NEW: speculative abstraction`

## Over-engineering signals (if relevant)
- Only implied: choosing scalability over simplicity with no need. Detect as above.

## Process lessons for a non-coder directing AI
- The human defines the problem: user needs, business goals turned into requirements, the problem broken into parts, all before prompting.
- The human owns the trade-off decisions. Write them down.
- Learn enough of the fundamentals to tell when output is wrong.

## Quotes
- "AI can generate answers. But only someone with real understanding can tell if those answers are right."

## Caveats
- Promotional, with categorical "can't" claims and no evidence.
- "AI can't ask clarifying questions" is disputed by humans-missing-from-coding-agent-research.md, which treats clarification as an agent capability gap under active research, not an inherent limit.
