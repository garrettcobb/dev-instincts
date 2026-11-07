# Monize: issue drafts, round 2026-11-02-93f4e68-review

Target: kenlasko/monize, `main` at `93f4e68` (2026-11-03 02:47 UTC). No dev branch; releases come from `main`. The repo has no issue template, so the §5 form is used as is. Nothing here is filed until Garrett says go for the batch. Four drafts (cap is six).

Duplicate check (read-only `gh api search/issues`, 2026-11-03): queries `payee delete`, `delete payee transactions`, `category delete budget`, `reconciled date`, `reconciled_date`, `timezone day`, `reassign parameters`, `bind message`, `delete category` returned no issue or PR describing any of the four below. #1931/#1935 (remove a category from a budget) and #1754 (loan interest category required) are adjacent and make MZ-L01 more consequential, not duplicates. #1911 fixed an auto-post timezone case, not the reconcile stamp.

---

## Draft 1 (MZ-L01)

**Title:** [Bug] Deleting an unused category silently deletes its payroll deduction rules and blanks its budget lines and loan category links

**Version:** `main` at `93f4e68`.

**Summary:** `CategoriesService.remove` refuses a delete only when `getTransactionCount` is non-zero, and that count covers transactions, transaction splits, scheduled transactions and scheduled splits (`backend/src/categories/categories.service.ts:654-698`). The schema has more tables pointing at `categories`: `payroll_deduction_rules.category_id` is `ON DELETE CASCADE` (`database/schema.sql:3640`); `budget_categories.category_id` and `budget_period_categories.category_id` are `ON DELETE SET NULL` (`schema.sql:2424`, `2472`); the loan columns `accounts.principal_category_id`, `interest_category_id`, `overpayment_category_id`, `asset_category_id` are `ON DELETE SET NULL` (`schema.sql:1197-1207`); so are `scheduled_transaction_overrides.category_id` (`schema.sql:1222`) and `shared_postings.category_id` (`schema.sql:4722`). None of them is counted, so a category with no transactions deletes cleanly and the database quietly removes or detaches those rows.

**Result:** a payroll deduction rule disappears with no message; a budget keeps a line that now reads "Uncategorized" (`budgets/budget-spending.util.ts:411-421`) and can never match spending again; a loan or mortgage whose interest category was required at setup (`accounts/loan-mortgage-account.service.ts:251`, `426`) is left with `interest_category_id = NULL`, which the setup path itself refuses.

**Where:** `backend/src/categories/categories.service.ts:579-651`, `654-698`; `database/schema.sql:3640`, `2424`, `2472`, `1197-1207`, `1222`, `4722`.

**Steps:**
1. Create a category "Union dues" with no transactions.
2. Add a payroll deduction rule for it, and add it to a budget.
3. Delete the category from the Categories page.
4. *Expected:* the delete is refused with a count of what still uses the category (as it is for transactions), or the referencers are listed for reassignment.
   *Actual:* the delete succeeds; the payroll deduction rule is gone and the budget line reads "Uncategorized".

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and the schema. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** the referencer count also runs in its own transaction before the deleting one (`categories.service.ts:600-608` vs `630-641`), so a transaction saved in between keeps its row and loses its category through `transactions.category_id ON DELETE SET NULL` (`schema.sql:387`) with no refusal; `accounts.delete` already re-checks under the lock inside the deleting transaction (`accounts.service.ts:2238-2248`) for the same reason.

**Possible fix:** count every table whose foreign key points at `categories` (or let one query over `information_schema.referential_constraints` drive it), do the count inside the deleting transaction, and refuse with the breakdown. A test that creates a category used only by a payroll rule and only by a budget line, deletes it, and expects a refusal in both cases would catch this.

---

## Draft 2 (MZ-L02)

**Title:** [Bug] Reconciling near midnight stamps the reconciled date with the server's day, not the user's

**Version:** `main` at `93f4e68`.

