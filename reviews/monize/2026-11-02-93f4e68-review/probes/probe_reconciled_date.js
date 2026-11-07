// Probe: the reconciled-date stamp uses the server's calendar day while the
// same write decides "future-dated" by the user's calendar day.
//
// Copied from kenlasko/monize, main at 93f4e68 (AGPL-3.0, licence file beside
// this probe), transcribed TypeScript -> JavaScript with types removed:
//   backend/src/common/date-utils.ts:55-60   formatDateYMDLocal
//   backend/src/common/date-utils.ts:84-103  todayInTimezone
//   backend/src/common/date-utils.ts:124-135 todayYMD
//   backend/src/common/date-utils.ts:164-166 isTransactionInFuture
//   backend/src/transactions/transaction-reconciliation.service.ts:160-182
//     the two "today" decisions of applyStatusTransition, reduced to the two
//     lines that read a clock (reconciledDate stamp, future test).
// Stand-in: getRequestTimezone() (common/request-context.ts:36-38) returns the
// zone given on the command line instead of reading AsyncLocalStorage. The
// clock is a fixed instant passed in, so the output is repeatable.
// Standard library only. No network, no files written. Run: TZ=UTC node probe_reconciled_date.js

"use strict";

// --- copied: date-utils.ts:55-60
function formatDateYMDLocal(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

// --- copied: date-utils.ts:84-103
function todayInTimezone(timezone, at = new Date()) {
  try {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: timezone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).formatToParts(at);
    const y = parts.find((p) => p.type === "year")?.value;
    const m = parts.find((p) => p.type === "month")?.value;
    const d = parts.find((p) => p.type === "day")?.value;
    if (!y || !m || !d) return null;
    return `${y}-${m}-${d}`;
  } catch {
    return null;
  }
}

// --- stand-in for request-context.ts:36-38
let requestTimezone;
function getRequestTimezone() {
  return requestTimezone;
}

// --- copied: date-utils.ts:124-135, with `new Date()` replaced by the fixed
// instant `now` so both decisions read the same clock.
function todayYMD(now) {
  const tz = getRequestTimezone();
  if (tz) {
    const inTz = todayInTimezone(tz, now);
    if (inTz) return inTz;
  }
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

// --- copied: date-utils.ts:164-166
function isTransactionInFuture(transactionDate, now) {
  return transactionDate > todayYMD(now);
}

// --- the two clock reads of applyStatusTransition, reduced:
//   line 167: fields.reconciledDate = formatDateYMDLocal(new Date());
//   line 172: if (isTransactionInFuture(locked.transactionDate)) { ... }
function reconcileDecisions(transactionDate, now) {
  const reconciledDate = formatDateYMDLocal(now); // server's day
  const treatedAsFuture = isTransactionInFuture(transactionDate, now); // user's day
  return { reconciledDate, userToday: todayYMD(now), treatedAsFuture };
}

// RECONCILED_THROUGH_SQL (stale-reconciliation.ts:63), in JS, for the readout:
//   LEAST(transaction_date, COALESCE(reconciled_date, transaction_date))
function reconciledThrough(transactionDate, reconciledDate) {
  return [transactionDate, reconciledDate ?? transactionDate].sort()[0];
}

const cases = [
  // A user west of UTC reconciling in the evening: 21:30 Toronto = 02:30Z next day.
  { tz: "America/Toronto", at: "2026-11-03T02:30:00Z", txDate: "2026-11-02" },
  // A user east of UTC reconciling in the morning: 07:30 Tokyo = 22:30Z the day before.
  { tz: "Asia/Tokyo", at: "2026-11-02T22:30:00Z", txDate: "2026-11-03" },
  // Same user, same hour, a row dated the user's today, plain and simple.
  { tz: "Asia/Tokyo", at: "2026-11-02T22:30:00Z", txDate: "2026-11-02" },
];

console.log(`server TZ=${process.env.TZ ?? "(unset)"}  (the backend container's default is UTC)`);
let mismatches = 0;
for (const c of cases) {
  requestTimezone = c.tz;
  const now = new Date(c.at);
  const r = reconcileDecisions(c.txDate, now);
  const through = reconciledThrough(c.txDate, r.reconciledDate);
  const mismatch = r.reconciledDate !== r.userToday;
  if (mismatch) mismatches++;
  console.log(
    `${c.tz.padEnd(16)} at ${c.at}  row dated ${c.txDate}\n` +
      `  user's today      = ${r.userToday}\n` +
      `  reconciledDate    = ${r.reconciledDate}  ${mismatch ? "<-- not the user's day" : ""}\n` +
      `  treated as future = ${r.treatedAsFuture}\n` +
      `  reconciled-through (LEAST) = ${through}`,
  );
}
console.log(`\n${mismatches} of ${cases.length} cases stamp a reconciledDate that is not the user's calendar day.`);
process.exitCode = mismatches > 0 ? 1 : 0;
