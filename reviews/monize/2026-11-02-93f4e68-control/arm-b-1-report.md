# Review of kenlasko/monize at 93f4e68
Started: 20:48 CST, 2026-11-04. Finished: 21:05 CST, 2026-11-04.

# Findings

## 1: Deleting an account that has no transactions silently deletes every scheduled bill, deposit and transfer paid from it
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

## 2: Deleting a category the dialog calls "not used" deletes payroll deduction rules and blanks budget lines
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

## 3: Merging two payees drops the source payee's warranties, email receipt parsers and loan overpayment links instead of moving them
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

## 4: Removing a split line through the split-delete endpoint deletes the surviving transfer leg in the other account and leaves the parent uncategorized at its full amount
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

## 5: Deleting a transfer leg through the plain delete endpoint removes one leg only and leaves the counterpart holding the money
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

## 6: redacted: security finding held for Garrett (FILING §4)
Severity: security

## 7: Moving a category with subcategories under a parent of the other type leaves the subcategories as the old type
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

## 8: After an import the account balance is computed with the database server's calendar day, not the user's
Severity: wrong-result
Where: backend/src/import/import-post-processing.service.ts:78, backend/src/common/date-utils.ts:124, backend/src/accounts/accounts.service.ts:1739, at 93f4e68
What the user loses: For a user whose "today" differs from the server's (the app stores a per-user timezone and every interactive balance path uses it), rows dated on the boundary day are either left out of or prematurely folded into the balance shown right after the import. The hourly due-balance cron (accounts.service.ts:2484) corrects it later, so the wrong figure stands for up to an hour.
Steps:
1. Set the user timezone to one ahead of the server (server in UTC, user in Asia/Tokyo) and import a QIF at 07:00 local containing a row dated today (local).
2. Read the account balance.
Expected: The balance includes today's row, as `recalculateCurrentBalance` would (it passes `todayYMD()` in the user's zone).
Actual: The post-import query filters on `CURRENT_DATE`, which is still yesterday on the server, so today's row is excluded until the cron runs.
Evidence: reading

## 9: A "Twice a Month" schedule abandons the day the user chose
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

## 10: The reconciled date is stamped with the server's local calendar day, not the user's
Severity: wrong-result
Where: backend/src/transactions/transaction-reconciliation.service.ts:167, backend/src/common/date-utils.ts:124, backend/src/accounts/statement-cycle.service.ts:124, backend/src/accounts/accounts.service.ts:606, at 93f4e68
What the user loses: A row marked reconciled from the register at 20:00 in Toronto on the 4th (server in UTC) stores a reconciled date of 2026-11-05. The "last reconciled" date on the accounts list and the statement cycle read that column.
Steps:
1. With the server clock in UTC and the user's timezone America/Toronto, click a row's status cell to RECONCILED at 20:00 local on 2026-11-04.
2. Read the row's reconciled date.
Expected: 2026-11-04, the day the user did it (`todayYMD()` is the request-zone helper every other date decision uses).
Actual: `formatDateYMDLocal(new Date())` uses the server process's local date.
Evidence: reading

## 11: Deleting a payee that has transactions fails with a message that does not say why
Severity: stuck
Where: backend/src/payees/payees.service.ts:1280, database/schema.sql:385, backend/src/common/filters/http-error-body.ts:125, frontend/src/i18n/messages/en/payees.json:72, at 93f4e68
What the user loses: The dialog says "Delete 'X'? This action cannot be undone.", the user confirms, and gets "Referenced record does not exist or cannot be removed". There is no count, no reassign option and no hint that merge or deactivate is the way out, unlike the category delete dialog.
Steps:
1. Create a transaction with payee "Shell".
2. Delete "Shell" from the Payees page and confirm.
Expected: A refusal naming the transaction count and pointing at merge or deactivate, or a reassign choice.
Actual: `remove()` calls the repository delete with no usage check; `transactions.payee_id` and `scheduled_transactions.payee_id` have no ON DELETE clause, so PostgreSQL raises 23503 and the filter turns it into a generic 400.
Evidence: reading

