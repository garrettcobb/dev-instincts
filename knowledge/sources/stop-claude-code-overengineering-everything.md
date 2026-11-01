# How To Stop Claude Code From Overengineering Everything
- **Source:** nathanonn.com, Nathan Onn (freelance web developer, writes "The Art of Vibe Coding" newsletter), Jul 18, 2025. https://www.nathanonn.com/how-to-stop-claude-code-from-overengineering-everything/
- **Type:** practitioner article
- **Evidence strength:** anecdotal. One feature in the author's own Next.js app. The key prompt text didn't survive capture (it was an image), the file counts are internally inconsistent, and the post sells a newsletter.

## Claims
- Examples of over-scoping: "Add email OTP login" becomes a "12-file authentication framework"; "Update the API route" spawns a middleware ecosystem; "Fix this type error" restructures half the app.
- For email OTP, Plan Mode proposed a tree:
  - `auth/providers` (OTPProvider, AbstractAuthProvider, AuthProviderFactory);
  - `strategies` (EmailOTPStrategy, BaseStrategy);
  - `services` (Token, Validation, Notification);
  - `middleware` (auth, session).
- He calls it "15 new files" with abstract base classes, strategy and factory patterns. The visible tree names about 10 files and the intro says 12, so the counts don't agree.
- The app already had NextAuth configured, email sending via Resend and simple session management.
- With his "surgical" prompt: 15 files became 3 and "1000+ lines" became 120, with "same functionality" and "90% less complexity". The complexity figure isn't measured.
- "Think harder" switches on extended thinking, 31,999 tokens instead of a default 4,000 ("8x"). This is an unsourced claim about mid-2025 Claude Code and may be out of date.
- The prompt's three working parts: "think harder"; "thoroughly examine similar areas" (look at existing code first); "minimal and necessary changes" as the main constraint. The full prompt and its four variants ("Pattern Detective", "Deletion First", "One-File Challenge", "Next.js Native") are missing from the capture.
- Claude pattern-matches to enterprise, academic and tutorial code and doesn't ask what's already in the app (asserted).
- "Less code = fewer bugs. Mathematical fact." (asserted). "You Ship 5x Faster" (asserted, no data).

## What humans catch that AI misses (per this source)
- The app already has the capability (auth library, mail sender, sessions), so a new framework is redundant.
- A small fix (a type error, one route) that touches far more than it should.
- Abstract base classes and factories for a single flow.

## Checks for the reviewer
- **Already in the stack.** For any new module, check the dependency manifest and the codebase for an existing capability doing the same job (auth, mail, sessions, HTTP client, dates, validation). Flag parallel implementations. `NEW: reuse before build`
- **New-folder smell.** New directories named `providers/`, `strategies/`, `factories/`, `services/` or `middleware/` created for one feature, or new `Abstract*` / `Base*` / `*Factory` files. `NEW: speculative abstraction`
- **Fix proportional to the bug.** A fix for a type error or one route that touches many files or restructures modules gets flagged. Compare `git diff --stat` with the stated task. `NEW: scope creep`
- **Follows existing patterns.** New code solves its problem the way the codebase already solves similar ones (the "Pattern Detective" idea). Grep for the nearest similar feature and compare structure. Maps to #23 (one way of doing the same thing), extended from labels to code structure.
- **Count it.** Record files changed and lines added per request, as the author recommends. `NEW: patch bloat`

## Over-engineering signals (if relevant)
- AbstractAuthProvider + AuthProviderFactory + BaseStrategy for one OTP method. Detect a base or factory with one concrete user.
- A middleware ecosystem for one route update. Detect new middleware files in a route-change diff.
- Abstractions added "for future auth methods" with no planned second method. Detect extension points nothing extends.

## Process lessons for a non-coder directing AI
- Let the agent plan first (Plan Mode), then reject the first plan ("No, keep planning") and require it to:
  - examine existing similar code;
  - propose "minimal and necessary changes".
- Ask "what if this could be done in just one file?" as a constraint test.
- Track files changed and lines added for every feature, and compare plans.
- Iterate if the first pass is still too complex. But don't over-restrict: if the foundation really is missing, build it, minimally and in the existing style.

## Quotes
- "Every abstraction is complexity you own forever."
- "'Add email OTP login' becomes a 12-file authentication framework."

## Caveats
- n=1, unverified line counts, inconsistent file counts (12 / 15 / ~10 visible), and the core prompt is missing from the capture.
- Its claims about specific Claude Code features are tied to mid-2025 versions. Check current behavior before relying on them.
- Treats "less code" as always better, which conflicts with sources that praise added input checks (human-vs-ai-code-human-still-wins.md).
