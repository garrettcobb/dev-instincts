# From Code Production to Code Orchestration: How AI Coding Assistants are Reshaping Software Engineering
- **Source:** ResearchGate preprint, Simon Stieber (listed as University of Augsburg; the paper names XITASO GmbH, Augsburg), March 2026, DOI 10.13140/RG.2.2.13510.95048 (OCR shows a comma in the DOI). URL truncated in the text: researchgate.net/publication/401655474_From_Code_Production_to_Code_Orchestration_... CC BY 4.0.
- **Type:** preprint
- **Evidence strength:** weak as extracted — a survey of "over 75" studies, but only the abstract and the start of the introduction survived extraction (pages 3–7 are blank). No figure can be traced to its source study. The author's employer is a software consultancy; no review-tool conflict visible.

## Claims
- Synthesizes over 75 peer-reviewed studies, large industry surveys and empirical analyses.
- 76% of developers use or plan to use AI coding tools (Stack Overflow Developer Survey 2024); 97% have tried them (GitHub).
- AI speeds code generation and makes "meta" work more important: requirements specification, testing strategy, security assessment, code review.
- "Testing paradox": AI test generation has 41% real-world accuracy vs. 92% on simple benchmarks. The source study isn't visible in the extract.
- About 30% of AI-generated code contains vulnerabilities spanning 43 CWE categories. The source isn't visible.
- Autonomous agents show rapid benchmark progress alongside systematic failure patterns in enterprise settings (details missing).
- Introduces "comprehension debt" as a long-term risk. The definition is missing; the reference list includes a study of comprehension debt in resource-constrained indie teams.
- Proposes a skills framework that favours evaluation, orchestration and quality gatekeeping over code production.

## What humans catch that AI misses (per this source)
- Per the abstract only: requirements, test strategy, security assessment and review are where human work matters most. The specifics are on the missing pages.

## Checks for the reviewer
- AI-written tests are unverified until proven. Run each guard test with its fix disabled; confirm expected values were computed outside the code. → #39, #42.
- Coverage isn't correctness: an AI test suite can be large and wrong. → #32.
- Security-scan every AI change with CWE mapping (semgrep, bandit or CodeQL if already in the project). → NEW: Security-scan every AI change.
- Comprehension debt: for each risky module (money, saving data, concurrency, permissions), can the developer or a second human explain what it does? Detect: risky modules with no human-reviewed note, ADR or spec. → #38.

## Over-engineering signals (if relevant)
- Not covered in the surviving text.

## Process lessons for a non-coder directing AI
- Put your effort into specifying requirements, setting the test strategy and gating quality; leave routine generation to AI.

## Quotes
- "AI makes testing more important while demonstrating poor quality in test generation"

## Caveats
- The body is missing from the text extract. The source PDF in the source PDF  (about 5 MB) probably holds it and is worth re-extracting.
- The 41%/92% and ~30% figures can't be checked from this text.
- Contradicts Estrin (The Human Factor of AI and Coding, same group), who rates AI better than humans at testing.
