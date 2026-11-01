# AI Coding vs Human Coding: A Detailed Analysis
- **Source:** Medium, Faisal Mahmood, Sep 2, 2025. https://medium.com/@faisal.mahmood106/ai-coding-vs-human-coding-a-detailed-analysis-d3fccb0f40d2
- **Type:** opinion/essay
- **Evidence strength:** anecdotal. No data, and the only example is hypothetical. The author's bio says digital marketer, contact at aidetector.pro, and the piece promotes CodeSpy.ai, an AI-code detector.

## Claims
All asserted without evidence:
- AI tools produce syntactically correct code "most of the time". They can still generate insecure code, miss performance bottlenecks, ignore project-specific requirements, and "hallucinate" functions or APIs that don't exist.
- Hypothetical example: AI writes password hashing with outdated methods, where a human would use bcrypt or Argon2.
- AI recombines known solutions and struggles with problems that aren't documented anywhere.
- Maintenance and debugging take "the majority" of a project's lifecycle. No figure is given.
- AI lacks project-wide context for debugging.
- Humans put structure, readability and maintainability first; AI may overlook them.
- CodeSpy.ai "detects whether code is AI-generated or human-written". No accuracy figure is given.

## What humans catch that AI misses (per this source)
- Outdated security primitives, such as weak password hashing.
- Calls to functions or APIs that don't exist.
- Edge cases a person knows from the domain or from past debugging.
- Performance bottlenecks.
- How today's change affects maintainability later.

## Checks for the reviewer
- **Password hashing goes through a vetted helper.** Detect: grep for `md5|sha1|sha256|hashlib|crypto.createHash` within a few lines of `password|passwd|pwd|secret`. Also flag any hand-written salt or hash code, and any password written to a log, a file or a plain-text column. Maps to NEW: Security primitives come from one vetted helper.
- **Every API the code calls exists in the pinned dependency version.** Detect: run the type checker or import resolution against the lock file (`mypy`/`pyright`, `tsc --noEmit`). Run the tests with deprecation warnings turned into errors (`python -W error::DeprecationWarning`). Maps to NEW: APIs exist in the pinned version.
- **Performance at real data size.** Maps to #13.

## Over-engineering signals (if relevant)
- Not discussed.

## Process lessons for a non-coder directing AI
- Use AI for boilerplate, CRUD, test scaffolds and docs. Keep human oversight on finance, healthcare and safety-critical code.

## Quotes
- "Without context, AI can “hallucinate” functions or APIs that don't exist."

## Caveats
- Generic and promotional. Only two examples are usable: the password hashing and the non-existent APIs.
- AI-detection tools say nothing about whether code is correct, so the CodeSpy.ai recommendation doesn't help review.
