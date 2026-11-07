// Transcribed from repo at 93f4e68:
//   backend/src/common/recurrence.ts:62-68   formatYMD, daysInMonth
//   backend/src/common/recurrence.ts:139-146 SEMIMONTHLY branch of calculateNextDueDate
// parseYMD stand-in (same shape as recurrence.ts's, control flow unchanged).
function parseYMD(s) { const [y, m, d] = s.split("-").map(Number); return { y, m, d }; }
function formatYMD(y, m, d) { return `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`; }
function daysInMonth(year, month) { return new Date(Date.UTC(year, month, 0)).getUTCDate(); }
function semimonthly(ymd) {
  const { y, m, d } = parseYMD(ymd);
  if (d <= 15) return formatYMD(y, m, daysInMonth(y, m));
  const total = y * 12 + m;
  const ny = Math.floor(total / 12);
  const nm = (total % 12) + 1;
  return formatYMD(ny, nm, 15);
}
for (const start of ["2026-01-01", "2026-01-10", "2026-01-16", "2026-01-20", "2026-12-20"]) {
  let cur = start; const seq = [cur];
  for (let i = 0; i < 5; i++) { cur = semimonthly(cur); seq.push(cur); }
  console.log(start + ":", seq.join(" -> "));
}
