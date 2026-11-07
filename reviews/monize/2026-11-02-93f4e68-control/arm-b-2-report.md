# Review of kenlasko/monize at 93f4e68
Started: 2026-11-04 23:41 CST. Finished: 2026-11-05 00:07 CST.

# Findings

## 1: Deleting an empty account silently deletes its scheduled bills and the transfer lines of other schedules that point at it
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

## 2: CSV import silently drops every row whose date it cannot read
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

## 3: CSV import stores zero, or the wrong sign, for amounts it cannot read
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

## 4: Deleting a category detaches budget lines and deletes payroll deduction rules without warning
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

## 5: Deleting a transfer leg through the single-transaction route leaves a one-sided transfer
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

## 6: Removing one split line through the API leaves the parent amount and the account balance unchanged
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

## 7: Reassigning a category's transactions fails for a user with more than 65535 transactions
Severity: crash
Where: backend/src/categories/categories.service.ts:721, backend/src/categories/categories.service.ts:738, backend/src/categories/categories.service.ts:751, backend/src/categories/categories.service.ts:763, at 93f4e68
What the user loses: The ability to move a category's transactions to another category, which is also the step the delete-category error tells them to take.
Steps:
1. Have a ledger with more than 65535 transactions (a twenty-year Money or Quicken import).
2. On a category, choose to reassign its transactions to another category.
Expected: The reassign completes.
Actual: `reassignTransactions` loads every transaction id of the user (categories.service.ts:721-727) and passes the whole list as `IN (:...transactionIds)` (categories.service.ts:738). TypeORM expands each id to its own bind parameter, and the PostgreSQL wire protocol carries the bind-parameter count as a 16-bit integer, so a statement with more than 65535 parameters cannot be executed and the query fails. The whole transaction is rolled back and the request fails with a database error. The same list is built again for scheduled splits (categories.service.ts:751-767), bounded by the number of schedules. The split filter only needs `transaction.user_id`, which the `getTransactionCount` query a few lines above already uses as a join.
Evidence: reading

## 8: The balance written after an import, and by undo, is bounded by the database server's date, not the user's
Severity: wrong-result
Where: backend/src/import/import-post-processing.service.ts:81, backend/src/action-history/action-history.service.ts:2111, backend/src/net-worth/net-worth.service.ts:2849, backend/src/net-worth/net-worth.service.ts:2937, backend/src/accounts/accounts.service.ts:1747, at 93f4e68
What the user loses: A balance that matches the register for part of the day. Every other balance writer bounds the ledger at `todayYMD()`, today in the user's timezone; these sites use SQL `CURRENT_DATE`, the server's date. The monthly net-worth history is cut at the same server date (net-worth.service.ts:2849, 2937), so its current month and the live balance can disagree over today's rows.
Steps:
1. Run the server in UTC. As a user in Australia at 09:00 on the 5th (still the 4th in UTC), import a statement that includes the 5th's transactions.
2. Look at the account balance right after the import, then compare with the register's running balance.
Expected: The balance includes every row dated on or before the user's today, as `recalculateCurrentBalance` (accounts.service.ts:1747) computes it.
Actual: The post-import recomputation sums rows with `transaction_date <= CURRENT_DATE` (import-post-processing.service.ts:81), so the 5th's rows are excluded and the balance is lower than the register until the hourly fold rewrites it. For a user west of the server (US evening), rows the user dated tomorrow are included instead. Undo of a transaction action recomputes the same way (action-history.service.ts:2111) and the figure then disagrees with the one the deleted or restored row's own path wrote. Both are corrected by the hourly `applyDueTransactionBalances` only when the account has a row inside its 7-day window.
Evidence: reading

