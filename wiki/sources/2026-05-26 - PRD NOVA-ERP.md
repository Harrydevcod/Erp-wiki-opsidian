---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/SSD/PRD.MD
source_type: product-requirements-document
author:
published: 2026-04-02
ingested: 2026-05-26
tags: [source, prd, nova-erp, product, roadmap]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]"]
confidence: high
---

# PRD NOVA-ERP

## Summary

The PRD defines NOVA-ERP as a modern multi-tenant ERP SaaS for Cabo Verde, built around native fiscal compliance, electronic invoicing, DNRE/e-Fatura integration, SAF-T CV, modular ERP operations, dashboards, auditability and future AI.

Source: `raw/assets/SSD/PRD.MD`

## Strategic Claims

- NOVA-ERP should compete with or replace Primavera, PHC, Odoo and SAP Business One in the Cabo Verde/local-regional ERP market.
- Fiscal compliance is not a later module; it is a product differentiator and design center.
- The product must support both cloud-ready and self-hosting-ready operation.
- The target product is not merely invoicing or commercial management; it is a complete operational ERP base.
- AI and analytics are strategic future layers, but they depend on authorized data, auditability and strong foundations.

## Included Scope

The PRD includes:

- multi-tenant platform;
- companies, users and permissions;
- entities, products and services;
- sales, purchases, inventory and treasury;
- accounting and fiscality;
- HR, assets and projects;
- reports, dashboards and SaaS subscriptions;
- SAF-T CV and e-Fatura/middleware;
- AI foundation.

## MVP Recommendation

The PRD recommends an MVP with:

- platform base;
- multi-tenant;
- users and permissions;
- entities;
- products/services;
- sales;
- purchases;
- base inventory;
- base treasury;
- base fiscality;
- base e-Fatura;
- base SAF-T;
- essential dashboards.

The PRD explicitly excludes from MVP:

- complete HR;
- advanced assets;
- complete projects;
- advanced AI;
- sophisticated SaaS billing.

## Roadmap Signal

The PRD phases the product as:

1. Core: multi-tenant, auth, permissions, companies, users, audit and configuration.
2. Master data: entities, products/services, series, taxes, warehouses and base documents.
3. Commercial operation: sales, purchases, inventory, current accounts and base treasury.
4. Fiscal core: document rules, IVA/REMPE, Modelo 106 base, e-Fatura base and SAF-T base.
5. Complete finance: accounting, reconciliation, closings and financial reports.
6. HR, assets and projects.
7. AI and automation.

## Non-Functional Bar

The PRD requires:

- tenant isolation;
- secure login and sessions;
- permission control by action;
- audit logs for critical events;
- performance for document issue and SAF-T generation;
- async jobs for heavy operations;
- observability, backups and fallback for integrations.

## Compliance Notes

The PRD includes regulatory context for e-Fatura and SAF-T CV, but these claims must be verified against current official Cabo Verde/DNRE sources before implementation.

## Open Questions

- Which official fiscal sources are current enough to turn PRD compliance assumptions into implementation requirements?
- Should accounting be pulled earlier than phase 5 because SAF-T and fiscal reporting depend on accounting consistency?
- Which dashboards count as "essential" for MVP?

