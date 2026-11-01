# Proposed instincts from the Ferrite case study (F1–F14)

Drafted while mining Ferrite's escaped bugs (`case-study-ferrite/report.md` §2.4). Nine were approved on 2026-10-31; their headings give their numbers. The rest are still drafts. These drafts were first numbered 46–59; those provisional numbers were replaced by the labels F1–F14 so they can't be confused with real instinct numbers. If approved, each takes the next free number at the end of `DEV-INSTINCTS.md`, along with the earlier proposal `2026-10-31-a-test-that-fails-sometimes-is-failing.md`.

84 of Ferrite's 154 bugs fit none of the 45 instincts. These drafts cover most of that gap, mainly the classes that matter in a desktop editor and not in a web app: text encodings, fonts, widget identity, window chrome, key ownership, platform differences, idle cost, themes, release-build guards, and handover drift.


These are drafts in our format. The numbers are suggestions; only the developer assigns permanent numbers.

#### F1. Bytes are not characters (approved as #49, 2026-10-31)
- **Tag:** `proposed:bytes-are-not-characters`
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

#### F2. Every glyph needs a font that has it (approved as #60, 2026-10-31)
- **Tag:** `proposed:every-glyph-has-a-font`
- **Instinct:** a character you draw is only visible if a loaded font contains it, on the user's machine and in the user's language.
- **Missed:**
  - FE-011, FE-013, FE-048, FE-049 (fixed twice), FE-061;
  - FE-084, FE-085 (UI language switch);
  - FE-072, FE-106 (font loading crashes);
  - FE-131 (double icons).
- **Ask:** which font draws this, if the user has none of my fonts and the UI is in Japanese?
- **Prove it:** a coverage test over every UI string, icon literal and locale file against the shipped fonts. Launch with each UI language and an empty system font directory, then screenshot.
- **Checklist:** "Every UI string and icon renders in every UI language with only the bundled fonts?"

#### F3. A cache key must tell its contents apart (approved as #50, 2026-10-31)
- **Tag:** `proposed:cache-key-identifies-content`
- **Instinct:** a cache, version counter or "same length means same" shortcut is only safe if no real change can leave the key equal. That is especially true when the cached value gets written back.
- **Missed:**
  - FE-113 (`is_modified` keyed on a counter that writers forget to bump);
  - FE-125 (per-tab counter used across tabs);
  - FE-100 (match offsets kept across edits);
  - live: L-06 (sampled hash), L-07 (same length assumed unchanged), L-02.
- **Ask:** what change leaves this key the same, such as the same length, a mid-file edit, another tab at version 0, or a writer that skips the bump? What gets written back from the stale value?
- **Prove it:** for each cache, mutate the content while holding the key's inputs constant. Assert a miss, and assert no write-back of stale data. Related to #42, but for runtime caches.
- **Checklist:** "Every cache misses on a same-length mid-file change and on another document at the same version?"

#### F4. Widget identity never depends on what it edits (approved as #61, 2026-10-31)
- **Tag:** `proposed:stable-widget-identity`
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

#### F5. Durable data carries durable identity (approved as #56, 2026-10-31)
- **Tag:** `proposed:durable-identity`
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

#### F6. One point, one owner (approved as #59, 2026-10-31)
- **Tag:** `proposed:one-point-one-owner`
- **Instinct:** every pixel of the window chrome has exactly one owner for press, drag and release, and paint order matches that owner.
- **Missed:**
  - FE-020, FE-037, FE-042, FE-055 (Linux title bar);
  - FE-036, FE-142 (button inside a resize zone);
  - FE-132, FE-140, FE-099, FE-066, FE-050.
- **Ask:** for this control, what else is under the pointer, and which one wins on release?
- **Prove it:** scripted presses and drags at every edge, corner and title-bar control, at 100/125/150% scaling, on Windows, X11 and Wayland.
- **Checklist:** "Every edge, corner and title-bar control does one thing at 100/125/150%, on each OS?"

#### F7. Every key has exactly one owner (approved as #55, 2026-10-31)
- **Tag:** `proposed:one-key-one-owner`
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

#### F8. Text round-trips byte for byte (approved as #53, 2026-10-31)
- **Tag:** `proposed:text-round-trips`
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

#### F9. Their machine is not your machine (approved as #47, 2026-10-31)
- **Tag:** `proposed:their-machine`
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

