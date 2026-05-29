# AGENTS.md

This vault is the NOVA-ERP Cabo Verde LLM Wiki: a persistent, compounding product, fiscal, domain and engineering memory maintained by LLM agents.

Before doing wiki work, read and follow [[CLAUDE]] / `CLAUDE.md`. That file is the canonical operating schema for the NOVA-ERP knowledge base.

## Project Focus

NOVA-ERP is a modern multi-tenant ERP SaaS for Cabo Verde. The wiki exists to support product definition, architecture, implementation and audit-grade reasoning across:

- fiscalidade Cabo Verde, IVA, e-Fatura, DNRE and SAF-T CV;
- faturacao, compras, vendas, inventario, tesouraria, contabilidade, RH/processamento salarial and ativos;
- SaaS tenancy, permissions, audit logs, subscriptions and Supabase deployment;
- module design decisions that should surpass legacy ERP workflows instead of copying them blindly.

## Local Operating Rule

For every interaction in this vault:

1. Read `index.md`.
2. Read recent relevant entries in `log.md`.
3. Classify the task as `ingest`, `query`, `maintain`, `lint`, `schema`, `tooling`, or `chat-only`.
4. Search relevant wiki pages before answering.
5. Update the wiki when the answer or operation creates durable knowledge.
6. Update `index.md` and append `log.md` whenever files change.
7. For module or compliance work, cite evidence and mark legal/fiscal uncertainty explicitly.

## Role Split

- The human curates sources, asks questions, and decides direction.
- The agent writes and maintains the wiki.
- Raw sources in `raw/` are immutable evidence.
- Generated knowledge lives in `wiki/`.

## Quality Bar

World-class only. Clear structure, cited claims, explicit uncertainty, maintained links, fiscal caution, implementation usefulness and no lazy summaries.
