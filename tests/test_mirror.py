"""tools/mirror.sh on scratch repos (Garrett, Task 4, 2026-11-03): one fixed name per
repo, <folder name>.bundle, written under a temporary name, verified, then renamed over
the old one; the old one is never removed before the new one verifies. A bundle also
holds the repo's tags, the copy SYNC.md's round tag and export tag rows name (Garrett,
tool task 5, 2026-11-03: SYNC's unchecked rows get checks).

mirror.sh mirrors the repo it sits in (its folder's parent) and the work folder beside
it (that folder's path plus "-work"). So each test commits a copy of this repo's
tools/mirror.sh into a scratch repo, instincts/, beside a scratch repo,
instincts-work/, and gives mirror.sh a scratch mirrors folder as its TARGET. HOME
points into the scratch folder too, so the default target (~/dev/mirrors) and git's
user settings are never the real ones, and GIT_CONFIG_NOSYSTEM keeps the system's
settings out. The real mirrors folder is never read or written.

A bundle that fails git bundle verify is made by a stand-in for git, put first on
PATH: it runs git, then writes over the file each "bundle create" made.
"""

import hashlib
import os
import shutil
import unittest

from support import ROOT, run, scratch

SCRIPT = os.path.join(ROOT, "tools", "mirror.sh")
NAME = "instincts"  # the scratch repo's folder name; the work folder's is NAME + "-work"

