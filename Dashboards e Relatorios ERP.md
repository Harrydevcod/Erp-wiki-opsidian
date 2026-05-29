---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, dashboards, relatorios, analytics, kpi]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]", "[[Permissoes e Auditoria ERP]]", "[[IA Assistente ERP]]"]
related: ["[[NOVA-ERP]]", "[[Permissoes e Auditoria ERP]]", "[[IA Assistente ERP]]", "[[Faturacao Eletronica]]", "[[Tesouraria ERP]]", "[[Inventario ERP]]", "[[Contabilidade ERP]]", "[[Projetos ERP]]", "[[Subscricoes SaaS ERP]]", "[[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]]"]
confidence: medium
---

# Dashboards e Relatorios ERP

## Purpose

Dashboards e Relatorios ERP is the governed visibility layer for [[NOVA-ERP]]: executive dashboards, operational KPIs, fiscal/financial reports, exception monitoring, report exports and curated analytical context for [[IA Assistente ERP]].

## Role In NOVA-ERP

Dashboards are how the ERP proves value daily. They should not be decorative. They should expose fiscal risk, cash position, sales, overdue balances, inventory pressure, accounting readiness, payroll cost, subscription health, project profitability and operational exceptions with permission-aware data.

Reporting must not become ad hoc SQL scattered across screens. NOVA-ERP needs stable KPI definitions, curated reporting views, permission-aware access, export controls and a clear distinction between operational analytics and statutory/fiscal reports.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[NOVA-ERP Product Authority Synthesis]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- Implementation prompt: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- Product synthesis: [[NOVA-ERP Product Authority Synthesis]], [[NOVA-ERP Module Priority Map]]
- Security boundary: [[Permissoes e Auditoria ERP]]
- AI boundary: [[IA Assistente ERP]]

## Design Gates Before Implementation

- Metric authority gate: define KPI names, formulas, source tables/views and refresh rules before displaying numbers.
- Data access gate: expose curated reporting views or service endpoints, not unrestricted table access.
- Permission gate: define role/module visibility for each dashboard, KPI, row group, export and sensitive drill-down.
- Freshness gate: define real-time, cached, snapshot and asynchronous report behavior per metric.
- Fiscal/reporting gate: distinguish management dashboards from statutory reports, SAF-T, IVA and official fiscal outputs.
- Export gate: define which reports can be exported, by whom, in which formats and with which audit logging.
- AI gate: decide which reporting views are safe for [[IA Assistente ERP]] retrieval.

## Core Workflows

- Present executive KPIs by tenant.
- Provide module dashboards for sales, purchases, fiscal/e-Fatura, treasury, inventory, accounting, payroll, projects, assets and subscriptions.
- Filter by period, tenant context, entity, warehouse, project, salesperson, status and relevant analytical dimensions.
- Surface exceptions: overdue payments, rejected e-Fatura documents, low stock, pending fiscal actions, audit anomalies, failed jobs, blocked exports and subscription risk.
- Drill down from KPI to source records where permission allows.
- Export or schedule reports where operationally necessary.
- Generate heavy reports asynchronously with status and history.
- Provide curated reporting context for [[IA Assistente ERP]].

## Required Master Data

- Report definitions.
- KPI definitions and formulas.
- Reporting datasets/views.
- Period calendars and date dimensions.
- User/role visibility rules.
- Export policies.
- Refresh/cache policies.
- Analytical dimensions such as project, warehouse, customer, supplier, salesperson, cost center, department or fiscal status.

## Candidate Domain Model

- `report_definitions`: report identity, module, purpose, parameters, sensitivity, output formats and owner.
- `kpi_definitions`: KPI name, formula, source dataset, unit, refresh policy, permission scope and explanation.
- `reporting_datasets`: curated views/materialized views/service datasets exposed to dashboards and AI.
- `dashboard_definitions`: dashboard layout, widgets, module scope and default filters.
- `dashboard_widgets`: widget type, KPI/report binding, chart/table configuration and drill-down route.
- `report_runs`: asynchronous report execution, parameters, actor, status, storage reference and result summary.
- `report_exports`: exported file metadata, format, actor, retention, sensitivity and audit reference.
- `report_subscriptions`: scheduled report delivery preferences where supported.
- `kpi_snapshots`: periodic KPI values used for trend, cache or historical comparison.
- `data_quality_flags`: metric/report blockers, stale data markers and source inconsistency indicators.

This model is provisional until actual schema/reporting implementation is designed. The committed target shape is in [[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]], which makes reporting a governed semantic layer: versioned KPI/report/dataset/dashboard definitions own metric meaning, dashboards and AI read only through curated tenant-scoped `reporting_datasets` (never operational tables), each value carries a freshness state, reads pass both permission and entitlement gates, and an `ai_safe` flag is the only surface [[IA Assistente ERP]] may consume.

## Candidate State Machine

### Report Run State

- `queued`: report request accepted.
- `running`: report generation underway.
- `completed`: output available.
- `failed`: generation failed with error summary.
- `expired`: output no longer retained.
- `cancelled`: run cancelled by user/system.

### Data Freshness State

- `live`: computed from current operational state.
- `cached`: served from recent cache.
- `snapshot`: historical snapshot for period/trend.
- `stale`: source data or refresh process is out of date.
- `blocked`: permissions, validation or source inconsistency prevents display.

## Reporting Source Boundary

Dashboards should consume governed source events and reporting views from modules:

- [[Compras e Vendas ERP]]: commercial document volume, sales/purchase status, transformations and pending approvals.
- [[Faturacao Eletronica]]: issued documents, authorization state, rejection reasons, contingency and fiscal actions.
- [[Tesouraria ERP]]: receivables, payables, overdue balances, cash/bank movements and reconciliation.
- [[Inventario ERP]]: stock availability, reservations, low stock, counts and movement anomalies.
- [[Contabilidade ERP]]: posting status, period locks, journal activity and SAF-T/accounting readiness.
- [[Processamento de Salarios ERP]]: payroll cost and payroll status only where privacy rules allow.
- [[Projetos ERP]]: operational profitability, budgets, allocations and cash effects.
- [[Subscricoes SaaS ERP]]: subscription lifecycle, plan mix, overdue risk and usage limits.

Dashboards should not mutate source module state. They may route the user to the owning module action.

## KPI Authority

Each KPI needs an explicit definition:

- business meaning;
- formula;
- source dataset;
- included/excluded document states;
- period basis;
- currency/tax treatment;
- refresh frequency;
- permission level;
- caveats or uncertainty.

This avoids misleading leadership with visually polished but semantically unstable numbers.

## Permission And Export Boundary

[[Permissoes e Auditoria ERP]] controls visibility. Report access must respect:

- tenant membership;
- module permission;
- sensitive field permission;
- payroll/privacy restrictions;
- fiscal/e-Fatura raw evidence restrictions;
- accounting period/security restrictions;
- SaaS entitlement where a report is plan-gated.

Exports are higher risk than screen views because they leave the application. Export actions should be permissioned and audited.

## AI Boundary

[[IA Assistente ERP]] should consume only curated reporting datasets, report definitions and KPI explanations. It should not query arbitrary operational tables.

AI-safe reporting context should include:

- KPI definitions;
- source record references;
- freshness state;
- permission-filtered aggregates;
- caveats and unresolved compliance uncertainty.

This lets AI explain dashboards without inventing metrics or leaking restricted records.

## Heavy Report And Job Boundary

The product synthesis notes that SAF-T and heavy reporting may require asynchronous processing. Dashboards should distinguish:

- lightweight screen KPIs;
- cached analytical widgets;
- heavy export jobs;
- statutory/fiscal exports;
- report histories with status and downloadable output.

Long-running report generation should have job status, retry/error summaries, actor attribution and retention policy.

## Audit, Security And Tenancy

- Dashboards must never leak cross-tenant data.
- Reporting datasets must be tenant-scoped or permission-filtered at the service/database boundary.
- Report access must follow role, module, field and entitlement permissions.
- KPI/report definitions should be stable, documented and versioned when formulas change.
- Exported reports can contain sensitive data and should be permissioned, logged and retained according to policy.
- Payroll, accounting, e-Fatura raw evidence and security logs require stricter reporting access than ordinary operational summaries.
- Platform/support aggregate analytics must be designed separately from tenant dashboards.

## Critical Domain Events

- `report.definition_created`
- `report.definition_changed`
- `kpi.definition_changed`
- `dashboard.viewed`
- `dashboard.drilldown_opened`
- `report.run_requested`
- `report.run_completed`
- `report.run_failed`
- `report.export_generated`
- `report.export_downloaded`
- `report.schedule_created`
- `report.access_denied`
- `kpi.snapshot_created`
- `reporting.dataset_refreshed`

## Cabo Verde Compliance Notes

Fiscal and statutory reports need separate evidence and validation. Dashboards may summarize compliance states, but official fiscal reporting must remain grounded in current legal and DNRE requirements.

Current cautions:

- e-Fatura status dashboards can show operational state, but raw XML/ZIP/DNRE response evidence remains restricted;
- SAF-T CV, IVA and accounting reports require current official source verification before production claims;
- payroll statutory reporting remains unresolved until current Cabo Verde payroll sources are ingested;
- management dashboards are not substitutes for official fiscal submissions.

## MVP Acceptance Criteria

For the first sellable release, dashboards/reporting are acceptable only if:

- every dashboard is tenant-scoped;
- key KPIs have documented definitions;
- report access respects permissions;
- fiscal/e-Fatura exception status is visible without exposing raw sensitive payloads;
- treasury overdue/cash indicators are derived from treasury movements and allocations;
- inventory indicators are derived from stock movements/reservations/counts;
- exports are permissioned and auditable;
- heavy reports run asynchronously or are explicitly out of scope;
- AI consumes only curated reporting context if AI is enabled.

## Non-MVP Until Confirmed

- Full self-service BI/query builder.
- Cross-tenant benchmarking.
- Automated email report scheduling.
- Advanced forecasting.
- AI-generated reports from unrestricted data.
- Statutory reports without current legal/source ingestion.
- Public/customer-facing reporting portal.

## Open Questions

- Which dashboard is the first screen after login?
- Which KPIs prove product value in the first sellable release?
- Should reports be generated directly from operational tables, curated SQL views or service-layer reporting APIs?
- Which report exports must exist in MVP?
- Which metrics require real-time freshness versus daily/hourly snapshots?
- Which dashboards are plan-gated by [[Subscricoes SaaS ERP]]?
- Which reporting views should be approved for [[IA Assistente ERP]]?

## Next Ingestion Targets

- `raw/assets/SSD/PRD.MD`
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- `raw/assets/DATABASE_ER_DIAGRAM.md`
- Current SAF-T CV, IVA and accounting report source set.
