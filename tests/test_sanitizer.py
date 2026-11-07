"""The export sanitizer: sanitize.py, then scan.py (Garrett, Task 6, 2026-11-02), and
sanitize.py's one-file mode, sanitize.py --file <in> <out> (Garrett, 2026-11-03).

The export tools live outside this repo, where EXPORT below looks for them;
DEV_INSTINCTS_EXPORT overrides it. They only ever run on scratch copies here,
never on a real repo.

Like the export, the flow copies the repo (as git would publish it), adds the test's
files, runs sanitize.py into a fresh output folder, then runs scan.py with an empty
exceptions file. The planted files and their clean twins are scanned on their own,
apart from the rest of the output, so the result is about them alone.

The one-file mode runs on a dummy transcript (.jsonl) and a dummy plain text file in
scratch folders, and each output is scanned in a folder of its own. Their paths are
this PC's: the projects folder (the folder holding the work folder, as sanitize.py
takes it), the user's folder, and a made-up path on another drive.

Nothing private is spelled in this file, or the export scan would flag it: the
names are the plain-word names scan.py itself lists (the organization's among
them), and the paths and the address are built when the test runs. A failure
message puts them back as words ([projects], [home], [user], [email], [name]).

Six more tests (Garrett, 2026-11-03, the last pass of the tool task) cover the values of
Claude Code's accountUuid and organizationUuid keys, which become <account> and
<organization>, and the repeatable --private <text>, which replaces each given text with
<private>. Their ids, handle and second text are made up: Claude Code's real ids are never
written here.

The folder mode, sanitize.py <src> <dst>, gets two more tests (Garrett, 2026-11-03),
each on a scratch copy of this repo's tracked files (git ls-files, as they are in the
working tree): with a planted .instinct-scratch/, which it must not copy; and as it
is, scanned with the real exceptions file beside scan.py, which must give 0 hits. A
third (Garrett, 2026-11-04) plants files whose names hold .private., which it must
not copy, beside their public twins, which it must.

Five more (Garrett, 2026-11-06). Three share one run of the folder mode on a scratch copy
of the tracked files with planted files beside them, given --private twice, as export.sh
passes each line of the work folder's export/private-texts.txt: each text becomes
<private> in any case; Git Bash's form of the projects folder and of its parent (the
folder holding it) becomes <projects>; and no file gains a CR its source didn't have. The
fourth checks that the folder mode refuses an empty --private text before it deletes
anything; the fifth, that scan.py, given a file of private texts, reports each in any
case by its number and never prints it. The two texts are made up and joined only when
the tests run, so this file never holds either whole.
"""

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import unittest

from support import PY, ROOT, copy_into, inside, read, repo_files, run, scratch, write

EXPORT = os.environ.get("DEV_INSTINCTS_EXPORT") or os.path.join(
    os.path.dirname(ROOT), os.path.basename(ROOT) + "-work", "export")
BS = chr(92)  # a backslash
PATH = "C:" + BS + BS.join(["Users", "example-user", "Documents", "notes.txt"])
EMAIL = "example.user" + chr(64) + "example.org"  # example.org is reserved for examples (RFC 2606)
KINDS = ("names", "path", "email")

# The one-file mode's folders, as sanitize.py takes them: the projects folder holds the
# work folder (EXPORT's grandparent); the user's folder is the home folder.
PROJECTS = os.path.dirname(os.path.dirname(os.path.abspath(EXPORT)))
HOME = os.path.expanduser("~")
OTHER = "D:" + BS + BS.join(["example-data", "notes.txt"])  # a made-up path on another drive


def listed_names():
    """The plain-word, any-case names in scan.py's PATTERNS: '(?i)word' gives 'word'."""
    tree = ast.parse(read(os.path.join(EXPORT, "scan.py")))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "PATTERNS" for t in node.targets):
            return [p[4:] for p in ast.literal_eval(node.value) if re.fullmatch(r"\(\?i\)[a-z][a-z-]*", p)]
    return []


def planted_files():
    """Per kind: (value, planted line, clean twin), the twin being the same line without the value."""
    return {
        "names": [(n, f"Prepared for {n.capitalize()}, 2026-10-31.", "Prepared for the team, 2026-10-31.")
                  for n in listed_names()],
        "path": [(PATH, f"The notes are in {PATH}.", "The notes are in ledger/README.md.")],
        "email": [(EMAIL, f"Questions go to {EMAIL}.", "Questions go to the project's issue tracker.")],
    }


_flow = {}


def flow():
    """Run the export's two steps once for all four tests; each test reads its part."""
    if not _flow:
        try:
            _flow.update(_run_flow())
        except Exception as e:  # every test reports it, rather than one setUp error
            _flow["error"] = f"{type(e).__name__}: {e}"
    return _flow