## 9: The budget page's "current period" is picked by the UTC month, so late on the last day of the month it shows next month
Severity: wrong-result
Where: backend/src/budgets/budget-date.utils.ts:15, backend/src/budgets/budgets.service.ts:1000, backend/src/budgets/budget-reports.service.ts:371, at 93f4e68
What the user loses: The right month's budget. A user west of UTC opening Budgets on the evening of the 31st sees next month's period, with zero spending, and the "previous month" report points at the month that is still in progress.
Steps:
1. Set the user's timezone to America/Los_Angeles. At 18:00 local on 31 October (01:00 UTC on 1 November) open the Budgets page.
Expected: October is the current period.
Actual: `getCurrentMonthPeriodDates` uses `new Date()` with `getUTCFullYear` and `getUTCMonth`, and `getCurrentPeriodDates` (budgets.service.ts:1000) and the reports (budget-reports.service.ts:363-371) call it. Everything else dates the user's "today" with `todayYMD()`.
Evidence: reading

## 10: A rule that converts a future-dated transaction into a transfer can put a leg into a closed account
Severity: wrong-result
Where: backend/src/transactions/convert-to-transfer.ts:165, at 93f4e68
What the user loses: A closed account that stays closed. On the due date the hourly fold moves the closed account's balance, which the user cannot touch without reopening it, the situation the account-close checks exist to prevent.
Steps:
1. Close account B (balance 0). Keep a transaction rule whose action converts matching rows into a transfer to B.
2. Enter a matching transaction dated next week.
Expected: The conversion is refused, as `assertAccountOpen` refuses a future-dated create and `assertAccountsOpen` refuses a future-dated transfer into a closed account.
Actual: `convertRowToTransfer` checks that the target exists and shares the currency, writes the counterpart, and for a future date calls `recalculateCurrentBalance` (convert-to-transfer.ts:165-166), which has no closed check. Only the past-dated branch, `updateBalance` with `openOnly`, would have refused.
Evidence: reading

## 11: Quick-fill copies an amount rounded to two decimals
Severity: wrong-result
Where: frontend/src/components/transactions/TransactionForm.tsx:798, at 93f4e68
What the user loses: Fractions of a cent, or the third decimal of a currency like KWD or BHD, when a recent transaction is used to pre-fill a new one. The rest of the form works at four decimals (`roundMoney`).
Steps:
1. In an account in a three-decimal currency, have a transaction of 12.345. Open the new-transaction form and quick-fill from that row.
Expected: 12.345.
Actual: `Math.round(Number(source.amount) * 100) / 100` gives 12.35 (TransactionForm.tsx:798).
Evidence: reading

## 12: Deleting a payee that has transactions fails with a message that does not say why
Severity: stuck
Where: backend/src/payees/payees.service.ts:1297, database/schema.sql:385, backend/src/common/filters/http-error-body.ts:125, frontend/src/components/payees/PayeeList.tsx:577, at 93f4e68
What the user loses: A way to finish. The payee list offers Delete on every payee and the dialog says only that it cannot be undone; the attempt fails with "Referenced record does not exist or cannot be removed", which names neither the transactions nor the fix (reassign or merge).
Steps:
1. Open Payees, pick a payee with a non-zero transaction count, choose Delete, confirm.
Expected: Either the delete is refused up front with the count, like categories and accounts, or the dialog explains.
Actual: `remove` calls `repository.remove(payee)` with no check (payees.service.ts:1297). `transactions.payee_id REFERENCES payees(id)` (schema.sql:385) has no `ON DELETE` clause, so PostgreSQL refuses with 23503, which the filter turns into the generic 400 text (http-error-body.ts:125-132). `scheduled_transactions.payee_id` (schema.sql:1084) behaves the same way.
Evidence: reading

## 13: A QIF file whose dates use dots, or a date the parser cannot read, fails row by row with a database error instead of a parse message
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

