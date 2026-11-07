"""tools/stats.py and the control's block (Garrett's ruling of 2026-11-06, testing/CONTROL.md section 5.2).

The ruling, in Garrett's words: "while the block state line reads open, tools/stats.py leaves
every row tagged control:B out of the check orders and the counts that feed them, says in
STATS.md's header how many rows it left out and why, and still counts them in the per-project
and per-round tables; when the block closes the next run includes them." And: "stats.py reads
the state line from testing/CONTROL.md and stops with a message if the line is missing."

The state line is section 5.2's "Block 1: open." or "Block 1: closed <date>.", alone on its
line, as tests/test_control_frozen.py reads it. Each test runs a copy of this repo's
tools/stats.py in a scratch folder holding what it opens: DEV-INSTINCTS.md as it is here;
testing/CONTROL.md as it is here, with its state line set for the case; and
ledger/findings.jsonl and ledger/projects.json as they stood at 74f2043, read with git cat-file
and checked against their SHA-256s below, so the hand-worked values stay right as the ledger
grows. Nothing here writes outside the scratch folders.

The architect's (2026-11-06; Garrett may change them): the header sentence below; the header's
open-or-unverified count, which counts every row and feeds no check order, kept at 460; the
parts of STATS.md that may differ between open and closed (the header and the two check
orders that hold the eleven rows), so every other table counts them in both states; a missing
testing/CONTROL.md read as a missing line.
"""

import hashlib
import os
import re
import subprocess
import unittest

from support import PY, ROOT, copy_into, read, run, scratch, write

# The ledger the expected values are worked from: 74f2043, the reviewer's ledger step of
# 2026-11-06 (the commit before this test). sha256sum of each file there: findings.jsonl
# 568,657 bytes, projects.json 1,929 bytes.
AT = "74f2043d53db134d5dfd580984428e817d405546"
PINNED = {
    "ledger/findings.jsonl": "1feca32d6f5295d8bae5c541d81d2d980a44526b7ff393a71747ee3567ee29e3",
    "ledger/projects.json": "18845871b7a4fb4229994caaa557e838b0617f2f6015cc495756f08c5e3139a1",
}
BLOCK_LINE = re.compile(r"^Block 1: (open|closed \d{4}-\d{2}-\d{2})\.$", re.M)
OPEN, CLOSED, NO_LINE, NO_FILE = "Block 1: open.", "Block 1: closed 2026-12-31.", None, "no file"
SENTINEL = "Not written by stats.py: a file it must overwrite, or leave as it is when it stops.\n"
ALL_KINDS = "## Check order, all kinds (highest cost first)"
WEB_APP = "## Check order for a web app (top 15)"

