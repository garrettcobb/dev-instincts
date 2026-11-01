# Human-AI Collaboration and the Transformation of Software Engineering Work
- **Source:** arXiv:2606.03394v1 [cs.SE], 02 Jun 2026 (the HTML page also shows "August 24, 2026"). Mamdouh Alenezi, Saudi Data and Artificial Intelligence Authority (SDAIA), Riyadh. https://arxiv.org/html/2606.03394v1
- **Type:** preprint
- **Evidence strength:** weak. A single-author interpretive synthesis with no new data. Its numbers come second-hand from cited studies, chiefly the AIDev archival preprint (Li, Zhang & Hassan). Its competency ratings and nine propositions are the author's judgments, not tested.

## Claims
**Cited from other studies, not the author's data**
- Peng et al.: developers with an AI pair programmer finished a standard task about 56% faster than a control group, with the largest gains for less-experienced participants.
- Vaithilingam et al.: programmers preferred AI help, but it didn't reliably improve completion time or success, and it often made generated code harder to understand, edit and debug.
- Barke et al.: AI use is bimodal. Acceleration when the goal is known; exploration when it isn't.
- Liang et al.: a survey of 410 developers found they often struggle to get output aligned with their requirements.
- Hamza et al.: a workshop with 22 professional engineers using ChatGPT for three hours.
- Treude et al.: a taxonomy of eleven developer–AI interaction types.
- AIDev:
  - 456,535 agent-authored PRs across 61,453 repositories and 47,303 developers, from five agents (OpenAI Codex, GitHub Copilot, Devin, Cursor, Claude Code);
  - one developer produced 164 agent-authored PRs in three days, against 176 human-authored PRs over the prior three years;
  - some agents close PRs "up to an order of magnitude faster" than humans;
  - agent PRs are less likely to be merged, especially for features and bug fixes, and change fewer structural aspects of the code (lower rates of cyclomatic-complexity change);
  - review is forming provider-aligned "closed loops", where an agent's output is reviewed mainly by a review bot from the same provider;
  - trusted security review remains "substantially rule-based".
- Abrahão et al.: pushed too far, AI turns into over-reliance, lost provenance, code and feature bloat, security exposure, technical debt and devalued craft.

**The author's own synthesis (asserted, framed as propositions)**
- Throughput is gated by verification capacity, not generation speed.
- The skills least replaceable by AI and most critical are critical judgment, systems thinking, trust calibration, and autonomy/accountability policy.
- Provider-aligned agent–reviewer loops raise short-term velocity but increase latent quality and security risk (Proposition P4).
- Over-reliance without foundational depth degrades diagnostic ability (P7).
- The text says nine propositions. In the OCR'd Table 8, only the P3 label is missing; nine proposition rows are present.

## What humans catch that AI misses (per this source)
- Plausible-but-wrong output: "critical evaluation", rated "very low" AI-substitutability.
- Whole-system and long-term effects of a change.
- Blind spots shared by an AI author and a same-provider AI reviewer.
- Ambiguous needs that must be turned into testable acceptance criteria.

## Checks for the reviewer
- **The reviewer is independent of the author, down to the provider.** The model or tool that reviews isn't the one that wrote the code, and ideally comes from a different provider. Detect: commit trailers (`Co-Authored-By`), PR bot configs, the agent settings. Maps to #31.
- **Every merged change has a verification record.** Tests run and their output captured. Detect: changes merged with no test run or report attached; the ratio of changes to verified changes. Maps to #26.
- **Requirements become acceptance tests.** Each requirement in the governing spec has a testable acceptance criterion and a test that names it. Detect: spec items with no linked test. Maps to #41 and #33.
- **Provenance.** Each commit records which agent or model wrote it and which plan or prompt it served. Detect: missing trailers or plan references in `git log`. Maps to #41.
- **Agent autonomy limits are written down and enforced.** For example, no unsupervised migrations, deletes, pushes or network calls. Detect: agent settings files with deny rules for destructive commands; flag a repo with none. Maps to NEW: Agent permissions written and enforced.
- **Change volume within review capacity.** Detect: diff size per change, and changes per day against changes reviewed. Maps to NEW: A change too big to verify is unverified.

## Over-engineering signals (if relevant)
- It lists "code and feature bloat" as a pathology (from Abrahão et al.) without detail.
- AIDev reports agent PRs are structurally simpler, with less cyclomatic-complexity change, not more complex.

## Process lessons for a non-coder directing AI
- Write prompts "like executable specifications with clear constraints and guardrails".
- Invest in verification capacity (tests, review tooling, reviewer time) so generation gains aren't lost to integration debt.
- Write an autonomy policy: when the agent may act, how its output is validated, and who answers for defects.
- Avoid a provider monoculture across the author agent and the reviewer agent.
- Calibrate trust: neither blind acceptance nor reflexive rejection.
- Keep enough foundational depth to step in when the tools fail.

## Quotes
- "as code becomes abundant, the durable value of the software engineer increasingly resides in intent specification, critical judgment, and accountable oversight"
- "trust is produced by the loop, not assumed of the generator"

## Caveats
- No primary data. The AIDev figures come from an archival preprint and may reflect early-adopter or novelty effects, as the author admits.
- The competency matrix ("very low" substitutability and so on) is the author's opinion.
- It cites both Peng (56% faster) and Vaithilingam (no reliable improvement) without resolving them.
- Two dates appear on the page.
