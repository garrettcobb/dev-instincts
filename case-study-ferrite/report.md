# Ferrite: escaped bugs, mined to calibrate the instinct reviewer

**Subject:** Ferrite (Rust/egui Markdown/JSON/YAML/TOML editor, ~133k lines in `src/`, MIT). Its README says the code is 100% AI-written (Claude via Cursor) and the maintainer "doesn't read code line by line". That is our developer's situation.

**Snapshot:** `kb/ferrite/Ferrite-master`, no git history. Report only: nothing in Ferrite or in `dev-instincts` was changed.

**What I read:**
- `CHANGELOG.md`, all versions 0.1.0 to Unreleased 0.3.1;
- both issue-reply docs;
- the four test plans and suites, plus the v0.3.0 regression matrix;
- every handover, note and PRD bug section;
- `refactoring-assessment.md`, `refactor.md`, `checklist-pr74.md`, `.planning/`, the root and `docs/` handover and context files;
- the ROADMAP's Known Issues;
- the technical docs that carry root causes.

Then I went into `src/`.

**Bottom line:**
- **154 escaped bugs.** 127 shipped to users and 27 were caught by the maintainer in pre-release testing. 11 are still open.
- **Evidence:** 37 are backed by code I located in `src/`. The other 117 rest on Ferrite's own docs only.
- **Spot-checks:** 19 of the most severe were checked in `src/`.
- **Latent bugs:** checking found 14 problems Ferrite's docs don't record. Nine of them are data-loss or crash, and several are siblings that the escaped bugs' fixes left behind.
- **Probes:** four of those 14 (L-01, L-02, L-06, L-14) were confirmed with small probes that copy Ferrite's exact logic into standalone Rust. I did not build Ferrite, because its crates aren't cached and it has system dependencies.

**Output files:**
- `kb/ferrite-findings.jsonl`: one ledger row per escaped bug.
- The latent findings are in this report only (the "Latent bugs" table under "At a glance"), because they are not "escaped".

---

## At a glance

### Severity

| Severity | Bugs | Open |
|---|---|---|
| data-loss | 14 | 0 |
| security | 0 | 0 |
| wrong-result | 37 | 2 |
| crash | 10 | 0 |
| stuck | 33 | 6 |
| process | 0 | 0 |
| cosmetic | 60 | 3 |

Severity follows our scale. My conventions:
- unusable slowness or a platform blocker counts as **stuck**;
- background resource waste counts as **cosmetic** with a `perf` tag;
- unreadable document text (CJK tofu) counts as **stuck**, but tofu in UI icons is **cosmetic**.

### Ranked: every data-loss and crash, then wrong-results caused by a fix

