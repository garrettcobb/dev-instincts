// Probe: semimonthly schedule abandons the user's chosen day.
// Copied from repo/backend/src/common/recurrence.ts lines 49-113
// (parseYMD, formatYMD, daysInMonth, calculateNextDueDate SEMIMONTHLY branch)
// and repo/backend/src/scheduled-transactions/schedule-cursor.ts lines 29-44
// (the advance loop, without the database writes). Transcribed to JavaScript.
const YMD_PATTERN = /^(\d{4})-(\d{2})-(\d{2})$/;
function parseYMD(ymd) {
  const match = YMD_PATTERN.exec(ymd);
  if (!match) throw new Error(`Invalid YYYY-MM-DD date string: ${ymd}`);
  return { y: Number(match[1]), m: Number(match[2]), d: Number(match[3]) };
}
function formatYMD(y, m, d) {
  return `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
}
function daysInMonth(year, month) {
  return new Date(Date.UTC(year, month, 0)).getUTCDate();
}
function calculateNextDueDate(ymd, frequency) {
  switch (frequency) {
    case "SEMIMONTHLY": {
      const { y, m, d } = parseYMD(ymd);
      if (d <= 15) {
        return formatYMD(y, m, daysInMonth(y, m));
      }
      const total = y * 12 + m;
      const ny = Math.floor(total / 12);
      const nm = (total % 12) + 1;
      return formatYMD(ny, nm, 15);
    }
    default:
      return ymd;
  }
}
for (const start of ["2026-01-01", "2026-01-10", "2026-01-20"]) {
  let cur = start;
  const dates = [cur];
  for (let i = 0; i < 5; i++) {
    cur = calculateNextDueDate(cur, "SEMIMONTHLY");
    dates.push(cur);
  }
  console.log(`start ${start}: ${dates.join(" -> ")}`);
}
