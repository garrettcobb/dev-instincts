"""Regenerate ledger/STATS.md from ledger/findings.jsonl and ledger/projects.json.

The agent reads STATS.md first: its check order is the order in which it
checks a change, so the instincts that have cost the most get looked at first.

Only the developer's own projects and AI-written outside projects feed the
check order. Human-written outside projects (mined for calibration) get their
own reference section, so a few big human repos can't bury the developer's
own record.

Run from the repo root:  python3 tools/stats.py
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "ledger" / "findings.jsonl"
PROJECTS = ROOT / "ledger" / "projects.json"
OUT = ROOT / "ledger" / "STATS.md"
CONTROL = ROOT / "testing" / "CONTROL.md"
# The control block's state line in testing/CONTROL.md section 5.2. While it reads
# open, rows tagged control:B (bugs only the plain session found) stay out of the
# check orders, so the frozen reviewer under test doesn't learn from the arm it is
# measured against (Garrett's ruling, 2026-11-06).
BLOCK_LINE = re.compile(r"^Block 1: (open|closed \d{4}-\d{2}-\d{2})\.$", re.MULTILINE)
HELD_TAG = "control:B"

# How much a miss of each severity costs. Data loss and security outrank a crash:
# a crash is seen at once, while lost data or a hole can go unseen.
WEIGHT = {
    "data-loss": 8,
    "security": 8,
    "wrong-result": 5,
    "crash": 4,
    "stuck": 2,
    "process": 2,
    "cosmetic": 1,
}
AUTHORSHIP = {"ai", "human", "mixed"}
OPEN = {"open", "not-fixed", "partly-fixed", "fixed-with-problem", "fixed-claimed"}
SEVERITIES = list(WEIGHT)
RANK_HEADER = [
    "#",
    "Instinct",
    "Findings",
    "Score",
    "Worst",
    "Regressions",
    "Open or unverified",
]


def instinct_titles():
    text = (ROOT / "DEV-INSTINCTS.md").read_text(encoding="utf-8")
    return {
        int(n): t.strip()
        for n, t in re.findall(r"^### (\d+)\. (.+)$", text, re.MULTILINE)
    }


def load_projects():
    projects = json.loads(PROJECTS.read_text(encoding="utf-8"))
    codes = Counter(p.get("code") for p in projects.values())
    for name, p in projects.items():
        missing = {"code", "kind", "authorship", "own"} - p.keys()
        if missing:
            raise SystemExit(f"projects.json: {name} is missing {sorted(missing)}")
        if p["authorship"] not in AUTHORSHIP:
            raise SystemExit(
                f"projects.json: {name} authorship must be one of {sorted(AUTHORSHIP)}"
            )
        if codes[p["code"]] > 1:
            raise SystemExit(f"projects.json: code {p['code']} is used twice")
    return projects


def load(projects):
    rows = []
    for number, line in enumerate(
        LEDGER.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as problem:
            raise SystemExit(
                f"ledger line {number} isn't valid JSON: {problem}"
            ) from None
        if row["project"] not in projects:
            raise SystemExit(
                f"ledger line {number}: project {row['project']!r} isn't in "
                "ledger/projects.json. Register it first."
            )
        if row.get("authorship", "ai") not in AUTHORSHIP:
            raise SystemExit(
                f"ledger line {number}: authorship must be one of {sorted(AUTHORSHIP)}"
            )
        rows.append(row)
    return rows


def authorship(row, projects):
    """A finding's own authorship if it has one, otherwise its project's."""
    return row.get("authorship") or projects[row["project"]]["authorship"]


def in_check_order(row, projects):
    """The developer's own projects always count; outside projects only when
    the code was AI-written, which is the situation the reviewer is for."""
    return projects[row["project"]]["own"] or authorship(row, projects) == "ai"


def block_open():
    """True while testing/CONTROL.md's block state line reads open. Exactly one
    such line must exist; otherwise stop before anything is written."""
    if not CONTROL.exists():
        raise SystemExit(
            f"{CONTROL.relative_to(ROOT)} is missing: it must hold one "
            "'Block 1: open.' or 'Block 1: closed <date>.' line (section 5.2)."
        )
    found = BLOCK_LINE.findall(CONTROL.read_text(encoding="utf-8"))
    if len(found) != 1:
        raise SystemExit(
            f"{CONTROL.relative_to(ROOT)} must hold exactly one 'Block 1: open.' or "
            f"'Block 1: closed <date>.' line (section 5.2); found {len(found)}."
        )
    return found[0] == "open"


def held_out(row, open_block):
    """A control:B row is held out of the check order while the block is open."""
    return open_block and HELD_TAG in row.get("tags", [])


def proposed_tags(row):
    return [t for t in row.get("tags", []) if t.startswith("proposed:")]


def score(row):
    weight = WEIGHT.get(row["severity"], 1)
    return weight * (2 if row.get("origin") in ("regression", "carry-over") else 1)


def worst(found):
    sev = Counter(r["severity"] for r in found)
    return next((s for s in SEVERITIES if sev[s]), "")


def group(rows):
    by_instinct = defaultdict(list)
    for row in rows:
        for n in row.get("instincts", []):
            by_instinct[n].append(row)
    return by_instinct


def rank(by_instinct, titles):
    ranked = sorted(
        by_instinct.items(),
        key=lambda item: (-sum(score(r) for r in item[1]), item[0]),
    )
    return [
        [
            n,
            titles.get(n, "(not in DEV-INSTINCTS.md)"),
            len(found),
            sum(score(r) for r in found),
            worst(found),
            sum(1 for r in found if r.get("origin") == "regression"),
            sum(1 for r in found if r["status"] in OPEN),
        ]
        for n, found in ranked
    ]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def kind_sections(rows, projects, titles, heading, note):
    """A ranking per kind of software, top 15, so a desktop app isn't checked
    in a web app's order or the reverse."""
    out = []
    for kind in sorted({projects[r["project"]]["kind"] for r in rows}):
        subset = [r for r in rows if projects[r["project"]]["kind"] == kind]
        names = sorted({r["project"] for r in subset})
        out += [
            heading.format(kind=kind),
            "",
            f"From {len(subset)} findings in {', '.join(names)}. {note}",
            "",
            table(RANK_HEADER, rank(group(subset), titles)[:15]),
            "",
        ]
    return out


