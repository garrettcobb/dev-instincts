# AI Hasn't Killed Coding. It's Made Knowing How to Code More Important.
- **Source:** Medium, Brandon A. Olivares, Apr 27, 2026. https://medium.com/@pbrandonaolivares/ai-hasnt-killed-coding-it-s-made-knowing-how-to-code-more-important-08257bf49a62
- **Type:** practitioner article
- **Evidence strength:** anecdotal. One bug in the author's own open-source Crockford Base32 TypeScript library. It is well described and the model admitted the error, but n=1.

## Claims
- The author's hand-coding is down "maybe 90%" in about a year. He still codes the nuanced parts by hand because the AI "butchers" them.
- Claude added checksum encoding after thinking for 6 minutes. All unit tests passed, and he saw no issues on review.
- On decoding, Claude applied the spec's look-alike substitutions (0/O and 1/I/L) to every character except the checksum character. The spec has no such exception, so valid input was rejected. All tests passed anyway.
- He caught it only because he knew the spec. When asked, Claude said it had made the rule up, fixed it and added regression tests.
- Asserted from experience: the AI "will iterate until the tests pass", so invalid code is rarely the problem. Hidden assumptions are.
- Every domain has hidden business rules. Technical judgment is also needed: when a database transaction is required, which columns need indexes, which authentication design fits.
- The example encodings were garbled by OCR (12099 shows as "sx1c" / "5x1g"; the checksum examples are garbled too). Don't use them.

## What humans catch that AI misses (per this source)
- A special case that isn't in the spec: a general rule silently exempted for one position (here, the last character).
- That a passing test suite says nothing about a rule nobody wrote a test for.
- Knowing where transactions and indexes are needed, and which auth design suits the app.

## Checks for the reviewer
- **Every special case cites the spec.** In code that implements a published spec, algorithm or business rule, list every branch that exempts a subset (last element, first row, one type, one status) from a general rule. Each needs a spec citation; flag the rest. Smell: index-based exemptions near rule logic, such as `slice(0, -1)`, `[-1]`, `i < len - 1`, `if (i === n - 1)`, `isLast`. `NEW: assumptions traced to spec`
- **Tests come from the spec.** Build test cases from the spec's own examples and tables, with every variant (case, substitution) at every position, including the edges. Tests the agent wrote for its own reading of the spec don't count. Maps to #42 and #33.
- **Multi-write paths are atomic.** Any function with two or more writes runs in one transaction. Maps to #1.
- **Filtered and joined columns are indexed.** Check query counts and plans at real size. Maps to #13.

## Over-engineering signals (if relevant)
- Not relevant. The bug was an invented rule, not excess structure.

## Process lessons for a non-coder directing AI
- Keep the spec (or business rules) in the repo, and require the agent to list every place its code departs from or adds to the spec.
- Ask pointed questions about specific behaviors. Claude admitted the invented rule as soon as it was asked directly.
- Green tests aren't proof. Someone who knows the domain, or an independent reviewer holding the spec, has to compare behavior with the rules.
- Treat the AI as "a drunk intern" (the author's workplace phrase): its brilliant and its wrong output look the same on the surface.

## Quotes
- "It failed because there was a hidden assumption that I almost missed."
- "All the tests passed — it will iterate until the tests pass so that's rarely a concern."

## Caveats
- One minor bug in a niche library, caught by an expert who knew the spec. It shows the failure mode exists, not how often it happens.
- The author's bio is unrelated to software, though the article shows a working developer.
