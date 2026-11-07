// Probe: what "Twice a Month" (SEMIMONTHLY) does to a schedule that starts on the 1st.
//
// Copied from kenlasko/monize at 93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9:
//   backend/src/common/recurrence.ts lines 48-79 (parseYMD, formatYMD, daysInMonth, addDays),
//   91-103 (addMonthsClamped), 123-166 (calculateNextDueDate), 173-181 (anchorDayOf),
//   183-192 (ensureYMD).
//   backend/src/scheduled-transactions/schedule-cursor.ts lines 70-75: each advance calls
//   calculateNextDueDate(previous, frequency, anchorDayOf(startDate, previous)).
// Transcribed to plain JS; no stand-ins needed (pure functions). Standard library only.
"use strict";
const YMD_PATTERN = /^(\d{4})-(\d{2})-(\d{2})$/;
function parseYMD(ymd) { const m = YMD_PATTERN.exec(ymd); if (!m) throw new Error("bad ymd " + ymd); return { y: Number(m[1]), m: Number(m[2]), d: Number(m[3]) }; }
function formatYMD(y, m, d) { return `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`; }
function daysInMonth(year, month) { return new Date(Date.UTC(year, month, 0)).getUTCDate(); }
function addDays(ymd, days) { const { y, m, d } = parseYMD(ymd); const n = new Date(Date.UTC(y, m - 1, d + days)); return formatYMD(n.getUTCFullYear(), n.getUTCMonth() + 1, n.getUTCDate()); }
function addMonthsClamped(ymd, months, anchorDay) { const { y, m, d: prevDay } = parseYMD(ymd); const d = anchorDay ?? prevDay; const total = y * 12 + (m - 1) + months; const ny = Math.floor(total / 12); const nm = (total % 12) + 1; const nd = Math.min(d, daysInMonth(ny, nm)); return formatYMD(ny, nm, nd); }
function calculateNextDueDate(ymd, frequency, anchorDay) {
  switch (frequency) {
    case "DAILY": return addDays(ymd, 1);
    case "SEMIMONTHLY": { const { y, m, d } = parseYMD(ymd); if (d <= 15) { return formatYMD(y, m, daysInMonth(y, m)); } const total = y * 12 + m; const ny = Math.floor(total / 12); const nm = (total % 12) + 1; return formatYMD(ny, nm, 15); }
    case "MONTHLY": return addMonthsClamped(ymd, 1, anchorDay);
    default: return ymd;
  }
}
function ensureYMD(v) { return typeof v === "string" ? (YMD_PATTERN.test(v) ? v : v.split("T")[0]) : v.toISOString().slice(0, 10); }
function anchorDayOf(startDate, current) { if (!startDate) return undefined; const { d: s } = parseYMD(ensureYMD(startDate)); const { y, m, d } = parseYMD(ensureYMD(current)); return d === Math.min(s, daysInMonth(y, m)) ? s : d; }

function walk(startDate, frequency, steps) {
  const out = [startDate]; let cur = startDate;
  for (let i = 0; i < steps; i++) { cur = calculateNextDueDate(cur, frequency, anchorDayOf(startDate, cur)); out.push(cur); }
  return out;
}
for (const start of ["2026-01-01", "2026-01-16", "2026-01-15", "2026-01-31"]) {
  console.log(`SEMIMONTHLY from ${start}: ${walk(start, "SEMIMONTHLY", 5).join(" -> ")}`);
}
console.log(`MONTHLY from 2026-01-31 (anchor kept): ${walk("2026-01-31", "MONTHLY", 3).join(" -> ")}`);
