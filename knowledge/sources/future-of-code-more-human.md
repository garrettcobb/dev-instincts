# Why The Future of Code Is More Human Than Ever
- **Source:** DEV Community, Leena Malhotra, posted Oct 10, 2025. https://dev.to/leena_malhotra/why-the-future-of-code-is-more-human-than-ever-13ij (OCR split the ID).
- **Type:** opinion/essay
- **Evidence strength:** anecdotal. One personal anecdote. It promotes Crompt AI four times (including its "AI Tutor", "Document Summarizer" and "Sentiment Analyzer") with no disclosure visible.

## Claims
- Claude Sonnet 4.5 built her a full-stack authentication system (JWT, password hashing, email verification, rate limiting) in ten minutes. Five years earlier it would have taken her three days (self-reported).
- She then spent two hours debugging why users couldn't reset passwords. The cause was a question she hadn't asked about how the email service handled temporary tokens. She says the code was "perfect".
- The bottleneck is shifting from writing code to understanding problems (asserted).
- Juniors can't tell whether a generated solution fits their context, or when it is "technically correct but strategically wrong" (asserted).
- A junior with Claude Opus 4.1 "can write code that handles edge cases they've never personally encountered" (asserted).
- AI excels at local optimization (one function) and struggles with global, system-level effects (asserted).
- "AI can generate optimal code" (asserted).
- The author has coded for fifteen years (self-reported).

## What humans catch that AI misses (per this source)
- Assumptions about how an external service behaves (token lifetime, one-time use, how the email service handles temporary tokens).
- Second- and third-order effects of a local change on the whole system.
- Whether a technically correct solution is the right one for the context.

## Checks for the reviewer
- **External-service contract written down.** For each integration (email, payments, identity provider, file storage), the assumptions about the provider's behavior (token expiry, single use, rate limits, retries, time zones, error codes) sit next to the integration and are covered by a test against a faithful fake or a sandbox. `NEW: assumptions traced to spec`. Expiry-related assumptions also map to #11 and #21.
- **End-to-end walk of each user flow.** Run the complete flow, including the email or link step (sign up, reset password, use the link, use it twice, use it after expiry), not just the unit pieces. Maps to #33, #17 and #2 (link used twice).

## Over-engineering signals (if relevant)
- Not addressed.

## Process lessons for a non-coder directing AI
- Define the problem precisely before generating: context, constraints and edge cases, including how outside services behave.
- The human integrates and decides fit. The AI's code passing its own checks doesn't mean the feature works in your environment.
- The author suggests comparing several models' approaches to the same problem. That is her own suggestion and is tied to the product she promotes.

## Quotes
- "The AI wrote flawless code. I wrote the wrong requirements."

## Caveats
- Undisclosed product promotion. The model names date it to late 2025.
- Her own anecdote undercuts "flawless": the feature didn't work end to end. Calling the code perfect because the requirement was missing lets the generated code off too lightly.
- Its claims that AI code is "production-ready" and "optimal", and that juniors with AI handle unseen edge cases, conflict with:
  - ai-made-knowing-how-to-code-more-important.md (an invented rule passed all tests);
  - humans-missing-from-coding-agent-research.md (over 50% of test-passing patches differ functionally; about a third on edge cases; less-experienced developers struggle most to review).
