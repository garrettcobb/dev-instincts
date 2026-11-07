// Transcribed from repo at 93f4e68, backend/src/common/recurrence.ts:
//   33-54 parseYMD, formatYMD, daysInMonth; 123-150 calculateNextDueDate (SEMIMONTHLY branch only)
const YMD_PATTERN = /^(\d{4})-(\d{2})-(\d{2})$/;
function parseYMD(ymd) { const m = YMD_PATTERN.exec(ymd); if (!m) throw new Error("bad " + ymd); return { y: +m[1], m: +m[2], d: +m[3] }; }
function formatYMD(y, m, d) { return `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`; }
function daysInMonth(year, month) { return new Date(Date.UTC(year, month, 0)).getUTCDate(); }
function nextSemimonthly(ymd) {
  const { y, m, d } = parseYMD(ymd);
  if (d <= 15) return formatYMD(y, m, daysInMonth(y, m));
  const total = y * 12 + m; const ny = Math.floor(total / 12); const nm = (total % 12) + 1;
  return formatYMD(ny, nm, 15);
}
for (const start of ["2026-01-01", "2026-01-16", "2026-01-10"]) {
  let d = start; const seq = [d];
  for (let i = 0; i < 5; i++) { d = nextSemimonthly(d); seq.push(d); }
  console.log("SEMIMONTHLY from", start + ":", seq.join(" -> "));
}
