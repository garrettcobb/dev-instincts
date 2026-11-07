// Transcribed from repo at 93f4e68, backend/src/import/qif-parser.ts:
//   544-553 normalizeDateSeparators, 555-605 detectDateFormat, 607-658 parseQifDate
function normalizeDateSeparators(dateStr) {
  let normalized = dateStr.replace(/^['"]|['"]$/g, "").trim();
  normalized = normalized.replace(/(\d)\s*['"]\s*(\d)/g, "$1/$2");
  normalized = normalized.replace(/\s*([/-])\s*/g, "$1");
  return normalized;
}
function detectDateFormat(dates) {
  if (dates.length === 0) return "MM/DD/YYYY";
  const normalizedDates = dates.map(normalizeDateSeparators);
  const isoMatch = normalizedDates[0]?.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
  if (isoMatch) {
    const [, , part2, part3] = isoMatch; const p2 = parseInt(part2), p3 = parseInt(part3);
    if (p2 > 12) return "YYYY-DD-MM"; if (p3 > 12) return "YYYY-MM-DD";
    for (const date of normalizedDates) { const m = date.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/); if (m) { if (parseInt(m[2]) > 12) return "YYYY-DD-MM"; if (parseInt(m[3]) > 12) return "YYYY-MM-DD"; } }
    return "YYYY-MM-DD";
  }
  for (const date of normalizedDates) {
    const match = date.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{1,4})$/);
    if (match) { const p1 = parseInt(match[1]), p2 = parseInt(match[2]); if (p1 > 12) return "DD/MM/YYYY"; if (p2 > 12) return "MM/DD/YYYY"; }
  }
  return "MM/DD/YYYY";
}
function parseQifDate(dateStr, format) {
  dateStr = normalizeDateSeparators(dateStr);
  let match = dateStr.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
  if (match) { const [, year, part2, part3] = match; let month, day;
    if (format === "YYYY-DD-MM") { day = part2.padStart(2, "0"); month = part3.padStart(2, "0"); } else { month = part2.padStart(2, "0"); day = part3.padStart(2, "0"); }
    return `${year}-${month}-${day}`; }
  match = dateStr.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{1,4})$/);
  if (match) { const [, part1, part2, yearRaw] = match; let year = yearRaw;
    if (year.length <= 2) { const yearNum = parseInt(year); year = yearNum > 50 ? `19${year.padStart(2, "0")}` : `20${year.padStart(2, "0")}`; }
    let month, day;
    if (format === "DD/MM/YYYY") { day = part1.padStart(2, "0"); month = part2.padStart(2, "0"); } else { month = part1.padStart(2, "0"); day = part2.padStart(2, "0"); }
    return `${year}-${month}-${day}`; }
  return dateStr;
}
const dotted = ["3.5.2026", "13.3.2026"];
console.log("detectDateFormat(dotted file) =", detectDateFormat(dotted));
for (const d of dotted) console.log(JSON.stringify(d).padEnd(14), "->", JSON.stringify(parseQifDate(d, detectDateFormat(dotted))));
console.log(JSON.stringify("not a date").padEnd(14), "->", JSON.stringify(parseQifDate("not a date", "MM/DD/YYYY")));
console.log(JSON.stringify("13/03/2026").padEnd(14), "forced MM/DD/YYYY ->", parseQifDate("13/03/2026", "MM/DD/YYYY"), "| auto-detect ->", detectDateFormat(["13/03/2026"]));
console.log(JSON.stringify("2/30/2026").padEnd(14), "MM/DD/YYYY ->", parseQifDate("2/30/2026", "MM/DD/YYYY"));
