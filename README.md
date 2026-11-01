# Dev Instincts

The reflexes an experienced developer brings that AI-written code and a green test suite keep missing, collected from real misses so they become checks instead of hindsight.

It started from a trial on a private procurement app (called PrivateApp here) built in a week with Claude Code. The app was refined through independent reviews and fix passes, to learn how deep the process has to go and whether refinement converges.

## What's public and what isn't

Everything needed to use the method is here: the instincts, the agents, the templates, the test battery, the stats tool, the ledger and the Ferrite case study.

PrivateApp's code, review reports and proof scripts are private. Its findings are in the ledger with their severity, area, instincts and status, but without file paths or links to the reports. Ferrite and Django findings keep their full detail because those projects are open source.

That means the overall check order leans on data you can't check: 290 of the 459 findings that set it come from PrivateApp. The desktop-app ranking in [STATS.md](ledger/STATS.md) is built from Ferrite alone, and every finding behind it traces to Ferrite's public source, changelog and issues. Use it to test the method against data you can verify.

## Start here
- **[WORKFLOW.md](WORKFLOW.md):** how a change goes from request to done: you decide, the devArchitect plans and writes acceptance tests, the coding session builds, the instinct reviewer checks. One writer at a time.
- **[agent/dev-architect.md](agent/dev-architect.md):** the devArchitect, a Claude Code agent (Opus, max effort) that turns a request into a plain-words plan, the decisions only you can make, and acceptance tests with hand-worked expected values. It never writes app code.
- **[agent/instinct-reviewer.md](agent/instinct-reviewer.md):** the instinct reviewer, a Claude Code agent that checks code against everything here, proves what it finds and records it in the ledger. Install: [agent/INSTALL.md](agent/INSTALL.md).
- **[ledger/](ledger/):** the database. Projects are registered in [projects.json](ledger/projects.json) with their kind and who wrote the code. It holds findings from PrivateApp (a web app built with AI), Ferrite (an open-source desktop editor, also 100% AI-written, imported as calibration data) and Django (human-written, mined as reference); the counts are in [STATS.md](ledger/STATS.md). Each is tagged with the instincts that should have caught it. STATS.md ranks the instincts by real cost, overall and per kind of app. That ranking is the reviewer's check order. Only your own projects and AI-written outside projects feed it; human-written repos mined for calibration are ranked separately as reference.
- **[DEV-INSTINCTS.md](DEV-INSTINCTS.md):** 63 instincts (18 approved from the ledger on 2026-10-31). Each has the reflex, the real miss, the question to ask and the test that proves it. A 51-line checklist at the bottom goes into prompts. Numbers are permanent.
- **[knowledge/HUMAN-REFERENCE.md](knowledge/HUMAN-REFERENCE.md):** what 35 outside sources say AI code gets wrong and what human reviewers catch, weighted by evidence: 1 strong, 6 measured, the rest opinion. It gives the reviewer its proportion-and-hygiene pass (scope, size, needless layers, unstated defaults, security basics). Index: [knowledge/README.md](knowledge/README.md).
- **[proposals/](proposals/):** 16 draft instincts still waiting for approval: 5 from Ferrite, 10 from the knowledge base, 1 from Django. Approved drafts stay there with their numbers. `STATS.md` counts the findings each draft has collected so far.
- **[LESSONS-LEARNED.md](LESSONS-LEARNED.md):** what the trial showed, what worked, what didn't, and what to carry forward.
- **[testing/TEST-BATTERY.md](testing/TEST-BATTERY.md):** the fixed yardstick to run every pass.
- **[testing/MINING.md](testing/MINING.md):** how the reviewer's mine mode grows the ledger from mature open-source repos across stacks: what to take, how much, when to stop.
- **[metrics/CONVERGENCE.md](metrics/CONVERGENCE.md):** the numbers per pass, and the rule for calling convergence.

## Layout

```
agent/
  instinct-reviewer.md    the reviewer agent (copy to ~/.claude/agents/)
  dev-architect.md        the planning agent (copy to ~/.claude/agents/)
  INSTALL.md              install, first run, everyday use
ledger/
  findings.jsonl          every finding, one JSON per line
  projects.json           every project: code, kind, authorship, source, what was mined
  STATS.md                generated: check order, reference rankings, coverage, the reviewer's record
  README.md               the schema and rules
reviews/<project>/         every published review's report and its proofs
proposals/                draft instincts awaiting approval (each shows its proposed:<slug> tag)
knowledge/
  HUMAN-REFERENCE.md      synthesis of the outside sources, and the reviewer's proportion pass
  README.md               index of sources with type and evidence strength
  sources/                one note per source, with its citation
tools/
  stats.py                regenerates ledger/STATS.md
DEV-INSTINCTS.md          the instincts + checklist
WORKFLOW.md               roles, sequence, one writer at a time, CLAUDE.md line
LESSONS-LEARNED.md        the trial's lessons
testing/
  TEST-BATTERY.md         layers, what each catches, pass criteria, scoring
  OFFLINE-ISOLATION.md    prove "offline" (Linux namespace + Windows firewall proof)
  REVIEW-METHOD.md        independent report-only reviewers, evidence rules, verifying fix passes
  PROBE-RECIPES.md        how to write throwaway proofs without touching a project
  MINING.md               mine mode: growing the ledger from open-source repos
templates/
  AUDIT-SPEC.md           the developer's full audit spec
  review-brief.md         shared brief for independent reviewers (+ finding format)
  verify-brief.md         shared brief for verifying a fix pass
  fix-agent-setup.md      shared setup for parallel fixing agents
metrics/CONVERGENCE.md    pass-by-pass data and the decision rule
context/
  BENCHMARKS.md           what fast AI delivery bought and left behind; vs. the average AI-assisted developer
  LICENSING.md            look-alike UI, icon packs, open-source notices
case-study-ferrite/       154 escaped + 14 latent bugs, probes, replay exercise
```

## How to use it on the next feature or project
1. Paste the checklist from `DEV-INSTINCTS.md` into the build prompt.
2. Build the shared guards first: one transaction-plus-event path, idempotent actions, input cleaning, stale-save refusal, error boundaries. Each gets a test that every route must pass.
3. Before calling a pass done, run `testing/TEST-BATTERY.md` and score it in `metrics/CONVERGENCE.md`.
4. Every miss becomes a new instinct here: the reflex, the miss, the question, the proof.

## Adding an instinct

```
### N. Short name
- **Instinct:** the reflex, one line.
- **Missed:** what actually happened (project, IDs).
- **Ask:** the question that would have caught it.
- **Prove it:** the test that settles it.
```

Then add one line to the checklist if it's general.

## License

MIT. See [LICENSE](LICENSE). The Ferrite probes keep their own MIT notice in `case-study-ferrite/probes/FERRITE-LICENSE`.
