---
type: synthesis
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [synthesis, nova-erp, modules, priority]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-26 - Captura Raw e Docs]]"]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Knowledge Architecture]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[Fiscalidade Cabo Verde]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# NOVA-ERP Module Priority Map

## Summary

NOVA-ERP should be built around a fiscal/commercial operating core first, then expanded into accounting depth, HR/payroll, assets, projects, SaaS billing, analytics and AI.

This is a synthesis from the deep-ingested PRD, SSD and structured backlog. It is still a planning map, not a committed delivery plan.

Source: [[2026-05-26 - PRD NOVA-ERP]]
Source: [[2026-05-26 - SSD NOVA-ERP]]
Source: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
Source: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]

## Foundation Layer

These modules should exist before any serious ERP workflow is trusted:

- [[ERP SaaS Multi-Tenant]]
- [[Permissoes e Auditoria ERP]]
- [[Supabase Deployment]]
- Tenant/company setup, users, roles, permissions, audit logs and configuration.

Rationale: multi-tenancy, permissions and auditability are structural constraints. Retrofitting them after fiscal documents or payroll exist would create unacceptable risk.

## Fiscal/Commercial Core

These modules form the first sellable ERP spine:

- [[Compras e Vendas ERP]]
- [[Faturacao Eletronica]]
- [[Fiscalidade Cabo Verde]]
- [[e-Fatura Cabo Verde]]
- [[SAF-T CV]]
- [[Inventario ERP]]
- [[Tesouraria ERP]]

Rationale: sales, purchases, stock and treasury generate the operational and fiscal events that make the ERP useful in Cabo Verde. Fiscal correctness must be designed into document creation, not bolted on later.

## Accounting And Operational Depth

These modules deepen business completeness:

- [[Contabilidade ERP]]
- [[Processamento de Salarios ERP]]
- [[Gestao de Ativos ERP]]
- [[Projetos ERP]]

Rationale: accounting, payroll, assets and projects are essential for a full ERP, but the first implementation must decide how much of each is required before launch versus phase two.

## Platform Business Layer

This layer commercializes NOVA-ERP itself:

- [[Subscricoes SaaS ERP]]

Rationale: the platform needs plans, entitlements, billing and access enforcement to operate as SaaS. The open design question is whether NOVA-ERP should use its own invoicing module for its SaaS invoices.

## Intelligence Layer

These modules create visibility and automation:

- [[Dashboards e Relatorios ERP]]
- [[IA Assistente ERP]]

Rationale: dashboards should ship earlier as product value and operational control. AI should wait until permissions, reporting views, audit logs and data quality are strong enough to avoid unsafe answers.

## Reconciled Backlog Phases

The structured backlog suggests:

- MVP phase 1: platform, entities, products/services, sales, purchases, inventory, treasury, fiscality, e-Fatura and SAF-T.
- Phase 2: accounting, dashboards and SaaS subscriptions.
- Phase 3: HR, assets, projects and AI.

This mostly matches the PRD/SSD roadmap. The main tension is that SAF-T and fiscal reporting may require accounting-grade data structures before full accounting UI is delivered.

## Foundation Release Build Order

The implementation prompt suggests this build order:

1. Architecture and project structure.
2. Schema and auth.
3. Multi-tenant memberships.
4. Permissions.
5. Entities.
6. Catalog.
7. Sales.
8. Purchases.
9. Inventory.
10. Treasury.
11. Base fiscality.
12. Base integrations.
13. Dashboard.
14. Final refinement.

This is the most actionable order for implementation work, while the broader PRD/SSD/backlog remain the authority for product scope and acceptance.

## Fiscal-First Reinforcement

[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] reinforces that fiscality, e-Fatura, SAF-T CV, Modelo 106, auditability and tenant isolation should constrain every module. Treat this as implementation posture, while validating legal specifics against official sources.

## Critical Open Decisions

- Which compliance flows are mandatory before production in Cabo Verde?
- Whether full accounting is required for the first sellable release.
- Whether e-Fatura communication should be synchronous or asynchronous.
- Whether subscriptions should be billed through NOVA-ERP's own invoicing module.
- Which AI capabilities are read-only versus action-capable.
- How much of the foundation release can reuse the current database without inheriting e-commerce/POS drift.
