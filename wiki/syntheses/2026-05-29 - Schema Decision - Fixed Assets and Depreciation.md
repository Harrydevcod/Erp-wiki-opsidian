---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-30
decision_status: provisional
tags: [schema, architecture, fixed-assets, depreciation, accounting, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]", "[[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]"]
related: ["[[NOVA-ERP]]", "[[Gestao de Ativos ERP]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[Projetos ERP]]", "[[Fiscalidade Cabo Verde]]"]
confidence: medium
---

# Schema Decision - Fixed Assets and Depreciation

## Decision

NOVA-ERP models fixed assets as a lifecycle register separate from inventory. Purchases may create acquisition evidence, but capitalization is an explicit asset decision. Asset value changes are represented by versioned lifecycle events: acquisition, capitalization, depreciation policy assignment, depreciation runs, transfers, maintenance, revaluation/impairment, disposal and write-off. Approved asset events feed accounting posting rules; accounting never posts from mutable asset master fields.

## Scope

- Module: [[Gestao de Ativos ERP]].
- Tables/objects: `asset_categories`, `fixed_assets`, `asset_components`, `asset_acquisitions`, `asset_depreciation_plans`, `asset_depreciation_policies`, `asset_depreciation_schedules`, `asset_depreciation_runs`, `asset_depreciation_lines`, `asset_extraordinary_depreciations`, `asset_transfers`, `asset_maintenance_events`, `asset_revaluations`, `asset_disposals`, `asset_accounting_events`; optional `asset_insurance_policies`.
- Workflows affected: asset registration, acquisition linkage, capitalization, depreciation calculation, transfer, maintenance, revaluation, impairment, disposal, write-off and accounting integration.
- Tenancy boundary: all rows carry `tenant_id`; sensitive valuation/disposal actions require asset/accounting permissions and audit.

## Source Basis

- Product source: PRD requires fixed asset/equipment lifecycle, acquisition, depreciation criteria, plans, classes, revaluation, maintenance, disposal, write-off, casualty/loss, legal maps and accounting integration.
- Product source: SSD requires parametrizable depreciation plans, complete lifecycle history and accounting integration.
- Backlog source: asset record must include type, classification, account, depreciation criteria, asset state and lifecycle history; depreciation calculation must follow configured plan and be auditable.
- Compliance source: the full primary regulation is captured in [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] (20 articles, in force for tax periods from 1 Jan 2015, under IRPC art. 43º nº5), and the **per-asset-class rate annex is now captured** in [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] (310 rows, Tabela I sector-specific + Tabela II generic; `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv`). Note: this primary text **revokes Portaria 2/84** (art. 19º), correcting the earlier secondary note in [[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]].
- Technical source: assets inherit tenant/RLS/audit foundation and post to accounting through approved source events.
- Legacy workflow reference: [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]] — corroborates the inventory-separate register, the document-per-event (`Alteração`) lifecycle, straight-line/declining-balance with ×1.5/×2/×2.5 coefficients, capitalization at full operational cost, and disposal types (alienação/abate/sinistro). It confirms **parallel accounting + fiscal depreciation plans**, configurable periodicity (anual/duodecimal/diária), and cost-center allocation via Repartições; and supplies extraordinary depreciation, impairment (loss+reversal), revaluation (market-value/replacement-cost), decomposition/copy, conservation and excess-amortization-on-disposal. PT Mapas Fiscais are not authority here.

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

- Entity/table: `asset_depreciation_plans` (legacy *Planos de Depreciação*)
  - Key fields: `id`, `tenant_id`, `code`, `plan_kind` (`fiscal|accounting|ias|other`), `currency`, `integrates_to_accounting` (bool), `is_default`, `status`.
  - Rationale: an asset carries **parallel** depreciation schedules — a `fiscal` plan (Portaria 42/2015 limits) and optionally an `accounting`/IAS plan — each with its own policies/schedules/runs; only the configured plan integrates to a given accounting or fiscal map. Resolves the "track tax and accounting depreciation as separate schedules?" open question as **yes, plan-scoped**. Legacy-sourced from [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]].
  - MVP note: the first release may ship only the `fiscal` plan; the `accounting` plan is schema-ready.

- Entity/table: `asset_depreciation_policies`
  - Key fields: `id`, `tenant_id`, `plan_id` (fk `asset_depreciation_plans`), `code`, `method` (`straight_line|declining_balance|low_value_expense|manual|other`), `periodicity` (`annual|duodecimal|daily`), `useful_life_months`, `rate`, `rate_mode` (`max|min|variable|zero` — legacy taxa máxima / mínima=máx÷2 / variável / zero), `residual_value_rule`, `start_rule`, `cost_cap`, `acquisition_date_rule`, `effective_from`, `effective_to`, `legal_source_ref`, `status`.
  - Constraints: statutory/tax policies require source references before production claims. Per [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]: default `straight_line` (quotas constantes); `declining_balance` (degressivas) optional with coefficient **×1.5 / ×2 / ×2.5** by useful life (<5y / 5–6y / >6y), excluded for used assets, buildings, light/mixed vehicles, furniture and social equipment, and only for assets in service from 2015-01-01 (art. 18º); `low_value_expense` for unit cost ≤ 20,000$ (single-period write-off, art. 15º); `cost_cap` = 4,000,000$ for light vehicles/boats/aircraft (art. 10º); minimum quota = **half** the rate (art. 14º); multi-shift uplift +25%/+50% (art. 7º). Rates seed from the Portaria 42/2015 annex — **now captured** in [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] (e.g. edifícios habitacionais 3%, industriais 5%, veículos ligeiros 14,28% (7 yr), pesados 20%, mobiliário 12,5%, computadores/intangível 33,33%); tenant picks the Tabela I sector rate when activity matches, else the Tabela II generic rate. Fiscal add-on: light-vehicle/moto charges (incl. depreciations) carry **10% tributação autónoma** under [[2015-01-07 - Lei 82-2015 Codigo do IRPC]] art. 89º — a posting consequence beyond the depreciation cap.
  - Real-estate rule: depreciate **construction value only, not land**; when land value is not stated, attribute **25% of global value** to land (art. 3º). Capitalize non-deductible IVA into the asset base. Intangibles: development-project and limited-life industrial property amortizable; **goodwill (trespasses) not amortizable** by default (art. 13º). Financial leasing: the **lessee** depreciates (art. 11º).

