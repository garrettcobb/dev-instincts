# Dev Instincts

The reflexes an experienced developer has that tests and AI reviewers kept missing.

Each one comes from a real miss in the PrivateApp trial. **Numbers are permanent:** the ledger refers to instincts by number, so new ones are added at the end, never renumbered. IDs refer to the private app's review reports (not published) (S- server, F- front end, FV-/S-V- pass-1 verification, NF- Explorer fidelity, OFF- offline, R/3.x/4.x from the 1.0.1 prompt).

Each entry has four parts:
- **Instinct:** the reflex, in one line.
- **Missed:** what actually went wrong.
- **Ask:** the question to put to yourself or to Claude before calling a feature done.
- **Prove it:** the test that settles it.

The checklist at the bottom is the short version. Paste it into a Claude Code prompt.

---

## A. Data and state

### 1. Every write has a partner
- **Instinct:** a state change and its record (history, audit, undo entry) are one thing. They save together or not at all.
- **Missed:**
  - Operations and their Undo entries were saved separately (R2).
  - After the fix, page deletes and "New takeoff" still weren't atomic (S-V06).
  - A long rename was saved while the user was told it failed (3.5).
- **Ask:** if the second write fails, what's left in the database?
- **Prove it:** force the event write to fail, assert nothing changed, then the reverse. Run it as one parametrized test over every state-changing route, so a new route can't skip it.

### 2. Assume the double-click
- **Instinct:** every button gets clicked twice, every form submitted twice, every request retried.
- **Missed:** "Move to new contract" made two contracts (S-06). AFP went Checked *and* Paid (F-06, S-V12). Change orders were created twice (S-V12). Fill from quote wrote two history entries (FV-08). Release returned a 500 after it had already worked (F-10).
- **Ask:** what happens if this exact request arrives twice, one millisecond apart?
- **Prove it:** post every action twice in a row. Assert one result, one event, no 500. Fix it on the server (expected-current-state check or submit token), not only with a disabled button.

### 3. Assume two people at once
- **Instinct:** someone else is changing the same record right now.
- **Missed:**
  - two AFPs at the same moment double-billed (S-04);
  - an RFQ was binned while materials moved into it (3.13);
  - a release was committed while the line moved off its contract (S-V14);
  - two change orders made at once gave a 500 (S-V09).
- **Ask:** what does this read that someone else could change before I write? Is it locked? Do I re-check the rule inside the lock?
- **Prove it:** two threads, same record, a barrier, five runs. Data stays consistent and the loser gets a clear refusal.

### 4. Missing is not blank
- **Instinct:** a field the client didn't send means "don't touch it", not "clear it".
- **Missed:**
  - Any price form cleared the price of every line it didn't send (S-V02).
  - A blank row in an upload cleared a price (S-V01).
  - This is how "a contract needs a price" got undone right after it was enforced.
- **Ask:** if the form only shows 10 of 96 lines, what happens to the other 86?
- **Prove it:** post a partial form and assert untouched rows are unchanged. Clearing a value must be an explicit action.

### 5. The screen is stale
- **Instinct:** what the user is looking at may already be out of date.
- **Missed:**
  - an old price dialog wiped prices added since it opened (S-V02);
  - a Details-pane edit was saved onto the next item clicked (F-02);
  - the Notes pane showed the previous project's notes (F-11);
  - the editor overwrote newer text (F-04).
- **Ask:** what if the data changed between load and save? What if the response for A arrives after the user moved to B?
- **Prove it:** send a version or modified time with every save and refuse stale saves with "changed since you opened this, reload". Drop late responses (AbortController or request id). Test with a delayed response.

### 6. A rule at one door is a rule at every door
- **Instinct:** if a rule matters, every path that can break it enforces it, not just the obvious screen.
- **Missed:**
  - "A material goes on a contract only with a price" was enforced at the move, then undone by four other routes (S-V01).
  - The per-person Recycle Bin was bypassed by restore, then Shift+Delete (S-V04).
  - Recycle Bin rules didn't count binned records, so delete checks passed when they shouldn't (R1).
- **Ask:** list every route that can change this field or record. Does each one check the rule?
- **Prove it:** put the rule in the model or service layer, where every route passes through. Add one test per route that tries to break it.

### 7. Undo reverses exactly what it did, nothing more
- **Instinct:** undo restores the before-state of *this* action only, and keeps everything it would otherwise lose.
- **Missed:**
  - undoing a lot move lost its SCN and date (3.8);
  - undoing a version restore lost typed prices (3.9);
  - later, it deleted lines another buyer had added since (S-V15).
- **Ask:** what did this action touch, what else could have changed since, and what does Undo throw away?
- **Prove it:** do → have someone else change something → undo. Assert only the action's own changes reversed.

### 8. A failure leaves nothing behind and jams nothing
- **Instinct:** a refused or failed action leaves no trace, and the next action still works.
- **Missed:**
  - one refused Undo jammed every later Ctrl+Z (R3);
  - after that fix, non-rule errors still jammed it (S-V11);
  - Shift+Delete left an Undo entry that could never work (3.3);
  - the Recycle Bin couldn't be emptied ever again (3.1).
