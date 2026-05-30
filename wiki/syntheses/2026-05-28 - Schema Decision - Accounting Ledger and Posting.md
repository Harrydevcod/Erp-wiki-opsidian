---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, accounting, ledger, posting, saft, nova-erp]
sources: ["[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]"]
related: ["[[NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Faturacao Eletronica]]", "[[Tesouraria ERP]]", "[[Inventario ERP]]", "[[SAF-T CV]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: medium
---

# Schema Decision - Accounting Ledger and Posting

## Decision

NOVA-ERP models accounting as an **immutable double-entry journal driven by posting rules over upstream domain events**, never hand-keyed from screens that mutate balances. A `journal_entry` is a balanced set of `journal_entry_lines` (debits = credits) carrying a `tenant_id`, a `period_id`, and a `source_ref` back to the originating event (fiscal document snapshot, treasury allocation, or stock valuation movement). Entries are posted, never edited; corrections are reversal entries. Balances, trial balance and ledgers are **projections** over posted lines. `posting_rules` map each upstream event type to a debit/credit template so revenue/tax/COGS/settlement postings are deterministic and auditable. Accounting consumes the *defined outputs* of the three financial-core ADRs — fiscal snapshots, treasury allocations, valuation layers — and **never** reads raw DFE XML, ZIP, middleware headers or certificate material. Period locks block back-dated postings. All tenant-scoped under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]].

## Scope

- Module: [[Contabilidade ERP]].
- Tables/objects: `chart_of_accounts`, `journals`, `accounting_periods`, `journal_entries`, `journal_entry_lines`, `posting_rules`, `tax_maps`, `analytic_dimensions`, `analytic_allocations`; `account_balances`, `trial_balance` as projections.
- Workflows affected: posting from fiscal/treasury/inventory events, manual entries, reversals, period open/close/reopen, trial balance/ledger, SAF-T CV accounting export.
- Tenancy boundary: all rows carry `tenant_id`; RLS per foundation ADR; posting/reversal/period/rule actions gated by `has_permission` keys (`accounting.post`, `accounting.reverse`, `accounting.period_manage`, `accounting.rule_admin`) — already enumerated in [[Permissoes e Auditoria ERP]].

## Source Basis

- Product source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]].
- Compliance source: [[SAF-T CV]] accounting export readiness; Cabo Verde chart-of-accounts (SNCRF, [[SAF-T CV Anexo II - SNCRF Account Taxonomy]]) and IVA maps. Corporate-tax parameters now primary-sourced from [[2015-01-07 - Lei 82-2015 Codigo do IRPC]]: IRPC **25%** (contabilidade organizada) / **4% TEU** (REMPE); **tributação autónoma** 40% (não documentadas) / 10% (viaturas, representação); **fiscal-loss carryforward 7 periods, capped at 50%** of each period's taxable profit (art. 59º); **impairment provisioning 25/50/75/100%** by arrears age (6–24 mo) — encode as `tax_maps`/posting rules and a receivables-provisioning rule. Current legal verification still required for IVA specifics — see [[Fiscalidade Cabo Verde]].
- Technical source: [[2026-05-28 - DATABASE ER Diagram Snapshot]] (no real ledger present — accounting is a new build, not an adapt).
- Inference: the posting-rule-over-events design and projection-based balances are architecture inferences grounded in standard double-entry practice.
- Legacy workflow reference: [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]] corroborates the spine — chart hierarchy with movement-only posting, posting by integration of upstream module events vs manual direct entries, periodic IVA apuramento, period open/close with year-end result apportionment, and SAF-T (SVAT) audit. It also validates **projection-based balances**: the legacy stored "Acumulados" require a "Reconstrução de Acumulados" step that computed balances eliminate. Legacy editable postings and stored accumulators are rejected.

## Context