def _run_flow():
    for tool in ("sanitize.py", "scan.py"):
        if not os.path.isfile(os.path.join(EXPORT, tool)):
            raise FileNotFoundError(f"no {tool} in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
    if not listed_names():
        raise ValueError("found no plain-word names in scan.py's PATTERNS")
    work = scratch()
    src, out = os.path.join(work, "src"), os.path.join(work, "out")
    copy_into(src, repo_files())
    for kind, entries in planted_files().items():
        write(os.path.join(src, f"planted-{kind}.md"), "".join(p + "\n" for _, p, _ in entries))
        write(os.path.join(src, f"clean-{kind}.md"), "".join(c + "\n" for _, _, c in entries))
    # sanitize.py deletes its output folder first: it must be this test's own.
    if not inside(out, work) or os.path.exists(out):
        raise RuntimeError(f"unsafe output folder {out}")
    r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), src, out], cwd=work)
    if r.returncode != 0 or "done" not in r.stdout:
        raise RuntimeError(f"sanitize.py failed (exit {r.returncode}):\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
    empty = os.path.join(work, "empty.exceptions")
    write(empty, "")
    result = {"out": out}
    for which in ("planted", "clean"):
        folder = os.path.join(work, f"scan-{which}")
        os.makedirs(folder)
        for kind in KINDS:
            shutil.copy2(os.path.join(out, f"{which}-{kind}.md"), folder)
        s = run([PY, "-I", os.path.join(EXPORT, "scan.py"), folder, empty], cwd=work)
        result[which] = (s.returncode, s.stdout, s.stderr)
    return result


class Sanitizer(unittest.TestCase):
    def missed(self, kind):
        """Planted lines still holding their value after sanitize.py that scan.py didn't report."""
        f = flow()
        if "error" in f:
            self.fail(f["error"])
        name = f"planted-{kind}.md"
        out_lines = read(os.path.join(f["out"], name)).splitlines()
        hits = {int(n) for n in re.findall(rf"^HIT {re.escape(name)}:(\d+):", f["planted"][1], re.M)}
        missed = []
        for value, _, _ in planted_files()[kind]:
            missed += [n for n, text in enumerate(out_lines, 1) if value.lower() in text.lower() and n not in hits]
        return name, out_lines, missed

    def test_finds_a_planted_organization_name(self):
        """the sanitizer finds a planted organization name in a scratch copy"""
        name, _, missed = self.missed("names")
        if missed:  # the names aren't printed: they are the private ones
            self.fail(f"scan.py reported nothing on {name} lines {missed}, each a name scan.py lists, "
                      "still in sanitize.py's output")

    def test_finds_a_planted_personal_path(self):
        """the sanitizer finds a planted personal path in a scratch copy"""
        name, lines, missed = self.missed("path")
        for n in missed:
            self.fail(f"scan.py reported nothing on {name} line {n}, {lines[n - 1]!r}; "
                      "sanitize.py left it in the export")

    def test_finds_a_planted_email(self):
        """the sanitizer finds a planted email in a scratch copy"""
        name, lines, missed = self.missed("email")
        for n in missed:
            self.fail(f"scan.py reported nothing on {name} line {n}, {lines[n - 1]!r}; "
                      "sanitize.py left it in the export")

    def test_passes_a_clean_copy_with_0_hits(self):
        """the sanitizer passes a clean copy with 0 hits"""
        f = flow()
        if "error" in f:
            self.fail(f["error"])
        code, out, err = f["clean"]
        last = out.strip().splitlines()[-1] if out.strip() else err.strip()
        self.assertEqual((code, last), (0, "0 hits, 0 stale exceptions"),
                         f"scan.py on the clean twins: exit {code}, {last!r}")


# The one-file mode (Garrett, 2026-11-03).

def forms(path):
    """A Windows path in Garrett's three forms: one backslash, the JSON-escaped two, forward slashes."""
    return path, path.replace(BS, BS * 2), path.replace(BS, "/")


def git_bash(path):
    """Git Bash's form of a Windows path: a slash, the drive letter in lower case, then forward slashes."""
    return "/" + path[0].lower() + path[2:].replace(BS, "/")


def slug(path):
    """Claude Code's name for a session folder under .claude/projects: every character not a letter or digit becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def mask(text):
    """A failure message with the private values this file builds put back as words."""
    words = [(EMAIL, "[email]")] + [(n, "[name]") for n in listed_names()]
    for path, word in ((PROJECTS, "[projects]"), (HOME, "[home]")):
        words += [(f, word) for f in (*forms(path), path.replace(BS, BS * 4), git_bash(path), slug(path))]
    words.append((os.path.basename(HOME), "[user]"))
    for value, word in sorted(words, key=lambda vw: -len(vw[0])):
        text = re.sub(re.escape(value), word, text, flags=re.I)
    return text


def compact(value):
    """A line as Claude Code writes its transcripts: compact JSON, non-ASCII kept as it is."""
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def jsonl_dummy():
    """The dummy transcript: (raw line, the JSON value expected after the scrub) per line.

    Each expected value is worked out by hand from Garrett's rules for --file: the
    projects folder becomes <projects> and the user's folder <home>, the rest of the
    path staying; any other drive path becomes <path>; an email <email>; and each hit
    of scan.py's patterns <private>.
    """
    p1, p2, p3 = forms(PROJECTS)
    h1, h2, h3 = forms(HOME)
    o1, o2, o3 = forms(OTHER)
    names = listed_names()
    steps = {"type": "assistant", "message": {"id": "msg_4", "role": "assistant", "content": [
        {"type": "text", "text": "Steps:" + chr(10) + "Expected: one row"}]}}
    decorator = {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "tu_5",
         "content": "import pytest" + chr(10) + "@pytest.fixture" + chr(10) + "def row():"}]}}
    clean = {"type": "user", "timestamp": "2026-11-02T18:00:00.000Z", "message": {"role": "user", "content":
             "Read src" + BS + "app.ts, then https://example.com/a/b at 18:05, caf" + chr(0xE9) + "."}}
    pairs = [
        # 1. The projects folder in the three forms: <projects> takes its place, the rest stays.
        ({"type": "system", "cwd": p1 + BS + "dev-control",
          "content": p2 + BS * 2 + "dev-instincts; " + p3 + "/dev-control/monize/repo"},
         {"type": "system", "cwd": "<projects>" + BS + "dev-control",
          "content": "<projects>" + BS * 2 + "dev-instincts; <projects>/dev-control/monize/repo"}),
        # 2. The user's folder in the three forms, in a tool result.
        ({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tu_1",
             "content": h1 + BS + ".claude" + BS + "settings.json, " + h2 + BS * 2 + ".claude, "
             + h3 + "/.claude/agents"}]}},
         {"type": "user", "message": {"role": "user", "content": [
             {"type": "tool_result", "tool_use_id": "tu_1",
              "content": "<home>" + BS + ".claude" + BS + "settings.json, <home>" + BS * 2 + ".claude, "
              "<home>/.claude/agents"}]}}),
        # 3. A path on another drive in the three forms: the whole path goes, a full stop after it stays.
        ({"type": "assistant", "message": {"id": "msg_1", "role": "assistant", "content": [
            {"type": "tool_use", "id": "tu_2", "name": "Read", "input": {"file_path": o1}},
            {"type": "text", "text": "Also " + o2 + " and " + o3 + "."}]}},
         {"type": "assistant", "message": {"id": "msg_1", "role": "assistant", "content": [
             {"type": "tool_use", "id": "tu_2", "name": "Read", "input": {"file_path": "<path>"}},
             {"type": "text", "text": "Also <path> and <path>."}]}}),
        # 4. Both folders in Git Bash's form, in a Bash command (the architect's addition, 2026-11-03).
        ({"type": "assistant", "message": {"id": "msg_2", "role": "assistant", "content": [
            {"type": "tool_use", "id": "tu_3", "name": "Bash", "input": {
                "command": "cd " + git_bash(PROJECTS) + "/dev-control && ls " + git_bash(HOME) + "/.claude/agents"}}]}},
         {"type": "assistant", "message": {"id": "msg_2", "role": "assistant", "content": [
             {"type": "tool_use", "id": "tu_3", "name": "Bash", "input": {
                 "command": "cd <projects>/dev-control && ls <home>/.claude/agents"}}]}}),
        # 5. Both folders as Claude Code names a session folder (the architect's addition, 2026-11-03).
        ({"type": "attachment", "attachment": {"type": "nested_memory", "path": h1 + BS + BS.join(
            [".claude", "projects", slug(p1 + BS + "dev-instincts"), "memory", "MEMORY.md"]), "folder": slug(HOME)}},
         {"type": "attachment", "attachment": {"type": "nested_memory", "path": "<home>" + BS + BS.join(
             [".claude", "projects", "<projects>-dev-instincts", "memory", "MEMORY.md"]), "folder": "<home>"}}),
        # 6. An email.
        ({"type": "user", "message": {"role": "user", "content": "Questions go to " + EMAIL + "."}},
         {"type": "user", "message": {"role": "user", "content": "Questions go to <email>."}}),
        # 7. Each plain-word name scan.py lists, the organization's among them.
        ({"type": "assistant", "message": {"id": "msg_3", "role": "assistant", "content": [
            {"type": "text", "text": "Prepared for " + ", ".join(n.capitalize() for n in names) + "."}]}},
         {"type": "assistant", "message": {"id": "msg_3", "role": "assistant", "content": [
             {"type": "text", "text": "Prepared for " + ", ".join("<private>" for _ in names) + "."}]}}),
        # 8. Nothing private. "Steps:" then a line break, which the raw line writes as a backslash
        #    and an n, so scan.py reads a letter, a colon and a backslash there; the value stays
        #    (test 3 checks the raw line).
        (steps, steps),
        # 9. Code holding a colon before a literal backslash: a hit of scan.py's drive pattern, so
        #    <private> takes the letter, the colon and the backslash (Garrett's rule: every hit).
        ({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tu_4", "content": 'print("run again:' + BS + 'n")'}]}},
         {"type": "user", "message": {"role": "user", "content": [
             {"type": "tool_result", "tool_use_id": "tu_4", "content": 'print("run agai<private>n")'}]}}),
        # 10. Nothing private. Code with a decorator at the start of a line: the raw line writes the
        #     line break as a backslash and an n, and that n, an at sign and the decorator's dotted
        #     name read as an email to scan.py; the value stays (test 3 checks the raw line).
        (decorator, decorator),
        # 11. Nothing private.
        (clean, clean),
    ]
    lines = [(compact(a), b) for a, b in pairs]
    # Line 11 is in json.dumps's default form (spaces, the accented letter escaped), so a line
    # written again instead of kept would show.
    lines[10] = (json.dumps(clean), clean)
    return lines


def txt_dummy():
    """The dummy plain text file: (line, the line expected after the scrub, worked by hand)."""
    p1, p2, p3 = forms(PROJECTS)
    h1, h2, h3 = forms(HOME)
    o1, o2, o3 = forms(OTHER)
    names = listed_names()
    clean = "Read src" + BS + "app.ts, then https://example.com/a/b at 18:05."
    return [
        ("cwd " + p1 + BS + "dev-control; " + p2 + BS * 2 + "dev-instincts; " + p3 + "/dev-control/monize/repo",
         "cwd <projects>" + BS + "dev-control; <projects>" + BS * 2 + "dev-instincts; <projects>/dev-control/monize/repo"),
        ("home " + h1 + BS + ".claude" + BS + "settings.json, " + h2 + BS * 2 + ".claude, " + h3 + "/.claude/agents",
         "home <home>" + BS + ".claude" + BS + "settings.json, <home>" + BS * 2 + ".claude, <home>/.claude/agents"),
        ("Also " + o1 + ", " + o2 + " and " + o3 + ".", "Also <path>, <path> and <path>."),
        ("cd " + git_bash(PROJECTS) + "/dev-control && ls " + git_bash(HOME) + "/.claude/agents",
         "cd <projects>/dev-control && ls <home>/.claude/agents"),
        (h1 + BS + BS.join([".claude", "projects", slug(p1 + BS + "dev-instincts")]) + " and " + slug(HOME),
         "<home>" + BS + BS.join([".claude", "projects", "<projects>-dev-instincts"]) + " and <home>"),
        ("Questions go to " + EMAIL + ".", "Questions go to <email>."),
        ("Prepared for " + ", ".join(n.capitalize() for n in names) + ".",
         "Prepared for " + ", ".join("<private>" for _ in names) + "."),
        ('print("run again:' + BS + 'n")', 'print("run agai<private>n")'),
        (clean, clean),
    ]


def tools():
    for tool in ("sanitize.py", "scan.py"):
        if not os.path.isfile(os.path.join(EXPORT, tool)):
            raise FileNotFoundError(f"no {tool} in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
    if not listed_names():
        raise ValueError("found no plain-word names in scan.py's PATTERNS")
    for name, path in (("projects folder", PROJECTS), ("user's folder", HOME)):
        if not re.match(r"[A-Za-z]:" + re.escape(BS) + r"[^" + re.escape(BS) + r"]", path):
            raise ValueError(f"these tests expect a Windows path with a drive for the {name}")


def scan_lines(result, name):
    """The line numbers scan.py reported in a file."""
    return sorted({int(n) for n in re.findall(rf"^HIT {re.escape(name)}:(\d+):", result.stdout, re.M)})


def last_line(result):
    out = result.stdout.strip()
    return out.splitlines()[-1] if out else result.stderr.strip()[-300:]


_one = {}


def one_file():
    """Run sanitize.py --file once on each dummy, the .jsonl and the .txt; each test reads its part."""
    if not _one:
        try:
            _one.update(_run_one_file())
        except Exception as e:  # every test reports it, rather than one setUp error
            _one["error"] = mask(f"{type(e).__name__}: {e}")
    return _one


def _run_one_file():
    tools()
    work = scratch()
    empty = os.path.join(work, "empty.exceptions")
    write(empty, "")
    result = {}
    for kind, dummy in (("jsonl", jsonl_dummy()), ("txt", txt_dummy())):
        name = f"transcript.{kind}"
        src_dir, out_dir = os.path.join(work, f"in-{kind}"), os.path.join(work, f"out-{kind}")
        src, out = os.path.join(src_dir, name), os.path.join(out_dir, name)
        write(src, "".join(line + "\n" for line, _ in dummy))
        os.makedirs(out_dir)
        r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), "--file", src, out], cwd=work)
        before = run([PY, "-I", os.path.join(EXPORT, "scan.py"), src_dir, empty], cwd=work)
        after = run([PY, "-I", os.path.join(EXPORT, "scan.py"), out_dir, empty], cwd=work)
        text = None
        if os.path.isfile(out):
            with open(out, encoding="utf-8", newline="") as f:
                text = f.read()
        result[kind] = {"name": name, "dummy": dummy, "run": r, "before": before, "after": after, "text": text}
    return result


class OneFile(unittest.TestCase):
    def output(self, kind):
        """sanitize.py --file's output for one dummy, split on line breaks, or the test fails."""
        f = one_file()
        if "error" in f:
            self.fail(f["error"])
        part = f[kind]
        r = part["run"]
        if r.returncode != 0 or part["text"] is None:
            self.fail(mask(f"sanitize.py --file on the dummy {kind}: exit {r.returncode}, no output written.\n"
                           f"{(r.stdout + r.stderr).strip()[-800:]}"))
        return part, part["text"].split("\n")

    def test_file_mode_scrubs_a_dummy_jsonl_to_0_hits(self):
        """sanitize.py --file scrubs a dummy .jsonl's planted paths, email and organization names to 0 hits under scan.py"""
        part, lines = self.output("jsonl")
        # Before, worked by hand from scan.py's patterns: lines 1 to 10 each hold a hit (a drive path
        # with a backslash, the users folder in Git Bash's form, an email or what reads as one, a
        # listed name, or a letter, a colon and a backslash); line 11 holds none. Line 1's forward
        # slashes, line 4's projects folder and line 5's session folder names are forms scan.py can't
        # see: only their expected values below show they were scrubbed.
        self.assertEqual(scan_lines(part["before"], part["name"]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         mask("scan.py's hits on the dummy before the scrub, below.\n" + part["before"].stdout[-1500:]))
        # After: no hit, no exception to go stale.
        self.assertEqual((part["after"].returncode, last_line(part["after"])), (0, "0 hits, 0 stale exceptions"),
                         mask("scan.py on the scrubbed .jsonl, below.\n" + part["after"].stdout[-1500:]))
        # Each line's value is the one worked out by hand in jsonl_dummy().
        wrong = []
        for n, (_, expected) in enumerate(part["dummy"], 1):
            try:
                got = json.loads(lines[n - 1])
            except (IndexError, ValueError) as e:
                got = f"not JSON ({e})"
            if got != expected:
                wrong.append(f"line {n}: got {got!r}, expected {expected!r}")
        if wrong:
            self.fail(mask("\n".join(wrong)))

    def test_file_mode_keeps_every_jsonl_line_parseable(self):
        """sanitize.py --file writes a .jsonl whose every line still parses as JSON"""
        _, lines = self.output("jsonl")
        # Eleven lines in, eleven out, each ending in a line break, so the split gives eleven and an empty last.
        self.assertEqual((len(lines), lines[-1]), (12, ""), f"{len(lines) - 1} lines out, not 11, or no final line break")
        broken = []
        for n, line in enumerate(lines[:-1], 1):
            try:
                json.loads(line)
            except ValueError as e:
                broken.append(f"line {n}: {e}")
        self.assertEqual(broken, [], "lines that no longer parse as JSON")

    def test_file_mode_leaves_a_line_with_nothing_private_unchanged(self):
        """sanitize.py --file leaves a .jsonl line with nothing private unchanged"""
        part, lines = self.output("jsonl")
        raw = [line for line, _ in part["dummy"]]
        # Line 11 holds nothing private and nothing scan.py reads as private: the same bytes come out.
        self.assertEqual(lines[10], raw[10], "line 11, with nothing private, came out changed")
        # Lines 8 and 10 hold nothing private, but their raw forms have what scan.py reads as private,
        # made by the backslash and n of a line break. Worked by hand: the same bytes but one character
        # written as its JSON escape, the same value.
        # Line 8: "Steps", a colon, then the line break's backslash and n: the colon becomes backslash u003a.
        # Line 10: the line break's backslash and n, then an at sign and "pytest.fixture": the at sign
        # becomes backslash u0040.
        for n, (made, escaped) in ((8, ("Steps:" + BS + "n", "Steps" + BS + "u003a" + BS + "n")),
                                   (10, (BS + "n@pytest", BS + "n" + BS + "u0040pytest"))):
            self.assertEqual(raw[n - 1].count(made), 1)
            expected = raw[n - 1].replace(made, escaped)
            self.assertEqual(lines[n - 1], expected, f"line {n} came out other than with its one character escaped")
            self.assertEqual(json.loads(lines[n - 1]), json.loads(raw[n - 1]), f"line {n}'s value changed")

    def test_file_mode_scrubs_a_plain_text_file(self):
        """sanitize.py --file scrubs the same planted values in a plain text file, the readable copy's form"""
        part, lines = self.output("txt")
        # Before, worked by hand: lines 1 to 8 each hold a hit of scan.py's patterns; line 9 none.
        self.assertEqual(scan_lines(part["before"], part["name"]), [1, 2, 3, 4, 5, 6, 7, 8],
                         mask("scan.py's hits on the text dummy before the scrub, below.\n" + part["before"].stdout[-1500:]))
        self.assertEqual((part["after"].returncode, last_line(part["after"])), (0, "0 hits, 0 stale exceptions"),
                         mask("scan.py on the scrubbed text file, below.\n" + part["after"].stdout[-1500:]))
        # Each line is the one worked out by hand in txt_dummy(), and the file still ends in a line break.
        expected = [after for _, after in part["dummy"]] + [""]
        if lines != expected:
            self.fail(mask("\n".join(f"line {n}: got {g!r}, expected {e!r}"
                                     for n, (g, e) in enumerate(zip(lines, expected), 1) if g != e)
                           or f"{len(lines)} pieces, expected {len(expected)}"))

    def test_file_mode_touches_no_folder_and_deletes_nothing(self):
        """sanitize.py --file touches no folder, deletes nothing, and refuses an output file that exists"""
        try:
            tools()
        except Exception as e:
            self.fail(mask(f"{type(e).__name__}: {e}"))
        d = scratch(self)
        src, out = os.path.join(d, "in.jsonl"), os.path.join(d, "out.jsonl")
        write(src, "".join(line + "\n" for line, _ in jsonl_dummy()))
        write(os.path.join(d, "keep.txt"), "kept\n")
        write(os.path.join(d, "sub", "keep.txt"), "kept\n")

        def state():
            """Every folder and file under d, with each file's SHA-256."""
            seen = {}
            for root, dirs, files in os.walk(d):
                for x in dirs:
                    seen[os.path.relpath(os.path.join(root, x), d).replace(os.sep, "/") + "/"] = "folder"
                for x in files:
                    with open(os.path.join(root, x), "rb") as fh:
                        seen[os.path.relpath(os.path.join(root, x), d).replace(os.sep, "/")] = \
                            hashlib.sha256(fh.read()).hexdigest()
            return seen

        def sanitize(dst):
            return run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), "--file", src, dst], cwd=d)

        before = state()
        # Worked by hand. Before: in.jsonl, keep.txt, sub/ and sub/keep.txt.
        self.assertEqual(sorted(before), ["in.jsonl", "keep.txt", "sub/", "sub/keep.txt"])
        # Run 1, out.jsonl beside them: exit 0; after, the same four, each with the same bytes, and out.jsonl.
        r1 = sanitize(out)
        after1 = state()
        self.assertEqual(r1.returncode, 0, mask(f"sanitize.py --file: exit {r1.returncode}\n{(r1.stdout + r1.stderr)[-800:]}"))
        self.assertEqual(sorted(after1), ["in.jsonl", "keep.txt", "out.jsonl", "sub/", "sub/keep.txt"])
        self.assertEqual({k: after1[k] for k in before}, before, "a file that was there changed")
        # Run 2, onto the out.jsonl run 1 wrote: refused, and nothing changes, out.jsonl's bytes included.
        r2 = sanitize(out)
        self.assertNotEqual(r2.returncode, 0, "sanitize.py --file wrote over an output file that exists")
        self.assertEqual(state(), after1, "a refused run changed the folder")
        # Run 3, into missing/, a folder that doesn't exist: refused, and no missing/ is made.
        r3 = sanitize(os.path.join(d, "missing", "out.jsonl"))
        self.assertNotEqual(r3.returncode, 0, "sanitize.py --file wrote into a folder that didn't exist")
        self.assertEqual(state(), after1, "a refused run changed the folder")


