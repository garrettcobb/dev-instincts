// Probe: the reconcile screen lets a statement that is one cent off be finished.
// Transcribed from repo/frontend/src/app/reconcile/page.tsx lines 381-390:
//   calculatedDifference = Math.round(((statementBalance ?? 0) - newBalance) * 100) / 100
//   if (Math.abs(calculatedDifference) > 0.01) -> refuse ("differenceRequired")
function canFinish(statementBalance, reconciledBalance, selectedSum) {
  const newBalance = reconciledBalance + selectedSum;
  const calculatedDifference =
    Math.round(((statementBalance ?? 0) - newBalance) * 100) / 100;
  const refused = Math.abs(calculatedDifference) > 0.01;
  return { calculatedDifference, finishAllowed: !refused };
}
console.log(JSON.stringify(canFinish(1000.0, 900.0, 100.0)));   // exact
console.log(JSON.stringify(canFinish(1000.01, 900.0, 100.0)));  // one cent off
console.log(JSON.stringify(canFinish(999.99, 900.0, 100.0)));   // one cent off
console.log(JSON.stringify(canFinish(1000.02, 900.0, 100.0)));  // two cents off
