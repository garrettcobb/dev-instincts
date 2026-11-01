# Probe recipes

How to write a throwaway proof (a "probe") inside a project without touching its tracked files. Everything goes in `.instinct-scratch/` at the project root. Add that folder to `.git/info/exclude` first, and delete it when done (keep the useful probes in `reviews/<project>/<round>/probes/`).

## Server (pytest)
- **Reuse the project's fixtures:** `.instinct-scratch/conftest.py` containing `from tests.conftest import *`. Then run `python -m pytest -q .instinct-scratch/test_probe_x.py`.
- **Separate database:** `export DATABASE_NAME=<project>_instinct`, or the project's equivalent setting, before running. Never the dev database.
- **Coverage gates:** if the project measures coverage over `.`, run probes outside the coverage command, or they change the numbers.
- **`transaction=True` tests:** needed when a probe must really commit, e.g. to see `on_commit` callbacks or real rollbacks. They can fail to flush on append-only history tables. Use unique usernames, and ignore teardown errors after the probe's own assertions have run.
- **Route walks inside a test transaction never really commit.** If a claim depends on commit or rollback, write a `transaction=True` probe that makes a real one.
- **Forced failure:** `monkeypatch.setattr(Model.objects, "create", boom)` or a raise inside the event writer, before and after the state write. Assert the whole affected table set is unchanged.
- **Double submit:** post the same body twice back to back. Assert one result and one event.
- **Two people:** two threads, a `threading.Barrier(2)`, and a connection each (`django.db.connections.close_all()` in each thread at the end).

## Front end (vitest, jsdom)
- **Own config:** `.instinct-scratch/fe/vitest.config.ts` extending the project's, with `server: { fs: { allow: ["../.."] } }`, plus a `node_modules` symlink to the project's `frontend/node_modules`. Run `npx vitest run --config .instinct-scratch/fe/vitest.config.ts <file>`.
- **Older code side by side:** `git archive <rev> frontend | tar -x -C .instinct-scratch/<dir>`. Same for `app` or any folder.
- **Real clicks move focus; `fireEvent.click` doesn't.** Focus the element first when testing keyboard behavior.
- **Flakiness:** run each new or changed test file three times alone, plus once with `--sequence.shuffle`.
- **Failure simulation:** fail **every** call the way a dropped connection or ended session would. Answering the first call OK and failing the next simulates a state the app can't reach (PA-IR-002).

## Browser (Playwright)
- The app as shipped (debug off, built bundle). Log `page.on('console')`, `page.on('pageerror')` and `page.on('request')`.
- Laptop size first: 1366×768 at device scale 1.25.
- Session expiry: sign in again in a second context, then act in the first. Network drop: `context.setOffline(true)` or route abort.

## PrivateApp specifics
- **Env:** `source <venv>/bin/activate` plus the env vars in `.env.example`. Postgres on 127.0.0.1.
- **Timing:** full pytest takes about 4.5 minutes, so prefer targeted files.
- **Test world:** `tests.test_smoke.build_world(project, account)`.
- **Gotchas:**
  - history tables refuse TRUNCATE (see `transaction=True` above);
  - `deploy/` is Windows-only and outside coverage;
  - the project's `docs/reviews/DEV-INSTINCTS.md` may be an older copy.