# --file's ids and --private (Garrett, 2026-11-03: "the values of the keys accountUuid and
# organizationUuid become <account> and <organization>; a repeatable --private <text> replaces
# each given text with <private>, in plain text and inside JSON strings alike").

# Made up for these tests: Claude Code's real account and organization ids are never written here.
ACCOUNT = "11111111-2222-4333-8444-555555555555"
ORGANIZATION = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
SESSION = "99999999-8888-4777-8666-555544443333"
PLACEHOLDER = {"accountUuid": "<account>", "organizationUuid": "<organization>"}
# Two made-up texts for --private: a handle, and a text with a space and capitals.
HANDLE = "example-handle"
SECOND = "Second Example"
PRIVATE_ARGS = ["--private", HANDLE, "--private", SECOND]


def owner(account, organization):
    """A session-owner record, as Claude Code writes one in a session's transcript."""
    return {"type": "session-owner", "accountUuid": account, "organizationUuid": organization, "sessionId": SESSION}


def ids_jsonl_dummy():
    """The ids' dummy transcript: (raw line, the JSON value expected after the scrub) per line.

    Worked by hand from Garrett's rule: the value of an accountUuid key becomes <account> and of
    an organizationUuid key <organization>, in a record or in JSON text inside a string, and
    nothing else changes.
    """
    credential = {"parentUuid": None, "isSidechain": False,
                  "attachment": {"type": "credential_org", "organizationUuid": ORGANIZATION},
                  "type": "attachment", "timestamp": "2026-11-02T18:00:00.000Z", "sessionId": SESSION}
    config = {"oauthAccount": {"accountUuid": ACCOUNT, "organizationUuid": ORGANIZATION, "displayName": "example"}}
    placed = {"oauthAccount": {**config["oauthAccount"], **PLACEHOLDER}}

    def printed(c):
        """A tool result holding a config file, as a session that printed one records it."""
        return {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tu_6", "content": json.dumps(c, indent=2)}]}}

    pairs = [
        # 1. A session-owner record with both ids: each value becomes its key's placeholder.
        (owner(ACCOUNT, ORGANIZATION), owner("<account>", "<organization>")),
        # 2. The credential_org attachment, which holds the organization id alone.
        (credential, {**credential, "attachment": {"type": "credential_org", "organizationUuid": "<organization>"}}),
        # 3. Both ids in JSON text inside a string: the raw line writes each of its quotes as a
        #    backslash and a quote.
        (printed(config), printed(placed)),
        # 4. Both keys already hold their placeholders: nothing to replace, and no hit.
        (owner("<account>", "<organization>"), owner("<account>", "<organization>")),
        # 5. Each key holds the other's placeholder: any value but its own placeholder is replaced.
        (owner("<organization>", "<account>"), owner("<account>", "<organization>")),
    ]
    lines = [(compact(a), b) for a, b in pairs]
    # Line 4 is in json.dumps's default form (spaces), so a line written again instead of kept would show.
    lines[3] = (json.dumps(pairs[3][0]), pairs[3][1])
    return lines


def ids_txt_dummy():
    """The ids' dummy plain text file: (line, the line expected after the scrub, worked by hand)."""
    return [
        # 1. JSON text with both ids, as a readable copy shows a printed config.
        (json.dumps({"accountUuid": ACCOUNT, "organizationUuid": ORGANIZATION}), json.dumps(PLACEHOLDER)),
        # 2. The keys named in prose, with no value: nothing to replace, and no hit.
        ("Claude Code's records hold the keys `accountUuid` and `organizationUuid`.",) * 2,
        # 3. A record in compact JSON, pasted as text.
        (compact(owner(ACCOUNT, ORGANIZATION)), compact(owner("<account>", "<organization>"))),
    ]


def private_jsonl_dummy():
    """The --private dummy transcript: (raw line, the JSON value expected after the scrub) per line.

    Worked by hand from Garrett's rule: each text given as --private becomes <private> wherever it
    is in a JSON string, a key included, and nothing else changes.
    """
    def result(content, n):
        return {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": f"tu_{n}", "content": content}]}}

    def bash(command):
        return {"type": "assistant", "message": {"id": "msg_5", "role": "assistant", "content": [
            {"type": "tool_use", "id": "tu_8", "name": "Bash", "input": {"command": command}}]}}

    def people(login, name):
        return {"type": "user", "toolUseResult": {"login": login, "name": name, "reactions": {login: 1}}}

    clean = {"type": "user", "message": {"role": "user", "content": "Review the example repo."}}
    pairs = [
        # 1. The handle in a tool's output.
        (result("github.com" + chr(10) + "  Logged in to github.com account " + HANDLE + " (keyring)", 7),
         result("github.com" + chr(10) + "  Logged in to github.com account <private> (keyring)", 7)),
        # 2. The handle in a repo's path: replaced there too, the rest of the path staying.
        (bash("git clone https://github.com/" + HANDLE + "/example-repo repo"),
         bash("git clone https://github.com/<private>/example-repo repo")),
        # 3. Both texts as values, and the handle as a key.
        (people(HANDLE, SECOND), people("<private>", "<private>")),
        # 4. The handle in JSON text inside a string, between the quotes the raw line escapes.
        (result(json.dumps({"login": HANDLE}), 9), result(json.dumps({"login": "<private>"}), 9)),
        # 5. Both texts in one string, the handle twice.
        (result(SECOND + " and " + HANDLE + ", then " + HANDLE + " again.", 10),
         result("<private> and <private>, then <private> again.", 10)),
        # 6. Neither text: nothing to replace.
        (clean, clean),
    ]
    lines = [(compact(a), b) for a, b in pairs]
    # Line 6 is in json.dumps's default form (spaces), so a line written again instead of kept would show.
    lines[5] = (json.dumps(clean), clean)
    return lines


def private_txt_dummy():
    """The --private dummy plain text file: (line, the line expected after the scrub, worked by hand)."""
    return [
        ("  Logged in to github.com account " + HANDLE + " (keyring)",
         "  Logged in to github.com account <private> (keyring)"),
        ("git clone https://github.com/" + HANDLE + "/example-repo repo",
         "git clone https://github.com/<private>/example-repo repo"),
        ("login " + HANDLE + ", name " + SECOND, "login <private>, name <private>"),
        (SECOND + " and " + HANDLE + ", then " + HANDLE + " again.", "<private> and <private>, then <private> again."),
        ("Review the example repo.",) * 2,
    ]


_extra = {}


def ids_and_private():
    """Run sanitize.py --file once on each of four dummies: the ids' .jsonl and .txt as they are, and
    the --private ones with --private given twice; each test reads its part."""
    if not _extra:
        try:
            _extra.update(_run_ids_and_private())
        except Exception as e:  # every test reports it, rather than one setUp error
            _extra["error"] = mask(f"{type(e).__name__}: {e}")
    return _extra


def _run_ids_and_private():
    tools()
    work = scratch()
    empty = os.path.join(work, "empty.exceptions")
    write(empty, "")
    result = {}
    for kind, dummy, args in (("ids-jsonl", ids_jsonl_dummy(), []), ("ids-txt", ids_txt_dummy(), []),
                              ("private-jsonl", private_jsonl_dummy(), PRIVATE_ARGS),
                              ("private-txt", private_txt_dummy(), PRIVATE_ARGS)):
        name = "transcript." + kind.split("-")[-1]
        src_dir, out_dir = os.path.join(work, f"in-{kind}"), os.path.join(work, f"out-{kind}")
        src, out = os.path.join(src_dir, name), os.path.join(out_dir, name)
        write(src, "".join(line + "\n" for line, _ in dummy))
        os.makedirs(out_dir)
        r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), "--file", src, out] + args, cwd=work)
        before = run([PY, "-I", os.path.join(EXPORT, "scan.py"), src_dir, empty], cwd=work)
        after = run([PY, "-I", os.path.join(EXPORT, "scan.py"), out_dir, empty], cwd=work)
        text = None
        if os.path.isfile(out):
            with open(out, encoding="utf-8", newline="") as f:
                text = f.read()
        result[kind] = {"name": name, "dummy": dummy, "run": r, "before": before, "after": after, "text": text}
    return result


