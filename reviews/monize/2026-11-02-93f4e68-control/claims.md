# Claims

Each claim has a code. The order is random.

## VM: The balance written after an import, and by undo, is bounded by the database server's date, not the user's

Severity: wrong-result
Where: backend/src/import/import-post-processing.service.ts:81, backend/src/action-history/action-history.service.ts:2111, backend/src/net-worth/net-worth.service.ts:2849, backend/src/net-worth/net-worth.service.ts:2937, backend/src/accounts/accounts.service.ts:1747, at 93f4e68
What the user loses: A balance that matches the register for part of the day. Every other balance writer bounds the ledger at `todayYMD()`, today in the user's timezone; these sites use SQL `CURRENT_DATE`, the server's date. The monthly net-worth history is cut at the same server date (net-worth.service.ts:2849, 2937), so its current month and the live balance can disagree over today's rows.
Steps:
1. Run the server in UTC. As a user in Australia at 09:00 on the 5th (still the 4th in UTC), import a statement that includes the 5th's transactions.
2. Look at the account balance right after the import, then compare with the register's running balance.
Expected: The balance includes every row dated on or before the user's today, as `recalculateCurrentBalance` (accounts.service.ts:1747) computes it.
Actual: The post-import recomputation sums rows with `transaction_date <= CURRENT_DATE` (import-post-processing.service.ts:81), so the 5th's rows are excluded and the balance is lower than the register until the hourly fold rewrites it. For a user west of the server (US evening), rows the user dated tomorrow are included instead. Undo of a transaction action recomputes the same way (action-history.service.ts:2111) and the figure then disagrees with the one the deleted or restored row's own path wrote. Both are corrected by the hourly `applyDueTransactionBalances` only when the account has a row inside its 7-day window.
Evidence: reading

## HG: Restoring a voided transfer leg to Reconciled marks the other account's leg Reconciled too, with no reconciled date

Severity: wrong-result
Where: backend/src/transactions/transaction-reconciliation.service.ts:240, backend/src/transactions/void-status-transition.util.ts:136, backend/src/transactions/transactions.service.ts:3111, at 93f4e68
What the user loses: the other account shows a row as reconciled that nobody reconciled there, with no reconciled date; its next reconciliation starts from a "previously reconciled" figure that includes it, and with the lock on the row is frozen. The status route accepts VOID -> RECONCILED although the dedicated reconcile route refuses it, and the mirror write copies the exact new status rather than only the VOID crossing.
Steps:
1. Create a transfer of 100.00 from Chequing to Savings, then void it (both legs VOID).
2. PATCH /transactions/<chequing leg id>/status with {"status":"RECONCILED"} (or PATCH /transactions/<id> with the same body).
3. Open the Savings register and the Savings reconcile screen.
Expected: a refusal, as POST /transactions/<id>/reconcile gives ("Cannot reconcile a void transaction"), or the Chequing leg reconciled and the Savings leg back in its own unreconciled state.
Actual: both legs RECONCILED; the Savings leg has no reconciled date and was never reconciled in Savings.
Evidence: probe
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

## MV: Voiding one leg of a transfer voids its reconciled counterpart in the other account while "Lock reconciled transactions" is on

