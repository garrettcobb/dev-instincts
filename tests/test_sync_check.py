"""tools/sync-check.sh against a scratch HOME (Garrett, Task 6, 2026-11-02).

The script finds the installed agents in $HOME/.claude/agents/ and the repo through
DEV_INSTINCTS_HOME, so HOME points at a scratch folder holding copies of agent/*.md.
The real ~/.claude/agents is never read or written.
"""

import os
import shutil
import unittest

from support import ROOT, run, scratch

AGENTS = ("instinct-reviewer", "dev-architect", "senior-coder")  # what agent/sync-agents.ps1 installs
SCRIPT = os.path.join(ROOT, "tools", "sync-check.sh")


class SyncCheck(unittest.TestCase):
    def setUp(self):
        self.sh = shutil.which("sh")
        if not self.sh:
            self.fail("no sh on PATH (run tools/check.sh from Git Bash)")
        self.home = scratch(self)
        self.installed = os.path.join(self.home, ".claude", "agents")
        os.makedirs(self.installed)
        for name in AGENTS:
            shutil.copyfile(os.path.join(ROOT, "agent", f"{name}.md"), os.path.join(self.installed, f"{name}.md"))
        real = os.path.join(os.path.expanduser("~"), ".claude", "agents")
        self.assertNotEqual(os.path.normcase(os.path.abspath(self.installed)), os.path.normcase(os.path.abspath(real)))

    def check(self, name):
        env = dict(os.environ, HOME=self.home.replace(os.sep, "/"), DEV_INSTINCTS_HOME=ROOT)
        r = run([self.sh, SCRIPT, name], env=env)
        return r.returncode, (r.stdout + r.stderr).strip()

    def test_reports_a_mismatch_when_one_byte_differs(self):
        """tools/sync-check.sh reports a mismatch when one byte of an installed agent file differs from agent/"""
        for name in AGENTS:
            path = os.path.join(self.installed, f"{name}.md")
            with open(path, "rb") as f:
                data = bytearray(f.read())
            original = bytes(data)
            data[len(data) // 2] ^= 0x01  # one byte, one bit
            with open(path, "wb") as f:
                f.write(data)
            code, out = self.check(name)
            with open(path, "wb") as f:
                f.write(original)
            self.assertEqual(code, 1, f"{name}: exit {code} for a changed byte, output {out!r}")
            self.assertIn(f"{name} in ~/.claude/agents/ differs from Dev Instincts agent/{name}.md", out)

    def test_is_silent_when_no_installed_agent_differs(self):
        """tools/sync-check.sh is silent when no installed agent file differs from agent/"""
        for name in AGENTS:
            code, out = self.check(name)
            self.assertEqual((code, out), (0, ""), f"{name}: exit {code}, output {out!r}")
