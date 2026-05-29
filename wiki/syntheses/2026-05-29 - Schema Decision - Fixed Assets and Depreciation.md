---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, fixed-assets, depreciation, accounting, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]"]
related: ["[[NOVA-ERP]]", "[[Gestao de Ativos ERP]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[Projetos ERP]]", "[[Fiscalidade Cabo Verde]]"]
confidence: medium
---

# Schema Decision - Fixed Assets and Depreciation

## Decision

NOVA-ERP models fixed assets as a lifecycle register separate from inventory. Purchases may create acquisition evidence, but capitalization is an explicit asset decision. Asset value changes are represented by versioned lifecycle events: acquisition, capitalization, depreciation policy assignment, depreciation runs, transfers, maintenance, revaluation/impairment, disposal and write-off. Approved asset events feed accounting posting rules; accounting never posts from mutable asset master fields.

## Scope

- Module: [[Gestao de Ativos ERP]].
- Tables/objects: `asset_categories`, `fixed_assets`, `asset_components`, `asset_acquisitions`, `asset_depreciation_policies`, `asset_depreciation_schedules`, `asset_depreciation_runs`, `asset_depreciation_lines`, `asset_transfers`, `asset_maintenance_events`, `asset_revaluations`, `asset_disposals`, `asset_accounting_events`.
- Workflows affected: asset registration, acquisition linkage, capitalization, depreciation calculation, transfer, maintenance, revaluation, impairment, disposal, write-off and accounting integration.
- Tenancy boundary: all rows carry `tenant_id`; sensitive valuation/disposal actions require asset/accounting permissions and audit.

## Source Basis

- Product source: PRD requires fixed asset/equipment lifecycle, acquisition, depreciation criteria, plans, classes, revaluation, maintenance, disposal, write-off, casualty/loss, legal maps and accounting integration.
- Product source: SSD requires parametrizable depreciation plans, complete lifecycle history and accounting integration.
- Backlog source: asset record must include type, classification, account, depreciation criteria, asset state and lifecycle history; depreciation calculation must follow configured plan and be auditable.
- Compliance source: current Cabo Verde depreciation/tax/legal map requirements are not yet ingested, so statutory treatment remains unresolved.
- Technical source: assets inherit tenant/RLS/audit foundation and post to accounting through approved source events.

## Context

The current database snapshot has product inventory but no fixed-asset register. Inventory and assets must remain separate: inventory tracks stock for sale/consumption; assets track long-lived company property and book value. This ADR defines how assets connect to purchases and accounting without letting purchase edits or asset field edits silently change the ledger.

## Data Model

- Entity/table: `asset_categories`
  - Key fields: `id`, `tenant_id`, `code`, `name`, `default_policy_id`, `asset_account_id`, `depreciation_expense_account_id`, `accumulated_depreciation_account_id`, `status`.
  - Purpose: category-level defaults and accounting mapping.

- Entity/table: `fixed_assets`
  - Key fields: `id`, `tenant_id`, `asset_no`, `name`, `category_id`, `status` (`draft|capitalized|active|suspended|disposed|written_off`), `acquisition_date`, `capitalization_date`, `original_cost`, `residual_value`, `current_book_value`, `location_id`, `custodian_ref`.
  - Constraints: unique asset number per tenant; current book value is derived/projection-friendly from approved events, not casually edited.

- Entity/table: `asset_components`
  - Key fields: `id`, `tenant_id`, `asset_id`, `name`, `cost`, `policy_id`, `status`.
  - Scope: optional componentization, schema-ready but not required for MVP.

- Entity/table: `asset_acquisitions`
  - Key fields: `id`, `tenant_id`, `asset_id`, `source_kind` (`purchase_document|manual|opening_balance`), `source_ref`, `supplier_entity_id`, `amount`, `tax_amount`, `capitalization_decision`, `evidence_ref`.
  - Relationship: links to commercial/fiscal purchase evidence where applicable.

- Entity/table: `asset_depreciation_policies`
  - Key fields: `id`, `tenant_id`, `code`, `method` (`straight_line|manual|other`), `useful_life_months`, `rate`, `residual_value_rule`, `start_rule`, `effective_from`, `effective_to`, `legal_source_ref`, `status`.
  - Constraints: statutory/tax policies require source references before production claims.

- Entity/table: `asset_depreciation_schedules`
  - Key fields: `id`, `tenant_id`, `asset_id`, `policy_id`, `period_id`, `planned_amount`, `opening_book_value`, `closing_book_value`, `status`.
  - Purpose: planned depreciation by period.

- Entity/table: `asset_depreciation_runs`
  - Key fields: `id`, `tenant_id`, `period_id`, `status` (`draft|calculated|pending_review|approved|posted|reversed`), `scope`, `created_by`, `approved_by`, `approved_at`.
  - Constraints: approved/posted runs are immutable; corrections use reversal or adjustment events.