class OneFileIdsAndPrivate(unittest.TestCase):
    def output(self, kind):
        """sanitize.py --file's output for one of the four dummies, split on line breaks, or the test fails."""
        f = ids_and_private()
        if "error" in f:
            self.fail(f["error"])
        part = f[kind]
        r = part["run"]
        if r.returncode != 0 or part["text"] is None:
            self.fail(mask(f"sanitize.py --file on the {kind} dummy: exit {r.returncode}, no output written.\n"
                           f"{(r.stdout + r.stderr).strip()[-800:]}"))
        return part, part["text"].split("\n")

    def counts(self, part):
        """What sanitize.py --file printed after its output's path: the lines changed and each count."""
        done = [line for line in part["run"].stdout.splitlines() if line.startswith("done: wrote ")]
        m = re.match(r"done: wrote .*, (\d+ of \d+ lines changed; .*)$", done[-1]) if done else None
        return m.group(1) if m else mask(part["run"].stdout.strip()[-300:])

    def wrong_values(self, part, lines):
        """The .jsonl lines whose JSON value isn't the one worked out by hand."""
        wrong = []
        for n, (_, expected) in enumerate(part["dummy"], 1):
            try:
                got = json.loads(lines[n - 1])
            except (IndexError, ValueError) as e:
                got = f"not JSON ({e})"
            if got != expected:
                wrong.append(f"line {n}: got {got!r}, expected {expected!r}")
        return wrong

    def test_file_mode_replaces_the_ids_in_a_jsonl(self):
        """sanitize.py --file writes <account> and <organization> for the values of a dummy .jsonl's accountUuid and organizationUuid keys, which scan.py flags before and finds none of after"""
        part, lines = self.output("ids-jsonl")
        # Before, worked by hand: scan.py flags lines 1, 2, 3 and 5, each with a key holding a value
        # other than its placeholder (line 3's in JSON text, its quotes escaped); line 4 holds only
        # the placeholders.
        self.assertEqual(scan_lines(part["before"], part["name"]), [1, 2, 3, 5],
                         mask("scan.py's hits on the ids' dummy before the scrub, below.\n" + part["before"].stdout[-1500:]))
        self.assertEqual((part["after"].returncode, last_line(part["after"])), (0, "0 hits, 0 stale exceptions"),
                         mask("scan.py on the scrubbed .jsonl, below.\n" + part["after"].stdout[-1500:]))
        self.assertEqual(((len(lines), lines[-1]), self.wrong_values(part, lines)), ((6, ""), []),
                         "five lines out, each with the value worked out by hand in ids_jsonl_dummy()")
        # Line 4, with nothing to replace, comes out as it went in; neither made-up id is left anywhere.
        self.assertEqual(lines[3], part["dummy"][3][0], "line 4, holding only the placeholders, came out changed")
        self.assertEqual([part["text"].count(v) for v in (ACCOUNT, ORGANIZATION)], [0, 0],
                         "a made-up id is still in the output (account, organization)")
        # The counts, by hand: <account> on lines 1, 3 and 5, so 3; <organization> on lines 1, 2, 3
        # and 5, so 4; lines 1, 2, 3 and 5 changed, 4 of 5.
        self.assertEqual(self.counts(part), "4 of 5 lines changed; <projects> 0, <home> 0, <path> 0, <email> 0, "
                                            "<private> 0, <account> 3, <organization> 4, --private 0")

    def test_file_mode_replaces_the_ids_in_a_plain_text_file(self):
        """sanitize.py --file writes <account> and <organization> for the ids in a dummy plain text file, which scan.py flags before and finds none of after"""
        part, lines = self.output("ids-txt")
        # Before, by hand: lines 1 and 3 have a key holding a value; line 2 names the keys, with none.
        self.assertEqual(scan_lines(part["before"], part["name"]), [1, 3],
                         mask("scan.py's hits on the ids' text dummy before the scrub, below.\n" + part["before"].stdout[-1500:]))
        self.assertEqual((part["after"].returncode, last_line(part["after"])), (0, "0 hits, 0 stale exceptions"),
                         mask("scan.py on the scrubbed text file, below.\n" + part["after"].stdout[-1500:]))
        self.assertEqual(lines, [after for _, after in part["dummy"]] + [""])
        self.assertEqual([part["text"].count(v) for v in (ACCOUNT, ORGANIZATION)], [0, 0],
                         "a made-up id is still in the output (account, organization)")
        # By hand: <account> and <organization> once each on lines 1 and 3; 2 of 3 lines changed.
        self.assertEqual(self.counts(part), "2 of 3 lines changed; <projects> 0, <home> 0, <path> 0, <email> 0, "
                                            "<private> 0, <account> 2, <organization> 2, --private 0")

    def test_file_mode_private_text_is_gone_from_a_jsonl(self):
        """sanitize.py --file, given --private twice, writes <private> for each given text in a dummy .jsonl's strings, keys included"""
        part, lines = self.output("private-jsonl")
        self.assertEqual([part["text"].count(t) for t in (HANDLE, SECOND)], [0, 0],
                         "a --private text is still in the output (the handle, the second text)")
        self.assertEqual(((len(lines), lines[-1]), self.wrong_values(part, lines)), ((7, ""), []),
                         "six lines out, each with the value worked out by hand in private_jsonl_dummy()")
        self.assertEqual(lines[5], part["dummy"][5][0], "line 6, holding neither text, came out changed")
        # By hand: the handle once on lines 1, 2 and 4 and twice on lines 3 (a value and a key) and 5;
        # the second text once on lines 3 and 5: 9 in all; lines 1 to 5 changed, 5 of 6.
        self.assertEqual(self.counts(part), "5 of 6 lines changed; <projects> 0, <home> 0, <path> 0, <email> 0, "
                                            "<private> 0, <account> 0, <organization> 0, --private 9")

    def test_file_mode_private_text_is_gone_from_a_plain_text_file(self):
        """sanitize.py --file, given --private twice, writes <private> for each given text in a dummy plain text file"""
        part, lines = self.output("private-txt")
        self.assertEqual([part["text"].count(t) for t in (HANDLE, SECOND)], [0, 0],
                         "a --private text is still in the output (the handle, the second text)")
        self.assertEqual(lines, [after for _, after in part["dummy"]] + [""])
        # By hand: the handle once on lines 1, 2 and 3 and twice on line 4; the second text once on
        # lines 3 and 4: 7 in all; lines 1 to 4 changed, 4 of 5.
        self.assertEqual(self.counts(part), "4 of 5 lines changed; <projects> 0, <home> 0, <path> 0, <email> 0, "
                                            "<private> 0, <account> 0, <organization> 0, --private 7")

    def refused(self, private, text):
        """sanitize.py --file on a one-line plain text dummy, with one --private: its run, and whether it wrote its output."""
        try:
            tools()
        except Exception as e:
            self.fail(mask(f"{type(e).__name__}: {e}"))
        d = scratch(self)
        src, out = os.path.join(d, "in.txt"), os.path.join(d, "out.txt")
        write(src, text + "\n")
        r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), "--file", src, out, "--private", private], cwd=d)
        return r, os.path.exists(out)

    def test_file_mode_refuses_an_empty_private_text(self):
        """sanitize.py --file refuses an empty --private text, which would put <private> between every two characters, and writes nothing"""
        r, wrote = self.refused("", "A line to scrub.")
        # By hand: the tool's own refusal, exit 1 with a message saying the text is empty, and no output.
        self.assertEqual((r.returncode, "empty" in r.stderr, wrote), (1, True, False),
                         mask(f"exit {r.returncode}, output written {wrote}: {(r.stdout + r.stderr).strip()[-400:]}"))

    def test_file_mode_refuses_a_private_text_left_in_its_result(self):
        """sanitize.py --file refuses, writing nothing, a result that still holds a --private text (here one that <private> itself holds)"""
        r, wrote = self.refused("private", "A private note.")
        # By hand: "private" becomes "<private>", which holds "private" again, so the result still holds
        # the text: the tool's own refusal, exit 1 with a message saying so, and no output.
        self.assertEqual((r.returncode, "still in" in r.stderr, wrote), (1, True, False),
                         mask(f"exit {r.returncode}, output written {wrote}: {(r.stdout + r.stderr).strip()[-400:]}"))


