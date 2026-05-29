---
type: project
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [nova-erp, erp, saas, cabo-verde, fiscalidade]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "raw/assets/SSD/PROMPT.MD", "raw/assets/SSD/BACKLOG SCRUM — NOVA-ERP.MD", "raw/assets/DATABASE_ER_DIAGRAM.md", "raw/assets/SUBSCRIPTION_ARCHITECTURE.md", "raw/assets/SUPABASE_DEPLOY.md"]
related: ["[[ERP SaaS Multi-Tenant]]", "[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]", "[[Supabase Deployment]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]"]
confidence: high
---

# NOVA-ERP

## Snapshot

NOVA-ERP is a planned modern ERP SaaS for Cabo Verde, designed as a multi-tenant platform with native fiscal compliance, electronic invoicing, DNRE/e-Fatura integration, SAF-T CV readiness, operational modules, dashboards, auditability and future AI assistance.

Source: [[2026-05-26 - PRD NOVA-ERP]]

## Product Thesis

The product aims to compete with or replace systems such as Primavera, PHC, Odoo and SAP Business One in the local/regional market by combining:

- Cabo Verde fiscal compliance from the foundation.
- Modern cloud-ready and self-hosting-ready architecture.
- Multi-company SaaS model.
- Strong document, tax, accounting, treasury and inventory flows.
- Better UX and automation than legacy ERP tools.
- Auditability and long-term extensibility.

## Core Modules

- Platform base and multi-tenant company management.
- Authentication, users, roles and permissions.
- Customers, suppliers and entities.
- Products, services, units, lots and serial numbers.
- Sales documents, corrective documents and document circuit.
- Purchases and goods reception.
- Inventory, warehouses, transfers and stock counts.
- Treasury, accounts receivable/payable, banks, cash and credit limits.
- Accounting and fiscal reporting.
- Cabo Verde fiscal rules, Modelo 106, e-Fatura, DNRE and SAF-T CV.
- HR and payroll.
- Asset management.
- Projects.
- SaaS subscriptions and plans.
- Dashboards, reports and AI assistant.

## Architecture Signals

- Frontend: React + TypeScript + Vite.
- UI: Tailwind CSS.
- Backend/database: Supabase PostgreSQL.
- Auth: Supabase Auth.
- Database governance: migrations, RLS, policies, triggers and storage.
- Runtime services: Supabase Edge Functions.
- Deployment: Supabase project link, `db push`, secrets and Edge Function deploy.

Sources: `raw/assets/LOCAL_SETUP.md`, `raw/assets/SUPABASE_DEPLOY.md`, `raw/assets/DATABASE_ER_DIAGRAM.md`

## Canonical Product Authority

- [[2026-05-26 - PRD NOVA-ERP]] defines product identity, scope, MVP intent and roadmap.
- [[2026-05-26 - SSD NOVA-ERP]] defines implementation requirements and module contracts before code.
- [[2026-05-26 - Backlog Estruturado NOVA-ERP]] defines execution epics, stories and acceptance criteria.
- [[NOVA-ERP Product Authority Synthesis]] reconciles the three.

## MVP Priority

The structured backlog suggests MVP emphasis on:

- Platform base.
- Entities.
- Products/services.
- Sales.
- Purchases.
- Inventory.
- Treasury.
- Fiscality.
- e-Fatura/middleware/DNRE.
- SAF-T CV.

Accounting, dashboards and SaaS subscriptions are indicated as later but still strategically important.

## Open Questions

- Should the MVP include accounting as operationally necessary, even if the backlog puts full accounting in phase 2?
- Which Cabo Verde compliance flows are legally mandatory before first production use?
- Should the ERP model be built around document immutability and certification from day one?

