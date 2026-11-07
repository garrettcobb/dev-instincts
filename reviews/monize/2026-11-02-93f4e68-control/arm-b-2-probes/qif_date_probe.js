// Probe: QIF date parsing passes unparseable or impossible dates through unchanged.
// Copied from repo/backend/src/import/qif-parser.ts lines 544-553 (normalizeDateSeparators)
// and 607-658 (parseQifDate), transcribed to JS. The result is written to
// transactions.transaction_date without validation
// (repo/backend/src/import/import-regular-processor.service.ts line 124).
// Standard library only. No network, no subprocess, no writes.

function normalizeDateSeparators(dateStr) {
  let normalized = dateStr.replace(/^['"]|['"]$/g, "").trim();
  normalized = normalized.replace(/(\d)\s*['"]\s*(\d)/g, "$1/$2");
  normalized = normalized.replace(/\s*([/-])\s*/g, "$1");
  return normalized;
}
function parseQifDate(dateStr, format) {
  dateStr = normalizeDateSeparators(dateStr);
  let match = dateStr.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
  if (match) {
    const [, year, part2, part3] = match;
    let month, day;
    if (format === "YYYY-DD-MM") { day = part2.padStart(2, "0"); month = part3.padStart(2, "0"); }
    else { month = part2.padStart(2, "0"); day = part3.padStart(2, "0"); }
    return `${year}-${month}-${day}`;
  }
  match = dateStr.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{1,4})$/);
  if (match) {
    const [, part1, part2, yearRaw] = match;
    let year = yearRaw;
    if (year.length <= 2) {
      const yearNum = parseInt(year);
      year = yearNum > 50 ? `19${year.padStart(2, "0")}` : `20${year.padStart(2, "0")}`;
    }
    let month, day;
    if (format === "DD/MM/YYYY") { day = part1.padStart(2, "0"); month = part2.padStart(2, "0"); }
    else { month = part1.padStart(2, "0"); day = part2.padStart(2, "0"); }
    return `${year}-${month}-${day}`;
  }
  return dateStr;
}

const cases = [
  ["13/03/2026", "MM/DD/YYYY"],   // a DD/MM file read as MM/DD: month 13
  ["2/30/2026", "MM/DD/YYYY"],    // Feb 30
  ["3.5.2026", "DD/MM/YYYY"],     // dot separators (German Quicken) are not accepted
  ["03/05/202", "MM/DD/YYYY"],    // 3-digit year
  ["not a date", undefined],
];
for (const [raw, fmt] of cases) {
  console.log(JSON.stringify(raw).padEnd(14), (fmt ?? "(auto)").padEnd(10), "->", JSON.stringify(parseQifDate(raw, fmt)));
}
