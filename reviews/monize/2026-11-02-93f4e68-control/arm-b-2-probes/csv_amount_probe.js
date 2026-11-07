// Probe: CSV amount parsing silently turns unparseable amounts into 0.
// Copied from repo/backend/src/import/amount-separators.util.ts lines 21-45
//   (normalizeAmountSeparators, countOf)
// and repo/backend/src/import/csv-parser.ts lines 804-820 (parseCsvAmount)
// and the caller at csv-parser.ts lines 1205-1227 (`?? 0` fallback), transcribed to JS.
// Standard library only. No network, no subprocess, no writes.

function countOf(value, separator) {
  return value.split(separator).length - 1;
}
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
// What parseCsv does with the result for a single "amount" column (line 1206):
function importedAmount(field) {
  return parseCsvAmount(field) ?? 0;
}

const cases = [
  "−12.34",      // Unicode minus sign U+2212, used by several bank exports
  "12.34-",           // trailing minus (SAP / some European banks)
  "12.34 CR",         // CR/DR suffix
  "DR 12.34",
  "CHF 12.34",        // currency code prefix (symbol stripper only knows $ £ € ¥ ₹)
  "12.34 kr",
  "-12.34",           // control: works
  "(12.34)",          // control: works
];
for (const c of cases) {
  console.log(
    JSON.stringify(c).padEnd(14),
    "parseCsvAmount ->",
    String(parseCsvAmount(c)).padEnd(6),
    " row imported with amount",
    importedAmount(c),
  );
}
