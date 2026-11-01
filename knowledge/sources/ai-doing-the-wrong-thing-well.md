# AI can be a great help in doing the wrong thing well
- **Source:** The Monospace Mentor blog, Jochen Lillich, 29 August 2026, https://monospacementor.com/knowhow/ai-overengineering/
- **Type:** practitioner article
- **Evidence strength:** anecdotal — one first-hand episode on a side project. The author sells DevOps courses and mentoring; no review-tool conflict.

## Claims
- On his side project Greenhouse, after he shipped a Twitch integration, the coding agent proposed a "resilience" follow-up: a durable EventSub subscription ownership record, a cleanup tombstone, operation fencing, and migration/backfill of connections already deployed.
- He didn't understand the proposal, trusted it and approved it, and it cost a day.
- The first implementation took hours; an isolated agent review judged it too flawed to salvage.
- His second attempt split the task into smaller chunks. It looked like success: lots of new code and tests covering every conceivable situation, including recovery for "Twitch issued a token but the app couldn't store it". That was far more complexity than a simple interactive site needs.
- Asked for a critical review of everyday usefulness against maintenance burden, the agent answered, in effect, "no".
- Asked where it went wrong, the LLM said its own distributed-systems vocabulary had pushed it toward protocol optimizations. It knew the app wasn't safety-critical but didn't let that constrain the design.
- His lesson: reviewing results after the agent finishes isn't enough. Understand what it intends to do before any code is written, even if that means admitting you don't understand.

## What humans catch that AI misses (per this source)
- Proportionality: a simple site doesn't need distributed-systems machinery.
- A plan you can't explain is a red flag, not a reason to trust it.

## Checks for the reviewer
- Plan gate: before any code, the agent restates its goal in words the developer can explain back. Detect: scan plan, ticket and commit text for terms like tombstone, fencing, ownership record, backfill, saga, outbox, distributed lock, leader election, eventual consistency in a single-server or single-PC app, and require a plain-words justification for each. → NEW: Plan in plain words before code.
- Scope vs. size: new tables, migrations or backfills in a "hardening"/"resilience" ticket. Detect: `git diff --stat` on migrations and models; lines added vs. the user-visible change the ticket names. → NEW: Complexity must be earned.
- Recovery paths for unlikely states: handlers for failure combinations nobody reported and the app's criticality doesn't call for. Detect: new branches or functions named recover/reconcile/repair/retry/fallback with no linked bug or requirement; ask what user-visible harm each prevents. → NEW: Defensive code only for reachable, costly states.
- The green-suite illusion: many new tests on an over-scoped design prove it was built, not that it was needed. → #32.
- A cost/benefit review for any change over a size threshold, asked of an independent reviewer: "does the everyday usefulness justify the maintenance burden?" → #31.

## Over-engineering signals (if relevant)
- Distributed-systems vocabulary in a small app's plan. Detect: grep plan and commit messages.
- A migration or backfill attached to a feature shipped days earlier.
- Retry/recovery code for third-party failures that don't put the user's data at risk.
- Splitting an over-scoped task into chunks yields more code, not less.

## Process lessons for a non-coder directing AI
- Understand and agree the plan before code. Say so when you don't understand it.
- State the app's criticality up front and make the agent design to it (e.g., "not safety-critical; a failed connect can be redone by hand").
- After a failed first attempt, question the goal, not just the method. Smaller chunks don't fix a wrong goal.
- Ask the agent directly whether the change is worth its maintenance burden; it may answer honestly.

## Quotes
- "it was building a castle where I needed a house. I could not read the blueprint well enough to stop it."
- "There is nothing so useless as doing efficiently that which should not be done at all." (Drucker, quoted by the author)

## Caveats
- One episode, one app, self-reported.
- Tension with this catalogue: #1, #8 and #15 want failure paths handled, and "token issued but not stored" is that class of failure. The test is whether the failure leaves bad data or a stuck user in *this* app. If it does, the handling is a real instinct, not over-engineering.
- The middle paragraphs are OCR-jumbled (lines interleaved). The summary follows the evident reading order.
