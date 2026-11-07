"""Shared helpers for Dev Instincts' own tests (tests/test_*.py). Standard library only.

Tests read this repo's files but write only inside scratch folders made here, in
the system temp dir, and every scratch folder is removed after its test.
"""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def scratch(case=None):
    """A new folder in the system temp dir, removed after the test (or after the module)."""
    path = tempfile.mkdtemp(prefix="dev-instincts-check-")
    if case is not None:
        case.addCleanup(remove, path)
    else:
        unittest.addModuleCleanup(remove, path)
    return path


def inside(path, folder):
    """True if path is folder or inside it."""
    path, folder = os.path.abspath(path), os.path.abspath(folder)
    return os.path.commonpath([path, folder]) == folder


def remove(path):
    """Remove a scratch folder, read-only files (git objects) included."""
    if not inside(path, tempfile.gettempdir()):
        raise RuntimeError(f"refusing to remove {path}: not in the temp dir")

    def retry(func, p, _):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=retry)
    else:
        shutil.rmtree(path, onerror=retry)


def run(args, **kw):
    """Run a command and capture its output as text."""
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)


def repo_files():
    """This repo's files as git would publish them: tracked, plus untracked ones not ignored."""
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z", "--cached", "--others",
                          "--exclude-standard"], capture_output=True, check=True).stdout
    names = sorted({n for n in out.decode("utf-8").split("\0") if n})
    return [n for n in names if os.path.isfile(os.path.join(ROOT, *n.split("/")))]


def copy_into(folder, names):
    """Copy repo-relative files into folder, keeping their paths."""
    for n in names:
        dst = os.path.join(folder, *n.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, *n.split("/")), dst)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
