# monize: issue drafts, batch 2 (control round `2026-11-02-93f4e68-control`)

Drafts 1 to 5 were posted on 2026-11-07, in their order, as #2070, #2071, #2072, #2073 and #2074, on Garrett's written go for this batch (`testing/FILING.md` §8), after FILING §3's re-check made again that day, and with no label; the posted bodies, byte for byte, are in `issues-batch-2/`, one file per issue, named by its number. Draft 6 is held, not posted, on Garrett's decision of that day under FILING §3, since #2042 rewrote its cited line after the read (`metrics/FILED.md`, *Held back*). Written 2026-11-07 by the architect, under `testing/CONTROL.md` §15 and FILING §3 to §5, from `verdicts.private.md`, `score.md`, `key.private.json` and the claims in `claims.private.md`.

**Target:** `kenlasko/monize`, `main` at `f3799f08979aaf20e177f9f2907f54dd21594c9e` (`f3799f0`, committed 2026-11-07 14:53 UTC; `gh api --method GET "repos/kenlasko/monize/commits?sha=main&per_page=1" --jq '.[0].sha'`), 400 commits after `93f4e68`, the sha every run and the judge read, and 278 after `051655e`, batch 1's. The re-check began at 14:46 UTC on `b89b1c7` (`b89b1c72a3843cfb474c62e83849da9a727a3452`, committed 13:32 UTC), and `main` moved to `f3799f0` while it ran, by the 20 commits of #2066 (the in-app help's header menu). Every file read below has the same blob at the two but the Budgets list page, where #2066 added a help link, so the drafts name `f3799f0` with the line numbers read at `b89b1c7`. `main` is again the repo's only branch (an agent's work branch for #2066 stood beside it until that merged), so there is no dev branch to re-check (FILING §3).

