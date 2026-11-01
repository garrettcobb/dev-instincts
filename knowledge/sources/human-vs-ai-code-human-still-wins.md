# Human vs AI Code: Why Human-Written Code Still Wins
- **Source:** Medium, Or Ben Shmueli. No publish date in the capture. https://medium.com/@orbens/human-vs-ai-code-why-human-written-code-still-wins-24ec092f97f4
- **Type:** practitioner article
- **Evidence strength:** anecdotal. Five one-line prompts, model and version not named, one output each, and the "human" versions were written by the author after seeing the AI output.

## Claims
- Email validation (C#):
  - AI: wraps `MailAddress` in a catch-all and returns false, with no null/whitespace check.
  - "Human": adds `IsNullOrWhiteSpace`, catches only `FormatException`, compares with `OrdinalIgnoreCase`.
- "Print price in dollars":
  - AI: concatenates `"Price: " + price + " USD"`.
  - "Human": uses `{price:C2}`, which the author calls culture-aware.
- Even numbers:
  - AI: a loop over `int[]` into a `List`.
  - "Human": LINQ over `IEnumerable`, with null input returning an empty sequence.
- Sorting names:
  - AI: `names.Sort()` in place.
  - "Human": `OrderBy` with `StringComparer.OrdinalIgnoreCase` into a new list ("culture-invariant", doesn't modify the original).
- Thread-safe counter:
  - AI: a public `int Value` with `Value++`. This is correct as a finding: `++` isn't atomic and races.
  - "Human": a private field with `Interlocked.Increment`.
- General claim: experienced developers add the safety checks and input handling that AI leaves out (asserted from these examples).

## What humans catch that AI misses (per this source)
- Null or blank input reaching a parser.
- Catch-all exception handling that hides the reason for a failure.
- Non-atomic updates to shared state.
- Formatting and sorting that depend on the machine's culture.
- Mutating the caller's collection in place.

## Checks for the reviewer
- **Swallowed exceptions.** Grep `catch\s*\{`, `catch\s*\(Exception`, `except:` and `except Exception` where the handler returns false/None/empty, or passes. A failure turned into a quiet default is a hidden bug. Maps to #25 (and #18 if the UI then shows success).
- **Non-atomic read-modify-write on shared state.** `x++` or `x += n` on fields, statics or module globals touched by concurrent requests or threads, and ORM `obj.n = obj.n + 1; save()` without `F()`, a row lock or a transaction. Maps to #3.
- **Money formatted by hand or by machine culture.** Grep `" USD"`, `"$" +`, `toFixed(2)`, `:C` / `ToString("C")` with no explicit culture. All money display goes through one formatter with a fixed currency. Maps to #10 and #23.
- **String sort and compare without explicit rules.** Sorting or comparing user-entered names with no explicit comparer or collation. Maps to #23.
- **Null in, empty out.** `?? Enumerable.Empty`, `or []` or `|| []` on internal APIs that turn a caller bug into "no results". Maps to #25.

## Over-engineering signals (if relevant)
- Not the article's topic. Its "human" fixes add defensive code, which the Humans-are-Missing paper classes as a cause of patch bloat when it guards states that can't happen. See Caveats.

## Process lessons for a non-coder directing AI
- One-line prompts get generic code. State the context the code runs in: concurrent requests, the currency and locale, where the input comes from, whether nulls can arrive.

## Quotes
- "This code looks correct, but it's not thread-safe. Value++ is not atomic and can cause race conditions."

## Caveats
- Several "human" fixes are themselves questionable:
  - `{price:C2}` uses the current culture's currency symbol, so "print price in dollars" prints a different currency on a non-US machine.
  - `?? Enumerable.Empty<int>()` silently hides a null-argument bug (against #25).
  - Case-insensitive email equality is a policy choice, not a fix.
- Cherry-picked, unnamed model, one run each. It shows typical gaps, not their frequency.
- It conflicts with humans-missing-from-coding-agent-research.md on whether extra null checks and validation are better or bloat. A likely reconciliation: validate at system boundaries (user input, files, network) and don't defend internal states that can't occur.