| Rank | ID | Found → fixed | Bug | Severity | Class | Instincts | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | FE-041 | 0.2.5.1 → 0.2.5.2 | Ctrl+X with nothing selected cut the entire document | data-loss | K7 | #4 | code | fixed-claimed |
| 2 | FE-104 | 0.2.7 → 0.2.8 | Editing a table in rendered view strips bold/italic/strikethrough (#117) | data-loss | K8 | #44 | code | fixed-claimed |
| 3 | FE-113 | 0.2.8 → 0.2.9 | No dirty marker, no save prompt, no auto-save after raw edits | data-loss | K7 | #1, #6, #28, #32 | code | fixed-claimed |
| 4 | FE-114 | 0.2.8 → 0.2.9 | Undo/redo did nothing after typing ('Nothing to undo') | data-loss | K7 | #1, #7, #28, #32 | code | fixed-claimed |
| 5 | FE-125 | 0.2.7 → 0.3.0 | Frontmatter panel shows the previous file; 'Add frontmatter' splices the wrong body | data-loss | K4 | #5 | code | fixed-claimed |
| 6 | FE-129 | 0.2.8 → 0.3.0 | Recovery/autosave applied to an unrelated tab; save overwrote the real file (Task 106) | data-loss | K6 | #25 | code | fixed-claimed |
| 7 | FE-130 | 0.3.0-dev → 0.3.0 | Second crash/restore cycle silently discards every edit since the first restore (Task 106.6) | data-loss | K6 | [] | code | fixed-claimed |
| 8 | FE-134 | 0.2.8 → 0.3.0 | Multi-cursor copy/cut kept only the primary selection | data-loss | K7 | [] | code | fixed-claimed |
| 9 | FE-139 | 0.3.0-dev → 0.3.0 | Quick note: closing a modified untitled tab discarded it without asking | data-loss | K7 | #6 | code | fixed-claimed |
| 10 | FE-002 | 0.1.0 → 0.2.0 | Rendered-mode list editing edits the wrong item | data-loss | K5 | #5 | changelog | fixed-claimed |
| 11 | FE-074 | 0.2.6 → 0.2.6.1 | Undo after formatting deletes the text (#73) | data-loss | K7 | #7 | changelog | fixed-claimed |
| 12 | FE-091 | 0.2.6.1 → 0.2.7 | Windows IME: Backspace during composition deletes committed text (#91) | data-loss | K13 | #20 | changelog | fixed-claimed |
| 13 | FE-098 | 0.2.7 → 0.2.8 | Editing a plain paragraph in rendered view drops trailing spaces | data-loss | K8 | #44 | changelog | fixed-claimed |
| 14 | FE-148 | 0.3.0-dev → 0.3.0 | Quick note: clean exit deleted recovery/, losing scratch tab text | data-loss | K6 | [] | changelog | fixed-claimed |
| 15 | FE-031 | 0.2.3 → 0.2.5 | Malformed Mermaid label hangs the layout (app freezes/crashes) | crash | K12 | #9, #19 | code | fixed-claimed |
| 16 | FE-073 | 0.2.6 → 0.2.6.1 | Portable build crashes at startup on a corrupt saved window position (#57) | crash | K12 | #9 | code | fixed-claimed |
| 17 | FE-088 | 0.2.6.1 → 0.2.7 | Crash deleting a large selection with word wrap | crash | K12 | #9 | code | fixed-claimed |
| 18 | FE-092 | 0.2.6.1 → 0.2.7 | Opening a binary file crashes ('byte index is not a char boundary') | crash | K1 | #9 | code | fixed-claimed |
| 19 | FE-106 | 0.2.7 → 0.2.8 | Choosing some system fonts crashes the app (#114) | crash | K3 | #9, #19 | code | fixed-claimed |
| 20 | FE-107 | 0.2.8-dev → 0.2.8 | Command palette crashed on commands that change view state | crash | K12 | [] | code | fixed-claimed |
| 21 | FE-112 | 0.2.8 → 0.2.9 | Split/Rendered crashes on an empty document (#127) | crash | K12 | #9, #19, #28 | code | fixed-claimed |
| 22 | FE-117 | 0.3.0-rc → 0.3.0 | Pasting mixed-script text aborts the app (I-3) | crash | K1 | #9 | code | fixed-claimed |
| 23 | FE-015 | 0.2.1 → 0.2.2 | Tree viewer panics on multi-byte UTF-8 (øæå, emoji) | crash | K1 | #9, #19 | changelog | fixed-claimed |
| 24 | FE-072 | 0.2.6 → 0.2.6.1/0.2.7 | Startup crash with a non-Auto CJK font preference (#63) | crash | K3 | #9, #26 | changelog | fixed-claimed |
| 25 | FE-065 | 0.2.6.1-dev → 0.2.6.1 | Ctrl+Shift+E bound to both Toggle File Tree and Export HTML (created by the #46 fix) | wrong-result | K13 | #28 | code | fixed-claimed |
| 26 | FE-118 | 0.2.8 → 0.3.0 | Only the first of consecutive fenced code blocks visible (#129) | wrong-result | K14 | #28 | changelog | fixed-claimed |

### Latent bugs found while spot-checking (not in Ferrite's docs, not in the JSONL)

| ID | Problem | Severity | Where | Evidence | Instincts |
|---|---|---|---|---|---|
| L-01 | Duplicate / Move / Delete Line add a **character** column to a **byte** offset and slice the string. The app aborts when the cursor sits after a multi-byte character (ø, 你). This was introduced by the 0.2.6.1 fix for FE-063. | crash | `src/app/line_ops.rs:89,130-133` / `:168,211-216` / `:273,317-326` | probe (copied logic): all three panic | #9, #28 |
| L-02 | Duplicate/Move/Delete Line, smart-paste link/image, auto-close wrap, drag-drop image link and Format Document all write `tab.content`, then call the legacy `record_edit`, which **does not bump `content_version`**. On a clean tab: no `*`, no save prompt, no auto-save, no crash recovery. This is the 0.2.9 critical (FE-113) class, still live. | data-loss | `src/state.rs:2666-2674`. Callers: `line_ops.rs:148,239,348`, `input_handling.rs:351,381,541`, `file_ops.rs:1459`, `formatting.rs:286` | probe (copied logic): `is_modified()` stays false after Duplicate Line | #1, #6, #27 |
| L-03 | Recovery's plain `Recovered` branch is also taken when the file on disk is **missing or not UTF-8**. It anchors `original_content` to the recovered buffer, so the tab looks saved; closing it loses the text. It also forces `utf-8`, so the next save changes the file's encoding. This is the FE-130 mechanism in the sibling branch. | data-loss | `src/state.rs:4942-4951`, `5326-5330`, `5363-5383` | reading | #27 |
| L-04 | Changing encoding in the status bar re-decodes the original bytes and replaces `content`, which **discards unsaved edits** with no prompt and no undo. | data-loss | `src/state.rs:2301-2336`; `src/app/status_bar.rs:829-831` | reading | #25, #44 |
| L-05 | Save ignores encoder errors. In encoding_rs, characters the target encoding can't represent become HTML numeric references (`&#8594;`). Choosing UTF-16 for a file without a BOM writes no BOM, and Ferrite then refuses to reopen it (FE-145). | data-loss | `src/state.rs:2382`, `2352-2376` | reading; the encoding_rs behaviour is from its documentation, not run here | #25 |
| L-06 | The new 0.3.1 CSV cell editing serializes the cached rows back over `tab.content`. The cache is gated by a hash of the length plus the first and last 4 KB, so a same-length edit mid-file (made in Raw view) is missed, and the next cell edit **reverts it**. A unit test explicitly accepts the missed middle edit. | data-loss (unreleased) | `src/markdown/csv_viewer.rs:615-625`, `1633-1634`, `1703`, `1115-1131`; test `2840-2849` | probe (copied hash): equal after a mid-file edit | #5, #42 |
| L-07 | For files over 5 MB the editor treats a same-length `tab.content` change as "unchanged" and never syncs it into the rope. The next keystroke writes the stale rope back (examples: move line, a same-length replace, checkbox toggle). | data-loss | `src/editor/widget.rs:507-512`, `822` | reading | #5 |
| L-08 | Two open paths with two rules. Under 5 MB, binary and UTF-16 files are rejected. At 5 MB or more, the background loader skips the binary check and lossy-decodes, discarding decode errors. A large binary opens as text and saving corrupts it. | data-loss | `src/app/file_ops.rs:135-137`, `234-238`; `src/state.rs:1915-1937` vs `4124` | reading | #6, #25 |
| L-09 | F12 is the default binding for both Open and Close Workspace. Neither is dispatched, but the palette and settings advertise F12. The only conflict test checks Save. | cosmetic | `src/config/settings.rs:877-878`, `4317`; `src/app/keyboard.rs:15-110` | reading (parsed 62 default bindings; this is the only duplicate) | #23, #39 |
| L-10 | Issue-reply drafts tell users that Ctrl+R / Ctrl+S / Ctrl+V (#98) and Ctrl+Shift+R / Ctrl+Shift+S (#105) switch views. In the code Ctrl+S is Save, Ctrl+Shift+S is Save As, and only Ctrl+E toggles. | cosmetic | `docs/github-issue-replies-0.2.7.md` #98, `-0.2.8.md` #105 vs `settings.rs:871-872,885` | reading | #37 |
| L-11 | The root handover tells a Rust task to "Run `python -m pytest`". Two handover systems and two `ai-context.md` files give opposite rules. | process | `current-handover-prompt.md`; `ai-context.md` vs `docs/ai-context.md` | reading | #41 |
| L-12 | `LARGE_FILE_THRESHOLD` has four meanings: 1 MB, 5 MB, 100,000 lines and 10 MB. On large-file undo limits, the CHANGELOG (0.2.6: "10 vs 100", `LARGE_FILE_MAX_UNDO (10)`) disagrees with the code and `docs/ai-context.md` (200 groups). | process | `state.rs:28,1045,1048`; `widget.rs:113`; `view.rs:26`; `markdown/csv_viewer.rs:40` | reading | #23, #37 |
| L-13 | Mojibake in source comments (`â”€â”€`, 90 lines across 3 files): the tool chain round-tripped UTF-8 through a Windows code page. | process | `src/markdown/editor.rs` (62), `editor/minimap.rs` (20), `editor/ferrite/highlights.rs` (8) | reading | [] |
| L-14 | The `catch_unwind` "safety nets" cited for the Mermaid and font crash fixes are **inert in shipped builds**: the release profile sets `panic = "abort"`. Tests run with unwinding, so they pass. | crash | `Cargo.toml:148`; `src/fonts.rs:844`; `src/markdown/mermaid/mod.rs:218,257` | probe: under `-C panic=abort` the process aborts (exit 134); under unwind it is caught | #19, #39 |

Probes: `probes/` (in this folder) (`probe_line_ops_all.rs`, `probe_move_line.rs`, `probe_dirty_flag.rs`, `probe_csv_hash.rs`, `probe_catch_unwind.rs`). Each probe copies the cited function body; none runs the real app. Build and run one with `rustc --edition 2021 <file> && ./<name>`.

---

## 1. Escaped bugs

### 1.1 How the list was built

- **Sources:**
  - every "Fixed" entry in the CHANGELOG, plus fixes filed under "Added" (memory leak, scroll accuracy, undo after formatting, palette crash, Mermaid hang);
  - the issue replies;
  - handovers (`handover-minor-bugs`, `handover-list-editing-bug`, `code-review-v0.2.0-findings`);
  - PRD bug sections (#46, #73, #71, list-editing PRD);
  - the regression matrix (I-1 to I-4);
  - `checklist-pr74.md`;
  - ROADMAP Known Issues;
  - technical docs with root causes (uniform-height overlap, quick-note recovery deletion).
- **Excluded:** feature requests and questions (#1, #36, #85, #94, #98, #99, #108), the theme-toggle preference in `handover-minor-bugs`, and the Gemini v0.1.0 review's speculative risks (it read no code; see §3).
- **Found → fixed:** "found" is the release the bug shipped in (the previous release when unknown). A `-dev`/`-rc` suffix means it was found in pre-release testing.
- **Caught by:** `user` means it shipped in a release, whoever filed it. `maintainer` means it was found in pre-release testing (regression matrix, PR checklist, dev handovers).
- **Status:** `fixed-claimed` means Ferrite's docs say fixed; `open` means acknowledged and unfixed, or with no fix recorded.
- **Evidence:** every row is `reading`. The extra field `evidence_basis` is `code` when I located the cause or the fix in `src/`, and `changelog` otherwise.

### 1.2 Spot-checks in `src/` (19 of the most severe)

| Bug | What I checked | What I found |
|---|---|---|
| FE-117 paste crash (I-3) | `is_url` | The fix is present: `s.get(colon_pos..colon_pos+3)` at `input_handling.rs:160`, plus 5 tests. The same class is still live elsewhere (L-01). |
| FE-113 no dirty flag | how raw edits bump the version | `widget.rs:819-834` now calls `record_external_edit_from_snapshot` (bumps `content_version`). The cache is at `state.rs:1984-2016`. The legacy `record_edit` (2666) still doesn't bump: L-02. |
| FE-114 undo broken | snapshot then record | `widget.rs:470` (prepare) and `833` (record): present. |
| FE-112 empty-doc crash | culling ranges | Half-open range in the bootstrap path (`editor.rs:1531-1535`); the fast path is guarded by `block_count > 0` (1292). |
| FE-129 recovery bleed | identity gating | `try_apply_recovery` (`state.rs:5279-5385`): path equality, then disk-hash check. Present. |
| FE-130 second-cycle loss | restore anchoring | The divergence branch builds from disk, then `set_content` (`state.rs:4959-4990`). The plain `Recovered` branch still uses `with_file(recovered)` when disk is unreadable or missing: L-03. |
| FE-125 frontmatter stale | cache key | Keyed on `(tab_id, content_version)` with tests (`frontmatter_panel.rs:225-264`, `706-735`). Present. |
| FE-139 quick-note discard | prompt context | `should_prompt_to_save` exempts only `AppExit` (`state.rs:2117-2122`). Present. |
| FE-094 crash detection | start-up order | Load session, then create lock (`app/mod.rs:253-262`). The lock stores a PID that is never checked. |
| FE-092 binary crash | stats slicing and binary check | `count_links` uses `char_indices` (`stats.rs:352`); `is_binary_content` exists (`state.rs:153`) but has a single caller on the under-5 MB path (L-08). I-4 is confirmed still open (null check at `:160`). |
| FE-041 Ctrl+X cut all | empty-selection guard | `has_any_selection()` guards at `ferrite/editor.rs:2349-2350, 2403-2404`. Present. |
| FE-073 NaN window position | config validation | `is_finite` plus range check at `settings.rs:2884-2890`; test at 3307. Present. |
| FE-051 Linux folder freeze | notify features | `Cargo.toml:62` is now `notify = "6"` (default features). Present. |
| FE-064/065 shortcut collisions | whole default table | 62 bindings parsed; only F12 is duplicated (L-09). Dispatch is first-match in a hand-ordered list. The only test checks Save. |
| FE-031 / FE-106 Mermaid hang, font crash | guards | Iteration cap present (`subgraph.rs:204`); font magic-byte validation present (`fonts.rs:773`). `catch_unwind` is inert in release (L-14). |
| FE-063 Duplicate Line position | cursor source | Now reads `tab.cursor_position` (`line_ops.rs:89`). That column is in characters (`cursor.rs:22`) but is used as bytes at 130-133: L-01. |
| FE-104 table formatting loss | serializer | `serialize_inline_content` (`widgets.rs:880`). Present. |
| FE-054 lines() collapse | line splitting | `LinesWithEndings` with an explicit warning comment (`syntax.rs:289-292`). Present. |
| FE-115 light selection | colour | `(100,170,245)` at `theme/mod.rs:219` matches the CHANGELOG. ROADMAP describes a different fix ("alpha reduction dark-mode-only"). |

**Pattern:** every fix I checked is present and well commented, and most have a pinned test. In four cases the same construct still exists one function or one branch over (L-01, L-02, L-03, L-08). Fixes were scoped to the reported path, not the class.

### 1.3 Full list

Cause text includes `file:line` only where `evidence_basis` is `code`.

| ID | Found → fixed | Title | What the user saw | Cause (file:line where located) | Severity | Instincts | Class | Evidence | Caught by |
|---|---|---|---|---|---|---|---|---|---|
| FE-001 | 0.1.0-dev → 0.1.0 | Formatted list items and paragraphs were read-only in rendered view | Clicking a list item or paragraph containing **bold**, *italic*, code or a link did nothing; only plain items were editable. | No edit path for formatted inline content; hybrid click-to-edit added. | stuck | #17 | K5 | changelog | maintainer |
| FE-002 | 0.1.0 → 0.2.0 | Rendered-mode list editing edits the wrong item | Clicking the first list item selected the heading above; typing in item N changed a different item. | Edit state keyed by node index / structural key that did not match the clicked node (off-by-one in index mapping). | data-loss | #5 | K5 | changelog | user |
| FE-003 | 0.1.x → unrecorded | Recent-files popup needs two clicks the first time | First click on the status-bar file path did nothing; second click opened the menu. | Popup state/id not toggled on first interaction (handover hypothesis). | stuck | #17 | K5 | changelog | maintainer |
| FE-004 | 0.1.x → unrecorded | Recent-files menu text nearly invisible in light mode | Light-grey paths on white background. | Hard-coded light grey instead of theme text colour. | cosmetic | [] | K15 | changelog | maintainer |
| FE-005 | 0.1.x → unrecorded | Settings gear icon misaligned with theme icon in status bar | Gear sits visibly higher than the neighbouring icon. | Different padding/layout between the two buttons. | cosmetic | #23 | K14 | changelog | maintainer |
| FE-006 | 0.1.x → 0.2.x | Toggle View Mode bound to Ctrl+Shift+V, the paste shortcut on many systems | Paste-as-plain-text keystroke switched views instead. | Shortcut chosen without checking OS conventions; moved to Ctrl+E. `src/config/settings.rs:885 (now Ctrl+E)` | wrong-result | [] | K13 | code | maintainer |
| FE-007 | 0.1.0 → 0.2.0 | Light mode text and borders below readable contrast | Faint text and invisible separators in light theme. | Light palette not checked for contrast. | cosmetic | [] | K15 | changelog | user |
| FE-008 | 0.1.0 → 0.2.0 | Search-in-files result opened the file but didn't scroll to the match | Clicking a result left the user at the top of the file. | No scroll-to-match after open. | cosmetic | #17 | K16 | changelog | user |
| FE-009 | 0.1.0 → 0.2.0 | Search panel clipped at top and bottom of the window | Parts of the panel off-screen. | Panel rect not constrained to viewport. | cosmetic | #24 | K9 | changelog | user |
| FE-010 | 0.2.0 → 0.2.1 | Mermaid labels sized by character count overflow their nodes | Node text spilled out of boxes; long edge labels overflowed. | Character-count width estimate instead of font metrics. | cosmetic | [] | K14 | changelog | user |
| FE-011 | 0.2.0 → 0.2.1 | Mermaid user-journey emoji rendered as tofu | Empty boxes where emoji icons should be. | Embedded fonts lack emoji glyphs; text fallbacks added. | cosmetic | [] | K3 | changelog | user |
| FE-012 | 0.2.1 → 0.2.2 | Linux .deb would not start on Ubuntu 22.04 (#6) | Binary refused to run: glibc 2.39 required, system has 2.35. | CI built on ubuntu-24.04. | stuck | [] | K10 | changelog | user |
| FE-013 | 0.2.1 → 0.2.2 | CJK text rendered as empty boxes (#7) | Korean/Chinese/Japanese documents unreadable. | Bundled Inter/JetBrains Mono have no CJK glyphs; system font fallback added. | stuck | [] | K3 | changelog | user |
| FE-014 | 0.2.1 → 0.2.2 | Undo resets scroll to top, drops focus, needs two presses (#5) | Ctrl+Z jumped to the top of the document and the editor stopped taking keys. | Full document refresh on undo instead of a minimal state update. | wrong-result | #22, #7 | K5 | changelog | user |
| FE-015 | 0.2.1 → 0.2.2 | Tree viewer panics on multi-byte UTF-8 (øæå, emoji) | Opening JSON/YAML with Norwegian or emoji text crashed the app. | Byte-index slicing of display strings. | crash | #9, #19 | K1 | changelog | user |
| FE-016 | 0.2.0 → 0.2.2 | Fold indicators shown but folding never hid text (#12) | Gutter arrows toggled but nothing collapsed. | Folding shipped as indicators only (text hiding deferred). | cosmetic | #18 | K16 | changelog | user |
| FE-017 | 0.2.1 → 0.2.2 | Typing lags in 5000+ line files | Keystrokes delayed in large files. | Syntax highlighting synchronous on every edit; deferred. | stuck | #13 | K11 | changelog | user |
| FE-018 | 0.2.2 → 0.2.3 | Task-list items with inline formatting rendered wrong; checkbox misaligned | Formatted task items looked broken in rendered view. | Renderer handled task items as plain text; switched to ASCII [ ]/[x] markers (later reported as #95). | cosmetic | [] | K14 | changelog | user |
| FE-019 | 0.2.2 → 0.2.3 | Intel Mac users got the wrong build (#16) | No working Intel macOS artifact. | Artifact naming/cross-compile setup; separate x86_64 build added. | stuck | [] | K10 | changelog | user |
| FE-020 | 0.2.2 → 0.2.3 | Linux cursor flickers between pointer and resize near the close button | Cursor shape flickered at the top-right corner. | North-edge resize zone overlapped title-bar buttons. | cosmetic | [] | K9 | changelog | user |
| FE-021 | 0.2.3 → 0.2.5 | Find highlights drift further from matches through the document | Highlight boxes progressively offset in non-ASCII text. | Byte positions used as character positions. | wrong-result | [] | K1 | changelog | user |
| FE-022 | 0.2.3 → 0.2.5 | Settings not persisted across restarts (#15) | Changed settings were gone after restart. | Window-state dirty flag not set, so config.json was not written. | wrong-result | #1 | K6 | changelog | user |
| FE-023 | 0.2.3 → 0.2.5 | Workspace folder and recent files not restored on restart | Reopening the app lost the workspace; recent list empty after updates. | Persisted only on exit; non-atomic writes; stale paths. | wrong-result | [] | K6 | changelog | user |
| FE-024 | 0.2.3 → 0.2.5 | Line-width setting ignored in rendered and split views (#15) | Text ran to the pane edge. | Setting applied only in raw editor. | cosmetic | #6 | K14 | changelog | user |
| FE-025 | 0.2.3 → 0.2.5 | Quick switcher: mouse hover flickers, click doesn't select | Items flickered under the mouse and clicks were ignored. | Hover/selection state fought between keyboard and mouse each frame. | stuck | [] | K5 | changelog | user |
| FE-026 | 0.2.3 → 0.2.5 | Rendered table cell loses focus after every keystroke | Could type only one character before the cell lost focus. | Each keystroke rebuilt the cell widget with a new identity; deferred commit model added. | stuck | [] | K5 | changelog | user |
| FE-027 | 0.2.3 → 0.2.5 | Zen mode didn't centre rendered/split content | Rendered text hugged the left in Zen mode. | Centering implemented for raw editor only. | cosmetic | #6 | K14 | changelog | user |
| FE-028 | 0.2.3 → 0.2.5 | Window couldn't be resized from the top edge on Windows (#15) | Top edge had no resize cursor. | Custom borderless window lacked a north resize zone. | cosmetic | [] | K9 | changelog | user |
| FE-029 | 0.2.3 → 0.2.5.1 | Intel Mac: high CPU from debug log spam and continuous repaint (#24) | Fans and CPU busy while idle in rendered mode. | ~50,000 [LIST_ITEM_DEBUG] lines per 22 s; Sense::hover on scroll content forced 60 fps repaints. | cosmetic | [] | K11 | changelog | user |
| FE-030 | 0.2.3 → 0.2.5 | Mermaid flowcharts dropped chained edges, ignored direction, lost nodes | A-->B-->C drew one edge; LR diagrams laid out top-down; some nodes missing. | Parser and layout gaps. | wrong-result | [] | K14 | changelog | user |
| FE-031 | 0.2.3 → 0.2.5 | Malformed Mermaid label hangs the layout (app freezes/crashes) | Diagram like H[Show "Try Again"] froze the editor. | Layout loop with no iteration limit; no panic guard around render. `src/markdown/mermaid/flowchart/layout/subgraph.rs:204; src/markdown/mermaid/mod.rs:218` | crash | #9, #19 | K12 | code | user |
| FE-032 | 0.2.3 → 0.2.5 | Mermaid diagrams clipped at negative coordinates; subgraph titles overflow | Parts of diagrams cut off; titles wider than their box. | Bounds ignored negative coords and title width. | cosmetic | [] | K14 | changelog | user |
| FE-033 | 0.2.5 → 0.2.5.1 | About 10% CPU while completely idle | Background CPU use and battery drain with nothing happening. | Repaint every frame; title command sent every frame; repaint_on_widget_change. | cosmetic | [] | K11 | changelog | user |
| FE-034 | 0.2.5 → 0.2.5.1 | Unmodified new tab still asks to save on close | Closing an untouched untitled tab prompted Save/Don't save. | Dirty flag set on creation. | cosmetic | #44 | K7 | changelog | user |
| FE-035 | 0.2.5 → 0.2.5.1 | CJK first-line indentation applied to the whole paragraph | Every line indented instead of only the first. | Indent applied to the block, not leading_space. | cosmetic | [] | K14 | changelog | user |
| FE-036 | 0.2.5 → 0.2.5.1 | Workspace close button overlaps resize handle | Clicks near the panel edge hit the wrong control. | Overlapping hit zones. | cosmetic | [] | K9 | changelog | user |
| FE-037 | 0.2.5 → 0.2.5.1 | Linux: window close button can't be clicked | Clicking × did nothing on Wayland/X11. | Title-bar drag rect allocated over the button area and consumed clicks (doc labels this both 0.2.5.1 and 'v0.2.6'). | stuck | [] | K9 | changelog | user |
| FE-038 | 0.2.5 → 0.2.5.1 | Scroll-to-line lands hundreds of pixels off in 3000+ line files | Find, outline, minimap and search-in-files jumped to the wrong place. | Mixed 0/1-indexed lines; stale default line height. | wrong-result | #13 | K4 | changelog | user |
| FE-039 | 0.2.5 → 0.2.5.1 | Outline/minimap highlight offset from the target line | Clicked heading highlighted the wrong text. | Character offsets used where search used byte offsets. | wrong-result | [] | K1 | changelog | user |
| FE-040 | 0.2.5 → 0.2.5.1 | Per-tab viewer state never freed on tab close (memory leak) | Memory grew as tabs were opened and closed. | tree_viewer_states, csv_viewer_states, sync_scroll_states maps keyed by tab id never pruned. | cosmetic | [] | K6 | changelog | user |
| FE-041 | 0.2.5.1 → 0.2.5.2 | Ctrl+X with nothing selected cut the entire document | The whole document vanished into the clipboard. | egui TextEdit treated an empty selection as everything. `src/editor/ferrite/editor.rs:2349-2350, 2403-2404 (guard now)` | data-loss | #4 | K7 | code | user |
| FE-042 | 0.2.5.1 → 0.2.5.2 | Linux: dragging the title bar leaves the mouse stuck in drag mode | After moving the window, the pointer kept dragging. | egui drag state desynchronised from the window manager after StartDrag. | stuck | [] | K9 | changelog | user |
| FE-043 | 0.2.5.1 → 0.2.5.2 | Split view: rendered pane overwrote the cursor, line ops hit the wrong line (#29) | Move/delete line in split view acted on a different line. | Both panes wrote cursor position each frame. | wrong-result | #5 | K4 | changelog | user |
| FE-044 | 0.2.5.1 → 0.2.5.2 | macOS tooltips said Ctrl instead of Cmd (#28) | Shortcut hints wrong on macOS. | Hard-coded 'Ctrl' strings. | cosmetic | #23 | K13 | changelog | user |
| FE-045 | 0.2.5.1 → 0.2.5.2 | Minimap highlight offset fixed a second time (byte offsets) | Same symptom as FE-039 after its fix. | Earlier fix did not cover all paths. | wrong-result | #26, #27 | K1 | changelog | user |
| FE-046 | 0.2.5.2 → 0.2.8 | macOS: .md files couldn't be opened from Finder (#102) | Open With / double-click did not hand the file to Ferrite. | Info.plist lacked UTImportedTypeDeclarations for net.daringfireball.markdown (first blamed on winit#1751). | stuck | [] | K10 | changelog | user |
| FE-047 | 0.2.5.2 → 0.2.5.3 | Wayland: window missing from alt-tab and taskbar | Ferrite invisible to the window switcher on KDE/GNOME Wayland. | No app_id on the viewport. | cosmetic | [] | K10 | changelog | user |
| FE-048 | 0.2.5.2 → 0.2.5.3 | UI symbols render as tofu (↳, ⋯, git ✕) | Square boxes in Find/Replace, tree viewer menu and file tree. | Glyphs missing from embedded Inter. | cosmetic | [] | K3 | changelog | user |
| FE-049 | 0.2.5.2 → 0.2.5.3 | Box-drawing characters render as squares (fixed in 0.2.5.3 and again in 0.2.6) | ─│┌┐ shown as boxes. | Inter lacks U+2500-257F; JetBrains Mono fallback added (listed as fixed twice). | cosmetic | #26 | K3 | changelog | user |
| FE-050 | 0.2.5.2 → 0.2.5.3 | Recent-files popup covers the button that opened it | Menu opened over the status-bar button. | Wrong anchor. | cosmetic | [] | K9 | changelog | user |
| FE-051 | 0.2.5.2 → 0.2.5.3 | Linux: opening a folder freezes the UI for 10+ seconds | App unresponsive after Open Folder on Fedora/KDE. | notify built without default features (no inotify, fell back to polling); recursive scan on the UI thread. `Cargo.toml:62 (now default features); src/workspaces/` | stuck | #13 | K11 | code | user |
| FE-052 | 0.2.5.2 → 0.2.5.3 | Hard line breaks in list items shown as a box (#41) | Trailing backslash rendered as a square. | Line-break node not handled in list rendering. | cosmetic | [] | K14 | changelog | user |
| FE-053 | 0.2.5.2 → 0.2.5.3 | Wide tables/blockquotes break line width for the rest of the document | One wide table made every later block full-width. | Wide content expanded the parent layout. | cosmetic | [] | K14 | changelog | user |
| FE-054 | 0.2.5.2 → 0.2.5.3 | Files without a syntax definition collapse to a single line | PowerShell and similar files displayed as one long line after first render. | Plain-text fallback used code.lines(), which strips newlines. `src/markdown/syntax.rs:289-292 (LinesWithEndings now)` | wrong-result | [] | K8 | code | user |
| FE-055 | 0.2.5.2 → 0.2.5.3 | Linux: clicking the view-mode segment starts a window drag | Raw/Split/Rendered buttons unclickable. | Drag exclusion zone narrower than the controls. | stuck | [] | K9 | changelog | user |
| FE-056 | 0.2.5.3 → 0.2.6 | 4 MB file uses 1.8 GB RAM and lags (#45) | Editor sluggish, memory climbing. | Document cloned every frame (~240 MB/s); bracket matching copied the whole buffer per frame; case-insensitive search copied the document. | stuck | #13 | K11 | changelog | user |
| FE-057 | 0.2.6-dev → 0.2.6 | New editor: cursor jumps to next line when typing at end of line | Text appeared on the wrong line. | FerriteEditor cursor handling at EOL. | wrong-result | [] | K4 | changelog | maintainer |
| FE-058 | 0.2.6-dev → 0.2.6 | New editor: last lines of large files unreachable | Could not scroll to the bottom, with or without wrap. | Content height computed short. | stuck | #13 | K11 | changelog | maintainer |
| FE-059 | 0.2.6-dev → 0.2.6 | Outline/minimap click lands several lines below the heading | Cursor placed below the clicked heading. | Line mapping off under the new view model. | wrong-result | [] | K4 | changelog | maintainer |
| FE-060 | 0.2.6-dev → 0.2.6 | Search highlights drift on wrapped lines in large files | Highlights offset on wrapped lines. | Uniform line height assumed. | cosmetic | [] | K4 | changelog | maintainer |
| FE-061 | 0.2.5.3 → 0.2.6 | File-browser context menu icons doubled or square | Broken icons in the right-click menu. | Icon glyph + label emoji / missing glyphs. | cosmetic | [] | K3 | changelog | user |
| FE-062 | 0.2.5.3 → 0.2.6 | Windows Start Menu icon pixelated | Low-resolution icon. | Single-size .ico. | cosmetic | [] | K10 | changelog | user |
| FE-063 | 0.2.6 → 0.2.6.1 | Duplicate Line inserts at the wrong position | Ctrl+Shift+D duplicated a different line / put the cursor elsewhere. | Read stale tab.cursors instead of the editor's cursor. The rewrite switched to a char column used as a byte offset (see latent L-01). `src/app/line_ops.rs:79-153` | wrong-result | #5, #28 | K4 | code | user |
| FE-064 | 0.2.6 → 0.2.6.1 | Ctrl+B bound to both Bold and Toggle File Tree (#46) | Bolding text also toggled the file tree. | Duplicate default bindings; PRD's fix moved File Tree to Ctrl+Shift+E. | wrong-result | [] | K13 | changelog | user |
| FE-065 | 0.2.6.1-dev → 0.2.6.1 | Ctrl+Shift+E bound to both Toggle File Tree and Export HTML (created by the #46 fix) | Toggling the tree exported HTML, or the reverse. | Moving File Tree to Ctrl+Shift+E collided with Export HTML; CHANGELOG reports this as #46 itself. `src/config/settings.rs:890` | wrong-result | #28 | K13 | code | maintainer |
| FE-066 | 0.2.6 → 0.2.6.1 | Maximize/restore icon disappears on hover | Button looked empty when hovered. | Icon painted under the hover background. | cosmetic | [] | K9 | changelog | user |
| FE-067 | 0.2.6 → 0.2.6.1 | Dropped image link inserted at a stale cursor position | Markdown image link landed somewhere else in the file. | Used stale tab.cursors instead of the editor cursor. `src/app/file_ops.rs:1440-1459` | wrong-result | #5 | K4 | code | user |
| FE-068 | 0.2.6 → 0.2.6.1 | Smart paste (URL over selection) did nothing | Pasting a URL over selected text inserted plain text instead of a link. | Selection read from stale tab.cursors. `src/app/input_handling.rs:300-390` | wrong-result | #5 | K4 | code | user |
| FE-069 | 0.2.6 → 0.2.6.1 | Title-bar auto-save toggle skipped toggle side effects | Auto-save state inconsistent after using the title-bar toggle. | Toggle flipped auto_save_enabled directly instead of calling toggle_auto_save() (which clears last_edit_time). | wrong-result | #6 | K7 | changelog | user |
| FE-070 | 0.2.6 → 0.2.6.1 | Switching Rendered→Raw recreated the editor (stutter, lost view state) | Visible stutter and scroll/syntax reset on mode switch. | FerriteEditor rebuilt instead of set_content(). | cosmetic | [] | K5 | changelog | user |
| FE-071 | 0.2.6.1-dev → 0.2.6.1 | Ctrl+` bound to both Inline Code and Toggle Terminal (PR #74 merge) | Formatting shortcut opened the terminal. | Contributor's terminal shortcut collided with an existing binding. | wrong-result | [] | K13 | changelog | maintainer |
| FE-072 | 0.2.6 → 0.2.6.1/0.2.7 | Startup crash with a non-Auto CJK font preference (#63) | App aborted on launch (0xc0000409) after choosing e.g. Japanese. | Font load panicked instead of returning None. CHANGELOG says fixed in 0.2.6.1; the issue reply says completed in 0.2.7 and tells users to uninstall to clear config. | crash | #9, #26 | K3 | changelog | user |
| FE-073 | 0.2.6 → 0.2.6.1 | Portable build crashes at startup on a corrupt saved window position (#57) | Portable Windows build would not start. | NaN/∞/off-screen window position from config passed to the OS; also portable zip lacked the portable/ folder. `src/config/settings.rs:2884-2890` | crash | #9 | K12 | code | user |
| FE-074 | 0.2.6 → 0.2.6.1 | Undo after formatting deletes the text (#73) | Select 'world', Ctrl+B, Ctrl+Z: 'world' disappeared instead of losing its bold. | Format op merged into the previous typing group. | data-loss | #7 | K7 | changelog | user |
| FE-075 | 0.2.6 → 0.2.6.1 | Consecutive blockquote lines render as separate quotes (#71) | One quote shown as several. | Renderer did not merge adjacent blockquotes. | cosmetic | [] | K14 | changelog | user |
| FE-076 | 0.2.6 → 0.2.6.1 | CJK first-line indentation fixed again (#20, #26) | Indentation still wrong after the 0.2.5.1 fix. | Second fix with LayoutJob leading_space. | cosmetic | #26 | K14 | changelog | user |
| FE-077 | 0.2.6.1-dev → open | PR #74 raised baseline memory from ~75 MB to ~300 MB | Maintainer measured 4x memory with terminal/productivity hub merged. | Terminal buffers / Tokio runtime / eager init suspected; checklist said do not merge. No recorded resolution. | stuck | #13 | K11 | changelog | maintainer |
| FE-078 | 0.2.6.1 → 0.2.7 | Linux tiling WMs: file dialogs fail silently (#97) | Export/Open did nothing on Hyprland/Sway/i3. | xdg-desktop-portal missing; error swallowed. Now a modal with install commands. `src/files/dialogs.rs` | stuck | #18 | K16 | code | user |
| FE-079 | 0.2.6.1 → 0.2.7 | Flatpak: Open Folder fails until a file from that folder is open (#96) | Folder picker failed on fresh installs. | Portal could not pick a default directory; no $HOME fallback. | stuck | #18 | K10 | changelog | user |
| FE-080 | 0.2.6.1 → 0.2.7 | macOS release blocked by Gatekeeper (#93) | Downloaded binary would not open. | Release shipped a raw binary, not an .app bundle. | stuck | [] | K10 | changelog | user |
| FE-081 | 0.2.6.1 → 0.2.7 | Task-list checkboxes rendered as ASCII with an extra bullet (#95) | [ ] / [x] text plus a bullet instead of checkboxes. | 0.2.3 had deliberately replaced interactive checkboxes with ASCII markers. | cosmetic | [] | K14 | changelog | user |
| FE-082 | 0.2.6.1 → 0.2.7 | Light mode: section headers invisible (white on white) | Bold labels in Settings, Terminal, Files, About invisible in light theme. | strong_text_color() returns active.fg_stroke, set to WHITE for pressed buttons. | cosmetic | [] | K15 | changelog | user |
| FE-083 | 0.2.6.1 → 0.2.7 | Markdown images not displayed in rendered/split view | ![](path) showed nothing. | Image loading/path resolution missing. | wrong-result | [] | K14 | changelog | user |
| FE-084 | 0.2.6.1 → 0.2.7 | Restored tabs show CJK as tofu with an explicit CJK preference (#76) | Chinese in restored tabs rendered as boxes after restart. | Fonts lazy-loaded only for the active tab. | stuck | [] | K3 | changelog | user |
| FE-085 | 0.2.6.1 → 0.2.7 | Switching UI language to Chinese/Japanese shows squares | Translated labels and language names unreadable until a CJK document opened. | CJK font not loaded on language switch; native-script names in the selector. | stuck | [] | K3 | changelog | user |
| FE-086 | 0.2.6.1 → 0.2.7 | Syntax highlighting re-parsed every frame before checking the cache | Lag on long lines. | highlight_line() called before the cache lookup. | cosmetic | #13 | K11 | changelog | user |
| FE-087 | 0.2.6.1 → 0.2.7 | Scrollbar position, drag and jumps wrong with word wrap | Thumb in the wrong place; drag jumped to the wrong line. | Uniform line height assumed; per-frame height rebuild. | wrong-result | #13 | K4 | changelog | user |
| FE-088 | 0.2.6.1 → 0.2.7 | Crash deleting a large selection with word wrap | Capacity overflow panic. | Unchecked usize subtraction with stale wrap info. `src/editor/ferrite/view.rs:1147 (truncate_wrap_info)` | crash | #9 | K12 | code | user |
| FE-089 | 0.2.6.1 → 0.2.7 | Long list items don't wrap in preview (#82) | List text ran past the pane edge. | List items used singleline TextEdit. | cosmetic | [] | K14 | changelog | user |
| FE-090 | 0.2.6.1 → 0.2.7 | Typing '- ' under a paragraph turns the paragraph into a heading (#82) | Paragraph above suddenly rendered as a large heading. | comrak reads a lone '-' line as a setext underline. `src/markdown/parser.rs:496` | wrong-result | [] | K8 | code | user |
| FE-091 | 0.2.6.1 → 0.2.7 | Windows IME: Backspace during composition deletes committed text (#91) | Pressing Backspace to fix pinyin deleted characters already in the document. | Raw Key::Backspace events processed alongside IME preedit. | data-loss | #20 | K13 | changelog | user |
| FE-092 | 0.2.6.1 → 0.2.7 | Opening a binary file crashes ('byte index is not a char boundary') | Opening a PNG as text aborted the app. | No binary check; count_links/count_images byte-sliced text. `src/editor/stats.rs:352; src/state.rs:153` | crash | #9 | K1 | code | user |
| FE-093 | 0.2.6.1 → 0.2.7 | Copying from rendered view inserts spaces at token boundaries | json.loads(f.read()) copied as json. loads( f. read()). | Each highlighted span a separate label with item_spacing.x between them. `src/markdown/editor.rs:4242` | wrong-result | #44 | K8 | code | user |
| FE-094 | 0.2.0 → 0.2.7 | Crash detection never worked: lock file created before reading the old one | Recovery dialog after 'Don't Save' offered back discarded text and closed the workspace; real crashes not detected. | create_lock_file() ran before load_session_state(), so check_and_clear_lock_file() always found the new lock. The v0.2.0 AI review listed the lock-file mechanism with 'No issues found'. `src/app/mod.rs:253-262; src/config/session.rs:1052-1110` | wrong-result | #39, #31 | K6 | code | user |
| FE-095 | 0.2.6 → 0.2.8 | Windows IME candidate box at screen origin or invisible (#103, #15) | Chinese/Japanese candidate list not near the cursor. | IMEOutput set in local widget coordinates; layer_transform_to_global() missing. `src/editor/ferrite/editor.rs:1957` | stuck | [] | K10 | code | user |
| FE-096 | 0.2.7 → 0.2.8 | '--' under a line renders it as H2; '-- ' lines collapse together | Norwegian dialogue text became headings or merged lines. | fix_false_setext_headings() only handled a single '-'. `src/markdown/parser.rs:496` | wrong-result | #27 | K8 | code | user |
| FE-097 | 0.2.7 → 0.2.8 | No space between paragraphs in rendered view (#109) | Paragraphs ran together. | item_spacing.y set to 1 px to keep viewport-culling height math tight. | cosmetic | #28 | K14 | changelog | user |
| FE-098 | 0.2.7 → 0.2.8 | Editing a plain paragraph in rendered view drops trailing spaces | Trailing double-space (a Markdown hard break) vanished from the file. | Edit buffer re-initialised from the AST every frame. | data-loss | #44 | K8 | changelog | user |
| FE-099 | 0.2.7 → 0.2.8 | Search highlights misplaced in tables; Jump-to menu above Find panel | Highlights off in table cells; menu covered the Find panel. | Find/render coordinate mapping; z-order. | cosmetic | [] | K9 | changelog | user |
| FE-100 | 0.2.7 → 0.2.8 | Search highlights drift after editing with Find open | Yellow boxes no longer over the matches after typing. | FindState.matches byte offsets not recomputed on edit. | wrong-result | #5 | K4 | changelog | user |
| FE-101 | 0.2.6.1 → 0.2.8 | Terminal: CJK characters overlap (#110) | Chinese output drawn on top of itself. | Every character assumed one column wide. | wrong-result | [] | K1 | changelog | user |
| FE-102 | 0.2.7 → 0.2.8 | Windows 11 borderless window: black bars, offset UI, dead buttons (#112) | UI drawn offset; buttons unclickable (Intel HD 4600). | DWM compositing with borderless glow surface; with_transparent(true) workaround. Close pending verification on target hardware. `src/main.rs:297-306` | stuck | [] | K10 | code | user |
| FE-103 | 0.2.7 → 0.2.8 | Scroll position leaks between tabs (#113) | Switching documents kept the previous scrollbar position. | Central-panel widget ids not scoped by tab id; egui ScrollArea state shared. | cosmetic | [] | K5 | changelog | user |
| FE-104 | 0.2.7 → 0.2.8 | Editing a table in rendered view strips bold/italic/strikethrough (#117) | Saving after a table edit removed formatting from every cell. | serialize_table and TableData::from_node used text_content(), which drops inline markup. `src/markdown/widgets.rs:880 (serialize_inline_content)` | data-loss | #44 | K8 | code | user |
| FE-105 | 0.2.7 → 0.2.8 | Linux Mint Cinnamon not recognised as native desktop (#116) | Unneeded portal fallback; cancelling a dialog reported as portal failure. | x-cinnamon missing from detection list; cancel misclassified. `src/files/dialogs.rs:121,192` | cosmetic | [] | K10 | code | user |
| FE-106 | 0.2.7 → 0.2.8 | Choosing some system fonts crashes the app (#114) | Selecting a .ttc, WOFF or corrupt font aborted Ferrite. | epaint panics on unsupported font data; also FONT_CUSTOM missing from the shaping match. `src/fonts.rs:773 (validate_font_bytes)` | crash | #9, #19 | K3 | code | user |
| FE-107 | 0.2.8-dev → 0.2.8 | Command palette crashed on commands that change view state | Toggle View Mode from the palette crashed. | Command executed mid-render, mutating state being drawn. `src/app/central_panel.rs:2473-2487` | crash | [] | K12 | code | maintainer |
| FE-108 | 0.2.7 → 0.2.8 | Rendered view unusable on large documents (#105) | 6k-line journal scrolled and typed with heavy lag. | Full parse + layout of the whole document every frame. | stuck | #13 | K11 | changelog | user |
| FE-109 | 0.2.8-dev → 0.2.8 | Uniform-height mode: wrapped lines overlap in 100K+ line files | Lines drawn over each other. | Wrapped galleys taller than the uniform line height. | cosmetic | #13 | K11 | changelog | maintainer |
| FE-110 | 0.2.7 → open | Ubuntu 24.04 Wayland: no keyboard input (#106) | Typing does nothing; workaround WAYLAND_DISPLAY=. | winit 0.29 Wayland backend; egui 0.34 shipped but not verified on hardware. | stuck | [] | K10 | changelog | user |
| FE-111 | 0.2.7 → open | macOS Sonoma: no keyboard input (#111) | Typing does nothing. | Suspected winit 0.29 input; not verified after the upgrade. | stuck | [] | K10 | changelog | user |
| FE-112 | 0.2.8 → 0.2.9 | Split/Rendered crashes on an empty document (#127) | Default view Split, new tab: app aborts. | Viewport-culling bootstrap used first_vis..=last_vis; with zero blocks it iterated once and indexed children[0]. `src/markdown/editor.rs:1531-1535 (half-open now), 1292` | crash | #9, #19, #28 | K12 | code | user |
| FE-113 | 0.2.8 → 0.2.9 | No dirty marker, no save prompt, no auto-save after raw edits | Edit, close: no '*', no 'Save changes?', work gone. | 0.2.8 cached is_modified() by content_version; raw FerriteEditor edits wrote tab.content without bumping it. `src/editor/widget.rs:819-834; src/state.rs:1984-2016` | data-loss | #1, #6, #28, #32 | K7 | code | user |
| FE-114 | 0.2.8 → 0.2.9 | Undo/redo did nothing after typing ('Nothing to undo') | Ctrl+Z could not undo anything typed in raw mode. | Ctrl+Z read tab.edit_history, which raw-mode edits never reached. `src/editor/widget.rs:470, 833` | data-loss | #1, #7, #28, #32 | K7 | code | user |
| FE-115 | 0.2.8 → 0.2.9 | Selection invisible in light mode (#121) | Selected text showed no highlight. | Pale selection colour at ~40% alpha over white. CHANGELOG and ROADMAP describe different fixes. `src/theme/mod.rs:219` | cosmetic | [] | K15 | code | user |
| FE-116 | 0.2.8 → 0.2.9 | Side-panel tab labels overlap at default width | Outline/Stats/Links/FM/Hub labels clipped. | Width / 5 per tab at a 200 px default. | cosmetic | #24 | K14 | changelog | user |
| FE-117 | 0.3.0-rc → 0.3.0 | Pasting mixed-script text aborts the app (I-3) | Paste of 'Hebrew: שלום' or 'note: 你好' killed Ferrite (0xc0000409). | is_url sliced &s[colon_pos..colon_pos+3] across a multi-byte char; runs on every paste. `src/app/input_handling.rs:141-160` | crash | #9 | K1 | code | maintainer |
| FE-118 | 0.2.8 → 0.3.0 | Only the first of consecutive fenced code blocks visible (#129) | Later code blocks blank or pushed off-screen. | Horizontal ScrollArea with auto_shrink([false,false]) produced wrong heights that the 0.2.8 height cache then latched. | wrong-result | #28 | K14 | changelog | user |
| FE-119 | 0.2.8 → 0.3.0 | Empty table cells hard to click and to Tab into (#131) | Could not start typing in an empty cell. | Zero-width hit target. | stuck | [] | K5 | changelog | user |
| FE-120 | 0.2.8 → 0.3.0 | Rendered/split: two clicks needed to move to another block | First click only defocused the edited block. | Per-widget defer/commit logic racing egui focus and content_hash id remaps. | stuck | [] | K5 | changelog | user |
| FE-121 | 0.2.8 → 0.3.0 | Caret flashes or vanishes while typing in rendered headings | Cursor disappeared mid-word. | ui.push_id(content_hash) remapped every TextEdit id when the text changed. | cosmetic | [] | K5 | changelog | user |
| FE-122 | 0.2.8 → 0.3.0 | Formatted block stuck in raw edit mode after clicking away | **bold** markers stayed visible as raw text. | Blur exit deferred one frame and never re-checked. | stuck | #8 | K5 | changelog | user |
| FE-123 | 0.2.8 → 0.3.0 | Rendered tables: two clicks to edit another cell after typing | First click on another cell ignored. | Table focus fought session focus. | stuck | [] | K5 | changelog | user |
| FE-124 | 0.2.8 → 0.3.0 | Ctrl+P ranked unrelated recent files above real matches | Typing 'tables' did not find test_tables.md first. | +100 recent-file boost and loose full-path fuzzy match. | wrong-result | [] | K18 | changelog | user |
| FE-125 | 0.2.7 → 0.3.0 | Frontmatter panel shows the previous file; 'Add frontmatter' splices the wrong body | FM tab showed another file's fields or 'No frontmatter'; adding frontmatter could write another tab's body. | Cache keyed on content_version alone; every tab's counter starts at 0. `src/ui/frontmatter_panel.rs:225-264` | data-loss | #5 | K4 | code | user |
| FE-126 | 0.2.8 → 0.3.0 | Preview 'ghost snaps' after scrolling with Sync off | Preview jumped after scrolling stopped. | Stale pending_scroll_* from earlier sync still applied. | cosmetic | #8 | K4 | changelog | user |
| FE-127 | 0.3.0-dev → 0.3.0 | Split 2-way sync: preview jumps up when scrolled to bottom | Preview bounced away from the bottom. | Raw-pane target written into the slot the preview consumes. | cosmetic | [] | K4 | changelog | maintainer |
| FE-128 | 0.2.8 → 0.3.0 | File opened from Explorer lost when the recovery dialog appears | After a crash, double-clicking a file showed the recovery dialog; choosing Restore never opened the file. | CLI/file-association paths dropped while the modal was up. | wrong-result | #18 | K6 | changelog | user |
| FE-129 | 0.2.8 → 0.3.0 | Recovery/autosave applied to an unrelated tab; save overwrote the real file (Task 106) | A file opened with another buffer's text; saving destroyed the file's real content. | Recovery files persisted across launches but keyed by tab_id, which restarts every launch. `src/state.rs:5279-5321 (identity gating now); src/config/session.rs` | data-loss | #25 | K6 | code | user |
| FE-130 | 0.3.0-dev → 0.3.0 | Second crash/restore cycle silently discards every edit since the first restore (Task 106.6) | Edit, kill, restore OK; edit again, kill, restore: back to the pre-first-edit text. | Restore built the tab with Tab::with_file(path, recovered), making original_content the recovered buffer; next snapshot stored the wrong disk hash, which the next launch rejected. Residual branch remains (L-03). `src/state.rs:4959-4990` | data-loss | [] | K6 | code | maintainer |
| FE-131 | 0.3.0-dev → 0.3.0 | Export menu shows double icons | PDF / Print preview items had two icons. | Locale strings still contained emoji while the ribbon added Phosphor icons. | cosmetic | #23 | K14 | changelog | maintainer |
| FE-132 | 0.3.0-dev → 0.3.0 | Outline panel tab selector not clickable | Tabs in the side panel ignored clicks. | Nested allocate_ui_at_rect for icon labels broke hit-testing. | stuck | [] | K9 | changelog | maintainer |
| FE-133 | 0.2.8 → 0.3.0 | Mermaid flowcharts right-shifted with a big left gap (#83) | Diagrams with loops looked right-aligned. | Layers centred in available width while renderer sized to node bounds. | cosmetic | [] | K14 | changelog | user |
| FE-134 | 0.2.8 → 0.3.0 | Multi-cursor copy/cut kept only the primary selection | Cut with several cursors deleted every selection but the clipboard held one. | selected_text() returned only the primary range. `src/editor/ferrite/editor.rs:651` | data-loss | [] | K7 | code | user |
| FE-135 | 0.2.8 → 0.3.0 | Search in Files panel grows to full height frame by frame | Panel crept open slowly. | egui Window resize grows to last content size each frame. | cosmetic | [] | K14 | changelog | user |
| FE-136 | 0.2.8 → 0.3.0 | Detached Productivity Hub fights resizing | Window snapped back wider. | Content re-expanded window; 560 px width floor. | cosmetic | [] | K14 | changelog | user |
| FE-137 | 0.2.8 → 0.3.0 | CSV cells overflow into neighbouring columns | Long values drawn across columns. | 50-character cap does not guarantee pixel fit. | cosmetic | [] | K14 | changelog | user |
| FE-138 | 0.2.8 → 0.3.0 | Per-document view mode forgotten after closing the tab | File reopened in the default mode, not the one last used. | open_file ignored saved TabInfo; closing a tab dropped its entry on next save. | wrong-result | #4 | K6 | changelog | user |
| FE-139 | 0.3.0-dev → 0.3.0 | Quick note: closing a modified untitled tab discarded it without asking | Ctrl+W on a scratch tab with text: gone, no prompt. | Exit-only exemption applied to every close. `src/state.rs:2106-2136, 3242` | data-loss | #6 | K7 | code | maintainer |
| FE-140 | 0.2.8 → 0.3.0 | Document nav buttons painted above modal panels | Scroll buttons showed over Ctrl+P, palette and Search. | Both used Order::Foreground. `src/ui/nav_buttons.rs:106` | cosmetic | [] | K9 | code | user |
| FE-141 | 0.2.8 → 0.3.0 | Rendered view: Ctrl+Home/End moved within the block, not the document | Could not jump to document start/end in rendered mode. | Inline TextEdit consumed the keys. | wrong-result | #20 | K13 | changelog | user |
| FE-142 | 0.3.0-rc → 0.3.0 | Resizing from the bottom-right corner opens About/Help (I-1) | Releasing a resize drag opened the Help dialog. | Status-bar ? button overlapped the resize grab zone. `src/ui/window.rs:366` | cosmetic | [] | K9 | code | maintainer |
| FE-143 | 0.3.0-rc → 0.3.0 | Terminal echoes CJK input as ???? (I-2) | Prompt line showed question marks; shell received the right text. | Windows console code page not UTF-8. | wrong-result | [] | K2 | changelog | maintainer |
| FE-144 | 0.2.8 → 0.3.0 | Clicking a task checkbox nudges the preview scroll | Preview jumped when ticking a box. | One-char change invalidated culling; pointer-down treated as scrolling. | cosmetic | [] | K4 | changelog | user |
| FE-145 | 0.3.0-rc → open | UTF-16LE files rejected as binary (I-4) | Cannot open UTF-16 files under 5 MB; Ferrite offers UTF-16 when saving. | is_binary_content() rejects any null byte before BOM detection; ≥5 MB background path decodes BOM and opens. `src/state.rs:153-162, 4124, 2285` | stuck | #6 | K2 | code | maintainer |
| FE-146 | 0.2.8 → 0.3.0 | Intel macOS: font picker shows a spurious error toast (#133) | Error toast when browsing fonts. | Font loaded on hover/preview instead of on selection. | cosmetic | [] | K3 | changelog | user |
| FE-147 | 0.2.8 → open | macOS 15: unsigned .app blocked by Gatekeeper (#130) | App refuses to open without quarantine removal. | Not notarised; documented workaround only. | stuck | [] | K10 | changelog | user |
| FE-148 | 0.3.0-dev → 0.3.0 | Quick note: clean exit deleted recovery/, losing scratch tab text | Untitled notes gone after a normal restart. | Exit path deleted recovery/ instead of only the crash snapshot. | data-loss | [] | K6 | changelog | maintainer |
| FE-149 | 0.2.7 → 0.3.1 | Opening from Explorer doesn't raise the running window (#147) | File opened in a background window. | Windows foreground lock; AllowSetForegroundWindow added (unreleased). | cosmetic | [] | K10 | changelog | user |
| FE-150 | 0.2.6 → open | Word-wrapped documents micro-stutter while scrolling | Visible stutter scrolling wrapped text. | Per-line galley cost or height-cache granularity (unknown). | cosmetic | #13 | K11 | changelog | user |
| FE-151 | 0.3.0 → open | Code-block Run output attaches to the wrong block after edits above | Output disappears or appears under another block. | Run state keyed by the block's start line. | wrong-result | #5 | K4 | changelog | maintainer |
| FE-152 | 0.3.0 → open | bash fences on Windows without Git Bash run bash source as PowerShell/cmd | Confusing spawn/parse errors. | Fallback interpreter writes temp files with that interpreter's extension but keeps bash source. | wrong-result | [] | K10 | changelog | maintainer |
| FE-153 | 0.2.0-rc → 0.2.x | Git 'ignored' status never shown | Ignored files had no badge. | include_ignored(false) meant GitFileStatus::Ignored was never set (found by the v0.2.0 AI review). `src/vcs/git.rs:296 (now true)` | cosmetic | [] | K18 | code | maintainer |
| FE-154 | 0.2.6 → 0.2.6.1 | Portable zip shipped without portable/ folder; settings went to the user profile (#76 part 3) | Portable copy wrote settings to AppData. | Packaging omitted the marker folder; the 0.2.7 issue reply called the behaviour 'by design'. | wrong-result | #37 | K10 | changelog | user |

### 1.4 Notes on specific rows

- **#46 is misreported.** The PRD says #46 was Ctrl+B (Bold vs File Tree), with the fix "move File Tree to Ctrl+Shift+E". The CHANGELOG calls #46 the Ctrl+Shift+E collision, which is the fix's own regression. I split it into FE-064 and FE-065.
- **#63 "fixed" twice.** The CHANGELOG puts the fix in 0.2.6.1; the issue reply says "COMPLETED in v0.2.7 (was tagged 0.2.6.1)" and tells users to uninstall to clear config.
- **Re-fixes:** minimap byte offsets (FE-039 then FE-045), box-drawing glyphs (listed in both 0.2.5.3 and 0.2.6), CJK first-line indentation (FE-035 then FE-076).
- **Reviewer escape on record:** `code-review-v0.2.0-findings.md` reviewed session persistence ("Lock file mechanism for crash detection … No issues found"). Crash detection was broken until 0.2.7 (FE-094).
- **0.2.9 was a hotfix for four critical 0.2.8 regressions.** Two were data-loss (FE-113, FE-114) and were side effects of the 0.2.8 per-frame O(N) performance work.

---

## 2. Classes

### 2.1 Ranking

Score = our ledger weights (data-loss 8, wrong-result 5, crash 4, stuck 2, cosmetic 1), doubled for a regression.

| Rank | Class | Name | Bugs | Worst | Data-loss | Crash | Score | Top instincts | Bugs with an instinct |
|---|---|---|---|---|---|---|---|---|---|
| 1 | K7 | Edit paths that skip shared bookkeeping | 8 | data-loss | 6 | 0 | 70 | #6×3, #7×2, #1×2 | 7/8 |
| 2 | K4 | Stale derived state and wrong cache keys | 15 | data-loss | 1 | 0 | 62 | #5×7, #13×2, #28×1 | 10/15 |
| 3 | K6 | Persistence, recovery and durable identity | 9 | data-loss | 3 | 0 | 50 | #1×1, #39×1, #31×1 | 5/9 |
| 4 | K14 | Rendering and layout fidelity | 23 | wrong-result | 0 | 0 | 40 | #23×2, #6×2, #28×2 | 8/23 |
| 5 | K13 | Key routing and shortcut collisions | 7 | data-loss | 1 | 0 | 39 | #20×2, #23×1, #28×1 | 4/7 |
| 6 | K8 | Text round-trip fidelity | 6 | data-loss | 2 | 0 | 36 | #44×3, #27×1 | 4/6 |
| 7 | K10 | Platform, desktop environment and packaging | 16 | wrong-result | 0 | 0 | 34 | #18×1, #37×1 | 2/16 |
| 8 | K1 | Byte / char / column confusion in string indexing | 7 | wrong-result | 0 | 3 | 32 | #9×3, #19×1, #26×1 | 4/7 |
| 9 | K5 | Widget identity and focus (immediate-mode UI) | 13 | data-loss | 1 | 0 | 32 | #17×2, #5×1, #22×1 | 5/13 |
| 10 | K12 | Hostile, empty and corrupt input | 5 | crash | 0 | 5 | 24 | #9×4, #19×2, #28×1 | 4/5 |
| 11 | K3 | Glyph and font availability | 10 | crash | 0 | 2 | 19 | #26×2, #9×2, #19×1 | 3/10 |
| 12 | K11 | Performance at real size and at idle | 11 | stuck | 0 | 0 | 18 | #13×9 | 9/11 |
| 13 | K9 | Hit zones, z-order and custom window chrome | 13 | stuck | 0 | 0 | 17 | #24×1 | 1/13 |
| 14 | K2 | Encoding and code pages at I/O boundaries | 2 | wrong-result | 0 | 0 | 7 | #6×1 | 1/2 |
| 15 | K18 | Other feature logic | 2 | wrong-result | 0 | 0 | 6 | none | 0/2 |
| 16 | K15 | Theme visibility | 4 | cosmetic | 0 | 0 | 4 | none | 0/4 |
| 17 | K16 | Silent failure and fake affordances | 3 | stuck | 0 | 0 | 4 | #18×2, #17×1 | 3/3 |

### 2.2 What dominates

- **By cost, state integrity dominates:** K7 edit-path bookkeeping, K4 stale state and cache keys, K6 persistence and recovery identity. Together they hold 10 of the 14 data-loss bugs. Each one is a write path, cache or durable file that doesn't carry the identity or bookkeeping the rest of the system assumes.
- **By count, the desktop surface dominates:**
  - rendering fidelity (K14, 23);
  - platform and packaging (K10, 16);
  - widget identity and focus (K5, 13);
  - hit zones and window chrome (K9, 13);
  - glyphs and fonts (K3, 10);
  - performance (K11, 11).
- **Crashes are almost all hostile text or empty input:** UTF-8 slicing (K1), empty document, NaN config, corrupt fonts, malformed Mermaid. With `panic = "abort"`, every one kills the whole app.
- **Fixes make bugs.** 7 escaped bugs tie to #28, and #28 is Ferrite's top-scoring instinct. The 0.2.8 performance work caused the dirty-flag and undo data-loss; the culling work caused paragraph spacing and the fenced-block bug; the #46 fix caused a new collision; the Duplicate Line fix introduced L-01.

### 2.3 Our instincts on Ferrite

| # | Instinct | Ferrite bugs | Score |
|---|---|---|---|
| 28 | Fixes make bugs | 7 | 66 |
| 5 | The screen is stale | 8 | 46 |
| 9 | Every input is hostile | 9 | 40 |
| 1 | Every write has a partner | 3 | 37 |
| 6 | A rule at one door is a rule at every door | 6 | 33 |
| 32 | Green checks prove intent, not behavior | 2 | 32 |
| 7 | Undo reverses exactly what it did, nothing more | 3 | 29 |
| 13 | Test at real size | 11 | 26 |
| 44 | What you show is what you save | 4 | 22 |
| 19 | One broken view doesn't kill the app | 4 | 20 |
| 4 | Missing is not blank | 2 | 13 |
| 20 | Shortcuts don't fire while typing | 2 | 13 |
| 26 | "Fixed" means proven, not claimed | 4 | 11 |
| 18 | Never fake success, never spin forever | 4 | 10 |
| 27 | Fix the class, not the instance | 2 | 10 |
| 25 | When data lands wrong, say so loudly | 1 | 8 |
| 17 | Every dead end is a bug | 3 | 5 |
| 22 | Focus goes back where it came from | 1 | 5 |
| 31 | The reviewer mustn't be the author | 1 | 5 |
| 37 | The docs' front door matches today | 1 | 5 |
| 39 | Prove the test catches the bug | 1 | 5 |
| 8 | A failure leaves nothing behind and jams nothing | 2 | 3 |
| 23 | Same thing, same name, same format | 3 | 3 |
| 24 | Test on the user's real screen | 2 | 2 |

**Never applied to any Ferrite bug:** #2 Assume the double-click, #3 Assume two people at once, #10 Money checks itself, #11 Dates have a direction, #12 Exports run code, #14 Migrations go backward too, #15 Files on disk don't roll back, #16 A greyed-out button says why, #21 Session expiry is a normal path, #29 Freeze features while stabilizing, #30 Measure with a fixed yardstick, #33 Domain testing finds what code review can't, #34 Decide the direction before polishing, #35 "Offline" is proven by cutting the network, not by grep, #36 Check the license when you add the asset, #38 Someone else must be able to run it, #40 A changed test expectation needs a reason, #41 The governing documents live in the repo, #42 Expected numbers come from outside the code, and must be able to tell values apart, #43 One PC, many people, #45 Selection follows what's on screen.

Why they're absent:
- **Domain:** #10 money, #11 dates, #12 exports run code, #14 migrations, #21 session expiry, #43 one PC many people.
- **Architecture:** #2 and #3 are server concurrency; Ferrite's analogue is two widgets writing one field (FE-043, FE-127), which I mapped to #5. #15 needs a database transaction.
- **PrivateApp process misses:** #29, #30, #34, #35, #36, #38, #40, #41 and #42 were not visible in Ferrite's bug records. Ferrite shows the same process failures (§3), but as causes, not as bugs. L-06's test that accepts the bug is a #42/#39 case; L-11 is #41.
- **#19** ("one broken view doesn't kill the app") now appears only through FE-015, FE-031, FE-106 and FE-112. In Rust with `panic = "abort"` there is no boundary to wrap. The instinct needs a Rust form: views must not panic, and any boundary must be proven in the release profile (L-14).

**Coverage gap:** 84 of 154 Ferrite bugs (55%) map to no existing instinct. They concentrate in:
- K10 platform: 14 of 16 unmapped;
- K14 rendering: 15 of 23;
- K9 hit zones: 12 of 13;
- K5 widget identity: 8 of 13;
- K3 glyphs: 7 of 10;
- K15 themes: 4 of 4.

Our catalogue was learned on a web app; it is weakest exactly where a native desktop editor differs.

### 2.4 Candidate new instincts

These are drafts in our format. The numbers are suggestions; only the developer assigns permanent numbers.

#### 46. Bytes are not characters
- **Instinct:** every index into text says which unit it is: byte, char, grapheme or screen column. Every slice is checked against that unit.
- **Missed (Ferrite):**
  - crashes: FE-015 tree viewer, FE-092 binary/stats, FE-117 paste;
  - drift: FE-021, FE-039, FE-045 highlights;
  - display width: FE-101 terminal overlap, FE-137 CSV;
  - code page: FE-143;
  - live: L-01 line ops.
  
  Ferrite's own `ai-context.md` lists "Byte vs char index" as a critical gotcha, and the class still escaped four more times.
- **Ask:** what unit is this number in, who produced it, and what happens when the char at that position is 2, 3 or 4 bytes?
- **Prove it:** run every text action (paste, find, line ops, truncate, stats, terminal echo) over a fixture of Hebrew, Bengali, CJK, emoji ZWJ and combining marks, with the cursor placed just after a multi-byte character, in the release profile.
- **Checklist:** "Every text action works with the cursor after ø, 你 and 👨‍👩‍👧, in a release build?"

#### 47. Every glyph needs a font that has it
- **Instinct:** a character you draw is only visible if a loaded font contains it, on the user's machine and in the user's language.
- **Missed:**
  - FE-011, FE-013, FE-048, FE-049 (fixed twice), FE-061;
  - FE-084, FE-085 (UI language switch);
  - FE-072, FE-106 (font loading crashes);
  - FE-131 (double icons).
- **Ask:** which font draws this, if the user has none of my fonts and the UI is in Japanese?
- **Prove it:** a coverage test over every UI string, icon literal and locale file against the shipped fonts. Launch with each UI language and an empty system font directory, then screenshot.
- **Checklist:** "Every UI string and icon renders in every UI language with only the bundled fonts?"

#### 48. A cache key must tell its contents apart
- **Instinct:** a cache, version counter or "same length means same" shortcut is only safe if no real change can leave the key equal. That is especially true when the cached value gets written back.
- **Missed:**
  - FE-113 (`is_modified` keyed on a counter that writers forget to bump);
  - FE-125 (per-tab counter used across tabs);
  - FE-100 (match offsets kept across edits);
  - live: L-06 (sampled hash), L-07 (same length assumed unchanged), L-02.
- **Ask:** what change leaves this key the same, such as the same length, a mid-file edit, another tab at version 0, or a writer that skips the bump? What gets written back from the stale value?
- **Prove it:** for each cache, mutate the content while holding the key's inputs constant. Assert a miss, and assert no write-back of stale data. Related to #42, but for runtime caches.
- **Checklist:** "Every cache misses on a same-length mid-file change and on another document at the same version?"

#### 49. Widget identity never depends on what it edits
- **Instinct:** in immediate-mode UI, a widget's id and focus must survive the user's own keystroke, an insert above, and a tab switch.
- **Missed:**
  - FE-002 (edits land in another item);
  - FE-026 (cell loses focus every keystroke);
  - FE-103 (scroll state leaks across tabs);
  - FE-120, FE-121, FE-123 (two clicks needed, caret vanishes);
  - FE-070, FE-025.
- **Ask:** when the user types one character, does any id, index or key in scope change?
- **Prove it:** a scripted run that types into, switches between, and inserts above each block type, asserting focus and caret position. Also run it with two tabs of identical content.
- **Checklist:** "Typing, inserting above and switching tabs keep focus and caret in every editable block?"

#### 50. Durable data carries durable identity
- **Instinct:** anything that outlives the process (recovery files, per-file settings, run output) is keyed by something that also outlives it, and restoring must not rewrite the baseline it is compared against.
- **Missed:**
  - FE-129 (recovery keyed by tab id, which restarts each launch: overwrote a real file);
  - FE-130 (restore made the recovered text the "original": second crash lost everything);
  - FE-148 (clean exit deleted recovery);
  - FE-151 (run output keyed by line number);
  - FE-040 (per-tab maps never freed);
  - FE-094 (lock file);
  - live: L-03.
- **Ask:** what is this keyed by, and is it still unique after a restart? After a restore, what does "modified" compare against?
- **Prove it:** crash, restore, edit, crash, restore (two cycles). Do it with tabs opened in a different order, with the file missing, renamed, non-UTF-8 and edited externally. Assert no buffer appears in the wrong tab, and edits survive with the dirty mark shown.
- **Checklist:** "Two crash/restore cycles, files missing or renamed: every edit back, in the right tab, still marked unsaved?"

#### 51. One point, one owner
- **Instinct:** every pixel of the window chrome has exactly one owner for press, drag and release, and paint order matches that owner.
- **Missed:**
  - FE-020, FE-037, FE-042, FE-055 (Linux title bar);
  - FE-036, FE-142 (button inside a resize zone);
  - FE-132, FE-140, FE-099, FE-066, FE-050.
- **Ask:** for this control, what else is under the pointer, and which one wins on release?
- **Prove it:** scripted presses and drags at every edge, corner and title-bar control, at 100/125/150% scaling, on Windows, X11 and Wayland.
- **Checklist:** "Every edge, corner and title-bar control does one thing at 100/125/150%, on each OS?"

#### 52. Every key has exactly one owner
This extends #20.
- **Instinct:** each default binding is unique, wired to a handler, and not swallowed first by an inline widget or an IME composition.
- **Missed:**
  - FE-006 (paste collision);
  - FE-064, FE-065 (the fix's own collision), FE-071;
  - FE-091 (IME Backspace deleted committed text);
  - FE-141 (inline widget ate Ctrl+Home);
  - live: L-09.
- **Ask:** what else is bound to this, what OS convention does it shadow, and who sees the key first?
- **Prove it:** a test that every default binding is unique and every command in the table is dispatched; an IME composition test with Backspace, Enter and arrows; global keys tested while an inline editor has focus.
- **Checklist:** "Default bindings unique and all dispatched; IME composition swallows editing keys?"

#### 53. Text round-trips byte for byte
This extends #44 from fields to files.
- **Instinct:** open, view, copy or edit one part, and save: every byte you didn't intend to change is identical. That covers newlines, trailing spaces, inline markup, BOM and encoding.
- **Missed:**
  - FE-104 (table edit stripped formatting);
  - FE-098 (trailing spaces dropped);
  - FE-054 (`lines()` stripped newlines);
  - FE-093 (copy added spaces);
  - FE-090, FE-096 (setext misparse);
  - live: L-04, L-05.
- **Ask:** what does this view or serializer drop or add that the source had or didn't have?
- **Prove it:** a golden-file corpus (CRLF, BOM, trailing spaces, setext edge cases, tables with inline markup, Windows-1252, UTF-16) opened and saved through each view and serializer. Assert a byte-identical result except for the intended edit.
- **Checklist:** "Corpus open-edit-one-cell-save is byte-identical elsewhere, in every view?"

#### 54. Their machine is not your machine
- **Instinct:** a desktop build is untested on any OS, display server, desktop environment, DPI or install path you didn't run it on, and a fix there isn't fixed until it runs there.
- **Missed:**
  - FE-012 (glibc);
  - FE-019, FE-080, FE-147 (macOS packaging);
  - FE-046 (Finder UTI);
  - FE-095 (IME coordinates);
  - FE-102, FE-110, FE-111 (open or "fixed" pending hardware);
  - FE-079, FE-105 (portals).
- **Ask:** which rows of the platform matrix did this build actually run on?
- **Prove it:** a release matrix with a named owner per OS row, and status "fixed" only when that row has run on the target. Build on the oldest supported runner.
- **Checklist:** "Built on the oldest supported target and run on each OS row before 'fixed'?"

#### 55. Idle is a state
- **Instinct:** in an immediate-mode UI, every line in the frame loop runs 60 times a second. At rest the app should do nothing, and no per-frame path may touch the whole document.
- **Missed:**
  - FE-033 (10% idle CPU);
  - FE-029 (log spam, hover repaint);
  - FE-056 (1.8 GB: clone per frame);
  - FE-086, FE-108.
- **Ask:** what does this cost per frame when nothing changes?
- **Prove it:** idle CPU and allocations per idle frame measured with a large document open, with a ceiling enforced in CI. Complements #13 (size) with frequency.
- **Checklist:** "Idle CPU under 1% and zero O(N) work per frame with a 100 MB file open?"

#### 56. Every theme is a test target
- **Instinct:** light mode is a second product, and every text and background pair is checked in each theme.
- **Missed:** FE-004, FE-007, FE-082 (white on white), FE-115 (invisible selection).
- **Ask:** did I look at this in light and dark, including pressed, selected and disabled states?
- **Prove it:** screenshot tests per theme, plus a contrast check over the theme's token pairs.
- **Checklist:** "Every state readable in light and dark?"

#### 57. The safety net must fire in the shipped build
This could be an amendment to #39.
- **Instinct:** a guard is only real if it works under release settings (`panic = "abort"`, LTO, no debug assertions).
- **Missed:** L-14. `catch_unwind` cited for FE-031 and FE-106 cannot catch anything in release, while tests run with unwinding and pass.
- **Ask:** does this guard depend on a build setting that differs between test and release?
- **Prove it:** run guard tests with the release profile, or against the shipped binary.
- **Checklist:** "Each crash guard seen working in a release build?"

#### 58. The handover is code
Process; this extends #41.
- **Instinct:** handover prompts and context files are checked against the repo like code: one source, and every command, path and number must exist today.
- **Missed (Ferrite):**
  - the root handover says `python -m pytest` in a Rust repo;
  - two handover systems (Task Master vs cyclopsctl) and two `ai-context.md` files with opposite rules (L-11);
  - undo limits stated differently in the CHANGELOG and the context file (L-12);
  - an issue reply giving shortcuts that don't exist (L-10).
- **Ask:** if the agent follows this handover literally, does every command run and every path exist?
- **Prove it:** a script that extracts commands, paths and constants from handover and context files and checks them against the repo, failing on a miss.
- **Checklist:** "Every command and path in the handover runs and exists?"

#### 59. A test plan nobody ran is not a gate
Process; related to #26 and #30.
- **Instinct:** a release is gated on an executed plan with a signed row (tester, build SHA, results), not on the plan existing.
- **Missed (Ferrite):**
  - the v0.2.8 suite had 0 of 237 boxes checked, yet it names "Modified indicator (*) updates correctly" and "Ctrl+Z / Ctrl+Y — undo/redo", the two data-loss regressions that 0.2.9 hotfixed;
  - every "Issues Found" table is empty.
- **Ask:** who ran this, on which build, and where did failures go?
- **Prove it:** the tag script refuses unless the plan has a sign-off row with a SHA and every P0 line is marked.
- **Checklist:** "Release plan executed, signed with a build SHA, failures logged?"

**Smaller candidates (one bug each, so not drafted):**
- Never mutate what you're drawing (FE-107, palette crash mid-render).
- Plural by default (FE-134, multi-cursor cut kept one selection).

---

## 3. Process lessons from Ferrite's AI workflow

The workflow is close to ours: PRD → Task Master tasks → one fresh Cursor/Claude session per task → paste a handover → test by hand → "update handover" prompt → next session.

**1. Nobody owns edge cases.**
- "The AI handles code quality (patterns, style, edge cases). I handle product quality (does this feature make sense?)." (`docs/ai-workflow/ai-development-workflow.md:122`)
- In the ledger above, edge cases (empty document, non-ASCII, second crash cycle, light mode, Linux) are where the bugs live. Our equivalent is the reviewer; no code review is recorded in Ferrite after v0.2.0.

**2. Confidence rose while severity didn't fall.**
- "I trust the AI more now than I did a year ago." (`ai-development-workflow.md:558`)
- After that was written: 0.2.8 shipped two data-loss regressions (hotfixed in 0.2.9), and 0.3.0 fixed two more data-loss bugs (FE-129, FE-130, the second labelled CRITICAL) plus a CRITICAL abort on paste. The trend measure was the author's feeling, not escapes. This matches our #30 and the ledger's "escapes going down" rule.

**3. Task-scoped handovers strip the context a class fix needs.**
- "Handovers should be task-focused, not project-focused." (`ai-development-workflow.md:107`)
- The anti-pattern list removes "Previous task details — Unless the current task directly continues from it" (`:423`).
- Results:
  - the 0.2.6.1 Duplicate Line rewrite lost the char-to-byte handling that 0.2.3 had described (L-01);
  - Task 106.6 fixed one restore branch and left the sibling (L-03);
  - the 0.2.9 dirty-flag fix covered raw typing but not the `record_edit` paths (L-02).
- Our #27 needs the class in front of the fixer. A task-only handover hides it.

**4. Handover drift.**
- The root `current-handover-prompt.md` says "Run `python -m pytest` before finishing; meet the task test strategy." in a Cargo project.
- Its task is "Manual QA + documentation only" on Wayland, Sonoma and Windows hardware, assigned to "Composer 2.5". The test strategy is "Diff review of the matrix and CHANGELOG confirms no row left blank", which rewards filling rows, not running them.
- `ai-context.md` (root) says "DO: Update `ai-context.md` project memory"; `docs/ai-context.md` says "Never auto-update this file".
- Compare our #41: Ferrite's governing documents are in the repo, but there are two of each and nothing checks them.

**5. A broken suite gets normalised.**
- "Full `cargo test` may fail due to pre-existing unrelated test compile errors on this branch — fix only if your changes touch those modules." (`docs/current-handover-prompt.md`)
- The PR #74 audit: "Tests: 973 passed, 1 failed (pre-existing, unrelated)" (`.planning/v0.5.0-MILESTONE-AUDIT.md`).
- The v0.3.0 matrix verified the I-3 fix while "verification blocked by 2 unrelated WIP build errors", on "uncommitted" builds (`v0.3.0-regression-matrix.md:423-424`).
- Our #28 (re-run the whole battery) is impossible if the battery doesn't compile.

**6. Plans written, not run.**

| Plan | Boxes checked |
|---|---|
| v0.2.6 suite | 105 of 186 |
| v0.2.7 plan | 47 of 156 |
| v0.2.8 suite | 0 of 237 |
| v0.3.0 suite | 134 of 135 |

- Sign-off and "Issues Found" are empty in the three suites that have them; the v0.2.7 plan has neither.
- The v0.2.8 suite lists "Unsaved changes dialog appears if tab has modifications" (§2), "Modified indicator (*) updates correctly" (§4.3) and "Ctrl+Z / Ctrl+Y — undo/redo" (§12.1). Those three lines describe the 0.2.9 critical regressions.
- When the v0.3.0 matrix was actually executed, it caught an S1 crash (I-3) and three more issues before release.
- **Lesson:** the plan was good, and running it was the missing step.

**7. AI review checked docs against code, not behaviour.**
- The v0.2.0 review method: "Read the technical documentation… Check for consistency between docs and code" (`code-review-handover.md:20-26`).
- Its verdict: "Documentation ⭐⭐⭐⭐⭐ Excellent - docs match implementation" and "I found **no critical bugs**" (`code-review-v0.2.0-findings.md:12,19`). Session persistence got "No issues found" while crash detection was broken (FE-094).
- The Gemini v0.1.0 review never read code ("Based on the egui + eframe stack and your feature set, the core loop appears to be…"). It warned about path separators, which never escaped. It missed every class that did.
- The contributor's GSD audit scored "15/15 requirements … PASSED" by locating symbols ("✓ Task::from_markdown()"). The maintainer's own checklist the same week said "❌ **Do not merge yet** — Memory blocker" (4x memory) (`checklist-pr74.md`).
- Same lesson as our #31 and #32. The new detail is that an AI reviewer given the author's docs grades the docs.

**8. Refactors claim zero behaviour change without proof.**
- "Zero behavior changes, all 83 tests pass" (flowchart split, CHANGELOG 0.2.7).
- The app.rs split (0.2.6.1) shipped with three bugs from a stale mirror field `tab.cursors` left behind by the FerriteEditor rewrite (FE-063, FE-067, FE-068).
- `refactoring-assessment.md` is a line-count inventory ("No code was changed for this assessment"), with no risk or behaviour content.
- `refactor.md` is a pasted chat answer ("Based on our discussion and your repository's goals, I have designed…") targeting eframe 0.29 and comrak 0.18 while the project was on egui 0.28 heading to 0.34. It was never reconciled or executed.
- Lesson for us: a refactor needs our #39-style proof (the behaviour battery before and after), not a passing unit suite.

**9. Root-cause writing is excellent, but it never becomes a check.**
- Almost every CHANGELOG fix has a "Root cause" paragraph and a pinned test. That is better than most human projects, and it made this mining possible.
- But the lessons stay prose. `docs/ai-context.md` lists "Byte vs char index" under "Critical Gotchas", and that class escaped again in May 2026 (I-3) and is live today (L-01).
- A gotcha table is not a check. This is the exact gap Dev Instincts exists to close: miss → instinct → test.

**10. User-facing text is generated and unchecked.**
- Issue-reply drafts give shortcuts that don't exist (L-10).
- #63's fix version disagrees with the CHANGELOG.
- ROADMAP and CHANGELOG describe different fixes for #121.
- Our #37 covers the docs' front door. Ferrite adds support replies as a channel that reaches users.

**What worked and is worth copying:**
- the bug-fix handover template's **"Previous Attempts"** and **"Regression Check"** sections (`docs/handover/template-handover-bugfix.md`);
- stable test IDs in the regression matrix (LAU/FILE/KBD/IME…);
- identity-gated recovery that emits diagnostic events on rejection (`session_recovery_identity_mismatch`);
- severity S1–S3 with an explicit release gate.

When those were used (v0.3.0), the release went out with its S1 caught.

---

## 4. Calibration exercise: replaying escaped bugs through the instinct reviewer

**Goal:** measure the reviewer's recall on bugs a human found later, before Ferrite's findings are added to the ledger.

### Set-up (same for every case)

1. **Copy, never edit:** `cp -r kb/ferrite/Ferrite-master <scratch>/replay-RN` and a second copy `<scratch>/control-RN`.
2. **Reconstruct** the buggy code in `replay-RN` with the one hunk given below. Leave `control-RN` as shipped (fixed).
3. **Strip the answers from both copies:**
   - delete `docs/`, `CHANGELOG.md`, `ROADMAP.md`, `README*`, `.planning/`, `test_md/`, `ai-context.md`, `*handover*.md`;
   - remove comments and tests that name the bug: grep `-i` for `issue|#1[0-9][0-9]|Task 10[0-9]|I-[0-9]|CRITICAL|regression|panic|hotfix|v0\.2\.[89]`.
   
   Strip the same lines from both copies, so the only difference is the hunk.
4. **Isolate the ledger:**
   - point the reviewer's `DEV_INSTINCTS_HOME` at a copy of dev-instincts without `FE-*` lines and without this report (the smells would give the answers);
   - give it fresh agent memory for the project.
5. **Run in named-files mode** (the agent's "a named feature or files also works") with a neutral brief:
   > "Review the <feature> implementation in these files before release. Report-only."
   
   Don't use diff mode for the main score: a one-hunk diff points straight at the bug. Run diff mode separately as an upper bound.
6. **No build is expected:** Ferrite's crates aren't cached. The reviewer may write isolated probes, as in this report. Count `reading` evidence.

### Cases

| # | Escaped bug | Reconstruction (one hunk) | Files to give | Feature named in the brief |
|---|---|---|---|---|
| R1 | FE-094 crash detection never worked (the v0.2.0 AI review passed it) | In `src/app/mod.rs` move `create_lock_file();` (262) above `let recovery_result = load_session_state();` (257); delete comments 253-255 and 260-261. | `src/app/mod.rs` (FerriteApp::new), `src/config/session.rs` | session persistence and crash recovery start-up |
| R2 | FE-117 paste of mixed-script text aborts | `src/app/input_handling.rs`: replace line 160 with `if colon_pos + 3 <= s.len() && &s[colon_pos..colon_pos + 3] == "://" {`; delete the comment at 155-159 and the test module (645-706). | `input_handling.rs`, `Cargo.toml` | smart paste |
| R3 | FE-125 frontmatter panel shows or splices another file | `src/ui/frontmatter_panel.rs`: key the cache on `content_version` alone (line 264 and the `cached_key` field type); delete the doc comment at 225-230 and the cache-key tests in the test module (from 611). | `frontmatter_panel.rs`, its call site in `src/app/central_panel.rs`, `Tab::content_version` in `src/state.rs` | frontmatter panel |
| R4 | FE-130 second crash/restore cycle loses all edits | `src/state.rs:4959-4990`: build the `RecoveredWithDiskDivergence` tab as `Tab::with_file(self.next_tab_id, path.clone(), content.clone())` like the `Recovered` arm; delete the CRITICAL comment and the tests at `state.rs:6243` and `:6322`. | `src/state.rs` (with_file, is_modified, disk_content_hash, capture_session_state, restore_from_session_result, try_apply_recovery), `src/config/session.rs` | crash recovery restore |
| R5 | FE-113 no dirty marker or save prompt | Variant A: delete `widget.rs:470` (prepare) and `:833` (record). Variant B: **no change**; the class is live in `record_edit` paths (L-02). | `src/state.rs:1940-2680`, `src/editor/widget.rs`, `src/app/line_ops.rs`, `src/app/input_handling.rs` | unsaved-changes tracking |

### What counts

- **Catch (2 points), all three of:**
  1. the right function, within about 15 lines;
  2. the mechanism:
     - R1: the check sees the lock it just made;
     - R2: the slice can split a multi-byte character;
     - R3: the key is a per-tab counter, shared across tabs;
     - R4: `original_content` is set to the recovered text, so the next snapshot's disk hash is wrong;
     - R5: the version isn't bumped, so `is_modified()` stays cached;
  3. the user consequence:
     - R1: false recovery prompt, and real crashes undetected;
     - R2: the app aborts on paste;
     - R3: wrong fields, and a wrong body spliced in;
     - R4: edits lost on the second crash;
     - R5: no `*`, no prompt, edits lost on close.
  
  Severity must be within one level of the real one.
- **Partial (1 point):** location plus mechanism without the consequence, or the consequence through a different but valid mechanism.
- **Miss (0):** anything else.

**Also record:**
- **Rank:** where the catch appears in the reviewer's report (top three or not).
- **Precision:** any finding about the same lines in `control-RN` is noise.
- **Class extension, the most important number:**
  - did R2 also find L-01 (line ops);
  - did R4 also find L-03 (the `Recovered` branch);
  - did R5 find L-02.
  
  That measures #27 ("fix the class"), which is where Ferrite failed.

**Recall** = points ÷ 10.
- Run once now as a baseline.
- Run again after any of §2.4's candidates are accepted, to see whether they move recall.
- Keep the five replay folders as a fixed yardstick (#30), so later reviewer versions are scored on the same cases.

### Why these five
- Each fix is one hunk, so reconstruction is exact.
- Four were data-loss and one an abort.
- They span the top cost classes (K6, K4, K1, K7).
- R1 is the only case on record of an AI reviewer passing the exact code that later escaped.

**Optional sixth:** FE-104, table formatting stripped on save. Swap `serialize_inline_content` for `text_content()` in `serialize_table` (`src/markdown/widgets.rs`).

---

## Notes for importing into the ledger

These are not applied; `dev-instincts` was not touched.

1. **`origin: "escaped"` distorts the reviewer's own record.**
   - `ledger/README.md` defines escaped as "the reviewer's own miss", and `tools/stats.py` counts it under "Escaped a review".
   - Appending these 154 rows would move that figure from 3 to 157 and blame the instinct reviewer for Ferrite.
   - Either filter by project in that table, or import with `origin: "pre-existing"` plus a tag such as `escaped-to-users`.
2. **`caught_by: "maintainer"` is not in the schema's list.** Add it, or map it to `domain-testing`.
3. **The project code `FE`** needs a row in `ledger/README.md`.
4. **Areas used:** `front` and `ui` only; platform is a tag.
5. **Extra fields:** `found_in`, `fixed_in`, `cause`, `evidence_basis` and `class`. `stats.py` ignores unknown fields.
6. **Instinct numbers are valid.** All were checked against `DEV-INSTINCTS.md` by the generator, so `stats.py` will not refuse.
7. **Regression weighting:** regressions are marked with a `regression` tag because `origin` must be `escaped`. `stats.py` doubles only `origin: "regression"`, so on import those six rows score single, while §2.1 here doubles them.
8. **Dry run:** I appended the rows to a scratch copy of the ledger and ran `stats.py`. It accepted all 377 rows, and "Escaped a review" read 157.
9. **Check order:** importing will move #28, #5 and #9 up. That's the intended calibration effect, but the weight is now 154 Ferrite rows against 223 PrivateApp rows. Consider whether one project should dominate.