- **Ask:** after this fails, can the user do the next thing?
- **Prove it:** make the action fail, then run the next normal action, and assert it works.

### 9. Every input is hostile
- **Instinct:** users, files and the network will send NUL characters, Infinity, 30-digit numbers, letters in id fields, empty strings and 100,000 blank rows.
- **Missed:**
  - 500s on huge numbers, NUL, Infinity and non-numeric ids (S-16..S-18);
  - after the "fix", Notes still gave a 500 on NUL (S-V03);
  - uploads had no row limit (S-V16).
- **Ask:** what's the worst thing that could arrive in each field?
- **Prove it:** a permanent fuzz test over every POST route and API that asserts no 500.

### 10. Money checks itself
- **Instinct:** money is Decimal end to end, one rounding rule, display precision = stored precision, and every amount is checked against what it's supposed to equal.
- **Missed:**
  - an AFP amount was never checked against the SOV, so $1,000,000 went through on a $250 line (S-02);
  - a quantity of 0 billed everything (S-03);
  - a full quantity for a token amount spent the row (S-V05);
  - half-even rounding left a stuck cent (S-11);
  - unit prices shown rounded made rows not add up (F-08);
  - moved lines silently became $0 (the original user bug).
- **Ask:** what should this number equal, and what refuses it if it doesn't?
- **Prove it:** a full workflow test that asserts every money figure against hand math to the cent (passed in pass 1, and keep it), plus edge cases at 0, the balance, balance + 0.01 and negative.

### 11. Dates have a direction
- **Instinct:** shipped can't come before released, paid can't come before checked, nothing is dated in the future, and derived dates anchor to the right event.
- **Missed:**
  - shipped in 2020 on a 2026 release, checked in 2030 (S-09);
  - an AFP due date moved when later shipments arrived (S-08);
  - a release was always dated today, so a real earlier shipment couldn't be recorded (S-V08).
- **Ask:** what order must these dates be in? What's the earliest and latest this one can be?

### 12. Exports run code
- **Instinct:** anything the user typed that ends up in an Excel or CSV file can become a formula.
- **Missed:** vendor downloads wrote text starting with `=` as live formulas (S-V07, proved with HYPERLINK and DDE payloads). The 0.20.0 audit flagged this, and nobody fixed it.
- **Prove it:** put `=1+1` in every text field, export, and assert the cell is text.

### 13. Test at real size
- **Instinct:** it'll be fine with 5 rows. It won't be with 500.
- **Missed:**
  - about 6 queries per line on the RFQ view, so about 3,000 for a 500-line takeoff;
  - about 43 queries per contract on the Overview;
  - 2.9 s to open at 4× CPU (FV-09).
- **Prove it:** query-count ceilings at 10 and 500 rows, and browser timings at 4× CPU throttle.

### 14. Migrations go backward too
- **Instinct:** a rollback with real data in it must either work or refuse *before* it changes anything.
- **Missed:**
  - rolling back 0025 brought binned rows back as live (S-25);
  - after the fix, it undid three migrations and then refused, leaving the database half rolled back (S-V13).
- **Prove it:** migrate forward, back, forward on seeded data, including data that should block it.

### 15. Files on disk don't roll back
- **Instinct:** a database transaction can't undo a file write. Saving a file and then rolling back leaves an orphan, and deleting a file before commit can lose it for good.
- **Missed:** pass 2 made every request one transaction. Uploads still write to the media folder before the transaction commits, so a forced failure leaves the row gone but the file kept.
- **Ask:** if this request fails after the file is written, what's left on disk? If it fails after a delete, is the file already gone?
- **Prove it:** a forced-failure test on every upload route asserting no row **and** no file. Delete files only in `on_commit`.

---

## B. Screens and workflow

### 16. A greyed-out button says why
- **Instinct:** a disabled control with no reason is a dead end.
- **Missed:** "Enter an AFP" went grey after the first AFP, with no explanation. It was the original user complaint, and the rule (release → ship with an SCN → bill) was invisible.
- **Ask:** for every disabled control, what would a new buyer think?
- **Prove it:** a test asserts that every disabled action has a tooltip or reason text.

### 17. Every dead end is a bug
- **Instinct:** at every step, the user can see the next step.
- **Missed:**
  - Release only existed on the RFQ, not the contract;
  - Mark sent was hidden under "…" at 1366px (FV-04);
  - closeout couldn't be reached from the tracker folders, and paste there silently did nothing (FV-07);
  - Ctrl+A → Move was refused with 60 names (FV-03).
- **Prove it:** walk the whole job end to end in the browser, the way a buyer would, at a laptop screen size. Note every "now what?".