- Entity/table: `asset_depreciation_schedules`
  - Key fields: `id`, `tenant_id`, `asset_id`, `plan_id`, `policy_id`, `period_id`, `planned_amount`, `opening_book_value`, `closing_book_value`, `status`.
  - Purpose: planned depreciation by period, **per plan** (an asset has one schedule per active plan, e.g. fiscal and accounting).

- Entity/table: `asset_depreciation_runs`
  - Key fields: `id`, `tenant_id`, `period_id`, `status` (`draft|calculated|pending_review|approved|posted|reversed`), `scope`, `created_by`, `approved_by`, `approved_at`.
  - Constraints: approved/posted runs are immutable; corrections use reversal or adjustment events.

- Entity/table: `asset_depreciation_lines`
  - Key fields: `id`, `tenant_id`, `run_id`, `asset_id`, `plan_id`, `period_id`, `depreciation_amount`, `accepted_amount`, `lost_amount` (legacy *taxa perdida* = min−used on the fiscal plan), `opening_book_value`, `closing_book_value`, `policy_snapshot_json`, `status`.
  - Relationship: source evidence for accounting events. On the `fiscal` plan, the split between `accepted_amount` (aceite fiscal) and `lost_amount` (não aceite / perdida) feeds the tax map.

- Entity/table: `asset_extraordinary_depreciations` (legacy *Depreciação Extraordinária*)
  - Key fields: `id`, `tenant_id`, `asset_id`, `plan_id`, `period_id`, `amount`, `reason`, `evidence_ref`, `status`.
  - Rationale: extra depreciation outside the normal schedule, processed separately and posted to its own accounts; distinguishable from ordinary depreciation in the asset extrato.

- Entity/table: `asset_transfers`
  - Key fields: `id`, `tenant_id`, `asset_id`, `from_location_id`, `to_location_id`, `from_custodian_ref`, `to_custodian_ref`, `effective_date`, `reason`, `status`.

- Entity/table: `asset_maintenance_events`
  - Key fields: `id`, `tenant_id`, `asset_id`, `event_date`, `kind`, `description`, `cost_source_ref`, `evidence_ref`, `status`.

- Entity/table: `asset_revaluations`
  - Key fields: `id`, `tenant_id`, `asset_id`, `plan_id`, `event_date`, `kind` (`revaluation_market_value|revaluation_replacement_cost|impairment_loss|impairment_reversal|adjustment`), `amount_delta`, `new_book_value`, `reason`, `evidence_ref`, `status`.
  - Legacy-sourced kinds: market-value vs replacement-cost revaluation (justo valor, producing a revaluation excedente) and impairment loss vs reversal — reversal is **capped** at the value the asset would have had without the original impairment.

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

On **disposal** (alienação/abate/sinistro), depreciation already taken in periods beyond the disposal date (under duodecimal/annual periodicity) must be **corrected back** as part of the disposal posting, and gain/loss = net proceeds − net book value; this is a posting rule, not a status change (legacy-validated). Cost-center/function allocation of depreciation (legacy **Repartições**, Fixa/Variável) is optional and expressed by tagging asset depreciation lines with values from [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]] — not a separate mandatory mechanism.

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

- Resolved (primary law): methods, coefficients, low-value/vehicle/min-quota/multi-shift/real-estate/intangibles/leasing rules are captured from [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]], and the per-asset-class **rate/useful-life annex** is now captured in [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] (310 rows). Still open: whether later OE laws changed the 20,000$/4,000,000$ thresholds, and verification of the heuristically de-wrapped CSV designations against the PDF before legal display.
- Resolved (legacy-validated by [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]]): tax and accounting depreciation are tracked as **separate plan-scoped schedules** (`asset_depreciation_plans.plan_kind`); depreciation periodicity is **configurable** (annual/duodecimal/daily); project/cost-center allocation is **optional via Repartições** mapped to analytical dimensions, not mandatory.
- How many depreciation plans ship in MVP — just `fiscal` (Portaria 42/2015), or `accounting` + `fiscal` from day one?
- Are impairment and free/extraordinary revaluation (IAS) in MVP scope, or deferred after statutory straight-line depreciation?
- Is the criteria-inheritance hierarchy (class/fiscal-classification config with cascade) worth building, or is per-asset policy enough for the first release?
- Are assets in first sellable release, or only source-ready for later capitalization?
- Should purchase documents create draft assets automatically or require manual creation?
- Are legal asset maps required for first release?

## Maintenance Notes

- Update after fixed-asset/Cabo Verde legal source ingestion and actual Supabase migrations/RLS inspection.
- Depends on tenant foundation, document core and accounting ADRs; may feed [[Projetos ERP]] if depreciation/cost allocation by project becomes mandatory.
