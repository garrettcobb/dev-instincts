# Position: Humans are Missing from AI Coding Agent Research
- **Source:** Position paper by Zora Zhiruo Wang, John Yang, Kilian Lieret, Alexa Tartaglini, Valerie Chen, Yuxiang Wei, Zijian Wang, Lingming Zhang, Karthik Narasimhan, Ludwig Schmidt, Graham Neubig, Daniel Fried and Diyi Yang (Carnegie Mellon, Stanford, Princeton, UIUC). No date or venue in the text; it cites 2026 work and models up to GPT-5.2 and Claude Opus 4.5.
- **Type:** preprint (position paper)
- **Evidence strength:** moderate. The main argument is a position. Its own measurements are real but proxy-based:
  - patch size against SWE-bench Verified "gold" patches, resolved instances only, run with mini-swe-agent across ~15+ models;
  - causes and functional differences labelled by two small LLM judges (GPT-5 mini, Claude Haiku 4.5) that treat the gold patch as optimal.
  Several authors built SWE-bench/SWE-agent.

## Claims
**Its own measurements (appendix A)**
- Agent patches are consistently longer than the human gold patches on SWE-bench Verified, even when they pass. Per-model values in Figures 1 and 5 are garbled by OCR. The Figure 1 axis spans a bloat ratio of about 1.0 to 2.0.
- Method: remove newly added files, non-Python files and test-file changes from both patches, then compare character lengths. "Bloated" means more than 1.5x the gold patch.
- Average bloat is "largely uncorrelated" with resolve rate and trends upward with model release date: newer models write bigger patches.
- Every model has more than 15% of resolved patches bloated beyond 1.5x, so it isn't just outliers.
- Causes of bloat, on resolved patches longer than gold (multi-label, two LLM judges):
  - verbose implementation ~60%;
  - scope creep 50–65%;
  - overly defensive code 20–30%;
  - excessive documentation 20–30%;
  - over-engineered architecture ~10%.
- Functional discrepancy against gold in resolved (test-passing) patches:
  - over 50% for every model;
  - Haiku flags 66%, GPT-5 mini 62%, both 57% (the conservative figure);
  - standard-behavior and edge-case differences each affect about one third;
  - about 20% miss functionality the gold patch has;
  - over 10% include unrelated functional changes;
  - discrepancies correlate weakly with resolve rate and are more common in newer models.

**Cited from others**
- Stack Overflow 2025: of the 84% of developers using AI coding tools, nearly half don't trust the output, and two-thirds say half-baked solutions mean heavier debugging.
- Sonar 2026 (a vendor survey):
  - developers rarely write tests before prompting, so tests are generated along with the code;
  - less-experienced developers report both the biggest productivity gains and the hardest time reviewing agent output.
- Cursor Tab RL mined 400M+ daily accept/reject decisions and found that when to suggest matters as much as what to suggest.
- The CUPS taxonomy splits programmer–AI interaction into 12 states.
- 850 SWE-bench tasks come from Django, yet solving one doesn't help with the next.
- Amodei (March 2025) said AI would soon write 90% of code.
- Computable proxies for maintenance burden exist: cyclomatic complexity, cognitive complexity, maintainability index, readability metrics.

**Argued (position)**
- The bottleneck is shifting from "can it work?" to whether humans can understand, steer, verify and trust the agent.
- Models start implementing without inferring unstated constraints, which produces a "clarification spiral" of rejections and new misunderstandings.
- Agent "memory" and "skills" are mostly indexed markdown files, not real learning.
- Safety failures are breakdowns of steerability (no checkpoint before an irreversible action) or of verification (output not assessed before commit).

## What humans catch that AI misses (per this source)
- Behavior differences on standard inputs and on edge cases (None, empty, zero, boundaries, error paths) that hidden tests don't cover.
- Functionality the request implied but the patch left out.
- Unrelated changes riding along: reformatting, import reordering, dependency edits, touched files the fix doesn't need.
- Unstated constraints and intent.
- Whether the tests encode the intent at all.