# The folder mode on the tracked files (Garrett, 2026-11-03).

def tracked_files():
    """This repo's tracked files (git ls-files), as they are in the working tree."""
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"], capture_output=True, check=True).stdout
    names = sorted({n for n in out.decode("utf-8").split("\0") if n})
    return [n for n in names if os.path.isfile(os.path.join(ROOT, *n.split("/")))]


def everything_under(folder):
    """Every folder (with a final /) and file under folder, as paths relative to it."""
    seen = []
    for root, dirs, files in os.walk(folder):
        rel = os.path.relpath(root, folder).replace(os.sep, "/")
        prefix = "" if rel == "." else rel + "/"
        seen += [prefix + d + "/" for d in dirs] + [prefix + f for f in files]
    return sorted(seen)


class FolderMode(unittest.TestCase):
    def folder_mode(self, plant=None):
        """sanitize.py's folder mode on a scratch copy of the tracked files and any planted ones: its output folder."""
        for tool in ("sanitize.py", "scan.py", "sanitize.exceptions"):
            if not os.path.isfile(os.path.join(EXPORT, tool)):
                self.fail(f"no {tool} in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
        work = scratch(self)
        src, out = os.path.join(work, "src"), os.path.join(work, "out")
        copy_into(src, tracked_files())
        for rel, text in (plant or {}).items():
            write(os.path.join(src, *rel.split("/")), text)
        # sanitize.py deletes its output folder first: it must be this test's own.
        self.assertTrue(inside(out, work) and not os.path.exists(out), f"unsafe output folder {out}")
        r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), src, out], cwd=work)
        if r.returncode != 0 or "done" not in r.stdout:
            self.fail(mask(f"sanitize.py's folder mode failed (exit {r.returncode}):\n"
                           f"{(r.stdout + r.stderr).strip()[-1500:]}"))
        return work, out

    def test_folder_mode_copies_nothing_from_a_planted_instinct_scratch(self):
        """sanitize.py's folder mode copies nothing from a planted .instinct-scratch/ in a scratch copy of the repo"""
        # .instinct-scratch/ is git-ignored and holds clones and raw transcripts: planted here,
        # a clone's file and a transcript line, nothing private in either.
        plant = {
            ".instinct-scratch/file/example/repo/README.md": "A file of a clone.\n",
            ".instinct-scratch/file/example/transcript.jsonl":
                '{"type":"user","message":{"role":"user","content":"Review the repo."}}\n',
        }
        _, out = self.folder_mode(plant)
        # Expected, by hand: the copy was made (README.md and tools/control.py are in it), and
        # nothing in it is under .instinct-scratch/, neither the two files nor their folders.
        self.assertEqual([os.path.isfile(os.path.join(out, *p.split("/"))) for p in ("README.md", "tools/control.py")],
                         [True, True], "the folder mode's output is missing the repo's own files")
        copied = [p for p in everything_under(out) if p.split("/")[0] == ".instinct-scratch"]
        self.assertEqual(copied, [], "the folder mode copied these from the planted .instinct-scratch/")

    def test_folder_mode_copies_no_file_with_private_in_its_name(self):
        """sanitize.py's folder mode copies no file whose name holds .private., at any depth, and still copies each public twin"""
        # A file holding a security finding's text is committed with .private. in its name and never
        # exported (Garrett, 2026-11-04; FILING section 4). Planted here at three depths, each beside
        # its public twin, nothing private in either. One is spelled .Private.: the architect's call
        # (2026-11-04) is that the skip ignores case, since Windows file names do.
        control = "reviews/example/2026-11-04-abc1234-control/"
        plant = {
            "notes.private.md": "A held finding.\n",
            "notes.md": "A redacted twin.\n",
            control + "arm-b-1-report.private.md": "A held finding.\n",
            control + "arm-b-1-report.md": "A redacted twin.\n",
            control + "transcripts/arm-b-1.private.jsonl":
                '{"type":"user","message":{"role":"user","content":"Review the repo."}}\n',
            control + "transcripts/arm-b-1.Private.txt": "A held finding.\n",
        }
        _, out = self.folder_mode(plant)
        # Expected, by hand: the two twins are in the output; none of the four files whose names
        # hold .private. (any case) is, at the top, in the control folder or in its transcripts/.
        expected = {p: ".private." not in p.lower() for p in plant}
        got = {p: os.path.isfile(os.path.join(out, *p.split("/"))) for p in plant}
        self.maxDiff = None
        self.assertEqual(got, expected, "True: in the folder mode's output; False: not in it")

    def test_tracked_files_sanitized_give_0_hits_with_the_real_exceptions(self):
        """this repo's tracked files, sanitized by sanitize.py's folder mode and scanned with the real exceptions file, give 0 hits, 0 stale exceptions"""
        work, out = self.folder_mode()
        s = run([PY, "-I", os.path.join(EXPORT, "scan.py"), out, os.path.join(EXPORT, "sanitize.exceptions")], cwd=work)
        # Expected, by hand: scan.py prints its count line last, here "0 hits, 0 stale exceptions",
        # and exits 0: nothing in the sanitized copy matches its patterns but the exceptions, and
        # each exception still matches.
        hits = [line for line in s.stdout.splitlines() if line.startswith(("HIT ", "STALE "))]
        per_file = {}
        for line in hits:
            name = line.split(" ", 1)[1].split(":", 1)[0] if line.startswith("HIT ") else "(stale exceptions)"
            per_file[name] = per_file.get(name, 0) + 1
        self.assertEqual((s.returncode, last_line(s)), (0, "0 hits, 0 stale exceptions"),
                         mask(f"scan.py on the sanitized tracked files: exit {s.returncode}, {last_line(s)!r}; "
                              f"per file {per_file}; the first 40:\n" + "\n".join(hits[:40])))


