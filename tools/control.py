#!/usr/bin/env python3
"""Helpers for the control protocol, testing/CONTROL.md.

  shuffle    Give the runs' findings random codes, in a random order, for a blind
             judge: two runs (A1, B1), or on the first repo four (A1, A2, B1, B2).
             Writes the judge's claims file and the key that maps each code back
             to its arm and run. The seed is the SHA-256 of every run's file, so
             nobody picks it, and a re-run on the same files gives the same output.
  agreement  From the key and the judge's first two runs: the agreement rate, the
             disputed codes, and claims-3.md, the disputed claims copied from
             claims.md for the judge's third run.
  final      The final verdicts.md, from the judge's first two runs and the third
             if there is one: the agreed verdicts, run 3's on the disputed claims,
             and the groups joined across the runs.
  score      Map the final verdicts back to the runs through the key, score each
             run on its own, and print the measures of CONTROL.md section 12 with
             the noise floor of section 12.1.
  session    Read one Claude Code session transcript (.jsonl): model, effort,
             version, permission mode, start, end and time used, tokens, tools
             used, the context Claude Code attached (and any CLAUDE.md or
             AGENTS.md it loaded), any Dev Instincts term that reached it, and the
             SHA-256 of its first prompt beside a prompt file's, a paste's wrapper
             stripped first and the strip reported.

Standard library only. It reads and writes only the files named on its command
line. It never runs, imports or installs anything from a reviewed repo.

  python -I tools/control.py shuffle --run A1 <file> [--run A2 <file>] --run B1 <file> [--run B2 <file>] --out claims.md --key key.json
  python -I tools/control.py agreement key.json judge-1.md judge-2.md --claims claims.md --out claims-3.md
  python -I tools/control.py final key.json judge-1.md judge-2.md [judge-3.md] --out verdicts.md
  python -I tools/control.py score key.json verdicts.md --minutes A1=17.8 [A2=<m>] B1=<m> [B2=<m>]
  python -I tools/control.py session <transcript.jsonl> [--clone DIR] [--report FILE] [--leak] [--term TEXT] [--prompt FILE]
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction

SEVERITIES = ("data-loss", "security", "wrong-result", "crash", "stuck", "process", "cosmetic")
WEIGHTS = {"data-loss": 4, "security": 4, "wrong-result": 3, "crash": 3,
           "stuck": 2, "process": 1, "cosmetic": 1}
# Consonants only, and no B: a code never reads as a word or as an arm's name.
LETTERS = "CDFGHJKLMNPQRSTVWXZ"
LEAK_TERMS = ("instinct", "findings.jsonl", "filing.md", "stats.md",
              "agent-memory", "agents-parked")
LEDGER_ID = re.compile(r"\b[a-z]{2}-l\d{2}\b")
# A finding pointing to another by its number (CONTROL.md section 4): "finding 2", "findings 1
# and 3", "finding #2". An issue's or a pull request's number ("#12") is allowed.
FINDING_REF = re.compile(r"\bfindings?\s+(?:#\s*)?\d+\b")
# The runs a shuffle takes: one per arm, or on the first repo two per arm (section 12.1).
RUN_SETS = ({"A1", "B1"}, {"A1", "A2", "B1", "B2"})
# How Claude Code 2.1.317 writes a paste into the transcript: the open tag and a line break,
# the text, a line break and the close tag. 2.1.318 writes it the same way, with two line
# breaks before the block and one after it (arm B run 1's first prompt, 2026-11-04).
PASTE = re.compile(r'<pasted_content id="([^"]*)">\n(.*)\n</pasted_content id="\1">', re.S)
VERDICT_WORDS = {"confirmed": "confirmed", "refuted": "refuted", "cant-tell": "can't tell"}
# The headline measures (section 12): label, decimals printed, and which sign of A - B is A's way.
HEADLINE = (("Confirmed per hour", 1, 1), ("Refuted per finding", 2, -1))


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def norm_severity(text):
    t = re.sub(r"\s+", "-", text.lower().replace("`", "").replace("*", "").replace("_", "-").strip())
    for sev in SEVERITIES:
        if t.startswith(sev):
            return sev
    return "unknown"


def norm_verdict(text):
    t = re.sub(r"[^a-z]", "", text.lower())
    return {"confirmed": "confirmed", "refuted": "refuted", "canttell": "cant-tell",
            "cannottell": "cant-tell", "cantell": "cant-tell"}.get(t)


def field(lines, name):
    for line in lines:
        s = line.strip().lstrip("-* ").replace("**", "")
        if s.lower().startswith(name.lower() + ":"):
            return s[len(name) + 1:].strip()
    return ""


def parse_findings(path):
    """Findings are '## <id>: <title>' blocks, under '# Findings' if the file has it."""
    lines = read_text(path).splitlines()
    start, fence = None, False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif not fence and line.strip().lower() == "# findings":
            start = i + 1
            break
    sectioned = start is not None
    found, cur, fence = [], None, False
    for line in lines[start if sectioned else 0:]:
        is_fence = line.lstrip().startswith("```")
        if not fence and not is_fence:
            if sectioned and line.startswith("# "):
                break
            if line.startswith("## "):
                arm_id, sep, title = line[3:].partition(":")
                if not sep or not arm_id.strip() or not title.strip():
                    sys.exit(f"{path}: a finding's heading must read '## <id>: <title>', got: {line}")
                cur = {"arm_id": arm_id.strip(), "title": title.strip(), "body": []}
                found.append(cur)
                continue
        if is_fence:
            fence = not fence
        if cur is not None:
            cur["body"].append(line)
    for f in found:
        body = f["body"]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        f["severity"] = norm_severity(field(body, "Severity"))
        ev = field(body, "Evidence").lower()
        f["evidence"] = "probe" if ev.startswith("probe") else "reading" if ev.startswith("reading") else "missing"
    return found


def draws(seed):
    i = 0
    while True:
        yield int.from_bytes(hashlib.sha256(seed + i.to_bytes(8, "big")).digest()[:8], "big")
        i += 1


def shuffled(items, rnd):
    items = list(items)
    for i in range(len(items) - 1, 0, -1):
        j = next(rnd) % (i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def run_files(pairs):
    """The --run pairs as {run: file}, in label order: two runs, A1 and B1, or four, A1, A2, B1 and B2."""
    runs = {}
    for label, path in pairs:
        label = label.upper()
        if label in runs:
            sys.exit(f"--run {label} is given twice")
        runs[label] = path
    if set(runs) not in RUN_SETS:
        sys.exit("--run takes two runs, A1 and B1, or four, A1, A2, B1 and B2; got " + ", ".join(sorted(runs)))
    return dict(sorted(runs.items()))


def cmd_shuffle(a):
    runs = run_files(a.run)
    found = {run: parse_findings(path) for run, path in runs.items()}
    for run, path in runs.items():
        if not found[run]:
            sys.exit(f"run {run}: no '## <id>: <title>' findings in {path}")
    hints = []
    for run in runs:
        for f in found[run]:
            low = "\n".join([f["title"]] + f["body"]).lower().replace("\\", "/")
            hit = ([t for t in LEAK_TERMS + ("dev-control",) if t in low] + LEDGER_ID.findall(low)
                   + [" ".join(m.split()) for m in FINDING_REF.findall(low)])
            if hit:
                hints.append(f"run {run} {f['arm_id']}: {', '.join(sorted(set(hit)))}")
    if hints:
        sys.exit("these findings would tell the judge where they came from, or point to another finding by "
                 "its number; cut that (CONTROL.md sections 4 and 13, step 5) and run again:" "\n  "
                 + "\n  ".join(hints))
    parts = [b"control-shuffle-2"]
    for run, path in runs.items():
        with open(path, "rb") as f:
            parts += [run.encode("ascii"), f.read()]
    seed = hashlib.sha256(b"\0".join(parts)).digest()
    rnd = draws(seed)
    pool = [dict(f, run=run, arm=run[0]) for run in runs for f in found[run]]
    order = shuffled(pool, rnd)
    codes = shuffled([x + y for x in LETTERS for y in LETTERS], rnd)
    if len(order) > len(codes):
        sys.exit(f"{len(order)} findings, and only {len(codes)} codes; nothing written")
    out = ["# Claims", "", "Each claim has a code. The order is random.", ""]
    claims = []
    for code, f in zip(codes, order):
        # The severity line is rewritten to the scale's own word, so spelling can't hint at an arm.
        body = [f"Severity: {f['severity']}" if f["severity"] != "unknown" and field([line], "Severity")
                else line for line in f["body"]]
        out += [f"## {code}: {f['title']}", ""] + body + [""]
        claims.append({"code": code, "arm": f["arm"], "run": f["run"], "arm_id": f["arm_id"], "title": f["title"],
                       "severity": f["severity"], "evidence": f["evidence"]})
    write_text(a.out, "\n".join(out).rstrip("\n") + "\n")
    key = {
        "protocol": "testing/CONTROL.md",
        "made": datetime.now().astimezone().isoformat(timespec="seconds"),
        "seed": seed.hex(),
        "seed_from": "SHA-256 of 'control-shuffle-2', then each run's label and file in label order, a NUL byte between",
        "inputs": {run: {"file": os.path.basename(path), "sha256": sha256_file(path)} for run, path in runs.items()},
        "claims_file": {"file": os.path.basename(a.out), "sha256": sha256_file(a.out)},
        "claims": claims,
    }
    write_text(a.key, json.dumps(key, indent=2, ensure_ascii=False) + "\n")
    for c in claims:
        if c["severity"] == "unknown" or c["evidence"] == "missing":
            print(f"note: {c['run']} {c['arm_id']}: severity {c['severity']}, evidence {c['evidence']}")
    counts = ", ".join(f"{len(found[run])} from {run}" for run in runs)
    print(f"claims {os.path.basename(a.out)} sha256 {sha256_file(a.out)} ({len(claims)}: {counts})")
    print(f"key    {os.path.basename(a.key)} sha256 {sha256_file(a.key)}")
    print(f"seed   {seed.hex()}")


def parse_verdicts(path, claims, need=None):
    """The rows of a verdicts table for the codes in claims; each code in need (all of claims if None) must have one."""
    rows = {}
    for n, line in enumerate(read_text(path).splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        code = cells[0].strip("`* ").upper()
        if code not in claims:
            continue
        if len(cells) < 4:
            sys.exit(f"{path}:{n}: the row for {code} needs Claim, Verdict, Group and Severity")
        if code in rows:
            sys.exit(f"{path}:{n}: {code} has two rows")
        verdict = norm_verdict(cells[1])
        if verdict is None:
            sys.exit(f"{path}:{n}: the verdict must be confirmed, refuted or can't tell, got {cells[1]!r}")
        try:
            group = int(cells[2].strip("`*# "))
        except ValueError:
            sys.exit(f"{path}:{n}: the group must be a number, got {cells[2]!r}")
        severity = norm_severity(cells[3])
        if verdict == "confirmed" and severity not in WEIGHTS:
            sys.exit(f"{path}:{n}: a confirmed claim needs a severity on the scale, got {cells[3]!r}")
        rows[code] = {"verdict": verdict, "group": group, "severity": severity}
    missing = sorted(set(claims if need is None else need) - set(rows))
    if missing:
        sys.exit(f"{path}: no verdict for {', '.join(missing)}")
    return rows


def agree(one, two):
    """Runs 1 and 2 agree on a claim: the same verdict and, when both confirm it, the same severity (section 12.2)."""
    return one["verdict"] == two["verdict"] and (one["verdict"] != "confirmed" or one["severity"] == two["severity"])


def judged(a):
    """The key, its codes in claims.md's order, runs 1 and 2's verdicts, and the disputed codes in that order."""
    key = json.loads(read_text(a.key))
    claims = {c["code"]: c for c in key["claims"]}
    order = [c["code"] for c in key["claims"]]
    one, two = parse_verdicts(a.judge1, claims), parse_verdicts(a.judge2, claims)
    return key, claims, order, one, two, [c for c in order if not agree(one[c], two[c])]


def rate(order, disputed):
    agreed = len(order) - len(disputed)
    return f"{agreed / len(order):.2f}: {agreed} of {len(order)} claims agree"


def claim_blocks(path, codes):
    """claims.md as its header and one block per code: a claim's '## <code>:' heading up to the next, outside code fences."""
    header, blocks, cur, fence = [], {}, None, False
    for line in read_text(path).splitlines():
        is_fence = line.lstrip().startswith("```")
        if not fence and not is_fence and line.startswith("## "):
            code = line[3:].split(":", 1)[0].strip()
            if code in codes:
                if code in blocks:
                    sys.exit(f"{path}: two claims are headed {code}")
                cur = blocks[code] = []
        if is_fence:
            fence = not fence
        (header if cur is None else cur).append(line)
    missing = [c for c in codes if c not in blocks]
    if missing:
        sys.exit(f"{path}: no claim is headed {', '.join(missing)}")

    def trimmed(lines):
        while lines and not lines[-1].strip():
            lines.pop()
        return lines

    return trimmed(header), {c: trimmed(b) for c, b in blocks.items()}


