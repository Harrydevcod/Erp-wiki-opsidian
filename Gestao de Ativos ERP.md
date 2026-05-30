---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-30
tags: [erp-module, ativos, equipamentos, depreciacao]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Compras e Vendas ERP]]", "[[Tesouraria ERP]]", "[[Projetos ERP]]", "[[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]]"]
related: ["[[NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Compras e Vendas ERP]]", "[[Tesouraria ERP]]", "[[Projetos ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]"]
confidence: medium
schema_decision: "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]"
---

# Gestao de Ativos ERP

## Purpose

Gestao de Ativos ERP is the fixed assets and equipment lifecycle module for [[NOVA-ERP]], covering acquisition, registration, depreciation, transfers, conservation, revaluation, disposal, insurance and accounting evidence.

## Role In NOVA-ERP

Assets sit downstream from purchases and upstream from accounting. A purchase may become an asset; an asset then generates depreciation, maintenance history, location/responsibility changes, revaluation or disposal events that may affect accounting and management reports.

Asset management should not be a static equipment list. It needs controlled lifecycle events, valuation history, depreciation plans, audit trails and clear separation from inventory stock. Inventory tracks consumable or saleable stock; fixed assets track long-lived company property and accounting value.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Contabilidade ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- ERP workflow reference: [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]] (ingested; PT Mapas Fiscais not authority)
- Accounting boundary: [[Contabilidade ERP]]
- Purchase/payment boundary: [[Compras e Vendas ERP]], [[Tesouraria ERP]]
- Project/cost allocation boundary: [[Projetos ERP]]

## Design Gates Before Implementation

- Legal/fiscal gate: verify Cabo Verde depreciation, revaluation, disposal and reporting rules before implementing statutory treatment.
- Acquisition gate: define when a purchase line can create an asset record and when manual capitalization is required.
- Depreciation gate: define methods, useful life, rates, start date, residual value, pause/recalculation and accounting posting rules.
- Accounting gate: define acquisition, depreciation, impairment/revaluation, transfer and disposal source events before ledger integration.
- Lifecycle gate: define controlled state transitions for registration, active use, suspended use, disposed and written-off assets.
- Security gate: define permissions for asset creation, valuation changes, depreciation run, revaluation and disposal.
- Inventory boundary gate: decide how stocked equipment or items become fixed assets without mixing stock balances with asset register.

## Core Workflows

- Register fixed assets and equipment.
- Link acquisition evidence to purchase, supplier or accounting records where applicable.
- Configure asset categories, depreciation policies and useful-life assumptions.
- Generate depreciation schedules and depreciation runs.
- Transfer assets between locations, departments, cost centers or responsible users.
- Record maintenance/conservation, insurance and documentation.
- Revalue, impair, dispose or write off assets through controlled flows.
- Produce asset register, depreciation and lifecycle reports.
- Provide accounting evidence for acquisition, depreciation, revaluation and disposal.

## Required Master Data

- Asset categories/classes.
- Depreciation methods and policies.
- Useful-life and residual-value rules.
- Asset locations.
- Departments, cost centers or projects.
- Responsible users or custodians.
- Suppliers and acquisition documents.
- Insurance policies or references where needed.
- Maintenance/conservation categories.
- Disposal reasons.

## Candidate Domain Model

The schema boundary is now filed in [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]. That ADR keeps fixed assets separate from inventory, makes capitalization explicit, and turns depreciation/revaluation/disposal into approved lifecycle events consumed by accounting posting rules.

- `asset_categories`: class, default depreciation policy, accounting mapping and reporting group.
- `fixed_assets`: tenant-owned asset header, code, name, category, status, acquisition date, capitalization date, original cost, residual value and current book value.
- `asset_components`: optional componentization for assets with separately depreciable parts.
- `asset_acquisitions`: source purchase/accounting evidence, supplier, document, amount and capitalization decision.
- `asset_locations`: physical or organizational locations.
- `asset_custodians`: responsible user/department history.
- `asset_depreciation_policies`: method, useful life, rate, residual value and effective dates.
- `asset_depreciation_schedules`: planned depreciation periods and amounts.
- `asset_depreciation_runs`: execution batch, period, status and accounting linkage.
- `asset_depreciation_lines`: per-asset depreciation result.
- `asset_transfers`: movement between locations, custodians, departments, projects or cost centers.
- `asset_maintenance_events`: conservation/maintenance/repair history and cost links.
- `asset_revaluations`: revaluation, impairment or value adjustment with reason and evidence.
- `asset_disposals`: sale, scrapping, loss, write-off or transfer-out evidence.
- `asset_accounting_events`: source events prepared for accounting posting.

This is provisional until asset and accounting sources are deeply ingested.

## Candidate State Machine

### Asset State

