# AI Will Not Remove Overengineering. It Will Accelerate It
- **Source:** Anton Minin Baranovskii, personal site (contact hi@antonmb.com), 8/3/2026. Part 6 of 8 in the series "Systems that survive contact with reality". URL not shown.
- **Type:** opinion/essay
- **Evidence strength:** weak. Reasoned argument with no data. The Stripe figure is "according to public descriptions", with no citation.

## Claims
- Models reproduce big-company solutions because those dominate open source and blogs. Asked to "write authentication", they produce layers, interfaces and handling for scenarios you'll never have (asserted).
- Complexity used to cost time: five abstraction layers took about a week, and around day three people doubted they were needed. That cost acted as a brake. Now the same layers take a minute (asserted).
- Most of the cost of complexity falls on maintenance, not writing, so generated complexity is technical debt taken on instantly without a decision (asserted).
- A model asked to simplify spots what is redundant more accurately than it invents what is needed (asserted, from experience).
- Stripe runs "more than a thousand pull requests a week" through AI. Tasks are narrowly bounded, the agent's tools are picked by hand, and every result is reviewed ("according to public descriptions", uncited).
- Google, Shopify and Airbnb embed agents in existing processes (GitHub, Slack, Linear) and surround them with checks. None takes generated output as is (asserted).
- Incentives favor complexity: complex reads as professional, simple as unfinished (asserted).

## What humans catch that AI misses (per this source)
- That a 500-line generated module contains parts the task doesn't need. "Nobody is going to work out which parts are unnecessary."
- A mismatch between the architecture and the real scale (microservices for a landing page, Kubernetes for ten users).
- The day-three doubt, which now has to be a deliberate step.

## Checks for the reviewer
- **Deletion pass.** For each new module, remove one layer, function or option at a time and re-run the tests and the end-to-end walk. If behavior is unchanged, the code is either unneeded or untested; report which. A fresh session can also be asked: "Remove everything it can keep working without; list what can be thrown away." `NEW: patch bloat` (also #39 when deletion leaves tests green)
- **Infrastructure fits the stated scale.** Compare new infrastructure in the diff (queues, caches, extra services, container orchestration, Redis, message brokers, sharding) with the scale written in the project docs. Flag anything without a stated need. `NEW: speculative abstraction`
- **Change size.** Flag agent changes much larger than one bounded change: many files or hundreds of lines for one request. `NEW: scope creep`

## Over-engineering signals (if relevant)
- Layered authentication with interfaces and handlers for scenarios the app will never have. Detect interfaces with one implementation and handlers that are never reached.
- An architecture built for a million requests on modest traffic. Detect infrastructure with no load requirement in the docs.
- A whole generated module dropped in at once. Detect a large single-commit addition with no prior smaller version.

## Process lessons for a non-coder directing AI
- Use AI as an editor, not a generator. The author writes ~30 lines himself and then asks AI to cut. A non-coder can't do the first step, but can still run a separate "simplify and delete" session over generated code.
- Put constraints in the prompt, e.g. "The simplest solution that works. No frameworks, no layers of abstraction. SQLite, one file."
- Give the project context: "I have 100 users and a ten dollar server" changes the answer more than rewording does. Put it in the project's CLAUDE.md.
- Frame agent tasks narrowly (a bounded change, not "build a feature") and review every result.

## Quotes
- "It is not about the quality of the generation: the code can be excellent. It is that the code became too cheap."
- "When generating, there is no reference point, so the model substitutes the average one."

## Caveats
- No measurements. The company examples are secondhand.
- "Write it yourself first" assumes the developer codes, which doesn't hold for this developer.
- The page's related-posts list (other articles by the author) was ignored.