# The folder mode's --private texts, the Git Bash spellings of the projects folder and of its
# parent, and its line endings; and scan.py's file of private texts (Garrett, 2026-11-06).

# Made up for these tests, and joined only when they run: the folder mode runs on a copy of this
# repo's tracked files, this file among them, so only the planted files hold either text whole.
PLANTED_HANDLE = "-".join(["planted", "handle", "7f3"])
PLANTED_NAME = " ".join(["Plantedname", "Seven"])
CRLF = chr(13) + chr(10)
ELLIPSIS = chr(0x2026)  # the transcripts' fragments: Git Bash's form, a slash, then an ellipsis


def parent_git_bash():
    """Git Bash's form of the projects folder's parent, which must be a folder below a drive."""
    parent = os.path.dirname(PROJECTS)
    if not re.match(r"[A-Za-z]:" + re.escape(BS) + r"[^" + re.escape(BS) + r"]", parent):
        raise ValueError("these tests expect the projects folder's parent to be a folder below a drive")
    return git_bash(parent)


def mask_parent(text):
    """mask(), with the parent's Git Bash form put back as a word too."""
    text = mask(text)
    try:
        return re.sub(re.escape(parent_git_bash()), "[parent]", text, flags=re.I)
    except ValueError:
        return text


def folder_plants():
    """The planted files: {path: (the bytes planted, the bytes the folder mode must write)}.

    Worked out by hand from Garrett's rules of 2026-11-06: each --private text becomes <private>
    in any case, wherever it is, a JSON key included; Git Bash's form of the projects folder and
    of its parent becomes <projects>, the rest of the path staying, but not where the form is the
    start of a longer name or ends a longer one; nothing else in a line changes, so a .jsonl line
    is not written again; and a file keeps the line endings it came with.
    """
    h, n = PLANTED_HANDLE, PLANTED_NAME
    p, u = git_bash(PROJECTS), parent_git_bash()

    def lines(pairs):
        return tuple("".join(x + "\n" for x in side).encode("utf-8") for side in zip(*pairs))

    def people(login, name):
        return {"type": "user", "toolUseResult": {"login": login, "name": name, "reactions": {login: 1}}}

    def bash(command, n_id):
        return {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": f"tu_{n_id}", "name": "Bash", "input": {"command": command}}]}}

    def said(words):
        return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": words}]}}

    clean = {"type": "user", "message": {"role": "user", "content": "Review the example repo."}}
    return {
        # The handle once on each of lines 1 and 2, the name twice on line 3: 4.
        "planted/folder-private.md": lines([
            ("Logged in to github.com account " + h + " (keyring)",
             "Logged in to github.com account <private> (keyring)"),
            ("git clone https://github.com/" + h.upper() + "/example-repo repo",
             "git clone https://github.com/<private>/example-repo repo"),
            ("Reviewed by " + n.lower() + " and " + n + ".", "Reviewed by <private> and <private>."),
            ("Review the example repo.",) * 2,
        ]),
        # The handle twice on line 1 (a value and a key) and the name once there, the name once on
        # line 2: 4. Line 3, in json.dumps's default form, comes out as it went in.
        "planted/folder-private.jsonl": lines([
            (compact(people(h, n.upper())), compact(people("<private>", "<private>"))),
            (compact(bash("grep -ri '" + n.lower() + "' notes", 9)), compact(bash("grep -ri '<private>' notes", 9))),
            (json.dumps(clean),) * 2,
        ]),
        # Line 4's four are longer names: the parent's form then letters, a hyphen, or a full stop
        # and a letter, and a letter before it.
        "planted/folder-gitbash.md": lines([
            ("cd " + p + "/dev-instincts && git status", "cd <projects>/dev-instincts && git status"),
            ("Git Bash's form (`" + u + "/" + ELLIPSIS + "`) and the session folder's name",
             "Git Bash's form (`<projects>/" + ELLIPSIS + "`) and the session folder's name"),
            ("find " + u + " -maxdepth 3 -name mirror.sh; ls " + p.upper() + ".",
             "find <projects> -maxdepth 3 -name mirror.sh; ls <projects>."),
            ("Longer names stay: " + u + "ices/null, " + u + "-tools/x, x" + u + "/y, " + u + ".d/z",) * 2,
            ("Read src/app.ts at 18:05.",) * 2,
        ]),
        "planted/folder-gitbash.jsonl": lines([
            (compact(bash("cd " + p + "/dev-control && ls", 10)), compact(bash("cd <projects>/dev-control && ls", 10))),
            (compact(said("both folders: Git Bash's form (`" + u + "/" + ELLIPSIS + "`)")),
             compact(said("both folders: Git Bash's form (`<projects>/" + ELLIPSIS + "`)"))),
            (json.dumps(clean),) * 2,
        ]),
        # A CRLF file: both forms replaced, each line still ending CRLF.
        "planted/folder-crlf.txt": (
            ("cd " + p + "/x" + CRLF + "ls " + u + "/" + ELLIPSIS + CRLF).encode("utf-8"),
            ("cd <projects>/x" + CRLF + "ls <projects>/" + ELLIPSIS + CRLF).encode("utf-8")),
    }


_folder_extra = {}


def folder_extra():
    """Run the folder mode once, with --private twice, on a scratch copy of the tracked files and
    the planted files; each test reads its part."""
    if not _folder_extra:
        try:
            _folder_extra.update(_run_folder_extra())
        except Exception as e:  # every test reports it, rather than one setUp error
            _folder_extra["error"] = mask_parent(f"{type(e).__name__}: {e}")
    return _folder_extra


def _run_folder_extra():
    for tool in ("sanitize.py", "scan.py"):
        if not os.path.isfile(os.path.join(EXPORT, tool)):
            raise FileNotFoundError(f"no {tool} in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
    plants = folder_plants()
    work = scratch()
    src, out = os.path.join(work, "src"), os.path.join(work, "out")
    copy_into(src, tracked_files())
    for name, (raw, _) in plants.items():
        path = os.path.join(src, *name.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(raw)
    # sanitize.py deletes its output folder first: it must be this run's own.
    if not inside(out, work) or os.path.exists(out):
        raise RuntimeError(f"unsafe output folder {out}")
    r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), src, out,
             "--private", PLANTED_HANDLE, "--private", PLANTED_NAME], cwd=work)
    written, gained = {}, []
    for rel in (everything_under(out) if os.path.isdir(out) else []):
        if rel.endswith("/"):
            continue
        with open(os.path.join(out, *rel.split("/")), "rb") as fh:
            got = fh.read()
        if rel in plants:
            written[rel] = got
        source = os.path.join(src, *rel.split("/"))
        had = open(source, "rb").read() if os.path.isfile(source) else b""
        if b"\r" in got and b"\r" not in had:
            gained.append(rel)
    return {"run": r, "plants": plants, "written": written, "gained": gained}


