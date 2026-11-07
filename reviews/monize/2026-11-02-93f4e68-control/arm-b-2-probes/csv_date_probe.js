// Probe: CSV date parsing drops rows silently and accepts impossible dates.
// Copied from repo/backend/src/import/csv-parser.ts lines 626-631 (KNOWN_FORMATS),
// 637-649 (validateAndFormat), 655-659 (resolveYear), 666-724 (parseDateCustom),
// 735-747 (stripTime), 749-802 (parseCsvDate); escapeRegExp from
// repo/backend/src/common/escape-regexp.util.ts lines 24-26. Transcribed to JS.
// The caller at csv-parser.ts lines 1187-1197 skips a row whose date is null
// with `continue` and records nothing.
// Standard library only. No network, no subprocess, no writes.

const KNOWN_FORMATS = new Set(["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD", "YYYY-DD-MM"]);
function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function validateAndFormat(year, month, day) {
  const y = parseInt(year);
  const m = parseInt(month);
  const d = parseInt(day);
  if (m < 1 || m > 12 || d < 1 || d > 31 || y < 1900 || y > 2100) return null;
  return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
}
function resolveYear(raw) {
  if (raw.length === 4) return raw;
  const n = parseInt(raw);
  return n > 50 ? `19${raw}` : `20${raw}`;
}
function parseDateCustom(dateStr, format) {
  let regex = "^";
  const groups = [];
  let i = 0;
  while (i < format.length) {
    if (format.substring(i, i + 4) === "YYYY") { regex += "(\\d{4})"; groups.push("year4"); i += 4; }
    else if (format.substring(i, i + 2) === "YY") { regex += "(\\d{2})"; groups.push("year2"); i += 2; }
    else if (format.substring(i, i + 2) === "MM") { regex += "(\\d{1,2})"; groups.push("month"); i += 2; }
    else if (format.substring(i, i + 2) === "DD") { regex += "(\\d{1,2})"; groups.push("day"); i += 2; }
    else { regex += escapeRegExp(format[i]); i += 1; }
  }
  regex += "$";
  const match = dateStr.match(new RegExp(regex));
  if (!match) return null;
  let year = "", month = "", day = "";
  for (let g = 0; g < groups.length; g++) {
    const val = match[g + 1];
    switch (groups[g]) {
      case "year4": year = val; break;
      case "year2": year = resolveYear(val); break;
      case "month": month = val; break;
      case "day": day = val; break;
    }
  }
  if (!year || !month || !day) return null;
  return validateAndFormat(year, month, day);
}
function stripTime(dateStr) {
  const tIndex = dateStr.indexOf("T");
  if (tIndex > 0) return dateStr.substring(0, tIndex);
  const spaceMatch = dateStr.match(/^(\S+)\s+\d{1,2}:\d{2}/);
  if (spaceMatch) return spaceMatch[1];
  return dateStr;
}
function parseCsvDate(dateStr, format) {
  const trimmed = stripTime(dateStr.trim());
  if (!trimmed) return null;
  if (!KNOWN_FORMATS.has(format)) return parseDateCustom(trimmed, format);
  let year, month, day;
  if (format === "YYYY-MM-DD" || format === "YYYY-DD-MM") {
    const match = trimmed.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$/);
    if (!match) return null;
    year = match[1];
    if (format === "YYYY-DD-MM") { day = match[2].padStart(2, "0"); month = match[3].padStart(2, "0"); }
    else { month = match[2].padStart(2, "0"); day = match[3].padStart(2, "0"); }
  } else {
    const match = trimmed.match(/^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})$/);
    if (!match) return null;
    year = resolveYear(match[3]);
    if (format === "DD/MM/YYYY") { day = match[1].padStart(2, "0"); month = match[2].padStart(2, "0"); }
    else { month = match[1].padStart(2, "0"); day = match[2].padStart(2, "0"); }
  }
  return validateAndFormat(year, month, day);
}

console.log("A DD/MM/YYYY statement imported under the MM/DD/YYYY mapping:");
for (const raw of ["05/03/2026", "12/03/2026", "13/03/2026", "28/03/2026"]) {
  const r = parseCsvDate(raw, "MM/DD/YYYY");
  console.log("  ", raw, "->", r === null ? "null  (row silently dropped)" : r + "  (imported with month and day swapped)");
}
console.log("Impossible calendar dates accepted and handed to the database:");
for (const [raw, fmt] of [["02/30/2026", "MM/DD/YYYY"], ["04/31/2026", "MM/DD/YYYY"], ["2026-02-29", "YYYY-MM-DD"]]) {
  console.log("  ", raw, "->", parseCsvDate(raw, fmt));
}
console.log("Month-name dates: MMM is not a token, so every row of such a file is dropped:");
console.log("  ", "05 Mar 2026 under DD MMM YYYY ->", parseCsvDate("05 Mar 2026", "DD MMM YYYY"));
console.log("Control:", "2026-03-05 14:30 under YYYY-MM-DD ->", parseCsvDate("2026-03-05 14:30", "YYYY-MM-DD"));