# Expected, by hand, from the ledger at 74f2043.
#
# Rows: 650 in 4 projects and 60 rounds. 519 feed the check order (the developer's own
# projects and AI-written outside ones: tools/stats.py's in_check_order) and 131 are reference
# data (Django's human-written rows). The 11 rows tagged control:B are MZ-L13 to MZ-L23, all
# Monize's, a web app registered ai and not own, so all 11 feed the check order today. With
# the block open: 519 - 11 = 508 feed it, 11 are left out, 131 stay reference, and
# 508 + 11 + 131 = 650.
#
# Open or unverified (status open, not-fixed, partly-fixed, fixed-with-problem or
# fixed-claimed): 460 over every row, the 131 reference rows included, as the Status table
# sums it (fixed-claimed 305 + open 130 + fixed-with-problem 11 + partly-fixed 9 + not-fixed
# 5 = 460). It feeds no check order, so it stays 460 with the block open. (The 11 are 7 open
# and 4 fixed-claimed, all 11 in that count, so leaving them out of it would give 449.)
#
# The score, as tools/stats.py's score() and rank() have it at 74f2043: each finding weighs
# data-loss 8, security 8, wrong-result 5, crash 4, stuck 2, process 2, cosmetic 1, doubled
# for origin regression or carry-over, and counts once for each instinct it lists (a finding
# with two instincts counts for both); instincts rank by score, highest first, a tie by the
# lower number. The 11, every one origin pre-existing (so not doubled):
#   MZ-L13 wrong-result 5 [23, 11]    MZ-L17 data-loss 8 [6, 27]       MZ-L21 wrong-result 5 [6]
#   MZ-L14 wrong-result 5 [58, 9]     MZ-L18 data-loss 8 [6, 27]       MZ-L22 data-loss 8 [9, 6]
#   MZ-L15 wrong-result 5 [51, 10]    MZ-L19 wrong-result 5 [6, 51]    MZ-L23 wrong-result 5 [10]
#   MZ-L16 data-loss 8 [6, 10]        MZ-L20 crash 4 [9]
# What they add to each instinct: #6 six findings (L16, L17, L18, L19, L21, L22),
# 8 + 8 + 8 + 5 + 5 + 8 = 42; #27 two (L17, L18), 8 + 8 = 16; #10 three (L15, L16, L23),
# 5 + 8 + 5 = 18; #9 three (L14, L20, L22), 5 + 4 + 8 = 17; #51 two (L15, L19), 5 + 5 = 10;
# #23, #11 and #58 one each, 5. Nothing to #28, #3, #7 or #5.
#
# All kinds, closed (every row that feeds it; the architect's count of the ledger, apart
# from tools/stats.py, gives what STATS.md at 74f2043 prints): #6 60 findings, score 367;
# #28 32, 244; #3 40, 217; #27 39, 192; #7 25, 179; then #5 27, 156. 55 instincts ranked.
# All kinds, open: #6 60 - 6 = 54, 367 - 42 = 325; #28 32, 244; #3 40, 217; #7 25, 179;
# #27 39 - 2 = 37, 192 - 16 = 176. So #7 (179) and #27 (176) change places, and #5's 156 stays
# sixth. #51's only findings in the check order are L15 and L19 (closed: 2 findings,
# 5 + 5 = 10), so it drops out: 54 ranked.
#
# Web app (Django, Monize, PrivateApp), closed: from 351 findings; #6 52, 318; #3 40, 217;
# #28 24, 174; #27 35, 166; #7 22, 150; then #5 17, 94.
# Web app, open: from 351 - 11 = 340; #6 52 - 6 = 46, 318 - 42 = 276; #3 40, 217; #28 24, 174;
# #27 35 - 2 = 33, 166 - 16 = 150, and #7 22, 150: a tie, the lower number first, so #7 is
# fourth and #27 fifth; #5's 94 stays sixth. The desktop app's order (Ferrite) holds none of
# the 11 and doesn't change.
#
# Per project and per round, the same in both states: Monize has 23 rows, MZ-L01 to MZ-L23,
# every one with an instinct and origin pre-existing, in 3 rounds (7 + 5 + 11 = 23), so
# Coverage reads 23, 100%, 0%, 0%; Targets 23, none escaped and no regression, its last 5
# rounds being all 3; and By round gives the control round its 11.
OPEN_HEADER = (
    "**650 findings** across 4 project(s) and 60 round(s). 508 feed the check order; 11 rows "
    "tagged `control:B` are left out of it while the block state line in testing/CONTROL.md "
    "§5.2 reads open; 131 are reference data from human-written outside projects. Open or "
    "unverified: 460."
)
CLOSED_HEADER = (
    "**650 findings** across 4 project(s) and 60 round(s). 519 feed the check order; 131 are "
    "reference data from human-written outside projects. Open or unverified: 460."
)
MONIZE_ROWS = [
    "| Monize | web app | ai | 23 | 100% | 0% | 0% |",  # Coverage of outside projects
    "| Monize | all rounds | 23 | 0 (0%) | 0 (0%) |",  # Targets
    "| Monize | last 5 rounds | 23 | 0 (0%) | 0 (0%) |",  # Targets
    "| Monize | 2026-11-02-93f4e68-control | 11 | 0 | 0 |",  # By round
]


