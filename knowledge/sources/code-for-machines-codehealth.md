# Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics
- **Source:** arXiv:2601.02200v1 [cs.SE], 5 Jan 2026. Markus Borg and Adam Tornhill (CodeScene), Nadim Hagatulah and Emma Söderberg (Lund University). Replication package: https://github.com/codescene-research/ai-friendliness-forge-2026
- **Type:** preprint
- **Evidence strength:** moderate. Large controlled sample: 5,000 files, 5 open models plus Sonnet 4.5 and Claude Code, a test-suite oracle, significance tests with Holm correction. Against that:
  - the code is competitive-programming Python of 60–120 lines, far from business apps;
  - CodeScene authors are testing their own proprietary metric, a conflict of interest;
  - the Sonnet and Claude Code runs used only n=1,000;
  - the per-file prediction is weak (AUC about 0.55).

## Claims
**Dataset**
- Built from DeepMind's CodeContests: 13,210,440 solutions, then 1,502,532 in Python 3, 1,390,531 after removing duplicates, 88,156 with at least one CodeScene smell, 18,074 at 60–120 SLOC, and finally 5,000 (2,500 Healthy, 2,500 Unhealthy).
- CodeHealth (CH) is scored 1–10:
  - Healthy is about 9 and above (the OCR drops the ≥/> sign);
  - Warning is between 4 and 9;
  - Alert is below 4.
- A sampling-script bug treated CH = 9 as Unhealthy; the authors say all analyses use the intended convention.
- CodeScene detects 25 smells for Python; 9 occur in the dataset. The top five:
  - Bumpy Road Ahead (n=4,901);
  - Complex Method (3,572);
  - Deep Nested Complexity (2,433);
  - Complex Conditionals (1,328);
  - Excessive Function Arguments (724).

**Setup**
- Models: Gemma-3-27b-it, GLM-4-32B-0414, Granite-4.0-H-Small, gpt-oss-20b, Qwen3-Coder-30B-A3B-Instruct, claude-sonnet-4-5-20250929, and Claude Code v2.0.13 (agentic).
- Temperature 0.7, at most 8,192 new tokens.
- Each model got a single "refactor for maintainability" prompt. A refactor counts as broken if any original test fails.

**RQ1: perplexity**
- Perplexity is not meaningfully associated with CH: directions are mixed and effect sizes trivial.

**RQ2: break rates (tests passed, Healthy vs. Unhealthy)**
- Qwen: 80.72% vs. 72.16%.
- GPT: 64.13% vs. 52.98%.
- GLM: 60.14% vs. 50.02%.
- Gemma: 55.74% vs. about 40.6%.
- Granite: 46.46% vs. about 37.2%.
- For Gemma and Granite, the Unhealthy cells in Table 2 are OCR-garbled; the values above are from Table 3.
- Sonnet: 86.77% vs. 84.03% (not significant, p=0.439).
- Claude Code: 96.19% vs. 94.81% (not significant), so it broke about 5% of test suites either way.
- Risk differences in break rate for the medium models are all significant: from −8.58 pp (Qwen) to −15.12 pp (Gemma).
- Relative risk of breaking ranges from 0.692 (Qwen) to 0.852 (Granite), stated as a risk reduction of "about 15%" for the weakest model and "30%" for the strongest.
- Overall break rates for the medium models: Qwen 0.236, GPT 0.414, GLM 0.449, Gemma 0.518, Granite 0.582.

**RQ3: predicting breaks**
- CH is the root split in all five decision trees. The learned thresholds run from CH < 8.285 to < 9.195, four of them near 9. One threshold is labelled "Qwen" twice in the text, probably a typo for Gemma.
- Tree AUC is only 0.544–0.565.
- CH carries "~3-10x more predictive information" than perplexity or SLOC.
- Logistic-regression odds ratios for CH: Qwen 1.347, GPT 1.307, GLM 1.215, Gemma 1.420, Granite 1.240. One standard deviation of CH (about 0.65) raises the odds of a non-breaking refactor by "roughly 20–40%".
- Break rate falls as CH rises for every model. For Sonnet, the safer zone may start around CH≈8.

