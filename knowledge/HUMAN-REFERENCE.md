# Human reference: what the evidence says about AI-written code

A synthesis of the developer's knowledge base: 35 distinct sources on human vs AI coding and AI over-engineering, collected 2026-10-30. One note per source is in `sources/`, and `README.md` indexes them with their type and evidence strength.

**Weigh it honestly:**
- 1 source is strong evidence;
- 6 are moderate: measured studies, mostly preprints;
- 27 are weak or anecdotal: opinion pieces and practitioner articles;
- 1 is off-topic and empty.

The rest of this file leans on the measured studies and treats the opinions as hypotheses for the reviewer to test. Our own record is real evidence too, from the PrivateApp and Ferrite ledgers, and where it disagrees with an opinion, it wins.

---

## 1. What the measured studies show

**More code, not more software.** A Harvard working paper (Chen & Stratton, via Ars Technica) covered 700+ firms and 300M work events, comparing each firm before and after it adopted agents. After adoption:
- 30% more lines of code, 20% more commits and 23% more PRs;
- no significant change in issues or epics resolved;
- review time up 49%;
- the share of PRs sent back for changes nearly doubled;
- 35% more review comments.

The gain is absorbed by review. This is the strongest source in the set. *(agents-more-code-not-more-software)*

**Passing isn't matching.** A position paper (Wang et al.: CMU, Stanford, Princeton) measured agent patches on SWE-bench against the human fix, counting only patches that pass the tests:
- **Bloat:** every model had more than 15% of its passing patches over 1.5× the human fix's size, and newer models wrote bigger patches.
- **Causes of bloat** (multi-label, judged by two LLMs):
  - verbose implementation, about 60%;
  - scope creep, 50–65%;
  - overly defensive code and excess comments, 20–30% each;
  - over-engineered architecture, about 10%.
- **Behavior:** more than half of the passing patches behave differently from the human fix:
  - about a third differ on standard behavior, and a third on edge cases;
  - about 20% miss functionality the human fix has;
  - more than 10% include unrelated functional changes.
- **Tests:** "When AI is producing both, the tests no longer serve as independent evidence."

*(humans-missing-from-coding-agent-research)*

**AI code in real repositories.** Mao et al. compared 19,816 AI-attributed files against same-repo human files:
- **Size:** AI files are bigger (257 vs 193 lines), with more statements per function and deeper call chains.
- **Reuse:** less cross-file reuse (17% vs 25% cross-file duplicated lines), but more small duplicate fragments per file. The authors read this as one-off code instead of shared helpers.
- **Rework:** files are revisited and reworked more at 30–90 days.
- **Security:** high-severity CodeQL security alerts are roughly double (0.93 vs 0.46 per 1,000 lines), and there are more API keys, tokens and private keys in code (human files had more hard-coded passwords).
- **Shared top problems:** unused assignments, dead code, and catching generic exceptions.

*(ai-code-in-real-world-repos)*

**Isolated functions, older models.** Cotroneo et al. analysed 507k functions:
- AI code is shorter and simpler.
- It's heavy on unused parameters and variables, file I/O without an explicit encoding, and print/stack-trace debug leftovers.
- It's more vulnerable: command injection, XML external entities, resource exhaustion, information exposure through logs, hard-coded credentials, path traversal.
- Human code was the most secure overall.

*(human-vs-ai-code-defects)*

**Messy code breaks under AI edits.** Borg et al. ran "refactor for maintainability" on 5,000 files:
- Code-health score was the best predictor of whether a refactor broke the tests, though still a weak one (tree AUC about 0.55). The effect was significant for the five open models, not for Sonnet 4.5 or Claude Code.
- Claude Code broke about 5% of test suites while its summaries claimed zero functional changes.

*(code-for-machines-codehealth)*

**The human side.** A six-month study of 95 engineers (Vella & Blincoe):
- Work shifted toward verification.
- 84% felt more productive at both points, yet the share reporting a worse experience on at least one dimension doubled (14% → 27%).
- Productivity and experience moved independently.

Separately, an IEEE study cited by TechTarget found developers using AI got further on tasks but answered 12.5% fewer questions about their own code correctly. *(longitudinal-ai-coding-assistants, risks-of-ai-overreliance-in-se)*

**Vendor report, weak evidence.** CodeRabbit (470 PRs, using its own taxonomy, and it sells a review tool) reports:
- 1.7× more issues per AI PR;
- about 8× more excessive I/O;
- about 2× more concurrency and dependency-order problems;
- 2.66× more formatting noise;
- security led by password handling and insecure object references.

Treat these as directions, not magnitudes. *(coderabbit-ai-vs-human-code-report)*

## 2. What a human reviewer catches that tests and AI miss

Across the measured sources and our own two ledgers, it comes down to eight things:
1. **Intent:** the change does something other than what was asked, does more, or leaves part of it out. Tests the same agent wrote can't catch this.
2. **Edge paths:** None, empty, zero, boundaries, error paths, and second use.
3. **Unstated constraints and invented rules:** defaults nobody chose; external-service behaviour assumed and never written down.
4. **Proportion:** more code, layers, options or infrastructure than the problem needs.
5. **Local fit:** a generic idiom where the project already has a helper or a pattern.
6. **Security basics:** secrets, crypto and passwords, object ownership, injection, leaky errors and logs.
7. **Hidden costs:** I/O inside loops, work that grows with size, idle cost.
8. **Whether the tests mean anything:** expected values that came from the code, tests that can't fail.

