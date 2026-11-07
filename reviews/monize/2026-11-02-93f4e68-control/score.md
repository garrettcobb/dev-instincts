| Measure | A1 | A2 | B1 | B2 |
|---|---|---|---|---|
| Findings | 7 | 5 | 12 | 13 |
| Proven (a probe ran) | 1 of 7 | 3 of 5 | 3 of 12 | 3 of 13 |
| Confirmed (distinct bugs) | 7 | 5 | 12 | 12 |
| Refuted | 0 | 0 | 0 | 1 |
| Can't tell | 0 | 0 | 0 | 0 |
| Unique to the arm | 2 | 2 | 7 | 8 |
| Overlap (confirmed by both) | 6 | 6 | 6 | 6 |
| Severity-weighted confirmed | 20 | 16 | 40 | 38 |
| Accepted upstream | 0 | 0 | 3 | 3 |
| Rejected upstream (descriptive, not pre-registered) | 2 | 1 | 1 | 1 |
| Minutes | 17.8 | 16.4 | 16.7 | 26.4 |
| Confirmed per hour | 23.6 | 18.3 | 43.1 | 27.3 |
| Refuted per finding | 0.00 | 0.00 | 0.00 | 0.08 |

Re-scored 2026-11-05 (`testing/CONTROL.md` §12, *Accepted upstream*), after that day's re-check of the filed issues (`metrics/FILED.md`, 3d8ee65): the Accepted upstream row alone, from the four acknowledged groups, 8 (#2025), 9 (#2026), 12 (#2028) and 21 (#2030), a run counting each in which it has a confirmed claim: A1 and A2 none, B1 groups 8, 9 and 12, B2 groups 8, 12 and 21. Worked by hand from the groups below; `tools/control.py score` with the same minutes and `--accepted KR --accepted ZD --accepted MN --accepted SL`, run into a scratch file, printed this file as it stands without this note.

Re-scored 2026-11-06 (`testing/CONTROL.md` §12, *Accepted upstream* and *Maintainers have the last word*), after that day's re-check of the filed issues (`metrics/FILED.md`): the four groups' issues, 8 (#2025), 9 (#2026), 12 (#2028) and 21 (#2030), are now `fixed`, their pull requests merged, and §12 counts `acknowledged` and `fixed` alike, so the Accepted upstream row stands: A1 and A2 none, B1 groups 8, 9 and 12, B2 groups 8, 12 and 21. The issues of groups 10 (#2027) and 18 (#2029) were `rejected`, closed as not planned with reasons that dispute neither bug, so no verdict changes (no `--not-a-bug`) and neither counts as accepted. The Rejected upstream row beneath it is descriptive and not pre-registered, a measure §12 doesn't define: per run, its confirmed groups whose filed issue was rejected, A1 groups 10 (JH) and 18 (GG), A2 group 10 (XX), B1 group 10 (LH), B2 group 10 (TG). Worked by hand from the groups below; `tools/control.py score` with the same minutes and `--accepted KR --accepted ZD --accepted MN --accepted SL`, run into a scratch file, printed this file as it stands without its two notes and the Rejected upstream row, which it doesn't compute; with `--accepted JH --accepted GG` instead, used only to count each run's confirmed groups among 10 and 18, its Accepted upstream row read 2, 1, 1 and 1.

Headline measures, each run on its own (section 12.1):
| Headline measure | Within A | Within B | Floor | A | B | Gap A - B | Reading |
|---|---|---|---|---|---|---|---|
| Confirmed per hour | 5.3 | 15.8 | 15.8 | 20.9 | 35.2 | -14.2 | no difference |
| Refuted per finding | 0.00 | 0.08 | 0.08 | 0.00 | 0.04 | -0.04 | no difference |

Groups (the judge's numbers):
- 1: VM (B2 8: confirmed, wrong-result); ML (A1 3: confirmed, wrong-result); XT (B1 8: confirmed, wrong-result)
- 2: HG (A2 2: confirmed, wrong-result)
- 3: MV (A2 1: confirmed, wrong-result)
- 4: ZX (B2 9: confirmed, wrong-result)
- 5: CT (B2 3: confirmed, wrong-result)
- 6: MG (B2 11: confirmed, wrong-result)
- 7: GN (A1 4: confirmed, crash); VP (B2 7: confirmed, crash); JK (A2 4: confirmed, crash)
- 8: VF (B2 6: confirmed, wrong-result); KR (B1 4: confirmed, data-loss)
- 9: ZD (B1 3: confirmed, data-loss)
- 10: TG (B2 4: confirmed, data-loss); XX (A2 3: confirmed, data-loss); LH (B1 2: confirmed, data-loss); JH (A1 1: confirmed, data-loss)
- 11: PN (A1 5: confirmed, stuck); GM (B1 11: confirmed, stuck); LP (B2 12: confirmed, stuck)
- 12: MN (B1 1: confirmed, data-loss); TX (B2 1: confirmed, data-loss)
- 13: SQ (B1 6: confirmed, security)
- 14: DR (B1 5: confirmed, wrong-result); WV (B2 5: confirmed, wrong-result)
- 15: FP (A1 2: confirmed, wrong-result); LM (B1 10: confirmed, wrong-result)
- 16: VL (A1 7: confirmed, process)
- 17: GC (B2 13: confirmed, crash)
- 18: GG (A1 6: confirmed, data-loss)
- 19: JN (A2 5: confirmed, wrong-result); QR (B1 9: confirmed, wrong-result)
- 20: WF (B1 7: confirmed, wrong-result)
- 21: SL (B2 2: confirmed, data-loss)
- 22: CG (B2 10: refuted)
- 23: PC (B1 12: confirmed, wrong-result)
