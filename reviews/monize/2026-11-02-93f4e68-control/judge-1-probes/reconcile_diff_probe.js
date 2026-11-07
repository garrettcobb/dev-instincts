// Transcribed from repo at 93f4e68, frontend/src/app/reconcile/page.tsx:381-392
//   calculatedDifference rounding and the handleFinishReconciliation guard.
function calculatedDifference(statementBalance, reconciledBalance, selectedSum) {
  return Math.round(((statementBalance ?? 0) - (reconciledBalance + selectedSum)) * 100) / 100;
}
function finishAllowed(diff) { return !(Math.abs(diff) > 0.01); }
for (const stmt of [1000.00, 1000.01, 999.99, 1000.02]) {
  const diff = calculatedDifference(stmt, 1000.00, 0);
  console.log(JSON.stringify({ statementBalance: stmt, calculatedDifference: diff, finishAllowed: finishAllowed(diff) }));
}