## Checks for the reviewer
The paper's five bloat categories (appendix A.2) and five discrepancy categories (A.3) are ready-made reviewer rubrics.
- **Scope creep.** Every hunk in the diff maps to the request. Flag:
  - whitespace-only hunks (`git diff -w` shrinks them);
  - quote or import reordering;
  - lockfile or dependency changes with no stated need;
  - edits to files or functions the task doesn't involve;
  - unrelated comment edits.
  `NEW: scope creep`
- **Bloat ratio.** Track non-test, non-new-file lines added per change and flag outliers against the project's history. Where a minimal fix is obvious, flag diffs over 1.5x it. `NEW: patch bloat`
- **Verbose implementation.** Explicit loops where a built-in exists, intermediate variables used once, long condition chains, logic duplicated instead of reusing an existing helper. `NEW: patch bloat` and `NEW: reuse before build`
- **Overly defensive code.** New try/except around code the rest of the codebase trusts, None or type checks on values that can't be None, broader exception catches, `errors='ignore'`, unneeded fallback paths. Defending impossible states: `NEW: defensive code for impossible states`. Swallowing real errors: #25.
- **Temporal comments.** Comments describing the change instead of the code: `# now`, `# fixed`, `# updated to`, `# changed`, `# new:`. `NEW: patch bloat` (minor)
- **Over-engineered.** New classes, functions or modules the fix doesn't need, config parameters "for flexibility", wrappers, decorators or factories, extensibility scaffolding. `NEW: speculative abstraction`
- **Edge-path behavior.** For each change, list behavior on None, empty, zero, boundary and error paths, and require a test per path derived from the spec, not from the code. Maps to #9 and #42. Where the spec is silent: `NEW: assumptions traced to spec`
- **Missing functionality.** Walk the requirement list item by item against the diff (about 20% of passing patches missed something). Maps to #33. `NEW: assumptions traced to spec`
- **Co-generated tests.** Tests written in the same change by the same agent aren't independent evidence. Require expected values from outside the code, and confirm each new test fails when the fix is reverted. Maps to #42, #39, #31.
- **Complexity delta.** Compute cyclomatic or cognitive complexity for changed functions and flag increases above a threshold. `NEW: complexity ceiling on new code`
- **Irreversible actions.** Deletes, migrations and external side effects in the change have a checkpoint or a confirmation and a rollback test. Maps to #14 and #15.

## Over-engineering signals (if relevant)
These are the paper's own definitions; detect each by comparing the diff with a minimal fix.
- Unnecessary new classes, functions or modules.
- Config options or parameters for flexibility nobody asked for.
- Generic solutions where a specific fix would do.
- Layers of indirection: wrappers, decorators, factories.
- Infrastructure for future extensibility.
- Overly defensive code: checks for cases the surrounding code trusts won't happen.
- Verbose implementation: same logic, more lines.
- Excessive documentation: comments explaining obvious code or describing what changed.

## Process lessons for a non-coder directing AI
- Write the critical requirements and tests before prompting. Tests generated with the code only move the checking burden to "do the tests capture intent?".
- Ask for verification evidence you can check without reading code: a visual render for UI work, a short summary for data work (e.g. how missing values were handled), a recording of the flow.
- Expect the clarification spiral. Front-load unstated constraints, and ask the agent to stop at real decision points (trade-offs, irreversible steps) instead of presenting a finished plan to accept or reject.
- Persist preferences in a rules file (AGENTS.md / CLAUDE.md) and check they actually hold in the next session. The paper's example: "use logging instead of print".
- A newer model isn't automatically better here: newer models wrote bigger patches with more functional differences.

## Quotes
- "When AI is producing both, the tests no longer serve as independent evidence for building trust."
- "even resolved instances can have functional discrepancies with the gold patch"

## Caveats
- Treating the gold patch as minimal and correct is an assumption. Some "discrepancies" may be legitimate alternatives (the paper says so).
- The judges are two small LLMs that agree less on individual categories than on the overall flag.
- SWE-bench is Python issue fixing in mature repos, not building new features, so its "overengineered ~10%" may understate architecture bloat in greenfield builds.
- It conflicts with human-vs-ai-code-human-still-wins.md on defensive checks.
- Its reading of Stack Overflow 2025 ("two-thirds … heavier debugging burdens") differs from TechTarget's reading of the same survey (66% "almost right", 45% say debugging takes longer).
- Exact per-model numbers in the figures are unreadable in this OCR.