**The form:** monize still has no issue template on `main` (the tree holds no `.github/ISSUE_TEMPLATE`, and the community profile's `issue_template` is null), so FILING §5's form is used as it stands. `CONTRIBUTING.md`, `SECURITY.md`, `.github/pull_request_template.md` and `docs/agent-instructions.md` are the blobs batch 1 read at `051655e`, so no rule on AI-assisted or AI-generated reports has appeared since (`reviews/monize/2026-11-02-ai-policy-check.md`); `AGENTS.md` changed only its line on money precision.

**The order:** batch 1's (CONTROL §15), unchanged: batch 2 is groups 1 to 6, each wrong-result by the judge's final verdicts, in the judge's group order.

| Batch | Groups in order, with their claims in `claims.md` order |
|---|---|
| 1 | 8 (VF, KR), 9 (ZD), 10 (TG, XX, LH, JH), 12 (MN, TX), 18 (GG), 21 (SL): data-loss; posted 2026-11-05 as #2025 to #2030 |
| 2 | 1 (VM, ML, XT), 2 (HG), 3 (MV), 4 (ZX), 5 (CT), 6 (MG): wrong-result |
| 3 | 7 (GN, VP, JK): crash; 14 (DR, WV), 15 (FP, LM): wrong-result; 17 (GC): crash; 19 (JN, QR), 20 (WF): wrong-result |
| 4 | 23 (PC): wrong-result |

**Where the steps start** (Garrett's instruction of 2026-11-07, after the maintainer closed #2027 and #2029 as not reachable in practice): each draft's steps start from an action a user takes in the app, on a screen, with a button or by an import, wherever the group's bug allows it, the app's own doors read on `main`: its screens' calls, the edit form's routes, and the fields of the assistant's and the MCP tools' actions. Where only a crafted input reaches the bug, a hand-made API call, a malformed file or a race needing two connections, the steps say so where it is needed. A file in a form that bank or spreadsheet exports write counts as a user's import, though the user guide may not list the form. These criteria are the architect's reading (2026-11-07), for Garrett to confirm. One draft rests on a crafted input: draft 3 (group 3), reached only by a hand-made API call.

## The re-check and the duplicate search (FILING §3), 2026-11-07

Every cited file was fetched read-only at `93f4e68` and at `b89b1c7` (`gh api --method GET "repos/kenlasko/monize/contents/<path>?ref=<sha>" -H "Accept: application/vnd.github.raw"`), each checked against its tree's blob sha (`gh api --method GET "repos/kenlasko/monize/git/trees/<sha>?recursive=1"`), and the cited lines compared; the tree at `f3799f0` gives each the blob it has at `b89b1c7`. *Unchanged* means the same blob at `93f4e68` and `main`; *moved*, the same code at new line numbers; *changed*, the cited line itself rewritten since the read. Of the 400 commits since `93f4e68`, the ones that touch the six groups' files come from merged pull requests: before `051655e`, #2001, #2003, #2015 and #2023, away from the cited lines; since, batch 1's fixes #2034 (closing #2028), #2035 (closing #2030) and #2037 (closing #2025), #2041 (closing #2039, the follow-ups of #2037) and #2043 (closing #2040, #2030's), and #2042 (money stored at eight places, rounded per currency, merged 2026-11-06 as `f73f6de`), which reaches every group but group 4; and #2024, #2063 and #2065, away from the cited lines. What each does to a group is said under it. No group's mechanism is fixed on `main`, and no group is filed upstream, so all six are drafted and none is held back. Group 6 is *changed*: drafted on `main`'s code, and Garrett may hold it (under it). Drafting a group whose cited line was rewritten, while its confirmed outcome holds on `main`, is the architect's reading of FILING §3's "changed since the read" (2026-11-07), for Garrett to confirm.

Each search ran in batch 1's four forms: `gh search issues --repo kenlasko/monize "<words>" --limit 50` and `gh search prs --repo kenlasko/monize "<words>" --limit 50`, both states (gh searches the quoted words as a phrase), then `gh issue list` and `gh pr list --repo kenlasko/monize --state all --search "<words>" --limit 50`, which search the words apart (*50* there is the limit); the 72 calls ran from 15:04:51 to 15:07:48 UTC. As a cross-check, the titles and bodies of all 1,916 issues and pull requests (`gh api --method GET "repos/kenlasko/monize/issues?state=all&per_page=100" --paginate`, read at 15:08 UTC) were searched for the function names and the user's words below. The one open pull request, #1883 (accrual accounting, 638 files, conflicted, last updated 2026-11-02), closes no issue and changes ten of the cited files; what it does to each group is said under it.

- **Group 1 (draft 1).** Moved. `CURRENT_DATE` bounds the undo's recompute at `action-history.service.ts:2226` (`93f4e68`: 2111; the method 2197-2247, was 2086-2129) and the import's at `import-post-processing.service.ts:86` (was 81); #2042 changed only how each rounds its sum, per currency. `recalculateCurrentBalance` still binds `todayYMD()` (`accounts.service.ts:1984`, `:1988`; was 1747, 1751), and the hourly job's seven-day window is the same (`:2823-2832`, `DUE_BALANCE_CATCH_UP_DAYS` at `:323`; was 2519-2528, 263). The same bound in `net-worth.service.ts:2854`, `:2942` (was 2849, 2937) and `portfolio-calculation.service.ts:680`, `:2592` (was 681, 2586). `date-utils.ts` and `scoped-db.ts`: unchanged; no time zone is set on the database connection (`backend/src/app.module.ts`) or on the `postgres` service (`docker-compose.prod.yml`). The rest of these files' changes, #2001's, #2023's, #2024's, #2034's and #2063's, are elsewhere. Searches: "CURRENT_DATE": issues none, PRs #447, #1816, #317, words none and the same three; "balance timezone": issues none, PRs none, words 7 and 20; "undo balance": issues none, PRs none, words 11 and 26. Bodies: `CURRENT_DATE` 3 (#1816, #447, #317), `recalculateBalance` 1 (#1816), `import-post-processing` none, an undo beside a balance's day or time zone none. None reports this. Nearest: #447 (merged 2026-04-24), which bound two balance queries by `todayYMD()` instead of `CURRENT_DATE`; these two recomputes kept it. #1883 changes neither bound.
- **Group 2 (draft 2).** Moved. `void-status-transition.util.ts`: unchanged (the write at `:136`). `transaction-reconciliation.service.ts` changed below the cited lines (#2042, the reconcile screen's rounding) and gained five import lines above them, so `updateStatus` is `:237-257` (was 232-252), the reconciled-date stamp `:167-175` (was 162-170), the mirror call `:213-219` (was 208-214) and the reconcile route's refusal `:316-323` (was 311-318). `transactions.service.ts`: the generic update's VOID crossing `:3322-3339` (was 3103-3120) and its reconciled date taken from the body only `:3237-3238` (was 3018-3019), the same code. The edit form saves a transfer through `updateTransfer`, whose VOID-crossing pairing is `transaction-transfer.service.ts:2196-2268`, the same lines as `93f4e68`'s 1998-2070; the re-check read it as the app's own door to this state, so it carries the steps. Searches: "void reconciled": issues #2053, PRs #2065, #1169, #438, words 8 and 20; "unvoid": none in all four; "applyVoidTransitionToMirrorLeg": none in all four. Bodies: `applyVoidTransitionToMirrorLeg` none, "un-void" or "unvoid" 2 (#1816, #1129), "sub-status" none, VOID to RECONCILED none. None reports this. Nearest: #1147 (merged 2026-08-13), which made VOID pair-wide and kept Cleared, Reconciled and the reconciled date on the leg being changed; `updateTransfer`'s comment (`:2248-2252`) leaves the un-void sub-status open. #1883 adds an accrual check to the status route and leaves the mirror write alone.
- **Group 3 (draft 3).** Moved. Group 2's lines, and `reconciled-lock.util.ts` and `remove-transaction-leg.ts`: unchanged. The status route asks the lock of the requested row only (`transaction-reconciliation.service.ts:135-140`, was 130-135), and the generic update too (`transactions.service.ts:2959`, was 2813). The claim's split side, the legs a split parent holds in other accounts deleted after a lock check on the parent only, is fixed: #2041's `8731bb8` (merged 2026-11-06, closing #2039) locks and asks each such leg before the first write, so it is in the draft's *Related*, not its *Result*. The web app's doors to a status change, read on `main`: the register's status cycle has no VOID (`frontend/src/lib/transaction-status-cycle.ts:12-16`, `:31-39`); the edit form saves a transfer through `updateTransfer`, which asks both legs (`transaction-transfer.service.ts:2162-2164`); the bulk edit adds the counterparts before its check (`transaction-bulk-update.service.ts:255-262`, `:340-345`); and the assistant's and the MCP tools' edit actions carry no status (`backend/src/ai/actions/ai-action.types.ts`, `backend/src/mcp/tools/transactions.tool.ts`). So only a hand-made API call reaches it. Searches: "lock reconciled transactions": issues #1937, PRs #1940, #1303, #1221, #1202, words 7 and 17; "void transfer counterpart": issues none, PRs none, words 7 and 16; "assertReconciledRowsMutable": issues #1815, PRs #1221, the same by words. Bodies: `assertReconciledRowsMutable` 2 (#1815, #1221), a counterpart beside a reconciled lock 8 (#1940, #1937, #1816, #1815, #1528, #1147, #1096, #369), "mirror leg" 4 (#1942, #1816, #882, #880), `void-status-transition` none. None reports this. Nearest: #1815 (fixed by #1816), each branch of the transfer edit and delete asking the lock; #2039 (fixed by #2041), the split side. #1883 leaves the mirror write and its lock alone.
- **Group 4 (draft 4).** Unchanged: `budget-date.utils.ts`, `budgets.service.ts`, `budget-reports.service.ts`, `budgets.controller.ts`, `date-utils.ts` and the client's `frontend/src/lib/budgets.ts` are the same blobs; the Budgets list page changed only its help link. Searches: "budget current period": issues none, PRs none, words 4 and 18; "getCurrentMonthPeriodDates": issues #1825, PRs none, words 1 and none; "budget month timezone": issues none, PRs none, words none and 4. Bodies: `getCurrentMonthPeriodDates` 1 (#1825), `budget-date.utils` none, `getUTCMonth` none, a budget beside UTC or a time zone 3 (#1489, #1353, #70). None reports this. Nearest: #1825 (closed), the next period after a close dated from the wall clock, another path. #1883 keeps `getCurrentMonthPeriodDates` as the current period's source.
- **Group 5 (draft 5).** Moved. `parseCsvAmount` is byte for byte `csv-parser.ts:923-942` (was 804-823), and `amount-separators.util.ts` is unchanged; #2035's fix (closing #2030) moved the row loop's amount read into `readRowAmount` (`:1225-1252`, its three fallbacks to 0 at `:1230`, `:1239`, `:1243`, was 1205, 1213, 1218) and reports an unreadable date by row (`:1419-1428`), not an unreadable amount; #2043 (closing #2040) changed date detection and investment rows only. Searches: "csv amount": issues #1450, PRs #1451, words 31 and 41; "parseCsvAmount": issues #1450, #1458, PRs #1451, #1459, the same by words; "minus sign": issues #1499, PRs #802, words 3 and 5. Bodies: `parseCsvAmount` 2 (#1459, #1451), "trailing minus", "U+2212" and "Unicode minus" none, "minus sign" 2 (#1499, #802), a CSV amount beside zero none. None reports this. Nearest: #1450 (fixed by #1451) and #1459, the decimal comma. #1883 doesn't touch the CSV import.
- **Group 6 (draft 6).** Changed. #2042 (its commit `3321294`) rewrote the cited line: quick-fill now rounds with `roundToEntryPlaces` (`TransactionForm.tsx:842`, was 798's rounding to two places), so a coin's amount keeps its registered places, the case its comment names, and every ISO currency's still rounds at two (`format.ts:189-193`; the registry holds no ISO code, `currency-decimals.ts:12-15`), so the claim's case, a three-decimal currency, is as read. Edit and Duplicate load the stored amount at four places for fiat (`TransactionForm.tsx:471-476`, was 443-444), the ground of the judge's final verdict, so the bug holds on `main`, and it is drafted on `main`'s code. The amount field takes the same two places (`NormalTransactionFields.tsx:263`). `CurrencyInput.tsx` and `create-transaction.dto.ts` changed with #2042, and the form with #2015, #2023 and #2065, elsewhere. Searches: "quick fill": issues #2009, PRs #1883, #2018, #1263, #2023, #2015, #1303, #465, words 4 and 10; "handleQuickFill": issues none, PRs #1263, #465, words none and the same two; "quick-fill amount": issues none, PRs none, words 2 and 7. Bodies: `handleQuickFill` 2 (#1263, #465), quick-fill 4 (#2018, #1303, #1263, #465), `roundToEntryPlaces` and `entryDecimalPlaces` none, a three-decimal currency beside its places 1 (#300). None reports this. Nearest: #1263 (merged), which kept the form's account, currency and date on quick-fill. #1883 doesn't touch quick-fill.

---

## Draft 1 (group 1)

**Title:** [Bug] Undo and import recompute the balance by the database's day, so it counts or drops a day's transactions for a few hours

**Version:** `main` at `f3799f0`. Read at `93f4e68`; the code below is the same at the two, at new line numbers on `main`, where the two recomputes now round per currency, and the line numbers are `main`'s.

**Summary:** `ActionHistoryService.recalculateBalance` (`backend/src/action-history/action-history.service.ts:2197-2247`), the recompute an undo or redo of a transaction, transfer or split ends with (for a deleted transaction, `:1231`), sums the account's transactions up to `CURRENT_DATE` (`:2226`), the database server's day, though its comment says it uses "the same recalculation logic as AccountsService" (`:2216`). The import's recompute does the same (`backend/src/import/import-post-processing.service.ts:86`). `AccountsService.recalculateCurrentBalance` bounds the same sum by `todayYMD()`, the user's day in their time zone (`backend/src/accounts/accounts.service.ts:1984`, `:1988`; `backend/src/common/date-utils.ts:124-135`), and every create, edit and delete decides "future-dated" by that day (`date-utils.ts:164-166`). Nothing sets a time zone on the database session, so for the hours the two days differ, an undo or an import writes a balance that counts a day's transactions the rest of the app leaves out, or leaves out ones it counts.

**Result:** a user west of the database's time zone who undoes a change in the evening, or imports then, gets a balance that already counts tomorrow's transactions; a user east of it in the morning gets one that leaves out today's. The wrong figure stays until the hourly balance job recomputes the account, which it does only for an account with a transaction dated in the last seven days (`accounts.service.ts:2823-2832`, `:323`), and each edit in between moves the balance from it.

**Where:** `backend/src/action-history/action-history.service.ts:2197-2247` (`:2216`, `:2226`), `:1231`; `backend/src/import/import-post-processing.service.ts:74-89` (`:86`); `backend/src/accounts/accounts.service.ts:1972-2020` (`:1984`, `:1988`), `:2823-2832`; `backend/src/common/date-utils.ts:124-135`, `:164-166`.

**Steps:**
1. Run the database in UTC, as `docker-compose.prod.yml` leaves its `postgres` service (it sets no time zone), and use the app as a user in Toronto at 21:00 Toronto time (02:00 UTC the next day).
2. In a chequing account, enter a transaction dated tomorrow for -100.00. The balance doesn't change, rightly: the transaction is future-dated.
3. Delete any other transaction in the account, then undo the delete (Undo in the history panel, or Ctrl+Z).

**Expected:** the balance is back to what it was before the delete.

**Actual:** the balance is 100.00 lower: the undo's recompute counted tomorrow's -100.00, since the database's day is already tomorrow. An edit afterwards moves the balance from this wrong total.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** #447 bound two balance queries by `todayYMD()` instead of `CURRENT_DATE` for this reason, so that a transaction entered late in the evening wasn't counted twice; these two recomputes kept `CURRENT_DATE`. The monthly net-worth history (`backend/src/net-worth/net-worth.service.ts:2854`, `:2942`) and two portfolio queries (`backend/src/securities/portfolio-calculation.service.ts:680`, `:2592`) are cut at `CURRENT_DATE` too, so their current month can disagree with the balance over the same hours.

**Possible fix:** bound both recomputes by the user's day, passed as a parameter as `recalculateCurrentBalance` passes `todayYMD()`, or call `recalculateCurrentBalance` itself, as the undo's comment says it does. A test: with the clock at 02:00 UTC and the request time zone America/Toronto, a transaction dated the user's tomorrow is left out of the balance after an undo and after an import.

*Outside the issue:* Arm: A+B. Claims VM (arm B run 2, finding 8), ML (arm A run 1, finding 3) and XT (arm B run 1, finding 8), all final wrong-result. Both arms have claims here, so the clearer steps were taken: ML's (arm A run 1), the undo, each step a user action in the app, with its numbers; VM's and XT's import case is in *Summary* and *Result*. That `docker-compose.prod.yml` sets no time zone for the database, and the app none on its connection (`backend/src/app.module.ts`), is the architect's reading at the re-check, in no claim; so is *Related*'s #447.

---

## Draft 2 (group 2)

**Title:** [Bug] Restoring a voided transfer as Reconciled marks the other account's leg Reconciled too, with no reconciled date

**Version:** `main` at `f3799f0`. Read at `93f4e68`; the code below is the same at the two, at new line numbers on `main`, and `void-status-transition.util.ts` is unchanged; the line numbers are `main`'s.

**Summary:** When a transfer leaves VOID, the status the user picked is written onto both legs, not only the leg they changed. The edit form saves a transfer through `TransactionTransferService.updateTransfer` (`frontend/src/components/transactions/TransactionForm.tsx:1520`), which keeps a status change on the opened leg unless it crosses VOID, and on a VOID crossing writes it onto the counterpart too (`backend/src/transactions/transaction-transfer.service.ts:2196-2268`, the crossing's branch at `:2256-2260`). The status route does the same through `applyVoidTransitionToMirrorLeg`, which writes `{ status: newStatus }` onto the counterpart (`backend/src/transactions/void-status-transition.util.ts:136`, called at `transaction-reconciliation.service.ts:213-219` and from the generic update at `transactions.service.ts:3330`). Neither gives the counterpart a reconciled date. INV-TRANSFER-001 says reconciliation states are kept per account and not mirrored, only VOID inclusion being shared (`docs/system-invariants.md:955-958`), and the comment at `transaction-transfer.service.ts:2248-2252` leaves "the un-void sub-status question" open.

**Result:** the other account's leg is Reconciled though nobody reconciled it there, and it has no reconciled date. It drops off that account's reconcile screen, which lists only Unreconciled and Cleared rows (`transaction-reconciliation.service.ts:495`), and its amount is counted in the reconciled balance that account's next reconciliation starts from (`:508`). With "Lock reconciled transactions" on, it can't be changed.

**Where:** `backend/src/transactions/transaction-transfer.service.ts:2196-2268`, `:2248-2252`; `backend/src/transactions/void-status-transition.util.ts:116-146` (`:136`); `backend/src/transactions/transaction-reconciliation.service.ts:213-219`, `:237-257`; `backend/src/transactions/transactions.service.ts:3322-3339`; `docs/system-invariants.md:955-958`.

**Steps:**
1. Create a transfer of 100.00 from Chequing to Savings.
2. Open it, set Status to Void and save. Both legs are void.
3. Open it again from Chequing, set Status to Reconciled and save.
4. Open the Savings register and the Savings reconcile screen.

**Expected:** the Chequing leg Reconciled and the Savings leg back to its own status, Unreconciled; or the change refused, as the reconcile route refuses a void transaction ("Cannot reconcile a void transaction", `transaction-reconciliation.service.ts:316-323`).

**Actual:** the Savings leg is Reconciled, with no reconciled date, though Savings was never reconciled. It isn't listed on the Savings reconcile screen, and its 100.00 is in the reconciled balance there. The status route, `PATCH /api/v1/transactions/<chequing leg id>/status` with `{"status":"RECONCILED"}`, leaves the Savings leg the same way (the probe below).

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `applyStatusTransition` and `applyVoidTransitionToMirrorLeg` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_void_mirror_leg.js`, plain Node, standard library only; its second scenario, the status route):
```
Scenario 2: both legs VOID; PATCH /transactions/legA/status {status: RECONCILED}
  before
    legA (Chequing): status=VOID reconciledDate=null
    legB (Savings):  status=VOID reconciledDate=null
    balances: Chequing=1000.00 Savings=1000.00
    status route result: balanceMoved=true counterpartAccounts=["sav"]
  after
    legA (Chequing): status=RECONCILED reconciledDate=2026-11-04
    legB (Savings):  status=RECONCILED reconciledDate=null
    balances: Chequing=900.00 Savings=1100.00
```

**Related:** #1147 made VOID transitions pair-wide while keeping Cleared, Reconciled and the reconciled date on the leg being changed; leaving VOID still carries them across. Restoring a void transfer as Cleared marks the other leg Cleared the same way.

**Possible fix:** on a VOID crossing, pair only VOID itself: entering it, write VOID on both legs; leaving it, write the chosen status on the leg the user changed and Unreconciled, or its status from before the void, on the counterpart, with no reconciled date copied. That means `updateTransfer`, `applyVoidTransitionToMirrorLeg` and the bulk status update, which the comment says pairs the same way. A test: a voided transfer restored as Reconciled from Chequing leaves the Savings leg Unreconciled with no reconciled date, through the edit form's route, the status route and the bulk update.

*Outside the issue:* Arm: A. Claim HG (arm A run 2, finding 2; final wrong-result), the group's only claim, and its probe output (arm A run 2's `probe_void_mirror_leg.js`, scenario 2, which copies the status route; its copied lines are the same on `main`). The claim's steps send the status route by API; the numbered steps here are the architect's, through the edit form, whose route, `updateTransfer`'s VOID-crossing pairing (the same lines at `93f4e68`, 1998-2070), the re-check read on `main` as the app's own door to the same state. That route, the comment at `:2248-2252` and #1147 are the architect's reading at the re-check, not part of the claim. The comment calls the case an open "platform-wide decision", so the maintainer may answer that it is known; Garrett may hold this draft for that.

---

## Draft 3 (group 3)

**Title:** [Bug] Voiding one leg of a transfer through the API voids its reconciled counterpart in the other account, with "Lock reconciled transactions" on

**Version:** `main` at `f3799f0`. Read at `93f4e68`; the code below is the same at the two, at new line numbers on `main`, and `void-status-transition.util.ts` and `reconciled-lock.util.ts` are unchanged; the line numbers are `main`'s.

**Summary:** The strict reconciled lock is asked of the row a status change names, not of the counterpart the same write changes. `applyStatusTransition` checks `[locked]` only (`backend/src/transactions/transaction-reconciliation.service.ts:135-140`); then `applyVoidTransitionToMirrorLeg` locks the counterpart, sets its status and moves its account's balance with no lock check, leaving its reconciled date in place (`backend/src/transactions/void-status-transition.util.ts:125-145`, called at `transaction-reconciliation.service.ts:213-219`). The generic update does the same (`backend/src/transactions/transactions.service.ts:2959`, then `:3330`). The app's own doors ask both legs: the edit form's `updateTransfer` (`backend/src/transactions/transaction-transfer.service.ts:2162-2164`), the transfer delete (`:1784-1792`) and the bulk edit, which adds the counterparts before its check (`backend/src/transactions/transaction-bulk-update.service.ts:255-262`, `:340-345`).

**Result:** with the lock on, a void sent for the unreconciled leg of a transfer sets the other account's Reconciled leg to Void, its reconciled date kept, and moves that account's balance by the leg's amount. The account no longer matches the statement it was reconciled to, changed by a request that never named that row. INV-RECONCILE-001 says no request may change a Reconciled transaction's status while the lock is on (`docs/system-invariants.md:1226-1233`).

**Where:** `backend/src/transactions/transaction-reconciliation.service.ts:135-140`, `:213-219`; `backend/src/transactions/void-status-transition.util.ts:125-145`; `backend/src/transactions/transactions.service.ts:2959`, `:3330`.

**Steps:**
1. In Settings, turn on "Lock reconciled transactions".
2. Create a transfer of 100.00 from Chequing to Savings, dated last month.
3. In the Savings register, set that leg's status to Reconciled, and wait out the ten-second undo window.
4. Void the Chequing leg through the API, with a personal access token or a script: `PATCH /api/v1/transactions/<chequing leg id>/status` with `{"status":"VOID"}`, or `PATCH /api/v1/transactions/<id>` with the same body. The web app doesn't send this request: its edit form and bulk edit ask the lock of both legs and refuse, and the register's status cell doesn't offer Void (`frontend/src/lib/transaction-status-cycle.ts:12-16`). Only a hand-made API call reaches this.
5. Open Savings.

**Expected:** 409 "This transaction is reconciled and locked", as the edit form and `DELETE /api/v1/transactions/<id>/transfer` answer for the same pair; nothing written.

**Actual:** 200. The Savings leg is Void with its reconciled date still set, and Savings' balance is 100.00 below the statement it was reconciled to.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `applyStatusTransition`, `applyVoidTransitionToMirrorLeg` and `assertReconciledRowsMutable` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_void_mirror_leg.js`, plain Node, standard library only; its first scenario):
```
Scenario 1: strict lock ON, Savings leg RECONCILED; PATCH /transactions/legA/status {status: VOID}
  before
    legA (Chequing): status=CLEARED reconciledDate=null
    legB (Savings):  status=RECONCILED reconciledDate=2026-10-31
    balances: Chequing=900.00 Savings=1100.00
    DELETE /transactions/legA/transfer (both legs checked): 409 reconciledLockedError: This transaction is reconciled and locked.
    status route result: balanceMoved=true counterpartAccounts=["sav"] (no refusal)
  after
    legA (Chequing): status=VOID reconciledDate=null
    legB (Savings):  status=VOID reconciledDate=2026-10-31
    balances: Chequing=1000.00 Savings=1000.00
```

**Related:** #2039, fixed by #2041, made the split paths lock and ask the transfer legs a split parent holds in other accounts before deleting or relinking them; the status route's mirror write is the one left. #1815, fixed by #1816, made each branch of the transfer edit and delete ask the lock.

**Possible fix:** in `applyVoidTransitionToMirrorLeg`, pass the locked counterpart through `assertReconciledRowsMutable` before writing, and refuse. A test: with the lock on and the Savings leg Reconciled, a VOID sent for the Chequing leg through the status route, and through the generic update, answers 409 and leaves both legs and both balances unchanged.

*Outside the issue:* Arm: A. Claim MV (arm A run 2, finding 1; final wrong-result), the group's only claim; its steps, and its probe output (`probe_void_mirror_leg.js`, scenario 1; its copied lines are the same on `main`). **Rests on a crafted input:** step 4's door is a hand-made API call alone. The re-check read the app's doors on `main`, the register's status cycle, the edit form's `updateTransfer`, the bulk edit, and the assistant's and the MCP tools' edit actions, which carry no status, and none sends this request; step 4's sentence on the web app is the architect's. The claim's split side, the legs a split parent holds in other accounts deleted after a lock check on the parent only, was fixed after the read by #2041 (`8731bb8`), so it is the first sentence of *Related* and not in *Result*.

---

## Draft 4 (group 4)

**Title:** [Bug] On the evening of a month's last day, a budget's current period is next month, picked by the UTC month

**Version:** `main` at `f3799f0`. Read at `93f4e68`; every file below is the same at the two, so the line numbers are those read.

**Summary:** `getCurrentMonthPeriodDates` picks the month from `new Date()` with `getUTCFullYear` and `getUTCMonth` (`backend/src/budgets/budget-date.utils.ts:15-18`), and `getPreviousMonthPeriodDates` the month before it the same way (`:42-50`). `BudgetsService.getCurrentPeriodDates` returns it (`backend/src/budgets/budgets.service.ts:1000-1002`) for a budget's summary (`:428`) and velocity (`:542`), the dashboard's budget summary (`:872`) and the category budget status (`:973`), and the budget reports fall back to it (`backend/src/budgets/budget-reports.service.ts:358-372`); the client sends no period for these. Everything else dates the user's today with `todayYMD()`, in the user's time zone (`backend/src/common/date-utils.ts:124-135`).

**Result:** for the hours each month when the UTC month and the user's month differ, a budget's current period is the wrong month. West of UTC, on the evening of the last day, it is next month, with no spending yet, and the "previous month" report is the month still in progress; east of UTC, on the morning of the 1st, it is the month just ended.

**Where:** `backend/src/budgets/budget-date.utils.ts:15-18`, `:42-50`; `backend/src/budgets/budgets.service.ts:1000-1002`, `:428`, `:542`, `:872`, `:973`; `backend/src/budgets/budget-reports.service.ts:358-372`.

**Steps:**
1. As a user in Los Angeles, at 18:00 on 31 October (01:00 on 1 November in UTC), open a monthly budget.
2. Look at the period it shows as current, and its spending.

**Expected:** October, with October's spending.

**Actual:** November, with no spending; the "previous month" report shows October, which hasn't ended.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Possible fix:** take the month from the user's day, `todayYMD()`, as the rest of the app does, in `getCurrentMonthPeriodDates` and `getPreviousMonthPeriodDates`. A test: with the clock at 01:00 UTC on 1 November and the request time zone America/Los_Angeles, the current period is October and the previous one September.

*Outside the issue:* Arm: B. Claim ZX (arm B run 2, finding 9; final wrong-result), the group's only claim; its steps, in two. The callers beyond the claim's, the velocity (from the judge's run 1 notes), the dashboard's summary and the category budget status (the architect's reading of `budgets.service.ts` at the re-check), and the east-of-UTC case are added in *Summary* and *Result*.

---

## Draft 5 (group 5)

**Title:** [Bug] CSV import stores zero, or the wrong sign, for an amount it can't read, and reports nothing

**Version:** `main` at `f3799f0`. Read at `93f4e68`; `parseCsvAmount` and `normalizeAmountSeparators` are the same at the two, the row loop's amount read has moved into `readRowAmount` unchanged, and the line numbers are `main`'s.

**Summary:** `parseCsvAmount` handles parentheses, strips only `$ £ € ¥ ₹` and whitespace, normalizes the separators and calls `parseFloat` (`backend/src/import/csv-parser.ts:923-942`). A Unicode minus sign, a currency code or a "DR" prefix makes the value unreadable, and `readRowAmount` turns that into 0 (`:1230`, `:1239`, `:1243`), so the row is imported at 0.00; `parseFloat` stops at a trailing minus, so "12.34-" is imported as +12.34. Since #2030 the loop reports a row whose date it can't read (`:1419-1428`); a row whose amount it can't read is still imported, with no report.

**Result:** the bank's amount is replaced by 0.00, or an expense becomes income of the same size, and the account's balance after the import is off by those amounts. Nothing in the preview or the result flags the rows.

**Where:** `backend/src/import/csv-parser.ts:923-942`, `:1225-1252` (`:1230`, `:1239`, `:1243`), `:1412`, `:1419-1428`; `backend/src/import/amount-separators.util.ts:21-44`.

**Steps:**
1. Import a CSV whose amount column holds values such as "12.34-" (a trailing minus), "−12.34" (the Unicode minus sign, U+2212) or "CHF 12.34".
2. Map the amount column and import.
3. Look at the imported rows and the account's balance.

**Expected:** an amount that doesn't parse is reported for its row, as an unreadable date now is, or the row is refused; a trailing minus reads as a negative number.

**Actual:** "−12.34", "CHF 12.34" and "DR 12.34" are imported as 0.00, and "12.34-" as +12.34; no row is flagged.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `parseCsvAmount` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`csv_amount_probe.js`, plain Node, standard library only; it copies `parseCsvAmount` and `normalizeAmountSeparators`, and the caller's fallback to 0):
```
=== csv_amount_probe.js
"−12.34"       parseCsvAmount -> null    row imported with amount 0
"12.34-"       parseCsvAmount -> 12.34   row imported with amount 12.34
"12.34 CR"     parseCsvAmount -> 12.34   row imported with amount 12.34
"DR 12.34"     parseCsvAmount -> null    row imported with amount 0
"CHF 12.34"    parseCsvAmount -> null    row imported with amount 0
"12.34 kr"     parseCsvAmount -> 12.34   row imported with amount 12.34
"-12.34"       parseCsvAmount -> -12.34  row imported with amount -12.34
"(12.34)"      parseCsvAmount -> -12.34  row imported with amount -12.34
```

**Related:** #1450, fixed by #1451, and #1459 taught `parseCsvAmount` the decimal comma; the user guide's *Amount Parsing* note lists the forms it reads (`website/docs/importing-transactions.md:152`).

**Possible fix:** return an amount that doesn't parse among the result's skipped rows, with its row number and raw text, as the unreadable dates are, instead of falling back to 0; read a trailing minus, the Unicode minus and a leading or trailing currency code. A test: a CSV with "12.34-", "−12.34" and "CHF 12.34" rows gives -12.34, -12.34 and 12.34, or one skipped row each with its reason, never 0.00.

*Outside the issue:* Arm: B. Claim CT (arm B run 2, finding 3; final wrong-result, the judge's run 3, where the claim said data-loss), the group's only claim; its steps, and its probe output as arm B run 2's report gives it (the judge's three runs reproduced it with programs of their own; the copied lines are the same on `main`). The comparison with the unreadable-date report, from #2030's fix, and *Related* are the architect's reading at the re-check. Step 1's values are forms bank and spreadsheet exports can write, so this rests on a user's import, not a crafted input (the architect's reading); the user guide doesn't list them, so the maintainer may call them unsupported, and the ask is then the per-row report.

---

## Draft 6 (group 6)

**Title:** [Bug] Quick-fill saves a three-decimal amount rounded to two places, where Duplicate keeps it

**Version:** `main` at `f3799f0`. Read at `93f4e68`, where quick-fill rounded with `Math.round(Number(source.amount) * 100) / 100`; #2042 changed that line to the form currency's entry places, which keeps a coin's places and leaves an ISO currency's amount at two, as before. The line numbers are `main`'s.

**Summary:** `handleQuickFill` rounds the chosen row's amount to the form currency's entry places (`frontend/src/components/transactions/TransactionForm.tsx:842`, `roundToEntryPlaces`), which are two for every ISO currency, three-decimal ones included (`entryDecimalPlaces`, `frontend/src/lib/format.ts:189-193`; the currency registry holds places only for codes `Intl` doesn't know, `frontend/src/lib/currency-decimals.ts:12-15`). Opening a row to edit or to Duplicate loads the amount as stored, at its money precision, four places for fiat (`TransactionForm.tsx:471-476`). So the two ways of starting a transaction from an existing one save different amounts.

**Result:** a transaction quick-filled from a 12.345 row in a three-decimal currency (KWD, BHD, OMR) is saved as 12.35, where Duplicate saves 12.345; a four-place amount from a currency conversion, such as 12.3456, is saved as 12.35 the same way.

**Where:** `frontend/src/components/transactions/TransactionForm.tsx:839-863` (`:842`), `:471-476`; `frontend/src/lib/format.ts:189-193`, `:214-219`.

**Steps:**
1. In a KWD account, import a CSV statement with a row of -12.345; the import keeps the third decimal.
2. Open New Transaction, pick that row under Recent (the history button by the Payee field), and save.
3. Duplicate the imported row and save it.
4. Compare the two new transactions.

**Expected:** both -12.345, the amount of the row they copy.

**Actual:** the quick-filled one is saved as -12.35, the duplicated one as -12.345.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Possible fix:** load the chosen row's amount as Edit and Duplicate do, at the form currency's money precision (`moneyDecimalsForCurrency(accountCurrency)`, four places for fiat), rather than at its entry places. A test: quick-fill from a KWD -12.345 row, and from a CAD -12.3456 row, gives the amount Duplicate gives.

*Outside the issue:* Arm: B. Claim MG (arm B run 2, finding 11; final wrong-result, the judge's run 3, after run 1 said cosmetic and run 2 wrong-result), the group's only claim. **Changed since the read, not only moved:** #2042 (its commit `3321294`, merged 2026-11-06) replaced the claim's line with `roundToEntryPlaces`, its comment "a coin's own ..., otherwise two as before": a coin's amount is fixed, and an ISO currency's, three-decimal ones included, still rounds at two, so the claim's case is as read, and so is judge run 3's ground, that Duplicate keeps four places (`:471-476`). Drafted on `main`'s code: *Summary*, *Result* and the steps are the architect's (the claim's steps started from a row that already held 12.345; the import keeping the third decimal is the architect's reading of `backend/src/import/import-context.ts`, which refuses a file amount with more places than four and never rounds one), and judge run 2's probe, which copied the old line, isn't quoted. #2042 states its fiat rule in `entryDecimalPlaces`' comment ("every fiat surface keeps the cents it has always used"), and the amount field takes the same two places (`frontend/src/components/transactions/NormalTransactionFields.tsx:263`), so the maintainer may answer that it is by design; and FILING §3 drops what changed since the read. Garrett may hold this draft for either.

---

## Not in this batch

- **Batches 3 and 4,** the seven confirmed crash and wrong-result groups left, in the order of the table above; each waits for its own drafts and Garrett's go.
- **Not filed (FILING §4):** group 11 (PN, GM, LP), stuck, and group 16 (VL), process, stay in the ledger. Group 22 (CG) was refuted by the judge's final verdict, so it isn't filed.
