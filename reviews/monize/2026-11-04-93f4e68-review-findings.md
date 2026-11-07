# Review of kenlasko/monize at 93f4e68

# Findings

## 1: Voiding one leg of a transfer voids its reconciled counterpart in the other account while "Lock reconciled transactions" is on
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

## 2: Restoring a voided transfer leg to Reconciled marks the other account's leg Reconciled too, with no reconciled date
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

## 3: Deleting a category deletes the payroll deduction rules that use it and leaves budget lines with no category
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

## 4: Reassigning a category fails with a database error once the user has more than 65,535 transactions
Severity: crash
Where: backend/src/categories/categories.service.ts:723, backend/src/categories/categories.service.ts:738, backend/src/categories/categories.service.ts:751, at 93f4e68
What the user loses: with a long history (the README's own case is thirty years of Money data) they cannot reassign a category's transactions, and so cannot delete a category the guard says to reassign first. The method selects every transaction id the user owns and binds the whole list as one IN (...) parameter per id; the PostgreSQL protocol carries the parameter count in 16 bits, so a list over 65,535 ids cannot be bound and the request fails. The same shape, with the smaller scheduled-transaction list, is in getTransactionCount (:677-690).
Steps:
1. A user with more than 65,535 transactions.
2. Categories page: reassign any category's transactions to another (POST /categories/<id>/reassign).
Expected: the rows move and a count is returned.
Actual: 500; nothing moves (one transaction, rolled back).
Evidence: reading

## 5: "Twice a Month" steps to the 15th and month-end whatever the start date, so a bill on the 1st and 16th gets the wrong due dates
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

# Not reached

Read in the two hours: transaction update and delete, transfer create and delete, the VOID mirror and split side-effect helpers, status transitions and bulk reconcile, the bulk status balance path and the start of bulk delete, account delete and the balance helpers, category delete and reassign, scheduled skip and the cursor, the recurrence helpers, the import transfer dedupe, the amount-separator and OFX parsers, the money rounding helpers. Not reached: scheduled post and auto-post, the loan and mortgage paths, the MNY and CSV importers' write paths, bank sync, investments and holdings, backup and restore, the joint and delegated ledgers, the AI and MCP tool paths beyond locating the status door, the frontend beyond the status cycle and the frequency helper, and all of auth, 2FA and OIDC.

# Text in the repo addressed to an agent

Data only; none of it was followed.
- AGENTS.md:5: "This is the canonical instruction file for every coding agent; CLAUDE.md imports it and adds only what Claude Code specifically should do."
- AGENTS.md:11: "Before working in a layer, read its CLAUDE.md, then only the rows of its 'Read when the work touches it' table that match the task."
- AGENTS.md:183: "While working: change what was asked and the tests that prove it; report an unrelated defect instead of fixing it in passing. ... When a guard fails, stop and report what it names rather than routing around it."
- CLAUDE.md (12 lines) imports AGENTS.md; backend/CLAUDE.md, frontend/CLAUDE.md, database/CLAUDE.md, e2e/CLAUDE.md and backend/src/mcp/CLAUDE.md are per-layer indexes for the same agents; .claude/commands/audit.md is empty.
- .github/pull_request_template.md:20: "Run an AI code review before opening this PR and fix what it finds (Claude Code: /code-review, Codex: /review)."
- CONTRIBUTING.md:37: "AGENTS.md is the canonical instruction file for any coding agent".