#### F10. Idle is a state
- **Tag:** `proposed:idle-is-a-state`
- **Instinct:** in an immediate-mode UI, every line in the frame loop runs 60 times a second. At rest the app should do nothing, and no per-frame path may touch the whole document.
- **Missed:**
  - FE-033 (10% idle CPU);
  - FE-029 (log spam, hover repaint);
  - FE-056 (1.8 GB: clone per frame);
  - FE-086, FE-108.
- **Ask:** what does this cost per frame when nothing changes?
- **Prove it:** idle CPU and allocations per idle frame measured with a large document open, with a ceiling enforced in CI. Complements #13 (size) with frequency.
- **Checklist:** "Idle CPU under 1% and zero O(N) work per frame with a 100 MB file open?"

#### F11. Every theme is a test target
- **Tag:** `proposed:every-theme`
- **Instinct:** light mode is a second product, and every text and background pair is checked in each theme.
- **Missed:** FE-004, FE-007, FE-082 (white on white), FE-115 (invisible selection).
- **Ask:** did I look at this in light and dark, including pressed, selected and disabled states?
- **Prove it:** screenshot tests per theme, plus a contrast check over the theme's token pairs.
- **Checklist:** "Every state readable in light and dark?"

#### F12. The safety net must fire in the shipped build
- **Tag:** `proposed:release-build-guards`
This could be an amendment to #39.
- **Instinct:** a guard is only real if it works under release settings (`panic = "abort"`, LTO, no debug assertions).
- **Missed:** L-14. `catch_unwind` cited for FE-031 and FE-106 cannot catch anything in release, while tests run with unwinding and pass.
- **Ask:** does this guard depend on a build setting that differs between test and release?
- **Prove it:** run guard tests with the release profile, or against the shipped binary.
- **Checklist:** "Each crash guard seen working in a release build?"

#### F13. The handover is code
- **Tag:** `proposed:handover-is-code`
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

#### F14. A test plan nobody ran is not a gate
- **Tag:** `proposed:plan-nobody-ran`
Process; related to #26 and #30.
- **Instinct:** a release is gated on an executed plan with a signed row (tester, build SHA, results), not on the plan existing.
- **Missed (Ferrite):**
  - the v0.2.8 suite had 0 of 237 boxes checked, yet it names "Modified indicator (*) updates correctly" and "Ctrl+Z / Ctrl+Y — undo/redo", the two data-loss regressions that 0.2.9 hotfixed;
  - every "Issues Found" table is empty.
- **Ask:** who ran this, on which build, and where did failures go?
- **Prove it:** the tag script refuses unless the plan has a sign-off row with a SHA and every P0 line is marked.
- **Checklist:** "Release plan executed, signed with a build SHA, failures logged?"

**Smaller candidates (one bug each, so not drafted):**
- Never mutate what you're drawing (FE-107, palette crash mid-render). Tag `proposed:no-mutation-mid-frame`.
- Plural by default (FE-134, multi-cursor cut kept one selection). Tag `proposed:plural-by-default`.

---

## Evidence added by mining Django (2026-10-31-a05e16a-mine)

Reference data (Django is human-written), all `reading`. Report: `reviews/Django/2026-10-31-a05e16a-mine.md`.
- **54 `proposed:their-machine`** (10 rows). The same class shows up on the back end, with "database" and "Windows" standing in for "OS row":
  - SQLite parameter limits hit only past about 500 rows (DJ-003, DJ-026);
  - Windows-only Unicode-normalisation denial of service (DJ-111, DJ-121, DJ-128);
  - injection or wrong results on one database only (DJ-053, DJ-119, DJ-123, DJ-132);
  - a feature built on a database pre-release that the vendor then withdrew (DJ-086).
- **48 `proposed:cache-key-identifies-content`** (5 rows):
  - the shared response cache keyed per URL while the response depended on Cookie or Authorization (DJ-095, DJ-101);
  - two Vary headers with the same value produced one key (DJ-014);
  - `name + salt` signer namespaces collided (DJ-098);
  - a cached metadata property missing from the expiry list (DJ-004).
- **46 `proposed:bytes-are-not-characters`** (2 rows): `sys.getsizeof()` used as a buffer length (DJ-096); `force_str` on non-UTF-8 bytes passwords (DJ-057).
- **53 `proposed:text-round-trips`** (1 row): the wordwrap rewrite dropped blank lines (DJ-039).
