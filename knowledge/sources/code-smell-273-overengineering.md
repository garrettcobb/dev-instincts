# Code Smell 273 — Overengineering
- **Source:** Medium (Javarevisited publication), Maximiliano Contieri, Oct 5, 2024. medium.com/javarevisited/code-smell-273-overengineering-13399697eff5 (OCR split the ID).
- **Type:** opinion/essay (the author's disclaimer: "Code Smells are my opinion")
- **Evidence strength:** anecdotal. One toy example from the author's own smell catalog, no data.

## Claims
- Overengineering is a solution too complex for the problem: needless layers of abstraction, complex design patterns, bloated architecture (definition).
- Listed problems: accidental complexity, premature optimization, unnecessary abstractions, poor maintainability, overly detailed designs, slow iteration, "bijection violation" (the author's own model-to-reality concept), performance penalties. All asserted.
- Typical forms: overuse of factories, excessive inheritance, interfaces split too finely.
- AI generators often suggest factories or strategies where something simpler would work (asserted).
- AI can help detect overengineering by suggesting simplifications, but a human must judge whether the complexity serves a purpose (asserted).
- Detection is manual: it's a semantic smell.
- Example: an abstract `PlanetCalculator`, one subclass and a factory with a single branch that throws for any other type, versus one plain class with one method.

## What humans catch that AI misses (per this source)
- An inheritance hierarchy plus factory built for exactly one case.
- Classes, methods or features that don't contribute to solving the problem.
- Whether a pattern's complexity is earning its keep.

## Checks for the reviewer
- **One-implementation abstraction.** Find abstract classes, interfaces, Protocols and ABCs (`abstract class`, `interface `, `ABC`, `Protocol`, `Base*`) and count concrete implementers. Exactly one, with no second one planned in the docs, gets flagged. `NEW: speculative abstraction`
- **Single-product factory.** `*Factory` / `get*` / `create*` functions with one real branch and a throw or raise for everything else. `NEW: speculative abstraction`
- **One-strategy pattern.** `*Strategy`, `*Provider` or `*Handler` registries holding a single entry. `NEW: speculative abstraction`
- **Unreachable or unused code.** Run dead-code tools (vulture, ts-prune, knip) on the diff. Classes and methods no feature path calls get flagged. `NEW: speculative abstraction`

## Over-engineering signals (if relevant)
- Factory plus abstract base for one type. Detect with the counts above.
- Inheritance more than 2 levels deep for a single use. Detect from class-hierarchy depth on new classes.
- Interfaces split so finely that each has one method and one implementer. Detect by counting interfaces against implementers.
- Premature optimization: caching or pooling with no measured need. Detect caches or pools added without a perf test or stated requirement (links to #13).

## Process lessons for a non-coder directing AI
- AI defaults to patterns. Give explicit instructions to keep it simple (the article sets up with/without-instructions comparisons in several assistants, but shows no results).
- Use the AI to propose simplifications, but someone has to decide whether each abstraction has a real second use.

## Quotes
- "AI generators often introduce overengineering by suggesting patterns like factories or strategies where simpler solutions would work."
- "You can detect overengineering by looking for excessive classes, methods, or features that do not contribute directly to solving the problem."

## Caveats
- Written in 2024, before coding agents were common. Opinion, no measurement.
- "MAPPER" and "bijection" are the author's own framework, not a shared standard.