def percent(part, whole):
    return f"{round(100 * part / whole)}%" if whole else "-"


def coverage(rows, projects):
    """For each outside project: how much of it the instincts already cover.
    A falling 'fit nothing' share across projects of one kind means the
    instincts cover that kind; a high one means there are classes to draft."""
    out = []
    for name in sorted({r["project"] for r in rows}):
        p = projects[name]
        if p["own"]:
            continue
        found = [r for r in rows if r["project"] == name]
        fit = sum(1 for r in found if r.get("instincts"))
        draft = sum(1 for r in found if not r.get("instincts") and proposed_tags(r))
        nothing = len(found) - fit - draft
        out.append(
            [
                name,
                p["kind"],
                p["authorship"],
                len(found),
                percent(fit, len(found)),
                percent(draft, len(found)),
                percent(nothing, len(found)),
            ]
        )
    return out



def targets(rows):
    """Escape rate per project and for its latest rounds, against the goals, and the
    senior coder's severity-weighted hit rate from scored design notes."""
    own = [r for r in rows if r.get("origin") and r.get("origin") != "external"]
    out = []
    for project in sorted({r["project"] for r in own}):
        mine = [r for r in own if r["project"] == project]
        rounds = list(dict.fromkeys(r["round"] for r in mine))  # ledger order = time order
        recent = [r for r in mine if r["round"] in rounds[-5:]]
        for label, rs in (("all rounds", mine), ("last 5 rounds", recent)):
            esc = sum(1 for r in rs if r["origin"] == "escaped")
            reg = sum(1 for r in rs if r["origin"] == "regression")
            out.append([project, label, len(rs), f"{esc} ({percent(esc, len(rs))})",
                        f"{reg} ({percent(reg, len(rs))})"])
    # The hit rate scores predictions, not finds (Garrett, 2026-11-01). A finding
    # with caught_by "senior-coder" came from a note's own break cases, so the note
    # can't have missed it: counting those gave 72 of 73 (99%) by construction.
    # Only findings caught by someone else (the reviewer, the developer, a user)
    # on a rule a note covered are scored; the notes' own finds are counted apart.
    noted = [r for r in rows if isinstance(r.get("design_note"), dict)
             and r["design_note"].get("verdict") in ("predicted", "partly", "missed")]
    own_finds = [r for r in noted if r.get("caught_by") == "senior-coder"]
    scored = [r for r in noted if r.get("caught_by") != "senior-coder"]
    finds = f"; the notes' own finds ({len(own_finds)}, caught_by senior-coder) aren't scored"
    if scored:
        got = sum(WEIGHT[r["severity"]] * {"predicted": 1, "partly": 0.5, "missed": 0}[r["design_note"]["verdict"]] for r in scored)
        whole = sum(WEIGHT[r["severity"]] for r in scored)
        verdicts = Counter(r["design_note"]["verdict"] for r in scored)
        told = ", ".join(f"{verdicts[v]} {v}" for v in ("predicted", "partly", "missed") if verdicts[v])
        hit = (f"{got:g} of {whole} ({percent(got, whole)}) over {len(scored)} findings caught by "
               f"others on a rule a note covered ({told}){finds}")
    else:
        hit = ("no finding caught by someone else has been scored against a note yet "
               f"(calibration: 23 of 28, 82%, see agent/senior-coder.md){finds}")
    return out, hit