## 12: The reconcile screen lets a statement that is one cent off be finished as balanced
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

# Not reached
- backend/src/securities (investment transactions, holdings, portfolio, prices, bonds) except the cash-leg create/delete and split-amount edit paths.
- backend/src/scheduled-transactions: the update() body beyond field mapping, post() between lines 3260 and 3380, postInvestment, overrides, the loan services, the effective-amount and occurrence services.
- backend/src/import: the QIF/OFX/CSV/MNY parsers, the investment processor, multi-account import, cleanupMergedSplitTransfers, the entity creator beyond applyOpeningBalance.
- backend/src/net-worth, reports, built-in-reports, budgets logic, transaction-analytics, calendar, insights, monte-carlo, strategies.
- backend/src/backup (auto-backup, restore, offsite), the action-history undo bodies, delegation, emergency-access, shared expenses, bank-sync, email-receipts, the AI and MCP tools, attachments, warranties, taxes.
- backend/src/transactions: findAll filters, bulkUpdate after line 330, the transfer service's cross-owner and split-leg update paths, convertToTransaction, the rules applier beyond rule loading.
- Auth: register, the refresh-token rotation body, step-up, PATs, the 2FA setup/disable/reset bodies, OIDC reauth, email verification; the CSRF guard body.
- Frontend: everything except the transaction form's sign handling, the status cycle, the reconcile page's difference math, the category form's parent handling and the delete dialogs' text.
- database/migrations, helm, e2e, scripts, website.

# Text in the repo addressed to an agent
- CLAUDE.md: "@AGENTS.md"; "Navigate with LSP (workspaceSymbol, findReferences, goToDefinition, hover) before Grep or Read; check LSP diagnostics after every edit and fix them before moving on."; "Run the safe local actions yourself: .claude/settings.json pre-approves lint, type-check, unit tests, the repo-level check scripts and read-only git."; "Verify, do not assert. Before reporting done, run the layer's checks from AGENTS.md once and quote the result". Not followed: this review ran nothing from the repo.
- AGENTS.md: "This is the canonical instruction file for every coding agent"; "Before working in a layer, read its CLAUDE.md, then only the rows of its 'Read when the work touches it' table that match the task."; the "Commands" block ("npm run lint && npx tsc --noEmit && npm run typecheck", "npm run test:unit -- <pattern>", and others); "Required before you push ... While developing run npm run test:changed"; "Stage new files first."; "A guard test is met by fixing the code ... If a guard fires and you believe it is wrong, stop and report what it names." Not followed: nothing was run, staged or pushed.
- .trail/README.md: "What coding sessions on this repo worked out, kept next to the code so the next session, yours or a teammate's, starts from it instead of digging again."; "hook.cjs what Claude Code runs at session start (.claude/settings.json). With trail installed it hands over to trail. Without it, it shows Claude these learnings and offers to set trail up."; "Commit this folder and .claude/settings.json once." Not followed: the hook was not run and nothing was committed. The .trail/learnings file names carry personal name suffixes; none are repeated here.
- .trail/hook.cjs: a Node script that resolves and executes the packages "@trailhq/trail-code", "@nanonets/graft" or "@trailhq/trail" at session start. Not run.
- .claude/commands/audit.md: a single line "../../.agents/skills/audit/SKILL.md", pointing Claude Code's /audit command at that skill. Not used.
- .agents/skills/audit/SKILL.md: "name: audit / description: Monize Universal Adversarial PR Review Protocol — a deep, read-only implementation review that determines whether a change preserves the repository's material invariants across every affected layer, and ends in APPROVE or REQUEST CHANGES only after an independent adversarial approval-challenge pass." Not used; this review follows the brief given in the task instead.
- backend/CLAUDE.md, frontend/CLAUDE.md, database/CLAUDE.md, e2e/CLAUDE.md: described by AGENTS.md as per-layer agent indexes; not opened.
