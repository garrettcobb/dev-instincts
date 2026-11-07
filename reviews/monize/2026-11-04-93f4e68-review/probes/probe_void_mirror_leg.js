// Probe: a VOID-boundary status change on one transfer leg reaches the mirror leg
// without the strict reconciled lock, and copies the exact new status onto it.
//
// Copied from kenlasko/monize at 93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9:
//   backend/src/transactions/reconciled-lock.util.ts        lines 168-189 (assertReconciledRowsMutable)
//   backend/src/transactions/void-status-transition.util.ts lines 116-146 (applyVoidTransitionToMirrorLeg)
//   backend/src/transactions/transaction-reconciliation.service.ts
//       lines 130-135 (the own-row-only lock check), 157-159 (balanceMoved),
//       165-171 (reconciledDate for a new RECONCILED), 173-199 (balance moves on own leg),
//       201-216 (mirror propagation); updateStatus resolves to `() => ({ status })` (240-242).
//   backend/src/transactions/transaction-transfer.service.ts lines 1606-1616
//       (removeTransfer passes BOTH legs to the lock check) -- for contrast.
// Stand-ins, control flow unchanged: an in-memory row map replaces the EntityManager
// (lockTransactionRow = read by id; m.update = merge fields), a Map replaces the
// accounts table for updateBalance, isReconciledLockEnabled returns the scenario
// preference, isWithinReconciledUndoWindow returns false, isTransactionInFuture
// returns false (both legs dated in the past), lockEmbeddedInvestmentScopes and
// assertVoidTransitionAllowedOnRow are no-ops (plain transfer, no splits, no
// investment leg). Standard library only; no network, no files.
"use strict";

const TransactionStatus = { UNRECONCILED: "UNRECONCILED", CLEARED: "CLEARED", RECONCILED: "RECONCILED", VOID: "VOID" };

function makeWorld(scenario) {
  const rows = new Map(scenario.rows.map((r) => [r.id, { ...r }]));
  const balances = new Map(scenario.balances);
  const m = {
    lockTransactionRow: (id) => (rows.has(id) ? { ...rows.get(id) } : null),
    update: (id, fields) => Object.assign(rows.get(id), fields),
  };
  const accounts = {
    updateBalance: (accountId, amount) => balances.set(accountId, balances.get(accountId) + amount),
    recalculateCurrentBalance: () => { throw new Error("not reached: both legs are past-dated"); },
  };
  return { rows, balances, m, accounts, lockOn: scenario.lockOn };
}

// reconciled-lock.util.ts 168-189, with the two DB reads replaced by stand-ins.
function assertReconciledRowsMutable(world, rows, options = {}) {
  const closed = { undoWindowOpen: false };
  const hasReconciled = rows.some((row) => row?.status === TransactionStatus.RECONCILED);
  if (!hasReconciled) return closed;
  if (!world.lockOn) return closed;                       // isReconciledLockEnabled
  const withinUndoWindow = false;                          // isWithinReconciledUndoWindow
  if (options.undoWindowFor && withinUndoWindow) return { undoWindowOpen: true };
  throw new Error("409 reconciledLockedError: This transaction is reconciled and locked.");
}
function isReconciledUndo(current, next) {
  return current === TransactionStatus.RECONCILED && (next === TransactionStatus.UNRECONCILED || next === TransactionStatus.CLEARED);
}
const isTransactionInFuture = () => false;

// void-status-transition.util.ts 116-146
function applyVoidTransitionToMirrorLeg(world, row, newStatus) {
  if (!row.linkedTransactionId) return [];
  const counterpart = world.m.lockTransactionRow(row.linkedTransactionId);
  if (!counterpart || counterpart.isSplit) return [];
  const isVoid = newStatus === TransactionStatus.VOID;
  const counterpartWasVoid = counterpart.status === TransactionStatus.VOID;
  if (counterpartWasVoid === isVoid) return [];
  world.m.update(counterpart.id, { status: newStatus });
  if (isTransactionInFuture(counterpart.transactionDate)) {
    world.accounts.recalculateCurrentBalance(counterpart.accountId);
  } else {
    world.accounts.updateBalance(counterpart.accountId, isVoid ? -counterpart.amount : counterpart.amount);
  }
  return [counterpart.accountId];
}

