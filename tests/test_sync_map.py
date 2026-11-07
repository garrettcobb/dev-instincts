"""The checks SYNC.md's map names for rows that nothing checked before (Garrett, tool task 5,
2026-11-03: "SYNC's unchecked rows get checks").

- The public repo's lag, the *Public repo* line in metrics/FILED.md, and the export tag:
  the latest such line names the latest export/<date> tag, or, while this repo has no
  export tag, says its count is counted by date (WORKFLOW.md, Mirror, tag, export, 4).
  The rule is checked on this repo as it is, and on hand-worked lines.
- DEV_CONTROL_HOME: testing/CONTROL.md stops each window that builds a path from the
  variable where it isn't set: section 7's three (before the run, the session, after it)
  and section 10's three, the judge's. Each window opens with the guard line, whose throw
  stops it; the window's other lines sit inside the guard's else { }, closed by a lone },
  so PowerShell takes the window as one input however it is pasted.

The tags' copy, the mirror's bundle, is checked in tests/test_mirror.py. Nothing here
writes a file; git is asked only for this repo's tags.
"""

import os
import re
import unittest

from support import ROOT, read, run

FILED = os.path.join(ROOT, "metrics", "FILED.md")
CONTROL = os.path.join(ROOT, "testing", "CONTROL.md")

# A Public repo line in FILED.md: "**Public repo (<date>):** ...", one line each.
LAG_LINE = re.compile(r"^\*\*Public repo \((\d{4}-\d{2}-\d{2})\)\:\*\*.*$", re.M)
# An export tag as WORKFLOW.md names it: export/<date>, export/<date>-2 for that day's second.
EXPORT_TAG = re.compile(r"^export/(\d{4}-\d{2}-\d{2})(?:-(\d+))?$")
BY_DATE = "counted by date"
GUARD = 'if (-not $env:DEV_CONTROL_HOME) { throw "DEV_CONTROL_HOME is not set in this window" } else {'
# The windows that build a path from DEV_CONTROL_HOME, each as its section and the steps it
# holds, from testing/CONTROL.md read by hand: a step's window is the one its "# <n>. " line
# names, or step 1's. Section 7's step 5 moves the agents back with no path from the
# variable, so no window here holds it.
WINDOWS = {
    "section 7, window 1: steps 1 and 2, before the run": ("7", ["1", "2"]),
    "section 7, window 2: step 3, the session": ("7", ["3"]),
    "section 7, window 3: step 4, after the session": ("7", ["4"]),
    "section 10, window 1: step 1, before the run": ("10", ["1"]),
    "section 10, window 2: step 2, the session": ("10", ["2"]),
    "section 10, window 3: step 3, after the session": ("10", ["3"]),
}


def lag_line_problem(filed, tags):
    """What is wrong with the latest Public repo line in a FILED.md's text, given the repo's
    export tags; None when nothing is. The latest line has the latest date (of two with one
    date, the lower in the file); the latest tag has the latest date and, of one day's tags,
    the highest number, export/<date> itself being that day's first."""
    lines = [(m.group(1), i, m.group(0)) for i, m in enumerate(LAG_LINE.finditer(filed))]
    if not lines:
        return "no *Public repo* line"
    latest = max(lines)[2]
    keyed = []
    for tag in tags:
        m = EXPORT_TAG.match(tag)
        if m is None:
            return f"{tag} isn't export/<date> or export/<date>-<n> (WORKFLOW.md, Mirror, tag, export, 4)"
        keyed.append(((m.group(1), int(m.group(2) or 1)), tag))
    if not keyed:
        if BY_DATE in latest:
            return None
        return f"no export tag, and the latest *Public repo* line doesn't say it is {BY_DATE}"
    tag = max(keyed)[1]
    if re.search(r"(?<![\w/.-])" + re.escape(tag) + r"(?![\w-])", latest):
        return None
    return f"the latest *Public repo* line doesn't name the latest export tag, {tag}"


