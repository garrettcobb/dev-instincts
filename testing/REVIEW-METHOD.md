# How the reviews were run

This is what made the reviews find what 100% coverage didn't.

## Independent, report-only reviewers
- Each reviewer got its **own copy** of the code, its **own database**, and a brief, but **not** the author's reasoning or the fix notes. A reviewer handed your theory tends to confirm it.
- **Report only.** Reviewers find and prove; they never fix. Fixing happens in a separate pass, with its own context.
- **Split by area so they run in parallel:** server, front end, UI fidelity, offline. One brief is shared by all (`templates/review-brief.md`, `templates/verify-brief.md`), and each reviewer adds its own scope.

## Every finding is proved or marked
- **Format:** ID, severity, where (file:line), repro, evidence, why it matters to the user, fix. The template is in `templates/review-brief.md`.
- **Evidence** is either "reproduced", with the script that ran and its output, or "by reading". Count them separately. In the trial, 21 of 25 server findings and 22 of 24 front-end findings were reproduced.
- **Spot-check the reviewer.** In the trial, the main crash (F-01), the AFP checks (S-02, S-03), the proxy leak (OFF-01) and the price wipe (S-V02) were each confirmed in the code before going into a prompt.

## The known list
Give reviewers the list of what's already known, so they don't re-report it. This is how round 2 found 49 new items instead of repeating the first 42.

## Verifying a fix pass
Trace every prior finding to a verified status, using the earlier proof scripts re-run against the new code:
- **Verified fixed**;
- **Fixed with a problem** (say what);
- **Partly fixed**;
- **Not fixed**;
- **Changed by decision** (cite it);
- **Can't verify here** (say why).

"Claimed fixed" in an ADR or log is not evidence.

## Turning findings into work
- One prompt that the coding agent works from: rules, order of work, decisions to ask the developer, then the full reports as appendices.
- Ask about decisions that change behavior; don't let the agent invent rules. Examples: who may permanently delete, whether AFP amounts may be partial, how far back a release can be dated.

## Data hygiene
Synthetic data only, and never the organization's name. Scrub workspace paths and passwords before sharing reports. Throwaway scripts stay out of the product repo.
