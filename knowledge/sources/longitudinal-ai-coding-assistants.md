# The Impact of AI Coding Assistants on Software Engineering: A Longitudinal Study
- **Source:** arXiv:2605.23135v1 [cs.SE], 22 May 2026. Annie Vella and Kelly Blincoe, University of Auckland. Ethics approval UAHPEC27902. Partly supported by the first author's employer, Westpac New Zealand.
- **Type:** preprint
- **Evidence strength:** moderate.
  - For: a real longitudinal design with professional engineers, n=158/101 and a matched cohort of 95, mixed methods and Holm-corrected tests.
  - Against: everything is self-reported perception. There's survivor bias (current users only), 85% of the sample are men, 41% are in New Zealand, and one person did all the coding.
  - The data comes from Oct 2024 and Apr 2025, before today's agentic tools.

## Claims
**Sample**
- Q1 (Oct 2024): 224 responses, 158 eligible (71%).
- Q2 (Apr 2025): 111 responses, 101 eligible (91%).
- Matched cohort: 95 (60% of Q1). Attrition was not systematic (all p > 0.05, Cramér's V ≤ 0.23).

**Tools and attitudes**
- 37 distinct tools mentioned.
- Copilot and ChatGPT were each used by 70% at Q1 and 58% at Q2. Cursor rose from 16% to 29%.
- Tools per participant rose from 1.9 to 2.9, and 82% of matched participants changed their tool mix.
- Daily use: 57% at Q1, 61% at Q2.
- Quality was the top concern but fell from 44% to 36%. Maintainability as the top concern rose from 3% to 19%; it was the only significant change in ranking (n=89, p=0.003).

**Where the time goes**
- Writing code: 82% reported less time by Q2 (80% at Q1) and 2% more. Mean 2.10 at Q1, 1.93 at Q2.
- 69% reported less time overall across the six tasks.
- Reviewing was the only task above neutral (3.03 at Q1, 3.15 at Q2). Testing trended up but stayed below neutral.
- No single task changed significantly within participants (n=88). The balance between verification and creation did shift toward verification: 0.26 to 0.53, p_adj=0.006, r_rb=0.39.
- Only 8% both reduced writing and increased reviewing; 81% already wrote less at baseline.
- Transitions: testing 42% more, reviewing 40% more, writing 30% less.
- The creation and verification groupings have low internal consistency (α 0.40–0.49 and 0.56–0.57).

**Productivity**
- 84% reported improvement at both time points (M=4.08 at Q1, 4.03 at Q2). 77% gave identical ratings both times, and nobody turned negative.
- At Q2, productivity differed by primary concern (χ²=18.34, p=0.005): those worried about dependency reported the highest gains, those worried about quality the lowest.

**Developer experience**
- At Q1: 66% reported improved cognitive load, 62% improved feedback loops, 53% improved flow.
- Over time, only feedback loops improved significantly (3.73 to 3.95, p_adj=0.038). Cognitive load (3.74 to 3.60) and flow (3.54 to 3.36) declined, not significantly.
- The share reporting worse experience on at least one dimension rose from 14% to 27%.
  - Only 37% of the Positive cohort stayed positive.
  - Nobody in the Negative cohort recovered to Positive.
  - Flow was the issue for 54% of the Negative cohort at Q1 and 76% at Q2.
- Changes in developer experience didn't correlate with changes in productivity (smallest p_adj=0.313).

**Cited background**
- Stack Overflow 2025: 60% view AI tools favourably, down from over 70%. More developers distrust AI accuracy than trust it, and a majority are frustrated by solutions that are "almost right, but not quite".

**Proposed constructs**
- "Supervisory engineering work": directing, evaluating and correcting AI output.
- A "productivity-experience paradox".

## What humans catch that AI misses (per this source)
Practices participants described:
- Spotting when the model "has lost the thread" and halting it.
- AI referencing methods that no longer exist even after the version was specified (P26), and getting YAML templates "completely wrong" (P129).
- Not leaving in any code they don't understand or wouldn't have written themselves; not trusting AI on strategic or critical code.
- Seeing juniors chase "inappropriate solutions to the wrong problems much further" with AI.
- Reviewers trust the author less when they know the author leans heavily on AI.
- Keeping control of the overall architecture.

## Checks for the reviewer
- **APIs and versions.** Every library call exists, and isn't deprecated, in the version pinned in the lock file. Detect: a type check or import-resolve against the installed lock; tests run with deprecation warnings as errors. Maps to NEW: APIs exist in the pinned version.
- **Generated config validated.** YAML, JSON or TOML the agent wrote or changed passes a schema or the tool's own validator (e.g., `docker compose config`, CI linters, a settings-load test). Maps to NEW: Config is validated.
- **Explainability of risky code.** For money, saving data, concurrency and permissions, the reviewer writes a plain-language account of what the code does. Any part it can't explain from the code alone is a finding. Maps to #38.
- **Small units.** Flag changes that mix several concerns or modules in one diff; ask for them to be split. Maps to NEW: A change too big to verify is unverified.
- **Perceived vs. measured.** Judge passes by escapes and battery results, not by how productive the session felt. Maps to #30.

## Over-engineering signals (if relevant)
- Not discussed directly. The rise of maintainability as a concern (3% to 19%) suggests AI optimises for "works now" over "maintains later"; that reading is the authors' speculation.

## Process lessons for a non-coder directing AI
- Supervisory work is real work: directing, evaluating, correcting. Time saved on writing moves into it; it isn't free.
- Break work into smaller, specific modules and tie them together at the end, to reduce drift and hallucination.
- Be precise in prompts. A vague request failed where a specific one worked: "Use a react reference to track the width..."
- Corroborate AI answers elsewhere before relying on them. Stop the agent once it has lost the thread.
- Watch for the learning short-circuit: "you get a working solution, but not understanding why."

## Quotes
- "Identifying when the LLM has lost the thread of the problem and halting it is essential"
- "I almost never let it write production code, or at least never leave in code that I don't understand"

## Caveats
- Perceptions, not measured output. The 84% means 84% of continuing users.
- The tools were from late 2024 to early 2025, before agentic tools like current Claude Code.
- The per-task changes weren't significant; only the balance shift was.
- The authors used Claude Code to help write their R analysis scripts.
