---
type: map
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [lint, raw-assets, nova-erp, source-review]
sources: ["raw/assets/", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]"]
related: ["[[NOVA-ERP]]", "[[Mapa de Fontes - NOVA-ERP e Fiscalidade]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]", "[[Contradiction - Middleware URL Scope]]"]
confidence: high
---

# Revisao Raw Assets - 2026-05-26

## Scope

Reviewed `raw/assets/` as the source corpus for [[NOVA-ERP]]. Raw files were inspected, but not edited.

Evidence: `raw/assets/`

## Inventory

`raw/assets/` currently contains:

- product/spec sources:
  - `raw/assets/SSD/PRD.MD`
  - `raw/assets/SSD/SSD.md`
  - `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
  - `raw/assets/SSD/BACKLOG SCRUM — NOVA-ERP.MD`
  - `raw/assets/SSD/PROMPT.MD`
  - `raw/assets/NOVA_ERP_PRD.md`
  - `raw/assets/NOVA_ERP_PRD_AVANCADO.pdf`
  - `raw/assets/NOVA-ERP_Instrucoes_Oficiais_1.md`
- implementation/deployment sources:
  - `raw/assets/DATABASE_ER_DIAGRAM.md`
  - `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`
  - `raw/assets/SUPABASE_DEPLOY.md`
  - `raw/assets/LOCAL_SETUP.md`
  - `raw/assets/LOCAL_SETUP-Arydson.md`
  - `raw/assets/NOVA-ERP_Middleware_Dev_Local_para_VPS.md`

## Source Authority Assessment

### Canonical Product Sources

The highest-authority product sources remain:

- [[2026-05-26 - PRD NOVA-ERP]]
- [[2026-05-26 - SSD NOVA-ERP]]
- [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]
- [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

These should govern product scope, module sequencing and implementation requirements unless explicitly superseded.

### Implementation Prompt

[[2026-05-26 - Prompt Implementacao NOVA-ERP]] is highly actionable. It narrows the first foundation release around actual implementation: React, TypeScript, Vite, Supabase, RLS, tenant isolation, entities, catalog, sales, purchases, inventory, treasury, fiscal base, e-Fatura-ready adapters, SAF-T-ready jobs and dashboard.

Review result: ingested and reconciled into [[NOVA-ERP Product Authority Synthesis]].

### Official Instructions

[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] is strong as an operating manifesto for fiscal-first architecture, e-Fatura middleware, module coverage, security/audit and UX. It includes concrete rules but should be treated carefully where it makes legal or fiscal claims.

Review result: ingested and reconciled into [[NOVA-ERP Product Authority Synthesis]], [[Contradiction - Middleware URL Scope]] and later [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]].

### Middleware Dev/VPS Guide

[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] is operationally important for e-Fatura deployment, environments, local middleware, VPS production, tenant onboarding and contingency retry behavior.

Review result: ingested and reconciled into [[e-Fatura Cabo Verde]], [[Faturacao Eletronica]], [[Contradiction - Middleware URL Scope]] and later [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]].

### Subscription Architecture

`raw/assets/SUBSCRIPTION_ARCHITECTURE.md` is mature and implementation-shaped. It defines plan catalog, add-ons, contracts, billing runs, invoices, usage metrics, access enforcement, lifecycle states and audit events.

Review result: deep-ingest before building [[Subscricoes SaaS ERP]].

### Database ER Diagram

`raw/assets/DATABASE_ER_DIAGRAM.md` appears to describe an existing/current database snapshot with strong e-commerce/POS heritage: orders, reservations, wishlist, reviews, shipping costs, promotional banners and chat. It is useful evidence of current state, but it is not the target architecture for NOVA-ERP.

Review result: ingest as "current database snapshot" and reconcile against [[NOVA-ERP Product Authority Synthesis]] before schema decisions.

## Major Risks

### Current Database Drift

`DATABASE_ER_DIAGRAM.md` does not match the target ERP domain cleanly. It includes useful concepts such as documents, document series, financial transactions, inventory movements and e-Fatura logs, but also contains e-commerce structures that should not drive core ERP architecture.

Tracked in: [[Contradiction - Current Database Snapshot vs Target ERP Architecture]]

### Middleware Configuration Scope Conflict

`NOVA-ERP_Instrucoes_Oficiais_1.md` says middleware URL must be dynamic and persisted per tenant. `NOVA-ERP_Middleware_Dev_Local_para_VPS.md` says the ERP only needs one `MIDDLEWARE_URL` environment variable per environment.

Originally tracked in: [[Contradiction - Middleware URL Scope]]

Current interpretation: superseded by [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]].

### Sensitive Secret Handling

The reviewed files mostly use placeholders, not real secrets. Still, deployment and middleware docs mention service role keys, client secrets, certificates, keystores and webhook secrets. These files should remain raw evidence, but implementation must ensure secrets never enter committed config or wiki summaries.

Evidence: `raw/assets/SUPABASE_DEPLOY.md`, `raw/assets/NOVA-ERP_Middleware_Dev_Local_para_VPS.md`

### Encoding Quality

Several raw markdown files display mojibake in terminal output. The semantic content is still readable, but future ingestion should preserve original files and create clean UTF-8 wiki summaries rather than rewriting raw sources.

## Recommended Next Ingestion Order

1. `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`
2. `raw/assets/DATABASE_ER_DIAGRAM.md`
3. `raw/assets/SUPABASE_DEPLOY.md`
4. `raw/assets/LOCAL_SETUP-Arydson.md`
5. `raw/assets/NOVA_ERP_PRD_AVANCADO.pdf`
6. `raw/assets/NOVA_ERP_PRD.md`

## Actionable Recommendations

- Treat PRD/SSD/backlog as product authority.
- Treat [[2026-05-26 - Prompt Implementacao NOVA-ERP]] as implementation authority for the foundation release after reconciliation.
- Treat `DATABASE_ER_DIAGRAM.md` as current-state evidence, not target schema.
- Verify actual DNRE middleware emitter-group behavior before automating production tenant onboarding.
- Deep-ingest subscription architecture before building SaaS billing.
- Use [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] as operational input before production e-Fatura decisions.
- Keep raw files immutable; normalize encoding only in generated wiki pages.