**Summary:** `applyStatusTransition` sets `fields.reconciledDate = formatDateYMDLocal(new Date())` (`backend/src/transactions/transaction-reconciliation.service.ts:167`), which is the backend process's local calendar day (UTC in the shipped containers). Five lines later the same write decides whether the row is future-dated with `isTransactionInFuture(locked.transactionDate)` (`:172`), which goes through `todayYMD()` and the request's timezone (`common/date-utils.ts:124-135`). For the hours in which the user's day and the server's day differ, the two decisions disagree.

**Result:** a user in America/Toronto reconciling at 21:30 gets `reconciled_date` = tomorrow; a user in Asia/Tokyo reconciling at 07:30 gets yesterday, so a row dated today shows "reconciled through" yesterday (`transactions/stale-reconciliation.ts:63`: `LEAST(transaction_date, COALESCE(reconciled_date, transaction_date))`), and the account list's last-reconciled date (`accounts/accounts.service.ts:606`) and the statement cycle (`accounts/statement-cycle.service.ts:124`) read a day early.

**Where:** `backend/src/transactions/transaction-reconciliation.service.ts:167` vs `172`; `backend/src/common/date-utils.ts:55-60`, `124-135`.

**Steps:**
1. Run the backend with `TZ` unset (UTC) and set the user's timezone to Asia/Tokyo.
2. At 07:30 Tokyo time, reconcile a transaction dated today.
3. Open the account's reconciliation panel.
4. *Expected:* reconciled through today.
   *Actual:* reconciled through yesterday; the stored `reconciled_date` is yesterday's date.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `formatDateYMDLocal`, `todayInTimezone`, `todayYMD` and `isTransactionInFuture` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`TZ=UTC node probe_reconciled_date.js`):
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

**Related:** the same server-day form is used for "today" in `net-worth/net-worth.service.ts:2964`, `securities/holdings.service.ts:476` and `securities/portfolio-calculation.service.ts:790`.

**Possible fix:** `fields.reconciledDate = todayYMD()`. A unit test that sets the request timezone to Asia/Tokyo, fixes the clock at 22:30 UTC, reconciles a row dated the user's today and asserts `reconciledDate` equals that date would catch it.

---

## Draft 3 (MZ-L03)

**Title:** [Bug] Undo and import recompute the balance by the database's day, so it includes or drops a day's transactions for a few hours

**Version:** `main` at `93f4e68`.

**Summary:** `AccountsService.recalculateCurrentBalance` bounds the ledger with `t.transaction_date <= $2` where `$2 = todayYMD()`, the user's timezone day (`backend/src/accounts/accounts.service.ts:1739-1787`, `1751`). Two other absolute recomputes copy the query but bound it with Postgres `CURRENT_DATE`, the database session's day (UTC in the shipped containers): the undo path `ActionHistoryService.recalculateBalance` (`backend/src/action-history/action-history.service.ts:2111`; its comment at `2106` says "Use the same recalculation logic as AccountsService") and the import post-processing recompute (`backend/src/import/import-post-processing.service.ts:81`). Every delta path (create, edit, delete, void) decides "future-dated" by the user's day, so for the hours in which the two days differ the recompute writes a total the delta paths disagree with.

