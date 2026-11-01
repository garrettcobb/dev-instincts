# Proposed instinct: A check must fail on the old output

Proposed by the instinct reviewer, PrivateApp 2026-10-31-0284e02-learn, from PA-IR-024 (found by the developer) and PA-IR-025. Not yet approved; if approved it takes the next free number at the end of DEV-INSTINCTS.md. Tag: `proposed:check-fails-on-the-old-output`.

It could instead be approved as an amendment to #39 (prove the test catches the bug). #39 is about tests in the suite, proved by turning the fix off. This draft is about the check that runs right after a write in a script, a deploy or a backup, proved by making the write do nothing. It is a cousin of #35 (offline proven by cutting the network, not by grep), #62 (the checks build a fresh world, the app runs in an old one) and Ferrite draft F12 (`proposed:release-build-guards`). All of them are checks that prove a property close to the one that matters.

- **Instinct:** a check after a write has to test what the write was for: that the new content is there. If the check would also pass on yesterday's output, it proves nothing about today's write.
- **Missed:**
  - PA-IR-024: the backup mirror rewrote the git history bundle and then ran `git bundle verify`. That proves the file is a well-formed bundle whose prerequisites exist. It's just as true of the old bundle.
    - The target sometimes holds the file. When it did, git refused ("cannot create ...: Permission denied", exit 128), and the command line sent that to /dev/null.
    - Seconds later `git bundle verify` passed on the stale bundle ("The bundle records a complete history"). The mirror was reported as done, with "the history bundle verifies".
    - The "mirror check" (`diff -rq`) excluded the bundle by name, so it couldn't see it either.
  - PA-IR-025: the fix compares the bundle's HEAD with the commit just made. Its file check, though, only walks the files still tracked, so it still passes when the step that removes deleted files silently did nothing.
- **Ask:**
  - If this write had silently done nothing, would the check still pass?
  - What is the identity of the thing just made (commit, version, hash, row count, timestamp), and does the check compare the output against that?
  - Does the check look both ways: everything that should be there, and nothing that shouldn't?
- **Prove it:**
  - Make the write a no-op (a wrapper that exits 0, a held file, a step skipped) and confirm the check goes red. Do the same for every step the check is meant to cover, deletes included.
  - The check compares the output's identity with the input's: the bundle's heads with `git rev-parse HEAD`, the installed version with the built one, the file hash with the source's.
  - Never send a write's errors or exit status to /dev/null. Chain the steps with `&&` or `set -e`, and print the tool's own reason on failure.
- **Smell:**
  - `write ... >/dev/null 2>&1; check ...` joined with `;`;
  - a validity-only check: bundle verify, `zip -T`, "parses as JSON", HTTP 200, "file exists", "exit 0";
  - a comparison that excludes the artifact by name;
  - a postcondition loop over the source list only;
  - an operational step retyped by hand each time instead of run as one script.
- **Checklist:** "Every check after a write fails when the write silently does nothing, and compares what was written with what was meant?"
