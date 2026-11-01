# Proposed instinct: A test that fails sometimes is failing

**Approved as #63 on 2026-10-31.**

Proposed by the instinct reviewer, PrivateApp 2026-10-31-review, from PA-IR-006. Not yet approved; if approved it takes the next free number at the end of DEV-INSTINCTS.md. Tag: `proposed:flaky-test`.

- **Instinct:** a test that passes on one run and fails on the next is a failing test. Green means green every run, in any order, alone or with the rest.
- **Missed:** PrivateApp's Explorer test "titles a name clash Replace or Skip Files" failed 1 run in 3 when run alone, before and after the 1.2.0 fixes, and once in a 13-file run. The step's "every check passes" rested on a gate that could go either way, so a re-run could hide a real failure, or a real fix could look broken.
- **Ask:** if I run this test alone, three times, and in a different order, does it give the same answer every time? Does it wait for the exact thing it checks, or only for "a dialog" while two dialogs come and go?
- **Prove it:** run each new or changed test file three times alone and once shuffled (`vitest --sequence.shuffle`, `pytest -p random_order` only if the project already has it). Any mixed result is a finding. Wait on the specific element (`findByRole("button", { name })`), never on a container that another element can satisfy first.

Checklist line (draft): *Each new or changed test gives the same result alone, three times, and in shuffled order?*
