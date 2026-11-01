# AI Has No Wisdom and Neither Will You
- **Source:** alexn.org (personal blog), Alexandru Nedelcu, 22 September 2026, https://alexn.org/blog/2026/09/22/ai-has-no-wisdom-and-neither-will-you/
- **Type:** opinion/essay
- **Evidence strength:** anecdotal — an experienced developer's argument with no data. No commercial conflict.

## Claims
- Vibe-coded projects degrade over time into unmaintainable code. Asserted without evidence.
- Maintainability and architecture have no good immediate measurement; bad architecture shows up after months or years.
- Bad code, as he defines it: hard to read and evolve; a change breaks something far away; a feature needs edits in many places and some get missed; design invariants are unclear and their authors are gone; tests need mocks and expose implementation details, which blocks refactoring.
- Experts smell problems by intuition long before effects appear, and that intuition can't be reduced to rigid rules.
- AI isn't trained on maintainability: RL needs an immediate reward; models learn beginner rulebooks and mostly bad code from the wild; no fitness function for maintainable code exists, or linters would have it. Asserted.
- Current top models are bad at "simplifying": they split functions into smaller ones that aren't reusable. Asserted from his experience.
- People who let AI write and read code stop making choices, don't learn from mistakes, and won't reach mastery. Asserted.
- Prediction: companies will advertise "NO-AI" policies as an advantage. Speculation.
- Reader comment (not the author): someone who built a browser-only passport-photo tool says LLMs repeatedly proposed moving biometric processing to a server, breaking the app's core privacy invariant, and produced print geometry that "looked about right" but failed physical measurement. A single anecdote.

## What humans catch that AI misses (per this source)
- A helper that you have to read to understand its caller isn't a real abstraction.
- Changes that need the same edit in several places, one of which will be missed.
- Design invariants, and the change that quietly breaks one.
- Tests coupled to internals that will block the next refactor.

## Checks for the reviewer
- Single-use extracted helpers. Detect: functions defined and called exactly once (grep the name, count call sites), short, in the caller's module. Flag those where the caller can't be understood from the helper's name alone. → NEW: Every abstraction earns its place.
- One rule written in many places. Detect: the same status string, threshold or business-rule literal in 3+ files (grep the literal), or a feature diff making near-identical edits in many files. → #6, #27.
- Invariant breaks: the change adds network calls, server round-trips or external services to an app whose stated invariant forbids them. Detect: new `requests`/`httpx`/`urllib`/`fetch(`/`axios`/SDK imports or URLs in the diff, checked against the project's governing documents. → #35, #41.
- Over-mocked tests. Detect: tests that `mock.patch`/`jest.mock` private functions of the module under test, or assert call counts on internals instead of outputs and stored state. → NEW: Tests pin behavior, not implementation.
- Effects at a distance: after any change, run the whole battery, not just tests near the change. → #28.

## Over-engineering signals (if relevant)
- Decomposition without reuse: many tiny one-caller functions. Detect: call-site counts per function.
- A reply signed "Alex" (apparently the author) says more reasoning effort gives "overengineered" output. He calls it exaggeration; no evidence.

## Process lessons for a non-coder directing AI
- Don't hand both the writing and the reading of code to AI; a person has to keep making and owning the design choices.
- Tests passing today can't show maintainability. That takes a trained eye, or written invariants to check against.
- Checklists have limits: expert judgement depends on context.

## Quotes
- "AI is not trained on what it means for code to be maintainable."
- "There is no fitness function you can define for maintainable code"

## Caveats
- Opinion piece with no measurements.
- His "AI over-splits functions" claim sits awkwardly with Mao et al. (same group): AI files there have fewer functions (6.62 vs 11.67), though deeper call chains.
- Comments are reader content. The invariant anecdote is one person's report, and the comment thread names models that can't be checked here.