Severity: wrong-result
Where: backend/src/transactions/transaction-reconciliation.service.ts:130, backend/src/transactions/transaction-reconciliation.service.ts:208, backend/src/transactions/void-status-transition.util.ts:136, backend/src/transactions/transactions.service.ts:2813, backend/src/transactions/transactions.service.ts:3111, at 93f4e68
What the user loses: the account they reconciled against a bank statement no longer matches it: a row the lock promised was immovable is set to VOID (its reconciled date kept) and the account's balance moves by its amount, from a request that never named that row. On the split side the same gap deletes a reconciled counterpart leg outright (backend/src/transactions/transaction-split.service.ts:887, :1295, after a lock check on the parent only at :973, :1136, :1327).
Steps:
1. Settings: turn on "Lock reconciled transactions".
2. Create a transfer of 100.00 from Chequing to Savings, dated last month.
3. In Savings, reconcile that leg; wait past the ten-second undo window.
4. PATCH /transactions/<chequing leg id>/status with {"status":"VOID"} (or PATCH /transactions/<id> with the same body; the register's status cell does not offer VOID).
5. Open Savings.
Expected: 409 "This transaction is reconciled and locked", as DELETE /transactions/<id>/transfer answers for the same pair; nothing written.
Actual: 200; the Savings leg is VOID with its reconciled date still set, and Savings' balance is 100.00 below the statement it was reconciled to.
Evidence: probe
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

## ZX: The budget page's "current period" is picked by the UTC month, so late on the last day of the month it shows next month

Severity: wrong-result
Where: backend/src/budgets/budget-date.utils.ts:15, backend/src/budgets/budgets.service.ts:1000, backend/src/budgets/budget-reports.service.ts:371, at 93f4e68
What the user loses: The right month's budget. A user west of UTC opening Budgets on the evening of the 31st sees next month's period, with zero spending, and the "previous month" report points at the month that is still in progress.
Steps:
1. Set the user's timezone to America/Los_Angeles. At 18:00 local on 31 October (01:00 UTC on 1 November) open the Budgets page.
Expected: October is the current period.
Actual: `getCurrentMonthPeriodDates` uses `new Date()` with `getUTCFullYear` and `getUTCMonth`, and `getCurrentPeriodDates` (budgets.service.ts:1000) and the reports (budget-reports.service.ts:363-371) call it. Everything else dates the user's "today" with `todayYMD()`.
Evidence: reading

## CT: CSV import stores zero, or the wrong sign, for amounts it cannot read

Severity: data-loss
Where: backend/src/import/csv-parser.ts:804, backend/src/import/csv-parser.ts:1205, backend/src/import/csv-parser.ts:1213, backend/src/import/csv-parser.ts:1218, at 93f4e68
What the user loses: The amount the bank wrote. A row whose amount uses the Unicode minus sign, a currency code prefix such as "CHF", or a "DR" prefix is imported as 0.00. A row with a trailing minus ("12.34-") is imported as a positive amount, so an expense becomes income. The balance recomputed after the import is wrong by those amounts and nothing says so.
Steps:
1. Import a CSV whose amount column contains "−12.34" (U+2212, which several banks and spreadsheets export) or "12.34-" (trailing minus) or "CHF 12.34".
2. Map the amount column and import.
3. Look at the imported rows and the account balance.
Expected: An amount that does not parse is reported for that row, or the row is refused. A trailing minus is a negative number.
Actual: `parseCsvAmount` strips only `$ £ € ¥ ₹` and whitespace, then calls `parseFloat`; the callers at csv-parser.ts:1205, 1213 and 1218 replace a null result with `?? 0`, so the row is created with amount 0. `parseFloat("12.34-")` reads the digits and stops at the minus, so the sign is lost. No per-row warning is produced for either case.
Evidence: probe
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

## MG: Quick-fill copies an amount rounded to two decimals

Severity: wrong-result
Where: frontend/src/components/transactions/TransactionForm.tsx:798, at 93f4e68
What the user loses: Fractions of a cent, or the third decimal of a currency like KWD or BHD, when a recent transaction is used to pre-fill a new one. The rest of the form works at four decimals (`roundMoney`).
Steps:
1. In an account in a three-decimal currency, have a transaction of 12.345. Open the new-transaction form and quick-fill from that row.
Expected: 12.345.
Actual: `Math.round(Number(source.amount) * 100) / 100` gives 12.35 (TransactionForm.tsx:798).
Evidence: reading

## GN: Reassigning a category's transactions loads every transaction id the user owns and binds them into one IN (...) list; past the Postgres bind limit (65,535 parameters, about 65,000 transactions) the statement fails and the category can be neither reassigned nor deleted. The scheduled-split count and update do the same with schedule ids.

Severity: crash
Where: backend/src/categories/categories.service.ts:721-741 (getMany at 727, IN at 738); 674-690 and 749-766 (schedule ids), at 93f4e68
What the user loses: for a long Microsoft Money or Quicken history (the import this app is built for), "reassign transactions" for a category errors out, and because `remove` requires a zero count, the category can be neither emptied nor deleted. The message is a database error, not a domain one.
Steps:
1. Import a history of 70,000 transactions (any account mix).
2. Categories, pick any category, Reassign transactions to another category.
Expected: the rows move.
Actual: the request fails with a database error (bind parameter count), and the category cannot be deleted afterwards either.
Evidence: reading

## VF: Removing one split line through the API leaves the parent amount and the account balance unchanged

Severity: wrong-result
Where: backend/src/transactions/transaction-split.service.ts:1299, backend/src/transactions/transaction-split.service.ts:1368, backend/src/transactions/transaction-split.service.ts:1397, backend/src/transactions/transactions.controller.ts:1726, at 93f4e68
What the user loses: Agreement between the register and the reports. After a line is removed the parent still carries the full amount and the account balance still moves by it, while the category totals, and for a transfer line the other account, no longer show that money.
Steps:
1. Create a -100.00 split transaction on Chequing: -60.00 Groceries and -40.00 transfer to Savings. Savings shows +40.00.
2. Call `DELETE /api/transactions/{id}/splits/{splitId}` for the -40.00 line (the split editor in the UI resubmits the whole set instead, so this is the API and the Swagger documentation).
3. Look at Chequing and Savings.
Expected: The parent amount is refused from changing shape, or it becomes -60.00 and Chequing is credited 40.00, so that lines and parent agree as `validateSplitAmountSum` requires everywhere else.
Actual: `removeSplit` reverses and deletes the Savings leg (`removeLinkedLeg`), removes the split row (transaction-split.service.ts:1368), and when one line is left collapses the parent to a plain transaction with that line's category (transaction-split.service.ts:1397-1401). The parent's `amount` and Chequing's balance stay at -100.00. Savings is back to 0, so 40.00 has left Chequing and arrived nowhere. The sibling `addSplit` route likewise accepts a set whose lines sum to less than the parent (transaction-split.service.ts:1147 only refuses a sum that exceeds it).
Evidence: reading

## VP: Reassigning a category's transactions fails for a user with more than 65535 transactions

Severity: crash
Where: backend/src/categories/categories.service.ts:721, backend/src/categories/categories.service.ts:738, backend/src/categories/categories.service.ts:751, backend/src/categories/categories.service.ts:763, at 93f4e68
What the user loses: The ability to move a category's transactions to another category, which is also the step the delete-category error tells them to take.
Steps:
1. Have a ledger with more than 65535 transactions (a twenty-year Money or Quicken import).
2. On a category, choose to reassign its transactions to another category.
Expected: The reassign completes.
Actual: `reassignTransactions` loads every transaction id of the user (categories.service.ts:721-727) and passes the whole list as `IN (:...transactionIds)` (categories.service.ts:738). TypeORM expands each id to its own bind parameter, and the PostgreSQL wire protocol carries the bind-parameter count as a 16-bit integer, so a statement with more than 65535 parameters cannot be executed and the query fails. The whole transaction is rolled back and the request fails with a database error. The same list is built again for scheduled splits (categories.service.ts:751-767), bounded by the number of schedules. The split filter only needs `transaction.user_id`, which the `getTransactionCount` query a few lines above already uses as a join.
Evidence: reading

## ZD: Merging two payees drops the source payee's warranties, email receipt parsers and loan overpayment links instead of moving them

Severity: data-loss
Where: backend/src/payees/payees.service.ts:1953, database/schema.sql:3566, database/schema.sql:820, database/schema.sql:1203, database/schema.sql:4596, at 93f4e68
What the user loses: After a merge, a warranty recorded against the source payee has no payee; an email receipt parser bound to it stops matching that payee; a loan's overpayment payee and a shared-expense person's payee link are cleared.
Steps:
1. Create payees "Costco" and "Costco Wholesale"; record a warranty under "Costco Wholesale".
2. Merge "Costco Wholesale" into "Costco".
3. Open the warranty.
Expected: The warranty (and any parser, loan overpayment payee, shared person) now points at "Costco".
Actual: `mergePayees` re-points `transactions`, `scheduled_transactions` and `payee_aliases` only, then removes the source payee. `warranties.payee_id`, `email_receipt_parsers.payee_id`, `shared_people.payee_id` and the loan `overpayment_payee_id` are all `ON DELETE SET NULL`, so those links are nulled by the delete.
Evidence: reading

## ML: The absolute balance recomputes after an undo and after an import bound the ledger by Postgres CURRENT_DATE (the database's day, UTC in the shipped containers), while AccountsService.recalculateCurrentBalance and every delta path bound it by the user's timezone day; for the hours the two days differ the stored balance includes or omits a day's rows and flips back on the next edit.

Severity: wrong-result
Where: backend/src/action-history/action-history.service.ts:2111 (comment at 2106: same recalculation logic as AccountsService); backend/src/import/import-post-processing.service.ts:81; versus backend/src/accounts/accounts.service.ts:1739-1787 (todayYMD at 1751). Same bound in net-worth.service.ts:2849, 2937 and securities/portfolio-calculation.service.ts:681, 2586, at 93f4e68
What the user loses: a user in America/Toronto with a transaction dated tomorrow sees it excluded from the balance on entry (user's day), included after an undo or an import run between 19:00 and midnight (UTC day), and the figure stays until the next user-day recompute; a user east of UTC in the morning sees today's rows dropped instead.
Steps:
1. Backend with `TZ` unset (UTC); user timezone America/Toronto; at 21:00 Toronto time.
2. In a chequing account, enter a transaction dated tomorrow for -100.00. Balance unchanged (correct: future-dated).
3. Delete any other transaction in the account, then Undo it from History.
Expected: balance back to what it was before the delete.
Actual: balance is 100.00 lower: the undo's recompute counted tomorrow's row because `CURRENT_DATE` is already tomorrow in UTC. Editing any amount afterwards keeps the wrong total (the delta is applied to it).
Evidence: reading

## TG: Deleting a category detaches budget lines and deletes payroll deduction rules without warning

Severity: data-loss
Where: backend/src/categories/categories.service.ts:607, backend/src/categories/categories.service.ts:660, backend/src/categories/categories.service.ts:640, database/schema.sql:2424, database/schema.sql:2472, database/schema.sql:3640, at 93f4e68
What the user loses: The link between a budget line and its category, so the allocated amount stays in the budget total but no spending is ever counted against it; and any payroll deduction rule for the category, which is removed outright.
Steps:
1. Create a category "Gym" with no transactions yet. Add a 60.00 line for Gym to a budget. Optionally add a payroll deduction rule for Gym on a payroll schedule with no split line for it.
2. Delete the Gym category. The delete succeeds.
3. Open the budget and the payroll rules.
Expected: The delete is refused, as it is for a category with transactions, splits or scheduled lines, or the dialog names what will be removed.
Actual: `remove` refuses only when `getTransactionCount` (categories.service.ts:660-696) is non-zero, and that counts transactions, transaction splits, scheduled transactions and scheduled splits. It does not look at `budget_categories` or `budget_period_categories` (`category_id ... ON DELETE SET NULL`, schema.sql:2424 and 2472) or `payroll_deduction_rules` (`category_id ... ON DELETE CASCADE`, schema.sql:3640). After `m.remove(Category, category)` at categories.service.ts:640 the budget line has a null category: `computeActualIncome` (budgets.service.ts:1044) and the spending query (budget-spending.util.ts:240) filter out lines with a null category, so its allocation counts and its actuals are always zero. The payroll rule is gone.
Evidence: reading

## PN: Deleting a payee checks no referencers on any door (REST, AI batch action, MCP tool); transactions.payee_id and scheduled_transactions.payee_id have no ON DELETE action, so the database refuses and the user gets the generic 400 'Referenced record does not exist or cannot be removed' with no count and no pointer to Merge.

Severity: stuck
Where: backend/src/payees/payees.service.ts:1280-1308; database/schema.sql:385, 1084; backend/src/common/filters/http-error-body.ts:125; backend/src/ai/actions/ai-actions.service.ts:716-718; backend/src/mcp/tools/payees.tool.ts:604, 656, 750, at 93f4e68
What the user loses: **payee delete has no referencer check on any door.** stuck, reading. `payees.service.ts:1280-1308`; FKs without ON DELETE at `schema.sql:385`, `1084`; the filter maps 23503 to a generic 400 (`http-error-body.ts:125`). Same on the AI batch action and the MCP tool.
Steps:
Delete a payee that has one transaction (REST or the AI delete_payee action): 400 with the generic referenced-record message; the payee stays.
Evidence: reading

## MN: Deleting an account that has no transactions silently deletes every scheduled bill, deposit and transfer paid from it

Severity: data-loss
Where: backend/src/accounts/accounts.service.ts:1413, backend/src/accounts/accounts.service.ts:2207, database/schema.sql:1082, database/schema.sql:1120, database/schema.sql:1158, at 93f4e68
What the user loses: Every scheduled transaction whose source account is the deleted account is removed with its splits, overrides and posting history; scheduled transfers into the account lose their destination; a split line in another schedule that transfers to the account is dropped, so that schedule's lines no longer sum to its amount. None of this is mentioned before the delete.
Steps:
1. Create a new chequing account with no transactions.
2. Create a monthly scheduled bill (Bills & Deposits) paid from that account, and a scheduled transfer from Savings into it.
3. On the Accounts page use "Delete Account" (its tooltip reads "Permanently delete account (no transactions)") and confirm "Are you sure you want to permanently delete ... This action cannot be undone."
Expected: The delete is refused, or the dialog says the schedules will go too, the way the transaction-count refusal does.
Actual: `assertAccountEmpty` only counts `transactions` and `investment_transactions`. `scheduled_transactions.account_id` is `ON DELETE CASCADE`, `scheduled_transactions.transfer_account_id` is `ON DELETE SET NULL`, and `scheduled_transaction_splits.transfer_account_id` is `ON DELETE CASCADE`, so the schedules vanish, the transfer schedule points nowhere, and a sibling schedule loses a line. The action-history record stores only the account row, so undo does not bring the schedules back.
Evidence: reading

## GM: Deleting a payee that has transactions fails with a message that does not say why

Severity: stuck
Where: backend/src/payees/payees.service.ts:1280, database/schema.sql:385, backend/src/common/filters/http-error-body.ts:125, frontend/src/i18n/messages/en/payees.json:72, at 93f4e68
What the user loses: The dialog says "Delete 'X'? This action cannot be undone.", the user confirms, and gets "Referenced record does not exist or cannot be removed". There is no count, no reassign option and no hint that merge or deactivate is the way out, unlike the category delete dialog.
Steps:
1. Create a transaction with payee "Shell".
2. Delete "Shell" from the Payees page and confirm.
Expected: A refusal naming the transaction count and pointing at merge or deactivate, or a reassign choice.
Actual: `remove()` calls the repository delete with no usage check; `transactions.payee_id` and `scheduled_transactions.payee_id` have no ON DELETE clause, so PostgreSQL raises 23503 and the filter turns it into a generic 400.
Evidence: reading

## XX: Deleting a category deletes the payroll deduction rules that use it and leaves budget lines with no category

Severity: data-loss
Where: backend/src/categories/categories.service.ts:579, backend/src/categories/categories.service.ts:654, database/schema.sql:3640, database/schema.sql:2424, database/schema.sql:2472, backend/src/payroll-deductions/entities/payroll-deduction-rule.entity.ts:65, at 93f4e68
What the user loses: a payroll deduction rule they configured is deleted without warning (the foreign key cascades), and a budget line keeps its amount but loses its category (the foreign key sets it null). The delete guard counts only transactions, splits, scheduled transactions and scheduled splits, and the reassign step it points to moves only those. Today's main adds loan_fees, also cascading on category_id.
Steps:
1. Create a category with no transactions.
2. Add a payroll deduction rule for it, and a budget line for it in a budget.
3. Delete the category from the Categories page.
Expected: a refusal naming the rule and the budget line, as a referencing transaction gets, or a prompt to reassign them.
Actual: the category is deleted; the payroll deduction rule is gone with it; the budget line survives with no category.
Evidence: reading

## KR: Removing a split line through the split-delete endpoint deletes the surviving transfer leg in the other account and leaves the parent uncategorized at its full amount

Severity: data-loss
Where: backend/src/transactions/transaction-split.service.ts:1299, backend/src/transactions/transaction-split.service.ts:1375, backend/src/transactions/transactions.controller.ts:1726, at 93f4e68
What the user loses: The transfer leg that the remaining split created in the target account is deleted and its balance reversed, while the parent keeps its original amount with no category and no transfer. Money that was recorded as arriving in the other account disappears. The endpoint also leaves a parent whose amount no longer equals its lines when a non-last line is removed.
Steps:
1. Create a -100.00 split transaction: 60.00 to a category and 40.00 as a transfer to Savings.
2. Call DELETE /transactions/{id}/splits/{categorySplitId}. The route exists and the client library wraps it (frontend/src/lib/transactions.ts:457); the register's split editor does not call it, so this is reachable through the REST API, a personal access token or a script.
3. Open the transaction and the Savings register.
Expected: Either the delete is refused for a split whose last line is a transfer, or the parent becomes a plain -40.00 transfer to Savings (or the parent amount is re-derived from the lines).
Actual: With one line left, `removeSplit` calls `removeLinkedLeg` on the transfer line, deleting the +40.00 leg in Savings and reversing that balance, then sets the parent to `isSplit: false` with `categoryId` taken from the transfer line (null). The parent stays at -100.00, uncategorized, with no counterpart. The parent amount is never adjusted on any removal.
Evidence: reading

## SQ: redacted: security finding held for Garrett (FILING §4)

Severity: security

## LH: Deleting a category the dialog calls "not used" deletes payroll deduction rules and blanks budget lines

Severity: data-loss
Where: backend/src/categories/categories.service.ts:579, backend/src/categories/categories.service.ts:654, database/schema.sql:3640, database/schema.sql:2424, database/schema.sql:2472, at 93f4e68
What the user loses: A payroll deduction rule (yearly maximum, reset date, expected amount) keyed on the category is deleted; every budget line and budget period line for the category has its category set to null, so the budgeted amount disappears from the budget's totals.
Steps:
1. Create a category "CPP" with no transactions, add it to a budget with a monthly amount, and create a payroll deduction rule for it on a paycheque schedule.
2. Open the category's delete dialog.
3. Confirm.
Expected: The dialog counts the budget line and the payroll rule among the usages, or the delete is refused.
Actual: `getTransactionCount` sums transactions, transaction splits, scheduled transactions and scheduled splits only, so the dialog shows "This category is not used. It can be safely deleted." `payroll_deduction_rules.category_id` is `ON DELETE CASCADE`; `budget_categories.category_id` and `budget_period_categories.category_id` are `ON DELETE SET NULL`. The budget code reads only lines with a non-null category (budgets.service.ts:1044), so the orphaned line is ignored.
Evidence: reading

## LP: Deleting a payee that has transactions fails with a message that does not say why

Severity: stuck
Where: backend/src/payees/payees.service.ts:1297, database/schema.sql:385, backend/src/common/filters/http-error-body.ts:125, frontend/src/components/payees/PayeeList.tsx:577, at 93f4e68
What the user loses: A way to finish. The payee list offers Delete on every payee and the dialog says only that it cannot be undone; the attempt fails with "Referenced record does not exist or cannot be removed", which names neither the transactions nor the fix (reassign or merge).
Steps:
1. Open Payees, pick a payee with a non-zero transaction count, choose Delete, confirm.
Expected: Either the delete is refused up front with the count, like categories and accounts, or the dialog explains.
Actual: `remove` calls `repository.remove(payee)` with no check (payees.service.ts:1297). `transactions.payee_id REFERENCES payees(id)` (schema.sql:385) has no `ON DELETE` clause, so PostgreSQL refuses with 23503, which the filter turns into the generic 400 text (http-error-body.ts:125-132). `scheduled_transactions.payee_id` (schema.sql:1084) behaves the same way.
Evidence: reading

## DR: Deleting a transfer leg through the plain delete endpoint removes one leg only and leaves the counterpart holding the money

Severity: data-loss
Where: backend/src/transactions/transactions.service.ts:3250, backend/src/transactions/transactions.controller.ts:1578, database/schema.sql:402, at 93f4e68
What the user loses: The source leg is deleted and its balance reversed, while the destination leg survives with its link nulled and its balance intact, so the two accounts no longer agree.
Steps:
1. Create a 100.00 transfer from Chequing to Savings.
2. Call DELETE /transactions/{chequingLegId}. The web client sends transfers to DELETE /transactions/{id}/transfer (TransactionList.tsx:423), but the plain route accepts any id and is what a script, a personal access token or an older client would use.
3. Open the Savings register.
Expected: Both legs are removed, as the transfer route does, or the request is refused with a pointer to the transfer route (the AI and MCP paths already go through `removeAny` for this reason).
Actual: `remove()` handles only split-transfer legs (`parentSplit`). For a mirror leg it deletes the one row; the foreign key `linked_transaction_id ... ON DELETE SET NULL` detaches the other leg, which keeps its +100.00.
Evidence: reading

## FP: Reconciling a transaction stamps reconciledDate with the server's calendar day (formatDateYMDLocal(new Date())) while the same write decides 'future-dated' by the user's timezone day (todayYMD); for the hours the two calendars differ, 'reconciled through' and the account's last-reconciled date are a day off.

Severity: wrong-result
Where: backend/src/transactions/transaction-reconciliation.service.ts:167 vs 172; backend/src/common/date-utils.ts:55-60, 124-135; readers: transactions/stale-reconciliation.ts:63, accounts/accounts.service.ts:606, accounts/statement-cycle.service.ts:124, at 93f4e68
What the user loses: a user in America/Toronto reconciling at 21:30 gets `reconciled_date` = tomorrow; a user in Asia/Tokyo reconciling at 07:30 gets yesterday, so a row dated today shows "reconciled through" yesterday (`transactions/stale-reconciliation.ts:63`: `LEAST(transaction_date, COALESCE(reconciled_date, transaction_date))`), and the account list's last-reconciled date (`accounts/accounts.service.ts:606`) and the statement cycle (`accounts/statement-cycle.service.ts:124`) read a day early.
Steps:
1. Run the backend with `TZ` unset (UTC) and set the user's timezone to Asia/Tokyo.
2. At 07:30 Tokyo time, reconcile a transaction dated today.
3. Open the account's reconciliation panel.
Expected: reconciled through today.
Actual: reconciled through yesterday; the stored `reconciled_date` is yesterday's date.
Evidence: probe
```
America/Toronto  at 2026-11-03T02:30:00Z  row dated 2026-11-02
  user's today      = 2026-11-02
  reconciledDate    = 2026-11-03  <-- not the user's day
Asia/Tokyo       at 2026-11-02T22:30:00Z  row dated 2026-11-03
  user's today      = 2026-11-03
  reconciledDate    = 2026-11-02  <-- not the user's day
  reconciled-through (LEAST) = 2026-11-02
3 of 3 cases stamp a reconciledDate that is not the user's calendar day.
```

## JH: Deleting a category that no transaction uses silently deletes its payroll deduction rules and blanks its budget lines, loan interest/principal/overpayment/asset links, scheduled-occurrence overrides and shared postings: the referencer count covers transactions, splits, schedules and schedule splits only, and the foreign keys cascade or set null.

Severity: data-loss
Where: backend/src/categories/categories.service.ts:579-651 (remove), 654-698 (getTransactionCount); database/schema.sql:3640 (payroll_deduction_rules CASCADE), 2424, 2472 (budget lines SET NULL), 1197-1207 (accounts loan categories SET NULL), 1222 (scheduled_transaction_overrides SET NULL), 4722 (shared_postings SET NULL), at 93f4e68
What the user loses: a payroll deduction rule disappears with no message; a budget keeps a line that now reads "Uncategorized" (`budgets/budget-spending.util.ts:411-421`) and can never match spending again; a loan or mortgage whose interest category was required at setup (`accounts/loan-mortgage-account.service.ts:251`, `426`) is left with `interest_category_id = NULL`, which the setup path itself refuses.
Steps:
1. Create a category "Union dues" with no transactions.
2. Add a payroll deduction rule for it, and add it to a budget.
3. Delete the category from the Categories page.
Expected: the delete is refused with a count of what still uses the category (as it is for transactions), or the referencers are listed for reassignment.
Actual: the delete succeeds; the payroll deduction rule is gone and the budget line reads "Uncategorized".
Evidence: reading

## VL: The QIF/OFX/CSV import moves the account balance for every row before its status is consulted, so VOID rows and future-dated rows are added, and the correction is a post-import recompute inside a try/catch that only logs when it fails; the repo's own rule says VOID moves no balance on every path that writes one.

Severity: process
Where: backend/src/import/import-regular-processor.service.ts:154 (updateAccountBalance for every row; statusFromQifFlags returns VOID at import/qif-status.util.ts:47); backend/src/import/import-post-processing.service.ts:44-112, at 93f4e68
What the user loses: **import moves the balance for VOID and future rows, repaired afterwards.** process, reading. `import-regular-processor.service.ts:154`; the repair at `import-post-processing.service.ts:44-112` logs when it fails.
Steps:
Not run. Harmless when the post-import recompute succeeds; the inflated balance stays when it fails (logged as an error, not shown to the importer).
Evidence: reading

## XT: After an import the account balance is computed with the database server's calendar day, not the user's

Severity: wrong-result
Where: backend/src/import/import-post-processing.service.ts:78, backend/src/common/date-utils.ts:124, backend/src/accounts/accounts.service.ts:1739, at 93f4e68
What the user loses: For a user whose "today" differs from the server's (the app stores a per-user timezone and every interactive balance path uses it), rows dated on the boundary day are either left out of or prematurely folded into the balance shown right after the import. The hourly due-balance cron (accounts.service.ts:2484) corrects it later, so the wrong figure stands for up to an hour.
Steps:
1. Set the user timezone to one ahead of the server (server in UTC, user in Asia/Tokyo) and import a QIF at 07:00 local containing a row dated today (local).
2. Read the account balance.
Expected: The balance includes today's row, as `recalculateCurrentBalance` would (it passes `todayYMD()` in the user's zone).
Actual: The post-import query filters on `CURRENT_DATE`, which is still yesterday on the server, so today's row is excluded until the cron runs.
Evidence: reading

## GC: A QIF file whose dates use dots, or a date the parser cannot read, fails row by row with a database error instead of a parse message

Severity: crash
Where: backend/src/import/qif-parser.ts:607, backend/src/import/qif-parser.ts:657, backend/src/import/qif-parser.ts:555, backend/src/import/import-regular-processor.service.ts:124, backend/src/import/import.service.ts:525, at 93f4e68
What the user loses: The import of that file. Every row is written with the raw date string, PostgreSQL refuses each one, and the result lists one "Error importing transaction ... date/time field value out of range" per row rather than telling the user the date format was not recognised.
Steps:
1. Export a QIF from a European Quicken whose dates are written with dots ("D3.5.2026"), or any QIF with a date the parser does not recognise.
2. Preview and import it.
Expected: The preview reports the unrecognised date format, or the parser accepts dots as it accepts "/" and "-".
Actual: `normalizeDateSeparators` and both regexes in `parseQifDate` accept only "/" and "-" (qif-parser.ts:607-656); anything else is returned unchanged at qif-parser.ts:657, `detectDateFormat` falls back to MM/DD/YYYY, and the processor writes the string straight into `transactionDate` (import-regular-processor.service.ts:124). The per-row savepoint (import.service.ts:525-534) catches the database error and counts an error for every row. A row whose day and month were swapped by the wrong format ("13/03/2026" becoming "2026-13-03") fails the same way.
Evidence: probe
```
=== qif_date_probe.js
"13/03/2026"   MM/DD/YYYY -> "2026-13-03"
"2/30/2026"    MM/DD/YYYY -> "2026-02-30"
"3.5.2026"     DD/MM/YYYY -> "3.5.2026"
"03/05/202"    MM/DD/YYYY -> "202-03-05"
"not a date"   (auto)     -> "not a date"
```

## GG: Category delete runs its referencer count in one transaction and the delete in another; a transaction or split saved in between keeps its row and loses its category (FK SET NULL) with no refusal, the shape accounts.delete already closed for accounts (A26-M19).

Severity: wrong-result
Where: backend/src/categories/categories.service.ts:600-608 (count, own transaction) vs 630-641 (delete, own transaction); database/schema.sql:387, 430, at 93f4e68
What the user loses: **category delete counts in one transaction and deletes in another.** wrong-result, reading. `categories.service.ts:600-608` vs `630-641`; `transactions.category_id` is SET NULL (`schema.sql:387`).
Steps:
Not run (needs two concurrent requests against PostgreSQL).
Evidence: reading

## JN: "Twice a Month" steps to the 15th and month-end whatever the start date, so a bill on the 1st and 16th gets the wrong due dates

Severity: wrong-result
Where: backend/src/common/recurrence.ts:139, frontend/src/lib/frequency.ts:64, frontend/src/i18n/messages/en/scheduledTransactions.json:323, at 93f4e68
What the user loses: a scheduled item started on the 1st is next due on the 31st, then the 15th, and auto-posts on those days; the start day is never offered again. The label says "Twice a Month" and names no days; the loan label does ("Semi-Monthly (15th & month end)"). Both implementations agree and their tests assert it, so this may be a design the label hides rather than a defect.
Steps:
1. New scheduled transaction, frequency "Twice a Month", start date the 1st of next month.
2. Save and look at the next due dates (bills list, calendar).
Expected: the 1st and the 16th (or the two days the user chose).
Actual: the 31st, the 15th, the 28th, the 15th, ...
Evidence: probe
```
SEMIMONTHLY from 2026-01-01: 2026-01-01 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
SEMIMONTHLY from 2026-01-16: 2026-01-16 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31 -> 2026-04-15
SEMIMONTHLY from 2026-01-15: 2026-01-15 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
SEMIMONTHLY from 2026-01-31: 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31 -> 2026-04-15
MONTHLY from 2026-01-31 (anchor kept): 2026-01-31 -> 2026-02-28 -> 2026-03-31 -> 2026-04-30
```

## TX: Deleting an empty account silently deletes its scheduled bills and the transfer lines of other schedules that point at it

Severity: data-loss
Where: backend/src/accounts/accounts.service.ts:1413, backend/src/accounts/accounts.service.ts:2262, database/schema.sql:1082, database/schema.sql:1120, database/schema.sql:1158, backend/src/scheduled-transactions/scheduled-transactions.service.ts:3426, at 93f4e68
What the user loses: Every scheduled transaction (bill, deposit, loan payment) whose account is the deleted one, and every split line of any other schedule that transfers money into it. A scheduled transfer whose target was the deleted account is kept but silently turns into a plain expense.
Steps:
1. Create a new chequing account B with no transactions. Create a monthly scheduled bill "Rent" on B. Also give an existing schedule on account A a split line that transfers 200 to B.
2. On the Accounts page B shows as deletable ("no transactions"). Delete B and confirm the dialog, which only says the action cannot be undone.
3. Open Bills and Deposits, then open the schedule on A.
Expected: The delete is refused, or the dialog says the schedules will go, or the schedules survive without their account.
Actual: `assertAccountEmpty` (accounts.service.ts:1413) counts only `transactions` and `investment_transactions`. The `accounts` row is removed (accounts.service.ts:2262). `scheduled_transactions.account_id` is `ON DELETE CASCADE` (schema.sql:1082) so "Rent" disappears. `scheduled_transaction_splits.transfer_account_id` is `ON DELETE CASCADE` (schema.sql:1158) so the 200 line of A's schedule vanishes, leaving its lines no longer summing to its amount. `scheduled_transactions.transfer_account_id` is `ON DELETE SET NULL` (schema.sql:1120), and the posting code at scheduled-transactions.service.ts:3426 only writes a transfer when `transferAccountId` is set, so a scheduled transfer into B posts afterwards as an ordinary uncategorised transaction. Nothing is reported to the user; the account list's `canDelete` (accounts.service.ts:665) uses the same two counts.
Evidence: reading

## WF: Moving a category with subcategories under a parent of the other type leaves the subcategories as the old type

Severity: wrong-result
Where: backend/src/categories/categories.service.ts:507, backend/src/categories/categories.service.ts:526, frontend/src/components/categories/CategoryForm.tsx:93, at 93f4e68
What the user loses: Reports, budgets and the register's sign logic treat the moved category as income and its children as expenses (or the reverse), so an income tree contains expense lines and category totals are netted wrongly.
Steps:
1. Create expense category "Fees" with child "Bank fees".
2. Edit "Fees" and choose the income category "Salary" as its parent (the form allows any parent other than its own descendants and sets the type to match).
3. Open the category tree.
Expected: "Fees" and "Bank fees" both become income, as the server does when a top-level category's type is changed directly.
Actual: `update()` sets the moved category's type from the parent but calls `updateDescendantTypes` only when the category is top-level and the request itself carried the type flag. Neither holds for a re-parent, so the children keep the old type.
Evidence: probe
```
== category_reparent_probe
salary     parent=null    isIncome=true
fees       parent=salary  isIncome=true
bank-fees  parent=fees    isIncome=false
```

## SL: CSV import silently drops every row whose date it cannot read

Severity: data-loss
Where: backend/src/import/csv-parser.ts:1193, backend/src/import/csv-parser.ts:749, backend/src/import/csv-parser.ts:637, at 93f4e68
What the user loses: Rows of the bank statement that never reach the ledger, with no count, no message and no listing. With the wrong day/month order chosen, the rows with a day above 12 are dropped and the rest are imported on swapped dates, so the file looks imported.
Steps:
1. Export a statement from a bank that writes DD/MM/YYYY dates (most of Europe) and import it as CSV, leaving the date format on the default MM/DD/YYYY, or use any file whose dates carry a month name ("05 Mar 2026").
2. Map the columns and run the import.
3. Compare the register with the statement.
Expected: Unreadable dates are reported per row (the import result already has `skipped` and `skippedRows` for other reasons), or the import refuses the file.
Actual: `parseCsvDate` returns null for any day above 12 under MM/DD/YYYY and for any month-name date, and the loop at csv-parser.ts:1193-1197 does `continue` with no record. The rows with a day of 12 or less parse with month and day swapped. `parseCsv` returns no count of rows read versus rows kept, so the preview and the result cannot show the loss. `validateAndFormat` (csv-parser.ts:637) also accepts 30 February and 31 April; those rows fail only at the database and are then reported, which the dropped rows are not.
Evidence: probe
```
=== csv_date_probe.js
A DD/MM/YYYY statement imported under the MM/DD/YYYY mapping:
   05/03/2026 -> 2026-05-03  (imported with month and day swapped)
   12/03/2026 -> 2026-12-03  (imported with month and day swapped)
   13/03/2026 -> null  (row silently dropped)
   28/03/2026 -> null  (row silently dropped)
Impossible calendar dates accepted and handed to the database:
   02/30/2026 -> 2026-02-30
   04/31/2026 -> 2026-04-31
   2026-02-29 -> 2026-02-29
Month-name dates: MMM is not a token, so every row of such a file is dropped:
   05 Mar 2026 under DD MMM YYYY -> null
Control: 2026-03-05 14:30 under YYYY-MM-DD -> 2026-03-05
```

## CG: A rule that converts a future-dated transaction into a transfer can put a leg into a closed account

Severity: wrong-result
Where: backend/src/transactions/convert-to-transfer.ts:165, at 93f4e68
What the user loses: A closed account that stays closed. On the due date the hourly fold moves the closed account's balance, which the user cannot touch without reopening it, the situation the account-close checks exist to prevent.
Steps:
1. Close account B (balance 0). Keep a transaction rule whose action converts matching rows into a transfer to B.
2. Enter a matching transaction dated next week.
Expected: The conversion is refused, as `assertAccountOpen` refuses a future-dated create and `assertAccountsOpen` refuses a future-dated transfer into a closed account.
Actual: `convertRowToTransfer` checks that the target exists and shares the currency, writes the counterpart, and for a future date calls `recalculateCurrentBalance` (convert-to-transfer.ts:165-166), which has no closed check. Only the past-dated branch, `updateBalance` with `openOnly`, would have refused.
Evidence: reading

## JK: Reassigning a category fails with a database error once the user has more than 65,535 transactions

Severity: crash
Where: backend/src/categories/categories.service.ts:723, backend/src/categories/categories.service.ts:738, backend/src/categories/categories.service.ts:751, at 93f4e68
What the user loses: with a long history (the README's own case is thirty years of Money data) they cannot reassign a category's transactions, and so cannot delete a category the guard says to reassign first. The method selects every transaction id the user owns and binds the whole list as one IN (...) parameter per id; the PostgreSQL protocol carries the parameter count in 16 bits, so a list over 65,535 ids cannot be bound and the request fails. The same shape, with the smaller scheduled-transaction list, is in getTransactionCount (:677-690).
Steps:
1. A user with more than 65,535 transactions.
2. Categories page: reassign any category's transactions to another (POST /categories/<id>/reassign).
Expected: the rows move and a count is returned.
Actual: 500; nothing moves (one transaction, rolled back).
Evidence: reading

## LM: The reconciled date is stamped with the server's local calendar day, not the user's

Severity: wrong-result
Where: backend/src/transactions/transaction-reconciliation.service.ts:167, backend/src/common/date-utils.ts:124, backend/src/accounts/statement-cycle.service.ts:124, backend/src/accounts/accounts.service.ts:606, at 93f4e68
What the user loses: A row marked reconciled from the register at 20:00 in Toronto on the 4th (server in UTC) stores a reconciled date of 2026-11-05. The "last reconciled" date on the accounts list and the statement cycle read that column.
Steps:
1. With the server clock in UTC and the user's timezone America/Toronto, click a row's status cell to RECONCILED at 20:00 local on 2026-11-04.
2. Read the row's reconciled date.
Expected: 2026-11-04, the day the user did it (`todayYMD()` is the request-zone helper every other date decision uses).
Actual: `formatDateYMDLocal(new Date())` uses the server process's local date.
Evidence: reading

## QR: A "Twice a Month" schedule abandons the day the user chose

Severity: wrong-result
Where: backend/src/common/recurrence.ts:92, backend/src/scheduled-transactions/schedule-cursor.ts:29, frontend/src/i18n/messages/en/scheduledTransactions.json:323, at 93f4e68
What the user loses: A bill set up as "Twice a Month" starting on the 1st (or any day up to the 15th) is next due on the last day of that month and then on the 15th and month end thereafter; the chosen day never recurs and the first interval is up to 30 days. The bills list, forecast and auto-post all follow these dates.
Steps:
1. Create a scheduled bill, frequency "Twice a Month", next due 2026-01-01.
2. Post it and look at the next due date; repeat.
Expected: 2026-01-01, 2026-01-16 (or 15th), 2026-02-01, ... or at minimum a label that says the cadence is "15th and month end".
Actual: The SEMIMONTHLY branch returns month end for any day of 15 or less and the 15th of the next month otherwise. The scheduled-transactions label is "Twice a Month"; only the loan form says "(15th & month end)".
Evidence: probe
```
start 2026-01-01: 2026-01-01 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
start 2026-01-10: 2026-01-10 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
start 2026-01-20: 2026-01-20 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31 -> 2026-04-15
```

## WV: Deleting a transfer leg through the single-transaction route leaves a one-sided transfer

Severity: wrong-result
Where: backend/src/transactions/transactions.service.ts:3250, backend/src/transactions/transactions.service.ts:3342, backend/src/transactions/transactions.controller.ts:1578, database/schema.sql:402, at 93f4e68
What the user loses: A correct balance in the other account. One leg of a transfer is removed and its balance reversed, while the counterpart stays, still marked as a transfer, with its money, now linked to nothing.
Steps:
1. Create a transfer of 100 from Chequing to Savings.
2. Call `DELETE /api/transactions/{id}` on the Chequing leg (a personal access token, a script, or any client other than the two register screens, which branch to the `/transfer` route). Nothing refuses it.
3. Look at Savings.
Expected: Either both legs go, as `DELETE /transactions/{id}/transfer` does, or the request is refused with "use the transfer route", as the joint-register path does with `assertPlainRow`.
Actual: `remove` handles a split-transfer leg (`parentSplit`) and a split parent (`locked.isSplit`) but never looks at `isTransfer` or `linkedTransactionId`. It deletes the one row at transactions.service.ts:3342 and reverses its amount. The counterpart's `linked_transaction_id` is set to null by the foreign key (schema.sql:402, `ON DELETE SET NULL`), it keeps `is_transfer = true`, and Savings keeps the 100. The controller's `DELETE /:id` (transactions.controller.ts:1578-1598) calls `remove`, not `removeAny`, which is the dispatcher the AI and MCP paths use.
Evidence: reading

## PC: The reconcile screen lets a statement that is one cent off be finished as balanced

Severity: wrong-result
Where: frontend/src/app/reconcile/page.tsx:381, frontend/src/app/reconcile/page.tsx:389, at 93f4e68
What the user loses: Rows are marked RECONCILED while the cleared balance and the statement differ by 0.01, so a one-cent discrepancy is silently absorbed instead of being found.
Steps:
1. Start a reconciliation with statement balance 1000.01 where the reconciled balance plus the selected rows is 1000.00.
2. Press Finish.
Expected: Refused until the difference is 0.00 (the difference panel shows 0.01).
Actual: The check is `Math.abs(calculatedDifference) > 0.01` after rounding to cents, so exactly 0.01 passes.
Evidence: probe
```
{"calculatedDifference":0,"finishAllowed":true}
{"calculatedDifference":0.01,"finishAllowed":true}
{"calculatedDifference":-0.01,"finishAllowed":true}
{"calculatedDifference":0.02,"finishAllowed":false}
```
