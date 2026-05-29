---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/SSD/SSD.md
source_type: software-system-specification
author:
published: 2026-04-02
ingested: 2026-05-26
tags: [source, ssd, nova-erp, specification, architecture]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]"]
confidence: high
---

# SSD NOVA-ERP

## Summary

The SSD turns the NOVA-ERP vision into a functional, technical and operational development specification. It is the strongest source for how modules should be implemented before code is written.

Source: `raw/assets/SSD/SSD.md`

## Development Principles

- Multi-tenant by default.
- Fiscality as system core.
- Everything relevant is auditable.
- Everything is configurable by company.
- Modular, extensible and versionable.
- API-first where possible.
- Prepared for cloud and self-hosting.
- Security, fiscal immutability and traceability are base requirements.

## Technical Signals

The SSD names:

- frontend: React, Vite, TypeScript and Tailwind;
- backend: Node.js and TypeScript;
- database: PostgreSQL/Supabase;
- multi-tenant authentication and authorization;
- event-driven flows for critical operations;
- structured logs and total audit;
- tenant/plan feature flags;
- queues for heavy tasks;
- decoupled document generation.

## Architecture Layers

The SSD groups the ERP into:

- platform base;
- master data;
- transactional layer;
- fiscal and legal layer;
- intelligence and automation layer.

This layering supports the current wiki architecture and makes module sequencing explicit.

## Domain Events

The SSD identifies domain events such as:

- tenant creation and activation;
- user invitation and tenant membership;
- entity and item creation;
- sale document creation, certification, e-Fatura sending, authorization and rejection;
- purchase document posting;
- inventory movement and adjustment;
- receivable/payable creation;
- payment receipt and payment made;
- bank reconciliation;
- journal entry posting;
- SAF-T generation;
- tax period closing;
- payroll processing;
- asset depreciation;
- subscription changes.

## Critical Requirements

- All core and transactional tables must carry `tenant_id`.
- Audit logs must include tenant, actor, entity, action and before/after data where relevant.
- Automated tests must prevent cross-tenant access.
- Fiscal documents cannot be changed after certification/authorization.
- e-Fatura communication should use async queues and technical state tracking.
- SAF-T and heavy reports should be generated asynchronously.
- AI must never mutate critical data without human confirmation.

## Roadmap Signal

The SSD matches the PRD's phased structure:

1. Platform base.
2. Master data.
3. Commercial operation.
4. Fiscal core.
5. Complete finance.
6. HR/assets/projects.
7. Advanced AI and automation.

## Open Questions

- Which SSD requirements already exist in the code/database and which are still only target specification?
- Should domain events become a formal event table, audit stream, background-job queue, or all three?
- Which fiscal events require immutable logs versus normal audit logs?

