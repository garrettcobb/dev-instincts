# Benchmarks: how the trial compares

## Effort, measured from commit timestamps
- PrivateApp line: Oct 23 → Oct 30, 2026, 155 commits, about 39 active hours over 11 sessions. More, counting the developer's testing time; realistically 60–80 hours.
- Size after pass 1:
  - about 41k lines (25k app, 16k tests);
  - 3.5k lines of generated migrations;
  - about 9k lines of docs;
  - 29 ADRs.

## What the speed bought, and what it didn't

The point of these numbers isn't that one person beat a team. It's what fast AI delivery leaves behind.

The scope is a medium-to-high complexity business app:
- RFQ → contract → submittals → release → tracking → AFP → change orders → closeout;
- takeoffs, Files and Notes;
- accounts and dashboards;
- a full Explorer-style UI with Undo and Recycle Bin;
- an offline installer.

Published ranges for custom software of that size:
- **Keyhole Software:** medium projects run 4–8 months and $120k–300k; high-complexity ones 8–18+ months and $300k–1M+.
- **Clutch 2026 average:** $132k and 13 months.
- **McConnell:** 20–125 delivered lines a day on small projects. AI-written code runs more lines per feature, so a line count overstates how much was built.

The trial reached that feature scope in about 60–80 hours. It also carried about 91 defects at its first independent review, and the first fix pass added 32 new ones and at least 3 regressions. Most of the defects were the edge cases a team's code review and QA exist to catch.

What a team's timeline includes that the trial didn't have yet:
- a shared server;
- a security review;
- training;
- a warranty and support;
- more than one person who knows the code.

Those gaps are the honest cost of the speed. This repo is an attempt to close the review gap with checks instead of headcount.

## The average AI-assisted developer
- **Sonar 2026:** only 48% always check AI code before committing; 96% don't fully trust it.
- **METR, 2025 RCT:** experienced developers on large existing codebases were 19% slower with AI, while believing they were 20% faster.
- **DORA 2025:** for most teams, AI speed gains are cancelled by more failed changes. Only teams with strong practices benefit.

**Read:** the trial had more process than most AI-assisted work (decision records, a defect log, independent reviews) and less code literacy (AI reviewing AI). The bugs that got through were the edge cases a developer who reads code catches by instinct. That's the gap this repo targets.

## Sources
- https://keyholesoftware.com/cost-custom-software-development/
- https://www.apptunix.com/blog/procurement-software-development-cost-guide/
- https://successfulsoftware.net/2017/02/10/how-much-code-can-a-coder-code/
- https://community.sonarsource.com/t/results-from-the-2026-state-of-code-developer-survey-are-here/172502
- https://getdx.com/blog/metr-study-on-how-ai-affects-developer-productivity/
- https://blog.robbowley.net/2025/10/01/dora-2025-ai-assisted-dev-report-some-benefit-most-dont/
- https://www.dora.dev/research/ai
