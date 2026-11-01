# AI Loves to Over-Engineer Your Code (And You're Letting It)
- **Source:** DEV Community, Tyson Cung (Data & Cloud tech lead; CPO at hivo.co), date not shown, https://dev.to/tyson_cung/ai-loves-to-over-engineer-your-code-and-youre-letting-it-4p9m
- **Type:** opinion/essay
- **Evidence strength:** anecdotal — personal observation; its one number has no source.

## Claims
- Ask for something trivial (read a CSV) and AI returns a factory, configurable parsing strategies, an abstract data-source interface, custom exception hierarchies and a YAML config loader, where a human writes about five lines. Illustrative, not measured.
- AI assumes every problem must scale because it lacks context (e.g., that this is a throwaway script) and falls back on enterprise patterns from training. Asserted.
- "Microsoft's internal data" shows AI code is 20–30% more verbose than human equivalents. No citation; treat as unsupported.
- More lines mean more bug surface, longer review and more documentation nobody writes. Asserted.
- The author strips about 60% of AI suggestions before committing. Personal habit.

## What humans catch that AI misses (per this source)
- Which patterns not to use.
- Whether the code is a throwaway or a long-lived product.

## Checks for the reviewer
- Pattern inventory per feature. Detect: grep `class \w+(Factory|Strategy|Provider|Manager|Registry|Builder)`, `ABC`, `@abstractmethod`, `Protocol`, `interface `, `class \w+(Error|Exception)\(`, new config loaders/YAML files. For each, count implementations and call sites; flag one implementation, one caller, or no distinct handling. → NEW: Every abstraction earns its place.
- Delete-the-layer test: in a scratch copy, inline the abstraction and run the tests. If they pass and nothing else uses it, it's surplus. → NEW: Every abstraction earns its place.
- Config for constants: new settings, env vars or YAML keys that hold one value everywhere and are never overridden. Detect: grep the key; compare the default with overrides. → NEW: Every abstraction earns its place.
- Exception classes nobody catches. Detect: for each new exception class, grep `except <Name>` / `instanceof <Name>`; zero hits means surplus. → NEW: Every abstraction earns its place.

## Over-engineering signals (if relevant)
- A factory or strategy for one product; an interface with one implementation; a config loader for fixed values; exception classes nobody catches. Detection as above.
- A diff far larger than the request. His rule of thumb is that about 60% is removable.

## Process lessons for a non-coder directing AI
- Say what you don't want: "simple function, no classes, no patterns" works, per the author.
- Give the context (throwaway or long-lived) so the AI doesn't guess "enterprise".
- Ask: would I accept this if I had to maintain it alone?

## Quotes
- "The AI treats every problem like it might need to scale to a million users by Thursday."
- "If you can delete an abstraction layer and the code still works, delete it."

## Caveats
- Anecdote only; the Microsoft figure is unsourced.
- The two large studies in this group don't show AI adding classes or inheritance. Mao et al. find Java OOP metrics at parity and AI C++ classes simpler; Cotroneo et al. find AI functions shorter. The "enterprise pattern reflex" may depend on the tool (agent vs. completion) or the prompt.
- "Delete it, every time" must not remove guards this catalogue requires (#1, #2, #8, #9). Passing tests only prove the layer is unused if the tests cover it.
