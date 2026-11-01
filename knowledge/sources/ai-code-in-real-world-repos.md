# A Large-Scale Empirical Study of AI-Generated Code in Real-World Repositories
- **Source:** arXiv:2603.27130v2 [cs.SE], 3 Apr 2026. Tianhao Mao, Dongfang Zhao, Haixu Tang, Hang Zhang (Indiana University Bloomington); Xiaofeng Wang (Nanyang Technological University). CC BY 4.0. No URL in the text beyond the arXiv ID.
- **Type:** preprint
- **Evidence strength:** moderate — large matched sample (19,816 AI files / 12,749 commits vs 36,467 same-repo, same-language, similar-size human files) with significance tests and effect sizes; but AI code is found through self-attribution comments plus an LLM classifier (sampled precision 85–88%), most effects are small, and it covers public GitHub only. No vendor conflict.

## Claims
Method
- Initial pull: 31,726 commits, 44,616 files with comments naming LLM tools. Rule filtering left 4,882 commits / 8,141 files (manual check TP=88/100, TN=95/100). An LLM classifier (ChatGPT 5-mini) added 7,867 commits / 10,713 files (check TP=85/100, TN=93/100); 686 more positives were labelled by hand. Final set: 12,749 commits, 19,816 AI files.
- Each AI file is matched with two human files from the same repo and language, within 20% LOC where possible (36,467 human files).
- ChatGPT dominates; Python and JavaScript are the most common languages.

Code level
- AI files are bigger: physical LOC 256.57 vs 192.68; source LOC 171.47 vs 132.14; blank-line ratio 15.15% vs 13.46%. Comment ratio is about equal (18.01% vs 17.96%), so the extra size is code, not comments.
- Per function: more unique operators (8.79 vs 6.09, d=0.489), higher content ratio (35.91% vs 23.51%, d=0.658), lower lexical density (0.531 vs 0.692, d=−0.555).
- Per function: 8.20 vs 5.59 statements (+2.61), slightly more conditions, loops and parameters; effect sizes small (d<0.2).
- Cyclomatic complexity barely differs (2.62 vs 2.47, d=0.030). Max nesting depth 0.787 vs 0.582 (d=0.172). AI nests loops more; humans nest conditions and booleans slightly more.
- Halstead: AI functions are uniformly moderate; human code is heavy-tailed (a few very large functions).
- Per file: humans have more functions (11.67 vs 6.62) and larger ones (201.82 vs 138.97 AST nodes); AI has slightly more methods (4.95 vs 4.59). Recursion slightly rarer in AI (0.476 vs 0.525 recursive functions per file).
- Duplication is lower in AI: duplicated lines 18.69% vs 25.89%; cross-file duplicated lines 17.20% vs 24.52%; within-file about equal (1.86% vs 1.72%). AI has more clone instances per file (0.679 vs 0.534). The authors read this as AI writing one-off code instead of reusing shared utilities, and duplicating in small fragments.
- OOP differs by language: C++ human classes far more complex and coupled (WMC 31.52 vs 15.79; CBO 4.60 vs 1.22); Java near parity; Python AI slightly lower WMC/CBO and higher RFC (8.95 vs 7.62).
- Control-flow and data-flow graphs are slightly larger but less dense in AI code. Call graphs are the same size but deeper (depth 2.03 vs 1.89, d=0.108; diameter 3.06 vs 2.80). The authors call this a "layered" structure.
- CodeQL alerts per KLOC: total 12.81 vs 11.58; errors equal (0.840 vs 0.846); critical security slightly lower in AI (0.042 vs 0.052); high security 0.934 vs 0.464; medium 0.282 vs 0.182.
- The top CWEs are the same for both: CWE-563 unused assignment (32.3% of AI alerts), CWE-561 dead code (9.08%), CWE-396 catching generic exceptions (6.28%). AI-heavier secondary ones: CWE-20 input validation (2.88%), CWE-400 resource consumption (2.63%), CWE-117 log injection (2.34%). Human-heavier: CWE-208, CWE-772, CWE-570.
- By language (alerts/KLOC): JavaScript AI 13.98 vs 6.25, high-risk 4.02 vs 1.14. TypeScript is the reverse (high-risk 0.078 AI vs 0.794 human). Total alerts are higher in AI for C, C++, C#; lower for Java, Python, Ruby, TypeScript.
- Secrets per 10k lines: AI has more API keys/tokens (0.194 vs 0.098) and private keys (0.021 vs 0.006); humans have more hardcoded passwords (1.02 vs 0.703) and simple passwords (0.811 vs 0.512).