def pinned(path):
    """A ledger file's bytes as they stood at AT, checked against its SHA-256 above."""
    data = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", f"{AT}:{path}"],
                          capture_output=True, check=True).stdout
    have = hashlib.sha256(data).hexdigest()
    if have != PINNED[path]:
        raise AssertionError(f"{path} at {AT[:7]} hashes {have}, not {PINNED[path]}")
    return data


def stage(case, state):
    """A scratch folder holding what stats.py opens, with testing/CONTROL.md's Block 1 line
    set to state (NO_LINE: the line removed; NO_FILE: no testing/CONTROL.md), and a
    ledger/STATS.md holding SENTINEL."""
    work = scratch(case)
    copy_into(work, ["tools/stats.py", "DEV-INSTINCTS.md"])
    os.makedirs(os.path.join(work, "ledger"))
    for path in PINNED:
        with open(os.path.join(work, *path.split("/")), "wb") as f:
            f.write(pinned(path))
    if state != NO_FILE:
        text = read(os.path.join(ROOT, "testing", "CONTROL.md"))
        found = list(BLOCK_LINE.finditer(text))
        if len(found) != 1:
            raise AssertionError(f"testing/CONTROL.md has {len(found)} Block 1 lines; the test sets one")
        m = found[0]
        write(os.path.join(work, "testing", "CONTROL.md"),
              text[:m.start()] + (state or "") + text[m.end():])
    write(os.path.join(work, "ledger", "STATS.md"), SENTINEL)
    return work


def stats(work):
    """Run the folder's tools/stats.py from the folder."""
    return run([PY, "-I", "-B", os.path.join(work, "tools", "stats.py")], cwd=work)


def written(case, work):
    """The folder's ledger/STATS.md after a run that must succeed."""
    r = stats(work)
    case.assertEqual(r.returncode, 0, f"stats.py failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-800:]}")
    return read(os.path.join(work, "ledger", "STATS.md"))


def sections(text):
    """STATS.md's parts: the lines before its first "## " heading under "(top)", then each
    "## " heading's lines, its "### " sub-headings inside it."""
    out, key = {}, "(top)"
    for line in text.split("\n"):
        if line.startswith("## "):
            key = line
        out[key] = out.get(key, "") + line + "\n"
    return out


def header(text):
    """STATS.md's line that opens with the findings count."""
    lines = [line for line in text.split("\n") if line.startswith("**")]
    return lines[0] if len(lines) == 1 else lines


