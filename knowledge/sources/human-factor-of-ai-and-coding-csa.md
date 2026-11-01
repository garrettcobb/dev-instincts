# The Human Factor of AI and Coding

> Two copies of this article were in the collection (a PDF print and an .mhtml save); this note covers both.
- **Source:** Cloud Security Alliance (CSA) blog, Industry Insights. Eyal Estrin, cloud and information security architect. Published 08/10/2026. Page title: "AI and Coding: The Human Factor | CSA". No URL in the text.
- **Type:** practitioner article
- **Evidence strength:** anecdotal. Expert opinion walked through the SDLC phases, with no data or cases.

## Claims
All asserted without evidence:
- Phase verdicts:
  - Planning: humans do better.
  - Requirements: humans.
  - Design: humans.
  - Coding: a tie. AI writes boilerplate; humans verify logic and maintainability.
  - Testing: AI does better (repetitive unit tests, mocks, regression scripts).
  - Deployment: AI does better (anomaly detection, automatic rollback past preset thresholds).
  - Maintenance: humans.
- AI can't predict how an architecture choice will affect cloud spend or team topology "two years down the road".
- "Engineers must review every line of AI code" for subtle logic flaws and security vulnerabilities.
- AI works on probabilistic patterns rather than structural reasoning. That leaves it blind to system architecture and prone to generating security risks.

## What humans catch that AI misses (per this source)
- The gap between what a client says and what they need. Hidden assumptions. Feature requests that contradict each other.
- Cascading failures and systemic bottlenecks in an architecture.
- Subtle logic flaws and security holes in generated code.
- Exploratory and boundary testing: the "creative, chaotic" ways real users break software. Complex integration scenarios. Performance problems that aren't pass/fail.
- Refactoring an ageing system as a whole when business direction shifts.

## Checks for the reviewer
- **Each spec rule is enforced the same way on every path.** Detect: list each business rule in the governing spec and find every route that changes its field. Flag routes that skip the rule or enforce a different version. Maps to #6.
- **Hostile boundary inputs on every entry point.** Maps to #9.
- **The real job, end to end, as a scripted walk that includes the integration paths.** Maps to #33 and #17.
- **One failing dependency or view doesn't take the app down.** Maps to #19.
- **Spec gaps.** Flag requirements that don't say what happens with empty, duplicate, concurrent or late input, and ask the developer to decide. Maps to NEW: Unstated defaults are decisions.

## Over-engineering signals (if relevant)
- Not discussed.

## Process lessons for a non-coder directing AI
- Use AI for boilerplate, CRUD, syntax translation, first-draft schemas and test scaffolds.
- Keep requirements, design and acceptance decisions with a human.
- The role shifts from code writer to "AI orchestrator and system architect" with sharp auditing skills.

## Quotes
- "Humans figure out the creative, chaotic ways an actual user will break the software."

## Caveats
- Internally inconsistent: it gives exploratory and boundary testing to humans, then scores Testing for AI.
- The Testing verdict conflicts with DEV-INSTINCTS #32 (813 green tests still missed a crash, data loss and double-billing). It also conflicts with Alenezi (human-ai-collaboration-se-work.md) and Vella & Blincoe (longitudinal-ai-coding-assistants.md), where verification is the human bottleneck.
- "Review every line" isn't possible for a developer who doesn't read code; the reviewer agent has to stand in.
