# Stop Over-Engineering AI Apps: The Case for Boring Technologies
- **Source:** Tiger Data (Timescale, Inc.) blog, Jascha Beste, February 18th, 2025. https://www.tigerdata.com/blog/stop-over-engineering-ai-apps
- **Type:** practitioner article (vendor blog)
- **Evidence strength:** weak. An argument plus one framework example. The "many stories" are anecdotal; the six linked write-ups aren't in the capture. Conflict of interest: the vendor recommends its own product (PostgreSQL with pgai/pgvector).

## Claims
- Quotes Anthropic's "Building Effective Agents": the most successful implementations used simple, composable patterns, not complex frameworks.
- LangChain's example RAG app introduces seven new concepts (StateGraphs, sequences, graph builders, vector stores, splitters, documents, loaders) on top of the RAG basics. It also wraps standard pieces: `OpenAIEmbeddings` is LangChain's wrapper, not the official client, and BeautifulSoup sits inside a Loader.
- Many teams built RAG MVPs on LangChain and rebuilt without a framework "a month or so later" ("we've heard many stories"; anecdotal).
- Framework layers make debugging span several layers, make customization hard and add a parallel vocabulary to learn (asserted).
- LLM primitives are simple types (messages are strings, embeddings are lists of floats), so plain language features are enough (asserted).
- LiteLLM does one job (a unified API across LLM providers). Adding it to pgai Vectorizer gave support for "basically every embedding provider".
- PostgreSQL has been a backbone "for over 30 years". With pgvector, pgai and pgvectorscale it handles vector search alongside relational queries, and "works just as well" as specialized vector databases (asserted, no benchmark).
- The pgai SQL and SQLAlchemy samples are garbled in OCR (only fragments such as "768" survive). Don't use them.

## What humans catch that AI misses (per this source)
- A framework that buries simple operations under its own abstractions and vocabulary.
- A new service (a separate vector database plus sync logic) that adds failure modes when the existing database could do the job.
- Wrappers around official clients that add nothing.

## Checks for the reviewer
- **New dependency or service must earn its place.** For each new package or service in the diff (`package.json`, `requirements*.txt`, `pyproject`, `docker-compose`), require a one-line reason and check whether the existing stack already covers it. `NEW: reuse before build`
- **Pass-through wrappers.** Functions or classes whose body only calls one library function with the same arguments, or that rename a library's concepts without adding behavior. Detect with an AST scan for single-call bodies or by eye in the diff. `NEW: speculative abstraction`
- **Dual writes to two stores.** Writing the same data to the main DB and a second store (search index, vector DB, cache) without one transaction or outbox can leave them out of step. Maps to #1 (and #15 if one store is files).
- **Framework imported for one use.** A new framework imported in a single file for a single job. `NEW: speculative abstraction`

## Over-engineering signals (if relevant)
- "All-in-one" frameworks adopted for a narrow need. Detect a large dependency with one call site.
- Wrappers over official clients. Detect classes named after a library that only forward calls.
- A specialized datastore beside a general one that could do the job. Detect a new DB service plus sync code.
- A parallel vocabulary: new names for existing concepts. Detect types that rename library types one-to-one.

## Process lessons for a non-coder directing AI
- Tell the agent: no new frameworks, services or datastores without a written reason, and prefer the database and libraries already in the project.
- Choose boring, composable tools that do one thing.

## Quotes
- "Consistently, the most successful implementations weren't using complex frameworks or specialized libraries." (Anthropic, quoted by the author)
- "An application leveraging LLMs is still just an app."

## Caveats
- The vendor is promoting its own extension. "Works just as well" is unsupported.
- It's about how to architect LLM apps, not about AI-written code. It's relevant here only for the dependency and abstraction smells.
- Dated February 2025. The LangChain criticism may be stale.
- The related-posts section (other Tiger Data articles, 2026) was ignored.
