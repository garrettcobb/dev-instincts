# The risks of AI overreliance in software engineering
- **Source:** TechTarget (Informa TechTarget), "Expert Advice", Kashyap Kompella (founder, RPA2AI Research; AI industry analyst). Published Oct. 5, 2026. URL not shown.
- **Type:** practitioner article (an analyst summarizing studies)
- **Evidence strength:** moderate. It cites named peer-reviewed studies, surveys and DORA reports with sample sizes, but all secondhand, with no links in the capture and no primary data.

## Claims
- METR, "Measuring AI Ability to Complete Long Software Tasks": the task horizon of frontier systems "has historically doubled about every seven months since 2025" (as stated). Within a decade, agents could complete "a large fraction of software tasks that currently take humans days or weeks".
- Management Science (2026), "The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers":
  - Microsoft, Accenture and an anonymous Fortune 100 company; 4,867 developers ("surveyed", though described as field experiments);
  - developers with access to an AI assistant completed 26% more tasks;
  - less-experienced developers adopted more and gained more.
- 2026 meta-analysis of 23 programming studies: a moderate positive effect on productivity that varied a lot by setting, and no evidence that GenAI improved learning or skill development.
- DORA 2025, "State of AI-assisted Software Development": AI amplifies an organization's existing strengths and dysfunctions.
- DORA 2026 (qualitative), "The ROI of AI-assisted Software Development":
  - time saved creating code was often spent on auditing and verification (the "verification tax");
  - higher AI adoption went with both higher delivery throughput and higher delivery instability.
- July 2026, "AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise '2x' Mandate": after adoption, reviewer load doubles and automated review overtakes human review.
- Stack Overflow 2025 Developer Survey (49,000+ respondents): 66% are frustrated by AI output that is "almost right, but not quite", and 45% say debugging AI-generated code takes more time.
- IEEE Transactions on Software Engineering (2026), "More Code, Less Understanding?": 69 participants. With AI they reached more than twice the median task completeness, but their ability to answer technical questions about the code dropped 12.5%.
- No evidence yet of an industry-wide decline in debugging skill, because it's too early for longitudinal data (the author's own caveat). Deskilling from automation is a known mechanism in other fields.
- Areas with a heavy verification burden: authentication, payment systems, concurrency, infrastructure, database migrations.
- Plausible code (familiar patterns, sensible names, convincing comments) can hide subtle errors (asserted).

## What humans catch that AI misses (per this source)
- Where state lives, how data moves, what each component assumes, how dependencies fail, where security boundaries are.
- Subtle errors inside polished-looking code.
- The ability to explain why a change exists and how it can fail. This is what drops when the AI writes the code.

## Checks for the reviewer
- **Route by risk area.** Changes touching auth, payments or money, concurrency, infrastructure or migrations get the full behavioral battery, not a read-through. The reviewer's "kinds" table already does this via #10, #3, #14, #21, #43. Keep it.
- **Explain-it record for important changes.** Each important change has a note: why it exists, how it works, how it can fail, and what evidence shows it's correct. The reviewer checks the note exists and that every "how it can fail" item has a test. Maps to #38 and #26.
- **Requirements written before generation.** Critical requirements are committed before the code and tests that implement them (check commit order). Maps to #41 and #42.
- **Separate kinds of evidence.** CI runs type checks, static analysis and a security scanner (e.g. semgrep, bandit, `npm audit`) as separate gates, plus human review. "Tests pass" never stands in for the others. Maps to #32.
- **Instability alongside throughput.** Track reverts, defect rate and regressions per pass next to output. Maps to #30.
- **Error whack-a-mole.** A run of commits each patching the latest error in the same area ("paste error, apply fix") gets a class-level review. Maps to #27 and #28.
- **Polish isn't evidence.** Confident comments and names don't count as proof. Maps to #26.

## Over-engineering signals (if relevant)
- Not addressed directly.

## Process lessons for a non-coder directing AI
- Use agents freely for boilerplate, test scaffolding, routine transformations and well-bounded work. Important changes still need an accountable owner.
- Ask the AI to explain why a flaw occurs, not only to fix it. Explaining builds understanding; fixing doesn't.
- Keep compiler checks, static analysis, security tooling, review and production telemetry as distinct kinds of evidence.
- Do some work without AI from time to time, to check you can still handle a hard failure yourself.
- Warning signs: review queues lengthening, defects or reverts rising, sophisticated code nobody can explain.

## Quotes
- "Human understanding has no comparable scaling mechanism."
- "Plausible code deserves particular attention."

## Caveats
- Secondhand summaries. The cited studies' methods and confidence intervals aren't in the text.
- It reads Stack Overflow 2025 differently from the Humans-are-Missing paper (45% debugging vs. "two-thirds" debugging burden).
- The 26% task gain (task level) and Chen & Stratton's flat firm-level output (agents-more-code-not-more-software.md) measure different things, so they aren't necessarily in conflict.
- The METR "since 2025" phrasing is reproduced as stated and not checked here.
