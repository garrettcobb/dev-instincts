# Senior coder checklist

One line per miss: the question that would have found it, with its finding id. Read this before every design note.

- What other tables point at the rows this rule touches (submittal items, links, foreign keys), and what happens to each when the rule runs? (PA-IR-037, missed in calibration)
- What does `on_delete=CASCADE` take with it when this rule deletes or replaces a row, and does the version being restored still want those rows? (PA-IR-038, missed in calibration)
- Does a value someone removed stay removed, or can a merge or restore bring it back? (PA-IR-040, missed in calibration)
- Does the claim hold for every row, not just the kind I looked at? Read the field list the update actually writes. (PA-IR-030, partly: said contract lines only)
- Does the rule hold for old data, a record whose parent is already in the Recycle Bin or was restored without a check? (PA-IR-089, missed: reviews/PrivateApp/2026-11-01-844e811-bin-contract-lock-design.md)
- When the fix adds a lock to a shared function, which callers already hold locks when they call it (a loop over batches in one transaction, a put-back UPDATE), and in what order will they now take them? (PA-IR-093, partly: design check 2 named the multi-record mechanism, not purge)
- For an Undo invariant, which paths redo the action with a new id (Undo of a Restore, Redo), not only two of the same action at once? (PA-IR-091, partly: I4 listed the double Delete only)
- When the rule adds a new refusal inside a shared helper, does every door that calls the helper (each page view, not only the Explorer's /api/op/) turn it into words, or does one call it bare? (PA-IR-101, missed: the pages' Deletes were listed, not their error handling)
- For each row the path writes, is it found the same way the lock step finds it? A row reached through a stored id (deleted_info) rather than the live foreign key isn't in a lock set built from the key. (PA-IR-102, partly: _unbin's takeoff FOR UPDATE was in the data map, not outside the order)
- When a count changes to 'what it did', which items does an earlier step of the same request remove by cascade, so the loop skips them as gone? (PA-IR-104, partly: the 'gone already' skip and the count question were both named, not their meeting)
- When the rule checks one kind on its locked row, which other kinds in the same loop have the same hazard (binned twice, the first Ctrl+Z lost)? (PA-IR-105, missed: L10b found for takeoffs, not for their documents)
- List every door by searching the code (pages, Explorer, Undo and Redo, API), not from memory. (PA-IR-101, 102, 103: doors no note listed)