def control_steps(text, section):
    """The steps of a testing/CONTROL.md section's powershell blocks, as {step number: its
    lines}, or None if the section has no such block. A section runs from its "## <n>. "
    heading to the next heading of two or three #. Each block is split at its step lines,
    "# <n>. ", which are left out; the lines above a block's first step line go with it."""
    m = re.search(rf"^## {section}\. .*?(?=^#{{2,3}} |\Z)", text, re.M | re.S)
    blocks = re.findall(r"^```powershell\n(.*?)^```", m.group(0), re.M | re.S) if m else []
    if not blocks:
        return None
    steps = {}
    for block in blocks:
        above, step = [], None
        for line in block.splitlines():
            s = re.match(r"# (\d+)\. ", line)
            if s:
                step = s.group(1)
                steps[step] = above
                above = []
            elif step is None:
                above.append(line)
            else:
                steps[step].append(line)
    return steps


class SyncMap(unittest.TestCase):
    maxDiff = None  # a failure shows the whole dict

    def test_the_latest_public_repo_line_names_the_latest_export_tag(self):
        """the latest Public repo line in metrics/FILED.md names the latest export tag, or says it is counted by date while there is no export tag"""
        r = run(["git", "-C", ROOT, "tag", "--list", "export/*"])
        self.assertEqual(r.returncode, 0, f"git tag --list failed: {r.stderr.strip()}")
        got = {"this repo": lag_line_problem(read(FILED), r.stdout.split())}
        # The rule on hand-worked lines: each case is a FILED.md's Public repo lines and the export tags.
        cases = {
            "no tag; the line says it is counted by date": (
                "**Public repo (2026-11-03):** last export 2026-10-31; 61 or 62, counted by date.", []),
            "no tag; the line gives a count and not how": (
                "**Public repo (2026-11-03):** last export 2026-10-31; 61 or 62.", []),
            "one tag; the line names it": (
                "**Public repo (2026-11-05):** last export `export/2026-11-05`; 3 commits since.",
                ["export/2026-11-05"]),
            "a second export that day; the line names the first": (
                "**Public repo (2026-11-05):** last export `export/2026-11-05`; 1 commit since.",
                ["export/2026-11-05-2", "export/2026-11-05"]),
            "two lines; the newer names no tag": (
                "**Public repo (2026-11-05):** last export `export/2026-11-05`; 1 commit since.\n\n"
                "**Public repo (2026-11-06):** 4 commits since the last export.",
                ["export/2026-11-05"]),
            "a tag not in WORKFLOW.md's form": (
                "**Public repo (2026-11-05):** last export `export/latest`.", ["export/latest"]),
        }
        got.update({name: lag_line_problem(text, tags) for name, (text, tags) in cases.items()})
        # Expected, by hand. This repo: nothing wrong; it has no export tag yet, so its one line
        # must say "counted by date". The cases, in order: 1, nothing; 2, no tag and the words
        # missing; 3, nothing; 4, the latest tag is export/2026-11-05-2, the day's second, and the
        # line names only the first; 5, the latest line is 2026-11-06's, which names no tag;
        # 6, export/latest is neither export/<date> nor export/<date>-<n>.
        expected = {
            "this repo": None,
            "no tag; the line says it is counted by date": None,
            "no tag; the line gives a count and not how":
                "no export tag, and the latest *Public repo* line doesn't say it is counted by date",
            "one tag; the line names it": None,
            "a second export that day; the line names the first":
                "the latest *Public repo* line doesn't name the latest export tag, export/2026-11-05-2",
            "two lines; the newer names no tag":
                "the latest *Public repo* line doesn't name the latest export tag, export/2026-11-05",
            "a tag not in WORKFLOW.md's form":
                "export/latest isn't export/<date> or export/<date>-<n> (WORKFLOW.md, Mirror, tag, export, 4)",
        }
        self.assertEqual(got, expected)

    def test_control_md_stops_a_window_without_dev_control_home(self):
        """testing/CONTROL.md sections 7 and 10 stop each window where DEV_CONTROL_HOME isn't set, the after-session windows included"""
        text = read(CONTROL)
        got = {}
        for name, (section, steps) in WINDOWS.items():
            found = control_steps(text, section)
            self.assertIsNotNone(found, f"testing/CONTROL.md has no section {section} with a powershell block")
            lines = [line for step in steps for line in found.get(step, [])]
            filled = [line for line in lines if line.strip()]
            got[name] = (filled[0], filled[-1]) if filled else None
        # Expected, by hand: each window's first line is the guard, whose throw stops the window
        # and whose else { holds the rest, and its last line is the lone } that closes it.
        expected = {name: (GUARD, "}") for name in WINDOWS}
        self.assertEqual(got, expected)
