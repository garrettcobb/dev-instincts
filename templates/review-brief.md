# Shared brief for the PrivateApp 1.0.0 review (REPORT ONLY — do not fix anything)

PrivateApp is an construction-procurement app. Django 5.2 + PostgreSQL backend in `app/`; React 18 + Fluent UI React v9 front end in `frontend/src/` that clones Windows 11 File Explorer. Read docs/adr/024-explorer-front-end.md, docs/explorer/mapping.md, docs/explorer/changes.md first. The developer is not a coder; procurement staff of mixed ages who resist change are the users.

Your copy is yours alone (path in your brief). Edit nothing in <workspace> or <workspace> Throwaway scripts/tests to PROVE findings are encouraged — keep them in your copy only; nothing is committed anywhere.

Environment: `source <workspace>` (py3.12 venv + env vars). Then `export DATABASE_NAME=<your db name>` (unique, given in your brief). Postgres 127.0.0.1:5432 postgres/CHANGE_ME. Run pytest from your copy (`python -m pytest -q`, ~60s). node_modules is symlinked in your copy's frontend/. Chromium + Playwright preinstalled (`require('playwright')` from node, or python `playwright`).

To run the app (if your brief needs it): in your copy, `export DJANGO_DEBUG=true DJANGO_MEDIA_ROOT=$PWD/media DATABASE_NAME=<your app db>` then `createdb`-equivalent: `PGPASSWORD=CHANGE_ME psql -h 127.0.0.1 -U postgres -c "create database <your app db>"`, `python manage.py migrate`, then make synthetic data with `python manage.py shell` using the rules modules (services.create_rfq, services.add_quote, pricing.save, services.move_to_contract, submittals.release, tracking.move, payments.create_afp — see tests/conftest.py and tests/test_payments.py for exact calls). First account: visit / and create it, or create a User in the shell. `python manage.py runserver <port>` in the background, then drive `/explorer/` headless.

ALREADY KNOWN — do NOT re-report (being fixed separately): Recycle Bin empty failing after contract/takeoff + its RFQ binned; Undo jamming after a refused undo; Shift+Delete dead undo entry and generic error on lots; copy folder into own subfolder 500; long rename saved but reported failed; deleting submittal/lot/AFP via /api/op/ 500; contract/AFP rename doubling the prefix; lot-move undo losing SCN/since date; undoing a version restore losing quote prices; restoring a contract whose RFQ is binned; Up going to the wrong place; F5/Ctrl+Z inside a record; Ctrl+Shift+T; search not refreshing after delete / Back keeping search; per-account browser storage on shared computers; search min value crash on unpriced RFQs; deep nested folder delete crash; bin-while-moving race; Shift-click after filter; reopen history lost after Close others; cut lot left on clipboard; Undo skipping takeoff made from New; prices → $0 when moving materials into a contract with no/other quote; AFP button greyed with no reason and Release only on the RFQ view; no Ctrl/Shift multi-select in record tables; duplicated CSRF helper / extension parsing / contract delete rule; slow search/bin queries; Recycle Bin rules not counting binned records; op + undo entry not atomic.

Finding format (Markdown), one per finding:
### <ID> <short title>
- Severity: crash | data loss | wrong result | security | stuck/confusing | cosmetic
- Where: file:line (and route/screen)
- Repro: concrete steps or the script/test you ran
- Evidence: reproduced (say how, paste the key output) or by reading
- Why it matters to a buyer: one line
- Fix: one or two lines

Be rigorous: a finding you "reproduced" must really have been run. Don't pad — no style nitpicks unless they hurt users. Rank by severity in the file.