### 18. Never fake success, never spin forever
- **Instinct:** the user always finds out what really happened.
- **Missed:**
  - an upload said "Uploaded 1 of 1" when nothing was stored (F-05);
  - spinners ran forever when a load failed (F-13);
  - network failures were silent (F-12);
  - an offline upload was blamed on file size (FV-06).
- **Prove it:** for each action, test a 500, a network drop and an expired session. Each must give a clear message, keep the input, and never show a success.

### 19. One broken view doesn't kill the app
- **Instinct:** wrap views in error boundaries. Read event data before async state updates.
- **Missed:** scrolling turned the whole app white, because `e.currentTarget` was read inside a deferred updater (F-01). After the fix, Ctrl+Z inside a record still did it (FV-01): it was in a part the boundary didn't cover.

### 20. Shortcuts don't fire while typing
- **Instinct:** keyboard shortcuts are off inside inputs, selects, menus and dialogs.
- **Missed:** pressing Delete on a drop-down binned the selected RFQ (F-07).

### 21. Session expiry is a normal path
- **Instinct:** an 8-hour idle timeout, or signing in again in another tab, will happen daily.
- **Missed:**
  - every save failed with "Try again" (F-05);
  - the Details pane crashed (F-03);
  - Sign out showed Django's raw 403 page (FV-05);
  - one CSRF helper was missed in the cleanup (4.10).

### 22. Focus goes back where it came from
- **Missed:** after a dialog or rename, focus dropped to the page and the arrow keys died (F-14). A focus fix then drew a black frame around the whole content area (NF-01).

### 23. Same thing, same name, same format
- **Missed:**
  - "Mark ready for rfq" vs "Ready for RFQ" (NF-13);
  - a "Cancel RFQ" button next to "Cancel" (NF-12);
  - money labelled "Size" (NF-08);
  - mixed date formats and raw ISO dates (F-23).
- **Prove it:** one label table, one date formatter, one money formatter, used everywhere.

### 24. Test on the user's real screen
- **Instinct:** the buyer has a 1366×768 laptop at 125% scaling, not your monitor.
- **Missed:** at 1366px:
  - the next step was hidden (FV-04);
  - folders sat below a dashboard, off-screen (R1);
  - tables were clipped (NF-07);
  - chart text was 6px tall (NF-06);
  - an icon was blurry at 125% (NF-05).

### 25. When data lands wrong, say so loudly
- **Instinct:** silent fallbacks hide bugs from the one person who'd catch them.
- **Missed:** moved materials silently became $0 when the contract had no quote, or the wrong one (the original user bug). The fix was a visible refusal: "N have no price yet".

## C. Process

### 26. "Fixed" means proven, not claimed
- **Missed:**
  - tab separators were claimed fixed and never drew (T2);
  - change-order Print was "fixed" and printed blank (F-16 → FV-02);
  - the CSRF cleanup missed Sign out (4.10).
- **Rule:** every fix comes with the repro that failed before and passes after. Verify with an independent pass, not the author's word.

### 27. Fix the class, not the instance
- **Missed:** atomicity, double-submits, bad input and stale data were each fixed route by route, and new routes brought them back (S-V03, S-V06, S-V12).
- **Rule:** one shared guard that every route passes through, plus a permanent test that fails when a new route skips it.

### 28. Fixes make bugs
- **Missed:** a pass-1 fix caused the Ctrl+Z white screen (FV-01). A new rule (ADR-028) left four ways around it (S-V01).
- **Rule:** after every fix pass, re-run the *whole* battery, not just the fixed items.

### 29. Freeze features while stabilizing
- **Missed:** ADR-028 features landed mid-fix and brought new bugs at the old rate, which muddied whether the fixes were converging.

### 30. Measure with a fixed yardstick
- **Missed:** each audit went deeper than the last, so the drop in bug counts can't be trusted as convergence.
- **Rule:** the same battery every pass (`testing/TEST-BATTERY.md`). Track defects by severity and regressions caused by fixes.

### 31. The reviewer mustn't be the author
- **Missed:** AI wrote the code and AI-adjacent checks passed it (100% coverage, all green). Independent reviewers given only the code, not the author's reasoning, found 91 bugs, then 57 more.
- **Rule:** a separate reviewer with a fresh context, report-only, required to reproduce each claim (`testing/REVIEW-METHOD.md`).

### 32. Green checks prove intent, not behavior
- **Missed:** 813 tests at 100% branch coverage, and still a white-screen crash, data loss and double-billing.
- **Rule:** coverage shows the code ran, not that it's right. Add the behavior tests: fuzz, race, double-submit, stale, atomicity, the end-to-end walk, and real size.

### 33. Domain testing finds what code review can't
- **Kept:** the $0 prices and the AFP dead end came from doing the real job, not from any test.
- **Rule:** keep doing it. Turn every real-job session into a scripted walk, so it re-runs every pass.

### 34. Decide the direction before polishing
- **Missed:** the UI was rebuilt four times (ADRs 021, 023, 024, 027). Each rebuild reset the bug count.
- **Rule:** settle the look and the workflow with screenshots or mock-ups first, then build once.

