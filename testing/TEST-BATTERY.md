# The test battery: the fixed yardstick

Run the same battery after every pass. Count what it finds. If the battery changes, the numbers can't be compared, so add to it only between rounds and note when you did.

Each layer below lists what it catches, how it ran in the PrivateApp trial. The example scripts were specific to the private app (Django + React) and aren't published; the patterns are.

## 1. Baseline checks (necessary, not enough)
- Unit and integration tests at 100% branch coverage, plus lint, dead-code, type checks and the full front-end suite.
- The committed build is byte-identical to a fresh build.
- **What it catches:** code that doesn't run or doesn't match its intent.
- **What it missed:** everything else on this page. 813 green tests sat alongside a crash, data loss and double-billing.

## 2. Full workflow walk with money assertions
- The whole job through the app's own routes, start to finish, for each record type (PrivateApp: general and takeoff RFQ → template → quote → prices → contract → submittal → release → tracker → SCN → AFP → paid → change order → closeout).
- Assert every money figure against hand math to the cent.
- Run it twice: server-side (pytest through the HTTP routes) and in a real browser (Playwright on the built bundle).
- **Examples:** `server/test_zz_review_flow.py`, `browser/lib.cjs`, `browser/crawl.cjs`.

## 3. Fuzz every input
- Every POST route and JSON API. Change one field at a time to NUL, Infinity, `1e30`, 30-digit numbers, negative numbers, letters in ids, empty, very long, and wrong types. Malformed and oversized upload files.
- **Pass:** no 500s, ever. A clear refusal instead.
- **Example:** `server/test_zz_verify_fuzz.py` (40,338 posts).

## 4. Atomicity walk (forced failure)
- For every state-changing route, run it twice:
  - make the event/history/undo write raise **before** writing, then assert the whole database is unchanged;
  - let it write, then raise **after**, and assert the database is unchanged.
- **Example:** `server/test_zz_verify_atomic.py` (56 routes; 3 failed in pass 1).

## 5. Double-submit
- Post every action twice back to back, and double-click every button in the browser.
- **Pass:** one result, one event, no 500.
- **Examples:** `browser/f06.cjs`, plus the double-submit cases in the atomicity test.

## 6. Races
- Two threads, same record, a barrier to line them up, five runs per pair: bin vs move, release vs move back, two AFPs, two change orders.
- **Pass:** data is consistent and the loser gets a clear refusal (not a 500).
- **Examples:** `server/race.py`, `server/test_zz_review_race.py`.

## 7. Stale and partial
- Open → someone else changes → save. Partial forms (send 10 of 96 rows). Late responses (delay A's response, navigate to B).
- **Pass:** stale saves are refused, unsent fields are untouched, and late responses are dropped.

## 8. Failure paths in the browser
For each action, test:
- a server 500;
- a network drop (Playwright route abort);
- an expired session;
- signing in again in another tab;
- Back/Forward during a pending save.

**Pass:** a clear message, the input kept, no false success, no endless spinner, and no console errors or unhandled rejections.

**Example:** `browser/f05d.cjs`.

## 9. Real size and speed
- **Server:** query counts at 10 and at 500 rows, which should be flat or near flat (`django_assert_max_num_queries`; `server/test_zz_verify_perf.py`).
- **Browser:** open, click, select all, sort and scroll on 500 lines and 300 files at 4× CPU throttle through CDP. Target under 100 ms per interaction and under 1 s to open (`browser/perf.cjs`).

## 10. Layout, accessibility, keyboard
- 1366×768 and 1920×1080 at 100/125/150% scaling, in light and dark.
- No horizontal overflow, nothing clipped, and the next step visible.
- axe-core on each screen, plus a keyboard-only walk of the workflow.
- **Examples:** `browser/layout.cjs`, `browser/a11y.cjs`, `browser/kb.cjs`.

## 11. Fidelity measurement (when matching a reference UI)
- Measure with `getComputedStyle` and `getBoundingClientRect`, not by eye, and compare against documented values.
- Tag every reference value [doc], [known] or [est.]. Measure the [est.] ones on the real thing before building to them.
- **Examples:** `fidelity/capture.cjs`, `fidelity/keys.cjs`, `fidelity/gaps.cjs`.

## 12. Offline isolation
- See `OFFLINE-ISOLATION.md`. Run every pass if the app must stay on the PC.

## 13. Migrations
- Forward, back, forward on seeded data, including data that should block a rollback.
- **Pass:** it works, or it refuses before it changes anything.

## Scoring a pass

Record these in `../metrics/CONVERGENCE.md`:
- defects found by severity (crash / data loss / wrong result / security / stuck / cosmetic);
- regressions caused by the previous pass's fixes;
- "claimed fixed but not" count;
- layers added to the battery this round (if any, mark the round as not comparable).
