---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, contabilidade, fiscalidade, cabo-verde]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]]", "[[2026-05-29 - Codigo do IVA Cabo Verde]]", "docs/docsfiscal/FPG032 - Configuring - Financeira (2022-v1.0-PT).pdf"]
related: ["[[NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[SAF-T CV]]", "[[Tesouraria ERP]]", "[[Inventario ERP]]", "[[Processamento de Salarios ERP]]", "[[Gestao de Ativos ERP]]", "[[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]]"]
confidence: medium
---

# Contabilidade ERP

## Purpose

Contabilidade ERP is the accounting and fiscal ledger layer for NOVA-ERP, responsible for turning operational activity into auditable accounting movements, tax-relevant ledgers, reports and fiscal outputs.

## Role In NOVA-ERP

Accounting should be designed as an integrated consequence of ERP operations, not as an isolated bookkeeping island. Sales, purchases, treasury, inventory, assets and payroll should produce structured events that can become accounting movements with traceability.

For Cabo Verde, accounting also sits downstream from fiscal document integrity. [[Faturacao Eletronica]] and [[Fiscalidade Cabo Verde]] define the fiscal-document evidence; accounting consumes that evidence to support IVA apuramento, reports, SAF-T CV and financial statements. It should not mutate fiscal documents, DFE payloads or e-Fatura authorization evidence.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Fiscalidade Cabo Verde]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Fiscal authority/context: [[Fiscalidade Cabo Verde]], [[Faturacao Eletronica]]
- e-Fatura schema boundary: [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]
- ERP workflow reference: [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]] (ingested; PT fiscal maps not authority)
- Configuration reference (raw): `docs/docsfiscal/FPG032 - Configuring - Financeira (2022-v1.0-PT).pdf`
- Related concepts: [[SAF-T CV]], [[Tesouraria ERP]], [[Inventario ERP]]

## Design Gates Before Implementation

- Source authority gate: ingest the accounting/fiscal Cegid Primavera references and current Cabo Verde accounting/tax sources before final chart/reporting behavior.
- Fiscal boundary gate: decide how issued fiscal-document snapshots become accounting facts without coupling ledger entries to raw e-Fatura XML.
- Data model gate: define chart of accounts, journals, periods, journal entries, entry lines, posting rules, tax accounts and source-document references.
- Security/audit gate: define period locking, reversal, adjustment, approval and audit-log behavior before posting workflows.
- SAF-T gate: confirm which accounting/inventory data structures are required for SAF-T CV before finalizing ledger schema.

## Core Workflows

- Maintain chart of accounts and accounting periods.
- Configure journals, document classes and posting rules.
- Generate accounting movements from operational modules.
- Post sales, purchase, treasury, inventory, payroll and asset events.
- Support IVA apuramento and fiscal maps.
- Support closing/opening routines and period locks.
- Prepare data for SAF-T CV accounting exports.
- Preserve origin references back to operational and fiscal evidence.

## Accounting Boundary With e-Fatura

[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] separates fiscal documents, snapshots, DFE payloads, validation results and transmission attempts. Accounting should consume the fiscal/business evidence, not the technical transport evidence.

Accounting should depend on:

- issued fiscal document identity;
- immutable fiscal snapshot totals and tax breakdowns;
- customer/supplier/entity identity;
- document type and correction relationship;
- issue date/accounting date;
- authorization status where required by product/legal policy;
- payment/settlement events from [[Tesouraria ERP]];
- inventory valuation events where relevant.

Accounting should not depend directly on:

- raw signed XML;
- Deflate ZIP archives;
- middleware headers;
- raw DNRE response bodies;
- certificate secret material;
- retry-attempt internals.

Those remain audit/integration evidence under [[Faturacao Eletronica]] and e-Fatura integration controls.

## Candidate Domain Model

- `accounting_periods`: tenant fiscal/accounting periods, status, open/closed/locked dates.
- `chart_accounts`: tenant chart of accounts, account code, name, class, parent, active state and reporting mapping.
- `journals`: tenant journal definitions for sales, purchases, treasury, inventory, payroll, assets and adjustments.
- `posting_rules`: configurable mapping from source event/document/tax profile to journal entry lines.
- `journal_entries`: accounting header, tenant, journal, period, source module, source entity, posting date, status and audit metadata.
- `journal_entry_lines`: debit/credit lines, account, amount, currency, tax dimension, entity, cost center/project where applicable.
- `tax_posting_profiles`: IVA/REMPE/non-taxed/reverse-charge mapping to accounts and reporting boxes.
- `source_accounting_links`: immutable link between operational/fiscal source records and generated entries.
- `accounting_adjustments`: controlled manual adjustments with reason, approval and audit trail.
- `period_close_events`: close/open/reopen events, actor, reason and affected period.