def main():
    projects = load_projects()
    rows = load(projects)
    titles = instinct_titles()
    open_block = block_open()
    held = [r for r in rows if in_check_order(r, projects) and held_out(r, open_block)]
    counted = [
        r for r in rows if in_check_order(r, projects) and not held_out(r, open_block)
    ]
    reference = [r for r in rows if not in_check_order(r, projects)]
    held_note = (
        f"{len(held)} rows tagged `{HELD_TAG}` are left out of it while the block "
        "state line in testing/CONTROL.md §5.2 reads open; "
        if open_block
        else ""
    )
    by_instinct = group(rows)
    unknown = sorted(n for n in by_instinct if n not in titles)
    priority = rank(group(counted), titles)
    never = [n for n in sorted(titles) if n not in by_instinct]

    waiting = defaultdict(list)
    for r in rows:
        for tag in proposed_tags(r):
            waiting[tag.removeprefix("proposed:")].append(r)
    unclassified = [
        r
        for r in counted
        if not r.get("instincts")
        and "fidelity" not in r.get("tags", [])
        and not proposed_tags(r)
    ]

    target_rows, senior_hit = targets(rows)
    lines = [
        "# Ledger statistics",
        "",
        (
            "Generated by `tools/stats.py` from `findings.jsonl` and `projects.json`. "
            "Don't edit by hand."
        ),
        "",
        (
            f"**{len(rows)} findings** across "
            f"{len({r['project'] for r in rows})} project(s) and "
            f"{len({(r['project'], r['round']) for r in rows})} round(s). "
            f"{len(counted)} feed the check order; {held_note}{len(reference)} are reference "
            "data from human-written outside projects. "
            f"Open or unverified: {sum(1 for r in rows if r['status'] in OPEN)}."
        ),
        "",
        "## Check order, all kinds (highest cost first)",
        "",
        "From the developer's own projects and AI-written outside projects only. "
        "Score = severity weight × 2 for a regression or carry-over, summed over every "
        "finding that instinct covers. Weights: "
        + ", ".join(f"{k} {v}" for k, v in WEIGHT.items())
        + ". Check a change against the top of this table first.",
        "",
        table(RANK_HEADER, priority),
        "",
        *kind_sections(
            counted,
            projects,
            titles,
            "## Check order for a {kind} (top 15)",
            "Use this order when reviewing this kind of software.",
        ),
        "## Reference: human-written outside projects",
        "",
        (
            "Mined from mature open-source projects to test and widen the instincts. "
            "Not part of the check order: these show what experienced human teams "
            "still miss, which isn't the same as what AI-written code gets wrong."
        ),
        "",
        *(
            kind_sections(
                reference,
                projects,
                titles,
                "### Most costly instincts in human-written {kind}s (top 15)",
                "Reference only.",
            )
            if reference
            else ["None mined yet.", ""]
        ),
        "## Coverage of outside projects",
        "",
        (
            "How much of each outside project's record the instincts already cover. "
            "'Fit nothing' is the share no approved instinct or draft covers: when it "
            "stays low across new projects of one kind, the instincts cover that kind."
        ),
        "",
        table(
            [
                "Project",
                "Kind",
                "Authorship",
                "Findings",
                "Fit an instinct",
                "Fit only a draft",
                "Fit nothing",
            ],
            coverage(rows, projects),
        ),
        "",
        "## By severity",
        "",
        table(
            ["Severity", "Findings", "Open"],
            [
                [
                    s,
                    sum(1 for r in rows if r["severity"] == s),
                    sum(1 for r in rows if r["severity"] == s and r["status"] in OPEN),
                ]
                for s in SEVERITIES
            ],
        ),
        "",
        "## Who caught them",
        "",
        (
            "If a class is only ever caught by domain testing or verification, the review that "
            "came before missed it: that's where the reviewer's instincts are weakest."
        ),
        "",
        table(
            ["Caught by", "Findings"],
            Counter(r["caught_by"] for r in rows).most_common(),
        ),
        "",
        "## By round",
        "",
        table(
            ["Project", "Round", "Findings", "Regressions", "Carry-overs"],
            [
                [
                    p,
                    rd,
                    n,
                    sum(
                        1
                        for r in rows
                        if (r["project"], r["round"]) == (p, rd)
                        and r.get("origin") == "regression"
                    ),
                    sum(
                        1
                        for r in rows
                        if (r["project"], r["round"]) == (p, rd)
                        and r.get("origin") == "carry-over"
                    ),
                ]
                for (p, rd), n in Counter(
                    (r["project"], r["round"]) for r in rows
                ).items()
            ],
        ),
        "",
        "## Targets",
        "",
        (
            "Goals set by the developer (2026-11-01): escape rate under 5%, the high-performing mark "
            "(industry average 10 to 15%); regressions under 10% of fixes; the senior coder's "
            "prediction rate at 95% (bar to stay in the loop: 82%). Escaped means a review covering "
            "that code had already passed it. Regressions here are a share of findings; per fix, see "
            "metrics/CONVERGENCE.md."
        ),
        "",
        table(["Project", "Rounds", "Findings", "Escaped", "Regressions"], target_rows),
        "",
        f"Senior coder hit rate (severity-weighted): {senior_hit}.",
        "",
        "## Status",
        "",
        table(["Status", "Findings"], Counter(r["status"] for r in rows).most_common()),
        "",
        "## The reviewer's own record",
        "",
        (
            "Escapes are findings that slipped past a review covering that code; rejected are "
            "findings the developer judged not a defect. Falling escapes with few rejections is "
            "the sign the reviewer is getting better."
        ),
        "",
        table(
            ["Measure", "Count"],
            [
                [
                    "Found by the instinct reviewer",
                    sum(1 for r in rows if r["caught_by"] == "instinct-reviewer"),
                ],
                [
                    "Rejected (false positives)",
                    sum(1 for r in rows if r["status"] == "rejected"),
                ],
                [
                    "Escaped a review",
                    sum(1 for r in rows if r.get("origin") == "escaped"),
                ],
                [
                    "Other projects' own escapes (calibration data)",
                    sum(1 for r in rows if r.get("origin") == "external"),
                ],
                [
                    "Pre-existing, found later",
                    sum(1 for r in rows if r.get("origin") == "pre-existing"),
                ],
                [
                    "Regressions from fixes",
                    sum(1 for r in rows if r.get("origin") == "regression"),
                ],
                [
                    "Carry-overs (known, left unfixed)",
                    sum(1 for r in rows if r.get("origin") == "carry-over"),
                ],
                [
                    "Claimed fixed, not yet verified",
                    sum(1 for r in rows if r["status"] == "fixed-claimed"),
                ],
            ],
        ),
        "",
        "## Findings waiting on a proposed instinct",
        "",
        (
            "Findings tagged `proposed:<slug>` fit a draft in `proposals/` that isn't approved yet. "
            "A draft that keeps collecting findings has earned its number; one that collects none "
            "after several reviews may not be real."
        ),
        "",
        table(
            ["Proposal", "Findings", "Score", "Worst", "IDs"],
            [
                [
                    label,
                    len(found),
                    sum(score(r) for r in found),
                    worst(found),
                    ", ".join(r["id"] for r in found),
                ]
                for label, found in sorted(
                    waiting.items(), key=lambda item: -sum(score(r) for r in item[1])
                )
            ],
        )
        if waiting
        else "None yet.",
        "",
        "## Gaps in the ledger",
        "",
        (
            f"- Instincts with no finding yet: {', '.join(map(str, never)) or 'none'}. "
            "These came from process misses; they still go on the checklist."
        ),
        (
            f"- Findings in the check order with no instinct or draft (classify these on the "
            f"next run): {', '.join(r['id'] for r in unclassified) or 'none'}."
        ),
        (
            f"- Instinct numbers used in the ledger but missing from DEV-INSTINCTS.md: "
            f"{', '.join(map(str, unknown)) or 'none'}."
        ),
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(
        f"{len(rows)} findings ({len(counted)} in the check order, "
        f"{len(reference)} reference), {len(priority)} instincts ranked "
        f"-> {OUT.relative_to(ROOT)}"
    )
    if unknown:
        raise SystemExit(
            f"instincts {unknown} are in the ledger but not in DEV-INSTINCTS.md"
        )


if __name__ == "__main__":
    main()