# The stand-in for git, a shell script: the real git, then the file "bundle create" wrote is overwritten.
STAND_IN = """#!/bin/sh
"$REAL_GIT" "$@" || exit
prev= take= file=
for a in "$@"; do
    if [ -n "$take" ] && [ -z "$file" ]; then
        case $a in -*) ;; *) file=$a ;; esac
    fi
    [ "$prev $a" = "bundle create" ] && take=1
    prev=$a
done
[ -z "$file" ] || echo "not a bundle" > "$file"
"""


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Mirror(unittest.TestCase):
    def setUp(self):
        self.sh, self.git = shutil.which("sh"), shutil.which("git")
        if not (self.sh and self.git):
            self.fail("no sh or git on PATH (run tools/check.sh from Git Bash)")
        self.base = scratch(self)
        self.home, self.target = os.path.join(self.base, "home"), os.path.join(self.base, "mirrors")
        os.makedirs(self.home)
        os.makedirs(self.target)
        self.env = dict(os.environ, HOME=self.home.replace(os.sep, "/"), GIT_CONFIG_NOSYSTEM="1")
        # In mirror.sh's order: the repo it sits in, then the work folder.
        self.repos = {NAME: os.path.join(self.base, NAME), NAME + "-work": os.path.join(self.base, NAME + "-work")}
        for path in self.repos.values():
            r = run([self.git, "init", "-q", "-b", "main", path], env=self.env)
            self.assertEqual(r.returncode, 0, f"git init {path} failed. {r.stderr.strip()}")
        os.makedirs(os.path.join(self.repos[NAME], "tools"))
        shutil.copyfile(SCRIPT, os.path.join(self.repos[NAME], "tools", "mirror.sh"))
        self.heads = {name: self.commit(name, f"{name}, first commit") for name in self.repos}

    def git_in(self, repo, *args):
        r = run([self.git, "-C", repo, "-c", "user.name=Mirror test", "-c", "user.email=mirror-test", *args],
                env=self.env)
        self.assertEqual(r.returncode, 0, f"git {' '.join(args)} in {os.path.basename(repo)} failed. {r.stderr.strip()}")
        return r.stdout.strip()

    def commit(self, name, text):
        """A new commit in one scratch repo: a line added to notes.txt. Its sha."""
        repo = self.repos[name]
        with open(os.path.join(repo, "notes.txt"), "a", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
        self.git_in(repo, "add", "-A")
        self.git_in(repo, "commit", "-q", "-m", text)
        return self.git_in(repo, "rev-parse", "HEAD")

    def mirror(self, stand_in=False):
        """sh tools/mirror.sh <scratch mirrors folder>, from the scratch repo's copy: its exit code and output."""
        env = dict(self.env)
        if stand_in:
            folder = os.path.join(self.base, "bin")
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "git"), "w", encoding="utf-8", newline="\n") as f:
                f.write(STAND_IN)
            env["REAL_GIT"] = self.git.replace(os.sep, "/")
            env["PATH"] = folder + os.pathsep + env["PATH"]
        r = run([self.sh, os.path.join(self.repos[NAME], "tools", "mirror.sh"), self.target], env=env)
        return r.returncode, (r.stdout + r.stderr).strip()

    def listing(self):
        return sorted(os.listdir(self.target))

    def held(self):
        """The HEAD each repo's <folder name>.bundle holds (git bundle list-heads), or None with no such file."""
        heads = {}
        for name in self.repos:
            path = os.path.join(self.target, name + ".bundle")
            out = self.git_in(self.repos[NAME], "bundle", "list-heads", path) if os.path.isfile(path) else ""
            found = [line.split()[0] for line in out.splitlines() if line.split()[1:] == ["HEAD"]]
            heads[name] = found[0] if found else None
        return heads

    def test_writes_one_bundle_per_repo_named_for_its_folder(self):
        """tools/mirror.sh writes one bundle per repo, named for its folder: instincts.bundle and instincts-work.bundle"""
        code, out = self.mirror()
        got = {"exit": code, "files": self.listing(), "held": self.held(),
               "lines": [line for line in out.splitlines() if " HEAD " in line]}
        # Expected, by hand: exit 0, and the mirrors folder holds each folder's name plus ".bundle",
        # sorted "instincts-work.bundle" then "instincts.bundle" (a hyphen sorts before a full stop),
        # and nothing else: no date in a name, no temporary file left. Each bundle holds its repo's
        # HEAD, and the run prints it beside the repo's, the repo it sits in first.
        expected = {"exit": 0, "files": ["instincts-work.bundle", "instincts.bundle"], "held": self.heads,
                    "lines": [f"{name} HEAD {self.heads[name]}  bundle HEAD {self.heads[name]}  verified"
                              for name in self.repos]}
        self.assertEqual(got, expected, out)

    def test_a_second_run_replaces_each_bundle(self):
        """a second tools/mirror.sh run replaces each repo's bundle with one that holds its new HEAD, under the same name"""
        code, out = self.mirror()
        self.assertEqual(code, 0, out)
        new = {name: self.commit(name, f"{name}, second commit") for name in self.repos}
        self.assertNotEqual(new, self.heads)
        code, out = self.mirror()
        got = {"exit": code, "files": self.listing(), "held": self.held()}
        # Expected, by hand: exit 0; the same two names and nothing else; each bundle now holds its
        # repo's second commit, not the one the first run took.
        expected = {"exit": 0, "files": ["instincts-work.bundle", "instincts.bundle"], "held": new}
        self.assertEqual(got, expected, out)

    def test_a_bundle_that_fails_to_verify_leaves_the_old_one_untouched(self):
        """when a new bundle fails git bundle verify, tools/mirror.sh exits 1 and every old bundle is still there, byte for byte"""
        code, out = self.mirror()
        self.assertEqual(code, 0, out)
        before = {f: sha256(os.path.join(self.target, f)) for f in self.listing()}
        for name in self.repos:
            self.commit(name, f"{name}, second commit")
        code, out = self.mirror(stand_in=True)
        after = {f: sha256(os.path.join(self.target, f)) for f in self.listing()}
        # Expected, by hand: the stand-in writes over both new bundles, so both fail git bundle
        # verify: exit 1, and one "FAILED: git bundle verify" per repo, 2 in all. The mirrors folder
        # then holds what the first run left, the same names with the same bytes, and nothing more.
        self.assertEqual((code, out.count("FAILED: git bundle verify")), (1, 2), out)
        self.assertEqual(after, before, "the mirrors folder changed: an old bundle was written over or removed "
                                        "before its new one verified, or a temporary file was left. " + out)

    def test_each_bundle_holds_the_repos_tags(self):
        """a bundle tools/mirror.sh writes holds its repo's round/ and export/ tags, each on the commit it tags"""
        repo = self.repos[NAME]
        first, second = self.heads[NAME], self.commit(NAME, f"{NAME}, second commit")
        self.git_in(repo, "tag", "round/2026-11-03-example", first)
        self.git_in(repo, "tag", "export/2026-11-03", second)
        code, out = self.mirror()
        self.assertEqual(code, 0, out)
        listed = self.git_in(repo, "bundle", "list-heads", os.path.join(self.target, NAME + ".bundle"))
        tags = {ref: sha for sha, ref in (line.split() for line in listed.splitlines()) if ref.startswith("refs/tags/")}
        # Expected, by hand: the two tags made above and no other, the round tag on the first
        # commit and the export tag on the second. WORKFLOW.md's commands make lightweight tags,
        # so the bundle lists each with its commit's sha.
        self.assertEqual(tags, {"refs/tags/round/2026-11-03-example": first, "refs/tags/export/2026-11-03": second}, out)
