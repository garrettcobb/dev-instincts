# Shared brief: verify PrivateApp "pass 1" (VERSION 1.1.1, branch fix-1.1.2 HEAD 304a997). REPORT ONLY — do not fix.

Background. PrivateApp is the developer's construction-procurement app: Django 5.2 + PostgreSQL in `app/`, a React 18 + Fluent UI v9 Windows-11-File-Explorer clone in `frontend/src/`, shipped as an offline Windows disc (`deploy/offline/`: embedded Python + PostgreSQL, `launcher.py`). The developer isn't a coder; he tests in the app.
On 1.0.0 we did three reviews and wrote <workspace> (sections 2–8 = every finding; Appendices B1 server S-01..S-25, B2 front F-01..F-24, B3 Explorer fidelity gaps). Claude Code then did "pass 1": 1.0.1 → 1.0.2 (ADR-026) → 1.1.0/1.1.1 (ADR-027 fidelity) → fix-1.1.2 (ADR-028, in progress). Read docs/adr/026-*.md, 027-*.md, 028-*.md, docs/rtirr-log.md (RTIRR-024..140) and docs/explorer/changes.md (C35..C78) for what it CLAIMS. The developer's audit spec is <workspace> — your report feeds a "pass 2" prompt written in that spec's terms.

Your job: verify claims with evidence, then find what's still wrong. "Claimed fixed" is not "fixed" until you've run something that proves it.

Baseline already run by the integrator on this code (don't repeat unless you need to): pytest 813 passed, 100% branch coverage, ruff + format clean, vulture clean, tsc clean, vitest 328 passed (40 files).

Environment:
- `source <workspace>` (py3.12 venv + env vars), then `export DATABASE_NAME=<your db>` (given in your brief). Postgres 127.0.0.1:5432 postgres/CHANGE_ME. If postgres is down: `service postgresql start`.
- node_modules is symlinked into your copy's frontend/. Chromium + Playwright preinstalled (node `require('playwright')`, or python playwright).
- Run the app: in your copy `export DJANGO_DEBUG=true DJANGO_MEDIA_ROOT=$PWD/media DATABASE_NAME=<app db>`; `PGPASSWORD=CHANGE_ME psql -h 127.0.0.1 -U postgres -c "create database <app db>"`; `python manage.py migrate`; seed synthetic data with `python manage.py shell` using the rules modules (see tests/conftest.py; the 1.0.0 reviewers' seed scripts you may adapt: <reviewer-copy>/audit/front_seed.py and <reviewer-copy>/audit/fidelity/seed.py — APIs may have changed, e.g. ADR-028 requires prices before moving to a contract). `python manage.py runserver 127.0.0.1:<port>` in the background; drive /explorer/ headless. Stop your server when done.
- Reusable 1.0.0 proof scripts: server tests <reviewer-copy>/tests/test_zz_review_*.py; front Playwright <reviewer-copy>/audit/pw/*.cjs; fidelity <reviewer-copy>/audit/fidelity/*.cjs. Copy into YOUR copy and adapt; never edit those originals.
- Edit nothing outside your own copy. Throwaway scripts stay in your copy. Nothing gets committed anywhere.

Report format (Markdown):
1. A traceability table for your scope: Finding ID | Title | Pass-1 claim (ADR/RTIRR/C ref, or "not mentioned") | Verified status | Evidence (test/script name + key output, or file:line). Verified status is one of: **Verified fixed**, **Fixed with a problem** (say what), **Not fixed**, **Partly fixed**, **Changed by decision** (cite the ADR decision), **Can't verify here** (why).
2. NEW findings (regressions or problems in code added by pass 1, or missed before), one per finding:
   ### <ID> <title>
   - Severity: crash | data loss | wrong result | security | stuck/confusing | cosmetic
   - Where: file:line (route/screen)
   - Repro: concrete steps or script
   - Evidence: reproduced (how, key output) or by reading
   - Why it matters to a buyer: one line
   - Fix: one or two lines
3. Anything you couldn't test, and why.
Be rigorous and don't pad. Final message: counts per verified status, count of new findings by severity, and the top 10 new findings one line each.
