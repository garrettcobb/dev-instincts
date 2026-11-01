# Human-Written vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and Complexity
- **Source:** arXiv:2508.21634v1 [cs.SE], 29 Aug 2025. Domenico Cotroneo, Cristina Improta, Pietro Liguori (University of Naples Federico II). Replication: github.com/dessertlab/Human_vs_AI_Code_Quality; Zenodo 10.5281/zenodo.16853222. EU-funded (SERICS, PRIN 2022).
- **Type:** preprint
- **Evidence strength:** moderate — very large sample (507,044 functions: 285,249 Python, 221,795 Java; human code from 16,928 repos) with public replication data. But the AI code is generated from docstrings as isolated functions (not agent-built or integrated), the analysis is static only, and the models are older (gpt-3.5-turbo from April 2023; quantized DeepSeek-Coder 33B and Qwen2.5-Coder 32B). No vendor conflict.

## Claims
Method
- Human functions come from CodeSearchNet via the HMCorp dataset. Each docstring and signature was given to ChatGPT, DeepSeek-Coder (DSC) and Qwen-Coder.
- Defects: Pylint (350 rules after dropping style rules) and PMD (226 rules), hand-mapped by two authors (consensus) to Orthogonal Defect Classification types. Security: Semgrep, mapped to CWE. Complexity: lizard + tiktoken.

