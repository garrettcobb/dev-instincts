# Findings

## 1: Deleting a category that no transaction uses silently deletes its payroll deduction rules and blanks its budget lines, loan interest/principal/overpayment/asset links, scheduled-occurrence overrides and shared postings: the referencer count covers transactions, splits, schedules and schedule splits only, and the foreign keys cascade or set null.
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

## 2: Reconciling a transaction stamps reconciledDate with the server's calendar day (formatDateYMDLocal(new Date())) while the same write decides 'future-dated' by the user's timezone day (todayYMD); for the hours the two calendars differ, 'reconciled through' and the account's last-reconciled date are a day off.
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

## 3: The absolute balance recomputes after an undo and after an import bound the ledger by Postgres CURRENT_DATE (the database's day, UTC in the shipped containers), while AccountsService.recalculateCurrentBalance and every delta path bound it by the user's timezone day; for the hours the two days differ the stored balance includes or omits a day's rows and flips back on the next edit.
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

## 4: Reassigning a category's transactions loads every transaction id the user owns and binds them into one IN (...) list; past the Postgres bind limit (65,535 parameters, about 65,000 transactions) the statement fails and the category can be neither reassigned nor deleted. The scheduled-split count and update do the same with schedule ids.
Severity: crash
Where: backend/src/categories/categories.service.ts:721-741 (getMany at 727, IN at 738); 674-690 and 749-766 (schedule ids), at 93f4e68
What the user loses: for a long Microsoft Money or Quicken history (the import this app is built for), "reassign transactions" for a category errors out, and because `remove` requires a zero count, the category can be neither emptied nor deleted. The message is a database error, not a domain one.
Steps:
1. Import a history of 70,000 transactions (any account mix).
2. Categories, pick any category, Reassign transactions to another category.
Expected: the rows move.
Actual: the request fails with a database error (bind parameter count), and the category cannot be deleted afterwards either.
Evidence: reading

## 5: Deleting a payee checks no referencers on any door (REST, AI batch action, MCP tool); transactions.payee_id and scheduled_transactions.payee_id have no ON DELETE action, so the database refuses and the user gets the generic 400 'Referenced record does not exist or cannot be removed' with no count and no pointer to Merge.
Severity: stuck
Where: backend/src/payees/payees.service.ts:1280-1308; database/schema.sql:385, 1084; backend/src/common/filters/http-error-body.ts:125; backend/src/ai/actions/ai-actions.service.ts:716-718; backend/src/mcp/tools/payees.tool.ts:604, 656, 750, at 93f4e68
What the user loses: **payee delete has no referencer check on any door.** stuck, reading. `payees.service.ts:1280-1308`; FKs without ON DELETE at `schema.sql:385`, `1084`; the filter maps 23503 to a generic 400 (`http-error-body.ts:125`). Same on the AI batch action and the MCP tool.
Steps:
Delete a payee that has one transaction (REST or the AI delete_payee action): 400 with the generic referenced-record message; the payee stays.
Evidence: reading

## 6: Category delete runs its referencer count in one transaction and the delete in another; a transaction or split saved in between keeps its row and loses its category (FK SET NULL) with no refusal, the shape accounts.delete already closed for accounts (A26-M19).
Severity: wrong-result
Where: backend/src/categories/categories.service.ts:600-608 (count, own transaction) vs 630-641 (delete, own transaction); database/schema.sql:387, 430, at 93f4e68
What the user loses: **category delete counts in one transaction and deletes in another.** wrong-result, reading. `categories.service.ts:600-608` vs `630-641`; `transactions.category_id` is SET NULL (`schema.sql:387`).
Steps:
Not run (needs two concurrent requests against PostgreSQL).
Evidence: reading

## 7: The QIF/OFX/CSV import moves the account balance for every row before its status is consulted, so VOID rows and future-dated rows are added, and the correction is a post-import recompute inside a try/catch that only logs when it fails; the repo's own rule says VOID moves no balance on every path that writes one.
Severity: process
Where: backend/src/import/import-regular-processor.service.ts:154 (updateAccountBalance for every row; statusFromQifFlags returns VOID at import/qif-status.util.ts:47); backend/src/import/import-post-processing.service.ts:44-112, at 93f4e68
What the user loses: **import moves the balance for VOID and future rows, repaired afterwards.** process, reading. `import-regular-processor.service.ts:154`; the repair at `import-post-processing.service.ts:44-112` logs when it fails.
Steps:
Not run. Harmless when the post-import recompute succeeds; the inflated balance stays when it fails (logged as an error, not shown to the importer).
Evidence: reading
