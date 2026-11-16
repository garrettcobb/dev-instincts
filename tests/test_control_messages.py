"""No commit message names a control:B row while block 1 is open (Garrett's ruling of
2026-11-07 on dashboarr's arm A run 1; testing/CONTROL.md section 16 item 18 and section 17).

Claude Code puts the last commits' messages into every session's context, a subagent's
included, so a message that names a row tagged control:B in ledger/findings.jsonl reaches arm
A's reviewer, which must not see arm B's rows. The limit is a practice of the block from
2026-11-07: while section 5.2 reads "Block 1: open.", no commit after 678e222 on main (the
commit that adopted it) names such a row's id in its message; the diff carries them. Once the
line reads "Block 1: closed <date>.", nothing is checked.

The ids come from the ledger, not a list here: every row whose tags hold "control:B", by
its id. A message names an id when the id stands in it as a word: not preceded or followed by
a letter or digit, so MZ-L1 doesn't name MZ-L13 and a row's id inside a longer token doesn't
count. The rule is also checked on hand-worked messages and ids. This file asks git for the
messages (git log) and writes nothing.
"""

import json
import os
import re
import subprocess
import unittest

from support import ROOT, read
from test_control_frozen import BLOCK_LINE, subsection

CONTROL = os.path.join(ROOT, "testing", "CONTROL.md")
LEDGER = os.path.join(ROOT, "ledger", "findings.jsonl")
SINCE = "678e222"  # the commit that adopted the limit (2026-11-07); messages after it are checked
TAG = "control:B"


def control_b_ids(ledger_text):
    """The ids of the ledger's rows tagged control:B, in file order, each once."""
    ids = []
    for line in ledger_text.splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if TAG in row.get("tags", []) and row.get("id") and row["id"] not in ids:
            ids.append(row["id"])
    return ids


def names_in(message, ids):
    """The ids that stand in message as words, in ids' order."""
    return [i for i in ids
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(i) + r"(?![A-Za-z0-9])", message)]


def naming(messages, ids):
    """Which commits name a control:B row, as {commit: [ids named]}; empty when none does.
    messages is {commit: message}."""
    found = {}
    for commit, message in messages.items():
        named = names_in(message, ids)
        if named:
            found[commit] = named
    return found


def block_open(control):
    """True while testing/CONTROL.md section 5.2 reads "Block 1: open."; raises when the
    section or its one Block 1 line is missing, so a broken file can't pass as closed."""
    s = subsection(control, "5.2")
    if s is None:
        raise AssertionError("testing/CONTROL.md has no section 5.2")
    states = BLOCK_LINE.findall(s)
    if len(states) != 1:
        raise AssertionError(f"{len(states)} lines read 'Block 1: open.' or "
                             f"'Block 1: closed <date>.'; it needs one")
    return states[0] == "open"


def messages_after(since):
    """The messages of main's commits after since, as {short hash: message}, from git log."""
    out = subprocess.run(["git", "-C", ROOT, "log", "--format=%h%x1f%B%x1e", since + "..HEAD"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         check=True).stdout
    messages = {}
    for record in out.split("\x1e"):
        if record.strip():
            commit, _, message = record.strip("\n").partition("\x1f")
            messages[commit] = message
    return messages


class ControlMessages(unittest.TestCase):
    maxDiff = None  # a failure shows every commit and id

    def test_no_commit_message_after_678e222_names_a_control_b_row_while_block_1_is_open(self):
        """while testing/CONTROL.md section 5.2 reads Block 1: open, no commit message after 678e222 on main names the id of a row tagged control:B in ledger/findings.jsonl"""
        ids = control_b_ids(read(LEDGER))
        got = {"this repo": naming(messages_after(SINCE), ids) if block_open(read(CONTROL)) else {}}
        # The ledger holds control:B rows, so an empty result means no message named one, not
        # that there was nothing to name.
        got["this repo's ledger has control:B rows"] = bool(ids)

        # The rule on hand-worked messages: two control:B rows, XX-L1 and XX-L13; a third row,
        # XX-L2, tagged otherwise.
        ledger = "\n".join([
            '{"id": "XX-L1", "tags": ["latent", "control:B"]}',
            '{"id": "XX-L2", "tags": ["latent", "control:A"]}',
            '{"id": "XX-L13", "tags": ["control:B"]}',
            '{"id": "XX-L1", "tags": ["control:B"]}',
            "",
        ])
        sample_ids = control_b_ids(ledger)
        got.update({
            "ids from the sample ledger": sample_ids,
            "messages": naming({
                "aaaaaaa": "metrics/CONTROL.md: the judge's verdict on XX-L13 and XX-L2",
                "bbbbbbb": "ledger: rows XX-L1, XX-L13 join after the judge",
                "ccccccc": "RULES.md: R520, the limit; XX-L2 and XX-L130 and FXX-L1 don't count",
                "ddddddd": "a message naming nothing\n\nCo-Authored-By: nobody",
                "eeeeeee": "(XX-L1) in brackets, and XX-L13.",
            }, sample_ids),
            "no messages": naming({}, sample_ids),
            "no ids": naming({"aaaaaaa": "XX-L1"}, []),
        })
        # Expected, by hand: this repo's messages after 678e222 name none, and its ledger holds
        # control:B rows (monize's arm B rows, 2026-11-05). In the sample, XX-L2 is tagged
        # control:A and XX-L1's second row repeats it, so the ids are XX-L1 and XX-L13;
        # aaaaaaa names XX-L13 (XX-L2 isn't control:B); bbbbbbb names both; ccccccc names
        # none (XX-L130 and FXX-L1 run into a digit or a letter); ddddddd names none; eeeeeee
        # names both, a bracket and a full stop not being letters or digits.
        expected = {
            "this repo": {},
            "this repo's ledger has control:B rows": True,
            "ids from the sample ledger": ["XX-L1", "XX-L13"],
            "messages": {"aaaaaaa": ["XX-L13"], "bbbbbbb": ["XX-L1", "XX-L13"],
                         "eeeeeee": ["XX-L1", "XX-L13"]},
            "no messages": {},
            "no ids": {},
        }
        self.assertEqual(got, expected)

    def test_block_open_reads_section_5_2_and_refuses_a_missing_or_doubled_line(self):
        """the check runs while section 5.2 reads Block 1: open, stops once it reads closed, and refuses a file with no Block 1 line or two"""
        def control(line):
            return f"## 5. A\nx\n\n### 5.2 C\ny\n\n{line}\n\n## 6. D\nz\n"

        got = {"open": block_open(control("Block 1: open.")),
               "closed": block_open(control("Block 1: closed 2027-01-15."))}
        for name, text in {"no Block 1 line": control("The block is open."),
                           "two Block 1 lines": control("Block 1: open.\n\nBlock 1: closed 2027-01-15."),
                           "no section 5.2": "## 5. A\nx\n\n## 6. D\nBlock 1: open.\n"}.items():
            try:
                block_open(text)
                got[name] = "passed"
            except AssertionError as e:
                got[name] = str(e)
        # Expected, by hand: the hand-made texts read as their lines say, and a text with no one
        # Block 1 line raises. This repo's line is read by the test above, whichever way it reads.
        expected = {
            "open": True,
            "closed": False,
            "no Block 1 line": "0 lines read 'Block 1: open.' or 'Block 1: closed <date>.'; it needs one",
            "two Block 1 lines": "2 lines read 'Block 1: open.' or 'Block 1: closed <date>.'; it needs one",
            "no section 5.2": "testing/CONTROL.md has no section 5.2",
        }
        self.assertEqual(got, expected)