This is the **fifth and final financial-core ADR**, and unlike the others it is mostly a new build: the snapshot has documents and `financial_transactions` but **no real ledger**. It now has three defined upstream sources to consume:
1. `fiscal_documents` immutable snapshots ([[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]) → revenue + output/input IVA.
2. `allocations` + `treasury_movements` ([[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]) → cash/bank vs receivable/payable clearing.
3. `valuation_layers` + costed `stock_movements` ([[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]) → inventory + COGS.

This ADR fixes how those events become balanced entries so [[SAF-T CV]] accounting export has a defined ledger to read. Payroll and assets will add posting-rule event types later.

## Data Model

- Entity/table: `chart_of_accounts`
  - Key fields: `id`, `tenant_id`, `code`, `name`, `type` (`asset|liability|equity|income|expense`), `parent_id` (hierarchy), `is_postable`, `tax_relevant`, `taxonomy_code` (SAF-T `TaxonomyCode`, 1–660), `status`; tenant carries a `taxonomy_reference` (`S`/`N`/`P`/`O`).
  - Note: the Cabo Verde standard is the **SNCRF** (Sistema de Normalização Contabilística e de Relato Financeiro). Seed the default chart from the **SNCRF account set + Anexo II taxonomy** in [[SAF-T CV Anexo II - SNCRF Account Taxonomy]] (`raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv`); each account stores its `taxonomy_code` for SAF-T export.

- Entity/table: `journals`
  - Key fields: `id`, `tenant_id`, `code`, `name`, `kind` (`sales|purchases|treasury|inventory|general|opening`).

- Entity/table: `accounting_periods`
  - Key fields: `id`, `tenant_id`, `year`, `period_no`, `start_date`, `end_date`, `status` (`open|closed|locked`).
  - Constraints: a posting's date must fall in an `open` period; closing/reopening is permissioned + audited.

- Entity/table: `journal_entries`
  - Key fields: `id`, `tenant_id`, `journal_id`, `period_id`, `entry_date`, `status` (`draft|posted|reversed`), `source_kind` (`fiscal_document|treasury_allocation|stock_valuation|manual|reversal`), `source_ref` (polymorphic + id), `reversed_by` (nullable self-fk), `created_by`, `posted_at`.
  - Constraints: once `posted`, immutable; correction only via a reversal entry referencing it.

- Entity/table: `journal_entry_lines`
  - Key fields: `id`, `tenant_id`, `entry_id`, `account_id`, `debit`, `credit`, `tax_code` (nullable), `analytic_dimension_id` (nullable), `description`.
  - Constraints: per entry, Σdebit = Σcredit (enforced at post time); exactly one of debit/credit non-zero per line.

- Entity/table: `posting_rules`
  - Key fields: `id`, `tenant_id`, `event_type` (e.g. `invoice_issued`, `payment_allocated`, `goods_received`, `goods_delivered`), `template_json` (debit/credit legs keyed to account roles + tax handling), `active`, `version`.
  - Rationale: makes posting deterministic and configurable without code changes; versioned for audit. High-risk → `accounting.rule_admin` + audit.

- Entity/table: `tax_maps`
  - Key fields: `id`, `tenant_id`, `tax_code`, `account_id`, `direction` (`output|input`), `saft_tax_code`, `rate`.
  - Bridges IVA codes on documents to ledger accounts and SAF-T tax codes.

- Entity/table: `analytic_dimensions`, `analytic_allocations`
  - Cost-center/project analytical tagging (ties to [[Projetos ERP]]); MVP-optional, schema-ready.

- Projections: `account_balances` (per account/period from posted lines), `trial_balance` (period rollup). Views/materialized, never hand-maintained.

## State And Events

- State: `journal_entries.status`: `draft -> posted -> reversed`.
- State: `accounting_periods.status`: `open -> closed -> (reopened) open` (reopen permissioned + audited).
- Event (to `audit_log`): `accounting.journal_entry_posted`, `accounting.journal_entry_reversed`, `accounting.period_closed`, `accounting.period_reopened`, `accounting.posting_rule_changed`, `accounting.tax_profile_changed`, `accounting.saft_export_generated` — already listed in [[Permissoes e Auditoria ERP]].
- Transition rule: posting requires an open period and a balanced entry; a posted entry is never mutated; reversal creates a mirrored entry and audits before/after.

## Posting Policy (auto vs review)

- MVP default: upstream events create **draft** entries via posting rules; an accountant reviews and posts (resolves the auto-vs-review open question conservatively — auto-draft, manual post). A per-tenant config can later enable auto-post for trusted event types.

## Alternatives Considered

- Alternative: post directly from UI / mutate balances.
  Why not: breaks immutability, audit and SAF-T; balances must derive from posted lines.
- Alternative: hard-code posting logic in application code.
  Why not: `posting_rules` make it configurable, versioned and auditable per tenant/jurisdiction.
- Alternative: let accounting read fiscal/treasury/inventory raw tables directly.
  Why not: violates the consumption boundary; accounting reads defined *outputs/events*, not raw DFE XML or internal integration state.
- Alternative: single combined balances table updated transactionally.
  Why not: drift and contention; derive from immutable lines.

## Consequences

- Positive: deterministic, auditable, immutable ledger; SAF-T CV accounting export reads one defined source; clean separation from fiscal/treasury/inventory internals.
- Positive: posting rules + tax maps localize Cabo Verde accounting without code changes.
- Tradeoff: more upfront modeling; posting-rule engine and balance projections must be correct and tested; chart/tax-map seeding needs legal input.
- Migration impact: new build — no snapshot ledger to migrate; `financial_transactions` stays in treasury, not accounting.
- Operational impact: balances/trial balance are queries needing indexes/materialization; period close is an operational gate.

## Validation Plan

- Test: every posted entry balances (Σdebit = Σcredit); unbalanced post is rejected.
- Test: an `invoice_issued` event produces the expected revenue + output-IVA legs per its posting rule and tax map.
- Test: a `payment_allocated` event clears the receivable against cash/bank correctly.
- Test: a `goods_delivered` event posts COGS using the costed unit_cost from valuation layers.
- Test: posting into a closed period is blocked; reopening is permissioned and audited.
- Test: a posted entry cannot be edited or deleted; reversal mirrors it and audits.
- Test: cross-tenant isolation on every accounting table (inherits foundation ADR gates).
- Fixture/source: posting scenarios from [[2026-05-26 - Backlog Estruturado NOVA-ERP]]; tax maps cross-checked against [[SAF-T CV]] once the official accounting schema is ingested.

## Open Questions

- Resolved: the standard is the **SNCRF**; the default chart + per-account `taxonomy_code` seed from Anexo II of Portaria 47/2021 ([[SAF-T CV Anexo II - SNCRF Account Taxonomy]]). Remaining: which SNCRF chart **edition** ships as the tenant default and whether NRF-PE small-entity variants need a separate seed.
- Should NOVA-ERP ship full accounting in MVP or SAF-T-ready data first? (Open product call — schema supports both.)
- How closely must `journal_entry`/tax_map structures match official SAF-T CV accounting elements?
- Auto-draft + manual post confirmed for MVP — when is per-event auto-post enabled?
- Are analytic dimensions MVP or deferred with [[Projetos ERP]]?
- Multi-currency postings (FX revaluation) — in scope with treasury multi-currency or deferred?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are inspected and when `MCG001 - Contabilidade Geral` is deep-ingested. The official SAF-T CV accounting schema and the **SNCRF** chart taxonomy are now confirmed ([[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]], [[SAF-T CV Anexo II - SNCRF Account Taxonomy]]).
- Depends on the foundation, document-core, treasury and inventory ADRs; feeds [[SAF-T CV]]. Closes the financial-core schema sequence; remaining modules (payroll, assets) add posting-rule event types.
- Related log entry: 2026-05-28 accounting schema decision.
