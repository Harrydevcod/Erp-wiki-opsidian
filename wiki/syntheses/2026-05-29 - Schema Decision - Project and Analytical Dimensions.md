---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, projects, analytical-dimensions, cost-tracking, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]"]
related: ["[[NOVA-ERP]]", "[[Projetos ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[Compras e Vendas ERP]]", "[[Dashboards e Relatorios ERP]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]"]
confidence: medium
---

# Schema Decision - Project and Analytical Dimensions

## Decision

NOVA-ERP models projects as one **dimension type** inside a generic analytical-dimensions layer rather than as a standalone module or a parallel ledger. A small dimension machinery — `analytical_dimensions` (the catalog of dimension *types*: project, cost_center, department, salesperson…), `dimension_values` (the concrete instances), and a polymorphic `dimension_tags` link from any source record/line to one or more dimension values with an explicit allocation basis — lets every module carry analytical context without per-module columns. Projects extend a dimension value with budget, lifecycle and ownership (`projects`, `project_budgets`, `project_budget_lines`). Project profitability is **derived** (no stored totals): `project_cost_events` and `project_revenue_events` are read-projections over tagged source records (sales, purchases, treasury, inventory issues, payroll, journal lines), following each source's state and correction lineage. Projects never issue fiscal documents and never post journal entries; they consume the defined outputs of upstream ADRs. Crucially, the `dimension_tags` capability is part of the core schema from day one so projects/cost-centers can be adopted later **without destructive migration**, even if projects are not in the first release.

## Scope

- Module: [[Projetos ERP]] plus the shared analytical-dimension layer used by accounting, treasury, commercial, inventory and payroll.
- Tables/objects: `analytical_dimensions`, `dimension_values`, `dimension_tags`, `projects`, `project_members`, `project_budgets`, `project_budget_lines`, `project_milestones`, `project_status_events`; plus derived projections `project_cost_events`, `project_revenue_events`, `project_forecasts`.
- Workflows affected: project setup, budget approval, tagging of source records/lines, budget-vs-actual and profitability reporting, project closure/reopen.
- Tenancy boundary: every row carries `tenant_id`; RLS follows [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; visibility of profitability/labor/margin is permissioned per [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]].

## Source Basis

- Product source: PRD/SSD position projects as cost/profitability tracking for service, construction, consulting and internal initiatives — an analytical dimension, not a parallel accounting system.
- Backlog source: projects link commercial documents, purchases, treasury and accounting with budgets and budget-vs-actual reporting.
- Module source: [[Projetos ERP]] enumerates the candidate domain model, lifecycle and the explicit boundary that projects derive from source modules and do not post or issue.
- Financial sources: [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]], [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]], [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] own the source events tagged here.
- Compliance source: no current Cabo Verde source establishes statutory project-accounting rules; treat as management analytics unless later sources prove fiscal relevance.

## Context

The entry page left a decisive open question: "should cost centers and projects be separate dimensions or a unified analytical dimension?" Committing one generic dimension layer resolves it cleanly — projects and cost centers are distinct *types* sharing one tagging mechanism, so reports can slice by either without bespoke columns per module. It also satisfies the hardest MVP criterion: core modules must allow a future project/cost-center dimension without destructive migration. Putting `dimension_tags` in the foundation now makes projects a feature toggle later rather than a schema rewrite.

## Data Model

- Entity/table: `analytical_dimensions`
  - Key fields: `id`, `tenant_id` (nullable = system type), `key` (`project|cost_center|department|salesperson`), `name`, `is_required_for` (jsonb: modules that mandate this dimension), `status`.
  - Purpose: catalog of dimension types; controls which modules may/must tag.

- Entity/table: `dimension_values`
  - Key fields: `id`, `tenant_id`, `dimension_id` (fk), `code`, `name`, `parent_id` (nullable, for hierarchy), `status` (`active|archived`).
  - Constraints: unique (`tenant_id`, `dimension_id`, `code`).

- Entity/table: `dimension_tags`
  - Key fields: `id`, `tenant_id`, `source_type` (`sales_doc|purchase_doc|journal_line|treasury_movement|stock_movement|payroll_line`), `source_id`, `source_line_id` (nullable), `dimension_value_id` (fk), `allocation_basis` (`full|percent|amount`), `allocation_value`, `created_at`, `created_by`.
  - Constraints: a single source line may carry multiple tags across different dimensions; within one dimension, split allocations on the same line must sum to 100% / line amount.
  - This is the one join that turns any source record into analytical data — no module stores its own project column.

- Entity/table: `projects`
  - Key fields: `id`, `tenant_id`, `dimension_value_id` (fk — a project is registered as a `project`-type dimension value), `code`, `name`, `project_type`, `owner_user_id`, `customer_entity_id` (nullable), `start_date`, `end_date`, `status` (lifecycle), `created_at`.
  - Constraints: unique (`tenant_id`, `code`); 1:1 with its `dimension_values` row so tagging and project metadata stay in sync.

- Entity/table: `project_members`
  - Key fields: `id`, `tenant_id`, `project_id`, `user_id`, `responsibility`, `visibility_scope`.

- Entity/table: `project_budgets`
  - Key fields: `id`, `tenant_id`, `project_id`, `version`, `status` (`draft|submitted|approved|revised|closed`), `effective_from`, `approved_by`, `approved_at`.
  - Constraints: only one `approved` version active for budget-vs-actual; revisions supersede, never overwrite.

