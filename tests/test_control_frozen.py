"""The control's fixed parts stay fixed (Garrett's instructions of 2026-11-05).

- The hypotheses and measures: testing/CONTROL.md sections 1, 12 (with 12.1 and 12.2) and
  14 were fixed before their data and have not moved (its opening paragraph). Each must hash
  as it stood at c5149da, the last commit before arm B's first run. The SHA-256s below are
  each section's text in `git show c5149da:testing/CONTROL.md`, taken by this file's rule
  and again with sed and sha256sum, on 2026-11-05.
- The reviewer under test: while testing/CONTROL.md section 5.2 reads "Block 1: open.",
  agent/instinct-reviewer.md and DEV-INSTINCTS.md hash as frozen for the five-repo block, as
  they stood at their last change before its first run (aa4e22c and f59b36f), and section
  5.2 quotes both hashes. Once the line reads "Block 1: closed <date>.", the files may change
  and only the line itself is checked.

A section runs from its "## <n>. " heading to the next line that starts "## ", so its
"### " sub-headings stay inside it; section 5.2 runs from its "### 5.2 " heading to the next
heading of two or three #. Files are read as text, so a checkout with CRLF line ends hashes
as the LF one does. Each rule is also checked on hand-worked texts. Nothing here writes a
file or asks git.
"""

import hashlib
import os
import re
import unittest

from support import ROOT, read

CONTROL = os.path.join(ROOT, "testing", "CONTROL.md")

# Each section's SHA-256 at c5149da (2026-11-04), its text with LF line ends: 492, 4,415 and
# 1,602 bytes.
AT_C5149DA = {
    "1": "b297821f464d4cc38018fed1ab131c3ffdfaf3114e2a3a9f6beaa87542ea134d",
    "12": "f240e28a5738334a40fcc443eb125c94c624ff673aa6a8edbca316507502c84c",
    "14": "6a260b461e31b13023669700d11541e53c45c3ec50716a63b16d90b0422450d2",
}
# Frozen for block 1 (testing/CONTROL.md section 5.2): each file's sha256sum at 3d8ee65, where
# it is byte for byte its version at its last change, the commit named.
FROZEN = {
    "agent/instinct-reviewer.md": "7336de52647a3e25efd242aceba139e4cb55d0453b927a3878589c6882badfb2",  # aa4e22c
    "DEV-INSTINCTS.md": "df8ab4d8d44c4cfdbc3492f6330dfe76be3aeeecd80a9fc5994b964a2bf85134",  # f59b36f
}
BLOCK_LINE = re.compile(r"^Block 1: (open|closed \d{4}-\d{2}-\d{2})\.$", re.M)
# The SHA-256 of "abc", FIPS 180-2's published example, and of no bytes at all.
ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def section(text, n):
    """Section n of a CONTROL.md text, from its "## <n>. " heading to the next line starting
    "## ", or to the end; None unless exactly one line starts "## <n>. "."""
    starts = [m.start() for m in re.finditer(r"^## " + re.escape(n) + r"\. ", text, re.M)]
    if len(starts) != 1:
        return None
    nxt = re.compile(r"^## ", re.M).search(text, starts[0] + 1)
    return text[starts[0]:nxt.start() if nxt else len(text)]


def subsection(text, n):
    """Subsection n of a CONTROL.md text, from its "### <n> " heading to the next heading of
    two or three #, or to the end; None unless exactly one line starts "### <n> "."""
    starts = [m.start() for m in re.finditer(r"^### " + re.escape(n) + r" ", text, re.M)]
    if len(starts) != 1:
        return None
    nxt = re.compile(r"^#{2,3} ", re.M).search(text, starts[0] + 1)
    return text[starts[0]:nxt.start() if nxt else len(text)]


def freeze_problems(control, texts, frozen):
    """What breaks block 1's freeze, as {what: why}; empty when nothing does. control is a
    CONTROL.md text, texts each frozen file's text by its path, frozen each one's frozen
    SHA-256. Section 5.2 needs exactly one Block 1 line. While it reads open, a file whose
    text's SHA-256 isn't its frozen one is named with the SHA-256 it has, and a file whose
    frozen SHA-256 section 5.2 doesn't quote is named too; once it reads closed, no file is
    checked."""
    s = subsection(control, "5.2")
    if s is None:
        return {"section 5.2": "testing/CONTROL.md has no section 5.2"}
    states = BLOCK_LINE.findall(s)
    if len(states) != 1:
        return {"section 5.2": f"{len(states)} lines read 'Block 1: open.' or "
                               f"'Block 1: closed <date>.'; it needs one"}
    if states[0] != "open":
        return {}
    problems = {}
    for path, want in frozen.items():
        have = sha256(texts[path])
        if have != want:
            problems[path] = f"sha256 {have}, frozen {want}"
        elif want not in s:
            problems[path] = f"section 5.2 doesn't quote its frozen sha256, {want}"
    return problems


