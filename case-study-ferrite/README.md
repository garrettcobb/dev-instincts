# Case study: Ferrite

Ferrite is an open-source Rust/egui text editor for Markdown, JSON, YAML and TOML, about 133,000 lines (MIT licence, © OlaProeis). Its README says the code is 100% AI-generated, written by Claude via Cursor, and that its developer doesn't read code line by line. That's the same situation as PrivateApp's developer, which makes Ferrite a second, independent record of what slips through in that way of working. It's also a desktop app, where PrivateApp is a web app.

What's here:
- `report.md` contains:
  - the 154 bugs that reached users or testers, from Ferrite's own changelog, issue replies, test plans and handovers;
  - spot-checks of 19 of them in the source;
  - 14 latent bugs found in the current code that Ferrite's docs don't record;
  - the bug classes, the 14 candidate instincts (relabelled F1–F14; nine approved on 2026-10-31 as #47, #49, #50, #53, #55, #56, #59, #60, #61), the process lessons, and a replay exercise for measuring the reviewer's recall.
- `probes/` holds small standalone Rust programs that copy the relevant Ferrite function and show the bug. They don't run the real app. Build one with `rustc --edition 2021 <file>`. Ferrite's licence is in `probes/FERRITE-LICENSE`.

In the ledger:
- The 154 historical bugs are `FE-001…FE-154`, origin `external`. They're Ferrite's escapes, not this reviewer's, so they don't count against its record.
- The 14 latent bugs are `FE-L01…FE-L14`, origin `pre-existing`, status `open`.

Analysed from a snapshot of the Ferrite master branch (zip, no git history), 2026-10-31.
