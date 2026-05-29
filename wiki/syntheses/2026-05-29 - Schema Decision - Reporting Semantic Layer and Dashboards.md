---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, dashboards, reporting, kpi, semantic-layer, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]", "[[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]]", "[[2026-05-29 - Schema Decision - Project and Analytical Dimensions]]"]
related: ["[[NOVA-ERP]]", "[[Dashboards e Relatorios ERP]]", "[[IA Assistente ERP]]", "[[Permissoes e Auditoria ERP]]", "[[SAF-T CV]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]"]
confidence: medium
---

# Schema Decision - Reporting Semantic Layer and Dashboards

## Decision

NOVA-ERP reporting is a **governed semantic layer**, not ad-hoc SQL scattered across screens. KPI, report, dataset and dashboard *definitions* are first-class, versioned metadata that are the single source of truth for what every number means. Dashboards **and** [[IA Assistente ERP]] read only through curated `reporting_datasets` — tenant-scoped, permission-filtered views/materialized views/service endpoints — never raw operational tables. Each dataset and KPI declares a freshness policy, and every served value carries a runtime freshness state (`live|cached|snapshot|stale|blocked`). Reads pass both the user-permission gate ([[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]) and, where plan-gated, the tenant-entitlement gate ([[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]]). Heavy reports run asynchronously as `report_runs`; exports are a separate, higher-risk, always-audited action. The layer is strictly read-only and never mutates source modules; management dashboards are explicitly distinct from statutory/SAF-T/IVA outputs, which remain owned by the fiscal/accounting modules. An `ai_safe` flag on datasets is the only surface [[IA Assistente ERP]] may consume.

## Scope

- Module: [[Dashboards e Relatorios ERP]] and the shared reporting/semantic layer used by every module dashboard.
- Tables/objects: `reporting_datasets`, `kpi_definitions`, `report_definitions`, `dashboard_definitions`, `dashboard_widgets`, `report_runs`, `report_exports`, `report_subscriptions`, `kpi_snapshots`, `data_quality_flags`.
- Workflows affected: KPI/dataset/dashboard authoring and versioning, dashboard rendering, drill-down, async report generation, export, scheduling, AI dataset approval.
- Tenancy boundary: every served row is tenant-scoped or permission-filtered at the dataset boundary under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; platform/support analytics are designed separately, not on tenant dashboards.

## Source Basis

- Module source: [[Dashboards e Relatorios ERP]] requires stable KPI definitions, curated views (not unrestricted tables), permission-aware access, export controls, async heavy reports and an AI-safe context boundary.
- Product source: PRD/SSD/backlog require dashboards that expose fiscal risk, cash, sales, overdue, inventory, accounting readiness, payroll cost, subscription health and project profitability.
- Security source: [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]] supplies the permission keys, sensitive-evidence tiers and audit events reused here.
- Entitlement source: [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] supplies plan-gating for premium dashboards/reports.
- Dimension source: [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]] supplies the filter/slice dimensions.
- Compliance source: SAF-T CV, IVA and accounting report formats require current official verification; dashboards summarize, they do not certify.

## Context

The entry page warns that reporting must not become "ad hoc SQL scattered across screens" and that leadership must not be shown "visually polished but semantically unstable numbers." The architectural answer is a semantic layer: definitions own meaning, curated datasets own access, and the runtime only renders what those declare. This single boundary simultaneously enforces tenancy, permissions, entitlement, freshness and AI-safety — instead of each screen re-implementing them. It also resolves the entry page's open question "operational tables, curated SQL views, or service-layer APIs?" in favor of governed curated datasets.

## Data Model

- Entity/table: `reporting_datasets`
  - Key fields: `id`, `tenant_id` (nullable = system-defined template), `key`, `name`, `source_kind` (`view|matview|service`), `source_ref`, `dimensions` (jsonb: supported slice dimensions), `required_permission`, `required_entitlement` (nullable), `freshness_policy` (`live|cached:<ttl>|snapshot:<cron>`), `ai_safe` (bool), `version`, `status`.
  - Purpose: the only sanctioned read surface for dashboards and AI; carries its own access + freshness + AI policy.