class ControlFrozen(unittest.TestCase):
    maxDiff = None  # a failure shows the whole dict

    def test_control_md_sections_1_12_and_14_hash_as_at_c5149da(self):
        """testing/CONTROL.md sections 1, 12 (with 12.1 and 12.2) and 14 hash as they stood at c5149da, before arm B's first run"""
        text = read(CONTROL)
        found = {n: section(text, n) for n in AT_C5149DA}
        got = {"this repo": {n: (sha256(s) if s is not None else None) for n, s in found.items()}}
        # The rule on a hand-made text: a ### sub-heading stays inside its section, which keeps
        # its last blank line; a section stops at the next ## line; the last runs to the end;
        # "## 1. " is not "## 12. "; a heading found twice, or not at all, gives no section.
        sample = "# T\n\n## 1. One\na\n### 1.1 Sub\nb\n\n## 2. Two\nc\n## 12. Twelve\nd\n"
        got.update({
            "section 1": section(sample, "1"),
            "section 2": section(sample, "2"),
            "section 12, the last": section(sample, "12"),
            "section 2, found twice": section(sample + "## 2. Again\n", "2"),
            "section 14, missing": section(sample, "14"),
        })
        # Expected, by hand: this repo's are the SHA-256s at c5149da, above; the cases are read
        # off the sample's lines.
        expected = {
            "this repo": AT_C5149DA,
            "section 1": "## 1. One\na\n### 1.1 Sub\nb\n\n",
            "section 2": "## 2. Two\nc\n",
            "section 12, the last": "## 12. Twelve\nd\n",
            "section 2, found twice": None,
            "section 14, missing": None,
        }
        self.assertEqual(got, expected)

    def test_the_reviewer_under_test_is_unchanged_while_block_1_is_open(self):
        """while testing/CONTROL.md section 5.2 reads Block 1: open, agent/instinct-reviewer.md and DEV-INSTINCTS.md hash as frozen for the block"""
        texts = {path: read(os.path.join(ROOT, *path.split("/"))) for path in FROZEN}
        got = {"this repo": freeze_problems(read(CONTROL), texts, FROZEN)}

        # The rule on hand-made texts: one frozen file, f.md, frozen as the text "abc".
        def control(line, quote=ABC):
            return f"## 5. A\nx\n\n### 5.1 B\ny\n\n### 5.2 C\nFrozen: f.md, sha256 {quote}.\n\n{line}\n\n## 6. D\nz\n"

        frozen = {"f.md": ABC}
        got.update({
            "open; the file as frozen": freeze_problems(control("Block 1: open."), {"f.md": "abc"}, frozen),
            "open; the file emptied": freeze_problems(control("Block 1: open."), {"f.md": ""}, frozen),
            "closed; the file emptied": freeze_problems(control("Block 1: closed 2027-01-15."), {"f.md": ""}, frozen),
            "open; section 5.2 quotes another sha256": freeze_problems(
                control("Block 1: open.", quote=EMPTY), {"f.md": "abc"}, frozen),
            "no Block 1 line": freeze_problems(control("The block is open."), {"f.md": "abc"}, frozen),
            "closed with no date": freeze_problems(control("Block 1: closed soon."), {"f.md": "abc"}, frozen),
            "two Block 1 lines": freeze_problems(
                control("Block 1: open.\n\nBlock 1: closed 2027-01-15."), {"f.md": "abc"}, frozen),
            "the Block 1 line under section 6": freeze_problems(
                f"## 5. A\nx\n\n### 5.2 C\nFrozen: f.md, sha256 {ABC}.\n\n## 6. D\nBlock 1: open.\n",
                {"f.md": "abc"}, frozen),
            "no section 5.2": freeze_problems("## 5. A\nx\n\n## 6. D\nBlock 1: open.\n", {"f.md": "abc"}, frozen),
        })
        # Expected, by hand: this repo breaks nothing. "abc" hashes to ABC and the empty text to
        # EMPTY (above), so only the emptied file breaks an open block, and nothing a closed one;
        # a section 5.2 quoting EMPTY doesn't quote f.md's frozen ABC; a line that isn't
        # "Block 1: open." or "Block 1: closed <date>." counts as none, as does one outside 5.2.
        none_read = "0 lines read 'Block 1: open.' or 'Block 1: closed <date>.'; it needs one"
        expected = {
            "this repo": {},
            "open; the file as frozen": {},
            "open; the file emptied": {"f.md": f"sha256 {EMPTY}, frozen {ABC}"},
            "closed; the file emptied": {},
            "open; section 5.2 quotes another sha256": {"f.md": f"section 5.2 doesn't quote its frozen sha256, {ABC}"},
            "no Block 1 line": {"section 5.2": none_read},
            "closed with no date": {"section 5.2": none_read},
            "two Block 1 lines": {"section 5.2": "2 lines read 'Block 1: open.' or 'Block 1: closed <date>.'; it needs one"},
            "the Block 1 line under section 6": {"section 5.2": none_read},
            "no section 5.2": {"section 5.2": "testing/CONTROL.md has no section 5.2"},
        }
        self.assertEqual(got, expected)