class FolderModePrivateAndPaths(unittest.TestCase):
    maxDiff = None

    def part(self):
        """The shared run, or the test fails with why it didn't run."""
        f = folder_extra()
        if "error" in f:
            self.fail(f["error"])
        r = f["run"]
        if r.returncode != 0 or "done" not in r.stdout:
            self.fail(mask_parent(f"sanitize.py's folder mode failed (exit {r.returncode}):\n"
                                  f"{(r.stdout + r.stderr).strip()[-1500:]}"))
        return f

    def wrong(self, f, names):
        """Of the planted files named, those the folder mode didn't write as worked out by hand."""
        return {name: mask_parent(repr(f["written"].get(name))[:800])
                for name in names if f["written"].get(name) != f["plants"][name][1]}

    def test_folder_mode_writes_private_for_each_private_text_in_any_case(self):
        """sanitize.py's folder mode, given --private twice, writes <private> for each text in any case in a planted .md and .jsonl, and counts them on its done line"""
        f = self.part()
        names = ["planted/folder-private.md", "planted/folder-private.jsonl"]
        left = sum(f["written"].get(name, b"").decode("utf-8").lower().count(t.lower())
                   for name in names for t in (PLANTED_HANDLE, PLANTED_NAME))
        done = re.findall(r"^done: <projects> \d+, --private (\d+)$", f["run"].stdout, re.M)
        # By hand: both files as folder_plants() gives them; neither text left in them, in any
        # case; and the done line counts 4 in the .md and 4 in the .jsonl, 8, since no tracked
        # file holds either text whole.
        self.assertEqual((self.wrong(f, names), left, done), ({}, 0, ["8"]),
                         mask_parent("the files that came out otherwise, the texts left, the done line's --private count; "
                                     f"the folder mode printed: {f['run'].stdout.strip()[-300:]!r}"))

    def test_folder_mode_writes_projects_for_the_git_bash_projects_folder_and_its_parent(self):
        """sanitize.py's folder mode writes <projects> for Git Bash's form of the projects folder and of its parent in a planted .md and .jsonl, and leaves a longer name as it is"""
        f = self.part()
        self.assertEqual(self.wrong(f, ["planted/folder-gitbash.md", "planted/folder-gitbash.jsonl"]), {},
                         "the planted files that came out other than worked out by hand in folder_plants()")

    def test_folder_mode_keeps_line_endings(self):
        """sanitize.py's folder mode adds no CR to any file that had none, and a CRLF file keeps its CRLFs where it replaces a path"""
        f = self.part()
        # By hand: no output file holds a CR its source didn't have (the folder mode writes
        # with newline=''), and the planted CRLF file comes out as folder_plants() gives it.
        self.assertEqual((f["gained"], self.wrong(f, ["planted/folder-crlf.txt"])), ([], {}),
                         "the output files that gained a CR their source didn't have, and the CRLF file if wrong")

    def test_folder_mode_refuses_an_empty_private_text_before_it_deletes_anything(self):
        """sanitize.py's folder mode refuses an empty --private text, exit 1, before it deletes or writes anything"""
        if not os.path.isfile(os.path.join(EXPORT, "sanitize.py")):
            self.fail(f"no sanitize.py in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
        d = scratch(self)
        src, dst = os.path.join(d, "src"), os.path.join(d, "dst")
        write(os.path.join(src, "README.md"), "A repo.\n")
        write(os.path.join(dst, "keep.txt"), "kept\n")
        r = run([PY, "-I", os.path.join(EXPORT, "sanitize.py"), src, dst, "--private", ""], cwd=d)
        # By hand: the tool's own refusal, exit 1 with a message saying the text is empty, and the
        # output folder as it was, keep.txt alone in it.
        self.assertEqual((r.returncode, "empty" in r.stderr, everything_under(dst)), (1, True, ["keep.txt"]),
                         mask_parent(f"exit {r.returncode}: {(r.stdout + r.stderr).strip()[-400:]}"))

    def test_scan_reports_each_private_text_by_its_number_without_printing_it(self):
        """scan.py, given a file of private texts as its third argument, reports each text in any case as a hit by its number, prints none of them, not even in another hit's line, and exits 1"""
        if not os.path.isfile(os.path.join(EXPORT, "scan.py")):
            self.fail(f"no scan.py in {EXPORT}; set DEV_INSTINCTS_EXPORT to the export tools' folder")
        d = scratch(self)
        tree = os.path.join(d, "tree")
        write(os.path.join(tree, "notes.md"), "".join(line + "\n" for line in (
            "Prepared for " + PLANTED_NAME + ".",
            "login " + PLANTED_HANDLE.upper(),
            "Nothing here.",
            "both " + PLANTED_NAME.lower() + " and " + PLANTED_HANDLE,
            "mail " + EMAIL + " to " + PLANTED_NAME,
        )))
        texts = os.path.join(d, "texts.txt")
        with open(texts, "wb") as fh:  # the first line ends CRLF, as a file saved on Windows may
            fh.write((PLANTED_NAME + CRLF + PLANTED_HANDLE + "\n").encode("utf-8"))
        empty = os.path.join(d, "empty.exceptions")
        write(empty, "")
        s = run([PY, "-I", os.path.join(EXPORT, "scan.py"), tree, empty, texts], cwd=d)
        printed = (s.stdout + s.stderr).lower()
        # By hand: text 1, the name, on lines 1, 4 and 5, and text 2, the handle, on lines 2 and 4,
        # each hit named by its text's number; line 5's address a hit of scan.py's email pattern,
        # printed with its line as every such hit is, the name in it written <private text 1>, and
        # before the line's private text, since scan.py reads its patterns first; 6 hits; exit 1;
        # neither text printed, in any case.
        expected = ["HIT notes.md:1: private text 1", "HIT notes.md:2: private text 2",
                    "HIT notes.md:4: private text 1", "HIT notes.md:4: private text 2",
                    f"HIT notes.md:5: {EMAIL!r}  mail {EMAIL} to <private text 1>",
                    "HIT notes.md:5: private text 1", "6 hits, 0 stale exceptions"]
        printed_texts = [t.lower() in printed for t in (PLANTED_NAME, PLANTED_HANDLE)]
        self.assertEqual((s.stdout.splitlines(), s.returncode, printed_texts), (expected, 1, [False, False]),
                         "scan.py's lines, its exit code, and whether it printed each text")
