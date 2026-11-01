# Tired of AI Over-Engineering Your Code? This Plugin Teaches It to Write Like a Seasoned, Minimalist Dev
- **Source:** Medium, "AI Engineering" account, 14 Jun 2026 ("Original by winkrun"). Project: https://github.com/DietrichGebert/ponytail. No Medium URL in the text.
- **Type:** practitioner article (a promotional write-up of an open-source plugin)
- **Evidence strength:** weak — the benchmark was run by the plugin's own team, is small (5 tasks × 10 runs × 3 models, medians), used older models, and measured size, cost and speed, not correctness or security.

## Claims
- AI agents bloat simple tasks: asked for a date picker, they install a library (flatpickr), wrap it in a component, add styling and debate time zones, when `<input type="date">` does the job.
- Ponytail makes the agent go through six steps in order before coding: (1) is code needed at all (YAGNI)? (2) is it in the standard library? (3) is it a native platform feature? (4) is it in a dependency already installed? (5) can it be one line? (6) otherwise write the minimum.
- Security validation, data persistence and accessibility are never cut. Asserted.
- The team's benchmark: email validation, debouncing, CSV sum, countdown timer and rate limiter, each run 10 times on GPT-4o, Claude 3 Haiku and Claude 3 Sonnet, against an unconstrained agent and the "Caveman" plugin, taking medians. Against unconstrained agents: lines of code −80% to −94%, API cost −47% to −77%, runtime 3x–6x faster. Against Caveman the improvement is "significant" (no numbers given).
- It leaves a comment noting the shortcut and how to upgrade it later.
- Supports Claude Code, Codex, Cursor, Windsurf, OpenCode and Pi Agent. `/ponytail-review` checks the current diff for removable code.

## What humans catch that AI misses (per this source)
- That the platform or standard library already does it.
- That a new dependency isn't needed.

## Checks for the reviewer
- A new dependency for something native or already installed. Detect: diff `package.json`, `requirements*.txt` and lockfiles. For each added package, look for a stdlib, browser or framework equivalent and for existing dependencies that cover it (date pickers, debounce, UUID, CSV, email validation, deep clone). → NEW: Use what's already there.
- A hand-rolled utility the stdlib or framework provides. Detect: new functions named like debounce, throttle, validate_email, parse_csv, rate_limit, retry, deep_copy, format_date; search for equivalents. → NEW: Use what's already there.
- A removable-code pass on every diff: list code whose deletion breaks no test or stated requirement. → NEW: Every abstraction earns its place.
- Minimal mustn't strip guards: validation, persistence and accessibility stay. → #9, #1, #16.

## Over-engineering signals (if relevant)
- A library plus a wrapper plus styling for a native control. Detect: new dependency plus a new component wrapping it.
- A custom cache class (the FAQ jokes about a 120-line one). Detect: new classes named *Cache/*Manager with no measured need.

## Process lessons for a non-coder directing AI
- Put the six-step ladder in the build prompt or a rule file, and make the agent justify each new dependency and file.
- Ask for a review of the diff for removable code before accepting it.

## Quotes
- "Do you actually need to write any code for this feature at all?"
- "core requirements like security validation, data persistence, and accessibility are never cut"

## Caveats
- A self-benchmark by the tool's authors, on toy tasks and old models, with no correctness, security or maintainability measures.
- Native controls aren't always equivalent (display format, browser support). A one-line native date input can clash with #23 (one date format everywhere).
- Promotional tone. The FAQ line that code you don't write has zero bugs is a joke, not evidence.
- The instinct reviewer may not install new tools (its rule 5). The ladder can be used as prompt text without the plugin.
