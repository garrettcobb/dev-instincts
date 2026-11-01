# Why I Think Most AI Agents Are Overengineered
- **Source:** DEV Community, Jaideep Parashar (founder, ReThynk AI; author of "40+ books" on AI), posted Jun 21 (year not shown; the comments are dated June, probably 2026). No URL in the text.
- **Type:** opinion/essay
- **Evidence strength:** anecdotal — no data, only the author's experience.

## Claims
All asserted without evidence:
- Builders make six-agent pipelines (research, planner, retriever, memory, answer, reviewer) for PDF Q&A, which a linear workflow (PDF → chunk → embed → vector DB → LLM → response) handles.
- Most AI applications are deterministic workflows: document Q&A, customer support, meeting summaries, blog generation, code review, knowledge assistants.
- Every extra agent adds prompts (tokens), latency, chances for hallucinations to spread downstream, debugging pain, and infrastructure (memory, orchestration, retries, monitoring).
- Agents pay off for long-running tasks, real decision-making, human-in-the-loop systems and multi-tool collaboration.
- The industry is repeating its pattern with microservices, Kubernetes and distributed systems: adopting them before needing them.
- His rule: workflow first, agent second, multi-agent last.
- Reader comment: a builder of an accounting suite replaced most LLM calls with an OCR engine and kept the LLM only for "understanding", which made it faster, with fewer errors, at a fraction of the cost per page. Anecdote with no numbers. (A second comment's large performance claims are unverified and ignored here.)

## What humans catch that AI misses (per this source)
- Not about AI-written code.

## Checks for the reviewer
- Agent or orchestration layers in a linear pipeline. Detect: imports of agent frameworks (`crewai`, `langgraph`, `autogen`), or several chained LLM calls where each step is a fixed transform. Ask which step makes a real decision. → NEW: Complexity must be earned.
- An LLM doing deterministic extraction (layout, fixed-rule classification, field parsing). Detect: model calls whose prompt describes a fixed rule or format. → NEW: No probabilistic step where the answer must be exact.

## Over-engineering signals (if relevant)
- Multiple prompts, memory sync, retries and state management for a sequence with no branching. Detect: count LLM calls and branch points per request.

## Process lessons for a non-coder directing AI
- Before approving an agent design, ask whether a fixed workflow can do it. Start there, and add agents only when a real problem demands them.

## Quotes
- "Complexity should be earned, not assumed."
- "Workflow first. Agent second. Multi-agent last."

## Caveats
- About AI-app architecture, not code review. It's relevant only where a project embeds LLM pipelines.
- No evidence; promotional author profile.
