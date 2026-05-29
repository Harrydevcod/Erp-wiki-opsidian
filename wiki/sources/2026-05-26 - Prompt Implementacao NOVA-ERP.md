---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/SSD/PROMPT.MD
source_type: implementation-prompt
author:
published:
ingested: 2026-05-26
tags: [source, implementation, prompt, nova-erp, foundation-release]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]"]
confidence: high
---

# Prompt Implementacao NOVA-ERP

## Summary

This implementation prompt defines the expected foundation release for NOVA-ERP: a usable, coherent, modular and technically solid ERP SaaS base rather than a visual demo.

Source: `raw/assets/SSD/PROMPT.MD`

## Role In Source Hierarchy

This source is not the highest product authority. PRD, SSD and structured backlog define product intent and scope. This prompt translates that intent into implementation expectations for the first build.

Inference from: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]]

## Required Stack

- Frontend: React, TypeScript and Vite.
- UI: Tailwind CSS.
- Backend/API/server actions: TypeScript.
- Database: Supabase PostgreSQL.
- Auth: Supabase Auth.
- Validation: Zod or equivalent.
- Dashboards: a modern lightweight charting library.

## Implementation Principles

- Do not create disposable code.
- Do not rely on fake mocks where real structure is possible.
- Prioritize data model quality, domain separation, tenant isolation and security.
- Generate an initial seed.
- Implement routes, pages, components, database, security policies and principal flows.
- Avoid irresponsible hardcodes.
- Prepare the codebase for phased growth.

## Foundation Release Scope

The prompt asks to implement now:

1. Core/tenants/auth.
2. Entities.
3. Products/services.
4. Sales.
5. Purchases.
6. Inventory.
7. Treasury/current accounts.
8. Base Cabo Verde fiscality.
9. e-Fatura-ready integration domain/adapters.
10. SAF-T-ready export job structure.
11. Initial dashboard.
12. Scalability foundation.

## Minimum Data Model Signals

The prompt calls for:

- `tenants`, `tenant_memberships`, roles, permissions and audit logs;
- entities for customers, suppliers, third parties and anonymous/VD customer;
- products/services with stock behavior;
- sales documents, sale lines, document series and document types;
- purchase documents and purchase lines;
- warehouses, stock movements and stock balances or efficient equivalent;
- receivables/payables, payments, allocations, cash/bank accounts and cash movements;
- tax rates, tenant tax profiles, exemptions and fiscal periods;
- integration configs, certificate metadata, fiscal transmissions and transmission logs;
- SAF-T export jobs and export history.

## Required Screens

Public:

- login;
- registration/create company.

Private:

- dashboard;
- tenant/settings;
- users;
- profiles/permissions;
- customers;
- suppliers;
- articles;
- services;
- sales list/new/detail;
- purchases list/new;
- inventory;
- warehouses;
- treasury;
- pending documents;
- fiscality/configuration;
- integrations;
- SAF-T exports;
- audit.

## Required UI Components

- AppShell.
- Sidebar.
- Header.
- TenantSwitcher.
- PageHeader.
- DataTable.
- FilterBar.
- FormField.
- MoneyField.
- StatusBadge.
- EmptyState.
- ConfirmDialog.
- AuditTimeline.
- DocumentTotalsCard.

## Architectural Constraints

- All applicable domain tables include `tenant_id`.
- Users can belong to multiple tenants.
- Tenant switching is visible in UI.
- Permissions are evaluated by tenant.
- Supabase RLS/policies must enforce tenant isolation.
- Critical actions are protected and audited.
- Fiscal/e-Fatura/SAF-T structures are prepared even if full legal integration is not finished in this phase.

## Seed Requirements

The prompt expects a demo-ready seed with:

- one demo tenant;
- one demo admin;
- anonymous/VD customer;
- customers and suppliers;
- articles and services;
- one warehouse;
- one document series;
- sample documents;
- sample financial movements;
- visible dashboard data.

## Execution Order

The prompt orders execution as:

1. project architecture and structure;
2. schema and auth;
3. multi-tenant and memberships;
4. permissions;
5. entities;
6. catalog;
7. sales;
8. purchases;
9. inventory;
10. treasury;
11. base fiscality;
12. base integrations;
13. dashboard;
14. final refinement.

## Tensions And Risks

- The prompt asks for broad implementation in a single foundation release. Scope must be controlled to avoid shallow delivery.
- It prioritizes foundation solidity over visual polish, which is aligned with the wiki's architecture standard.
- Legal/fiscal completion is explicitly out of scope for this phase, but data structures and states must be prepared.
- e-Fatura and SAF-T placeholders must be real domain/adapters/jobs, not fake UI-only buttons.

## Open Questions

- Which implementation source wins if the prompt conflicts with SSD module sequencing?
- Which acceptance criteria from the backlog should become tests for the foundation release?
- Should the target schema be designed from this prompt before resolving the current database contradiction?