### 35. "Offline" is proven by cutting the network, not by grep
- **Missed:** the code read clean, but running it in an isolated network showed the launcher's health check goes through the system proxy (OFF-01). Then there's Kerberos to the domain controller (OFF-02), Edge's own sync and spellcheck (OFF-03), and no Cache-Control (OFF-04).
- **Rule:** `testing/OFFLINE-ISOLATION.md`: a namespace, strace on `connect()`, a browser request log, then the Windows firewall proof.

### 36. Check the license when you add the asset
- **Missed:** Icons8 free icons in a company app need a paid license or a visible link. The MIT notices for React and Fluent were dropped from the bundle (`context/LICENSING.md`).

### 37. The docs' front door matches today
- **Missed:**
  - the README still said the old app name and named old ISO paths;
  - the ADR index had stale statuses;
  - an old audit was presented as current;
  - there was no buyer guide and no IT/backup guide.
- **Rule:** README, a user quick-start and an IT install/backup/restore guide get updated with each release.

### 38. Someone else must be able to run it
- **Missed:** one person understands the design, and nobody reads the code.
- **Rule:** learn to read the risky parts yourself: money, saving data, two people at once, permissions. Have a second human review those.

### 39. Prove the test catches the bug
- **Instinct:** a passing test means nothing until you've seen it fail on the bug it guards.
- **Kept (pass 2):** the permanent atomicity test was run with the fix turned off and caught exactly the audit's three leaks. Do the same for every guard test: double-submit tokens, stale-save refusal, fuzz.
- **Prove it:** revert or disable the fix, confirm the test fails, restore it. Note it in the RTIRR entry.

### 40. A changed test expectation needs a reason
- **Instinct:** when a fix changes what old tests expect, each change is either the fix working as intended or a bug being hidden. Assume the second until shown otherwise.
- **Missed risk (pass 2):** "a few totals in older tests changed" after the AFP amount rule.
- **Rule:** every edited expectation gets a one-line reason in the RTIRR entry. The money walk is re-checked against hand math, never edited to pass.

## D. Added during pass 2

### 41. The governing documents live in the repo
- **Instinct:** the prompt, spec or plan that a pass works from is part of the code. It's committed, indexed and checksummed, so a lost or cut-off copy can't go unnoticed.
- **Missed:** the pass-2 prompt lived on the Desktop. When the folder vanished, the agent rebuilt it from session history, cut off at line 575 of 1,985, and kept working. It missed the data-integrity list, so two database constraints were never asked for (O-03, O-08). A guard test was also nearly lost in a `git stash` (O-11).
- **Ask:** if this machine died now, could the next session find every document this work depends on, whole?
- **Prove it:** an index of governing documents with SHA-256s, plus a test that fails when one is missing or differs. Unfinished work goes on a named branch, never a stash.

### 42. Expected numbers come from outside the code, and must be able to tell values apart
- **Instinct:** a test's expected value is worked out by hand or in a spreadsheet, never by running the code. Each assertion uses values that can't be confused with each other.
- **Missed:**
  - the money walk's inputs were built to hit published totals; it turned out independent, but only a recomputation proved it (O-07);
  - in the takeoff walk, billed and balance were the same number, so a swap would pass (O-05);
  - the reviewer's own prompt had a wrong figure, and the coding agent caught it (O-10).
- **Ask:** where did this expected number come from? If two fields were swapped, would this test notice?
- **Prove it:** recompute every expected figure from the inputs outside the app (plain arithmetic, a spreadsheet). Choose test data so related figures differ.

### 43. One machine, many people
- **Instinct:** on a single-machine install, everyone shares one address, one browser profile and one disk. On a server, everyone shares its caches. Anything keyed by "the machine" is keyed by everyone.
- **Missed:**
  - a new account saw the previous person's tabs, Recent places and Favorites (4.5);
  - anyone could empty everyone's Recycle Bin (S-01), and a restore then Shift+Delete got around the fix (S-V04);
  - Edge's cache and sync hold everyone's pages (OFF-03, OFF-04);
  - a login throttle keyed by address would lock every user out at once (O-09);
  - Django: six advisories where a server cache served one user's response to another, e.g. no `Vary: Authorization` (DJ-101) and cached `Set-Cookie` responses (DJ-095).
- **Ask:** what is keyed by machine, address, browser or a shared cache here, and should it be keyed by person?
- **Prove it:** two accounts on the same browser and address, in sequence and at once. Nothing of one shows to the other, and one person's mistakes don't lock out the other. Behind a server cache, two users request the same page and the second never gets the first's.

### 44. What you show is what you save
- **Instinct:** a value shown for editing must round-trip unchanged. Displayed decoration (prefixes, formatting, rounding) never ends up back in storage.
- **Missed:**
  - renaming "PO 12345" in place saved "PO PO 12345", and AFPs did the same (3.7);
  - unit prices shown rounded to cents didn't add up (F-08).