def ranked(section):
    """(instinct, findings, score) for each row of a check-order table in section."""
    out = []
    for line in (section or "").split("\n"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| ") and cells[0].isdigit():
            out.append((int(cells[0]), int(cells[-5]), int(cells[-4])))
    return out


def from_line(section):
    """A kind's check order's "From <n> findings in ..." line."""
    lines = [line for line in (section or "").split("\n") if line.startswith("From ")]
    return lines[0] if len(lines) == 1 else lines


def snapshot(folder):
    """Every file under folder, by its path in it, with its bytes."""
    out = {}
    for base, _, names in os.walk(folder):
        for name in names:
            path = os.path.join(base, name)
            with open(path, "rb") as f:
                out[os.path.relpath(path, folder)] = f.read()
    return out


class StatsBlock(unittest.TestCase):
    maxDiff = None  # a failure shows the whole dict

    def test_while_block_1_is_open_stats_leaves_the_control_b_rows_out_of_the_check_orders(self):
        """while testing/CONTROL.md section 5.2 reads Block 1: open, tools/stats.py leaves the 11 control:B rows out of the check orders, says how many and why in STATS.md's header, and still counts them per project and per round"""
        text = written(self, stage(self, OPEN))
        s = sections(text)
        lines = text.split("\n")
        got = {
            "header": header(text),
            "all kinds, top five": ranked(s.get(ALL_KINDS))[:5],
            "all kinds, instincts ranked": len(ranked(s.get(ALL_KINDS))),
            "all kinds, #51 ranked": 51 in [n for n, _, _ in ranked(s.get(ALL_KINDS))],
            "web app, from": from_line(s.get(WEB_APP)),
            "web app, top five": ranked(s.get(WEB_APP))[:5],
            "Monize's rows per project and per round": [row for row in MONIZE_ROWS if row in lines],
        }
        # Expected, by hand: above, the block open.
        expected = {
            "header": OPEN_HEADER,
            "all kinds, top five": [(6, 54, 325), (28, 32, 244), (3, 40, 217), (7, 25, 179), (27, 37, 176)],
            "all kinds, instincts ranked": 54,
            "all kinds, #51 ranked": False,
            "web app, from": "From 340 findings in Django, Monize, PrivateApp. Use this order when reviewing this kind of software.",
            "web app, top five": [(6, 46, 276), (3, 40, 217), (28, 24, 174), (7, 22, 150), (27, 33, 150)],
            "Monize's rows per project and per round": MONIZE_ROWS,
        }
        self.assertEqual(got, expected)

    def test_once_block_1_is_closed_stats_counts_the_control_b_rows_again(self):
        """once testing/CONTROL.md section 5.2 reads Block 1: closed with a date, tools/stats.py counts the control:B rows in the check orders again, and the two STATS.md files differ only in the header and the check orders that hold those rows"""
        opened = written(self, stage(self, OPEN))
        closed = written(self, stage(self, CLOSED))
        so, sc = sections(opened), sections(closed)
        got = {
            "header": header(closed),
            "all kinds, top five": ranked(sc.get(ALL_KINDS))[:5],
            "all kinds, instincts ranked": len(ranked(sc.get(ALL_KINDS))),
            "web app, from": from_line(sc.get(WEB_APP)),
            "web app, top five": ranked(sc.get(WEB_APP))[:5],
            "lines naming control:B": [line for line in closed.split("\n") if "control:B" in line],
            "the same parts, in the same order": list(so) == list(sc),
            "parts that differ": sorted(k for k in sc if so.get(k) != sc[k]),
        }
        # Expected, by hand: above, the block closed, as STATS.md read before the ruling; and
        # the only parts the 11 rows move, the header (its count and its clause), the all-kinds
        # order and the web-app order. The desktop order and every other table, the
        # per-project and per-round ones among them, count every row in both states.
        expected = {
            "header": CLOSED_HEADER,
            "all kinds, top five": [(6, 60, 367), (28, 32, 244), (3, 40, 217), (27, 39, 192), (7, 25, 179)],
            "all kinds, instincts ranked": 55,
            "web app, from": "From 351 findings in Django, Monize, PrivateApp. Use this order when reviewing this kind of software.",
            "web app, top five": [(6, 52, 318), (3, 40, 217), (28, 24, 174), (27, 35, 166), (7, 22, 150)],
            "lines naming control:B": [],
            "the same parts, in the same order": True,
            "parts that differ": sorted(["(top)", ALL_KINDS, WEB_APP]),
        }
        self.assertEqual(got, expected)

    def test_with_no_block_state_line_stats_stops_with_a_message_and_writes_nothing(self):
        """with no Block 1 line in testing/CONTROL.md, or no testing/CONTROL.md, tools/stats.py stops with a message naming the line and writes nothing"""
        got, expected = {}, {}
        for case, state in (("the line removed", NO_LINE), ("no testing/CONTROL.md", NO_FILE)):
            work = stage(self, state)
            before = snapshot(work)
            r = stats(work)
            said = r.stdout + r.stderr
            got[case] = {
                "exit status": r.returncode,
                "names CONTROL.md and the Block 1 line": "CONTROL.md" in said and "Block 1:" in said,
                "a traceback": "Traceback" in said,
                "every file as it was": snapshot(work) == before,
            }
            # Expected, by hand: stats.py's own stop, as its other refusals (raise SystemExit
            # with a message: exit status 1, no traceback), before it writes anything, so
            # ledger/STATS.md still holds SENTINEL and no file is new.
            expected[case] = {
                "exit status": 1,
                "names CONTROL.md and the Block 1 line": True,
                "a traceback": False,
                "every file as it was": True,
            }
        self.assertEqual(got, expected)