def cmd_agreement(a):
    key, claims, order, one, two, disputed = judged(a)
    if sha256_file(a.claims) != (key.get("claims_file") or {}).get("sha256"):
        sys.exit(f"{a.claims} isn't the claims file the key was made with (its SHA-256 isn't the key's); nothing written")
    header, blocks = claim_blocks(a.claims, order)
    print(f"agreement {rate(order, disputed)} (section 12.2)")
    print(f"disputed  {', '.join(disputed) if disputed else 'none'}")
    if not disputed:
        print("no claim is disputed, so there is no run 3, and no claims-3 file is written (section 10.1)")
        return
    out = header + [""]
    for c in disputed:
        out += blocks[c] + [""]
    write_text(a.out, "\n".join(out).rstrip("\n") + "\n")
    print(f"claims-3  {os.path.basename(a.out)} sha256 {sha256_file(a.out)} ({len(disputed)} claims, in claims.md's order)")


def said(row):
    return VERDICT_WORDS[row["verdict"]] + (f", {row['severity']}" if row["verdict"] == "confirmed" else "")


def cmd_final(a):
    key, claims, order, one, two, disputed = judged(a)
    if disputed and not a.judge3:
        sys.exit(f"disputed: {', '.join(disputed)}; final needs run 3's verdicts on them, judge-3.md (section 10.1)")
    three = {}
    if a.judge3:
        three = parse_verdicts(a.judge3, claims, need=disputed)
        extra = [c for c in order if c in three and c not in disputed]
        if extra:
            sys.exit(f"{a.judge3} rules on {', '.join(extra)}, which runs 1 and 2 agree on: "
                     "run 3 judges the disputed claims only (section 10.1)")
    # Two claims are one group if any run put them in one (section 12.2), so joined through every run.
    parent = {c: c for c in order}

    def root(c):
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c

    for rows in (one, two, three):
        first = {}
        for c in order:
            if c in rows:
                g = rows[c]["group"]
                if g in first:
                    parent[root(c)] = root(first[g])
                else:
                    first[g] = c
    number = {}
    for c in order:
        number.setdefault(root(c), len(number) + 1)  # numbered by each group's first claim in claims.md's order
    lines = ["# Verdicts", "", "| Claim | Verdict | Group | Severity | Evidence |", "|---|---|---|---|---|"]
    for c in order:
        row = three[c] if c in disputed else one[c]
        severity = row["severity"] if row["verdict"] == "confirmed" else "-"
        source = f"run 3; run 1 {said(one[c])}; run 2 {said(two[c])}" if c in disputed else "runs 1 and 2 agree"
        lines.append(f"| {c} | {VERDICT_WORDS[row['verdict']]} | {number[root(c)]} | {severity} | {source} |")
    inputs = [f"{os.path.basename(p)} (sha256 {sha256_file(p)})" for p in (a.judge1, a.judge2, a.judge3) if p]
    notes = (f"Final verdicts by tools/control.py final (testing/CONTROL.md section 12.2), from "
             f"{', '.join(inputs[:-1])} and {inputs[-1]}. Agreement {rate(order, disputed)}. "
             + (f"Disputed, so run 3's: {', '.join(disputed)}. " if disputed else "No claim is disputed. ")
             + "Two claims are one group if any run put them in one.")
    write_text(a.out, "\n".join(lines + ["", "# Notes", "", notes, ""]))
    print(f"verdicts  {os.path.basename(a.out)} sha256 {sha256_file(a.out)} ({len(order)} claims, {len(number)} groups; "
          f"agreement {rate(order, disputed)}; disputed {', '.join(disputed) or 'none'})")


