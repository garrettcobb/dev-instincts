# monize: issue drafts, batch 1 (control round `2026-11-02-93f4e68-control`)

All six were posted on 2026-11-05, in their order, as #2025 to #2030, on Garrett's written go for this batch (`testing/FILING.md` §8); the posted bodies, byte for byte, are in `issues-batch-1/`, one file per issue, named by its number. Written 2026-11-05 by the architect, under `testing/CONTROL.md` §15 and FILING §3 to §5, from `verdicts.private.md`, `score.md`, `key.private.json` and the claims in `claims.private.md`.

**Target:** `kenlasko/monize`, `main` at `051655e8f4e71e7e8896734370b22fd370bccdb8` (`051655e`, committed 2026-11-05 16:03 UTC; `gh api --method GET "repos/kenlasko/monize/commits?sha=main&per_page=1" --jq '.[0].sha'`), 122 commits after `93f4e68`, the sha every run and the judge read. `main` is the repo's only branch, so there is no dev branch to re-check (FILING §3).

**The form:** monize has no issue template on `main` (`.github/ISSUE_TEMPLATE` answers 404, and the community profile's `issue_template` is null), so FILING §5's form is used as it stands. `CONTRIBUTING.md` changed after `93f4e68` by one sentence (a pointer to `docs/agent-instructions.md`); neither it nor `SECURITY.md` and `.github/pull_request_template.md`, both unchanged, sets a rule on AI-assisted or AI-generated reports (`reviews/monize/2026-11-02-ai-policy-check.md`).

**The order:** the 19 groups the judge confirmed with a final severity of data-loss, crash or wrong-result, worst first: by the weight of the group's severity (CONTROL §12: data-loss 4, wrong-result 3, crash 3), and between groups of equal weight by the group's first claim in `claims.md`, the order the judge's group numbers follow. A group's severity is the highest final severity among its claims, as §12 weighs a group (the architect's reading, 2026-11-05; Garrett may change it before the batch is filed), so group 8 files as data-loss, KR's final severity, though VF's is wrong-result. Six to a batch (FILING §9). Read by KR's place (the 17th claim) rather than VF's (the 8th), group 8 would come fourth in batch 1, after group 12; the six would be the same.

| Batch | Groups in order, with their claims in `claims.md` order |
|---|---|
| 1 | 8 (VF, KR), 9 (ZD), 10 (TG, XX, LH, JH), 12 (MN, TX), 18 (GG), 21 (SL): data-loss |
| 2 | 1 (VM, ML, XT), 2 (HG), 3 (MV), 4 (ZX), 5 (CT), 6 (MG): wrong-result |
| 3 | 7 (GN, VP, JK): crash; 14 (DR, WV), 15 (FP, LM): wrong-result; 17 (GC): crash; 19 (JN, QR), 20 (WF): wrong-result |
| 4 | 23 (PC): wrong-result |

## The re-check and the duplicate search (FILING §3), 2026-11-05

Every cited file was fetched read-only at both shas (`gh api --method GET "repos/kenlasko/monize/contents/<path>?ref=<sha>" -H "Accept: application/vnd.github.raw"`), each checked against its tree's blob sha (`gh api --method GET "repos/kenlasko/monize/git/trees/<sha>?recursive=1"`), and the cited lines compared. *Unchanged* means the same blob at both shas; *moved*, the same code at new line numbers. No group's mechanism is fixed on `main`, and no group is filed upstream, so all six are drafted and none is held back.

Each search ran in four forms: `gh search issues --repo kenlasko/monize "<words>" --limit 50` and `gh search prs --repo kenlasko/monize "<words>" --limit 50`, both states (their `--state` takes only `open` or `closed`, so it was left off; gh searches the quoted words as a phrase), then `gh issue list` and `gh pr list --repo kenlasko/monize --state all --search "<words>" --limit 50`, which search the words apart (*50* there is the limit). As a cross-check, the titles and bodies of all 1,877 issues and pull requests (`gh api --method GET "repos/kenlasko/monize/issues?state=all&per_page=100" --paginate`) were searched for the function names and the user's words below. Open PR #1883 (accrual accounting, 638 files, conflicted, last updated 2026-11-02) changes seven of the cited files, none of the CSV import's; what it does to each group is said under it.

- **Group 8 (draft 1).** `transaction-split.service.ts` changed elsewhere; `removeLinkedLeg` and `removeSplit` (`93f4e68` lines 1288-1413) are byte for byte `main`'s 1431-1556: moved. `transactions.controller.ts`, `remove-transaction-leg.ts` and `frontend/src/lib/transactions.ts`: unchanged. Searches: "remove split": issues none, PRs #1116, words 50 and 50; "split transfer leg": issues #1937, #1815, #880, #1827, PRs #1940, #1816, #1147, #1828, #882, #1804, #1169, #1822, words 16 and 50; "removeSplit": issues none, PRs #1096, #1202, #515, words none and 3 (the same three). Bodies: `removeSplit` 2 (#1202, #515), `deleteSplit` 4 (#1942, #1816, #1015, #983), `removeLinkedLeg` none. None reports this. Nearest: #1815 (closed, fixed by #1816), the bulk delete of a split-transfer leg, another route. #1883 passes an accrual fingerprint through the route (`transactions.controller.ts`) and leaves `removeSplit` itself alone.
- **Group 9 (draft 2).** `payees.service.ts`, `payee-auto-merge.service.ts` and `payees.controller.ts`: unchanged. `database/schema.sql`: the four foreign keys unchanged, moved (`warranties` 3566 to 3567, `accounts.overpayment_payee_id` 1203 to 1204, `shared_people` 4596 to 4637; `email_receipt_parsers` still 820). Searches: "merge payee": issues #645, PRs #657, #671, #661, #658, #204, words 40 and 50; "mergePayees": issues #823, PRs #824, #204, words 1 and 2 (the same); "warranty payee": issues none, PRs none, words 4 and 9. Bodies: `mergePayees` 5 (#1916, #824, #823, #657, #204), merge wording 5, a warranty beside a payee 5, `overpayment_payee` 1 (#877). None reports links lost in a merge. #1883 changes `mergePayees` and the auto-merge apply, and moves none of the four links.
- **Group 10 (draft 3).** `categories.service.ts`, `budgets.service.ts`, `budget-spending.util.ts`, `payroll-deduction-rule.entity.ts`, the delete dialog `DeleteCategoryDialog.tsx` and the English `categories.json`: unchanged. `database/schema.sql`: the cited foreign keys unchanged, moved one line (`shared_postings` 4722 to 4763), and `main` adds `loan_fees.category_id`, `ON DELETE CASCADE` (`:3676`, from #2001). `loan-mortgage-account.service.ts` changed; its setup refusal moved (251 to 258, 426 to 448). Searches: "delete category": issues #1916, #1831, PRs #1925, #1084, #585, words 27 and 50; "payroll deduction": issues #1886, #1885, #1933, #1917, PRs #1894, #1893, #1884, #1892, #1934, #1924, #1942, words 4 and 7 (the same); "getTransactionCount": none in all four. Bodies: `getTransactionCount` none, payroll beside a category delete none, a budget line's category beside a delete 5 (#1935, #1931, #1825, #1818, #128), the dialog's "safely deleted" none, `loan_fees` 1 (#2001). None reports this. #1883 moves the delete's checks into the deleting transaction and still counts the same four tables.
- **Group 12 (draft 4).** `accounts.service.ts` changed above its line 344 only; the delete path is byte for byte, 18 lines down (`assertAccountEmpty` 1413 to 1431, `delete` 2207 to 2225, the remove 2262 to 2280, the list's `canDelete` 665 to 683): moved. `database/schema.sql`: the three foreign keys unchanged, one line down. `scheduled-transactions.service.ts`: unchanged. The English `accounts.json` changed elsewhere; its lines 89 and 116 are the same. Searches: "delete account": issues #1914, #1640, #279, PRs 24, none on this, words 50 and 50; "scheduled transactions deleted": issues none, PRs none, words 6 and 20; "assertAccountEmpty": issues none, PRs #1816, words none and 1 (#1816). Bodies: `assertAccountEmpty` 1 (#1816), an account delete beside schedules 6 (#1649, #1015, #877, #642, #555, #235). None reports this. Nearest: #555 (merged 2026-05-19) made transfer splits, scheduled ones too, cascade with their target account, for deleting a user; #1815 (fixed by #1816) moved the two counts into the deleting transaction. #1883 adds two lines to `accounts.service.ts`, neither in the delete path.
- **Group 18 (draft 5).** `categories.service.ts`: unchanged; `database/schema.sql:387` and `:430`: unchanged, same lines. Searches: "category delete race": none, none, none, and 11 PRs by words; "category transaction concurrent delete": none, none, then 3 and 10 by words. Bodies: a category delete beside race or lock wording none, `categories.service.ts` cited near these lines none, the method's `M23` note 3 (#1822, #1821, #128). None reports this. Nearest: #1815 (fixed by #1816), the same gap for deleting an account. #1883 rewrites this method: inside the deleting transaction it locks the category row (`SELECT ... FOR UPDATE`, in its new `backend/src/categories/category-mutation.ts`) before the count, which would close this if it merged in that form.
- **Group 21 (draft 6).** `csv-parser.ts` and `import.service.ts`, and the front end's `CsvColumnMappingStep.tsx`, `lib/import.ts` and `useImportWizard.ts`: unchanged. Searches: "csv date": issues none, PRs none, words 27 and 40; "parseCsvDate": none in all four; "DD/MM/YYYY": issues 13, PRs 30, the same by words. Bodies: `parseCsvDate`, `parseDateCustom` or `csv-parser.ts` 6 (#1451, #1194, #1088, #438, #229, #202), a CSV date beside skip or drop wording 4 (#1794, #1631, #1528, #1139), "DD/MM/YYYY" 5. None reports dropped rows. Nearest: #1794, which lists the rows the OFX import skips. #1883 doesn't touch the CSV import.

---

## Draft 1 (group 8)

**Title:** [Bug] Removing a split line through the API deletes the remaining transfer leg in the other account and leaves the parent at its full amount

**Version:** `main` at `051655e`. Read at `93f4e68`; the method below is unchanged between the two, 143 lines lower on `main`, and the line numbers are `main`'s.

**Summary:** `TransactionSplitService.removeSplit` (`backend/src/transactions/transaction-split.service.ts:1442-1555`, behind `DELETE /api/v1/transactions/:id/splits/:splitId`, `transactions.controller.ts:1726-1739`) deletes the chosen line, and that line's transfer leg if it has one (`:1500-1509`), but nothing in it changes the parent's `amount` or the parent account's balance. When one line is left it collapses the parent into a plain transaction: if that last line is a transfer, it first deletes the last line's counterpart in the other account and reverses that account's balance (`:1529-1538`, through `removeLockedTransactionLeg`, `remove-transaction-leg.ts:46-67`), then takes the category from that line, which a transfer line doesn't have (`:1540-1544`).

**Result:** removing the category line of a two-line split whose other line is a transfer deletes money recorded as arriving in another account, though the request never named that line; the parent stays at its full amount with no category and no transfer. Every removal leaves the parent's amount, and its account's balance, at the old total: with two or more lines left, they no longer add up to it; with one left, the parent takes that line's category at the full amount.

**Where:** `backend/src/transactions/transaction-split.service.ts:1442-1555` (`:1500-1509`, `:1511`, `:1519-1551`), `:1289`; `backend/src/transactions/transactions.controller.ts:1726-1739`; `backend/src/transactions/remove-transaction-leg.ts:46-67`.

**Steps:**
1. In Chequing, create a -100.00 split transaction: -60.00 to Groceries and -40.00 as a transfer to Savings. Savings shows the +40.00 leg.
2. Remove the Groceries line through the API: `DELETE /api/v1/transactions/<parent id>/splits/<Groceries line id>`. The web app's split editor sends the whole set of lines instead, so this route is reached by API clients (a personal access token, a script); the front end's client library wraps it as `deleteSplit` (`frontend/src/lib/transactions.ts:456-460`).
3. Open the transaction, and the Savings register.

**Expected:** the request is refused, or the parent becomes a plain -40.00 transfer to Savings, its amount taken from the line that is left.

**Actual:** the +40.00 leg in Savings is deleted and Savings' balance drops by 40.00. The parent is a plain -100.00 transaction in Chequing with no category and no transfer, so Chequing still shows 100.00 out and no account shows it arriving.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** removing the transfer line instead (step 2 with the -40.00 line) deletes the Savings leg, as asked, then collapses the parent into a plain -100.00 Groceries transaction: 40.00 has left Chequing and arrived nowhere, and Groceries reads 40.00 too high. `addSplit` refuses only lines that add up to more than the parent (`transaction-split.service.ts:1289`), not to less. #1815, fixed by #1816, dealt with the bulk delete of a split-transfer leg; this is the single split-delete route.

**Possible fix:** after removing a line, set the parent's amount from the remaining lines and move its account's balance by the difference, or refuse a removal that would change the parent's amount; when the last line left is a transfer, keep its leg and make the parent that transfer. A test with the -100.00 split above: removing the Groceries line keeps the Savings leg and leaves a -40.00 transfer (or is refused); removing the transfer line leaves a -60.00 Groceries transaction and Chequing 40.00 higher (or is refused).

*Outside the issue:* Arm: B. Claims KR (arm B run 1, finding 4; final data-loss) and VF (arm B run 2, finding 6; final wrong-result), both arm B's. The steps are KR's, the path that loses data, written with VF's account names and amounts; VF's own case is the first sentence of *Related*.

---

## Draft 2 (group 9)

**Title:** [Bug] Merging two payees leaves the merged payee's warranties, email receipt parsers and loan overpayment links with no payee

**Version:** `main` at `051655e`. Read at `93f4e68`; `payees.service.ts` is unchanged between the two, the foreign keys below are unchanged, three of them at new line numbers on `main`, and the line numbers are `main`'s.

**Summary:** `PayeesService.mergePayees` (`backend/src/payees/payees.service.ts:1953-2036`, the Merge dialog's `POST /api/v1/payees/merge`) moves the source payee's transactions, scheduled transactions and aliases to the target (`:1975-1979`, `:1983-1987`, `:2021-2025`), then deletes the source payee (`:2028`). Four more tables point at payees with `ON DELETE SET NULL`, and the merge doesn't move them, so the delete clears them: `warranties.payee_id` (`database/schema.sql:3567`), `email_receipt_parsers.payee_id` (`:820`), `accounts.overpayment_payee_id` (`:1204`) and `shared_people.payee_id` (`:4637`).

**Result:** after a merge, a warranty recorded against the merged payee has no payee; an email receipt parser bound to it loses its payee; a loan's overpayment payee and a shared-expense person's payee link are cleared. Nothing in the merge says so.

**Where:** `backend/src/payees/payees.service.ts:1953-2036`; `database/schema.sql:3567`, `:820`, `:1204`, `:4637`.

**Steps:**
1. Create payees "Costco" and "Costco Wholesale"; record a warranty under "Costco Wholesale".
2. Merge "Costco Wholesale" into "Costco".
3. Open the warranty.

**Expected:** the warranty, and any receipt parser, loan overpayment payee or shared-expense person, now points at "Costco".

**Actual:** the warranty has no payee.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** the Auto-Merge tool's apply (`backend/src/payees/payee-auto-merge.service.ts:789-811`) moves the same three tables and deletes each source payee the same way.

**Possible fix:** in both merges, move every table whose foreign key points at payees to the target before the source is deleted. A test that gives the source payee a warranty, a receipt parser, a loan overpayment link and a shared-expense person, merges it, and expects each to point at the target, through both the Merge dialog and Auto-Merge.

*Outside the issue:* Arm: B. Claim ZD (arm B run 1, finding 3), the group's only claim; its steps. The *Related* line, the Auto-Merge apply with the same cause (FILING §4's sibling path), is the architect's reading at the re-check, not part of the claim.

---

## Draft 3 (group 10)

**Title:** [Bug] Deleting a category the dialog calls unused deletes its payroll deduction rules and leaves its budget lines with no category

**Version:** `main` at `051655e`. Read at `93f4e68`; `categories.service.ts` is unchanged between the two, the foreign keys below are unchanged and a line or more lower on `main`, `main` adds one more cascading table (`loan_fees`), and the line numbers are `main`'s.

**Summary:** Past its checks for system categories and subcategories, `CategoriesService.remove` refuses a delete only when `getTransactionCount` is non-zero (`backend/src/categories/categories.service.ts:606-616`), and that count covers transactions, transaction splits, scheduled transactions and scheduled splits (`:654-698`); the delete dialog shows the same count (`frontend/src/components/categories/DeleteCategoryDialog.tsx:47`, `:131`). Other tables point at categories without being counted, so the database decides for them: `payroll_deduction_rules.category_id` and `loan_fees.category_id` are `ON DELETE CASCADE` (`database/schema.sql:3641`, `:3676`); `budget_categories.category_id` and `budget_period_categories.category_id` are `ON DELETE SET NULL` (`:2425`, `:2473`), and so are the loan category columns of `accounts` (`:1198`, `:1200`, `:1202`, `:1208`), `scheduled_transaction_overrides.category_id` (`:1223`) and `shared_postings.category_id` (`:4763`).

**Result:** a category with no transactions but with a payroll deduction rule and a budget line is deleted after the dialog says it isn't used. The payroll deduction rule, its yearly maximum and reset date with it, is gone. The budget line keeps its amount with no category: it reads "Uncategorized" (`backend/src/budgets/budget-spending.util.ts:410-421`), and no spending is counted against it again (`:239-241`). A loan or mortgage whose interest category it was is left with none, which its own setup refuses (`backend/src/accounts/loan-mortgage-account.service.ts:258`, `:448`), and a mortgage fee in the category is deleted with it.

**Where:** `backend/src/categories/categories.service.ts:579-652`, `:654-698`; `frontend/src/components/categories/DeleteCategoryDialog.tsx:47`, `:131`; `database/schema.sql:3641`, `:3676`, `:2425`, `:2473`, `:1198-1208`, `:1223`, `:4763`.

**Steps:**
1. Create a category "CPP" with no transactions, add it to a budget with a monthly amount, and create a payroll deduction rule for it on a paycheque schedule.
2. Open the category's delete dialog.
3. Confirm.

**Expected:** the dialog counts the budget line and the payroll rule among the category's uses, or the delete is refused with a count of what still uses the category, as it is for transactions.

**Actual:** the dialog says "This category is not used. It can be safely deleted." After the delete the payroll deduction rule is gone and the budget line reads "Uncategorized".

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** `reassignTransactions` (`categories.service.ts:700-775`), the step the refusal message points to, moves transactions, splits and scheduled items only, so the rule and the budget line can't be moved off the category before a delete either.

**Possible fix:** count every table whose foreign key points at categories (payroll rules, budget lines, loan links, occurrence overrides, shared postings, loan fees) beside `getTransactionCount`, and refuse with the breakdown or show it in the dialog; or move them in `reassignTransactions`. A test: a category used only by a payroll rule, then one used only by a budget line, is refused (or reported in the dialog's count).

*Outside the issue:* Arm: A+B. Claims TG (arm B run 2, finding 4), XX (arm A run 2, finding 3), LH (arm B run 1, finding 2) and JH (arm A run 1, finding 1), all final data-loss. Both arms have claims here, so the clearer steps were taken: LH's (arm B run 1), the only ones that show what the delete dialog tells the user, with JH's ending (arm A run 1: the rule gone, the line reading "Uncategorized"). LH's sentence that the budgeted amount leaves the budget's totals is left out: TG says it stays, and neither judge run settled it. The other tables in *Summary* are JH's; `loan_fees` is XX's remark about a later `main`, checked on `051655e`.

---

## Draft 4 (group 12)

**Title:** [Bug] Deleting an account with no transactions silently deletes its scheduled bills and the transfer lines of other schedules that point at it

**Version:** `main` at `051655e`. Read at `93f4e68`; the delete path below is unchanged between the two, 18 lines lower on `main`, the foreign keys are unchanged and a line lower, and the line numbers are `main`'s.

**Summary:** `AccountsService.delete` (`backend/src/accounts/accounts.service.ts:2225-2292`) refuses only through `assertAccountEmpty` (`:1431-1462`), which counts transactions and investment transactions, and the account list's `canDelete` uses the same two counts (`:683-685`). The schema then takes the rest with the account: `scheduled_transactions.account_id` is `ON DELETE CASCADE` (`database/schema.sql:1083`), so every schedule paid from the account goes, with its splits, overrides and postings; `scheduled_transaction_splits.transfer_account_id` is `ON DELETE CASCADE` (`:1159`), so another schedule's split line that transfers into the account goes; `scheduled_transactions.transfer_account_id` is `ON DELETE SET NULL` (`:1121`), and posting makes a transfer only when that column is set (`backend/src/scheduled-transactions/scheduled-transactions.service.ts:3424-3428`).

**Result:** the delete removes every scheduled bill, deposit and loan payment on the account, and drops lines from other schedules, whose lines then no longer add up to their amounts. A scheduled transfer into the account is kept and from then on posts as a plain transaction with no category. None of this is said before the delete, and the history entry holds only the account row (`accounts.service.ts:2283-2291`), so undo can't bring the schedules back.

**Where:** `backend/src/accounts/accounts.service.ts:1431-1462`, `:2225-2292`, `:683-685`; `database/schema.sql:1083`, `:1121`, `:1159`; `backend/src/scheduled-transactions/scheduled-transactions.service.ts:3424-3428`.

**Steps:**
1. Create a chequing account B with no transactions, and a monthly scheduled bill "Rent" paid from B. Give an existing schedule on account A a split line that transfers 200.00 to B.
2. On the Accounts page, B can be deleted; its button's tooltip reads "Permanently delete account (no transactions)". Delete B and confirm the dialog, which says only that the action can't be undone.
3. Open Bills & Deposits, then the schedule on A.

**Expected:** the delete is refused, or the dialog says the schedules will go, or the schedules survive without the account.

**Actual:** "Rent" is gone, and A's schedule has lost its 200.00 line, so its lines no longer add up to its amount.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** #555 made transfer splits, scheduled ones included, cascade with their target account, so that deleting a user no longer failed a check constraint; when the user deletes one account as empty, the guard neither counts these schedules nor says they will go. #1815, fixed by #1816, moved the same two counts into the deleting transaction.

**Possible fix:** count, in `assertAccountEmpty` and `canDelete`, the schedules paid from the account, the scheduled transfers into it and the schedule lines that transfer into it, and refuse with the counts ("close the account instead", as for transactions), or list them in the dialog. A test: an account with no transactions but one schedule, and another schedule's transfer line into it, can't be deleted.

*Outside the issue:* Arm: B. Claims MN (arm B run 1, finding 1) and TX (arm B run 2, finding 1), both final data-loss and both arm B's. The steps are TX's, which name the accounts and show another schedule losing its line, with MN's quote of the delete button's tooltip; MN's undo point closes *Result*.

---

## Draft 5 (group 18)

**Title:** [Bug] A transaction saved while its category is being deleted loses its category, and the delete isn't refused

**Version:** `main` at `051655e`. Read at `93f4e68`; `categories.service.ts` is unchanged between the two, the schema lines below are the same, and the line numbers are `main`'s.

**Summary:** `CategoriesService.remove` counts the category's uses in one database transaction (`getTransactionCount`, called at `backend/src/categories/categories.service.ts:607`, opens its own at `:660`) and deletes the category in another (`:632-641`), with no lock on the category and no second count. `transactions.category_id` and `transaction_splits.category_id` are `ON DELETE SET NULL` (`database/schema.sql:387`, `:430`). A transaction or split saved between the two keeps its row and loses its category, and the delete that should have been refused goes through.

**Result:** a transaction saved in that window, by the user in another tab, an import, a bank sync or a scheduled post, ends up uncategorized with nothing to say why, and the category is gone.

**Where:** `backend/src/categories/categories.service.ts:606-616`, `:632-641`, `:654-698`; `database/schema.sql:387`, `:430`.

**Steps:**
1. Have a category "Gym" with no transactions.
2. Delete "Gym" while another request saves a transaction in "Gym" (another tab, an import or a bank sync), so that the save commits after the delete's count and before the delete itself.
3. Open the saved transaction.

**Expected:** the delete is refused, as it is when the transaction was saved first, or the save fails because the category is gone.

**Actual:** the delete succeeds, and the saved transaction has no category.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code. Not reproduced in the running app, so the steps above are what the code says will happen.

**Related:** #1815, fixed by #1816, closed the same gap for deleting an account: there the deleting transaction locks the account and counts again (`backend/src/accounts/accounts.service.ts:2259-2268`). Open PR #1883 rewrites this method and locks the category row inside the deleting transaction before the count, which would close this if it merges in that form.

**Possible fix:** as for accounts: inside the deleting transaction, lock the category row, run the count there and refuse if it isn't zero. A test on two connections, like `backend/test/integration/account-delete-race.integration.spec.ts`: one saves a transaction in the category while the other deletes it; expect the refusal.

*Outside the issue:* Arm: A. Claim GG (arm A run 1, finding 6; final data-loss, where the claim said wrong-result), the group's only claim. The claim has no steps ("Not run (needs two concurrent requests against PostgreSQL)"), so the numbered steps are the architect's, written from the lines the claim cites. Arm A run 1 carried this in its first draft's *Related* line; the judge made it a group of its own, so it is an issue of its own here.

---

## Draft 6 (group 21)

**Title:** [Bug] CSV import silently drops every row whose date it cannot read

**Version:** `main` at `051655e`. Read at `93f4e68`; every file below is the same at the two, and the line numbers are `main`'s.

**Summary:** `parseCsv` skips a row whose date `parseCsvDate` can't read with a bare `continue` and records nothing (`backend/src/import/csv-parser.ts:1193-1197`), and its result carries no count of rows read against rows kept (`:1410-1433`), so neither the preview nor the result can show the loss. `parseCsvDate` (`:749-796`) returns null for a day above 12 under MM/DD/YYYY, and for any date with a month name, since a custom pattern knows only `YYYY`, `YY`, `MM` and `DD` (`:666-722`). The mapping step guesses the date format from the first five rows only (`frontend/src/components/import/CsvColumnMappingStep.tsx:80-87`, `frontend/src/lib/import.ts:31-71`, `backend/src/import/csv-parser.ts:1117`) and picks MM/DD/YYYY, which is also the default (`frontend/src/hooks/useImportWizard.ts:80`), when those five can be read either way.

**Result:** rows of the bank statement never reach the register, with no count and no message. With the day and month order wrong, the rows with a day above 12 are dropped and the rest are imported with day and month swapped, so the file looks imported. `validateAndFormat` (`csv-parser.ts:637-649`) also lets 30 February and 31 April through; those rows fail at the database and are reported, which the dropped rows are not.

**Where:** `backend/src/import/csv-parser.ts:1193-1197`, `:749-796`, `:666-722`, `:637-649`, `:1410-1433`; `frontend/src/components/import/CsvColumnMappingStep.tsx:80-87`.

**Steps:**
1. Take a statement from a bank that writes dates as DD/MM/YYYY, whose first five rows fall on the 1st to the 12th of the month (a March statement starting 02/03/2026, say), and import it as CSV; the date format stays MM/DD/YYYY.
2. Map the columns and run the import.
3. Compare the register with the statement.

**Expected:** each unreadable date reported by row (the import result already has `skipped` and `skippedRows` for other reasons), or the file refused.

**Actual:** every row dated the 13th or later is missing, with no count or message, and the rest are on swapped dates: 02/03/2026, 2 March, is imported as 3 February.

**How this was found:** an AI-assisted review of the source, confirmed by reading the code and running a small standalone program that copies the `parseCsvDate` logic. Not reproduced in the running app, so the steps above are what the code says will happen.

**Probe output** (`csv_date_probe.js`, plain Node, standard library only; it copies `parseCsvDate`, `parseDateCustom`, `validateAndFormat`, `stripTime` and `resolveYear`):
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

**Related:** the OFX import lists each row it skips with its date and amount (#1794); the CSV loop keeps no such record.

**Possible fix:** count the rows whose date doesn't parse and return them, with their row number and raw date, among the result's skipped rows, and show the count in the preview; refuse impossible calendar dates when parsing. A test: a CSV with a 13/03/2026 row under MM/DD/YYYY gives one skipped row with its reason, not a silent drop.

*Outside the issue:* Arm: B. Claim SL (arm B run 2, finding 2), the group's only claim; its probe output, as arm B run 2's report gives it (both judge runs reproduced it with programs of their own). The steps are SL's, narrowed by what the re-check read on `main`: the mapping step guesses the format from the first five rows (`CsvColumnMappingStep.tsx:80-87`), which neither the claim nor the judge mentions, so the step 1 file is one whose first five rows can be read either way. The claim's month-name case is in *Summary*.

---

## Not in this batch

- **Batches 2 to 4,** the 13 confirmed wrong-result and crash groups, in the order of the table above; each waits for its own drafts and Garrett's go.
- **Not filed (FILING §4):** group 11 (PN, GM, LP), stuck, and group 16 (VL), process, stay in the ledger. Group 22 (CG) was refuted by the judge's final verdict, so it isn't filed.
