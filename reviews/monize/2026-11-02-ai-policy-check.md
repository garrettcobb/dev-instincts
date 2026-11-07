# Monize: the AI-policy check (FILING §1, sixth check), 2026-11-02

Garrett added a sixth check to `testing/FILING.md` §1 on 2026-11-02: read a repo's CONTRIBUTING, its issue templates and its security policy for any rule on AI-assisted or AI-generated reports, quote it, and skip the repo if it bans them. Monize's round (`2026-11-02-93f4e68-review`) came before the check, so it was made afterwards, read-only, by the architect, at 23:40 local time (UTC-6) on 2026-11-02.

**Result: passes.** None of these files bans AI-assisted or AI-generated reports, or sets any rule for them. Monize's AI rules are for pull requests: disclose AI assistance and own the result.

**Commit:** `main` at `93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9` (93f4e68), the round's sha; the branch hadn't moved at the time of the check.

| File | At 93f4e68 | Rule on AI-assisted or AI-generated reports |
|---|---|---|
| `CONTRIBUTING.md` | present, 66 lines | none for reports; its AI rules cover pull requests (quoted below) |
| Issue templates, `.github/ISSUE_TEMPLATE/` | none: the folder doesn't exist (the contents API answers 404, and the community profile's `issue_template` is null) | none |
| `SECURITY.md` | present, 100 lines | none; the nearest is a scope line on automated scanners (below) |
| `.github/pull_request_template.md` | present, 36 lines | none for reports; an AI disclosure section for pull requests (below) |

Also read: `.github/DISCUSSION_TEMPLATE/announcements.md` (it sends bug reports to Issues; no AI rule), `.github/workflows/pr-checklist.yml` (no AI rule; it checks a pull request for an approved link and a ticked checklist) and `README.md` (the AI-written claim §1 quotes, at line 7; no rule on reports).

**Quotes, word for word:**
- `CONTRIBUTING.md`:7: "Monize has run into a recurring set of problems with unsolicited, AI-generated contributions:". The four lines under it are about pull requests and code: large PRs, the quality of AI-generated code, overlapping work, and the maintainer's cost of triage and QA.
- `CONTRIBUTING.md`:30, under *Pull request rules*: "**Disclose AI assistance and own the result.** Using AI to write code is fine and expected. The author is responsible for the correctness, conventions, and tests of what they submit — "the AI wrote it" is not an excuse for an unreviewed or untested change."
- `CONTRIBUTING.md`:54, under *Before you open a PR*: "AI assistance is disclosed, and you've reviewed and own the result."
- `.github/pull_request_template.md`:36: "Disclose any AI tools used. Using AI is fine and expected — you remain responsible for correctness, conventions, and tests."
- `SECURITY.md`:68, out of scope for security reports: "Findings from automated scanners without a demonstrated, exploitable impact."

**For Garrett:** no ban, so monize stays a candidate. Every issue already says how it was found, as an AI-assisted review (FILING §5), which is the disclosure the repo asks of pull requests. A security finding goes to Garrett, never into an issue (FILING §4), so the scanner line doesn't bear on a filed issue. Line 7's "unsolicited, AI-generated contributions" is the reason the repo gives for its propose-first workflow for pull requests; it doesn't say how the maintainer reads AI-found issues.

**How it was checked (read-only):**
```
gh api --method GET repos/kenlasko/monize                              # default branch, archived, issues, licence
gh api --method GET "repos/kenlasko/monize/commits?sha=main&per_page=1"
gh api --method GET repos/kenlasko/monize/community/profile            # contributing, issue_template, pull_request_template
gh api --method GET "repos/kenlasko/monize/git/trees/93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9?recursive=1"
gh api --method GET "repos/kenlasko/monize/contents/<path>?ref=93f4e685dc8b46e97adc8be2c7ed2ace766d7ee9" -H "Accept: application/vnd.github.raw"
    # CONTRIBUTING.md, SECURITY.md, .github/pull_request_template.md, README.md,
    # .github/DISCUSSION_TEMPLATE/announcements.md, .github/workflows/pr-checklist.yml;
    # .github/ISSUE_TEMPLATE: 404
```
The scratch clone (`.instinct-scratch/file/monize/`, a sparse checkout) holds none of these files, so they were read through `gh`.