def ratio(x, y, digits):
    return "n/a" if not y else f"{float(Fraction(x) / Fraction(y)):.{digits}f}"


def minutes_arg(items, runs):
    """--minutes RUN=MINUTES ...: each run's time used, one value for each run in the key."""
    got = {}
    for item in items:
        m = re.fullmatch(r"([ABab][12])=(\d+(?:\.\d+)?)", item.strip())
        if not m:
            sys.exit(f"--minutes takes RUN=MINUTES, such as A1=17.8; got {item!r}")
        run = m.group(1).upper()
        if run in got:
            sys.exit(f"--minutes {run} is given twice")
        got[run] = Fraction(m.group(2))
        if got[run] <= 0:
            sys.exit(f"--minutes {run}: the time used must be more than 0")
    if set(got) != set(runs):
        sys.exit(f"--minutes needs one value for each run in the key ({', '.join(runs)}); got {', '.join(sorted(got)) or 'none'}")
    return got


def headline(m, minutes, runs):
    """Section 12.1: each run's headline measures; with four runs the within-arm differences, the floor and the reading."""
    value = {run: {"Confirmed per hour": Fraction(m[run]["confirmed"]) * 60 / minutes[run],
                   "Refuted per finding": Fraction(m[run]["refuted"], m[run]["findings"])} for run in runs}
    four = len(runs) == 4
    print("Headline measures, each run on its own (section 12.1):")
    if four:
        print("| Headline measure | Within A | Within B | Floor | A | B | Gap A - B | Reading |")
        print("|---|---|---|---|---|---|---|---|")
    else:
        print("| Headline measure | A | B | Gap A - B | Reading |")
        print("|---|---|---|---|---|")
    for label, digits, a_way in HEADLINE:
        def f(x, sign=""):
            return f"{float(x):{sign}.{digits}f}"
        if four:
            within = {arm: abs(value[arm + "1"][label] - value[arm + "2"][label]) for arm in "AB"}
            floor = max(within.values())
            mean = {arm: (value[arm + "1"][label] + value[arm + "2"][label]) / 2 for arm in "AB"}
            gap = mean["A"] - mean["B"]
            if gap == 0 or abs(gap) < floor:
                reading = "no difference"
            else:
                reading = "A's way" if (gap > 0) == (a_way > 0) else "B's way"
            print(f"| {label} | {f(within['A'])} | {f(within['B'])} | {f(floor)} | {f(mean['A'])} | {f(mean['B'])} "
                  f"| {f(gap, '+')} | {reading} |")
        else:
            gap = value["A1"][label] - value["B1"][label]
            print(f"| {label} | {f(value['A1'][label])} | {f(value['B1'][label])} | {f(gap, '+')} "
                  f"| against the first repo's floor (section 12.1) |")