// transaction-reconciliation.service.ts applyStatusTransition (72-232) for a plain,
// non-split row.
function applyStatusTransition(world, transactionId, resolve) {
  const locked = world.m.lockTransactionRow(transactionId);
  if (!locked) throw new Error("404");
  const oldStatus = locked.status;
  const { undoWindowOpen } = assertReconciledRowsMutable(world, [locked], { undoWindowFor: transactionId }); // own row only
  const { status, clearReconciledDate } = resolve(oldStatus);
  if (undoWindowOpen && !isReconciledUndo(oldStatus, status)) throw new Error("409");
  const wasVoid = oldStatus === TransactionStatus.VOID;
  const isVoid = status === TransactionStatus.VOID;
  const balanceMoved = wasVoid !== isVoid;
  const fields = { status };
  if (status === TransactionStatus.RECONCILED && oldStatus !== TransactionStatus.RECONCILED) fields.reconciledDate = "2026-11-04";
  else if (clearReconciledDate) fields.reconciledDate = null;
  if (wasVoid && !isVoid) world.accounts.updateBalance(locked.accountId, locked.amount);
  else if (!wasVoid && isVoid) world.accounts.updateBalance(locked.accountId, -locked.amount);
  world.m.update(transactionId, fields);
  const counterpartAccountIds = [];
  if (balanceMoved) counterpartAccountIds.push(...applyVoidTransitionToMirrorLeg(world, locked, status));
  return { balanceMoved, counterpartAccountIds };
}

// transaction-transfer.service.ts 1606-1616: the paired delete passes both legs.
function removeTransferLockCheck(world, ownId, linkedId) {
  const ownLeg = world.m.lockTransactionRow(ownId);
  const linkedLeg = world.m.lockTransactionRow(linkedId);
  assertReconciledRowsMutable(world, [linkedLeg, ownLeg].filter((l) => l !== undefined));
  return "allowed";
}

function show(world, label) {
  const a = world.rows.get("legA"), b = world.rows.get("legB");
  console.log("  " + label);
  console.log("    legA (Chequing): status=" + a.status + " reconciledDate=" + a.reconciledDate);
  console.log("    legB (Savings):  status=" + b.status + " reconciledDate=" + b.reconciledDate);
  console.log("    balances: Chequing=" + world.balances.get("chq").toFixed(2) + " Savings=" + world.balances.get("sav").toFixed(2));
}

// Scenario 1: strict lock ON. A -100 transfer Chequing -> Savings; the Savings leg is
// RECONCILED against a statement. The Chequing leg is voided through the status route.
{
  const world = makeWorld({
    lockOn: true,
    rows: [
      { id: "legA", accountId: "chq", amount: -100, status: "CLEARED", reconciledDate: null, linkedTransactionId: "legB", isSplit: false, transactionDate: "2026-10-01" },
      { id: "legB", accountId: "sav", amount: 100, status: "RECONCILED", reconciledDate: "2026-10-31", linkedTransactionId: "legA", isSplit: false, transactionDate: "2026-10-01" },
    ],
    balances: [["chq", 900], ["sav", 1100]],
  });
  console.log("Scenario 1: strict lock ON, Savings leg RECONCILED; PATCH /transactions/legA/status {status: VOID}");
  show(world, "before");
  let paired;
  try { paired = removeTransferLockCheck(world, "legA", "legB"); } catch (e) { paired = e.message; }
  console.log("    DELETE /transactions/legA/transfer (both legs checked): " + paired);
  try {
    const r = applyStatusTransition(world, "legA", () => ({ status: "VOID" }));
    console.log("    status route result: balanceMoved=" + r.balanceMoved + " counterpartAccounts=" + JSON.stringify(r.counterpartAccountIds) + " (no refusal)");
  } catch (e) { console.log("    status route refused: " + e.message); }
  show(world, "after");
}

// Scenario 2: lock off. Both legs VOID; the Chequing leg is restored straight to
// RECONCILED through the status route (the dedicated reconcile route refuses VOID).
{
  const world = makeWorld({
    lockOn: false,
    rows: [
      { id: "legA", accountId: "chq", amount: -100, status: "VOID", reconciledDate: null, linkedTransactionId: "legB", isSplit: false, transactionDate: "2026-10-01" },
      { id: "legB", accountId: "sav", amount: 100, status: "VOID", reconciledDate: null, linkedTransactionId: "legA", isSplit: false, transactionDate: "2026-10-01" },
    ],
    balances: [["chq", 1000], ["sav", 1000]],
  });
  console.log("");
  console.log("Scenario 2: both legs VOID; PATCH /transactions/legA/status {status: RECONCILED}");
  show(world, "before");
  const r = applyStatusTransition(world, "legA", () => ({ status: "RECONCILED" }));
  console.log("    status route result: balanceMoved=" + r.balanceMoved + " counterpartAccounts=" + JSON.stringify(r.counterpartAccountIds));
  show(world, "after");
}