- Entity/table: `asset_depreciation_lines`
  - Key fields: `id`, `tenant_id`, `run_id`, `asset_id`, `period_id`, `depreciation_amount`, `opening_book_value`, `closing_book_value`, `policy_snapshot_json`, `status`.
  - Relationship: source evidence for accounting events.

- Entity/table: `asset_transfers`
  - Key fields: `id`, `tenant_id`, `asset_id`, `from_location_id`, `to_location_id`, `from_custodian_ref`, `to_custodian_ref`, `effective_date`, `reason`, `status`.

- Entity/table: `asset_maintenance_events`
  - Key fields: `id`, `tenant_id`, `asset_id`, `event_date`, `kind`, `description`, `cost_source_ref`, `evidence_ref`, `status`.

- Entity/table: `asset_revaluations`
  - Key fields: `id`, `tenant_id`, `asset_id`, `event_date`, `kind` (`revaluation|impairment|adjustment`), `amount_delta`, `new_book_value`, `reason`, `evidence_ref`, `status`.

- Entity/table: `asset_disposals`
  - Key fields: `id`, `tenant_id`, `asset_id`, `event_date`, `kind` (`sale|scrap|loss|write_off|transfer_out`), `proceeds_amount`, `buyer_entity_id`, `evidence_ref`, `status`.

- Entity/table: `asset_accounting_events`
  - Key fields: `id`, `tenant_id`, `asset_id`, `event_type` (`asset_capitalized|asset_depreciated|asset_revalued|asset_disposed|asset_written_off|asset_reversed`), `source_ref`, `status`, `journal_entry_id`.
  - Relationship: consumed by accounting posting rules.

## State And Events

- State: `fixed_assets.status`: `draft -> capitalized -> active`; branches include `suspended`, `disposed`, `written_off`.
- State: `asset_depreciation_runs.status`: `draft -> calculated -> pending_review -> approved -> posted`; correction path is `reversed`.
- Events: `asset.created`, `asset.capitalized`, `asset.acquisition_linked`, `asset.depreciation_policy_changed`, `asset.depreciation_run_calculated`, `asset.depreciation_run_approved`, `asset.depreciation_posted`, `asset.transferred`, `asset.maintenance_recorded`, `asset.revalued`, `asset.impaired`, `asset.disposed`, `asset.written_off`.
- Transition rule: depreciation, revaluation, disposal and write-off require approved lifecycle events; master-field edits do not change accounting.

## Accounting, Purchase And Treasury Boundary

Purchases provide source evidence, but the asset module owns capitalization. Once capitalized, later source-document corrections require explicit asset adjustment/reversal rather than silent mutation.

Assets do not write ledger lines directly. Approved asset accounting events are consumed by [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] posting rules for acquisition/capitalization, depreciation, revaluation/impairment and disposal gain/loss.

Treasury owns supplier payment and disposal proceeds settlement. Asset state should not depend on manually edited payment flags.

## Alternatives Considered

- Alternative: treat fixed assets as inventory products with an extra flag.
  Why not: stock quantity and asset lifecycle/book value are different accounting domains.
- Alternative: auto-capitalize every qualifying purchase line.
  Why not: capitalization requires policy, account, useful life and sometimes human judgment.
- Alternative: store depreciation as editable monthly fields.
  Why not: breaks auditability and accounting integration; runs/lines preserve reproducible calculations.
- Alternative: hard-code statutory depreciation rates now.
  Why not: current Cabo Verde legal/tax rules are not ingested.

## Consequences

- Positive: clean separation from inventory, auditable asset lifecycle and controlled accounting source events.
- Positive: purchase integration is possible without making purchasing the owner of asset value.
- Tradeoff: requires category/policy setup before depreciation is useful.
- Migration impact: no current fixed-asset tables in the snapshot; this is new-build schema.
- Operational impact: depreciation runs need review, period discipline and handling for closed accounting periods.

## Validation Plan

- Test: tenant A cannot access tenant B asset records, depreciation lines or disposal evidence.
- Test: a purchase link does not create a capitalized asset without explicit capitalization.
- Test: depreciation lines are generated from the active policy snapshot and cannot be edited after approval.
- Test: posted depreciation cannot be changed; reversal creates neutralizing evidence.
- Test: disposal blocks future depreciation for the asset.
- Test: accounting events generated from approved depreciation/disposal produce balanced draft entries.
- Test: closed accounting periods block retroactive depreciation posting unless reopened through accounting controls.

## Open Questions

- Which Cabo Verde depreciation methods, useful-life rules and tax limits must ship?
- Are assets in first sellable release, or only source-ready for later capitalization?
- Should purchase documents create draft assets automatically or require manual creation?
- Should depreciation run monthly, yearly or by configurable accounting period?
- Are legal asset maps required for first release?
- Should project/cost-center allocation be mandatory for asset depreciation?

## Maintenance Notes

- Update after fixed-asset/Cabo Verde legal source ingestion and actual Supabase migrations/RLS inspection.
- Depends on tenant foundation, document core and accounting ADRs; may feed [[Projetos ERP]] if depreciation/cost allocation by project becomes mandatory.
