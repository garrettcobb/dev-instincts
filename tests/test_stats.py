"""tools/stats.py regenerates ledger/STATS.md to a clean git tree (Garrett, Task 6, 2026-11-02),
under both line-ending settings, core.autocrlf true and false (Garrett, 2026-11-03).

stats.py writes beside itself (ROOT = its folder's parent), so the test runs a copy
in a scratch git repo holding the files stats.py opens, as they are in this repo now.
Each setting gets a scratch repo of its own and is set on each git command line
(git -c), so no real repo's config is read or written. Under true, git converts line
endings when it adds and compares, so it would hide a stats.py that writes CRLF;
under false, that shows as a changed file.
"""

import os
import unittest

from support import PY, copy_into, run, scratch

# What tools/stats.py opens: its four inputs (testing/CONTROL.md for the block
# state line, since 2026-11-06) and its output.
FILES = ("tools/stats.py", "ledger/findings.jsonl", "ledger/projects.json", "DEV-INSTINCTS.md",
         "testing/CONTROL.md", "ledger/STATS.md")


class StatsTool(unittest.TestCase):
    def regenerate(self, autocrlf):
        """stats.py in a scratch repo under one core.autocrlf setting: the files it changed and made, or why it failed."""
        work = scratch(self)
        copy_into(work, FILES)
        git = ["git", "-c", f"core.autocrlf={autocrlf}", "-c", "core.safecrlf=false", "-C", work]
        for args in (["init", "-q"], ["add", "-A"]):
            r = run(git + args)
            if r.returncode != 0:
                return f"git {' '.join(args)} in the scratch repo failed: {r.stderr.strip()}"
        r = run([PY, "-I", os.path.join(work, "tools", "stats.py")], cwd=work)
        if r.returncode != 0:
            return f"stats.py failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-800:]}"
        return {"changed": run(git + ["diff", "--name-only"]).stdout.split(),
                "new": run(git + ["ls-files", "--others", "--exclude-standard"]).stdout.split()}

    def test_stats_regenerates_stats_md_to_a_clean_git_tree(self):
        """tools/stats.py regenerates ledger/STATS.md to a clean git tree, under core.autocrlf true and under false"""
        got = {setting: self.regenerate(setting) for setting in ("true", "false")}
        # Expected, by hand: under each setting, no file changed and no file new.
        expected = {"true": {"changed": [], "new": []}, "false": {"changed": [], "new": []}}
        self.assertEqual(got, expected,
                         "stats.py changed the tree under a line-ending setting: ledger/STATS.md isn't what the "
                         "ledger generates (run python -I tools/stats.py and commit), or stats.py writes line "
                         "endings git doesn't keep")
