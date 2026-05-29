---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/NOVA-ERP_Instrucoes_Oficiais_1.md
source_type: project-operating-instructions
author:
published:
ingested: 2026-05-26
tags: [source, nova-erp, official-instructions, fiscalidade, middleware]
related: ["[[NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[Contradiction - Middleware URL Scope]]", "[[NOVA-ERP Product Authority Synthesis]]"]
confidence: medium
---

# Instrucoes Oficiais NOVA-ERP

## Summary

This source is an official project instruction note for NOVA-ERP. It frames the product as an enterprise-grade multi-tenant ERP SaaS native to Cabo Verde, with fiscal-first architecture, mandatory e-Fatura middleware integration, integrated modules, auditability and premium dark UI direction.

Evidence: `raw/assets/NOVA-ERP_Instrucoes_Oficiais_1.md`

## Role In Source Hierarchy

This source is a strong project operating manifesto. It is useful for non-negotiable posture, fiscal-first architecture, middleware expectations and UX direction.

It should not override PRD/SSD/backlog on scope sequencing, and it should not be treated as current legal authority for fiscal claims without official verification.

Inference from: [[NOVA-ERP Product Authority Synthesis]]

## Project Identity

The source defines NOVA-ERP as:

- modern ERP;
- multi-tenant SaaS;
- native to Cabo Verde;
- intended for enterprise-level quality comparable to SAP, Odoo and Primavera.

## Required Stack And Design Direction

The source requires:

- frontend: React, Vite, TypeScript and Tailwind CSS;
- backend: Node.js;
- database: Supabase/PostgreSQL;
- visual style: dark premium with blue and orange;
- visual references: Primavera EVO, Odoo and SAP.

## Immutable Principles

The source states:

- fiscality first;
- every company is an isolated tenant;
- SaaS subscriptions, plans and modules are part of the architecture;
- modules should be independent but fully integrated.

## e-Fatura Middleware Claims

The source states that NOVA-ERP communicates with e-Fatura through middleware, not a direct e-Fatura API.

It also states middleware URL should be:

- dynamic;
- persistent;
- tenant-scoped;
- never hardcoded;
- editable in an ERP configuration screen;
- testable through a connection check.

This directly informs [[Contradiction - Middleware URL Scope]].

Current interpretation: [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]] keeps the non-hardcoded, tenant-aware requirement but constrains URL override as platform-admin-controlled. Ordinary tenant configuration should expose readiness and health status, not unrestricted fiscal endpoint editing.

## Fiscal Claims Requiring Verification

The source mentions:

- Cabo Verde IVA code;
- e-Fatura/DNRE;
- SAF-T CV;
- Modelo 106;
- document codes FT, FR, NC, ND and GT;
- document fields such as NIF, issue date, series, sequential number, IVA, QR Code and IUD;
- fiscal rules such as non-deletion of documents, credit notes referencing original invoices, sequential numbering and invoice issuance deadline;
- regimes such as Regime Normal and REMPE.

These claims are valuable implementation prompts but must be verified against current official Cabo Verde/DNRE sources before being treated as legal requirements.

## Operational Module Coverage

The source lists:

- base entities;
- articles/products/services/assets;
- sales;
- purchases;
- inventory;
- treasury;
- accounting;
- fiscality;
- HR;
- assets;
- projects.

This aligns with the broader module architecture already captured in [[NOVA-ERP Module Priority Map]].

## Security And Audit Signals

The source requires:

- logs of all operations by tenant and user;
- full change history;
- fiscal document hash/IUD;
- fiscal period lock;
- total tenant data isolation.

## AI Direction

AI is phased:

1. SAF-T validation and fiscal error detection.
2. Automatic accounting classification suggestions.
3. Fiscal prediction and intelligent financial assistant.
4. Process automation across purchases, sales and reconciliation.

This reinforces the existing position that AI depends on strong data, permissions, auditability and fiscal correctness.

## Open Questions

- Which fiscal claims in this source are still current under Cabo Verde law and DNRE guidance?
- Should tenant endpoint override be exposed in a platform admin UI during MVP or left as controlled backend configuration?
- Should the dark premium blue/orange direction become a design-system requirement or remain a brand preference?
