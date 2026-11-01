# AI coding agents generate more code, but not more software
- **Source:** Ars Technica, Kyle Orland, Oct 9, 2026. https://arstechnica.com/ai/2026/10/ai-coding-agents-generate-more-code-but-not-more-software/ Reports a study by Fiona Chen and James Stratton (Harvard) that uses Jellyfish engineering-analytics data.
- **Type:** preprint (reported secondhand in a news article; the paper itself isn't in the text)
- **Evidence strength:** strong on scale and design, weaker on what it measures. 700+ firms, 700,000+ employees, 300M work events, 2021 to March 2026, difference-in-differences around each firm's adoption date. But it's a working paper relayed by a journalist, the data comes from a vendor (Jellyfish), and it measures throughput and process, not defects.

## Claims
- Agent adoption was identified from measured AI usage plus GitHub activity, separating assistants (autocomplete) from agents (write and submit code).
- After agent adoption, on average: +30% lines of code, +20% commits, +23% pull requests.
- Resolution rate for Jira issues and epics: no statistically significant change. No "compositional shift" in issue size or complexity.
- Review time (PR submitted to merged): +49% on average.
- Share of PRs with changes requested "nearly doubl[ed]". Comments per PR: +35%.
- Share of workers doing code review: +14%.
- No significant employment change attributable to AI (Jellyfish totals cross-checked with LinkedIn).
- By March 2026, 80% of firms used some AI code review. AI agents produced 23.3% of review comments and "10.8 percent of all pull requests". The article leaves it ambiguous whether that means PRs reviewed or PRs authored.
- 95% of firms in the study have adopted AI coding agents.
- Chart captions:
  - Lines of code: baseline mean 5016.57, pooled coefficient 1494.39 (s.e. 582.83), and a later-period coefficient 4095.84 (s.e. 1329.61). Its subscript is garbled by OCR.
  - Share of PRs with changes requested: baseline 13.00, pooled 11.84 (s.e. 1.01), later-period 21.07 (s.e. 2.26).
  - Pooled ÷ baseline ≈ 30% and ≈ 91%, which matches the text's "30 percent" and "nearly doubling" (my arithmetic).
- Study conclusion: coding gains are "absorbed by downstream constraints", with "little evidence that firms increase software output or reduce employment".

## What humans catch that AI misses (per this source)
- Not itemized. The measurable signal is that human reviewers requested changes on roughly twice the share of PRs after agents arrived, and left 35% more comments. Humans are catching enough in agent code to send it back far more often.

## Checks for the reviewer
- **Reviewability budget per change.** Record lines added, files touched and new files for every change, and flag changes over a set budget or far above the project's median. Big diffs are what make review the bottleneck. `NEW: patch bloat`
- **Rework rate as a pass metric.** In the ledger, track the share of agent changes that needed a fix after review and the number of fix rounds per finding, the same way every pass. Maps to #30.
- **Outcome, not volume.** Report finished requirements or issues per pass, never lines or commits. A pass that adds code without closing requirements is a warning sign. Maps to #30.

## Over-engineering signals (if relevant)
- Indirect only. +30% code with no change in finished issues means the extra code isn't extra delivered function. Some of it is likely bloat or rework (an inference, not measured).

## Process lessons for a non-coder directing AI
- Generating more code doesn't ship more software if review can't keep up. Budget review time and keep each agent task small enough to review.
- AI review was still marginal in this data (about a quarter of review comments), so human or independent review stays on the critical path.
- Measure delivered outcomes, not lines.

## Quotes
- "absorbed by downstream constraints in the production process"
- "little evidence that firms increase software output or reduce employment"

## Caveats
- The data stops in March 2026; agents have changed since. Firm-level averages hide variation, and many firms were still learning how to use agents.
- It measures process, not code quality. More changes requested is consistent with worse code, but doesn't prove it.
- Secondhand: the regression details, the controls and the exact meaning of the 10.8% figure aren't available here.
- It sits in tension with task-level studies that find gains (e.g. 26% more tasks in the Management Science study cited in risks-of-ai-overreliance-in-se.md). Task-level speedups and firm-level output measure different things.
