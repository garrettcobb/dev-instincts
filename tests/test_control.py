"""tools/control.py: shuffle, agreement, final, score and session (Garrett, Task 6, 2026-11-02;
tool task 3, 2026-11-03).

The tool as testing/CONTROL.md section 11 describes it, tested against Garrett's lists.
Every input is a dummy written here; nothing is read from a real control run. Each
expected value is worked out by hand in the comment above its assert.

Since tool task 3 the shuffle takes each run's file with its run (--run A1 <file> ...)
and score each run's minutes (--minutes A1=40 B1=30): the first four tests below are
the Task 6 tests, moved to those forms with the same expected values.
"""

import hashlib
import json
import os
import re
import unittest
from collections import Counter
from datetime import datetime, timezone

from support import PY, ROOT, read, run, scratch, write

TOOL = os.path.join(ROOT, "tools", "control.py")
FENCE = "`" * 3

# Two arms' findings in CONTROL.md section 4's form.
ARM_A = "\n".join([
    "# Findings",
    "",
    "## 1: A saved amount is lost when the form is sent twice",
    "Severity: data-loss",
    "Where: src/save.ts:12, at abc1234",
    "What the user loses: the second send overwrites the first amount.",
    "Steps:",
    "1. Fill in the form.",
    "2. Send it twice.",
    "Expected: one saved amount",
    "Actual: the first amount is overwritten",
    "Evidence: reading",
    "",
    "## 2: The total leaves out the last line",
    "Severity: wrong-result",
    "Where: src/total.ts:40, at abc1234",
    "What the user loses: every total is short by its last line.",
    "Steps:",
    "1. Add three lines.",
    "Expected: the sum of three lines",
    "Actual: the sum of two",
    "{extra}Evidence: probe",
    "",
    FENCE,
    "total(3 lines) = 20, expected 30",
    FENCE,
    "",
])

ARM_B = "\n".join([
    "# Findings",
    "",
    "## 1: Export crashes on an empty list",
    "Severity: crash",
    "Where: src/export.ts:7, at abc1234",
    "What the user loses: the export button fails until a row exists.",
    "Steps:",
    "1. Open an empty list.",
    "2. Press Export.",
    "Expected: an empty file",
    "Actual: an error page",
    "Evidence: reading",
    "",
    "## 2: The date filter drops the last day",
    "Severity: wrong-result",
    "Where: src/filter.ts:22, at abc1234",
    "What the user loses: rows from the end date are missing.",
    "Steps:",
    "1. Filter from the 1st to the 3rd.",
    "Expected: rows of the 1st, 2nd and 3rd",
    "Actual: rows of the 1st and 2nd",
    "Evidence: reading",
    "",
    "# Not reached",
    "- nothing",
    "",
])


def control(*args):
    return run([PY, "-I", TOOL, *args])


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def findings(name, n):
    """A findings file in section 4's form holding n findings, each titled with its run's name and row."""
    lines = ["# Findings", ""]
    for i in range(1, n + 1):
        lines += [f"## {i}: The {name} form drops row {i} on save", "Severity: wrong-result",
                  f"Where: src/form.ts:{10 + i}, at abc1234", "What the user loses: one saved row.",
                  "Steps:", "1. Save the form.", "Expected: every row kept", "Actual: one row gone",
                  "Evidence: reading", ""]
    return "\n".join(lines)


def key_file(path, claims, claims_md=None):
    """A key in the shuffle's form; claims are (code, run, id, severity, evidence), in claims.md's order."""
    key = {"protocol": "testing/CONTROL.md", "claims": [
        {"code": c, "arm": r[0], "run": r, "arm_id": i, "title": f"claim {c}", "severity": sev, "evidence": ev}
        for c, r, i, sev, ev in claims]}
    if claims_md:
        key["claims_file"] = {"file": os.path.basename(claims_md), "sha256": sha256(claims_md)}
    write(path, json.dumps(key, indent=2) + "\n")


def verdicts(rows):
    """A judge's verdicts.md in section 10's form; rows are (code, verdict, group, severity)."""
    lines = ["# Verdicts", "", "| Claim | Verdict | Group | Severity | Evidence |", "|---|---|---|---|---|"]
    lines += [f"| {c} | {v} | {g} | {s} | src/app.ts:1: what the code does |" for c, v, g, s in rows]
    return "\n".join(lines + ["", "# Notes", "None.", ""])


def tables(stdout):
    """Each table in the output, by its header's first cell: {row label: cells}, the header under '(header)'."""
    out, cur = {}, None
    for line in stdout.splitlines():
        if not line.startswith("|"):
            cur = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cur is None:
            cur = out.setdefault(cells[0], {"(header)": cells[1:]})
        elif set(cells[0]) != {"-"}:
            cur[cells[0]] = cells[1:]
    return out


