# Stop Overengineering: How to Write Clean Code That Actually Ships
- **Source:** DEV Community, TheBitForge (founder of a software and AI product agency). Posted Jan 10, edited Aug 20; the year isn't shown, and the author joined Oct 23, 2025, so probably 2026. https://dev.to/thebitforge/stop-overengineering-how-to-write-clean-code-that-actually-ships-18ni
- **Type:** opinion/essay
- **Evidence strength:** anecdotal. Personal war stories with no data. It isn't about AI at all; it's about human over-engineering.

## Claims
All from the author's experience or asserted without evidence:
- **CSV export.** The team built an `ExportStrategyFactory` with an `IExportStrategy` interface, a config mapping file types to strategies, and a custom streaming framework, when the largest customer had "maybe fifty thousand rows". It took three weeks. In two years nobody asked for anything but CSV; when PDF was finally needed, they had to hack around the abstraction.
- **Bakery app.** Seven services, each with its own database and pipeline, linked by a message queue. Nine months of work; the bakery never opened. A competitor shipped in three weeks.
- **Stripe integration.** About 100 lines of integration code inside about 500 lines of payment-gateway abstraction. No second processor was ever added in three years, and the abstraction didn't help with the one change that came (subscription pausing).
- **CRM `Entity` base class.** Shared by Companies, Contacts, Deals and Tasks. It grew fields that applied to only some types, type checks to skip validation, and UI special cases. It was ripped out and each type got its own code.
- **Email.** A "send an email" call passed through seven layers (EmailService → EmailProvider → EmailClient → EmailAdapter → MessageSender → TransportLayer → API). Finding a delivery failure took hours.
- **Data first.** Two weeks went into designing services and queues before anyone looked at the data. 90% of records turned out to be one simple type, with 10% needing special handling.
- **Email in the request handler.** Sent directly with try/catch and logging, then retried by hand. Over six months, tens of thousands of emails went out and "maybe a handful" failed.
- **Rule of Three.** Don't abstract until there are three concrete cases. "Duplication is better than the wrong abstraction." DRY means duplicated knowledge, not code that merely looks alike.
- **Review by criticality.** Heavy review for critical-path code, light review for internal tools, none for prototypes. The author claims this moved faster "without actually increasing our bug rate" (unmeasured).
- Twitter started as a Rails monolith, Facebook in PHP, Instagram as a Django app on "a handful of servers" when bought "for a billion dollars". Stated as fact without sources.
- Splitting a ten-person team into microservices "will slow them down by a factor of three". No evidence.
- Solo developers: "Don't write tests unless something keeps breaking"; keep a monolith; skip abstractions until code repeats three times.
- 90% of users of one feature wanted one button rather than the configurable power-user design.
- An authentication refactor with a feature flag and side-by-side versions took three weeks instead of three days, with no outage.
- Justified abstraction: real repetition of the same concept (a Validator built after the pattern appeared "a dozen times"); hiding complexity that's inherent (a legacy SOAP API adapter); or two real implementations that exist now. Even then, build both directly first, then extract.

## What humans catch that AI misses (per this source)
Framed as what experienced developers catch, not AI:
- Abstractions built on surface similarity that hide different concepts (registration form vs. profile form).
- Layers that only forward a call.
- Which code is critical (money, auth) and which is throwaway.
- Copying big-company architecture with none of the big-company problems.

## Checks for the reviewer
- **Pass-through layers.** A method or class whose body only calls one other function with the same arguments, or returns another object's result unchanged. Detect: AST, function bodies that are a single forwarding call; call chains of three or more hops to reach the real I/O. Maps to NEW: Layers that only forward.
- **An abstraction with one implementation.** An interface, base class or factory with a single concrete type. Detect: count implementers or subclasses. Maps to NEW: Speculative generality.
- **The wrong shared base.** A base class or generic component full of `isinstance`/`type ==`/`kind ==` branches, fields that are null for most subtypes, or validation skipped per type. Detect: type switches inside shared classes; nullable columns used by one subtype only. Maps to NEW: Speculative generality.
- **Per-caller flags.** A generic builder or helper whose boolean or option parameters are each used by exactly one caller. Detect: count call sites per option. Maps to NEW: Options nobody uses.
- **Optimisation without data.** Streaming, caching or queues added without a stated data size. Compare the design against the real row counts. Maps to NEW: Optimization needs a measurement, and #13 (test at real size, both ways).
- **State that must not live in memory.** Module-level mutable dicts used as caches or sessions in a multi-user web process; hard-coded server URLs. Detect: grep for module-level `{}`/`[]` mutated in request handlers; literal `http://host` strings. Maps to #43 and #3.
- **Risk-tiered review.** Money and auth code gets the heaviest checks. Maps to #38 and #10.

## Over-engineering signals (if relevant)
Each with a way to detect it:
- **Strategy factory for one format.** Detect: factory or registry with one entry.
- **A configuration system for values nobody changes.** Detect: config keys with one value across all environments.
- **Microservices or multiple deployables for a small user base or team.** Detect: count services, databases and queues against the number of users and developers.
- **A custom framework instead of the standard one.** Detect: in-house routing, ORM or DI layers in an app already using Django, Rails or React.
- **More test and abstraction code than feature code for a simple feature.** Detect: lines in the abstraction vs. lines in the concrete integration (500 vs. 100 here).
- **Generic base classes with type-specific special cases.** Detect: see "The wrong shared base" above.

## Process lessons for a non-coder directing AI
- Start from the data: what comes in, goes out and is stored. Then the code.
- Make it work, then make it right, then make it fast, and optimise only measured bottlenecks.
- Build the first and second real implementations directly; extract an abstraction only once they exist.
- Refactor incrementally after shipping, behind a feature flag, with tests on the parts that change.
- Spend review effort by risk: heavy on money and auth, light on internal tools.

## Quotes
- "Duplication is better than the wrong abstraction."
- "DRY is about eliminating duplication of knowledge, not duplication of code."

## Caveats
- Written about human developers chasing startup speed, not AI.
- Several of its shortcuts conflict with Dev Instincts and the AI-specific sources:
  - "no tests unless something keeps breaking", no review for prototypes, and "ugly code nobody touches is fine" all assume a human who knows the code. With an AI agent editing broadly, Borg et al. (code-for-machines-codehealth.md) show unhealthy code breaks more often under AI edits;
  - sending email in the request handler and logging failures for manual retry conflicts with #1 and #18 (a failure the user never sees);
  - skipping tests runs against #32.
- Use its over-engineering smells, but not its "skip verification" advice.
