# Proposed instincts from the human reference knowledge base (L1–L12)

Drafted from the 35 sources in `knowledge/sources/` (synthesis: `knowledge/HUMAN-REFERENCE.md`). Not yet approved. The labels L1–L12 are temporary; if approved, each takes the next free number at the end of `DEV-INSTINCTS.md`, after whichever Ferrite candidates (F1–F14) and the flaky-test proposal are approved first. L7 and L9 were approved on 2026-10-31 as #58 and #46.

**How strong the case is.** Most of the knowledge base is opinion. Each draft below says which measured studies back it and whether our own ledgers have any findings of the class. The ledgers have very few, but nobody was looking for bloat or scope creep in PrivateApp or Ferrite, so that's an absence of checking, not evidence of absence. Approve on the measured evidence, then let the ledger confirm or kill each one.

**Until approved:** the reviewer runs these checks (its proportion-and-hygiene pass) and records any hit with `instincts: []` plus the draft's tag (shown under each heading, e.g. `proposed:unstated-defaults`). `STATS.md` counts findings per proposed tag, so you can see which drafts are earning their place before approving them.

---

#### L1. Every change traces to the ask
- **Tag:** `proposed:traces-to-the-ask`
- **Instinct:** each changed hunk serves a line of the request or plan, and each line of the request has a hunk. Anything else is scope creep (extra) or a dropped requirement (missing).
- **Evidence:**
  - Wang et al. (moderate): scope creep in 50–65% of bloated agent patches; more than 10% of test-passing patches carry unrelated functional changes; about 20% miss functionality the human fix has.
  - Borg et al. (moderate): Claude Code broke about 5% of "no functional change" refactors.
  - Our ledgers: none recorded. Not checked for.
  - PrivateApp PA-IR-042 (2026-10-31-2ee2d05-learn): the developer answered "Refuse, like a contract ... One rule for both"; the fix refused only lines a restore takes away and allowed a change a contract line refuses, writing the carve-out in its own log instead of asking. A recorded decision is a line of the request: check each one is implemented as answered.
- **Ask:** which line of the request does this hunk serve? Which line of the request has no hunk?
- **Prove it:** a two-column table, request lines against hunks (`git diff --stat`, then `git diff -w` to drop whitespace-only noise). Unmatched hunks and unmatched request lines are findings. For any "no behavior change" claim, run the full suite before and after, and diff the outputs of a characterization run.
- **Checklist:** "Every hunk traces to a line of the request, and every line of the request has a hunk?"

#### L2. A change too big to verify is unverified
- **Tag:** `proposed:sized-to-verify`
- **Instinct:** size each change so it can actually be checked. Extra size is extra review cost and a place for bugs to hide.
- **Evidence:**
  - Chen & Stratton (strong): +30% lines of code with no change in issues resolved; review time +49%.
  - Wang et al.: more than 15% of every model's passing patches were over 1.5× the human fix, and newer models wrote bigger patches.
  - Mao et al. (moderate): AI files average 257 lines vs 193.
- **Ask:** what's the smallest change that does this, and how much bigger is this one?
- **Prove it:** lines added, files touched and new files, against the median of the project's last 20 commits (`git log --numstat`). Sketch the minimal fix in words. Over 1.5× the minimal fix, or over 2× the median with no written reason, is a `process` finding that names the excess.
- **Checklist:** "Change within 1.5× the minimal fix, or the excess justified in writing?"

#### L3. An abstraction earns its place
- **Tag:** `proposed:abstraction-earns-its-place`
- **Instinct:** an interface, factory, wrapper, helper, parameter, setting or exception class needs at least two real uses now, or a written reason. Speculative generality is code you pay for and never use.
- **Evidence:**
  - Wang et al.: over-engineered architecture in about 10% of bloated patches (much less than the essays claim).
  - Mao et al.: deeper call chains in AI files.
  - Many essays (anecdotal).
  - Our ledgers: none recorded.
