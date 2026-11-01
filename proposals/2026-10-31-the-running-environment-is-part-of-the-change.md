# Proposed instinct: The running environment is part of the change

**Approved as #62 on 2026-10-31.**

Proposed by the instinct reviewer, PrivateApp 2026-10-31-6ba30b8-learn, from PA-IR-015 (an escape found by the developer in the app). Not yet approved; if approved it takes the next free number at the end of DEV-INSTINCTS.md. Tag: `proposed:serving-state-matches-code`.

It sits next to #32 (green checks prove intent, not behavior) and #35 (proven where it runs, not by reading), and near #47 (their machine is not your machine, approved from Ferrite draft F9) and Ferrite draft F12 (`proposed:release-build-guards`). All four say the same thing from different sides: the place the checks run is not the place the code runs. It could instead be approved as an amendment to #32. The draft keeps it separate because its proof is a different command, run against a different database.

- **Instinct:** the checks build a fresh world; the app runs in an old one. A change that needs a migration, a setting, a package or a file isn't done until every place that serves it has it. Until then, that place refuses to serve and says why.
- **Missed:**
  - PA-IR-015: migrations 0032-0035 were committed. 0032 refused on the dev database (58 unpriced lines, deferred on purpose by ADR-029 Decision 20), so the database stayed at 0031. The dev server reloads the working tree as it changes, so it went on serving code that reads 0035's table on every sign-in, and every sign-in was a server error.
    - Every closing check was green. pytest builds its own database from all migrations, and `makemigrations --check` compares models with migration files. Nothing compared the serving database with the code.
    - The coding agent reported "the dev database is still at 0031" each time, as a state. It never said the consequence: the dev app can't sign in.
    - Django prints "You have N unapplied migration(s)" on every reload, but only to a container log nobody reads.
  - PA-IR-016 (same area): the container migrates on start with no backup, while the backup rule lives in a separate script.
- **Ask:**
  - What does the running app need that the tests build for themselves: tables, columns, settings, packages, files?
  - Which running environment (dev server, disc, server) is behind the code right now?
  - What does the user see there because of it?
- **Prove it:**
  - The closing checks run the framework's own drift check against each serving database: `manage.py migrate --check` in Django, or the equivalent elsewhere.
  - The serving process refuses or warns where the person will see it, in the browser and not only in a log, whenever its database is behind.
  - Probe: leave a database one migration behind a table the request path reads. The closing checks must go red, and the app must answer with a named reason instead of a 500.
  - Reporting rule: a known gap is reported with its consequence ("dev database at 0031, so sign-in fails in the dev app until it's migrated"), never as a bare state.
- **Smell:**
  - a live-reloading dev server over a mounted working tree;
  - migrate only at container start;
  - closing checks that all build their own fresh database;
  - a migration whose new table the first line of a hot path reads;
  - a deliberately deferred migration in a linear chain, so every later migration is deferred with it.

Checklist line (draft): *Every database the app serves from is at what the code needs (checked by a command, not assumed), and the app refuses loudly when it isn't?*

## Evidence
- PA-IR-015 (crash, reproduced; escaped from 2026-10-31-ddb38d8-verify)
