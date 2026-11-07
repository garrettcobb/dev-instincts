"""README.md names only files that exist (Garrett, Task 6, 2026-11-02).

Checked: every relative link target, and every name in the Layout block. In the
Layout block a line without indent is a path from the repo root, and an indented
line is a name inside the last folder above it; a placeholder such as
reviews/<project>/ is checked up to the placeholder.
"""

import os
import re
import unittest

from support import ROOT, read

README = os.path.join(ROOT, "README.md")


def link_targets(text):
    """Relative targets of [text](target) links, without their #anchor."""
    out = []
    for target in re.findall(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue  # a URL or an anchor in this file
        out.append(target.split("#", 1)[0])
    return out


def layout_names(case, text):
    section = re.search(r"^## Layout\s*$(.*?)^## ", text, re.M | re.S)
    case.assertIsNotNone(section, "README.md has no '## Layout' section")
    block = re.search(r"^```[^\n]*\n(.*?)^```", section.group(1), re.M | re.S)
    case.assertIsNotNone(block, "README.md's Layout section has no code block")
    names, folder = [], ""
    for line in block.group(1).splitlines():
        if not line.strip():
            continue
        name = line.split()[0]
        if line[0] != " ":
            path, folder = name, (name if name.endswith("/") else "")
        else:
            path = folder + name
        names.append(path.split("<", 1)[0])
    case.assertGreater(len(names), 10, f"read only {len(names)} names from the Layout block")
    return names


def missing(paths):
    """The paths that don't exist; a path ending in / must be a folder."""
    gone = set()
    for p in paths:
        if not p:
            continue
        full = os.path.join(ROOT, *p.rstrip("/").split("/"))
        if not (os.path.isdir(full) if p.endswith("/") else os.path.exists(full)):
            gone.add(p)
    return sorted(gone)


class Readme(unittest.TestCase):
    def test_every_governing_document_in_the_layout_exists(self):
        """every governing document named in README.md's Layout block exists"""
        gone = missing(layout_names(self, read(README)))
        if gone:
            self.fail(f"README.md's Layout names {len(gone)} that don't exist: {gone}")

    def test_every_file_readme_links_to_exists(self):
        """every file README.md links to exists"""
        targets = link_targets(read(README))
        self.assertGreater(len(targets), 10, f"read only {len(targets)} links from README.md")
        gone = missing(targets)
        if gone:
            self.fail(f"README.md links to {len(gone)} that don't exist: {gone}")
