// Probe for claims CT, SL, PC, MG, JN, QR at monize 93f4e68.
// Copied functions (TypeScript transcribed to plain JavaScript):
//  - backend/src/import/amount-separators.util.ts:21-48  normalizeAmountSeparators, countOf
//  - backend/src/import/csv-parser.ts:804-822            parseCsvAmount
//  - backend/src/import/csv-parser.ts:637-660            validateAndFormat, resolveYear
//  - backend/src/import/csv-parser.ts:666-721            parseDateCustom
//  - backend/src/import/csv-parser.ts:733-791            stripTime (tail), parseCsvDate
//  - backend/src/common/recurrence.ts:139-146            SEMIMONTHLY branch of calculateNextDueDate
//  - frontend/src/app/reconcile/page.tsx:381-389         difference rounding and finish check
//  - frontend/src/components/transactions/TransactionForm.tsx:798  quick-fill rounding
// Stand-ins (no control-flow change): parseYMD/formatYMD/daysInMonth/escapeRegExp are
// trivial helpers written here; KNOWN_FORMATS is the set listed at csv-parser.ts:625-631.

function countOf(value, separator) { return value.split(separator).length - 1; }
function normalizeAmountSeparators(value) {
  const commaCount = countOf(value, ",");
  const dotCount = countOf(value, ".");
  if (commaCount > 0 && dotCount > 0) {
    return value.lastIndexOf(",") > value.lastIndexOf(".")
      ? value.replace(/\./g, "").replace(",", ".")
      : value.replace(/,/g, "");
  }
  if (commaCount === 1) {
    const commaAt = value.indexOf(",");
    const integerPart = value.slice(0, commaAt).replace(/^[-+]/, "");
    const digitsAfter = value.length - commaAt - 1;
    const isGrouping = digitsAfter === 3 && !/^0*$/.test(integerPart);
    return isGrouping ? value.replace(",", "") : value.replace(",", ".");
  }
  if (commaCount > 1) return value.replace(/,/g, "");
  if (dotCount > 1) return value.replace(/\./g, "");
  return value;
}
function parseCsvAmount(value) {
  let cleaned = value.trim();
  if (!cleaned) return null;
  const parenMatch = cleaned.match(/^\((.+)\)$/);
  if (parenMatch) cleaned = "-" + parenMatch[1];
  cleaned = cleaned.replace(/[$£€¥₹\s]/g, "");
  cleaned = normalizeAmountSeparators(cleaned);
  const amount = parseFloat(cleaned);
  return isNaN(amount) ? null : amount;
}

const KNOWN_FORMATS = new Set(["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD", "YYYY-DD-MM"]);
function validateAndFormat(year, month, day) {
  const y = parseInt(year); const m = parseInt(month); const d = parseInt(day);
  if (m < 1 || m > 12 || d < 1 || d > 31 || y < 1900 || y > 2100) return null;
  return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
}
function resolveYear(raw) {
  if (raw.length === 4) return raw;
  const n = parseInt(raw);
  return n > 50 ? `19${raw}` : `20${raw}`;
}
function escapeRegExp(s) { const bs = String.fromCharCode(92); return s.split("").map((c) => /[A-Za-z0-9 ]/.test(c) ? c : bs + c).join(""); }
function parseDateCustom(dateStr, format) {
  let regex = "^"; const groups = []; let i = 0;
  while (i < format.length) {
    if (format.substring(i, i + 4) === "YYYY") { regex += "(\d{4})"; groups.push("year4"); i += 4; }
    else if (format.substring(i, i + 2) === "YY") { regex += "(\d{2})"; groups.push("year2"); i += 2; }
    else if (format.substring(i, i + 2) === "MM") { regex += "(\d{1,2})"; groups.push("month"); i += 2; }
    else if (format.substring(i, i + 2) === "DD") { regex += "(\d{1,2})"; groups.push("day"); i += 2; }
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

// recurrence.ts SEMIMONTHLY branch
function parseYMD(s) { const [y, m, d] = s.split("-").map(Number); return { y, m, d }; }
function pad(n) { return String(n).padStart(2, "0"); }
function formatYMD(y, m, d) { return `${y}-${pad(m)}-${pad(d)}`; }
function daysInMonth(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); }
function semimonthlyNext(ymd) {
  const { y, m, d } = parseYMD(ymd);
  if (d <= 15) return formatYMD(y, m, daysInMonth(y, m));
  const total = y * 12 + m;
  const ny = Math.floor(total / 12);
  const nm = (total % 12) + 1;
  return formatYMD(ny, nm, 15);
}

// reconcile/page.tsx:381-389
function finishAllowed(statementBalance, reconciledBalance, selectedSum) {
  const newBalance = Number(reconciledBalance) + selectedSum;
  const calculatedDifference = Math.round(((statementBalance ?? 0) - newBalance) * 100) / 100;
  return { calculatedDifference, finishAllowed: !(Math.abs(calculatedDifference) > 0.01) };
}

console.log("== CT parseCsvAmount (row amount = result ?? 0)");
for (const v of ["\u221212.34", "12.34-", "CHF 12.34", "DR 12.34", "-12.34", "(12.34)", "1.234,56"]) {
  const r = parseCsvAmount(v);
  console.log(JSON.stringify(v).padEnd(14), "->", r, "  stored:", r ?? 0);
}
console.log("== SL parseCsvDate");
for (const [v, f] of [["05/03/2026","MM/DD/YYYY"],["13/03/2026","MM/DD/YYYY"],["28/03/2026","MM/DD/YYYY"],["02/30/2026","MM/DD/YYYY"],["04/31/2026","MM/DD/YYYY"],["05 Mar 2026","DD MMM YYYY"],["2026-03-05 14:30","YYYY-MM-DD"]]) {
  console.log(JSON.stringify(v).padEnd(20), f.padEnd(12), "->", parseCsvDate(v, f));
}
console.log("== JN/QR SEMIMONTHLY");
for (const start of ["2026-01-01", "2026-01-16", "2026-01-15", "2026-01-31"]) {
  let d = start; const seq = [d];
  for (let i = 0; i < 5; i++) { d = semimonthlyNext(d); seq.push(d); }
  console.log(start, ":", seq.join(" -> "));
}
console.log("== PC finish check");
for (const sb of [1000.00, 1000.01, 999.99, 1000.02]) console.log(JSON.stringify(finishAllowed(sb, 1000.00, 0)));
console.log("== MG quick-fill rounding");
for (const a of ["12.345", "12.3456"]) console.log(a, "->", Math.round(Number(a) * 100) / 100);
