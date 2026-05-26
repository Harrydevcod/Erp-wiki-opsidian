# AGENTS.md

This vault is an LLM Wiki: a persistent, compounding second brain maintained by LLM agents.

Before doing wiki work, read and follow [[CLAUDE]] / `CLAUDE.md`. That file is the canonical operating schema.

## Local Operating Rule

For every interaction in this vault:

1. Read `index.md`.
2. Read recent relevant entries in `log.md`.
3. Classify the task as `ingest`, `query`, `maintain`, `lint`, `schema`, `tooling`, or `chat-only`.
4. Search relevant wiki pages before answering.
5. Update the wiki when the answer or operation creates durable knowledge.
6. Update `index.md` and append `log.md` whenever files change.

## Role Split

- The human curates sources, asks questions, and decides direction.
- The agent writes and maintains the wiki.
- Raw sources in `raw/` are immutable evidence.
- Generated knowledge lives in `wiki/`.

## Quality Bar

World-class only. Clear structure, cited claims, explicit uncertainty, maintained links, and no lazy summaries.

