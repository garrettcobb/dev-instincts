# Human reference knowledge

What people who study or practise software development say about AI-written code, and what a human reviewer catches that an AI misses. The instinct reviewer loads `HUMAN-REFERENCE.md` before every review; the notes in `sources/` are for checking a claim back to where it came from.

- **`HUMAN-REFERENCE.md`:** the synthesis. What the measured studies show, where sources disagree, advice for a developer who directs AI and doesn't read code, and the reviewer's proportion-and-hygiene pass.
- **`sources/`:** one note per source: citation, type, evidence strength, the claims, the checks it suggests, and caveats.

Collected 2026-10-30. Notes written 2026-10-31 from OCR of the PDFs (pdftoppm + tesseract) and text from the saved HTML. Where OCR lost text, the note says so.

## How much to trust it

| Strength | Count | What it means |
|---|---|---|
| Strong | 1 | Large, well-designed measurement, even if reported secondhand |
| Moderate | 6 | Real measurements, mostly preprints, each with stated limits |
| Weak | 9 | A vendor report, an untested framework, a synthesis with no new data, or an argument whose numbers have no source |
| Anecdotal | 18 | One person's experience or opinion |
| Off-topic | 1 | Nothing usable |

**Rule for the reviewer:** a check backed only by weak or anecdotal sources is a hypothesis. Run it, but its findings go to `proposals/` until the ledger shows the class is real. Our own ledger outranks any opinion piece.

## Index

### Strong
| Note | Source | Type |
|---|---|---|
| `agents-more-code-not-more-software.md` | Chen & Stratton (Harvard), via Ars Technica, Oct 2026: 700+ firms, before vs after agent adoption | Working paper reported in the news |

### Moderate
| Note | Source | Type |
|---|---|---|
| `ai-code-in-real-world-repos.md` | Mao et al., arXiv 2603.27130 (Apr 2026): 19,816 AI files vs same-repo human files | Preprint |
| `code-for-machines-codehealth.md` | Borg, Tornhill et al. (CodeScene, Lund), arXiv 2601.02200 (Jan 2026): 5,000 files, code health vs AI refactor breakage | Preprint; CodeScene sells code-health tooling |
| `human-vs-ai-code-defects.md` | Cotroneo et al. (Naples), arXiv 2508.21634 (Aug 2025): 507k functions, defects and vulnerabilities | Preprint |
| `humans-missing-from-coding-agent-research.md` | Wang, Yang, Neubig, Fried et al. (CMU, Stanford, Princeton…): bloat and behavior of passing agent patches | Position paper with measurements |
| `longitudinal-ai-coding-assistants.md` | Vella & Blincoe (Auckland), arXiv 2605.23135 (May 2026): 95 engineers over six months | Preprint |
| `risks-of-ai-overreliance-in-se.md` | TechTarget, Kompella (Oct 2026): a summary of named studies and DORA data | Analyst article, all secondhand |

### Weak
| Note | Source | Type |
|---|---|---|
| `ai-cant-feel-bad-code.md` | Jhavtech Studios, Steemit (2026) | Agency marketing; uncited statistics |
| `ai-undermining-problem-solving.md` | Nazir & Arif, ICCK J. Softw. Eng. (2026) | Peer-reviewed narrative review; untested framework, students |
| `ai-will-accelerate-overengineering.md` | Anton Minin Baranovskii, antonmb.com (Aug 2026) | Essay; no data |
| `code-production-to-orchestration.md` | Stieber, ResearchGate (Mar 2026) | Survey preprint; only the abstract and start of the introduction were in the copy |
| `coderabbit-ai-vs-human-code-report.md` | CodeRabbit (2026): 470 PRs | Vendor report; CodeRabbit sells AI review |
| `human-ai-collaboration-se-work.md` | Alenezi, arXiv 2606.03394 (Jun 2026) | Single-author synthesis, no new data |
| `ponytail-minimalist-plugin.md` | "AI Engineering", Medium (Jun 2026), on the Ponytail plugin | Promotional; benchmark run by the plugin's own team |
| `stop-over-engineering-ai-apps-boring-tech.md` | Tiger Data (Timescale) blog (Feb 2025) | Vendor blog |
| `what-ai-cant-do-yet-in-software-dev.md` | UC Berkeley Extension "Voices" (Apr 2026) | Essay; ends in a course promotion |

### Anecdotal
| Note | Source |
|---|---|
| `ai-agents-overengineered.md` | Jaideep Parashar, DEV Community |
| `ai-coding-vs-human-coding-detailed-analysis.md` | Faisal Mahmood, Medium (Sep 2025) |
| `ai-doing-the-wrong-thing-well.md` | Jochen Lillich, The Monospace Mentor (Aug 2026) |
| `ai-has-no-wisdom.md` | Alexandru Nedelcu, alexn.org (Sep 2026) |
| `ai-is-not-your-peer.md` | notyourpeer.com manifesto |
| `ai-loves-to-over-engineer.md` | Tyson Cung, DEV Community |
| `ai-made-knowing-how-to-code-more-important.md` | Brandon A. Olivares, Medium (Apr 2026) |
| `code-smell-273-overengineering.md` | Maximiliano Contieri, Medium (Oct 2024) |
| `future-of-code-more-human.md` | Leena Malhotra, DEV Community (Oct 2025) |
| `human-factor-of-ai-and-coding-csa.md` | Eyal Estrin, Cloud Security Alliance blog (Aug 2026). Covers both copies in the collection (PDF and .mhtml) |
| `human-vs-ai-code-human-still-wins.md` | Or Ben Shmueli, Medium |
| `karpathy-rules-ai-overengineering.md` | Evan-dong, DEV Community |
| `overengineering-trap-ai-automation.md` | Himanshu Sharma, Optimize Smart; practical section paywalled |
| `simple-query-over-ai.md` | Alan West, DEV Community |
| `stop-ai-over-engineering-simple-problems.md` | Arslan Ahmad, Substack (May 2026) |
| `stop-claude-code-overengineering-everything.md` | Nathan Onn, nathanonn.com (Jul 2025) |
| `stop-overengineering-clean-code-that-ships.md` | TheBitForge, DEV Community; about human over-engineering, not AI |
| `when-ai-turns-over-engineering-into-a-feature.md` | Clear Data Labs, DEV Community (May 2026) |

### Off-topic
| Note | Source |
|---|---|
| `algorithmic-instinct.md` | Seotan et al., ResearchGate (Apr 2025). About intuition in decision-making in general, not code; only an abstract, plus a leftover chatbot reply in the text |

## Adding a source
1. Put the original in the folder on the developer's PC.
2. Write a note in `sources/` in the same shape: Source, Type, Evidence strength, Claims, Checks (each mapped to an instinct number or `NEW: <name>`), Caveats.
3. Add it to the index above under its strength.
4. If it's measured, or it changes a conclusion, update `HUMAN-REFERENCE.md`. A new check with no instinct goes to `proposals/`.
