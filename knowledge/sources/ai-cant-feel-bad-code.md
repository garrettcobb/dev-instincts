# AI Can Write Code — But It Can't Feel Bad Code
- **Source:** Steemit post by user "jhavtech" (Jhavtech Studios, an app-development agency), #programming. Dated only "8 months ago (edited)"; the text places it in 2026. Path shown: /programming/@jhavtech/ai-can-write-code-but-it-can-t-feel-bad-code (host not shown).
- **Type:** opinion/essay (agency marketing)
- **Evidence strength:** weak. Every statistic is uncited ("a recent 2026 study", "recent reports", "the data is clear"). The author is an agency that sells review and "software rescue" work and cites its own unpublished analysis.

## Claims
- AI raises pull-request volume "by over 20%" while incidents per PR rose "nearly 24%" ("a recent 2026 study", no citation).
- Code duplication has risen "nearly eightfold" since AI agents became widespread ("reports from 2025 and 2026", no citation).
- Gartner: "nearly 40% of IT budgets" go to dealing with technical debt (attributed, no citation).
- "45% of the world's code is now deemed 'fragile'" (no source, no definition).
- AI-authored changes produce "1.7x more issues" than human-only ones (no source, no sample size).
- Jhavtech says its own analysis of "over 200 applications" found code smells more often in projects that lean on generation without professional review (no numbers, method or smell definition given).
- AI fixes one file and breaks modules outside its context window (asserted).
- AI follows "textbook" patterns that don't fit your infrastructure, leaving code that is rigid and bloated (asserted).
- AI ignores ambiguous names and Single Responsibility violations because it only tries to satisfy the prompt (asserted).

## What humans catch that AI misses (per this source)
- A 500-line function, a God object, a deeply nested loop: code that works now but will be painful to debug.
- A fix in one file that breaks callers in other modules.
- Copy-paste duplication.
- A poorly chosen or poorly wired dependency.
- Generic patterns that don't fit the actual infrastructure or scale.

## Checks for the reviewer
- **Callers of changed code.** For every changed function signature, return shape or field, grep the symbol across the repo and confirm each caller was updated and is covered by a test. Maps to #28 (and #6 when the change carries a rule).
- **Complexity of new code.** Flag new or modified functions over ~80 lines, nesting deeper than 3, or classes that mix unrelated responsibilities (many public methods touching unrelated tables). Use radon/lizard/eslint complexity rules on the diff. `NEW: complexity ceiling on new code`
- **Duplication.** Run a clone detector (jscpd, PMD CPD, `pylint --enable=duplicate-code`) on the changed files against the whole repo. Every new block that copies existing logic is a place where a later fix lands in one copy and misses the other. `NEW: reuse before build` (also #27)

## Over-engineering signals (if relevant)
- "Textbook" patterns imported regardless of fit. Detect by comparing new structure with how the rest of the codebase does the same job (see `NEW: reuse before build`).
- Bloat shows up as size. Track lines added per change and function length (see the complexity check).

## Process lessons for a non-coder directing AI
- Treat the AI as a literal intern who can't be held responsible. The human sets constraints and boundaries.
- Don't accept "almost right". The gap shows when review is skipped.
- Review should cover architecture, not just syntax: does it fit long-term goals, is it secure, can someone new understand it in six months.

## Quotes
- "AI predicts the next token; humans predict the next three years of maintenance."
- "acceleration without steering is just a faster way to crash."

## Caveats
- Self-promotional, with no sources. Don't cite its numbers. The 1.7x figure probably comes from the KB source "Our new report AI code creates 1.7x more problems" (note: coderabbit-ai-vs-human-code-report.md). Use that note instead.
- The "+20% PRs" roughly matches Chen & Stratton's measured +23% (see agents-more-code-not-more-software.md). The "+24% incidents per PR" has no traceable source.
- The comment thread is spam for a vibe-coding service.
