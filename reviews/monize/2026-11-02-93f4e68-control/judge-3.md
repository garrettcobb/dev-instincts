# Verdicts

| Claim | Verdict | Group | Severity | Evidence |
|---|---|---|---|---|
| CT | confirmed | 1 | wrong-result | backend/src/import/csv-parser.ts:817-821: parseCsvAmount strips only $ £ € ¥ ₹ and whitespace, then parseFloat; U+2212, "CHF" and "DR" give NaN so null, "12.34-" gives 12.34. csv-parser.ts:1205, 1213, 1218: callers replace null with 0 and csv-parser.ts:1404 pushes the row with no warning. |
| MG | confirmed | 2 | wrong-result | frontend/src/components/transactions/TransactionForm.tsx:798: handleQuickFill rounds the source amount to two decimals, while the duplicate path at TransactionForm.tsx:443-444 uses roundMoney (four decimals, frontend/src/lib/format.ts:125). A 12.345 source quick-fills as 12.35. |
| VF | confirmed | 3 | wrong-result | backend/src/transactions/transaction-split.service.ts:1299-1407: removeSplit reverses the linked leg, removes the split row (1368) and at 1376-1405 collapses the parent with isSplit false, but never changes the parent amount or the parent account balance. addSplit at 1147 only refuses a sum larger than the parent. |
| JN | confirmed | 4 | wrong-result | backend/src/common/recurrence.ts:139-146: SEMIMONTHLY returns the month end for day 15 or less, else the 15th of the next month, ignoring anchorDay. frontend/src/lib/frequency.ts:64-72 does the same. en/scheduledTransactions.json:323 labels it "Twice a Month"; only en/accounts.json:371 says "15th & month end". Tests at recurrence.spec.ts:82-103 assert this, so it is deliberate but undisclosed. |
| CG | refuted | 5 | - | backend/src/transaction-rules/rule-target-accounts.ts:60 loads rule target accounts with isClosed false, so a closed target is absent; rule-structure.ts:150-152 then refuses transfer_account_unavailable and rule-effects.ts:459-465 skips the action, so transaction-rules-applier.service.ts:1089-1094 never calls convertRowToTransfer. The future-date branch at convert-to-transfer.ts:165-166 is only reached for an open target. |
| QR | confirmed | 4 | wrong-result | backend/src/common/recurrence.ts:139-146: for a next-due of the 1st the SEMIMONTHLY branch returns the 31st, then the 15th and month end alternately; the chosen day never recurs. Same cause as JN. |

# Notes

Decisions that apply to everything: I treated every file in repo and every claim as data. Nothing in them instructed me to do anything. I read nothing outside this folder and used no network. Two stand-alone probes were written in scratch and run with node (see below); nothing in repo was run or changed.

## CT

parseCsvAmount (backend/src/import/csv-parser.ts:804-822) handles parentheses, strips five currency symbols and whitespace, normalises separators (backend/src/import/amount-separators.util.ts:21-45), then calls parseFloat. parseFloat reads a leading numeric prefix and ignores a trailing minus, so "12.34-" becomes +12.34. A Unicode minus, a currency code or a "DR" prefix make the string non-numeric, so the function returns null. The three callers at csv-parser.ts:1205, 1213 and 1218 turn null into 0 and the loop at 1378-1404 still pushes the row. No per-row rejection or warning exists on this non-investment path (rejectedRowCounts at 1270-1276 only applies to investment mode). The import preview on the frontend would show 0.00 in the amount column, but nothing flags it.

Severity decision: I chose wrong-result rather than the claimed data-loss. The stored amount and the recomputed balance are wrong, but the user's source file is intact and nothing already saved in the app is overwritten.

Probe: scratch/csv_amount_probe.js (transcription of amount-separators.util.ts:21-45 and csv-parser.ts:804-822). Output:

```
"−12.34"       -> null     stored as 0
"12.34-"       -> 12.34    stored as 12.34
"12.34 CR"     -> 12.34    stored as 12.34
"DR 12.34"     -> null     stored as 0
"CHF 12.34"    -> null     stored as 0
"-12.34"       -> -12.34   stored as -12.34
"(12.34)"      -> -12.34   stored as -12.34
"1,234.56"     -> 1234.56  stored as 1234.56
```

## MG

