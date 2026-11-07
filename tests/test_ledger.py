"""ledger/findings.jsonl against the schema in ledger/README.md (Garrett, Task 6, 2026-11-02).

The schema is read from README.md's Fields table each run, so README.md stays the
authority: a field is required unless its Values cell says "optional", and the
allowed values of the five checked fields are the backticked words in that cell.
"""

import json
import os
import re
import unittest

from support import ROOT, read

README = os.path.join(ROOT, "ledger", "README.md")
LEDGER = os.path.join(ROOT, "ledger", "findings.jsonl")
CHECKED = ("severity", "status", "origin", "caught_by", "evidence")


def fields():
    """README.md's Fields table: field name -> its Values cell."""
    table, inside = {}, False
    for line in read(README).splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Fields"
        if not inside or not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        m = re.fullmatch(r"`([a-z_]+)`", cells[0])
        if m and len(cells) >= 2:
            table[m.group(1)] = cells[1]
    return table


def schema(case):
    table = fields()
    required = {f for f, values in table.items() if "optional" not in values}
    allowed = {f: re.findall(r"`([^`]+)`", table.get(f, "")) for f in CHECKED}
    # If README.md's table changes shape, fail here rather than check nothing.
    case.assertTrue({"id", "project", "title"} | set(CHECKED) <= required,
                    f"couldn't read the required fields from {README}'s Fields table; read {sorted(required)}")
    for f in CHECKED:
        case.assertGreaterEqual(len(allowed[f]), 2,
                                f"couldn't read the allowed values of {f} from {README}; read {allowed[f]}")
    return required, allowed


def rows(case):
    out = []
    for n, line in enumerate(read(LEDGER).splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as e:
            case.fail(f"findings.jsonl line {n} isn't JSON: {e}")
        case.assertIsInstance(row, dict, f"findings.jsonl line {n} isn't a JSON object")
        out.append((n, row))
    case.assertTrue(out, "findings.jsonl has no rows")
    return out


def listed(problems, limit=15):
    more = f"\n... and {len(problems) - limit} more" if len(problems) > limit else ""
    return "\n".join(problems[:limit]) + more


class LedgerRows(unittest.TestCase):
    def test_every_row_has_the_fields_readme_requires(self):
        """every row of ledger/findings.jsonl has the fields ledger/README.md requires"""
        required, _ = schema(self)
        problems = []
        for n, row in rows(self):
            missing = sorted(required - set(row))
            if missing:
                problems.append(f"line {n} ({row.get('id', 'no id')}): no {', '.join(missing)}")
        if problems:
            self.fail(f"{len(problems)} rows miss a required field (below)\n{listed(problems)}")

    def test_every_row_uses_only_the_values_readme_lists(self):
        """every row of ledger/findings.jsonl uses only the severity, status, origin, caught_by and evidence values ledger/README.md lists"""
        _, allowed = schema(self)
        problems = []
        for n, row in rows(self):
            for f in CHECKED:
                if f in row and row[f] not in allowed[f]:
                    problems.append(f"line {n} ({row.get('id', 'no id')}): {f} {row[f]!r} isn't one of {allowed[f]}")
        if problems:
            self.fail(f"{len(problems)} values aren't in README.md's lists (below)\n{listed(problems)}")
