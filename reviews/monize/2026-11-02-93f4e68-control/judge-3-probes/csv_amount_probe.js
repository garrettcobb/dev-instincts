// Transcribed from repo at 93f4e68:
//   backend/src/import/amount-separators.util.ts:21-45  normalizeAmountSeparators, countOf
//   backend/src/import/csv-parser.ts:804-822            parseCsvAmount
// Caller behaviour mirrored from csv-parser.ts:1205 (`?? 0`).
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
for (const s of ["\u221212.34", "12.34-", "12.34 CR", "DR 12.34", "CHF 12.34", "-12.34", "(12.34)", "1,234.56"]) {
  const r = parseCsvAmount(s);
  console.log(JSON.stringify(s).padEnd(14), "->", String(r).padEnd(8), "stored as", r ?? 0);
}