- Entity/table: `kpi_definitions`
  - Key fields: `id`, `tenant_id` (nullable), `key`, `name`, `business_meaning`, `formula`, `dataset_id` (fk), `included_states` (jsonb), `period_basis`, `currency_tax_treatment`, `unit`, `refresh_policy`, `required_permission`, `caveats`, `version`, `status`.
  - Constraints: formula changes create a new `version`; old versions retained for historical comparability.

- Entity/table: `report_definitions`
  - Key fields: `id`, `tenant_id` (nullable), `key`, `module`, `purpose`, `parameters` (jsonb), `dataset_ids` (jsonb), `sensitivity` (`standard|sensitive|fiscal_raw`), `output_formats`, `required_permission`, `required_entitlement` (nullable), `is_statutory` (bool), `owner`.
  - Note: `is_statutory = true` reports are owned/validated by fiscal/accounting modules; the reporting layer only orchestrates their run.

- Entity/table: `dashboard_definitions`
  - Key fields: `id`, `tenant_id` (nullable), `key`, `name`, `module_scope`, `default_filters` (jsonb), `required_permission`, `required_entitlement` (nullable), `display_order`, `status`.

- Entity/table: `dashboard_widgets`
  - Key fields: `id`, `tenant_id`, `dashboard_id`, `widget_type` (`kpi|chart|table|exception_list`), `binding_kind` (`kpi|report|dataset`), `binding_ref`, `config` (jsonb), `drilldown_route`, `display_order`.

- Entity/table: `report_runs`
  - Key fields: `id`, `tenant_id`, `report_id`, `parameters` (jsonb), `requested_by`, `status` (`queued|running|completed|failed|expired|cancelled`), `storage_ref`, `result_summary`, `error_summary`, `correlation_id`, `expires_at`, `created_at`.
  - Constraints: heavy/statutory reports run here, never inline; attribution + retention required.

- Entity/table: `report_exports`
  - Key fields: `id`, `tenant_id`, `report_run_id` (nullable), `format`, `actor_user_id`, `sensitivity`, `storage_ref`, `retention_until`, `audit_ref`, `created_at`, `downloaded_at`.
  - Constraints: every export is permissioned and audited (`report.export_generated`/`report.export_downloaded`); private storage for sensitive output.

- Entity/table: `report_subscriptions`
  - Key fields: `id`, `tenant_id`, `report_id`, `schedule`, `recipients`, `delivery_channel`, `status`. (Scheduling is non-MVP per the entry page; schema-ready.)

- Entity/table: `kpi_snapshots`
  - Key fields: `id`, `tenant_id`, `kpi_id`, `kpi_version`, `period_start`, `period_end`, `value`, `dimensions` (jsonb), `captured_at`.
  - Purpose: trend/cache/historical comparison without recomputing live.

- Entity/table: `data_quality_flags`
  - Key fields: `id`, `tenant_id`, `dataset_id` (nullable), `kpi_id` (nullable), `flag_kind` (`stale|inconsistent|blocked|source_gap`), `detail`, `raised_at`, `cleared_at`.
  - Purpose: drives the `stale`/`blocked` freshness state honestly instead of silently showing wrong numbers.

## State And Events

- State: `report_runs.status`: `queued -> running -> completed`; `running -> failed`; `completed -> expired`; `* -> cancelled`.
- State: data freshness (per served value, derived): `live | cached | snapshot | stale | blocked`. `stale`/`blocked` are driven by `data_quality_flags` and permission/validation outcomes.
- Events (to `audit_log`, taxonomy in the permissions ADR): `report.definition_created`, `report.definition_changed`, `kpi.definition_changed`, `dashboard.viewed`, `dashboard.drilldown_opened`, `report.run_requested`, `report.run_completed`, `report.run_failed`, `report.export_generated`, `report.export_downloaded`, `report.schedule_created`, `report.access_denied`, `kpi.snapshot_created`, `reporting.dataset_refreshed`.
- Transition rule: a KPI/report formula change bumps `version` and emits a definition-changed event; historical snapshots keep the version they were computed under.

## Access, Permission And AI Boundary

