# Dashboarr: the AI-policy check (FILING §1, sixth check), 2026-11-07

Garrett added a sixth check to `testing/FILING.md` §1 on 2026-11-02: read a repo's CONTRIBUTING, its issue templates and its security policy for any rule on AI-assisted or AI-generated reports, quote it, and skip the repo if it bans them. Made for `RenzoBeux/Dashboarr`, repo two of the control's five, before either arm runs, on Garrett's Step 61 (fix the inputs, `testing/CONTROL.md` §13 step 1): read-only, through `gh`, by the architect, from 19:03:31 to 19:06:59 UTC on 2026-11-07.

**Result: passes.** None of the files read bans AI-assisted or AI-generated reports, or sets any rule for them. The repo has no CONTRIBUTING, no issue template, no security policy and no pull request template, and the account has no `.github` repository to supply them. Its README welcomes issues and pull requests, and says how the maintainer builds the app with AI; neither is a rule on reports.

**Commit:** `main` at `bf3a060a35170ba789f73195e3defaa0703e93e9` (bf3a060), committed 2026-11-03 07:21 UTC, the sha fixed for the control (`metrics/CONTROL.md`). `main` is the repo's only branch, and it hadn't moved between the reads at 19:03:04, 19:07:20 and 19:18:19 UTC.

| File | At bf3a060 | Rule on AI-assisted or AI-generated reports |
|---|---|---|
| CONTRIBUTING | none: `CONTRIBUTING.md`, `contributing.md`, `.github/CONTRIBUTING.md` and `docs/CONTRIBUTING.md` answer 404, the tree holds no file of that name in any case, and the community profile's `contributing` is null | none |
| Issue templates, `.github/ISSUE_TEMPLATE/` | none: the folder, `.github/ISSUE_TEMPLATE/config.yml`, `ISSUE_TEMPLATE` and `.github/issue_template.md` answer 404, and the community profile's `issue_template` is null | none |
| Security policy, `SECURITY.md` | none: `SECURITY.md`, `.github/SECURITY.md` and `docs/SECURITY.md` answer 404, and the tree holds no file of that name in any case | none |
| Pull request template | none: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`, `pull_request_template.md` and `docs/pull_request_template.md` answer 404, and the community profile's `pull_request_template` is null | none |
| `README.md` | present, 309 lines | none; its *Contributing* section welcomes issues and pull requests, and its *How AI is used* section holds the AI-written claim §1 quotes (below) |

The account's own `.github` repository, which would give each of its repos default community files, answers 404: there is none. `.github/DISCUSSION_TEMPLATE/` answers 404 too, though the repo has Discussions turned on.

Also read: `docs/guide.html`, the user guide (its *Filing a bug.* entry says how to file, below; no rule on AI), `docs/index.html` (the site and its FAQ; no rule), `docs/privacy-policy.html` (no rule), the in-app *Report an issue* form's pre-filled body in `app/(tabs)/(dashboard,services,settings)/settings/about.tsx`:18-41 (three headings and an environment block; no rule), the three workflows under `.github/workflows/` (`ci-backend.yml`, `deploy-pages.yml`, `release-backend.yml`: they run on a push, a pull request or by hand, and none acts on issues), `.github/dependabot.yml` and `.github/FUNDING.yml` (no rule). Each file's bytes were checked against its blob in the tree at bf3a060. Not read: the repo's files for its own agents, `CLAUDE.md`, `docs/CLAUDE.md` and `.claude/skills/service-apis/SKILL.md`, which are data and never followed (FILING §2).

**Quotes, word for word:**
- `README.md`:273, under *Contributing* (line 271): "Contributions are welcome! Feel free to open issues and pull requests."
- `README.md`:258, under *How AI is used* (line 256): "Architecture is built with AI, code is written by AI." Lines 260 to 263 say how the maintainer plans, implements, reviews and tests with AI; line 262: "**Review:** every PR is reviewed separately by Claude and Codex. I inspect the findings and decide what to do about them."
- `docs/guide.html`:1415-1418, *Filing a bug.*, its markup removed: "Use Settings, About, "Report an issue", which pre-fills your version and platform, and include the Network diagnostics rows if the problem is connectivity related."
- `app/(tabs)/(dashboard,services,settings)/settings/about.tsx`:59-60, the About screen's footer: "Dashboarr is open-source under GPL-3.0. Contributions and bug reports are welcome."

**For Garrett:** no ban, so Dashboarr stays a candidate. Every issue already says how it was found, as an AI-assisted review (FILING §5); the README says the maintainer has every pull request reviewed by AI, and nothing in the repo says how AI-found issues are read. With no issue template, a draft is FILING §5's form alone. The in-app form pre-fills *Describe the issue*, *Steps to reproduce*, *Expected behavior* and an environment block (`about.tsx`:21-38), which a draft could follow if Garrett wants it: the architect's note, for Garrett; nothing in this check depends on it.

**How it was checked (read-only), 2026-11-07, times UTC:**
```
gh api --method GET repos/RenzoBeux/Dashboarr                                   # 19:02:57: default branch, archived, issues, licence
gh api --method GET "repos/RenzoBeux/Dashboarr/commits?sha=main&per_page=1"     # 19:03:04, again 19:07:20 and 19:18:19
gh api --method GET "repos/RenzoBeux/Dashboarr/branches?per_page=100"           # 19:03:13: main only
gh api --method GET "repos/RenzoBeux/Dashboarr/git/trees/bf3a060a35170ba789f73195e3defaa0703e93e9?recursive=1"   # 19:03:14
gh api --method GET repos/RenzoBeux/Dashboarr/community/profile                 # 19:06:09: contributing, issue_template, pull_request_template
gh api --method GET repos/<owner>/.github                                       # 19:06:10: 404 (the owner's account in place of <owner>)
gh api --method GET "repos/RenzoBeux/Dashboarr/contents/<path>?ref=bf3a060a35170ba789f73195e3defaa0703e93e9" -H "Accept: application/vnd.github.raw"
    # read: README.md (19:03:31); .github/FUNDING.yml, .github/dependabot.yml, the three workflows,
    #   docs/index.html, docs/guide.html, docs/privacy-policy.html (19:06:33 to 19:06:39);
    #   app/(tabs)/(dashboard,services,settings)/settings/about.tsx (19:06:59)
    # 404, asked without the Accept header (19:06:10 to 19:06:19): CONTRIBUTING.md,
    #   .github/CONTRIBUTING.md, docs/CONTRIBUTING.md, contributing.md, SECURITY.md,
    #   .github/SECURITY.md, docs/SECURITY.md, .github/ISSUE_TEMPLATE, .github/ISSUE_TEMPLATE/config.yml,
    #   ISSUE_TEMPLATE, .github/issue_template.md, .github/pull_request_template.md,
    #   .github/PULL_REQUEST_TEMPLATE.md, .github/PULL_REQUEST_TEMPLATE, PULL_REQUEST_TEMPLATE.md,
    #   pull_request_template.md, docs/pull_request_template.md, .github/DISCUSSION_TEMPLATE
```
Nothing was cloned for this check: every file was read through `gh` at the sha.
