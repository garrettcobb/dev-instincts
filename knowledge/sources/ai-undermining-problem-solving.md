# Is AI Code Generation Undermining Developers' Problem-Solving Skills? (Review Article)
- **Source:** ICCK Journal of Software Engineering, Vol. 2 No. 1 (2026), pp. 1–10. Moomna Nazir (COMSATS University Islamabad, Sahiwal), Yasir Arif (Global Institute, Lahore). Submitted 2 Aug 2025, accepted 30 Oct 2025, published 27 Jan 2026. DOI 10.62762/JSE.2025.847963.
- **Type:** peer-reviewed
- **Evidence strength:** weak — a narrative review with no stated search method; the proposed framework is untested (the authors admit it); focus is students and junior developers. No funding, no declared conflicts.

## Claims
Mostly other studies' results as the review reports them:
- Peng et al.: developers with Copilot finished an HTTP-server task in 55.8% less time; success rate didn't differ significantly.
- Microsoft enterprise data: 73% of Copilot users said it speeds up tasks; 68% said it improved task quality (self-report).
- Students using ChatGPT/StarCoder completed more tasks but showed surface reasoning and less understanding and creativity than peers coding by hand.
- Students found correcting AI code in assessments much harder than correcting their own (Kohen-Vacs et al., 2025).
- Meta-analysis of 35 controlled studies (2020–2024): AI-assisted learners improved in task time and scores (SMD +0.86) but not in conceptual understanding (SMD +0.16, p ≈ 0.41; one occurrence is OCR-garbled as "p + 0.41").
- 2024 study: ChatGPT-assisted students used fewer self-initiated debugging strategies and accepted suggestions uncritically.
- 2025 quasi-experiment with 234 Java undergraduates: AI pair programming (GPT-3.5, Claude 3 Opus) raised motivation, cut anxiety and improved performance (p < .001); perceived collaboration was still highest with human pairs.
- 2025 study: developers who see AI as an "expert assistant" over-trust it, even with small logic errors or context mismatches; those who see it as a collaborator question it and intervene more.
- Asserted by the authors: junior developers are most at risk of accepting AI code without understanding it.
- Proposes Detect–Engage–Verify: AI for exploration; a human writes the core logic until a minimal working program runs; then AI for optimization, readability, edge cases and review. Not validated (the authors say long-term outcomes are untested and validation used self-reported student feedback).

## What humans catch that AI misses (per this source)
- Small logic errors and context mismatches that over-trusting users accept.
- Edge cases and behaviour checks, when the human has done the reasoning themselves.

## Checks for the reviewer
- Unexplained acceptance: an AI change in money, saving data, concurrency or permissions with no human-written spec or explanation behind it. Detect: changed files in those areas with no linked ADR, spec or plan line. → #38; NEW: Plan in plain words before code.
- Claims without proof: summaries that say "works" or "fixed" with no run behind them. → #26.
- Reviewer independence: the authoring agent's own review doesn't count. → #31.
- An edge-case pass as its own step after the code works (the "Verify" phase): ask for boundary tests at 0, max, max+1 and negative. → #9, #10.

## Over-engineering signals (if relevant)
- Not covered.

## Process lessons for a non-coder directing AI
- Treat AI as a collaborator to question, not an expert to defer to.
- Keep the core decisions human-owned. For a non-coder, that means writing down the domain rules; AI implements them, then a separate AI pass hunts edge cases.
- Require AI output to be tested, explained and critiqued before it's accepted.

## Quotes
- "developers who viewed AI as a partner in collaboration instead of as a decision-maker took a more critical approach"
- "AI can derive code, but human professionals need to verify, assess, and provide the necessary context."

## Caveats
- Secondary reporting; the cited numbers aren't checked against the original studies here.
- Aimed at learners. The "write the core logic yourself" step doesn't map directly to a developer who doesn't read code.
- Small, newer journal; two cited works are the second author's own unrelated defect-prediction papers.
- The 68% "improved quality" figure is self-reported perception. It doesn't directly contradict the measured defect and vulnerability findings of Mao et al. and Cotroneo et al. (same group), but it points the other way.