def cmd_score(a):
    key = json.loads(read_text(a.key))
    claims = {c["code"]: c for c in key["claims"]}
    runs = sorted({c["run"] for c in key["claims"]})
    if set(runs) not in RUN_SETS:
        sys.exit(f"{a.key}: its runs are {', '.join(runs)}; score takes A1 and B1, or A1, A2, B1 and B2")
    minutes = minutes_arg(a.minutes, runs)
    v = parse_verdicts(a.verdicts, claims)
    for name, codes in (("--not-a-bug", a.not_a_bug), ("--accepted", a.accepted)):
        for code in codes:
            if code.upper() not in claims:
                sys.exit(f"{name} {code}: no such claim in the key")
    flipped = {v[c.upper()]["group"] for c in a.not_a_bug}
    for code, row in v.items():
        if row["group"] in flipped and row["verdict"] == "confirmed":
            row["verdict"], row["overridden"] = "refuted", True
    accepted = {v[c.upper()]["group"] for c in a.accepted}
    m, conf = {}, {}
    for run in runs:
        mine = [c for c in key["claims"] if c["run"] == run]
        groups = {}
        for c in mine:
            row = v[c["code"]]
            if row["verdict"] == "confirmed":
                groups[row["group"]] = max(groups.get(row["group"], 0), WEIGHTS[row["severity"]])
        conf[run] = groups
        m[run] = {"findings": len(mine),
                  "proven": sum(c["evidence"] == "probe" for c in mine),
                  "confirmed": len(groups),
                  "refuted": sum(v[c["code"]]["verdict"] == "refuted" for c in mine),
                  "cant": sum(v[c["code"]]["verdict"] == "cant-tell" for c in mine),
                  "weighted": sum(groups.values()),
                  "accepted": len(set(groups) & accepted)}
    # An arm's confirmed groups are its runs' together: unique to a run means no run of the other
    # arm confirmed that group; the overlap is one number per repo.
    by_arm = {arm: set().union(*[set(conf[run]) for run in runs if run[0] == arm]) for arm in "AB"}
    overlap = by_arm["A"] & by_arm["B"]
    for run in runs:
        m[run]["unique"] = len(set(conf[run]) - by_arm["B" if run[0] == "A" else "A"])
    rows = [
        ("Findings", lambda x, run: str(x["findings"])),
        ("Proven (a probe ran)", lambda x, run: f"{x['proven']} of {x['findings']}"),
        ("Confirmed (distinct bugs)", lambda x, run: str(x["confirmed"])),
        ("Refuted", lambda x, run: str(x["refuted"])),
        ("Can't tell", lambda x, run: str(x["cant"])),
        ("Unique to the arm", lambda x, run: str(x["unique"])),
        ("Overlap (confirmed by both)", lambda x, run: str(len(overlap))),
        ("Severity-weighted confirmed", lambda x, run: str(x["weighted"])),
        ("Accepted upstream", lambda x, run: str(x["accepted"])),
        ("Minutes", lambda x, run: f"{float(minutes[run]):g}"),
        ("Confirmed per hour", lambda x, run: ratio(x["confirmed"], minutes[run] / 60, 1)),
        ("Refuted per finding", lambda x, run: ratio(x["refuted"], x["findings"], 2)),
    ]
    print("| Measure | " + " | ".join(runs) + " |")
    print("|---|" + "---|" * len(runs))
    for label, fn in rows:
        print(f"| {label} | " + " | ".join(fn(m[run], run) for run in runs) + " |")
    print()
    headline(m, minutes, runs)
    print()
    print("Groups (the judge's numbers):")
    for g in sorted({row["group"] for row in v.values()}):
        parts = []
        for c in key["claims"]:
            row = v[c["code"]]
            if row["group"] == g:
                note = " (maintainer: not a bug)" if row.get("overridden") else ""
                sev = f", {row['severity']}" if row["verdict"] == "confirmed" else ""
                parts.append(f"{c['code']} ({c['run']} {c['arm_id']}: {row['verdict']}{sev}{note})")
        print(f"- {g}: " + "; ".join(parts))


