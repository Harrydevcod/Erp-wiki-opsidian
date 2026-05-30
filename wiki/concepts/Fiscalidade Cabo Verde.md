---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [fiscalidade, cabo-verde, iva, compliance]
sources: ["[[2026-05-29 - Codigo do IVA Cabo Verde]]", "[[2014-12-31 - Lei 78-2014 Codigo do IRPS]]", "[[2015-01-07 - Lei 82-2015 Codigo do IRPC]]", "[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]", "[[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]]", "[[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]]", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]", "[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf", "raw/assets/SSD/PRD.MD"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[SAF-T CV]]", "[[ERP SaaS Multi-Tenant]]", "[[DNRE]]", "[[2026-05-29 - Codigo do IVA Cabo Verde]]"]
confidence: medium
---

# Fiscalidade Cabo Verde

## Definition

Fiscalidade Cabo Verde, in this wiki, means the legal and operational tax requirements an ERP must support for companies operating in Cabo Verde, especially IVA, invoice rules, fiscal declarations, electronic invoice flows, SAF-T CV reporting, fiscal auditability and tenant-scoped compliance configuration.

## Current Synthesis

[[NOVA-ERP]] must treat fiscality as a product core, not as a later reporting module. Fiscal rules affect document creation, numbering, tax calculation, document correction, immutability, audit history, e-Fatura communication, SAF-T readiness, treasury/accounting links and tenant configuration.

The working model is:

- fiscal substance comes from current Cabo Verde law, IVA/CIVA/REMPE rules, invoice rules and DNRE guidance;
- electronic fiscal-document implementation comes from modern e-Fatura technical authority, especially [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] and [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]];
- older fiscal guides such as [[2026-05-28 - Manual de Faturas em Cabo Verde]] remain useful for invoice-rule substance, but not as the final implementation contract for DFE/XML/API behavior;
- legacy ERP material such as Cegid Primavera is workflow reference, not architecture authority;
- current database artifacts such as [[2026-05-28 - DATABASE ER Diagram Snapshot]] are implementation evidence, not fiscal target schema.

Source: [[2026-05-28 - Manual de Faturas em Cabo Verde]], [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Current Database Snapshot Classification]]

## Fiscal Rule Layer

[[2026-05-28 - Manual de Faturas em Cabo Verde]] provides the current wiki's practical invoice-rule map:

- invoices are tied to goods/services, advance payments and changes in taxable value;
- required fields include party identity/NIF, goods/services, taxable value, IVA rate/amount, non-taxation justification and series;
- numbering must be sequential, chronological, non-repeating and non-deletable;
- rectification documents must reference the original invoice and altered mentions;
- special rule areas include REMPE, public works/State invoicing, reverse charge, transport documents and electronic invoice storage.

[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] classifies this 2018 material: fiscal substance largely survives, but paper-era/electronic-invoice processing mechanics are superseded or narrowed by modern e-Fatura.

## e-Fatura Technical Layer

The current e-Fatura technical contract adds implementation constraints that normal invoice-rule summaries do not cover:

- DFE XML and XSD validation;
- namespace `urn:cv:efatura:xsd:v1.0`;
- IUD, LED, repository code and document type code;
- digital signature with XMLDSig/XAdES-BES;
- synchronous PE authorization attempt after submission;
- Deflate ZIP multipart DFE submission;
- OAuth/PKCE and middleware headers;
- official DFE type vocabulary;
- `IssueReasonCode`, `RappelPeriod`, `SelfBilling`, contingency, references and DTE route rules.
- official event payloads for `FDC` cancellation/anulation and `UDN` unused-number inutilization.

Implementation implication: NOVA-ERP cannot model e-Fatura as a string status on an invoice. It needs fiscal snapshots, DFE payloads, XSD validation results, signed XML storage references, transmission batches/attempts, references, contingency records, self-billing authorizations, correction/rappel structures and event payloads for cancellation/anulation/inutilization. The first DFE payload boundary is filed in [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]; event payloads are filed in [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]].

Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[Faturacao Eletronica]], [[e-Fatura Cabo Verde]]

## Data Model Boundary

[[2026-05-28 - Current Database Snapshot Classification]] makes the fiscal schema boundary explicit:

- current `documents`, `document_items` and `document_series` can inform the target fiscal document model, but require heavy refactoring;
- current `efatura_settings`, `efatura_logs` and `efatura-certificates` should be replaced or split into implementation-grade e-Fatura objects;
- current e-commerce/POS tables should not shape the fiscal core;
- target fiscal tables must be tenant-scoped, protected by RLS, auditable and aligned with official DFE schema/API contracts.

This turns the database contradiction into a concrete fiscal rule: no production fiscal implementation should reuse the current document/e-Fatura tables without SQL, RLS, storage and migration review.

Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]], [[2026-05-28 - Current Database Snapshot Classification]], [[Contradiction - Current Database Snapshot vs Target ERP Architecture]]

## Operational Territory

The Cegid Primavera fiscality materials show expected ERP workflow territory:

- invoice emission;
- IVA Modelo 106;
- regularization annexes;
- credit note scenarios;
- SAF-T CV accounting/inventory files;
- accounting/fiscal integration.

Use this as process reference only. NOVA-ERP should translate these workflows into modern tenant-scoped, audit-first, API-first product design.

## Implementation Implications

- Product: fiscal UX must prevent invalid finalization before tax, series, document type, customer/NIF and tenant configuration are valid.
- Architecture: fiscality crosses sales, purchases, inventory, treasury, accounting, SAF-T and e-Fatura; it cannot live in a single isolated "tax report" module.
- Data model: fiscal documents need immutable snapshots, explicit correction references, tax breakdowns, fiscal numbering events and technical e-Fatura state.
- Security/audit: issuing, correcting, cancelling, reprocessing, exporting and configuring fiscal credentials require separate permissions and immutable logs.
- Compliance: old source claims must be marked as background until checked against current law and official DNRE/e-Fatura sources.

## Evidence

- Source: [[2026-05-29 - Codigo do IVA Cabo Verde]]
- Source: [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]
- Source: [[2026-05-28 - Manual de Faturas em Cabo Verde]]
- Source: [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]
- Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]
- Source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]
- Source: [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]
- Source: [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]
- Source: [[2026-05-28 - Current Database Snapshot Classification]]
- Evidence: `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
- Evidence: `raw/assets/SSD/PRD.MD`

## Uncertainty Register

- Legal currency: current CIVA/IVA/REMPE rules still need authoritative legal ingestion before production compliance claims.
- Public works/State invoicing: still unresolved after the 2018 manual classification.
- Reverse charge: current legal basis must be verified before implementation.
- Penalties/sanctions: older orientative source is not sufficient for production behavior.
- e-Fatura event legality: the technical event schema for `FDC` and `UDN` is captured, but current legal rules and product scope still need verification before production cancellation/anulation/inutilization workflows.
- Database reuse: actual SQL/RLS/storage policies behind the current ER snapshot must be inspected before reuse decisions.

## Related Pages

- [[e-Fatura Cabo Verde]]
- [[Faturacao Eletronica]]
- [[SAF-T CV]]
- [[NOVA-ERP]]
- [[ERP SaaS Multi-Tenant]]
- [[DNRE]]

## Open Questions

- Which IVA rules have changed since the included sources were published?
- What is mandatory for first production release versus later compliance depth?
- Which current CIVA/REMPE provisions should be ingested next to replace old orientative claims?
- Which current legal texts govern public works/State invoicing and reverse charge?
- Should `FDC` and `UDN` ship in MVP, or should MVP only preserve the schema boundary for them?