**Result:** a user in America/Toronto with a transaction dated tomorrow sees it excluded from the balance on entry (user's day), included after an undo or an import run between 19:00 and midnight (UTC day), and the figure stays until the next user-day recompute; a user east of UTC in the morning sees today's rows dropped instead.

**Where:** `backend/src/action-history/action-history.service.ts:2106-2122`; `backend/src/import/import-post-processing.service.ts:74-85`; versus `backend/src/accounts/accounts.service.ts:1751`.

**Steps:**
1. Backend with `TZ` unset (UTC); user timezone America/Toronto; at 21:00 Toronto time.
2. In a chequing account, enter a transaction dated tomorrow for -100.00. Balance unchanged (correct: future-dated).
3. Delete any other transaction in the account, then Undo it from History.
4. *Expected:* balance back to what it was before the delete.
   *Actual:* balance is 100.00 lower: the undo's recompute counted tomorrow's row because `CURRENT_DATE` is already tomorrow in UTC. Editing any amount afterwards keeps the wrong total (the delta is applied to it).

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** `net-worth/net-worth.service.ts:2849`, `2937` and `securities/portfolio-calculation.service.ts:681`, `2586` bound monthly sums and holdings by `CURRENT_DATE` too, so the net-worth and portfolio figures can disagree with the account balance for the same hours.

**Possible fix:** pass the user's day as a parameter to both recomputes (the import runs under the importing user's context; the undo under the acting user's), or call `recalculateCurrentBalance` itself, as the comment says it does. A test that fixes the clock at 02:00 UTC, sets the request timezone to America/Toronto, creates a row dated the user's tomorrow and runs undo and import post-processing, asserting the balance excludes it, would catch it.

---

## Draft 4 (MZ-L04)

**Title:** [Bug] Reassigning or deleting a category fails for a user with more than about 65,000 transactions

**Version:** `main` at `93f4e68`.

**Summary:** `CategoriesService.reassignTransactions` selects the id of every transaction the user owns (`backend/src/categories/categories.service.ts:721-727`) and binds the whole list into the next statement with `transactionId IN (:...transactionIds)` (`:738`). TypeORM expands that into one bind parameter per id, and the PostgreSQL wire protocol carries the parameter count in 16 bits, so the statement fails once the user has 65,535 or more transactions. The scheduled-split count and update do the same with schedule ids (`:674-690`, `:749-766`), at a far higher threshold. The list exists only to scope the splits to the user's transactions, which the `transactions` join already does.

**Result:** for a long Microsoft Money or Quicken history (the import this app is built for), "reassign transactions" for a category errors out, and because `remove` requires a zero count, the category can be neither emptied nor deleted. The message is a database error, not a domain one.

**Where:** `backend/src/categories/categories.service.ts:721-741`; `674-690`, `749-766`.

**Steps:**
1. Import a history of 70,000 transactions (any account mix).
2. Categories, pick any category, Reassign transactions to another category.
3. *Expected:* the rows move.
   *Actual:* the request fails with a database error (bind parameter count), and the category cannot be deleted afterwards either.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Possible fix:** replace the id list with a subquery or join on `transaction.userId` (`UPDATE transaction_splits SET category_id = ... FROM transactions t WHERE t.id = split.transaction_id AND t.user_id = $1 AND split.category_id = $2`), and the same for scheduled splits. A test that seeds 66,000 transactions for one user and reassigns a category would catch it; a lighter guard test could forbid `IN (:...` fed by a `getMany()` over all of a user's rows.

---

## Not filing

- **MZ-L05, payee delete has no referencer check (stuck).** `PayeesService.remove` (`payees.service.ts:1280-1308`) deletes without counting; `transactions.payee_id` and `scheduled_transactions.payee_id` have no `ON DELETE` action (`schema.sql:385`, `1084`), so the database refuses and the HTTP filter turns code 23503 into a generic 400 "Referenced record does not exist or cannot be removed" (`http-error-body.ts:125`). Nothing is lost; the user is left without a count or a pointer to Merge, on the REST, AI batch (`ai-actions.service.ts:716-718`) and MCP (`payees.tool.ts:604`, `656`, `750`) doors alike. §4 keeps `stuck` in the ledger.
- **MZ-L06, category delete count-then-delete race (wrong-result).** Same door as Draft 1; carried in its *Related* line rather than filed twice.
- **MZ-L07, import moves the balance for VOID and future rows (process).** `import-regular-processor.service.ts:154` adds every row's amount before its status matters; the post-import recompute (`import-post-processing.service.ts:44-112`) corrects it in the normal case and only logs when it fails. The repo's own rule ("VOID means no balance moved, on every path that writes one") is broken in form, not, in the usual run, in effect. Ledger only.