Items 1, 2, 5 and 8 are already partly in Dev Instincts (#26, #31, #32, #39, #42, #9). Items 3, 4 and 6 are mostly new: see `proposals/2026-10-31-literature-candidates.md`.

## 3. Where the sources disagree, and how to read it

- **Defensive code: too much or too little?** Wang et al. and several essays say AI adds guards for impossible states. CodeRabbit says AI leaves out null checks and guardrails. Both are true in different places. **Check placement, not volume:** validate at boundaries (user input, files, network, other systems), and don't defend states the code itself guarantees. Never swallow a real failure (#25).
- **Is AI code bigger or smaller?** It's bigger in real repositories and agent patches (Mao; Wang), and smaller as isolated functions from older models (Cotroneo). For agents working in a codebase, the bigger reading applies.
- **Is architecture bloat the main problem?** Essays say yes. Measurement says verbosity and scope creep dominate, with architecture at about 10% of bloated patches. Our own ledger agrees with measurement: our misses were mostly edge cases and rules not enforced everywhere, not class hierarchies.
- **Who reviews?** Some say a human reads every line; others say a human reviews the plan and machines audit the diff. For a developer who doesn't read code, the second is the only workable answer, with one caveat from the sources: a reviewer from the same model family shares the author's blind spots. That's why the instinct reviewer runs report-only, in its own context, and has to prove its claims.
- **Productivity:** task-level studies show gains (+26% tasks); firm-level data shows none in delivered output. Measure delivered outcomes, never lines of code.

## 4. What this means for a developer who directs AI and doesn't read code

1. **Have the plan restated in plain words before any code is written.** If you can't restate the goal, or the plan uses machinery the app doesn't need (queues, sagas, vector databases, "frameworks" for one case), stop it there.
2. **Write the key requirements and acceptance tests before prompting,** with expected values worked out by hand (#42). Tests generated with the code are not evidence.
3. **Keep each change small enough to verify.** Big diffs are where review fails, and review is the bottleneck.
4. **Ask for evidence you can check without reading code:** a screenshot, a short recording, a before/after number, the failing-then-passing test (#39).
5. **Put standing rules in CLAUDE.md, and check they actually held in the next session.**
6. **A newer model isn't automatically safer:** newer models wrote bigger patches with more behavioural differences.
7. **Before letting AI refactor messy code, cover it with tests first.** Unhealthy code breaks most.

## 5. The reviewer's proportion-and-hygiene pass

Run on every change, alongside the instinct checks. Until the proposed instincts are approved, record findings from this pass with `instincts: []` and the tag shown (e.g. `"tags": ["proposed:traces-to-the-ask"]`). The drafts, with their evidence and proofs, are in `proposals/2026-10-31-literature-candidates.md`.

| Check | How to detect it | Tag |
|---|---|---|
| Every hunk maps to the request; nothing asked for is missing | Read the request or plan; walk `git diff --stat` and `git diff -w`; flag reformat-only hunks, unrelated files, dependency or lockfile changes; tick off each requirement | `proposed:traces-to-the-ask` (L1) |
| Change size against the project's normal | Lines added, files touched and new files per change vs the median; flag over 1.5× an obvious minimal fix | `proposed:sized-to-verify` (L2) |
| Abstractions earn their place | Interfaces, factories or strategies with 1 implementation; helpers with 1 caller; layers that only forward; parameters no caller passes; config keys with one value; exception classes never caught. Then the delete-the-layer test: remove it and run the tests | `proposed:abstraction-earns-its-place` (L3) |
| Reuse before build | New utility, dependency or service: is there an existing helper, standard-library function or installed package that already does it? Run a clone detector only if the project already has one | `proposed:reuse-before-build` (L4) |
| Complexity earned | A model, agent, queue, cache or framework where a query, a rule or a plain function would do; an optimization with no measurement behind it | `proposed:complexity-earned` (L5) |
| Defence where it counts | Guards at boundaries yes; guards for states the code guarantees no; no `except: pass`, no catch-all that returns a default | `proposed:defend-where-it-happens` (L6) |
| Assumptions written down | Every special-case branch and default traces to the spec or to a decision; external-service behaviour (expiry, single use, retries) stated and tested | #58 (approved) |
| Unused inputs | Unused parameters, variables and fields: ask whether a filter or scope was dropped (ruff ARG/F841, pylint W0613/W0612, TS `noUnused*`) | `proposed:unused-input` (L8) |
| Security basics | Secret scan; password and crypto through one vetted helper; every route taking an id checks ownership; no `shell=True`, string-built SQL, unsafe XML/pickle/yaml loads, or paths built from request data; no debug prints, stack traces or `str(e)` in responses; no raw user input in logs | #46 (approved) |
| Dependencies and config exist and are valid | Imports and calls resolve against the locked versions; type-check; deprecation warnings as errors; a missing or wrong-typed setting is refused at start-up | `proposed:dependencies-exist` (L10) |
| No model output where an exact answer is required | Model output never feeds money, permissions, priorities or stored records without a deterministic check | `proposed:no-model-where-exact` (L11) |
| Messy code covered before AI edits it | Complexity or nesting above the project's threshold, with no tests, in a file the change refactors | `proposed:tests-before-ai-edits` (L12) |

## 6. Source index
See `README.md`.
