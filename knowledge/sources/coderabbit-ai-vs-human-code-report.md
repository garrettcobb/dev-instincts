# State of AI vs. Human Code Generation Report (blog: "Our new report: AI code creates 1.7x more problems")
- **Source:** CodeRabbit blog. No author or date shown (page captured 10/30/26). https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
- **Type:** industry report (vendor)
- **Evidence strength:** weak. The sample is moderate (n=470 PRs), but:
  - CodeRabbit sells an AI review tool, and the issues were classified with its own taxonomy;
  - AI vs. human authorship was inferred from co-author signals, and "human" PRs may include AI work;
  - the human group is small (150);
  - only the blog summary is in the text, not the full methodology.

## Claims
- An unnamed "recent report": pull requests per author rose 20% year over year with AI help, while incidents per PR rose 23.5%. Cited without a source in the text.
- Sample: 470 open-source GitHub PRs, 320 AI co-authored and 150 human-only. Findings were normalised to issues per 100 PRs and compared by rate ratios.
- No issue category was unique to AI. Most categories had significantly more issues in AI PRs.
- AI PRs had about 1.7x more issues overall: 10.83 per PR vs. 6.45 for human-only PRs. High-issue outliers were much more common in AI PRs.
- AI PRs had 1.4x more critical and 1.7x more major issues. The chart's raw numbers are OCR-garbled ("240 (Human) || 257 (Human)").
- Critical and major issues included business-logic mistakes, incorrect dependencies, flawed control flow and misconfigurations.
- Readability was "the single biggest difference" in the dataset; the multiplier isn't legible in the OCR. AI code "looks consistent but violates local patterns around naming, clarity, and structure."
- AI code often omits null checks, early returns, guardrails and comprehensive exception logic. Multiplier not in the OCR.
- Security: the most prominent pattern was improper password handling and insecure object references. No vulnerability type was unique to AI, but "nearly all were amplified". Multiplier not in the OCR.
- Excessive I/O operations were about 8x more common in AI PRs.
- Concurrency and dependency-correctness problems (wrong ordering, faulty dependency flow, misused concurrency primitives) were about 2x more common.
- Formatting problems were 2.66x more common, "even teams with formatters and linters".
- Naming inconsistencies were nearly 2x more common.
- A chart lists "Unused/redundant code" among the quality categories where AI makes more mistakes; no number given.
- Findings 3–7 are only partly captured by the OCR; their headings and some multipliers are missing.
- The stated causes (asserted):
  - AI infers patterns statistically, not semantically, and misses local business rules;
  - its correctness is surface-level;
  - it drifts to generic idioms;
  - it recreates legacy security patterns from older training data unless prompted;
  - it favours clarity over efficiency (simple loops, repeated I/O).
- "Reviewer fatigue has been found to lead to more issues and missed bugs." Asserted, with no citation in the text.

## What humans catch that AI misses (per this source)
- The local business rules senior engineers have internalised.
- Missing control-flow protections: null checks, early returns, exception paths.
- Wrong dependency or initialisation order and misused concurrency primitives.
- Drift from the repo's naming, structure and idioms.
- Outdated security patterns: ad-hoc password handling, object references without an ownership check.
- Wasteful I/O.

## Checks for the reviewer
- **Error paths are covered.** For each new external call (DB, file, network, email), force it to fail. Expect a clear message, no partial write and no false success. Detect: new I/O call sites with no failure-path test. Maps to #18, #8 and #1.
- **Missing guards.** New functions that take external input with no `None`/empty/type check or early return. Detect: parameters from request, form or file used without validation. Maps to #9.
- **Concurrency and ordering.** Shared state written without a lock or transaction. Initialisation that depends on import or call order. Detect: module-level mutable state; read-then-write without `select_for_update` or an equivalent. Maps to #3.
- **Insecure object references.** Every route that takes an object id checks the requester's right to that object in the service layer, with one test per route that tries someone else's id. Maps to #6 and #43.
- **Password and credential handling through one approved helper.** Detect: grep for `hashlib|md5|sha1|sha256` near `password`; credentials in source or logs; ad-hoc comparisons. Maps to NEW: Security primitives come from one vetted helper.
- **Config values validated.** Settings and env values are checked for type and range at startup; generated config passes a schema. Detect: `os.environ[...]`/`getenv` reads with no validation; config files with no schema test. Maps to NEW: Config is validated.
- **I/O in loops.** Queries, file reads or HTTP calls inside loops; query-count ceilings at 10 and 500 rows. Maps to #13.
- **Naming drift.** The same concept under different identifiers or labels in the change. Detect: a glossary or label table compared with new identifiers and UI strings. Maps to #23.
- **Formatting and style churn mixed with logic.** Detect: compare `git diff --stat` with `git diff -w --stat`; hunks that only change quotes or whitespace; a formatter or linter not run in CI. Maps to NEW: Diff traces to the ask/plan.
- **Repo idioms.** New code uses the project's existing helpers (money formatter, date formatter, DB access pattern, error type) rather than a generic re-implementation. Detect: new functions duplicating an existing helper's job. Maps to NEW: Follow local idioms (related to #23).
- **Non-trivial control flow has tests.** Detect: branch coverage of new code; new branches with no test. Maps to #32.

## Over-engineering signals (if relevant)
- "Unused/redundant code" is higher in AI PRs. Detect with dead-code tools (`vulture`, `ts-prune`, eslint `no-unused-vars`) and unreferenced functions or files.

## Process lessons for a non-coder directing AI
- Give the agent the business rules, configuration schemas and architectural constraints, as "repo-specific instruction capsules".
- Enforce style with CI formatters and linters (policy-as-code) instead of review.
- Require tests for non-trivial control flow. Mandate nullability and type assertions. Standardise exception handling. Prompt explicitly for guardrails.
- Centralise credential handling, block ad-hoc password code, and run SAST and security linters automatically.
- Give guidelines for batching I/O and choosing data structures.
- Use an AI-aware PR checklist:
  - Are error paths covered?
  - Are the concurrency primitives correct?
  - Are config values validated?
  - Are passwords handled via the approved helper?
- The vendor's own recommendation: use an AI review tool such as CodeRabbit.

## Quotes
- "humans and AI make the same kinds of mistakes. AI just makes many of them more often"
- "AI-generated code often omits null checks, early returns, guardrails, and comprehensive exception logic"

## Caveats
- Vendor marketing for a review product. Its numbers can't be checked from this text.
- Its finding that AI omits guardrails conflicts with Ahmad's claim that AI adds defensive code for impossible cases. Its finding that AI neglects efficiency (8x excessive I/O) conflicts with Ahmad's claim that AI adds premature optimisation (stop-ai-over-engineering-simple-problems.md).
- Open-source PRs only; no business-app data.