class Shuffle(unittest.TestCase):
    def setUp(self):
        self.dir = scratch(self)

    def files(self, texts, folder="in"):
        """One findings file per run, {run: text}: the shuffle's --run arguments for them."""
        args = []
        for name, text in texts.items():
            path = os.path.join(self.dir, folder, f"{name.lower()}.md")
            write(path, text)
            args += ["--run", name, path]
        return args

    def shuffle(self, run_args, out_name="out"):
        out = os.path.join(self.dir, out_name)
        os.makedirs(out, exist_ok=True)
        claims, key = os.path.join(out, "claims.md"), os.path.join(out, "key.json")
        r = control("shuffle", *run_args, "--out", claims, "--key", key)
        return r, claims, key

    def two_runs(self, extra=""):
        return self.files({"A1": ARM_A.replace("{extra}", extra), "B1": ARM_B})

    def test_shuffle_gives_the_same_codes_and_order_on_a_second_run(self):
        """control.py shuffle gives the same codes and order on a second run of the same inputs"""
        args = self.two_runs()
        r1, claims1, key1 = self.shuffle(args, "run-1")
        r2, claims2, key2 = self.shuffle(args, "run-2")
        self.assertEqual((r1.returncode, r2.returncode), (0, 0), r1.stderr + r2.stderr)
        first, second = json.loads(read(key1)), json.loads(read(key2))

        def order(key):
            return [(c["code"], c["run"], c["arm"], c["arm_id"]) for c in key["claims"]]

        # Expected, by hand: two findings from each run, so four claims with four codes, and the
        # same codes in the same order, the same seed and the same claims.md the second time.
        self.assertEqual(len(order(first)), 4, "two findings from each run")
        self.assertEqual(len({code for code, _, _, _ in order(first)}), 4, "each claim has its own code")
        self.assertEqual(order(first), order(second), "codes or order changed on the second run")
        self.assertEqual(first["seed"], second["seed"])
        self.assertEqual(read(claims1), read(claims2), "claims.md changed on the second run")

    def refused(self, extra, term):
        """(refused, files written, the planted text named in the message) for arm A with extra in its finding 2."""
        r, claims, key = self.shuffle(self.two_runs(extra))
        wrote = [os.path.basename(p) for p in (claims, key) if os.path.exists(p)]
        return (r.returncode == 1, wrote, term in r.stderr), r

    def test_shuffle_refuses_a_cross_reference_to_the_ledger(self):
        """control.py shuffle refuses an input with a cross-reference to the ledger (a ledger-style id)"""
        # Expected, by hand: arm A's finding 2 names XY-L07, so the shuffle refuses (exit 1, its own
        # refusal; a usage error is exit 2), writes neither file, and its message names what it found, xy-l07 (it reads the text in lower case).
        got, r = self.refused("Same fault as XY-L07.\n", "xy-l07")
        self.assertEqual(got, (True, [], True), f"exit {r.returncode}, stderr {r.stderr.strip()[-400:]!r}")

    def test_shuffle_refuses_a_cross_reference_to_another_finding(self):
        """control.py shuffle refuses an input with a cross-reference to another finding by its number"""
        # CONTROL.md section 4: "each stands alone: no reference to another finding by its number".
        # Expected, by hand: arm A's finding 2 says "finding 1", so the shuffle refuses (exit 1), writes
        # neither file, and its message names "finding 1".
        got, r = self.refused("Same fault as finding 1, one screen later.\n", "finding 1")
        self.assertEqual(got, (True, [], True), f"exit {r.returncode}, stderr {r.stderr.strip()[-400:]!r}")

    def test_shuffle_takes_an_issue_number_and_the_word_finding_with_no_number(self):
        """control.py shuffle takes an issue number, and the word finding with no number after it"""
        # The prompts ask for issues and pull requests by number, so "#12" must pass, and so must
        # "finding" with no number after it. Expected, by hand: exit 0, both files written.
        r, claims, key = self.shuffle(self.two_runs("Reported in issue #12 and PR #3; this finding stands alone.\n"))
        self.assertEqual((r.returncode, os.path.exists(claims), os.path.exists(key)), (0, True, True),
                         r.stderr.strip()[-400:])

    def test_shuffle_of_four_runs_counts_each_run_and_repeats_itself(self):
        """control.py shuffle of four runs counts each run's findings, gives the same output twice and in any flag order, and seeds from every file"""
        counts = {"A1": 2, "A2": 1, "B1": 3, "B2": 4}
        texts = {name: findings(name, n) for name, n in counts.items()}
        args = self.files(texts)
        r1, claims1, key1 = self.shuffle(args, "first")
        self.assertEqual(r1.returncode, 0, r1.stderr)
        key = json.loads(read(key1))
        # Expected, by hand: 2 + 1 + 3 + 4 = 10 claims, 10 distinct codes; per run 2, 1, 3 and 4; per
        # arm A 2 + 1 = 3 and B 3 + 4 = 7; ids 1 to n in each run; each run's file and its SHA-256 in
        # the key; claims.md's headings in the key's order; and the printed count line below.
        self.assertEqual(Counter(c["run"] for c in key["claims"]), Counter(counts))
        self.assertEqual(Counter(c["arm"] for c in key["claims"]), Counter({"A": 3, "B": 7}))
        self.assertEqual(len({c["code"] for c in key["claims"]}), 10)
        self.assertEqual({name: sorted(int(c["arm_id"]) for c in key["claims"] if c["run"] == name) for name in counts},
                         {"A1": [1, 2], "A2": [1], "B1": [1, 2, 3], "B2": [1, 2, 3, 4]})
        self.assertEqual(key["inputs"], {name: {"file": f"{name.lower()}.md",
                                                "sha256": sha256(os.path.join(self.dir, "in", f"{name.lower()}.md"))}
                                         for name in counts})
        self.assertEqual(re.findall(r"^## ([A-Z]{2}): ", read(claims1), re.M), [c["code"] for c in key["claims"]])
        self.assertIn("(10: 2 from A1, 1 from A2, 3 from B1, 4 from B2)", r1.stdout)
        # Second run on the same files: the same claims (code, run, id, in order), claims.md and seed.
        r2, claims2, key2 = self.shuffle(args, "second")
        again = json.loads(read(key2))

        def order(k):
            return [(c["code"], c["run"], c["arm_id"]) for c in k["claims"]]

        self.assertEqual((order(again), again["seed"], read(claims2)), (order(key), key["seed"], read(claims1)))
        # The flags in another order (B2, A1, B1, A2): the same, since the seed reads the runs by label.
        pairs = [args[i:i + 3] for i in range(0, len(args), 3)]
        swapped = [x for i in (3, 0, 2, 1) for x in pairs[i]]
        r3, claims3, key3 = self.shuffle(swapped, "swapped")
        other = json.loads(read(key3))
        self.assertEqual((order(other), other["seed"], read(claims3)), (order(key), key["seed"], read(claims1)))
        # One title changed in one file at a time: four new seeds, each unlike the first and the others.
        seeds = []
        for changed in counts:
            folder = f"in-{changed.lower()}"
            new = dict(texts, **{changed: texts[changed].replace("drops row 1 on save", "drops row 1 on send")})
            r, _, k = self.shuffle(self.files(new, folder), f"out-{changed.lower()}")
            self.assertEqual(r.returncode, 0, r.stderr)
            seeds.append(json.loads(read(k))["seed"])
        self.assertEqual(len(set(seeds) | {key["seed"]}), 5, "a file's change left the seed as it was")

    def test_shuffle_takes_two_runs_or_four_and_refuses_any_other_set(self):
        """control.py shuffle takes two runs (A1, B1) or four (A1, A2, B1, B2), and refuses any other set without writing"""
        one = findings("one", 1)
        cases = {
            "three runs": self.files({"A1": one, "B1": one, "B2": one}, "three"),
            "one arm only": self.files({"A1": one, "A2": one}, "one-arm"),
            "a run that isn't A1, A2, B1 or B2": self.files({"A1": one, "C1": one}, "c1"),
            "A1 twice": self.files({"A1": one, "B1": one}, "twice") + ["--run", "A1", os.path.join(self.dir, "twice", "a1.md")],
        }
        got = {}
        for i, (case, args) in enumerate(cases.items()):
            r, claims, key = self.shuffle(args, f"case-{i}")
            got[case] = (r.returncode == 1, [os.path.basename(p) for p in (claims, key) if os.path.exists(p)],
                         "--run" in r.stderr)
        # Expected, by hand: each refused by the tool itself (exit 1; a usage error is exit 2), neither file
        # written, and the message names --run.
        self.assertEqual(got, {case: (True, [], True) for case in cases})