Commit level
- AI commits are slightly more often outside work hours (0.372 vs 0.358) and less often within 30 days before a release (0.622 vs 0.694).
- AI commits are smaller: mean files changed 92.85 vs 344.64; lines churned 24.70 vs 152.02 (means with very large SDs).
- Merge commits: 0.126 AI vs 0.000 human.
- Little difference at 7 days. At 30/90 days AI files are revisited more: files touched within 90 days 0.020 vs 0.003; touches 0.050 vs 0.004; line churn 3.19 vs 0.275; authors 0.024 vs 0.003. Stabilization 0.658 vs 0.035 days. Fixing commits within 14 days 0.003 vs 0.001. Reverts: no difference.
- First edit after 26.16 vs 11.10 days; handoff latency 28.28 vs 11.23 days (not significant in the matched pairwise tests).
- Most medians are zero: the maintenance effects come from a subset of commits.
- Conclusion: the main risk is structural inefficiency (verbosity, less reuse, fragmented logic), not correctness failure. This is the authors' reading of the pattern; they don't measure its cost.

## What humans catch that AI misses (per this source)
- Existing shared utilities: humans reuse them, while AI writes each piece fresh.
- Compression: humans write the same logic in fewer, denser constructs, while AI spells it out in extra statements, loops and nesting.
- Security-relevant patterns: AI code has about twice the high-severity CodeQL alerts per KLOC, and JavaScript is the worst.
- Token and key handling: AI more often leaves API keys, tokens and private keys in code.

## Checks for the reviewer
- Unused assignments and dead code (the top CWEs in both groups). Detect: ruff F841, pylint unused-variable, eslint no-unused-vars, TS `noUnusedLocals`, CodeQL if present, on the diff. → NEW: An unused input is an ignored requirement.
- Hardcoded tokens, API keys, private keys. Detect: regex scan of diff and config: `-----BEGIN [A-Z ]*PRIVATE KEY-----`, `(api[_-]?key|secret|token|passw(or)?d)\s*[:=]\s*["'][^"']{8,}`, long hex/base64 literals; gitleaks only if already in the project. → NEW: No secrets in code.
- Log injection (CWE-117): user-controlled text written to logs unsanitized. Detect: log calls interpolating `request.` data; check CR/LF stripping. → NEW: No debug leftovers; logs and errors don't leak.
- Resource consumption (CWE-400): unbounded reads, loops over user-sized input, no size or row caps. Detect: `.read()` with no size, `readlines()`, unpaginated `.objects.all()` in views, upload handlers without limits. → #9, #13.
- Input validation (CWE-20). → #9 (fuzz every POST route).
- Generic catch, or error detected with no action (CWE-396, CWE-390). Detect: `except:` / `except Exception:` followed by `pass`, `continue` or a default return; `catch (e) {}`. → #25, #18.
- Plain-JavaScript front-end files get the security pass first (highest AI high-risk density; TypeScript the opposite). Detect: `.js/.jsx` in the diff; run the project's eslint/semgrep security rules if installed. → NEW: Security-scan every AI change.
- Fragmented duplication. Detect: jscpd (if installed) on changed files against the repo; flag small repeated blocks within a file and near-copies of existing helpers. → NEW: Use what's already there.
- Layering. Detect: max nesting above 3 (ruff PLR1702, eslint max-depth); functions whose body only calls another function with the same arguments. → NEW: Every abstraction earns its place.
- Late churn. Re-review AI-heavy files 30 and 90 days after merge; count follow-up commits (`git log --since=... --follow <file>`). → #30.

## Over-engineering signals (if relevant)
- More statements per function for the same job. Detect: compare diff size against a minimal rewrite; statements per function.
- Deeper nesting and deeper call chains with the same number of functions. Detect: max nesting depth, call depth.
- Class/method organisation where free functions would do. Detect: classes with one method and no state (pylint too-few-public-methods).
- Small fragments repeated instead of one shared helper. Detect: clone instances per file.

## Process lessons for a non-coder directing AI
- AI shifts effort from writing to validation and maintenance. Budget review and testing beyond the first week.
- Treat AI output as a draft to consolidate: deduplicate, simplify, flatten, reuse.
- Developers in the sample used AI less in the 30 days before a release, keeping it away from stability-critical stages (the authors' interpretation).

## Quotes
- "the primary risk is not correctness failure, but structural inefficiency"
- "Developers may benefit from treating AI outputs as drafts to be consolidated"

## Caveats
- Selection bias: it only includes code whose authors labelled AI use in comments. ChatGPT, Python and JavaScript dominate.
- Most effect sizes are small; the authors note the large sample makes small effects significant.
- It measures code after humans selected and edited it, so model behaviour and human integration are mixed.
- "Lower duplication = less reuse" is the authors' interpretation; it could also just mean less copy-paste.
- Some commit figures look odd as stated (mean 92.85 vs 344.64 files changed per commit; a 0.000 human merge-commit rate). They're unexplained and possibly a pipeline artifact.
- Conflicts with Cotroneo et al. (Human-Written vs. AI-Generated Code, same group) on size: there AI functions are shorter and simpler. The settings differ (isolated generated functions vs. integrated repo files).
- CodeQL alerts are not confirmed bugs.