- Read path: client/AI requests a `dataset`/`kpi`/`report` by key → service checks `required_permission` via `has_permission` and `required_entitlement` via `saas_get_tenant_access` → returns tenant-filtered rows with freshness state, or `blocked`.
- Sensitive tiers reuse the evidence tiers from the permissions ADR: payroll cost, raw e-Fatura evidence and security logs require the raw/secret tiers, never the status tier.
- New permission keys (feed the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]): `report.view`, `report.run`, `report.export`, `report.schedule`, `kpi.manage`, `dashboard.manage`, `reporting.dataset_manage`.
- AI boundary: [[IA Assistente ERP]] may consume only datasets with `ai_safe = true`, plus `kpi_definitions` (meaning/formula/caveats) and freshness state. It never reads operational tables or non-ai_safe datasets. This is the contract the AI ADR builds on.

## Statutory vs Management Boundary

- Management dashboards/KPIs are operational analytics and are labeled as such; they are not statutory submissions.
- `is_statutory` reports (SAF-T CV, IVA, accounting maps) are owned and validated by the fiscal/accounting modules and grounded in current DNRE/legal sources; the reporting layer only schedules/stores their runs and must not present unverified figures as official.
- Operational profitability, cash flow and accounting profit stay distinct, consistent with [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]].

## Alternatives Considered

- Alternative: dashboards query operational tables directly with per-screen SQL.
  Why not: re-implements tenancy/permission/freshness everywhere, drifts metric definitions, and exposes raw sensitive data.
- Alternative: store computed KPI values as the source of truth.
  Why not: KPIs must be reproducible from definitions over datasets; snapshots are a cache/trend aid, not truth.
- Alternative: one "reporting role" gates all reports.
  Why not: collapses the sensitive-evidence tiers; payroll/fiscal-raw/accounting need distinct permissions.
- Alternative: let AI query datasets freely.
  Why not: needs an explicit `ai_safe` allowlist or AI can surface restricted aggregates or invent metrics.

## Consequences

- Positive: one governed boundary enforces tenancy, permission, entitlement, freshness and AI-safety; metric meaning is stable and versioned.
- Positive: heavy/statutory reports are async and attributable; exports are auditable and retention-bound.
- Positive: the `ai_safe` dataset surface makes the AI ADR a thin, safe consumer.
- Tradeoff: authoring curated datasets/definitions is upfront work vs quick ad-hoc queries.
- Tradeoff: materialized views/snapshots need refresh orchestration and honest staleness flagging.
- Migration impact: new build; the snapshot has no semantic-layer tables.

## Validation Plan

- Test: a dashboard widget renders only via a `reporting_dataset`; no client path reads an operational table directly.
- Test: tenant A never sees tenant B rows through any dataset/report/export.
- Test: a user lacking `report.export` cannot export; every successful export writes an audit row.
- Test: a plan-gated dashboard is denied when the tenant entitlement is absent, independent of user permission.
- Test: a payroll-cost KPI is `blocked` for a user without the payroll salary tier.
- Test: a stale/failed source raises a `data_quality_flag` and the value renders `stale`/`blocked`, never a silently wrong number.
- Test: AI retrieval returns only `ai_safe` datasets and KPI definitions, never operational tables.
- Test: a KPI formula change creates a new version and prior `kpi_snapshots` keep their original version.

## Open Questions

- Which dashboard is the first post-login screen and which KPIs prove value in the first release?
- Which exports are MVP and in which formats?
- Which metrics need live vs cached vs daily-snapshot freshness?
- Which dashboards/reports are plan-gated by [[Subscricoes SaaS ERP]]?
- Which datasets are approved `ai_safe` for launch?
- Are tenant-defined custom KPIs in scope, or system-defined only at launch?

## Maintenance Notes

- Update when actual Supabase migrations/RLS/materialized-view strategy are available (see [[2026-05-29 - Supabase Implementation Artifact Gap]]) and when SAF-T CV/IVA report formats are verified against current DNRE sources.
- Depends on tenant foundation, permissions/audit, subscriptions and analytical-dimensions ADRs; directly enables [[IA Assistente ERP]] via the `ai_safe` dataset contract. New `report.*`/`kpi.manage`/`dashboard.manage`/`reporting.dataset_manage` keys must be added to the permission catalog.