class Agreement(unittest.TestCase):
    # Six claims in claims.md's order, KD TX MF ZC HS PW, and the two judge runs' verdicts:
    #
    #   code  run 1                        run 2                        agree?
    #   KD    confirmed, data-loss, grp 1  confirmed, data-loss, grp 1  yes
    #   TX    confirmed, crash, grp 2      confirmed, wrong-result, 2   no: the severities differ
    #   MF    refuted, grp 3               refuted, grp 5               yes: the groups don't count
    #   ZC    can't tell, grp 4            can't tell, grp 4            yes
    #   HS    confirmed, cosmetic, grp 5   refuted, grp 6               no: the verdicts differ
    #   PW    refuted, grp 6               refuted, crash, grp 7        yes: a severity counts only when both confirm
    #
    # Agreed 4 of 6 = 0.666..., printed 0.67. Disputed: TX and HS, in claims.md's order (HS, TX would be
    # the alphabet's).
    CLAIMS = "\n".join([
        "# Claims", "", "Each claim has a code. The order is random.", "",
        "## KD: A saved amount is lost when the form is sent twice", "", "Severity: data-loss",
        "Where: src/save.ts:12, at abc1234", "Evidence: reading", "",
        "## TX: Export crashes on an empty list", "", "Severity: crash", "Where: src/export.ts:7, at abc1234",
        "Evidence: probe", "", FENCE, "## not a heading: the probe's output", "export([]) threw", FENCE, "",
        "## MF: The total leaves out the last line", "", "Severity: wrong-result",
        "Where: src/total.ts:40, at abc1234", "Evidence: reading", "",
        "## ZC: The date filter drops the last day", "", "Severity: wrong-result",
        "Where: src/filter.ts:22, at abc1234", "Evidence: reading", "",
        "## HS: The label is cut", "", "Severity: cosmetic", "Where: src/total.ts:41, at abc1234",
        "Evidence: reading", "",
        "## PW: A row is saved twice", "", "Severity: data-loss", "Where: src/save.ts:20, at abc1234",
        "Evidence: reading", ""])
    ORDER = ("KD", "TX", "MF", "ZC", "HS", "PW")

    def setUp(self):
        self.dir = scratch(self)
        self.claims = os.path.join(self.dir, "claims.md")
        write(self.claims, self.CLAIMS)
        self.key = os.path.join(self.dir, "key.json")
        key_file(self.key, [(c, "A1" if i % 2 == 0 else "B1", str(i // 2 + 1), "wrong-result", "reading")
                            for i, c in enumerate(self.ORDER)], self.claims)
        write(os.path.join(self.dir, "judge-1.md"), verdicts([
            ("KD", "confirmed", 1, "data-loss"), ("TX", "confirmed", 2, "crash"), ("MF", "refuted", 3, "-"),
            ("ZC", "can't tell", 4, "-"), ("HS", "confirmed", 5, "cosmetic"), ("PW", "refuted", 6, "-")]))
        write(os.path.join(self.dir, "judge-2.md"), verdicts([
            ("KD", "confirmed", 1, "data-loss"), ("TX", "confirmed", 2, "wrong-result"), ("MF", "refuted", 5, "-"),
            ("ZC", "can't tell", 4, "-"), ("HS", "refuted", 6, "-"), ("PW", "refuted", 7, "crash")]))

    def agreement(self, claims):
        out = os.path.join(self.dir, "claims-3.md")
        r = control("agreement", self.key, os.path.join(self.dir, "judge-1.md"), os.path.join(self.dir, "judge-2.md"),
                    "--claims", claims, "--out", out)
        return r, out

    def test_agreement_on_six_claims_with_four_agreed(self):
        """control.py agreement on six claims with four agreed prints 0.67 and the two disputed, and writes claims-3.md with those two from claims.md"""
        r, out = self.agreement(self.claims)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lines = r.stdout.splitlines()
        # Expected, by hand (the table above): the rate line and the disputed line, word for word.
        self.assertEqual(lines[:2], ["agreement 0.67: 4 of 6 claims agree (section 12.2)", "disputed  TX, HS"])
        # claims-3.md: claims.md's header, then TX's block and HS's, word for word and in claims.md's
        # order; TX's block keeps its code fence, whose "##" line is not a claim's heading.
        expected = "\n".join([
            "# Claims", "", "Each claim has a code. The order is random.", "",
            "## TX: Export crashes on an empty list", "", "Severity: crash", "Where: src/export.ts:7, at abc1234",
            "Evidence: probe", "", FENCE, "## not a heading: the probe's output", "export([]) threw", FENCE, "",
            "## HS: The label is cut", "", "Severity: cosmetic", "Where: src/total.ts:41, at abc1234",
            "Evidence: reading", ""])
        self.assertEqual(read(out) if os.path.exists(out) else None, expected)

    def test_agreement_refuses_a_claims_md_the_key_was_not_made_with(self):
        """control.py agreement refuses a claims.md that isn't the one the key was made with, and writes nothing"""
        other = os.path.join(self.dir, "other-claims.md")
        write(other, self.CLAIMS.replace("The label is cut", "The label is cut short"))
        r, out = self.agreement(other)
        # Expected, by hand: one word added, so its SHA-256 isn't the key's: refused (exit 1), no claims-3.md, and
        # the message names the key.
        self.assertEqual((r.returncode == 1, os.path.exists(out), "key" in r.stderr), (True, False, True),
                         r.stdout + r.stderr)


class Final(unittest.TestCase):
    # Five claims in claims.md's order, from runs A1 and B1:
    #
    #   code  run id   judge-1                         judge-2                         judge-3
    #   KD    A1  1    confirmed, data-loss, grp 1     confirmed, data-loss, grp 7     -
    #   TX    B1  1    confirmed, data-loss, grp 2     confirmed, data-loss, grp 7     -
    #   MF    A1  2    confirmed, wrong-result, grp 3  confirmed, wrong-result, grp 1  -
    #   ZC    B1  2    refuted, grp 4                  confirmed, crash, grp 2         refuted, grp 1
    #   HS    A1  3    confirmed, cosmetic, grp 3      confirmed, cosmetic, grp 3      -
    #
    # Agreed: KD, TX, MF, HS (same verdict, and the same severity where both confirm) = 4 of 5 = 0.80.
    # Disputed: ZC, so its final verdict is run 3's: refuted, severity -.
    # Groups: judge-1 splits KD and TX and joins MF and HS; judge-2 joins KD and TX and splits MF and HS.
    # Two claims are one bug if any run put them in one group, so {KD, TX}, {MF, HS} and {ZC}, numbered by
    # their first claim in claims.md's order: KD's group 1, MF's 2, ZC's 3.
    # Score on the final verdicts, minutes A1 60 and B1 30:
    #   A1: KD, MF, HS = 3 findings; confirmed groups {1, 2} = 2 (MF and HS once, though judge-2 split them).
    #   B1: TX, ZC = 2; confirmed {1} = 1; ZC refuted = 1.
    #   Overlap {1} = 1 (KD and TX one bug, though judge-1 split them). Unique: A1 {2} = 1, B1 none = 0.
    #   Weighted: A1 group 1 data-loss 4 + group 2 max(wrong-result 3, cosmetic 1) 3 = 7; B1 4.
    # (Run 1's groups alone would give an overlap of 0; run 2's alone, A1 3 confirmed: each mix-up shows.)
    def setUp(self):
        self.dir = scratch(self)
        self.key = os.path.join(self.dir, "key.json")
        key_file(self.key, [("KD", "A1", "1", "data-loss", "reading"), ("TX", "B1", "1", "data-loss", "probe"),
                            ("MF", "A1", "2", "wrong-result", "probe"), ("ZC", "B1", "2", "crash", "reading"),
                            ("HS", "A1", "3", "cosmetic", "reading")])
        self.j = [os.path.join(self.dir, f"judge-{n}.md") for n in (1, 2, 3)]
        write(self.j[0], verdicts([("KD", "confirmed", 1, "data-loss"), ("TX", "confirmed", 2, "data-loss"),
                                   ("MF", "confirmed", 3, "wrong-result"), ("ZC", "refuted", 4, "-"),
                                   ("HS", "confirmed", 3, "cosmetic")]))
        write(self.j[1], verdicts([("KD", "confirmed", 7, "data-loss"), ("TX", "confirmed", 7, "data-loss"),
                                   ("MF", "confirmed", 1, "wrong-result"), ("ZC", "confirmed", 2, "crash"),
                                   ("HS", "confirmed", 3, "cosmetic")]))
        write(self.j[2], verdicts([("ZC", "refuted", 1, "-")]))

    def test_final_joins_groups_across_runs_and_takes_run_3_on_a_dispute(self):
        """control.py final joins groups across the judge's runs, takes run 3's verdict on a disputed claim, and score counts a joined group once"""
        out = os.path.join(self.dir, "verdicts.md")
        r = control("final", self.key, *self.j, "--out", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # Expected, by hand (the table above): section 10's form, one row per claim in claims.md's order;
        # the evidence cell says where the verdict came from; the notes name the inputs and their SHA-256s.
        h = [sha256(p) for p in self.j]
        expected = "\n".join([
            "# Verdicts", "",
            "| Claim | Verdict | Group | Severity | Evidence |",
            "|---|---|---|---|---|",
            "| KD | confirmed | 1 | data-loss | runs 1 and 2 agree |",
            "| TX | confirmed | 1 | data-loss | runs 1 and 2 agree |",
            "| MF | confirmed | 2 | wrong-result | runs 1 and 2 agree |",
            "| ZC | refuted | 3 | - | run 3; run 1 refuted; run 2 confirmed, crash |",
            "| HS | confirmed | 2 | cosmetic | runs 1 and 2 agree |",
            "", "# Notes", "",
            f"Final verdicts by tools/control.py final (testing/CONTROL.md section 12.2), from judge-1.md "
            f"(sha256 {h[0]}), judge-2.md (sha256 {h[1]}) and judge-3.md (sha256 {h[2]}). Agreement 0.80: "
            "4 of 5 claims agree. Disputed, so run 3's: ZC. Two claims are one group if any run put them in one.",
            ""])
        self.assertEqual(read(out) if os.path.exists(out) else None, expected)
        s = control("score", self.key, out, "--minutes", "A1=60", "B1=30")
        self.assertEqual(s.returncode, 0, s.stdout + s.stderr)
        got = {k: v for k, v in tables(s.stdout).get("Measure", {}).items()
               if k in ("(header)", "Findings", "Confirmed (distinct bugs)", "Refuted", "Unique to the arm",
                        "Overlap (confirmed by both)", "Severity-weighted confirmed")}
        self.assertEqual(got, {"(header)": ["A1", "B1"], "Findings": ["3", "2"], "Confirmed (distinct bugs)": ["2", "1"],
                               "Refuted": ["0", "1"], "Unique to the arm": ["1", "0"],
                               "Overlap (confirmed by both)": ["1", "1"], "Severity-weighted confirmed": ["7", "4"]})

    def test_final_refuses_a_dispute_without_run_3_or_run_3_on_an_agreed_claim(self):
        """control.py final refuses a disputed claim without run 3's verdict, and run 3's verdicts on a claim not disputed, writing nothing"""
        extra = os.path.join(self.dir, "judge-3-extra.md")
        write(extra, verdicts([("ZC", "refuted", 1, "-"), ("KD", "confirmed", 1, "data-loss")]))
        got = {}
        for case, inputs in (("ZC disputed, no judge-3.md", self.j[:2]), ("judge-3.md also rules on KD", [*self.j[:2], extra])):
            out = os.path.join(self.dir, f"verdicts-{len(got)}.md")
            r = control("final", self.key, *inputs, "--out", out)
            got[case] = (r.returncode == 1, os.path.exists(out), ("ZC" if "no judge-3" in case else "KD") in r.stderr)
        # Expected, by hand: ZC is disputed (refuted against confirmed), so without run 3 there is no final
        # verdict for it; and KD is agreed, so run 3 had no claim to judge there. Each refused (exit 1), no file
        # written, and the message names the claim.
        self.assertEqual(got, {case: (True, False, True) for case in got})


class Score(unittest.TestCase):
    def test_score_matches_the_hand_worked_six_claim_example(self):
        """control.py score matches the hand-worked six-claim example"""
        # Six claims, runs A1 and B1, two groups, one refuted, one can't tell.
        #
        #   code  run id  evidence  verdict     group  severity (weight, CONTROL.md section 12)
        #   KD    A1  1   probe     confirmed   1      data-loss (4)
        #   TX    B1  1   probe     confirmed   1      crash (3)
        #   MF    A1  2   probe     confirmed   2      wrong-result (3)
        #   ZC    B1  2   reading   can't tell  2      -
        #   HS    A1  3   reading   confirmed   2      cosmetic (1)
        #   PW    A1  4   probe     refuted     1      -
        #
        # A1: findings A1 1 to 4 = 4; probes 1, 2, 4 = 3 of 4.
        #   Confirmed: 1 in group 1, 2 and 3 in group 2, so groups {1, 2} = 2 (2 and 3 are one bug).
        #   Refuted: 4 = 1. Can't tell: 0.
        #   Weighted: group 1 = 4 (1; 4 is refuted); group 2 = max(3, 1) = 3; 4 + 3 = 7.
        # B1: findings B1 1 and 2 = 2; probes 1 = 1 of 2.
        #   Confirmed: 1 in group 1, so {1} = 1. Refuted 0. Can't tell: 2 = 1.
        #   Weighted: group 1 = 3 (B1 1, crash).
        # Overlap: {1, 2} and {1} share {1} = 1. Unique: A1 {2} = 1; B1 none = 0.
        # Accepted upstream: no --accepted, so 0 and 0.
        # Minutes 40 and 30. Confirmed per hour: A1 2 / (40/60) = 2 x 1.5 = 3.0; B1 1 / (30/60) = 1 x 2 = 2.0.
        # Refuted per finding: A1 1 / 4 = 0.25; B1 0 / 2 = 0.00.
        # (Summing every confirmed claim's weight would give A1 4 + 3 + 1 = 8, and counting claims
        #  would give A1 3 confirmed: the numbers are picked so each mix-up shows.)
        expected = {
            "(header)": ["A1", "B1"],
            "Findings": ["4", "2"],
            "Proven (a probe ran)": ["3 of 4", "1 of 2"],
            "Confirmed (distinct bugs)": ["2", "1"],
            "Refuted": ["1", "0"],
            "Can't tell": ["0", "1"],
            "Unique to the arm": ["1", "0"],
            "Overlap (confirmed by both)": ["1", "1"],
            "Severity-weighted confirmed": ["7", "3"],
            "Accepted upstream": ["0", "0"],
            "Minutes": ["40", "30"],
            "Confirmed per hour": ["3.0", "2.0"],
            "Refuted per finding": ["0.25", "0.00"],
        }
        expected_groups = {1: {"KD", "TX", "PW"}, 2: {"MF", "ZC", "HS"}}

        d = scratch(self)
        key_file(os.path.join(d, "key.json"), [
            ("KD", "A1", "1", "data-loss", "probe"), ("TX", "B1", "1", "crash", "probe"),
            ("MF", "A1", "2", "wrong-result", "probe"), ("ZC", "B1", "2", "wrong-result", "reading"),
            ("HS", "A1", "3", "cosmetic", "reading"), ("PW", "A1", "4", "data-loss", "probe")])
        write(os.path.join(d, "verdicts.md"), "\n".join([
            "# Verdicts", "",
            "| Claim | Verdict | Group | Severity | Evidence |",
            "|---|---|---|---|---|",
            "| KD | confirmed | 1 | data-loss | src/save.ts:12: overwrites the saved row |",
            "| TX | confirmed | 1 | crash | src/save.ts:12: throws on the second send |",
            "| MF | confirmed | 2 | wrong-result | src/total.ts:40: stops one line early |",
            "| ZC | can't tell | 2 | - | src/total.ts:40: turns on data the repo doesn't hold |",
            "| HS | confirmed | 2 | cosmetic | src/total.ts:41: the label is cut |",
            "| PW | refuted | 1 | - | src/save.ts:20: the row is locked first |",
            "", "# Notes", "None.", ""]))

        r = control("score", os.path.join(d, "key.json"), os.path.join(d, "verdicts.md"), "--minutes", "A1=40", "B1=30")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(tables(r.stdout).get("Measure"), expected)
        groups = {int(m.group(1)): set(re.findall(r"\b([A-Z]{2}) \(", m.group(2)))
                  for m in re.finditer(r"^- (\d+): (.*)$", r.stdout, re.M)}
        self.assertEqual(groups, expected_groups)

    def test_score_of_four_runs_prints_the_noise_floor(self):
        """control.py score of four runs scores each run alone and prints the noise floor, with no difference for a gap under it"""
        # Each run's claims (each in a group of its own unless named; every confirmed one wrong-result, 3):
        #   A1: 4 findings, 2 confirmed (groups 1, 2), 2 can't tell; 40 minutes.
        #   A2: 5 findings, 1 confirmed (group 1, A1's first bug again), 1 refuted, 3 can't tell; 30 minutes.
        #   B1: 5 findings, 1 confirmed (group 9), 2 refuted, 2 can't tell; 30 minutes.
        #   B2: 5 findings, 3 confirmed (groups 9, 14, 15), 1 refuted, 1 can't tell; 100 minutes.
        # Each run on its own:
        #   confirmed per hour  A1 2 x 60/40 = 3.0; A2 1 x 60/30 = 2.0; B1 1 x 60/30 = 2.0; B2 3 x 60/100 = 1.8
        #   refuted per finding A1 0/4 = 0.00; A2 1/5 = 0.20; B1 2/5 = 0.40; B2 1/5 = 0.20
        #   weighted A1 3 + 3 = 6; A2 3; B1 3; B2 9. Arm A's groups {1, 2}, arm B's {9, 14, 15}: overlap 0;
        #   unique A1 2, A2 1, B1 1, B2 3.
        # Headline (section 12.1):
        #   confirmed per hour: within A |3.0 - 2.0| = 1.0; within B |2.0 - 1.8| = 0.2; floor 1.0;
        #     A (3.0 + 2.0)/2 = 2.5; B (2.0 + 1.8)/2 = 1.9; gap 2.5 - 1.9 = +0.6, under 1.0: no difference.
        #   refuted per finding: within A |0.00 - 0.20| = 0.20; within B |0.40 - 0.20| = 0.20; floor 0.20;
        #     A (0.00 + 0.20)/2 = 0.10; B (0.40 + 0.20)/2 = 0.30; gap 0.10 - 0.30 = -0.20: its size is the
        #     floor, not under it, so it has a direction (section 12.1, "at or over"); fewer refuted is
        #     H2's side for A: A's way. In floats the mean of 0.40 and 0.20 is 0.30000000000000004, so
        #     only exact sums make the gap the floor's size here; the readings use exact fractions.
        plan = {"A1": [("confirmed", 1), ("confirmed", 2), ("can't tell", 3), ("can't tell", 4)],
                "A2": [("confirmed", 1), ("refuted", 5), ("can't tell", 6), ("can't tell", 7), ("can't tell", 8)],
                "B1": [("confirmed", 9), ("refuted", 10), ("refuted", 11), ("can't tell", 12), ("can't tell", 13)],
                "B2": [("confirmed", 9), ("confirmed", 14), ("confirmed", 15), ("refuted", 16), ("can't tell", 17)]}
        letters = iter([a + b for a in "CDFG" for b in "HJKLMNPQRS"])
        claims, rows = [], []
        for name, items in plan.items():
            for i, (verdict, group) in enumerate(items, 1):
                code = next(letters)
                claims.append((code, name, str(i), "wrong-result", "reading"))
                rows.append((code, verdict, group, "wrong-result" if verdict == "confirmed" else "-"))
        d = scratch(self)
        key_file(os.path.join(d, "key.json"), claims)
        write(os.path.join(d, "verdicts.md"), verdicts(rows))
        r = control("score", os.path.join(d, "key.json"), os.path.join(d, "verdicts.md"),
                    "--minutes", "A1=40", "A2=30", "B1=30", "B2=100")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        got = tables(r.stdout)
        per_run = {k: v for k, v in got.get("Measure", {}).items()
                   if k in ("(header)", "Findings", "Confirmed (distinct bugs)", "Refuted", "Can't tell",
                            "Unique to the arm", "Overlap (confirmed by both)", "Severity-weighted confirmed",
                            "Minutes", "Confirmed per hour", "Refuted per finding")}
        self.assertEqual(per_run, {
            "(header)": ["A1", "A2", "B1", "B2"],
            "Findings": ["4", "5", "5", "5"],
            "Confirmed (distinct bugs)": ["2", "1", "1", "3"],
            "Refuted": ["0", "1", "2", "1"],
            "Can't tell": ["2", "3", "2", "1"],
            "Unique to the arm": ["2", "1", "1", "3"],
            "Overlap (confirmed by both)": ["0", "0", "0", "0"],
            "Severity-weighted confirmed": ["6", "3", "3", "9"],
            "Minutes": ["40", "30", "30", "100"],
            "Confirmed per hour": ["3.0", "2.0", "2.0", "1.8"],
            "Refuted per finding": ["0.00", "0.20", "0.40", "0.20"],
        })
        self.assertEqual(got.get("Headline measure"), {
            "(header)": ["Within A", "Within B", "Floor", "A", "B", "Gap A - B", "Reading"],
            "Confirmed per hour": ["1.0", "0.2", "1.0", "2.5", "1.9", "+0.6", "no difference"],
            "Refuted per finding": ["0.20", "0.20", "0.20", "0.10", "0.30", "-0.20", "A's way"],
        })


class Session(unittest.TestCase):
    def test_session_reports_model_effort_version_times_and_a_planted_leak_term(self):
        """control.py session reports the model, effort, version, times and a planted leak term of a dummy transcript"""
        # The dummy, in the shape of a Claude Code transcript (one JSON object per line):
        #   line 1  user prompt  18:00:00Z  version 2.1.999, permission mode auto
        #   line 2  assistant    18:00:05Z  request msg_1: claude-fable-5-1, effort high, one Read
        #   line 3  tool result  18:05:00Z  holds the planted term findings.jsonl
        #   line 4  assistant    18:17:48Z  request msg_2: claude-fable-5-1, effort high
        # The report file's last write is set to 18:17:48Z.
        # Expected: version 2.1.999 on 4 lines; model claude-fable-5-1 on 2 requests; effort high 2;
        # first prompt 18:00:00Z and last message 18:17:48Z, in this PC's time zone as the tool prints
        # them; time used 18:17:48 - 18:00:00 = 17 min 48 s = 17 + 48/60 = 17.8 min; one leak hit,
        # findings.jsonl on line 3.
        def utc(h, m, s):
            return datetime(2026, 11, 2, h, m, s, tzinfo=timezone.utc)

        def stamp(t):
            return t.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        def local(t):
            return t.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

        start, end = utc(18, 0, 0), utc(18, 17, 48)
        usage = {"input_tokens": 10, "output_tokens": 20, "cache_creation_input_tokens": 100,
                 "cache_read_input_tokens": 0}
        lines = [
            {"type": "user", "timestamp": stamp(start), "version": "2.1.999", "permissionMode": "auto",
             "message": {"role": "user", "content": "Review the repo and write report.md."}},
            {"type": "assistant", "timestamp": stamp(utc(18, 0, 5)), "version": "2.1.999", "effort": "high",
             "requestedModel": "claude-fable-5-1",
             "message": {"id": "msg_1", "model": "claude-fable-5-1", "role": "assistant", "usage": usage,
                         "content": [{"type": "text", "text": "Reading the code."},
                                     {"type": "tool_use", "id": "tu_1", "name": "Read",
                                      "input": {"file_path": "repo/src/app.ts"}}]}},
            {"type": "user", "timestamp": stamp(utc(18, 5, 0)), "version": "2.1.999",
             "message": {"role": "user", "content": [
                 {"type": "tool_result", "tool_use_id": "tu_1",
                  "content": "1  // rows are kept in data/findings.jsonl"}]}},
            {"type": "assistant", "timestamp": stamp(end), "version": "2.1.999", "effort": "high",
             "requestedModel": "claude-fable-5-1",
             "message": {"id": "msg_2", "model": "claude-fable-5-1", "role": "assistant", "usage": usage,
                         "content": [{"type": "text", "text": "Done."}]}},
        ]
        d = scratch(self)
        transcript, report = os.path.join(d, "session.jsonl"), os.path.join(d, "report.md")
        write(transcript, "".join(json.dumps(o) + "\n" for o in lines))
        write(report, "# Findings\n")
        os.utime(report, (end.timestamp(), end.timestamp()))

        r = run([PY, "-I", TOOL, "session", transcript, "--report", report, "--leak"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = r.stdout.splitlines()
        got = {line[:16].strip(): line[16:].strip() for line in out if line[:1] not in (" ", "")}
        expected = {
            "claude code": "2.1.999 (4 lines)",
            "model": "claude-fable-5-1 2   (requests: 2)",
            "requested model": "claude-fable-5-1 2",
            "effort": "high 2",
            "first prompt": f'{local(start)}   "Review the repo and write report.md."',
            "report written": local(end),
            "time used": "17.8 min (from first prompt to report written)",
            "last message": local(end),
            "leak terms": "1 distinct hits; first 20:",
        }
        self.assertEqual({k: got.get(k) for k in expected}, expected)
        hits = [line.strip() for line in out if line.startswith("  line ")]
        self.assertEqual(len(hits), 1, hits)
        self.assertTrue(hits[0].startswith("line 3 (user): 'findings.jsonl' in"), hits[0])

    def test_session_prompt_gives_the_first_prompts_sha256_and_whether_a_file_matches(self):
        """control.py session --prompt prints the SHA-256 of the transcript's first prompt and whether a prompt file matches it"""
        # The prompt as written: two lines, nothing after the last. A paste reaches the transcript in a
        # block (Claude Code 2.1.317): the open tag and a line break, the text, a line break, the close
        # tag. A subagent's first prompt is the text as sent. Both sides are compared with line breaks
        # as LF, whitespace at either end stripped and a byte-order mark dropped.
        text = "Review the repo.\nWrite report.md here."
        pasted = '<pasted_content id="ab12">\n' + text + '\n</pasted_content id="ab12">\n'
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        # Expected, by hand, per case: the first prompt's SHA-256 and how it was read; the file's match.
        #   the paste vs same.txt (a byte-order mark, CRLF, a final line break): h, inside its paste block, matches
        #   the paste vs other.txt ("there" for "here"): h, inside its paste block, does not match
        #   the subagent's plain prompt vs same.txt: h, as written, matches
        #   the paste plus typed words vs same.txt: the whole text's SHA-256, as written, does not match
        d = scratch(self)
        same, other = os.path.join(d, "same.txt"), os.path.join(d, "other.txt")
        with open(same, "wb") as f:
            f.write(b"\xef\xbb\xbf" + b"Review the repo.\r\nWrite report.md here.\r\n")
        write(other, "Review the repo.\nWrite report.md there.\n")
        other_h = hashlib.sha256("Review the repo.\nWrite report.md there.".encode("utf-8")).hexdigest()
        typed = pasted + "And be quick."
        typed_h = hashlib.sha256(typed.strip().encode("utf-8")).hexdigest()
        cases = {"paste, same.txt": (pasted, same), "paste, other.txt": (pasted, other),
                 "plain, same.txt": (text, same), "paste and typed words, same.txt": (typed, same)}
        expected = {
            "paste, same.txt": (f"{h} (inside its paste block)",
                                f"same.txt: matches; its text's sha256 {h}, the file's sha256sum {sha256(same)}"),
            "paste, other.txt": (f"{h} (inside its paste block)",
                                 f"other.txt: does not match; its text's sha256 {other_h}, the file's sha256sum {sha256(other)}"),
            "plain, same.txt": (f"{h} (as written)",
                                f"same.txt: matches; its text's sha256 {h}, the file's sha256sum {sha256(same)}"),
            "paste and typed words, same.txt": (f"{typed_h} (as written)",
                                                f"same.txt: does not match; its text's sha256 {h}, the file's sha256sum {sha256(same)}"),
        }
        got = {}
        for i, (case, (first, prompt_file)) in enumerate(cases.items()):
            transcript = os.path.join(d, f"t{i}.jsonl")
            write(transcript, "".join(json.dumps(o) + "\n" for o in [
                {"type": "user", "timestamp": "2026-11-03T18:00:00.000Z", "message": {"role": "user", "content": first}},
                {"type": "assistant", "timestamp": "2026-11-03T18:00:05.000Z",
                 "message": {"id": "msg_1", "model": "claude-fable-5-1", "role": "assistant",
                             "content": [{"type": "text", "text": "Done."}]}}]))
            r = run([PY, "-I", TOOL, "session", transcript, "--prompt", prompt_file])
            lines = {line[:16].strip(): line[16:].strip() for line in r.stdout.splitlines() if line[:1] not in (" ", "")}
            got[case] = (lines.get("prompt sha256"), lines.get("prompt file")) if r.returncode == 0 else \
                f"exit {r.returncode}: {r.stderr.strip()[-300:]}"
        self.assertEqual(got, expected)

    def test_session_prompt_strips_a_paste_wrapper_and_says_so(self):
        """control.py session --prompt strips the paste wrapper round a pasted first prompt, and nothing else, says whether it did, and matches the prompt file"""
        # Claude Code 2.1.318 records a pasted first message the way arm B run 1's transcript holds
        # it (2026-11-04): two line breaks, <pasted_content id="19fa">, a line break, the text, a
        # line break, </pasted_content id="19fa">, a line break (Garrett, 2026-11-04: the check
        # strips that wrapper and nothing else, says it did, and matches the file). The prompt
        # file holds the text and nothing else: LF line breaks, none at its end, so its sha256sum
        # is its text's.
        text = "Review the repo here.\n\n1. Read only.\n  Write report.md here."
        near_text = "Review the repo here.\n1. Read only.\n  Write report.md here."
        wrapped = '\n\n<pasted_content id="19fa">\n' + text + '\n</pasted_content id="19fa">\n'
        # Expected, by hand: each SHA-256 is sha256sum's, of a file holding that text's bytes and
        # nothing else (the architect's run, 2026-11-04), not control.py's own hashing:
        #   the text, 60 bytes: 21, 2 line breaks, 13, 1 line break, 23
        #   near_text, the text without its blank line, 59 bytes
        #   the paste with "And be quick." typed after it, both ends stripped: the open tag (26),
        #   a line break, the text (60), a line break, the close tag (27), a line break and the
        #   typed words (13), 129 bytes
        h = "902cc65b8003ad97464f1de813d49b86adb6ed494d251b92220a4b636728deb8"
        near_h = "fa9d9a4396b9170cd42846effc328f3a50201351135054c9aabe3965d5920447"
        typed_h = "e45bc4a16bb9a64456f86f1fac1775beaea4de3747671874c124eb7c40900261"
        stripped = '<pasted_content id="19fa"> ... </pasted_content id="19fa"> stripped before hashing'
        unstripped = "none stripped: the first prompt is not one paste block alone, so it is hashed as written"
        d = scratch(self)
        prompt, near = os.path.join(d, "prompt.txt"), os.path.join(d, "near.txt")
        for path, body in ((prompt, text), (near, near_text)):
            with open(path, "wb") as f:
                f.write(body.encode("utf-8"))
        cases = {"wrapped, prompt.txt": (wrapped, prompt), "plain, prompt.txt": (text, prompt),
                 "wrapped, near.txt": (wrapped, near),
                 "wrapped and typed words, prompt.txt": (wrapped + "And be quick.", prompt)}
        # Per case: the wrapper line, the first prompt's SHA-256 and how it was read, and the file's
        # match. A strip that took more than the wrapper (the blank line) would match near.txt.
        expected = {
            "wrapped, prompt.txt": (stripped, f"{h} (inside its paste block)",
                                    f"prompt.txt: matches; its text's sha256 {h}, the file's sha256sum {h}"),
            "plain, prompt.txt": (unstripped, f"{h} (as written)",
                                  f"prompt.txt: matches; its text's sha256 {h}, the file's sha256sum {h}"),
            "wrapped, near.txt": (stripped, f"{h} (inside its paste block)",
                                  f"near.txt: does not match; its text's sha256 {near_h}, "
                                  f"the file's sha256sum {near_h}"),
            "wrapped and typed words, prompt.txt": (unstripped, f"{typed_h} (as written)",
                                                    f"prompt.txt: does not match; its text's sha256 {h}, "
                                                    f"the file's sha256sum {h}"),
        }
        got = {}
        for i, (case, (first, prompt_file)) in enumerate(cases.items()):
            transcript = os.path.join(d, f"t{i}.jsonl")
            write(transcript, "".join(json.dumps(o) + "\n" for o in [
                {"type": "user", "timestamp": "2026-11-04T20:48:24.000Z", "message": {"role": "user", "content": first}},
                {"type": "assistant", "timestamp": "2026-11-04T20:48:30.000Z",
                 "message": {"id": "msg_1", "model": "claude-fable-5-1", "role": "assistant",
                             "content": [{"type": "text", "text": "Done."}]}}]))
            r = run([PY, "-I", TOOL, "session", transcript, "--prompt", prompt_file])
            lines = {line[:16].strip(): line[16:].strip() for line in r.stdout.splitlines() if line[:1] not in (" ", "")}
            got[case] = (lines.get("prompt wrapper"), lines.get("prompt sha256"), lines.get("prompt file")) \
                if r.returncode == 0 else f"exit {r.returncode}: {r.stderr.strip()[-300:]}"
        self.maxDiff = None
        self.assertEqual(got, expected)
