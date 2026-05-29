---
type: synthesis
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [synthesis, nova-erp, product-authority, roadmap, architecture]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]"]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Module Priority Map]]", "[[NOVA-ERP Knowledge Architecture]]"]
confidence: high
---

# NOVA-ERP Product Authority Synthesis

## Core Interpretation

NOVA-ERP's source hierarchy should be:

1. [[2026-05-26 - PRD NOVA-ERP]] for product identity, scope, strategy, roadmap and MVP intent.
2. [[2026-05-26 - SSD NOVA-ERP]] for functional/technical implementation requirements before code.
3. [[2026-05-26 - Backlog Estruturado NOVA-ERP]] for execution decomposition into epics, features, user stories and acceptance criteria.
4. [[2026-05-26 - Prompt Implementacao NOVA-ERP]] for the first foundation release implementation shape: stack, schema expectations, pages, components, seed, RLS and execution order.
5. [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] for operating posture: fiscal-first, enterprise quality, middleware expectations, non-hardcoded configuration and design direction.
6. [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] for e-Fatura middleware environment/deployment operations, contingency and tenant onboarding flow.

Inference from: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]]

## Product Thesis

NOVA-ERP is not a narrow invoicing app. It is intended as a complete, modular, multi-tenant ERP SaaS for Cabo Verde, with fiscal compliance, commercial operations, inventory, treasury, accounting, SAF-T CV, e-Fatura, dashboards and future AI.

Source: [[2026-05-26 - PRD NOVA-ERP]]

## Non-Negotiable Architecture

The three product sources converge on these constraints:

- tenant isolation is foundational;
- permissions are evaluated per tenant;
- audit logs are required for critical actions;
- fiscal documents must become immutable after certification/authorization;
- heavy fiscal/reporting tasks need asynchronous processing;
- e-Fatura communication needs technical states, retries and request/response history;
- AI must respect authorization and cannot mutate critical data without human confirmation.

Source: [[2026-05-26 - SSD NOVA-ERP]]

## Reconciled Module Sequencing

The safest sequencing is:

1. Foundation: multi-tenant platform, auth, permissions, audit and setup.
2. Master data: entities, products/services, taxes, series, warehouses and document base.
3. Commercial core: sales, purchases, inventory, current accounts and base treasury.
4. Fiscal core: fiscal rules, IVA/REMPE, Modelo 106 base, e-Fatura base and SAF-T base.
5. Finance depth: accounting, banks, reconciliation, closings and financial reports.
6. Operational expansion: HR, assets and projects.
7. Intelligence: dashboards mature into analytics; AI assistant becomes safe once permissions, audit and reporting are trustworthy.

This reconciles the PRD/SSD roadmaps with the backlog's MVP and later phases.

Source: [[2026-05-26 - PRD NOVA-ERP]]
Source: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]

## Major Tension

The backlog places full accounting in phase 2, while the PRD/SSD position SAF-T and fiscal reporting in the MVP/fiscal core. This creates a design tension:

- SAF-T accounting exports and robust fiscal reporting require accounting-grade data consistency.
- A first sellable MVP may still launch with "accounting readiness" or partial accounting integration if full accounting is too large.

Current interpretation: do not build SAF-T as a detached XML generator. Build the fiscal core with accounting-compatible event and data structures from day one, even if full accounting screens ship later.

Inference from: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]]

## MVP Boundary

The MVP should include:

- tenant/company setup;
- users, roles, permissions and audit;
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

The MVP should not include complete HR, advanced assets, complete projects, advanced AI or sophisticated SaaS billing.

Source: [[2026-05-26 - PRD NOVA-ERP]]

## Foundation Release Implementation Boundary

The implementation prompt narrows the first actual build into a foundation release that should include real schema, auth, RLS, tenant memberships, permissions, entities, catalog, sales, purchases, inventory, treasury, fiscal configuration, e-Fatura-ready adapters, SAF-T-ready jobs, dashboard and demo seed.

It explicitly does not require complete legal/e-Fatura/SAF-T implementation in this phase, but requires correct domain shape, states, fields, adapters and extension points.

Source: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]

## Operating Instructions Layer

The official instruction source reinforces that NOVA-ERP should be fiscal-first, enterprise-grade, multi-tenant from the first line of code and designed with e-Fatura middleware as a critical integration path. It also introduces a stronger UX/brand direction: dark premium, blue/orange, productivity-first and responsive.

These instructions are valid as product/implementation posture. Fiscal claims inside them still require current official verification before implementation.

Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]

## e-Fatura Operational Layer

The middleware guide indicates that e-Fatura should be designed as an Edge Function mediated integration with:

- one middleware endpoint per environment as the likely default;
- tenant-level emitter/certificate/credential configuration;
- request/response logging;
- contingency queue;
- retry job;
- private-network production deployment where possible.

This does not resolve all DNRE/legal details, but it gives a concrete operational model for the implementation architecture.

Source: [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

## Implementation Implications

- Every module page should be checked against PRD intent, SSD rules and backlog acceptance criteria before implementation.
- Foundation-release implementation should additionally check [[2026-05-26 - Prompt Implementacao NOVA-ERP]] for required screens, components, seed and execution order.
- Acceptance criteria from the backlog should be converted into tests when work begins.
- Fiscal and payroll claims still require current legal/source verification; the product docs are not legal authority.
- The data model should support future accounting, SAF-T, audit and AI from the beginning.
- Dashboards and AI should never bypass permissions or tenant isolation.

## Decisions Still Needed

- Should partial accounting infrastructure be part of the MVP even if complete accounting is phase 2?
- Which official Cabo Verde fiscal sources are current enough to govern implementation?
- Which dashboards are "essential" for the first usable release?
- Should SaaS subscriptions use NOVA-ERP's own invoicing/fiscal engine?
- Which AI functions are read-only versus action-capable?
- Which current database tables can be reused without compromising the target foundation schema?
- Whether the middleware URL decision should be captured as an ADR before e-Fatura implementation.
- Whether tenant onboarding into middleware can be automated safely without exposing certificates or client secrets.