# Not reached
Read in full or in the parts that matter: transaction create, update, remove and the parent-split removal; the deletion-balance helper; the row lock helpers; account delete, close, reopen, update, updateBalance, recalculateCurrentBalance and the hourly due-balance fold; category remove, count and reassign; payee remove; transfer create (leg writing), update (balance section) and remove (entry); convert-to-transfer; split validation, createSplits entry, addSplit, removeSplit; bulk update (first half) and bulk delete (first half); reconciliation data, bulk reconcile and status transitions; the recurrence and schedule-cursor math; scheduled skip and the first half of post; the CSV and QIF date and amount parsers; the QIF import loop's savepoint handling; import post-processing; the budget date utilities; the loan amortization utilities; the frontend running-balance walk, frequency math, date parsing, the transaction form's rounding and delete call sites. For security only: the refresh-token rotation, TOTP check and replay claim, password reset, 2FA disable and reset routes, context switch, PAT hashing, OIDC state and nonce presence, the attachment download guard, the delegate decorators and the joint-register row guard. Nothing wrong was found in the security paths read.

Not read: the register query and its page starting balance (transactions.service.ts 1268-1600); the transaction analytics, search and tool-prep services; the second half of bulk update and bulk delete; the split service's updateSplits and transfer-counterpart propagation; the transfer service's cross-owner paths and preview methods; most of the scheduled-transactions service (create, update, auto-post cron, loan posting, effective amounts, overrides); the import service beyond the loop (QIF multi-account, OFX, .mny, investment processing, dedupe); bank sync; backup export and restore; net worth; reports and built-in reports; securities, bonds, holdings and portfolio calculations; budgets beyond the date utilities; loans, mortgages, scenarios and installments; AI, MCP and email-receipt actions beyond their delete dispatch; notifications, push, warranties, shared expenses, emergency access; the OIDC callback body, the login and lockout code, step-up, RLS policies and migrations; the frontend beyond the files named above; the e2e suite.

# Text in the repo addressed to an agent
All of it is instruction to coding agents working on the repository. None of it was followed; the review was read-only.

- `AGENTS.md`: "This is the canonical instruction file for every coding agent; `CLAUDE.md` imports it and adds only what Claude Code specifically should do." It then lists commands to run ("Run from the layer directory. ... `npm run lint && npx tsc --noEmit && npm run typecheck`"), "Required before you push" steps, and rules such as "A guard test is met by fixing the code. Baselines, allowlists and grandfather lists are shrink-only. If a guard fires and you believe it is wrong, stop and report what it names."
- `CLAUDE.md`: "@AGENTS.md ... **Navigate with LSP** (`workspaceSymbol`, `findReferences`, `goToDefinition`, `hover`) before Grep or Read; check LSP diagnostics after every edit and fix them before moving on. ... **Run the safe local actions yourself**: `.claude/settings.json` pre-approves lint, type-check, unit tests, the repo-level check scripts and read-only git. ... **Verify, do not assert.** Before reporting done, run the layer's checks from `AGENTS.md` once and quote the result".
- `backend/CLAUDE.md`, `frontend/CLAUDE.md`, `database/CLAUDE.md`, `e2e/CLAUDE.md`: layer indexes, e.g. backend: "This file is an index. The rules themselves live in `docs/backend/` ... Before changing a balance, a holding, a transfer, a scheduled occurrence, a cron, a token, or anything that writes outside PostgreSQL, read the relevant one and name its ID in the PR".
- `.claude/settings.json`: a permissions allow-list ("Bash(npm run lint*)", "Bash(npm install*)", "Bash(git add*)", "Bash(git checkout -b*)" and more) and a hook entry pointing at `.trail/hook.cjs`.
- `.trail/README.md`: "hook.cjs     what Claude Code runs at session start (`.claude/settings.json`). With trail installed it hands over to trail. Without it, it shows Claude these learnings and offers to set trail up." `.trail/hook.cjs` is a Node script that resolves and runs an external package ("The same code ships as @trailhq/trail-code and as @nanonets/graft"); it was not run. `.trail/learnings/` holds dated markdown notes from earlier sessions.
- `.claude/commands/audit.md` is a link to `.agents/skills/audit/SKILL.md`: "name: audit ... Monize Universal Adversarial PR Review Protocol — a deep, read-only implementation review ... You are performing deep, read-only implementation reviews of pull requests and feature branches in the `monize` repository."
