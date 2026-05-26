---
type: index
status: active
created: 2026-05-26
updated: 2026-05-26
---

# LLM Wiki Index

This is the navigation layer for the second brain. Read this file first before answering questions or updating the wiki.

## Operating Files

- [[CLAUDE]] - Primary schema and operating contract for maintaining this wiki.
- [[AGENTS]] - Codex bridge that points agents back to the schema.
- [[log]] - Chronological record of ingests, queries, lint passes, and maintenance.

## Source Pipeline

- `raw/inbox/` - New sources waiting to be processed.
- `raw/archive/` - Sources already ingested. Keep originals unchanged.
- `raw/assets/` - Local images, PDFs, screenshots, audio, video, and clipped article assets.

## Wiki Areas

### Sources

- [[2026-05-26 - Captura Raw e Docs]] - Consolidated capture of `raw/` and `docs/` source folders, including NOVA-ERP product docs and fiscal/Cegid Primavera documents.

### Entities

- [[Cegid Primavera]] - ERP reference corpus for fiscal, accounting, treasury, logistics, HR, asset and extensibility workflows.
- [[DNRE]] - Cabo Verde tax authority context behind invoice and electronic invoice materials.
- [[Supabase]] - Backend platform for NOVA-ERP: PostgreSQL, Auth, RLS, storage and Edge Functions.

### Concepts

- [[ERP SaaS Multi-Tenant]] - Tenant-isolated ERP SaaS architecture model for NOVA-ERP.
- [[Fiscalidade Cabo Verde]] - Tax/compliance domain for IVA, invoices, declarations, e-Fatura and SAF-T CV.
- [[e-Fatura Cabo Verde]] - Electronic invoice domain and DNRE integration context.
- [[SAF-T CV]] - Cabo Verde fiscal audit/export reporting domain.
- [[Supabase Deployment]] - Deployment and runtime process for the Supabase backend stack.

### Syntheses

No synthesis pages yet.

### Questions

No filed answers yet.

### Projects

- [[NOVA-ERP]] - Modern multi-tenant ERP SaaS for Cabo Verde with fiscal compliance and future AI layer.

### People

No people pages yet.

### Places

- [[Cabo Verde]] - Primary jurisdiction and market context for NOVA-ERP.

### Maps

- [[Mapa de Fontes - NOVA-ERP e Fiscalidade]] - Source map connecting product, architecture, fiscal and ERP reference materials.

### Contradictions

No contradiction notes yet.

## Maintenance Queue

- Deep-ingest `raw/assets/SSD/PRD.MD` as the canonical product source.
- Deep-ingest `raw/assets/SSD/SSD.md` and reconcile it against the PRD.
- Deep-ingest the e-Fatura technical manual before implementation decisions.
- Verify current Cabo Verde fiscal rules before treating old fiscal documents as implementation authority.
- Deduplicate the two Cegid Primavera fiscalidade decks.