def walk_strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for value in x.values():
            yield from walk_strings(value)
    elif isinstance(x, list):
        for value in x:
            yield from walk_strings(value)


def local(stamp):
    if isinstance(stamp, str):
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone()
    return datetime.fromtimestamp(stamp, tz=timezone.utc).astimezone()


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text")
    return ""


def prompt_text(text):
    """A prompt as --prompt compares it: line breaks as LF, whitespace at either end stripped."""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def cmd_session(a):
    first = first_text = first_full = last = None
    versions, modes, tools, attachments = Counter(), Counter(), Counter(), Counter()
    msgs, tool_ids, loads = {}, set(), []
    auto_mode = False
    terms = (list(LEAK_TERMS) if a.leak else []) + [t.lower().replace("\\", "/") for t in a.term]
    hits = {}
    with open(a.transcript, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            ts = o.get("timestamp")
            if ts and (last is None or local(ts) > last):
                last = local(ts)
            if "version" in o:
                versions[o["version"]] += 1
            if "permissionMode" in o:
                modes[o["permissionMode"]] += 1
            kind = o.get("type")
            if kind == "attachment":
                att = o.get("attachment") or {}
                attachments[att.get("type")] += 1
                auto_mode = auto_mode or att.get("type") == "auto_mode"
                # An instruction file Claude Code put in the context: a path to a CLAUDE.md or AGENTS.md.
                if att.get("type") != "prompt_snapshot":
                    for s in walk_strings(att):
                        t = s.strip().lower().replace("\\", "/")
                        entry = f"line {n} ({att.get('type')}): {s.strip()}"
                        if "/" in t and t.endswith(("/claude.md", "/claude.local.md", "/agents.md")) \
                                and entry not in loads:
                            loads.append(entry)
            if kind == "user" and first is None and ts and not o.get("isMeta"):
                text = text_of((o.get("message") or {}).get("content"))
                # Slash commands and their output are recorded as user lines too; a paste is a prompt.
                if text.strip() and not text.lstrip().startswith(("<command-", "<local-command-")):
                    first, first_text, first_full = local(ts), " ".join(text.split())[:70], text
            if kind == "assistant":
                msg = o.get("message") or {}
                rec = msgs.setdefault(msg.get("id") or f"line{n}", {"usage": Counter()})
                rec["model"] = msg.get("model") or rec.get("model")
                rec["requested"] = o.get("requestedModel") or rec.get("requested")
                rec["effort"] = o.get("effort") or rec.get("effort")
                for k, val in (msg.get("usage") or {}).items():
                    if isinstance(val, int):
                        rec["usage"][k] = max(rec["usage"][k], val)
                for part in msg.get("content") or []:
                    if isinstance(part, dict) and part.get("type") == "tool_use" and part.get("id") not in tool_ids:
                        tool_ids.add(part.get("id"))
                        tools[part.get("name")] += 1
            if terms:
                for s in walk_strings(o):
                    low = s.lower().replace("\\", "/")
                    found = [t for t in terms if t in low]
                    if a.leak:
                        found += [mt.group(0) for mt in LEDGER_ID.finditer(low)]
                    for t in found:
                        i = low.find(t)
                        context = " ".join(low[max(0, i - 40):i + len(t) + 40].split())
                        hits.setdefault((t, context), (n, kind))
    if first is None:
        sys.exit(f"{a.transcript}: no prompt found")
    usage = Counter()
    for rec in msgs.values():
        usage.update(rec["usage"])
    count = lambda key: ", ".join(f"{k} {c}" for k, c in Counter(r.get(key) for r in msgs.values()).most_common())
    fmt = lambda d: d.strftime("%Y-%m-%d %H:%M:%S %z")
    print(f"transcript      {os.path.basename(a.transcript)}")
    print(f"claude code     {', '.join(f'{k} ({c} lines)' for k, c in versions.most_common()) or 'not recorded'}")
    print(f"model           {count('model')}   (requests: {len(msgs)})")
    print(f"requested model {count('requested')}")
    print(f"effort          {count('effort')}")
    print(f"permission mode {', '.join(f'{k} {c}' for k, c in modes.most_common()) or 'not recorded'}"
          f"{'; auto mode notice present' if auto_mode else ''}")
    print(f"first prompt    {fmt(first)}   \"{first_text}\"")
    if a.prompt:
        # A first prompt that is one paste block and nothing else is compared by what is inside it:
        # the wrapper's two tag lines are stripped, nothing else, and the check says whether it
        # stripped them (Garrett, 2026-11-04).
        whole = prompt_text(first_full)
        block = PASTE.fullmatch(whole)
        mine = prompt_text(block.group(2)) if block else whole
        with open(a.prompt, "rb") as f:
            raw = f.read()
        theirs = prompt_text(raw.decode("utf-8-sig"))  # a byte-order mark isn't part of the text
        h, h2 = (hashlib.sha256(t.encode("utf-8")).hexdigest() for t in (mine, theirs))
        if block:
            tag = block.group(1)
            print(f'prompt wrapper  <pasted_content id="{tag}"> ... </pasted_content id="{tag}"> stripped before hashing')
        else:
            print("prompt wrapper  none stripped: the first prompt is not one paste block alone, so it is hashed as written")
        print(f"prompt sha256   {h} ({'inside its paste block' if block else 'as written'})")
        print(f"prompt file     {os.path.basename(a.prompt)}: {'matches' if h == h2 else 'does not match'}; "
              f"its text's sha256 {h2}, the file's sha256sum {hashlib.sha256(raw).hexdigest()}")
    start, start_from = first, "first prompt"
    if a.clone:
        st = os.stat(a.clone)
        born = local(getattr(st, "st_birthtime", st.st_ctime))
        print(f"clone created   {fmt(born)}")
        if born > start:
            start, start_from = born, "clone created"
    if a.report:
        end = local(os.stat(a.report).st_mtime)
        mins = (end - start).total_seconds() / 60
        print(f"report written  {fmt(end)}")
        print(f"time used       {mins:.1f} min (from {start_from} to report written)")
    print(f"last message    {fmt(last)}")
    total_in = usage["input_tokens"] + usage["cache_creation_input_tokens"] + usage["cache_read_input_tokens"]
    print(f"tokens          output {usage['output_tokens']:,}; input {total_in:,} "
          f"(new {usage['input_tokens']:,}, cache write {usage['cache_creation_input_tokens']:,}, "
          f"cache read {usage['cache_read_input_tokens']:,})")
    print(f"tools used      {', '.join(f'{k} {c}' for k, c in tools.most_common()) or 'none'}")
    print(f"attachments     {', '.join(f'{k} {c}' for k, c in attachments.most_common()) or 'none'}")
    print(f"instruction files loaded  {'; '.join(loads[:10]) if loads else 'none'}")
    if terms:
        if not hits:
            print("leak terms      none found")
        else:
            print(f"leak terms      {len(hits)} distinct hits; first 20:")
            for (t, context), (n, kind) in sorted(hits.items(), key=lambda kv: kv[1])[:20]:
                print(f"  line {n} ({kind}): {t!r} in \"{context}\"")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("shuffle", help="codes and order for the blind judge")
    s.add_argument("--run", nargs=2, action="append", required=True, metavar=("RUN", "FILE"),
                   help="a run (A1, A2, B1 or B2) and its findings file; two runs, or four")
    s.add_argument("--out", required=True, help="the judge's claims file to write")
    s.add_argument("--key", required=True, help="the key file to write")
    s.set_defaults(fn=cmd_shuffle)
    s = sub.add_parser("agreement", help="the judge's runs 1 and 2: agreement, disputed codes, claims-3.md")
    s.add_argument("key")
    s.add_argument("judge1", metavar="judge-1.md")
    s.add_argument("judge2", metavar="judge-2.md")
    s.add_argument("--claims", required=True, help="claims.md, as the shuffle wrote it")
    s.add_argument("--out", required=True, help="claims-3.md to write: the disputed claims, for run 3")
    s.set_defaults(fn=cmd_agreement)
    s = sub.add_parser("final", help="the final verdicts.md from the judge's runs")
    s.add_argument("key")
    s.add_argument("judge1", metavar="judge-1.md")
    s.add_argument("judge2", metavar="judge-2.md")
    s.add_argument("judge3", metavar="judge-3.md", nargs="?", help="run 3's verdicts on the disputed claims")
    s.add_argument("--out", required=True, help="verdicts.md to write")
    s.set_defaults(fn=cmd_final)
    s = sub.add_parser("score", help="measures from the key and the final verdicts")
    s.add_argument("key")
    s.add_argument("verdicts")
    s.add_argument("--minutes", nargs="+", required=True, metavar="RUN=MINUTES",
                   help="each run's time used, such as A1=17.8 B1=64")
    s.add_argument("--not-a-bug", action="append", default=[], metavar="CODE",
                   help="a maintainer said the filed issue for this claim's group is not a bug")
    s.add_argument("--accepted", action="append", default=[], metavar="CODE",
                   help="the filed issue for this claim's group was acknowledged or fixed upstream")
    s.set_defaults(fn=cmd_score)
    s = sub.add_parser("session", help="check one session transcript")
    s.add_argument("transcript")
    s.add_argument("--clone", help="the session's clone folder (its creation time)")
    s.add_argument("--report", help="the session's report file (its last write)")
    s.add_argument("--leak", action="store_true", help="scan for Dev Instincts terms and ledger ids")
    s.add_argument("--term", action="append", default=[], help="another text to scan for")
    s.add_argument("--prompt", help="the run's prompt file, to set beside the transcript's first prompt")
    s.set_defaults(fn=cmd_session)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