This is provisional until accounting sources and current legal/reporting requirements are ingested.

## Candidate State Machine

### Journal Entry State

- `draft`: generated or manual entry not posted.
- `pending_review`: requires approval or accountant review.
- `posted`: affects ledger and reports.
- `reversed`: neutralized by a reversal entry.
- `voided`: invalid before posting or under controlled correction path.

### Accounting Period State

- `open`: normal posting allowed.
- `soft_closed`: operational posting restricted, adjustments allowed by permission.
- `closed`: normal posting blocked.
- `locked`: no mutation except controlled reopening process.

## Critical Domain Events

- `accounting.period_opened`
- `accounting.period_soft_closed`
- `accounting.period_closed`
- `accounting.period_reopened`
- `accounting.journal_entry_generated`
- `accounting.journal_entry_posted`
- `accounting.journal_entry_reversed`
- `accounting.posting_rule_changed`
- `accounting.tax_profile_changed`
- `accounting.saft_export_generated`

Events generated by fiscal and operational modules should remain source events; accounting creates derived posting events linked back to them.

## Integration Points

- [[Faturacao Eletronica]] provides issued fiscal-document snapshots, tax breakdowns and correction references.
- [[Tesouraria ERP]] provides receipts, payments, bank and cash movements.
- [[Inventario ERP]] provides stock valuation and movement evidence.
- [[Processamento de Salarios ERP]] provides salary, deduction and employer cost postings.
- [[Gestao de Ativos ERP]] provides acquisition, depreciation, transfer and disposal postings.
- [[SAF-T CV]] consumes accounting and operational data for fiscal audit/export.

## Audit, Security And Tenancy

- Accounting records must be tenant-scoped.
- Posting, reversal, manual adjustment, rule changes and period close/reopen actions should be permissioned separately.
- Generated movements should preserve origin references back to operational documents and fiscal snapshots.
- Period locking should prevent silent mutation of already reported accounting data.
- Manual adjustments require reason, actor, timestamp and preferably approval workflow.
- Posting rules and tax profiles are high-risk configuration and should be auditable.

## Cabo Verde Compliance Notes

The current wiki supports the following caution:

- fiscal documents and e-Fatura evidence are upstream sources for accounting, not casual mutable sales records;
- IVA and SAF-T CV requirements make accounting schema a compliance boundary;
- Cegid Primavera materials are useful workflow references for IVA maps, fiscal regularizations and SAF-T preparation;
- current legal/accounting requirements still need authoritative ingestion before production compliance claims.

Source: [[Fiscalidade Cabo Verde]], [[SAF-T CV]], [[2026-05-26 - SSD NOVA-ERP]]

## MVP Acceptance Criteria

For the first sellable release, accounting is acceptable only if its scope is explicit:

- If full accounting is not MVP, fiscal documents must still preserve enough structured evidence for later posting and SAF-T/accounting migration.
- If base accounting is MVP, journal entries must be tenant-scoped, source-linked, auditable and protected by period state.
- Posting rules must be deterministic and reviewable.
- Accounting entries generated from fiscal documents must reference immutable fiscal snapshots, not editable draft data.
- Period close/lock rules must prevent untracked mutation of reported data.

## Non-MVP Until Confirmed

- Full statutory accounting claim for Cabo Verde without current legal/accounting source ingestion.
- Automatic posting for every module without reviewed posting rules.
- Payroll, assets and inventory valuation posting before those modules are deeply ingested.
- SAF-T accounting export finalization before SAF-T CV requirements are deeply ingested.
- Free-form edits to posted entries without reversal/adjustment audit trail.

## Open Questions

- Should full accounting be part of the MVP or phase two?
- Which accounting events must exist before e-Fatura/SAF-T CV launch?
- What level of accounting configurability is necessary for the first Cabo Verde market release?
- Should base fiscal documents post immediately to accounting, wait for PE authorization, or post on a configurable policy?
- What is the minimum chart of accounts and tax-posting profile for Cabo Verde MVP?

## Next Ingestion Targets

- ~~FPG003 — Using — Contabilidade e Fiscalidade~~ — **ingested** as [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]].
- `docs/docsfiscal/FPG032 - Configuring - Financeira (2022-v1.0-PT).pdf` (optional config detail).
- `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
- ~~SAF-T CV official/current source set~~ — **ingested**: [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]], [[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]], [[SAF-T CV Anexo II - SNCRF Account Taxonomy]].

