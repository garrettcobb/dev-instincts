# Verdicts

| Claim | Verdict | Group | Severity | Evidence |
|---|---|---|---|---|
| VM | confirmed | 1 | wrong-result | runs 1 and 2 agree |
| HG | confirmed | 2 | wrong-result | runs 1 and 2 agree |
| MV | confirmed | 3 | wrong-result | runs 1 and 2 agree |
| ZX | confirmed | 4 | wrong-result | runs 1 and 2 agree |
| CT | confirmed | 5 | wrong-result | run 3; run 1 confirmed, wrong-result; run 2 confirmed, data-loss |
| MG | confirmed | 6 | wrong-result | run 3; run 1 confirmed, cosmetic; run 2 confirmed, wrong-result |
| GN | confirmed | 7 | crash | runs 1 and 2 agree |
| VF | confirmed | 8 | wrong-result | run 3; run 1 confirmed, wrong-result; run 2 confirmed, data-loss |
| VP | confirmed | 7 | crash | runs 1 and 2 agree |
| ZD | confirmed | 9 | data-loss | runs 1 and 2 agree |
| ML | confirmed | 1 | wrong-result | runs 1 and 2 agree |
| TG | confirmed | 10 | data-loss | runs 1 and 2 agree |
| PN | confirmed | 11 | stuck | runs 1 and 2 agree |
| MN | confirmed | 12 | data-loss | runs 1 and 2 agree |
| GM | confirmed | 11 | stuck | runs 1 and 2 agree |
| XX | confirmed | 10 | data-loss | runs 1 and 2 agree |
| KR | confirmed | 8 | data-loss | runs 1 and 2 agree |
| SQ | confirmed | 13 | security | redacted: security finding held for Garrett (FILING §4) |
| LH | confirmed | 10 | data-loss | runs 1 and 2 agree |
| LP | confirmed | 11 | stuck | runs 1 and 2 agree |
| DR | confirmed | 14 | wrong-result | runs 1 and 2 agree |
| FP | confirmed | 15 | wrong-result | runs 1 and 2 agree |
| JH | confirmed | 10 | data-loss | runs 1 and 2 agree |
| VL | confirmed | 16 | process | runs 1 and 2 agree |
| XT | confirmed | 1 | wrong-result | runs 1 and 2 agree |
| GC | confirmed | 17 | crash | runs 1 and 2 agree |
| GG | confirmed | 18 | data-loss | runs 1 and 2 agree |
| JN | confirmed | 19 | wrong-result | run 3; run 1 confirmed, cosmetic; run 2 confirmed, wrong-result |
| TX | confirmed | 12 | data-loss | runs 1 and 2 agree |
| WF | confirmed | 20 | wrong-result | runs 1 and 2 agree |
| SL | confirmed | 21 | data-loss | runs 1 and 2 agree |
| CG | refuted | 22 | - | run 3; run 1 confirmed, wrong-result; run 2 refuted |
| JK | confirmed | 7 | crash | runs 1 and 2 agree |
| LM | confirmed | 15 | wrong-result | runs 1 and 2 agree |
| QR | confirmed | 19 | wrong-result | run 3; run 1 confirmed, cosmetic; run 2 confirmed, wrong-result |
| WV | confirmed | 14 | wrong-result | runs 1 and 2 agree |
| PC | confirmed | 23 | wrong-result | runs 1 and 2 agree |

# Notes

Final verdicts by tools/control.py final (testing/CONTROL.md section 12.2), from judge-1.private.md (sha256 6c2a957cef381ea7c9315da3292a37840cf203d5de71b48b54b31d946a199c43), judge-2.private.md (sha256 52ca03caab9b6ddbbe605e473d0e25aa924c31d0b592fc9cecca02a568720f33) and judge-3.md (sha256 baf558a28104da6c7be81a3638af028e9eed55ebee2ae850ce66c16d141c1805). Agreement 0.84: 31 of 37 claims agree. Disputed, so run 3's: CT, MG, VF, JN, CG, QR. Two claims are one group if any run put them in one.
