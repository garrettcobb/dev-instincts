# How to Stop AI From Over-Engineering Simple Problems
- **Source:** Substack, Arslan Ahmad, May 09, 2026. https://arslandg.substack.com/p/how-to-stop-ai-from-over-engineering
- **Type:** practitioner article
- **Evidence strength:** anecdotal. No data. Claims such as "dramatically simpler" and "noticeably simpler" are never measured.

## Claims
All asserted without evidence:
- Three forces push AI toward complexity:
  - the training data is dominated by production code, frameworks and large open-source projects, while throwaway scripts are under-represented;
  - training rewards "best practices" and maintainability;
  - the model reads a request charitably, as asking for robust, reusable, future-proof code.
- AI "generates code that would be appropriate for a system ten times more complex" than the one being built. This is a figure of speech, not a measurement.
- Over-engineered output "works. It compiles. It passes tests." The developer who accepts it inherits the complexity without noticing.
- Explicit limits on lines, files or abstractions produce "dramatically simpler output".
- A two-step prompt (describe the simplest approach first, then code) produces "noticeably simpler code".
- Asked to justify an abstraction, models defend it unless told "be honest, don't just defend the design".
- Asked to "rewrite in half the lines, no classes", the simpler version is usually equivalent or better.
- When more structure is right:
  - code that's about to be extended (e.g., ten more config sources coming);
  - code inside a codebase with an established pattern (consistency beats local simplicity);
  - high-consequence code (financial, security, user data), where AI's validation and error handling is "a feature, not a bug".

## What humans catch that AI misses (per this source)
- Whether the task is a one-off script or a production component. The AI can't tell unless told.
- Whether the "flexibility" an abstraction buys will ever be used.
- Whether the error handling defends against a failure that can actually happen.

## Checks for the reviewer
- **A class that's really one function.** The class is instantiated at one site and only one public method is ever called. Detect: AST, count instantiation sites and distinct method calls per class. Maps to NEW: Speculative generality.
- **An interface for one implementation.** An abstract base class or interface (`ABC`, `Protocol`, `interface`, `Abstract*`) with exactly one concrete implementer. Detect: grep the declarations and count subclasses or implementers. Maps to NEW: Speculative generality.
- **Options nobody uses.** Parameters with defaults that no call site ever passes, and config keys read in code but set to one value everywhere. Detect: for each defaulted parameter, search call sites for that keyword or position. Maps to NEW: Options nobody uses.
- **Defence against impossible failures.** A try/except wrapped around parsing a literal or constant; null checks on module constants or on values the code itself just created. Detect: try blocks whose inputs are all literals or constants; `is None` checks on names bound to literals. Maps to NEW: Defensive code for impossible states.
- **Framework instead of feature.** A plugin registry, multi-backend switch, retry queue or config file supporting exactly one backend or plugin. Detect: registry dicts or factory maps with one entry; strategy selection keyed by config with one possible value. Maps to NEW: Speculative generality.
- **Unmeasured optimisation.** Caching, memoisation, lazy evaluation or batching added to code that runs rarely or on small data, with no measurement cited. Detect: `@lru_cache`/`@cache`, cache layers or batch helpers added in the change, with no perf test or benchmark that motivated them. Maps to NEW: Optimization needs a measurement.
- **Don't strip validation from risky code.** Money, permissions and user data are where this source says defensive code is right. Over-engineering findings there need care. Maps to #10 and #9.

## Over-engineering signals (if relevant)
- Each check above is a signal. Also:
  - a "FileProcessor with configurable strategies" for a single file read;
  - a "small utility becomes a small framework";
  - six optional parameters nobody asked for;
  - `AbstractWidgetProcessor` with only `WidgetProcessor` implementing it.
- A size check: if the change's line count or file count is far above what the request implies, ask for a half-size rewrite and compare.

## Process lessons for a non-coder directing AI
- State the scope in the prompt, for example: "one-time utility, not production code"; "under 30 lines"; "single file, under 50 lines, standard library only, no classes, no configuration, no abstract interfaces".
- Ask for the simplest approach in 2–3 sentences before any code, then approve it or ask for more structure.
- Challenge any abstraction the agent adds: "If I removed it, what specifically would break? Be honest, don't just defend the design."
- Paste examples of the codebase's own simple style and ask the agent to match them.
- Tell the agent which code is high-consequence, so it keeps defensive code there and drops it elsewhere.

## Quotes
- "The code works. It compiles. It passes tests. It just does too much, in too many files, with too many layers"
- "be honest, don't just defend the design"

## Caveats
- No evidence for any effect size.
- Its claim that AI adds error handling for impossible cases sits awkwardly with the CodeRabbit data (coderabbit-ai-vs-human-code-report.md): AI PRs omit null checks, early returns and exception logic. Its claim of premature optimisation conflicts with CodeRabbit's finding that AI favours simple patterns and does about 8x more excessive I/O.
- Both can be true, with defence and effort in the wrong places. The reviewer should check where defensive code is, not how much there is.