- `draft`: asset record prepared but not capitalized.
- `capitalized`: recognized as fixed asset and ready for depreciation policy.
- `active`: in use and depreciating as applicable.
- `suspended`: temporarily not depreciating or out of service by policy.
- `transferred`: moved to another location/custodian while remaining active.
- `disposed`: sold, scrapped, lost or otherwise removed from service.
- `written_off`: removed through loss/write-off process.

### Depreciation Run State

- `draft`: run prepared.
- `calculated`: depreciation lines generated.
- `pending_review`: requires review/approval.
- `approved`: ready for accounting posting.
- `posted`: accounting evidence generated or linked.
- `reversed`: neutralized through controlled reversal.

## Acquisition Boundary

[[Compras e Vendas ERP]] and supplier documents may originate acquisition evidence, but the asset module owns capitalization.

Rules to preserve:

- a purchase line is not automatically a fixed asset unless capitalization rules or user action say so;
- acquisition evidence should preserve supplier document, cost, date and tax/accounting context;
- later edits to purchase documents should not silently mutate capitalized asset values;
- acquisition corrections require explicit adjustment/revaluation or controlled reversal.

## Accounting Boundary

[[Contabilidade ERP]] owns ledger posting. Assets provide source events such as:

- asset capitalized;
- depreciation calculated/approved;
- asset transferred where accounting dimensions change;
- revaluation or impairment approved;
- asset disposed or written off;
- disposal gain/loss source evidence.

Accounting should post from approved asset events, not from direct edits to asset master fields.

## Treasury Boundary

[[Tesouraria ERP]] controls payment to suppliers or proceeds from disposal. Asset management may link to:

- acquisition payment status;
- maintenance payment evidence;
- sale/disposal receipt evidence.

Asset ownership/value should not depend on a manually edited payment flag.

## Project And Cost Allocation Boundary

[[Projetos ERP]] may consume depreciation, equipment usage or maintenance cost allocation when project costing requires it. This should remain optional until project and accounting dimensions are finalized.

## Audit, Security And Tenancy

- Asset records must be tenant-scoped.
- Capitalization, depreciation policy changes, revaluation, impairment, disposal and write-off require explicit permission.
- Depreciation runs and disposal events should preserve before/after values and source evidence.
- Asset register history should be append-friendly: lifecycle events should not be erased.
- Attachments such as invoices, insurance files, photos or maintenance reports should use private storage policies.
- Closed accounting periods should prevent silent retroactive changes to depreciation or disposal events.

## Critical Domain Events

- `asset.created`
- `asset.capitalized`
- `asset.acquisition_linked`
- `asset.depreciation_policy_changed`
- `asset.depreciation_run_calculated`
- `asset.depreciation_run_approved`
- `asset.depreciation_posted`
- `asset.transferred`
- `asset.maintenance_recorded`
- `asset.revalued`
- `asset.impaired`
- `asset.disposed`
- `asset.written_off`

## Cabo Verde Compliance Notes

Current wiki evidence for assets is mostly product intent and ERP workflow reference. Tax treatment of depreciation, revaluation, impairment, asset disposal, deductible limits or statutory reporting in Cabo Verde requires authoritative legal/fiscal verification before production implementation.

Implementation caution:

- do not hard-code depreciation rates from memory;
- distinguish management depreciation from statutory/tax depreciation if both become necessary;
- disposal may have fiscal/accounting consequences and should be verified before automation;
- SAF-T/accounting export impact remains unresolved until current requirements are ingested.

## MVP Acceptance Criteria

For the first sellable release, assets are acceptable only if scope is explicit:

- If assets are not MVP, purchases/accounting should still preserve enough source evidence for later capitalization.
- If base assets are MVP, asset records are tenant-scoped and permissioned.
- Asset acquisition links preserve source document evidence.
- Depreciation policies are explicit and versioned.
- Depreciation runs are auditable and reviewable before posting.
- Revaluation/disposal/write-off are controlled events, not silent field edits.
- Accounting integration uses approved asset events.
- Statutory/tax depreciation claims are not made without current Cabo Verde source ingestion.

## Non-MVP Until Confirmed

- Full statutory fixed-asset tax automation.
- Complex component depreciation.
- Maintenance scheduling and work orders.
- Barcode/RFID asset tracking.
- Insurance claim workflows.
- Automated project equipment costing.
- Multi-country asset regimes.

## Open Questions

- Which depreciation methods and statutory/tax rules are required for Cabo Verde companies?
- Should asset management ship before or after full accounting?
- Should purchase documents create draft assets automatically or require manual capitalization?
- Should depreciation post monthly, yearly or by configurable period?
- Should project/cost-center allocation be mandatory for assets?
- What reports are required: asset register, depreciation map, disposal report, insurance list?

## Next Ingestion Targets

- ~~FPG006 — Using — Gestão de Equipamentos e Ativos~~ — **ingested** as [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]].
- Current Cabo Verde legal/accounting sources for fixed asset depreciation, revaluation and disposal (esp. the Portaria 42/2015 **per-class rate annex**, still uncaptured).
- SAF-T CV official/current source set if asset data is required for exports.
