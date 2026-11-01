# Shared setup for PrivateApp 1.0.1 agents

Repo: a git worktree of <workspace> (branch fix-1.0.1). Django 5.2 + PostgreSQL backend (`app/`), React + Fluent UI v9 front end (`frontend/src/`). Read CLAUDE.md, docs/adr/004-lighter-working-rule.md and docs/adr/024-explorer-front-end.md first. docs/explorer/changes.md and mapping.md describe the Explorer behaviors.

Environment (already installed; don't reinstall):
- Python: `source <workspace>` (activates the py3.12 venv and sets env vars). Then OVERRIDE the DB name so your test DB doesn't collide with other agents: `export DATABASE_NAME=<your-agent-db-name>` (given in your brief). Postgres runs on 127.0.0.1:5432, user postgres / CHANGE_ME.
- Python checks: `python -m pytest -q` (full run ~60s), `coverage run -m pytest && coverage report` (must stay 100% branch), `ruff check . && ruff format --check .`, `vulture`.
- Frontend: in your worktree run `ln -s <workspace> frontend/node_modules` if it's missing. Type check: `cd frontend && npx tsc --noEmit`. Tests: `npx vitest run <files>` (full run ~75s).
- Do NOT run `npm run build`, and do NOT commit anything under `app/static/app/explorer/` (the built bundle). The integrator builds once at the end.
- Do NOT edit VERSION, docs/adr/*, docs/rtirr-log.md or docs/explorer/changes.md. Instead write your log entries in your own fragment file (named in your brief) using the rtirr format: `### RTIRR-?? — <title>` then Date (2026-10-28), Step (1.0.1), What happened, Cause, Fix, Test (test name). The integrator numbers and merges them. If you change a behavior (not just fix it), also add a short "changes" entry (Function / Old / New / Files / Data impact / Tests) in the same fragment under a "## Changes" heading.

Rules (the developer's working rule):
- Every fix gets a test that fails before the fix and passes after. Test names read as plain sentences (e.g. `test_emptying_the_bin_works_after_a_contract_and_its_rfq_are_binned`).
- No unused code. Delete replaced code in the same change. Keep 100% branch coverage, Ruff and Vulture clean.
- No new packages, no new technologies.
- Synthetic data only. Never name a real organization.
- Commit in small commits in your worktree with messages saying what changed and why. End each commit message with:
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- Don't touch migrations unless a fix truly needs one; if it does, make it reversible and say so in your report.
- Stay inside your assigned scope. Another agent works on the other parts in parallel; if a fix needs a file outside your scope, keep the change minimal and name it in your report.

Your final report (plain text, concise): branch name and worktree path, each item → fixed / not reproducible / not fixed (why), tests added, anything that needs the developer's decision, and the final check results (pytest count + coverage %, ruff, vulture, tsc, vitest).