**Refactors that pass tests can still make the code worse**
- Every model sometimes lowered CH (added or worsened smells) on refactors that passed the tests. From Table 3, OCR-noisy: Qwen 27.01% of passing Healthy refactors, Sonnet 26.33%, Claude Code 11.04%.
- Sonnet improved CH in 57.74% (Healthy) and 82.42% (Unhealthy) of passing refactors.
- "Success" (tests pass and CH rises): Sonnet 50.10% / 69.26%; GPT 38.44% / 43.52%, the best of the medium models; Claude Code 19.24% / 24.75%.

**Claude Code's behaviour**
- Claude Code was the most conservative: CH unchanged in 68.81% (Healthy) and 60.76% (Unhealthy) of cases according to the text; Table 3 reads 68.96 / 60.63, a discrepancy.
- It mostly renamed variables, reorganised code to convention and fixed whitespace.
- Its summaries claiming "zero functionality changes" were overconfident: it sometimes broke behaviour.
- The authors found no pattern in when it chose a bolder refactor.

**Background claims cited, not the authors' own data**
- About 80% of developers use AI tools (2025).
- Gartner predicts adoption rising from 14% (early 2024) to 90% by 2028.
- Fewer than 10% of organisations track technical debt methodically.
- Developers waste up to 42% of their time on poor code quality.
- Developers find defects faster when variables have appropriate names.

## What humans catch that AI misses (per this source)
- A "refactor" that changed behaviour although the agent's summary says nothing changed. A human runs the tests rather than trusting the summary.
- Refactors that pass the tests but add new smells.
- Humans and LLMs are confused by the same smells. Nested, branchy, long-argument code is where both break things, so that's where human oversight should go.

## Checks for the reviewer
- **"No behaviour change" claims are run, not read.** For any commit described as refactor, cleanup or "maintainability", run the full suite before and after, and require zero edits to test expectations. Detect: a refactor-labelled commit that touches test assertions. Maps to #26 and #40.
- **Code health gate on AI edits.** Score each changed file before the edit. Detect with lizard, radon or eslint `complexity`/`max-depth`/`max-params`:
  - cyclomatic complexity above about 10 per function;
  - nesting depth of 4 or more;
  - more than about 5 parameters;
  - conditions with 3 or more boolean operators;
  - several separately nested blocks in one function (Bumpy Road).

  If the file is in that bucket, require behaviour tests covering it before accepting the AI edit. Maps to NEW: Unhealthy code gets tests before AI edits.
- **Did the change make the code worse?** Compare complexity metrics before and after for each touched function; flag increases in a change that claims to simplify. Maps to #28 and NEW: Unhealthy code gets tests before AI edits.
- **The agent's completion summary is a claim.** Any "all functionality preserved" or "verified" line needs command output behind it. Maps to #26.

## Over-engineering signals (if relevant)
- A generic "refactor for maintainability" prompt sometimes produced bold restructuring: class extraction, "single responsibility", decomposition. The paper doesn't measure whether that structure was needed.
- Excessive Function Arguments is a detectable smell: the function does too much or lacks an abstraction.

## Process lessons for a non-coder directing AI
- Start AI work on healthy code, or raise code health in an area before scaling AI changes there. Expect more human involvement where CH is low.
- Agentic Claude Code trades benefit for safety: expect renames and formatting from "refactor" requests, and occasional silent breakage.
- The authors pinned the model version and turned off Bash, WebFetch, WebSearch and MCP in `.claude/settings.json` to control the agent. Scoped permissions are a usable pattern.
- The authors suggest giving the coding agent a code-quality tool (a CH check) alongside its tests and linter.

## Quotes
- "Claude's statements about “zero functionality changes” and “file maintains its original functionality” are overconfident"
- "expect more human involvement with lower CH."

## Caveats
- Competitive-programming code, which the authors say "would never enter production repositories". Python only, small files, very few samples below CH 7.
- The vendor's own metric. CH is a weak per-file predictor (AUC about 0.55) even though it's the best of the three features tested.
- Claude Code v2.0.13 and Sonnet 4.5 are older versions; the Sonnet and Claude Code runs may be underpowered.
- Several table cells are OCR-garbled. Use the summary numbers in the text.