Defects
- Python defective samples: Human 55.47% (158,221); ChatGPT 38.75%; DSC 60.96%; Qwen 62.48%. Incorrect (unparseable or empty): Human 1.30%; ChatGPT 0.89%; DSC 7.29%; Qwen 2.52%. Total defects: Human 429,247; ChatGPT 185,110; DSC 319,643; Qwen 574,916.
- About 47% of human Python defects (202,259) are a single rule, protected-access. Without it, the human total (~227k) is comparable to ChatGPT's.
- Java defective: Human 34.29%; ChatGPT 35.28%; DSC 69.92% (plus 15.50% incorrect); Qwen 27.23% (1.73% incorrect). Totals: Human 202,129; ChatGPT 161,056; DSC 242,437; Qwen 123,180.
- Averaged over the three models vs. human: about −4k defective samples in Python, +22k in Java.
- Top AI defects in Python: unused-argument (ChatGPT 32,992; DSC 111,703; Qwen 213,264), unused-variable (ChatGPT 14,408), unspecified-encoding on file I/O (ChatGPT 14,312), too-few-public-methods, i.e. trivial or placeholder classes (DSC 64,279), redefined-outer-name (Qwen 57,252).
- Top AI defects in Java: ImmutableField (DSC 41,669), SystemPrintln (DSC 37,986; Qwen 13,329; ChatGPT 10,428), printStackTrace, UnusedPrivateField, UnusedFormalParameter (Qwen 24,660), UseVarargs (ChatGPT 9,124).
- Top human defects: Python no-else-return (22,619) and raise-missing-from (10,108); Java CyclomaticComplexity (15,435), AvoidInstantiatingObjectsInLoops (14,351), CognitiveComplexity (13,065), AvoidCatchingGenericException (9,749).
- 16 useless-with-lock cases in ChatGPT code (a lock that doesn't lock). Pylint is weak at concurrency defects.
- The authors' reading: AI copies parameters from the signature and then doesn't use them.

Security
- Python vulnerable samples: Human 15,835 (5.55%); ChatGPT 22,864; DSC 22,878 (each about 8%); Qwen 16,316 (5.72%). Issues per vulnerable sample: Human 1.62; ChatGPT and DSC 1.75; Qwen 2.10. Distinct CWEs are similar (43–45).
- Java vulnerable samples: Human 6,660 (3%); ChatGPT 18,144 (8.18%); DSC 43,386 (19.56%; 76,678 issues; 51 CWEs); Qwen 13,620 (6.14%).
- Averaged AI vs. human: +5k vulnerable samples in Python, +18k in Java. The introduction's "45k" for Python is an OCR error; the key-finding section reads +5k.
- Python: CWE-78 OS command injection ChatGPT 13,419 and DSC 10,908 vs. human 2,243. CWE-400 (resource consumption) and CWE-611 (XXE) are almost absent in human code but occur thousands of times in DSC/ChatGPT output. Human code skews to CWE-754, improper check for exceptional conditions (13,157). CWE-319 cleartext transmission appears only in DSC.
- Java: CWE-532 information exposure through log files, DSC 30,031 vs. human 3,736. DSC also leads on CWE-489 active debug code, CWE-798 hardcoded credentials, CWE-209 information exposure through error messages. Path traversal (CWE-22) appears for ChatGPT and DSC but not human code (heatmap). Other heatmap cells are partly OCR-garbled and not used.
- Human code was the most secure overall.

Complexity
- Python average NLOC: Human 12.72; ChatGPT 6.89; DSC 5.16; Qwen 4.47. CCN: 3.97 vs 2.47 / 2.00 / 1.84. Tokens: 142.45 vs 79.33 / 68.37 / 58.68.
- Java NLOC: 13.38 vs 8.42 / 6.70 / 6.14. CCN: 3.48 vs 2.35 / 1.83 / 1.90.
- AI function names are longer (Java: DSC 19.32, ChatGPT 18.92 vs. human 13.98 characters).
- AI has fewer unique tokens (Python: human 70,542 vs. about 60–63k; Java: 57,356 vs. about 47–53k).
- Averaged, AI code has −6.75 NLOC, −1.66 CCN, −63.74 tokens and −7,756 unique tokens.
- The authors suggest shorter, simpler code may under-specify behaviour and skip error and edge-case handling. This is stated as a risk, not measured.

## What humans catch that AI misses (per this source)
- Parameters accepted but never used.
- Debug prints and stack traces left in the code.
- Shell commands, XML parsers and log lines fed unsanitized input; credentials in code.
- Placeholder classes with nothing in them.
- Missing edge-case and error handling in short, clean-looking functions (the authors' hypothesis).

## Checks for the reviewer
- Unused parameters, fields and variables. Detect: pylint W0613/W0612; ruff ARG001–ARG005, F841; PMD UnusedFormalParameter/UnusedPrivateField; TS `noUnusedParameters`. For each hit, ask whether the caller expects it to matter: an ignored `user_id`, `project_id` or `since` is a scope or permission bug. → NEW: An unused input is an ignored requirement.
- Debug leftovers. Detect: `print(`, `pprint(`, `breakpoint()`, `pdb`, `console.log`, `debugger`, `System.out.println`, `printStackTrace`, `traceback.print_exc`, `DEBUG = True` outside dev settings. → NEW: No debug leftovers; logs and errors don't leak.
- Information exposure through logs and errors (CWE-532, CWE-209). Detect: log calls carrying passwords, tokens, request bodies or whole objects; error responses returning `str(e)`, `repr(e)` or tracebacks. → NEW: No debug leftovers; logs and errors don't leak (also #21, raw error pages).
- Hardcoded credentials and keys (CWE-798, CWE-321). Detect: secret regex scan of the diff and settings. → NEW: No secrets in code.
- OS command injection (CWE-78). Detect: `subprocess.*shell=True`, `os.system(`, `os.popen(`, `Runtime.exec(` with built-up strings. → #12 (user text becomes code; extend beyond exports), #9.
- SQL injection (CWE-89). Detect: f-strings, `%` or `+` building SQL passed to `execute(`, `.raw(`, `.extra(`, `RawSQL`. → #12 (extend), #9.
- XXE (CWE-611) and unsafe deserialization (CWE-502). Detect: `xml.etree`/`lxml`/`minidom` parsing uploaded files without defusedxml (xlsx and docx are XML); `pickle.loads`; `yaml.load(` without SafeLoader. → #9; NEW: Security-scan every AI change.
- Path traversal (CWE-22). Detect: file paths built from request data (`os.path.join(MEDIA_ROOT, name)`, `open(` on a user-supplied name) without normalizing and checking the result stays inside the folder. → #9, #15.
- Resource consumption (CWE-400). Detect: unbounded reads; no row or size limits on uploads. → #9, #13.
- Network calls without a timeout (pylint missing-timeout). Detect: `requests.(get|post|put|patch|delete|request)\(` without `timeout=`. → #18.
- File I/O without explicit encoding. Detect: `open(` without `encoding=`; `read_text()`/`write_text()` without encoding. On Windows the default codepage breaks non-ASCII text. → NEW: Don't lean on platform defaults.
- Locks that don't lock (useless-with-lock). Detect: `with threading.Lock():` or `with Lock():` creating a new lock inline. → #3.
- Trivial classes. Detect: pylint too-few-public-methods (R0903) on new classes. → NEW: Every abstraction earns its place.
- Weak randomness or crypto (CWE-330, CWE-327). Detect: `random.` used for tokens, passwords or ids instead of `secrets`; md5/sha1 used for passwords. → NEW: Security-scan every AI change.

## Over-engineering signals (if relevant)
- Placeholder or trivial classes (too-few-public-methods): structure with no purpose. Detect with pylint R0903.
- This study finds AI code shorter and simpler, not bloated. Its over-engineering signal is empty structure, not volume.

## Process lessons for a non-coder directing AI
- Check AI code for design quality and security, not only whether it runs.
- Results differ by model and language (Qwen was worst in Python and best in Java). Don't generalise from one model.

## Quotes
- "AI-generated code is generally simpler and more repetitive, yet more prone to unused constructs and hardcoded debugging"
- "AI-generated code also contains more high-risk security vulnerabilities"

## Caveats
- Isolated functions generated from docstrings, not agent-built features in a real codebase.
- Old or quantized models; current agents may behave differently.
- The human baseline is popular open-source code that may itself be in the models' training data.
- Static-analysis flags aren't confirmed bugs, and the ODC mapping is manual judgement.
- "Incorrect" includes empty outputs (DSC: 19,612 empty in Python), which skews some model totals.
- Contradicts Mao et al. (same group) on size and complexity: there AI files and functions are larger. Agrees with Mao that AI code has more high-severity security findings.
- Contradicts Cung's "enterprise patterns" anecdote (same group): no sign of bloat here.