- Entity/table: `project_budget_lines`
  - Key fields: `id`, `tenant_id`, `budget_id`, `category`, `kind` (`revenue|cost`), `expected_amount`, `quantity`, `unit`, `margin_target`, `notes`.

- Entity/table: `project_milestones`
  - Key fields: `id`, `tenant_id`, `project_id`, `name`, `due_date`, `status`, `billing_link_ref` (nullable).

- Entity/table: `project_status_events`
  - Key fields: `id`, `tenant_id`, `project_id`, `from_status`, `to_status`, `reason`, `actor`, `created_at`.

- Derived projections (read models, not editable totals):
  - `project_cost_events`: cost evidence resolved from `dimension_tags` over purchases, payroll lines, inventory issues, treasury expenses and cost journal lines.
  - `project_revenue_events`: revenue evidence resolved from sales/fiscal documents and revenue journal lines.
  - `project_forecasts`: optional cost-to-complete / revenue-to-complete snapshots.

## State And Events

- State: `projects.status`: `draft -> active -> on_hold -> active`; `active -> completed -> closed`; `* -> cancelled`. `closed`/`cancelled` protect historical reporting; reopen requires permission + audit.
- State: `project_budgets.status`: `draft -> submitted -> approved`; `approved -> revised` (new version) ; `* -> closed`.
- Events: `project.created`, `project.activated`, `project.status_changed`, `project.budget_submitted`, `project.budget_approved`, `project.budget_revised`, `project.allocation_added`, `project.allocation_removed`, `project.milestone_completed`, `project.closed`, `project.reopened`, `project.forecast_updated` — all to `audit_log`.
- Transition rule: allocations added or removed after a source document is finalized require explicit permission and an audit event; closing a project blocks new tags except via audited reopen.

## Derivation And Boundary Rules

- No stored totals: every project figure is computed from `dimension_tags` + source records. Editing a source corrects the project view automatically; the project never holds an independent number that can drift.
- Commercial boundary: a sales/purchase document may be tagged to a project, but [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]] still owns issuance, correction, cancellation and transformation; project reporting follows that lineage.
- Treasury boundary: project cash-in/cash-out is derived from [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]] allocations, never manually edited.
- Accounting boundary: the `project`/`cost_center` dimensions ride on `journal_entry_lines` via `dimension_tags`; projects never write journal entries. Posting rules preserve the dimension where relevant per [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]].
- Reporting labels: operational profitability (document totals), cash flow (treasury) and accounting profit (ledger) are distinct and must be labeled as such; operational profitability is not statutory profit.

## Security And Tenancy

- All dimension/project rows are tenant-scoped under the foundation RLS pattern.
- New permission keys (feed the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]): `project.view`, `project.manage`, `project.allocate`, `project.budget_manage`, `project.budget_approve`, `project.profitability_view`, `project.close`, `dimension.manage`.
- Profitability, labor cost and margin visibility are gated behind `project.profitability_view`, separate from `project.view`.

## Alternatives Considered

- Alternative: a standalone projects module with its own cost/revenue tables.
  Why not: duplicates commercial/treasury/accounting records and lets project totals drift from source truth.
- Alternative: separate, unrelated `cost_centers` and `projects` subsystems.
  Why not: doubles the tagging machinery and reporting code; one dimension layer with typed values is simpler and more extensible.
- Alternative: add a `project_id` column to every source table.
  Why not: rigid (one dimension only, no split allocation) and requires destructive migration to add cost centers/departments later. `dimension_tags` supports many dimensions and split allocation.
- Alternative: store computed project totals for speed.
  Why not: violates the derive-from-source invariant; use materialized/cached projections instead, refreshed from source.

## Consequences

- Positive: one analytical machinery serves projects, cost centers and departments; reports slice by any dimension.
- Positive: adopting projects later is a feature toggle, not a migration; satisfies the non-destructive MVP criterion.
- Positive: project numbers can never drift from source documents.
- Tradeoff: split-allocation validation and multi-dimension tagging add UI/service complexity.
- Tradeoff: derived projections may need materialization/caching for large tenants.
- Migration impact: new build; the snapshot has no project/dimension tables.

## Validation Plan

- Test: a source line tagged to two projects with `percent` 60/40 splits cost accordingly and the splits sum to 100%.
- Test: correcting/cancelling a source document updates derived project cost/revenue without editing project rows.
- Test: tenant A cannot read tenant B's projects, dimensions or tags.
- Test: a user with `project.view` but not `project.profitability_view` cannot read margin/labor cost.
- Test: budget-vs-actual uses the single `approved` budget version and source-derived actuals.
- Test: a `closed` project rejects new tags except via an audited reopen.
- Test: adding the `cost_center` dimension to an existing tenant requires no source-table schema change.

## Open Questions

- Is projects a first-release dimension (`projects` + `dimension_tags` only) or a later full module with milestones/forecasts?
- Which Cabo Verde industries (construction, consulting, public works) are the first target, and do public-works contracts add fiscal/reporting rules?
- Should `dimension_tags` allow header-level tags that cascade to lines, or line-level only?
- Which dimensions are mandatory vs optional per module (`is_required_for`)?
- Do project profitability projections need materialization for launch scale?

## Maintenance Notes

- Update after current Supabase migrations/RLS are available (see [[2026-05-29 - Supabase Implementation Artifact Gap]]) and if public-works/State-contract fiscal sources are ingested.
- Depends on tenant foundation and the financial-core ADRs; the `project.*`/`dimension.manage` keys must be added to the permission catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]; feeds [[Dashboards e Relatorios ERP]].
