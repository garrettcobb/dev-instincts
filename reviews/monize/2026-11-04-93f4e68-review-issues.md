# monize: issue drafts, round 2026-11-04-93f4e68-review

Second file-mode run on kenlasko/monize (control run, arm A run 2). Reviewed `main` at `93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9`; today's `main` is `fbf01ab`, and none of the cited files changed between the two except `database/schema.sql`, which adds one more table that cascades on category delete (named in draft 3). Nothing here is filed: `gh` stayed read-only, and each draft waits for Garrett's written go (FILING.md section 8). The repo has no issue template, so the section 5 form is used as is. Four drafts; two findings held back under *Not filing*.

Before drafting, open and closed issues and pull requests were searched (`gh search issues` / `gh search prs`, 2026-11-04) for each finding: no match. Issue #1815 (closed 2026-10-22) fixed the strict reconciled lock being skipped on split-transfer and cross-owner edits of the *requested* row (its A26-M11); draft 1 is the next door along and cites it under Related.

---

## Draft 1

**Title:** [Bug] Voiding one leg of a transfer voids its reconciled counterpart in the other account, with "Lock reconciled transactions" on

**Version:** `main` at `93f4e68` (unchanged on today's `main`, `fbf01ab`).

**Summary:** The strict reconciled lock is asked of the row the request names and never of the rows the same write reaches. `applyStatusTransition` checks `[locked]` only (`backend/src/transactions/transaction-reconciliation.service.ts:130-135`), then `applyVoidTransitionToMirrorLeg` (`backend/src/transactions/void-status-transition.util.ts:125-144`) locks the counterpart leg, writes `status` on it and moves its account balance with no lock check. The generic row update does the same (`backend/src/transactions/transactions.service.ts:2813`, then `:3111`). The paired routes get it right: `removeTransfer` passes both legs to the check (`backend/src/transactions/transaction-transfer.service.ts:1606-1616`) and the bulk route expands to mirror legs before checking (`transaction-bulk-update.service.ts:1418-1470`, `:725`).

**Result:** with the lock on, voiding the unreconciled leg of a transfer sets the other account's RECONCILED leg to VOID (its `reconciled_date` stays), and that account's balance moves by the leg's amount. The account the user reconciled against a statement no longer matches it, and the row that should have been immovable was changed by a request that never named it.

**Where:** `backend/src/transactions/transaction-reconciliation.service.ts:130-135`, `:208-214`; `backend/src/transactions/void-status-transition.util.ts:125-144`; `backend/src/transactions/transactions.service.ts:2813`, `:3111`.

**Steps:**
1. Settings: turn on "Lock reconciled transactions".
2. Create a transfer of 100.00 from Chequing to Savings, dated last month.
3. In Savings, reconcile that leg (status cell to Reconciled; wait past the ten-second undo window).
4. Void the Chequing leg through the status route: `PATCH /transactions/<chequing leg id>/status` with `{"status":"VOID"}` (the register's status cell does not offer VOID, so the API, the MCP tools or the assistant are the doors; `PATCH /transactions/<id>` with `{"status":"VOID"}` is the same path).
5. Open Savings.

**Expected:** 409 "This transaction is reconciled and locked", as `DELETE /transactions/<id>/transfer` answers for the same pair; nothing written.

**Actual:** 200. The Savings leg is now VOID with its reconciled date still set, and Savings' balance is 100.00 lower than the statement it was reconciled to.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `applyStatusTransition`, `applyVoidTransitionToMirrorLeg` and `assertReconciledRowsMutable` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_void_mirror_leg.js`, scenario 1):
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

**Related:** the same cause on the split side: replacing or removing a split parent's lines checks the lock on the parent only (`transactions.service.ts:2813` then `:2895`; `transaction-split.service.ts:973`, `:1136`, `:1327`) and `deleteSplitSideEffects` / `removeLinkedLeg` then delete the transfer counterpart legs in other accounts (`transaction-split.service.ts:884-888`, `:1295`) whatever their status, so a reconciled counterpart leg is deleted outright. #1815 (A26-M11) closed the neighbouring gap where the *requested* row's lock was skipped.

**Possible fix:** in `applyVoidTransitionToMirrorLeg`, pass the locked counterpart through `assertReconciledRowsMutable` before writing (and refuse, not skip); in `deleteSplitSideEffects` do the same for the locked legs before `removeLockedTransactionLeg`. Test: lock on, counterpart RECONCILED, each of the three doors (status route, generic update, split rebuild) returns 409 and leaves both rows and both balances unchanged; `reconciled-lock.guard.spec.ts` could require every `removeLockedTransactionLeg` / mirror write to sit after an assertion over the same rows.

---

## Draft 2

**Title:** [Bug] Restoring a voided transfer leg to Reconciled marks the other account's leg Reconciled too, with no reconciled date

**Version:** `main` at `93f4e68` (unchanged on today's `main`, `fbf01ab`).

**Summary:** `updateStatus` resolves to whatever status the request carries (`backend/src/transactions/transaction-reconciliation.service.ts:240-242`), so VOID -> RECONCILED is accepted there although the dedicated `reconcile` route refuses it (`:311-318`). When the transition crosses the VOID boundary, `applyVoidTransitionToMirrorLeg` writes the *exact* new status onto the counterpart leg (`backend/src/transactions/void-status-transition.util.ts:136`), not merely the crossing. INV-TRANSFER-001 says reconciliation states are per ledger and only VOID inclusion is shared. The generic update has the same two steps (`transactions.service.ts:3016-3017`, `:3111`).

**Result:** the leg in the other account becomes RECONCILED without that account having been reconciled, with `reconciled_date` NULL; that account's next reconciliation starts from a "previously reconciled" figure that includes a row nobody reconciled, and with the strict lock on the row is frozen.

**Where:** `backend/src/transactions/transaction-reconciliation.service.ts:240-242`; `backend/src/transactions/void-status-transition.util.ts:136`; `backend/src/transactions/transactions.service.ts:3111`.

**Steps:**
1. Create a transfer of 100.00 from Chequing to Savings, then void it (both legs VOID).
2. `PATCH /transactions/<chequing leg id>/status` with `{"status":"RECONCILED"}` (also reachable as `PATCH /transactions/<id>` with `{"status":"RECONCILED"}`).
3. Open the Savings register and the Savings reconcile screen.

**Expected:** either a refusal, as `POST /transactions/<id>/reconcile` gives ("Cannot reconcile a void transaction"), or the Chequing leg reconciled and the Savings leg restored to its own unreconciled state.

**Actual:** both legs are RECONCILED; the Savings leg has no reconciled date and was never reconciled in Savings.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `applyStatusTransition` and `applyVoidTransitionToMirrorLeg` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`probe_void_mirror_leg.js`, scenario 2):
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

**Related:** VOID -> CLEARED through the same route marks the counterpart CLEARED, the same mirroring at lower cost.

**Possible fix:** have `updateStatus` refuse VOID -> RECONCILED as `reconcile` does; in `applyVoidTransitionToMirrorLeg`, write the counterpart as UNRECONCILED when leaving VOID (keep VOID when entering it). Test: both legs VOID, status route to RECONCILED on one leg: refusal, or own leg RECONCILED with a date and the counterpart UNRECONCILED.

---

## Draft 3

**Title:** [Bug] Deleting a category deletes the payroll deduction rules that use it and leaves budget lines with no category

**Version:** `main` at `93f4e68`; today's `main` (`fbf01ab`) adds `loan_fees`, also `ON DELETE CASCADE` on `category_id`.

**Summary:** `CategoriesService.remove` refuses a delete only for subcategories and for references counted by `getTransactionCount` (transactions, splits, scheduled transactions, scheduled splits: `backend/src/categories/categories.service.ts:582-616`, `:654-697`). Nothing counts budget lines or payroll deduction rules, and the schema decides for them: `payroll_deduction_rules.category_id` is `ON DELETE CASCADE` (`database/schema.sql:3640`; `backend/src/payroll-deductions/entities/payroll-deduction-rule.entity.ts:65`), `budget_categories.category_id` and `budget_period_categories.category_id` are `ON DELETE SET NULL` (`database/schema.sql:2424`, `:2472`).

**Result:** a category with no transactions but a payroll deduction rule and a budget line can be deleted with no warning; the rule is gone and the budget line survives with no category (how such a line renders was not checked). The action-history entry records only the category.

**Where:** `backend/src/categories/categories.service.ts:582-616`, `:654-697`; `database/schema.sql:2424`, `:2472`, `:3640`.

**Steps:**
1. Create a category "Union dues" with no transactions.
2. Add a payroll deduction rule for it, and a budget line for it in a budget.
3. Delete the category from the Categories page.

**Expected:** a refusal naming the rule and the budget line, as a referencing transaction gets ("Cannot delete category with N referencing transaction(s)"), or a prompt to reassign.

**Actual:** the category is deleted; the payroll deduction rule is gone with it, and the budget line keeps its amount with no category.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** `reassignTransactions` (`categories.service.ts:700-775`), the step the refusal points the user to, moves transactions, splits and scheduled items only, so neither the rule nor the budget line can be moved before the delete.

**Possible fix:** count payroll deduction rules, budget lines (and `loan_fees` on main) in the delete guard and refuse with their names, or reassign them in `reassignTransactions`. Test: a category referenced only by a payroll rule, then only by a budget line, is refused; after a reassign both point at the target.

---

## Draft 4

**Title:** [Bug] Reassigning a category fails with a database error once the user has more than 65,535 transactions

**Version:** `main` at `93f4e68` (unchanged on today's `main`, `fbf01ab`).

**Summary:** `reassignTransactions` selects every transaction id the user owns and passes the whole list as `IN (:...transactionIds)` to the split update (`backend/src/categories/categories.service.ts:723-739`), and does the same for scheduled transaction ids (`:751-766`). TypeORM expands a spread array into one bind parameter per element, and the PostgreSQL wire protocol carries the parameter count as a 16-bit integer, so a list over 65,535 ids cannot be bound: the driver reports a bind error and the request fails. The list is the user's entire ledger, not the rows that reference the category.

**Result:** a user with a large history (the README's own case is thirty years of Microsoft Money data) cannot reassign a category, and since the delete guard points to reassign first, cannot delete one either. Below the limit the query still ships every id on each call.

**Where:** `backend/src/categories/categories.service.ts:723-739`, `:751-766`; the same shape with the (smaller) scheduled list in `getTransactionCount`, `:677-690`.

**Steps:**
1. A user with more than 65,535 transactions (an import of a long Money or Quicken history).
2. Categories page: reassign any category's transactions to another category (`POST /categories/<id>/reassign`).

**Expected:** the rows move; a count is returned.

**Actual:** 500; nothing moves (the update runs inside one transaction, so the transaction update is rolled back with it).

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app and no probe was possible without a database, so the steps above are what the code says will happen.

**Possible fix:** update `transaction_splits` with a subquery or join (`WHERE category_id = $1 AND transaction_id IN (SELECT id FROM transactions WHERE user_id = $2)`), and the scheduled splits likewise; same in `getTransactionCount`. Test: a user with 70,000 transactions, one of which references the category, reassigns it.

---

## Not filing

- **Finding 5, "Twice a Month" steps to the 15th and month-end whatever the start date** (`backend/src/common/recurrence.ts:139-148`; `frontend/src/lib/frequency.ts:64-73`; label `frontend/src/i18n/messages/en/scheduledTransactions.json:323`). A schedule started on the 1st is next due on the 31st, then the 15th: a bill on the 1st and 16th gets the wrong due dates and the wrong auto-post days (probe `probe_semimonthly_step.js`: `2026-01-01 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28`). Held back because the two implementations agree, their tests assert it (`OccurrenceDatePicker.test.tsx:296`) and the loan label spells it out ("Semi-Monthly (15th & month end)"): a design the scheduled-transaction label hides rather than a defect the maintainer would call one. Garrett decides; if filed it is a wording or a feature request, not a `[Bug]`.
- **Nothing in auth, 2FA or OIDC** was read in this round (time box), so there is no security item for Garrett.