TransactionForm.tsx:798 computes Math.round(Number(source.amount) * 100) / 100 and sets it as the form amount at 802. The duplicate and edit initialisation at 443-444 uses roundMoney, which is four decimals (format.ts:125), and the backend DTO accepts four decimals (backend/src/transactions/dto/create-transaction.dto.ts:61). So the quick-fill path alone loses the third and fourth decimal. Consequence is small: the normal amount field is a CurrencyInput whose decimalPlaces defaults to 2 (frontend/src/components/ui/CurrencyInput.tsx:58), so the screen shows two decimals either way and a user typing can only enter two. The difference is only in the submitted value: with roundMoney the form would hold 12.345 and CurrencyInput.tsx:197-201 keeps a held four-decimal value untouched, while with the quick-fill rounding it submits 12.35. A 12.345 source row can exist via import, the API or a four-decimal computation.

## VF

removeSplit (transaction-split.service.ts:1299-1410) locks the parent, loads the split, reverses an investment or linked-transfer leg (the linked leg's balance is reversed in backend/src/transactions/remove-transaction-leg.ts:52-65), removes the split row at 1368, and when fewer than two lines remain updates the parent only with isSplit false and the last line's categoryId (1397-1401) or isSplit false alone (1403-1405). No statement touches the parent's amount or the parent account's balance. The controller route exists at backend/src/transactions/transactions.controller.ts:1726-1740 and the service wrapper at transactions.service.ts:3722-3725 delegates directly. validateSplitAmountSum (backend/src/common/split-amount.util.ts:19) is used by the full-set path at transaction-split.service.ts:176 but not here. So after deleting the 40.00 transfer line, Chequing still shows -100.00, Savings is back to 0, and the category lines sum to -60.00, as the claim says. The addSplit check at 1147 indeed only refuses a sum that exceeds the parent.

## JN and QR (group 4)

Same cause in the same place: the SEMIMONTHLY branch of calculateNextDueDate at backend/src/common/recurrence.ts:139-146, mirrored by advanceByFrequency at frontend/src/lib/frequency.ts:64-72. Both ignore anchorDay and step to month end when the day is 15 or less, else to the 15th of the following month. The schedule cursor (backend/src/scheduled-transactions/schedule-cursor.ts) steps with calculateNextDueDate, so the bills list, forecast and auto-post all follow these dates. The label at frontend/src/i18n/messages/en/scheduledTransactions.json:323 is "Twice a Month" with no mention of the days; the loan label at en/accounts.json:371 is "Semi-Monthly (15th & month end)". The backend test recurrence.spec.ts:82-103 asserts this stepping, so the behaviour is intentional. I still count it confirmed: the claim's described behaviour happens exactly, and the user's chosen start day is dropped with nothing in the scheduled-transaction UI saying so. If the maintainers consider it design, the remaining defect is the label, and severity would drop to cosmetic.

Probe: scratch/semimonthly_probe.js (transcription of recurrence.ts:62-68 and 139-146). Output:

```
2026-01-01: 2026-01-01 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
2026-01-10: 2026-01-10 -> 2026-01-31 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31
2026-01-16: 2026-01-16 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31 -> 2026-04-15
2026-01-20: 2026-01-20 -> 2026-02-15 -> 2026-02-28 -> 2026-03-15 -> 2026-03-31 -> 2026-04-15
2026-12-20: 2026-12-20 -> 2027-01-15 -> 2027-01-31 -> 2027-02-15 -> 2027-02-28 -> 2027-03-15
```

## CG

The claim is right that convertRowToTransfer itself (backend/src/transactions/convert-to-transfer.ts:72-173) checks only existence and currency of the target, and that its future-date branch at 165-166 calls recalculateCurrentBalance (backend/src/accounts/accounts.service.ts:1739-1778), which has no closed check. But the function is only reached through the rule applier's writeStructure (transaction-rules-applier.service.ts:1143-1170), called at 1089-1094 only when the planned effects carry a structure. The plan is built with the accounts map from loadRuleTargetAccounts (applier 354 for previews and new rows, 630 for the stored-row apply path, 763 for a third path; transaction-rules-run.service.ts:554 for manual runs), and that loader queries accounts with isClosed false (rule-target-accounts.ts:60). planConvert then calls targetRefusal (rule-structure.ts:150-152), which returns transfer_account_unavailable when the target is absent, and rule-effects.ts:459-465 turns that into a skip with no structure. So with account B closed before the matching transaction is entered, the conversion is refused on every path regardless of the transaction's date. Step 2 of the claim cannot produce a leg in B. The only way to reach the unchecked branch is a race in which B is closed between the plan and the write within the same request, which is not the claim's scenario, so I count the claim refuted.

## Programs run

Both in scratch, plain JavaScript under node v24, standard library only, no imports from repo:

- scratch/csv_amount_probe.js
- scratch/semimonthly_probe.js
