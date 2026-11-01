# How to Stop Over-Engineering with AI When a Simple Query Will Do
- **Source:** DEV Community, Alan West (full-stack developer), posted Mar 25, edited Mar 29 (year not shown), https://dev.to/alanwest/how-to-stop-over-engineering-with-ai-when-a-simple-query-will-do-26b7
- **Type:** practitioner article
- **Evidence strength:** anecdotal — two first-hand examples; the latency and cost figures are rules of thumb, not measured here.

## Claims
- He spent three days building embeddings + vector DB + RAG search for an internal tool over 12,000 well-structured records. PostgreSQL full-text search (tsvector + GIN index) did the job.
- Root cause: solution-first thinking ("how can I use AI here?" instead of "what does the feature need?").
- Failure modes of unneeded AI: latency (an LLM call adds 500 ms–3 s to something that could take 5 ms), unpredictable token cost (e.g., a feature hit 10,000 times a day), and non-deterministic output where you need determinism.
- A colleague sent every support ticket to an LLM to get its priority. It was replaced by regex rules derived from 6 months of ticket data: less nuanced, but consistent, testable, instant and free.
- A hosted-model API call takes at least 200–500 ms even for simple tasks.
- Even at temperature 0, outputs can vary across model versions.
- He replaced an AI feature with 40 lines of SQL, and it hasn't needed a prompt change since.
- Decision questions: is the input structured? Is deterministic output required? What's the latency budget? Could a senior developer write the rules in an afternoon? What happens when the AI is wrong (data corruption, security issues, billing errors)?
- AI is the right call for long-document summarization, semantic search over truly unstructured data, code generation/transformation, and nuanced moderation at scale.

## What humans catch that AI misses (per this source)
- Not about AI-written code; it's about people reaching for AI. The human catch here is the teammate asking "couldn't you just use full-text search?"

## Checks for the reviewer
- An LLM or embedding call over structured data. Detect: imports of `openai`, `anthropic`, embedding or vector-DB clients (`chromadb`, `pinecone`, `pgvector`, `langchain`); check what data flows in and whether a query, index or regex would do. → NEW: Complexity must be earned.
- A probabilistic step in a path that must be exact: model output feeding money, priority, permissions or stored records. Detect: trace the model call's return value to writes (`save()`, `UPDATE`, totals, status changes). → NEW: No probabilistic step where the answer must be exact.
- A rules-based replacement must be tested: every regex or rule gets positive and negative cases, including look-alike words. → #9, #32.

## Over-engineering signals (if relevant)
- Vector DB/RAG for a few thousand structured rows; LLM classification for rules you could write in an afternoon; an external API call in a hot path. Detect: dependency diff plus call sites.

## Process lessons for a non-coder directing AI
- Pre-flight before any AI component: write down in plain English what the feature must do; try the standard library and the database; then a well-known non-AI library (regex, full-text search, rules engine); only then prototype with AI, and measure latency, cost and accuracy against the simple version on real data.
- If you can't say why the AI version is meaningfully better, drop it.

## Quotes
- "I'd built a Ferrari to drive to the mailbox."
- "Start with the simplest thing that works. Add complexity only when the simple thing fails."

## Caveats
- About choosing AI as a component, not about AI-written code. It's relevant to the reviewer only where an app embeds model calls.
- The code samples are OCR-garbled (e.g., `5[@-9]` for `5[0-9]`), and the Python embedding example is unreadable.
- The article's own priority regex appears to match `down` anywhere, so "download" or "dropdown" would be rated high priority. That's exactly the edge case its "testable" claim depends on someone testing. This reading may be affected by OCR.