- **Ask:** how many implementations, callers or distinct values does this have today?
- **Prove it:** grep the counts. Then the delete-the-layer test: inline it, run the tests. If everything still passes and nothing reads worse, it's a finding.
- **Checklist:** "Every new layer, helper, option and setting has two real uses, or a written reason?"

#### L4. Reuse before build
- **Tag:** `proposed:reuse-before-build`
- **Instinct:** before writing a utility, check the project, the standard library and the locked dependencies. A second implementation is a second place for the rule to drift (#6, #23).
- **Evidence:**
  - Mao et al.: less cross-file reuse in AI code (17% vs 25% of duplicated lines), more small duplicate fragments in each file.
  - CodeRabbit (weak): generic re-implementations of repo helpers.
  - Our ledgers: related only (#6 findings where one rule was enforced in one route and not another).
- **Ask:** does the project already have a helper for this (money, dates, DB access, error type)? Does the standard library?
- **Prove it:** grep for the operation's key call or name across the repo. Run a clone detector only if the project already has one installed (hard rule 5).
- **Checklist:** "No new helper duplicates an existing one, a standard-library function, or a locked dependency?"

#### L5. Complexity must be earned
- **Tag:** `proposed:complexity-earned`
- **Instinct:** a cache, queue, background job, model, agent or framework needs a measured reason. The plainest thing that works (a query, a rule, a function) is the default.
- **Evidence:**
  - Mostly anecdotal: simple-query-over-ai, stop-over-engineering-ai-apps-boring-tech, overengineering-trap-ai-automation.
  - Measured only indirectly (Wang's 10% architecture share).
  - Weakest case in this set. Approve last, or fold into L3.
- **Ask:** what's the plain alternative, and which case does it fail? For an optimization: what number shows it was needed?
- **Prove it:** name the plain alternative and show the input it fails on. An optimization needs a before-and-after measurement at real size (#13).
- **Checklist:** "Every cache, queue, job or framework added has a failing plain alternative or a measurement behind it?"

#### L6. Defend where it can happen, never where it can't
- **Tag:** `proposed:defend-where-it-happens`
- **Instinct:** validate at boundaries (user input, files, network, other systems). Don't guard states the code itself guarantees. Never catch everything and carry on.
- **Evidence:**
  - Wang et al.: overly defensive code in 20–30% of bloated patches.
  - CodeRabbit: missing null checks and guardrails, the opposite failure.
  - Mao et al.: catching generic exceptions is a top shared problem.
  - Read together: placement is the problem, not volume.
  - Extends #25 (say so loudly) and #9 (every input is hostile).
- **Ask:** can this state actually happen? From where? If it can, does the user find out?
- **Prove it:** for each new guard, a test that reaches it. A guard nothing can reach is dead code. For each broad catch, force the exception and check the user sees a clear message and nothing half-done is saved (#8).
- **Checklist:** "Every new guard is reachable by a test, and every broad catch reports the failure?"

#### L7. Unstated defaults are decisions (approved as #58, 2026-10-31)
- **Tag:** `proposed:unstated-defaults`
- **Instinct:** every default value, fallback and special case is a business decision. If it isn't written down in the spec, an ADR or a recorded decision, the code invented it.
- **Evidence:**
  - **Our ledger, strongest of the set:**
    - PA-O-04: switching a contract to another vendor's quote silently kept the old vendor's prices. Resolved by a decision: refuse the switch and name the lines with no price.
    - PA-S-03: an AFP quantity of 0 or blank silently billed the whole received quantity.
  - Wang et al.: about a third of passing patches differ from the human fix on edge cases.
  - The CSA note (anecdotal): flag spec gaps on empty, duplicate, concurrent or late input.
- **Ask:** who decided this value or branch, and where is it written? What did the spec say should happen here?
- **Prove it:** list every default, fallback and special-case branch the change adds. Each must trace to the spec, an ADR or a decision. Anything else is a finding that asks the developer to decide. Write the test from his answer, not from the code.
- **Checklist:** "Every default and special case traces to a written decision?"

#### L8. An unused input is an ignored requirement
- **Tag:** `proposed:unused-input`
- **Instinct:** a parameter, field or variable that's accepted and then ignored usually means a filter, scope or option that was asked for and dropped.
- **Evidence:**
  - Cotroneo et al. (moderate): unused parameters and variables are among the most common AI defects.
  - Mao et al.: unused assignments are a top shared problem.
  - Our ledgers: none recorded.
- **Ask:** the caller passes this. What did it expect to happen?
- **Prove it:** the project's own linter (ruff `ARG`, `F841`; TypeScript `noUnusedParameters`/`noUnusedLocals`; Vulture where installed). For each hit, check the callers: if one relies on the value, it's a `wrong-result` finding, not a tidy-up.
- **Checklist:** "No accepted input is silently ignored?"

#### L9. Security basics on every change (approved as #46, 2026-10-31)
- **Tag:** `proposed:security-basics`
- **Instinct:** secrets, passwords and crypto, object ownership, injection, and what errors and logs reveal are checked on every change, not saved for a security review.
- **Evidence:**
  - Mao et al.: about 2× high-severity CodeQL security alerts per 1,000 lines, and more keys and tokens in code.
  - Cotroneo et al.: command injection, XXE, path traversal, hard-coded credentials, information exposure through logs.
  - CodeRabbit: password handling and insecure object references lead its security list.
  - Our ledger: PA-S-V07 (xlsx formula injection, #12).
  - Overlaps #9 and #12; this makes the basics explicit.
- **Ask:** is any secret in the diff? Does every route that takes an id check that this user may see that record? Does any request data reach a shell, a query string, a file path or a parser unescaped? What does the error message show?
- **Prove it:**
  - grep the diff for key, token and password patterns and private-key headers;
  - user A requests user B's record id, expecting 403 or 404;
  - grep for `shell=True`, string-built SQL, `pickle`/`yaml.load`/unsafe XML parsing, and paths joined from request data;
  - force an error and read the response body for stack traces or `str(e)`.
  
  Passwords and crypto go through one vetted helper; flag `md5`, `sha1` or bare `sha256` near "password".
- **Checklist:** "No secret in the diff, every id checked for ownership, no request data unescaped into a shell, query, path or parser, no internals in error text or logs?"

#### L10. What the code depends on exists in the version you ship
- **Tag:** `proposed:dependencies-exist`
- **Instinct:** every library call exists, and isn't deprecated, in the version pinned in the lock file. Every config value is checked for type and range when it loads.
- **Evidence:**
  - Weak: AI tools invent functions or APIs (ai-coding-vs-human-coding, anecdotal); generated config should pass a schema (longitudinal study note, CodeRabbit).
  - Our ledger: PA-O-02, where the closing checks never covered `config/` (#26, #32), is related.
- **Ask:** does this call exist in the installed version? What happens if this setting is missing or the wrong type?
- **Prove it:** import or type-check against the locked install; run the tests with deprecation warnings as errors; a settings-load test with a missing value and a wrong-typed value, expecting a clear refusal at start-up.
- **Checklist:** "Every call resolves against the locked versions, with no deprecation warnings, and bad config is refused at start-up?"

#### L11. No model output where an exact answer is required
- **Tag:** `proposed:no-model-where-exact`
- **Instinct:** output from a language model never feeds money, permissions, priorities or stored records without a deterministic check. Where a query or rule gives the exact answer, use that.
- **Evidence:** anecdotal only (simple-query-over-ai, ai-agents-overengineered, overengineering-trap-ai-automation). PrivateApp has no model in the running app, so this is for future projects. Leave it parked until a project uses a model at run time.
- **Ask:** if the model answers wrong here, what gets saved, paid or granted?
- **Prove it:** feed a wrong model answer through a stub, and expect the deterministic check to refuse it.
- **Checklist:** "No model output reaches money, permissions or stored records unchecked?"

#### L12. Messy code gets tests before an AI edits it
- **Tag:** `proposed:tests-before-ai-edits`
- **Instinct:** before a refactor or a big edit to unhealthy code (high complexity, deep nesting, long functions, no tests), cover its current behavior with tests first.
- **Evidence:** Borg et al. (moderate): code health was the best predictor of whether an AI refactor broke the tests, though a weak one, and the effect was significant only for the five open models, not for Sonnet 4.5 or Claude Code. Claude Code still broke about 5% of test suites while claiming no functional change, so tests first is cheap insurance either way.
- **Ask:** what tests cover this file's behavior today, and would they notice if the refactor changed it?
- **Prove it:** complexity or nesting above the project's threshold (ruff `C901`, `PLR0912`/`PLR0915` where enabled) in a file the change refactors, with no covering behavior tests, is a finding. Compare complexity before and after on any change that claims to simplify (#28).
- **Checklist:** "Every unhealthy file a change refactors had behavior tests before the edit?"

---

## Candidates folded elsewhere or not drafted

| Candidate from the notes | Where it went |
|---|---|
| Follow local idioms | L4; related to #23 |
| Security primitives from one vetted helper | L9 |
| Config is validated | L10 |
| Optimization needs a measurement | L5; related to #13 |
| Explicit encoding on file I/O (Cotroneo) | #53 (text round-trips byte for byte) |
| Tests pin behavior; tests from the same agent aren't evidence | Existing #39, #42 and the flaky-test proposal |
| One source of truth, and automation that syncs duplicates is a symptom | Related to #6, #27 and Ferrite draft F13. One anecdotal source, so not drafted |
| Agent permissions written and enforced | A setup task, not a review instinct: see the report-only hook under "Later" in `agent/INSTALL.md` |
| Plan in plain words before code | Advice for the developer: `knowledge/HUMAN-REFERENCE.md` §4.1 |

## Suggested approval order
1. **L7, L1, L9.** Measured evidence and, for L7, real money findings in our own ledger.
2. **L2, L6, L8, L12.** Measured evidence, cheap to check.
3. **L3, L4, L10.** Moderate evidence, mostly cheap greps.
4. **L5, L11.** Anecdotal. Leave parked until the ledger shows hits.

## Evidence added by mining Django (2026-10-31-a05e16a-mine)

Reference data (Django is human-written), all `reading`. Report: `reviews/Django/2026-10-31-a05e16a-mine.md`.
- **L9 `proposed:security-basics`** (16 rows, 14 of them advisories that also fit #9):
  - SQL injection through column aliases, `order_by`, `_connector`, raster band indexes and Oracle JSON paths;
  - path containment by `startswith`;
  - unescaped log lines;
  - an exception's text piped into a 400 response (DJ-033, review).
  
  The alias denylist grew one character per advisory (DJ-123, DJ-117, DJ-119), which argues for adding "allowlist identifiers" to L9's Ask.
- **L8 `proposed:unused-input`** (4 rows):
  - a `select=False` flag ignored (DJ-041);
  - `for_save` accepted and not passed down, so None was saved as JSON null (DJ-042);
  - a migration computed its database alias and queried the default database (DJ-069);
  - a resolved list_display value ignored and recomputed from the wrong object (DJ-075).
- **L1 `proposed:traces-to-the-ask`** (3 rows):
  - an "optimisation" turned replace into append (DJ-018);
  - a tokenizer fix liberalised whitespace, was flagged in review, shipped, and came back as regression #37450 (DJ-023, DJ-076).
- **L7 `proposed:unstated-defaults`** (2 rows): checks defaulted to no databases (DJ-065); a CVE fix reused a 2048-character URL constant as a redirect limit (DJ-073).
- **L4 `proposed:reuse-before-build`** (1 row): a hand-written header parser replaced the stdlib's and became CVE-2026-84429 (DJ-088).
- **L10 `proposed:dependencies-exist`** (1 row): MariaDB GIS functions supported before the vendor shipped them for good (DJ-086).
