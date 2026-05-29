---
type: map
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [map, nova-erp, operating-model, knowledge-architecture]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "raw/assets/SSD/PRD.MD", "raw/assets/SSD/SSD.md"]
related: ["[[NOVA-ERP]]", "[[Mapa de Fontes - NOVA-ERP e Fiscalidade]]", "[[Fiscalidade Cabo Verde]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# NOVA-ERP Knowledge Architecture

## Purpose

This map defines how the LLM Wiki should organize knowledge for [[NOVA-ERP]], a Cabo Verde-focused ERP SaaS.

The goal is not to store notes. The goal is to create a compounding product and engineering memory that can support implementation decisions, compliance reasoning, module design and future audits.

Source: [[2026-05-26 - Captura Raw e Docs]]

## Operating Spine

Every durable page should connect to at least one of these layers:

1. Product strategy: what NOVA-ERP is and why it exists.
2. Domain/compliance: fiscal, legal and operational rules for Cabo Verde.
3. Module design: how each ERP area should behave.
4. Architecture: tenancy, data model, security, auditability, deployment and integrations.
5. Execution memory: decisions, open questions, contradictions and implementation-ready syntheses.

## Primary Maps

- [[Mapa de Fontes - NOVA-ERP e Fiscalidade]] - source inventory and ingestion order.
- [[NOVA-ERP]] - project-level product and architecture summary.
- [[Fiscalidade Cabo Verde]] - tax and compliance layer.
- [[e-Fatura Cabo Verde]] - electronic invoice and DNRE integration layer.
- [[SAF-T CV]] - audit/export reporting layer.
- [[ERP SaaS Multi-Tenant]] - tenancy and SaaS isolation model.
- [[Configuracao ERP]] - tenant setup, fiscal profile, module activation, document series and e-Fatura readiness control plane.
- [[Supabase Deployment]] - operational backend deployment model.

## Module Entry Points

Use these module notes as working doors into module-specific synthesis:

- [[Faturacao Eletronica]]
- [[Configuracao ERP]]
- [[Compras e Vendas ERP]]
- [[Contabilidade ERP]]
- [[Inventario ERP]]
- [[Tesouraria ERP]]
- [[Processamento de Salarios ERP]]
- [[Gestao de Ativos ERP]]
- [[Subscricoes SaaS ERP]]
- [[Permissoes e Auditoria ERP]]
- [[Projetos ERP]]
- [[Dashboards e Relatorios ERP]]
- [[IA Assistente ERP]]

## Priority Synthesis

- [[NOVA-ERP Product Authority Synthesis]] - reconciles PRD, SSD and structured backlog into source authority and implementation implications.
- [[NOVA-ERP Module Priority Map]] - first-pass synthesis of foundation, fiscal/commercial core, accounting/operational depth, SaaS business layer and intelligence layer.

Potential next module pages:

- [[Entidades ERP]]
- [[Produtos e Servicos ERP]]

## Evidence Discipline

For each module, separate evidence by source type:

- Product intent: PRD, SSD, backlog and implementation prompt.
- Compliance authority: Cabo Verde law, DNRE manuals and fiscal documents.
- Legacy workflow reference: Cegid Primavera materials and exercises.
- Implementation evidence: database diagrams, deployment notes and architecture documents.
- Inference: agent synthesis based on the previous sources.

Do not collapse these categories. The same workflow can be useful as ERP reference but weak as legal evidence.

## Required Shape For Module Pages

Module pages should include:

- purpose;
- role in NOVA-ERP;
- source basis;
- core workflows;
- required master data;
- integration points;
- audit and security constraints;
- Cabo Verde compliance notes, when relevant;
- open questions;
- next ingestion targets.

Use `templates/module.md` for new module pages.

## Maintenance Rules

- When a new module page is created, add it to `index.md` and this map.
- When a module answer becomes durable, file it in `wiki/questions/` or update the module page directly.
- When sources disagree, create a contradiction page instead of hiding the mismatch.
- When legal freshness matters, mark the claim as needing verification against current Cabo Verde authority.