- **Ask:** if the user opens this field and saves without typing, does the stored value change?
- **Prove it:** for every editable field, open then save with no change, and assert the stored value is identical.

### 45. Selection follows what's on screen
- **Instinct:** a range selection is the visible rows in visible order, from the anchor to the focused row. Hidden, filtered or unchoosable rows never sneak in, and never stop the range.
- **Missed:**
  - Shift-click after a filter selected hidden items (4.6);
  - a Shift range lagged on unchoosable rows (FV-10);
  - Shift+click on a name toggled one row (FV-11).
- **Prove it:** select ranges after filter, sort and refresh, and across rows that can't be chosen, with the mouse and the keyboard.

## E. Approved 2026-10-31 from the ledger

Drafts approved because the ledger showed they were real: at least 6 findings across the projects, or a hit in the developer's own project. Numbered in cost order at approval. Their drafts, with the full evidence, stay in `proposals/`.

### 46. Security basics on every change
- **Instinct:** secrets, passwords and crypto, object ownership, injection, and what errors and logs reveal get checked on every change, not saved for a security review. Identifiers that reach SQL, a shell, a path or a parser come from an allowlist, never a denylist that grows one character per incident.
- **Missed:**
  - Django, 16 advisories and review catches: SQL injection through column aliases with control characters, `#` and `$`, patched one character at a time (DJ-117, DJ-123, DJ-119, DJ-125); a `_connector` keyword and dotted names reaching SQL (DJ-122, DJ-118); a path check by `startswith` that let a sibling folder be written (DJ-124); CRLF in logged paths forging log lines (DJ-126); internal exception text in a 400 response (DJ-033); stored URLs rendered as links without checking the scheme (DJ-094);
  - PrivateApp: vendor downloads ran cell formulas (S-V07, under #12);
  - measured: AI-written files carry about twice the high-severity security alerts of human ones (`knowledge/HUMAN-REFERENCE.md`).
- **Ask:** is any secret in the diff? Does every route that takes an id check that this user may see that record? Does any request data reach a shell, a query, a path or a parser unescaped? What does the error message show?
- **Prove it:** grep the diff for keys, tokens, passwords and private-key headers. User A requests user B's record id, expecting 403 or 404. Feed each identifier input a control character, `#`, `$`, `.` and a newline, expecting a refusal. Force an error and read the response body and the log for internals.

### 47. Their machine is not your machine
- **Instinct:** code is untested on any OS, database backend or version, runtime, display server, DPI or install path you didn't run it on, and a fix there isn't fixed until it has run there.
- **Missed:**
  - Ferrite: glibc too new for users (FE-012); macOS packaging, three times (FE-019, FE-080, FE-147); IME coordinates (FE-095); fixes "done" pending hardware nobody had (FE-102, FE-110, FE-111);
  - Django: a per-column parameter count that broke past one backend's limit (DJ-003, DJ-026); JSON lookups on databases without native JSON (DJ-053); functions MariaDB later removed (DJ-086); Unicode normalisation that is slow only on Windows, a denial of service (DJ-111, DJ-121, DJ-128).
- **Ask:** which rows of the platform matrix (OS, database and version, runtime, browser, display) did this change actually run on?
- **Prove it:** a matrix with an owner per row, and "fixed" only when that row has run. Include the oldest supported version of each. For PrivateApp that's the disc's Windows, Edge and PostgreSQL.

### 48. Compare and key in one canonical form
- **Instinct:** when one thing has several spellings (case, padding, quoted or not, `name` vs `name_id`, `_` vs `-`), every comparison, lookup and map normalises first. When different things are joined into one key, the key must still tell them apart.
- **Missed:** Django: constraint checks registered `field.name` only and crashed on `author_id`, then the same fix shipped as a regression at a second site (DJ-070, DJ-071); a quoted id compared with an unquoted one (DJ-030); permission renames matched other models' permissions (DJ-032, DJ-080); `key + salt` signer namespaces collided, `Private` and padded `Vary` tokens slipped past case-sensitive checks, and `X_Header` and `X-Header` landed on one key (DJ-098, DJ-100, DJ-102, DJ-106).
- **Ask:** how many spellings can this value have, and does every comparison normalise them the same way? Can two different pairs join into the same key?
- **Prove it:** a table test over every spelling, expecting one result. For each composite key, two different inputs that concatenate to the same string, expecting different keys.

### 49. Bytes are not characters
- **Instinct:** every index into text says which unit it is: byte, character, grapheme or screen column. Every slice, length and buffer size is checked against that unit.
- **Missed:**
  - Ferrite: crashes in the tree viewer, binary stats and paste (FE-015, FE-092, FE-117); highlights drifting (FE-021, FE-039, FE-045); CSV and terminal widths (FE-101, FE-137); line operations still crashing in the current code (FE-L01);
  - Django: non-UTF-8 bytes passwords crashed two hashers (DJ-057); `sys.getsizeof()` used as a buffer length read past the buffer (DJ-096).
- **Ask:** what unit is this number in, who produced it, and what happens when the character at that position is 2, 3 or 4 bytes?
- **Prove it:** run every text action over a fixture of accented letters, CJK, emoji with joiners and combining marks, with the cursor just after a multi-byte character, and with bytes that aren't valid UTF-8.

### 50. A cache key must tell its contents apart
- **Instinct:** a cache, version counter or "same length means same" shortcut is only safe if no real change, and no other user, can leave the key equal. Everything that changes the answer is part of the key.
- **Missed:**
  - Ferrite: `is_modified` keyed on a counter that writers forget to bump (FE-113); a per-tab counter used across tabs (FE-125); a sampled hash and a same-length check in the current code (FE-L06, FE-L07);
  - Django: responses cached without `Vary: Authorization`, serving one user's page to another (DJ-101); `Set-Cookie` responses cached (DJ-095); two different `Vary` headers producing one key after a fix (DJ-014); cached model metadata never expired (DJ-004).
- **Ask:** what change, or which other user, leaves this key the same? What gets served or written back from the stale value?
- **Prove it:** for each cache, change the content while holding the key's inputs constant, and request as a second user. Assert a miss, and no stale write-back.

### 51. A shortcut gives the general path's answer
- **Instinct:** an optimisation that answers without going through the general path (a count without the join, a bulk insert without save, a "nothing to change" skip) must give the same result, side effects and signals as the general path for every input the general path accepts.
- **Missed:** Django: every count was 0 for a many-to-many on `to_field` (DJ-036); admin logging moved to a bulk insert that sends no signals (DJ-037); an insert loop that re-implemented a save step and dropped database-filled fields, two regressions from one optimisation (DJ-046, DJ-047); a rename skipped because "only the name changed" (DJ-054); a fast bulk path that truncated strings, then a fix that disabled it for every model with a foreign key (DJ-044, DJ-074).
- **Ask:** what does the general path do that this shortcut doesn't? Is there an input where the two answers differ?
- **Prove it:** a differential test: the same inputs through the shortcut and the general path, asserting identical results, side effects and signals.

### 52. Falsy, empty, None and "the database decides" are different values
- **Instinct:** `if x:` asks whether x is truthy, not whether it was given. Empty, zero, None, SQL NULL, JSON null and a "use the default" marker each mean something different and each needs its own test. This extends #4 from forms to code.
- **Missed:** Django: an empty filter, falsy but not None, turned into None, caught in one review and shipped elsewhere as a crash (DJ-027, DJ-064); None saved as JSON null instead of SQL NULL, then the fix flipped a filter the other way (DJ-042, DJ-043); the "database decides" marker read as "not set", so a Python default overrode the database's (DJ-048); a parameter that used to crash silently stored NULL (DJ-052).
- **Ask:** what does each falsy value mean here, and does `if x:` mean the one I intend?
- **Prove it:** a parametrised test over None, empty containers, 0, False and every marker the code accepts, with a distinct expected result for each.

### 53. Text round-trips byte for byte
- **Instinct:** open, view, copy or edit one part, and save: every byte you didn't intend to change is identical, including newlines, trailing spaces, inline markup, BOM and encoding. This extends #44 from fields to files.
- **Missed:** Ferrite: a table edit stripped formatting (FE-104); trailing spaces dropped (FE-098); newlines stripped (FE-054); copying added spaces (FE-093); headings misparsed (FE-090, FE-096); encoding changes and save discarding text in the current code (FE-L04, FE-L05).
- **Ask:** what does this view or serializer drop or add that the source didn't have?
- **Prove it:** a golden-file corpus (CRLF, BOM, trailing spaces, tables with inline markup, Windows-1252, UTF-16) opened and saved through each view. Assert byte-identical output except for the intended edit. File I/O always names its encoding.

### 54. List every type the value can be
- **Instinct:** a "string" can arrive as a string subclass, a lazy translation, bytes (valid UTF-8 or not), a number, an address object or None. A check written for one of them decides wrongly for the others.
- **Missed:** Django: `isinstance(path, str)` also caught safe strings, so their assets were percent-encoded (DJ-072); a lazy translation failed `startswith` (DJ-055); validators crashed on non-strings after a length guard was added (DJ-002, DJ-062); a blocklist checked strings and dicts and let bytes reach a network fetch (DJ-089).
- **Ask:** what types can actually arrive here, from callers, templates, translations and the network?
- **Prove it:** a parametrised test feeding each realistic type, asserting the intended branch for each.

### 55. Every key has exactly one owner
- **Instinct:** each default shortcut is unique, wired to a handler, and not swallowed first by an inline widget or an input-method composition. This extends #20.
- **Missed:** Ferrite: View Mode bound to the paste shortcut (FE-006); a fix that created its own collision (FE-064, FE-065); IME Backspace deleted committed text (FE-091); an inline widget ate Ctrl+Home (FE-141).
- **Ask:** what else is bound to this, what OS convention does it shadow, and who sees the key first?
- **Prove it:** a test that every default binding is unique and dispatched; global keys tested while an inline editor has focus; an IME composition test with Backspace, Enter and arrows.

### 56. Durable data carries durable identity
- **Instinct:** anything that outlives the process (recovery files, per-file settings, run output, undo history) is keyed by something that also outlives it, and restoring must not rewrite the baseline it is compared against.
- **Missed:** Ferrite: recovery keyed by a tab id that restarts each launch overwrote a real file (FE-129); a restore made the recovered text the "original", so a second crash lost everything (FE-130); a clean exit deleted recovery (FE-148); run output keyed by line number (FE-151).
- **Ask:** what is this keyed by, and is it still unique after a restart? After a restore, what does "modified" compare against?
- **Prove it:** crash, restore, edit, crash, restore, with items opened in a different order and the file missing or renamed. Every edit comes back in the right place, still marked unsaved.

### 57. An override point is an API
- **Instinct:** a method others override, a template block others extend, an attribute others read, a type others store, and a default others rely on are contracts, documented or not. Changing their signature, name, return type or default breaks code you can't see.
- **Missed:** Django: every model overriding a documented method crashed when a new argument was passed to it (DJ-051); a bug fix changed a public method's signature and return type (DJ-038); a hard-coded check overrode subclasses' `required=False` (DJ-063); an attribute a large third-party project used was repurposed (DJ-059); moving a template block broke projects' templates (DJ-084).
- **Ask:** who overrides, extends, stores or reads this from outside, and does the change keep their code working or warn them first?
- **Prove it:** an old-shape compatibility test per extension point: the old override signature, a template extending the old block, a stored-object round trip.

### 58. Unstated defaults are decisions
- **Instinct:** every default value, fallback, limit and special case is a business decision. If it isn't written in the spec, an ADR or a recorded decision, the code invented it.
- **Missed:**
  - PrivateApp: switching a contract to another vendor's quote silently kept the old vendor's prices (O-04, decided: refuse and name the lines); an AFP quantity of 0 or blank billed the whole received quantity (S-03); uploads stopped reading after a 100-row gap nobody chose and said nothing (IR-012);
  - Django: system checks silently ran against no databases (DJ-065); a CVE fix reused a 2048-character limit that rejected legitimate redirects (DJ-073);
  - measured: about a third of AI patches that pass the tests differ from the human fix on edge cases (`knowledge/HUMAN-REFERENCE.md`).
- **Ask:** who decided this value or branch, and where is it written?
- **Prove it:** list every default, fallback, limit and special case the change adds. Each traces to a written decision; anything else goes to the developer as a question, and the test comes from his answer, not from the code. The devArchitect does this before the build.

### 59. One point, one owner
- **Instinct:** every pixel of the window chrome has exactly one owner for press, drag and release, and paint order matches that owner.
- **Missed:** Ferrite: the Linux title bar, four times (FE-020, FE-037, FE-042, FE-055); a button inside a resize zone (FE-036, FE-142); FE-132, FE-140.
- **Ask:** for this control, what else is under the pointer, and which one wins on release?
- **Prove it:** scripted presses and drags at every edge, corner and title-bar control, at 100%, 125% and 150% scaling, on each OS.

### 60. Every glyph needs a font that has it
- **Instinct:** a character you draw is only visible if a loaded font contains it, on the user's machine and in the user's language.
- **Missed:** Ferrite: missing glyphs, one fixed twice (FE-011, FE-013, FE-048, FE-049); a UI language switch showing boxes (FE-084, FE-085).
- **Ask:** which font draws this if the user has none of my fonts and the UI is in another language?
- **Prove it:** a coverage test of every UI string, icon and locale file against the shipped fonts, and a launch in each UI language with an empty system font folder.

### 61. Widget identity never depends on what it edits
- **Instinct:** a control's identity and focus must survive the user's own keystroke, an insert above it, and a switch between tabs.
- **Missed:** Ferrite: a cell lost focus on every keystroke (FE-026); scroll state leaked across tabs (FE-103); two clicks needed and a vanishing caret (FE-120, FE-121); FE-025, FE-070.
- **Ask:** when the user types one character, does any id, index or key in scope change?
- **Prove it:** a scripted run that types into, inserts above and switches between each editable item, asserting focus and caret, including two tabs with identical content.

### 62. The running environment is part of the change
- **Instinct:** the checks build a fresh world; the app runs in an old one. A change that needs a migration, a setting, a package or a file isn't done until every place that serves it has it. Until then, that place refuses to serve and says why. Related to #32 and #47.
- **Missed:** PrivateApp: migrations 0032–0035 were committed but the dev database stayed at 0031, so every sign-in in the dev app was a server error while every closing check was green (IR-015). The agent reported "the dev database is still at 0031" as a state, never the consequence.
- **Ask:** what does the running app need that the tests build for themselves, and which running environment is behind the code right now?
- **Prove it:** the closing checks run the framework's drift check against each serving database (`manage.py migrate --check` in Django). Leave a database one migration behind and the checks go red, and the app answers with a named reason instead of a 500. Report a known gap with its consequence, never as a bare state.

### 63. A test that fails sometimes is failing
- **Instinct:** a test that passes on one run and fails on the next is a failing test. Green means green every run, in any order, alone or with the rest.
- **Missed:** PrivateApp: an Explorer test failed 1 run in 3 when run alone, before and after the fixes, so "every check passes" rested on a gate that could go either way (IR-006).
- **Ask:** run alone three times and in a different order, does it give the same answer? Does it wait for the exact thing it checks?
- **Prove it:** run each new or changed test file three times alone and once shuffled. Any mixed result is a finding. Wait on the specific element, never on a container another element can satisfy first.

---

## Checklist (paste into a prompt)

Before calling any feature done, answer each with a test, not a sentence. The `[#n]` after each line is the instinct it checks; findings and the ledger always use instinct numbers, never checklist line numbers.

1. If the second write fails, is the first rolled back? Is there one event per action, even on retry? [#1]
2. Same request twice, 1 ms apart: one result? [#2]
3. Two users on the same record at once: consistent data and a clear refusal for the loser? [#3]
4. Partial form: are unsent fields untouched? [#4]
5. Stale screen: is a stale save refused? Is a late response ignored? [#5]
6. Every route that can break this rule: does each one check it? [#6]
7. Undo after someone else changed something: are only this action's changes reversed? [#7]
8. After a failure, does the next action still work? [#8]
9. NUL, Infinity, huge numbers, letters in ids, 100k rows: no 500? [#9]
10. Every money figure equals hand math to the cent, with edge cases at 0, the balance, balance + 0.01 and negative? [#10]
11. Dates in order, none in the future, derived dates anchored right? [#11]
12. `=1+1` in every exported text field comes out as text? [#12]
13. 500 rows: are query counts flat? Is every interaction under 100 ms at 4× CPU? [#13]
14. Migration forward, back, forward on real data: works, or refuses before changing anything? [#14]
15. Every disabled control says why? [#16]
16. A new user can find the next step at 1366×768 and 125% scaling? [#17, #24]
17. 500, network drop and expired session each give a clear message, keep the input, and never show a false success? [#18, #21]
18. A crash in one view leaves the app usable? [#19]
19. Shortcuts are off while typing? [#20]
20. Focus returns after dialogs? [#22]
21. Same action, same name, same format everywhere? [#23]
22. Proved fixed by a repro that ran, and verified by someone other than the author? [#26, #31]
23. The whole battery re-run after the fix pass, with regressions counted? [#27, #28, #30]
24. Offline proven with the network cut, not by reading the code? [#35]
25. New assets license-checked? Docs updated? [#36, #37]
26. A failure after a file write leaves no file? Files deleted only after commit? [#15]
27. Each guard test seen failing with its fix turned off? [#39]
28. Every changed test expectation has a written reason, and the money walk still matches hand math? [#40]
29. Governing documents committed, indexed, checksummed? Unfinished work on a branch, not a stash? [#41]
30. Every expected figure recomputed outside the app? Related figures in the test data differ? [#42]
31. Two people on one machine or behind one cache: nothing leaks between them, and nothing keyed by address locks everyone out? [#43]
32. Open then save with no change leaves every stored value identical? [#44]
33. Ranges after filter, sort and refresh take only visible, choosable rows? [#45]
34. No secret in the diff, every id checked for ownership, identifiers from an allowlist, no internals in errors or logs? [#46]
35. Run on every OS, database version, runtime and browser it ships to, oldest supported included, before "fixed"? [#47]
36. Every comparison normalises all spellings, and no two different inputs share a key? [#48]
37. Every text action works after multi-byte characters and with bytes that aren't UTF-8? [#49]
38. Every cache misses when the content changes and when another user asks? [#50]
39. Every shortcut tested against the general path on the same inputs, with the same results and side effects? [#51]
40. Every truthiness test checked against empty, zero, None and each marker, each with its own result? [#52]
41. Open, edit one part, save: every other byte identical, and every file read and write names its encoding? [#53]
42. Each type check tested with every type that can really arrive? [#54]
43. Default shortcuts unique and all dispatched, and none swallowed by an inline editor or IME? [#55]
44. Two crash-and-restore cycles: every edit back, in the right place, still marked unsaved? [#56]
45. Every override point, template block or stored type the change touches has an old-shape compatibility test? [#57]
46. Every default, fallback, limit and special case traces to a written decision? [#58]
47. Every edge, corner and title-bar control does one thing at 100/125/150%, on each OS? [#59]
48. Every UI string and icon renders in every UI language with only the bundled fonts? [#60]
49. Typing, inserting above and switching tabs keep focus and caret in every editable item? [#61]
50. Every database and machine the app serves from is at what the code needs, checked by a command, and the app refuses loudly when it isn't? [#62]
51. Each new or changed test gives the same result alone, three times, and in shuffled order? [#63]
