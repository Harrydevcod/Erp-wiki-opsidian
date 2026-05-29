---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, projetos, custos, operacional]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]", "[[Compras e Vendas ERP]]", "[[Tesouraria ERP]]", "[[Contabilidade ERP]]", "[[Dashboards e Relatorios ERP]]"]
related: ["[[NOVA-ERP]]", "[[Compras e Vendas ERP]]", "[[Tesouraria ERP]]", "[[Contabilidade ERP]]", "[[Dashboards e Relatorios ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Processamento de Salarios ERP]]", "[[Gestao de Ativos ERP]]", "[[2026-05-29 - Schema Decision - Project and Analytical Dimensions]]"]
confidence: medium
---

# Projetos ERP

## Purpose

Projetos ERP is the project, cost-tracking and profitability dimension for [[NOVA-ERP]]. It helps companies organize operational work, budgets, costs, revenues, cash effects and accountability below the company level.

## Role In NOVA-ERP

Projects are not part of the first fiscal/commercial spine, but they become important once NOVA-ERP supports service companies, construction, consulting, internal initiatives, grants, long-running deliveries or any business that needs profitability and cost visibility by initiative.

Projects should not become a parallel accounting system. They should act as an operational and analytical dimension that links commercial documents, purchases, treasury movements, accounting lines, inventory consumption, payroll costs and dashboards.

Source: [[2026-05-26 - Captura Raw e Docs]], [[NOVA-ERP Product Authority Synthesis]], [[NOVA-ERP Module Priority Map]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- Product synthesis: [[NOVA-ERP Product Authority Synthesis]], [[NOVA-ERP Module Priority Map]]
- Commercial source boundary: [[Compras e Vendas ERP]]
- Financial source boundary: [[Tesouraria ERP]], [[Contabilidade ERP]]
- Reporting boundary: [[Dashboards e Relatorios ERP]]

## Design Gates Before Implementation

- Scope gate: decide whether MVP needs project as a simple analytical dimension or a full project management module.
- Dimension gate: define where project/cost-center tags can appear: document header, line, journal line, treasury movement, inventory issue or payroll allocation.
- Profitability gate: define whether project margin is calculated from document totals, treasury cash flow, accounting postings or a staged combination.
- Budget gate: define budget structure, revisions and approval before allowing budget-vs-actual reporting.
- Accounting gate: decide whether project appears as an accounting analytical dimension or only operational reporting metadata.
- Security gate: define who can view project profitability, labor cost, margin and budget variance.

## Core Workflows

- Create tenant-scoped projects with code, name, owner, customer/internal context, dates and status.
- Define project budget, expected revenue, expected cost and margin target where scoped.
- Associate sales documents, purchase documents, expenses, inventory movements, payroll allocations or accounting lines with projects.
- Track committed, actual and billed amounts.
- Monitor profitability, budget variance, cash position and operational status.
- Close projects and preserve historical reporting.
- Reopen projects only through controlled permission and audit.

## Required Master Data

- Project codes and names.
- Project statuses.
- Project owners/managers.
- Optional customer, supplier, department or internal sponsor.
- Budget categories.
- Cost/revenue categories.
- Analytical dimensions such as cost center, department, salesperson or warehouse where needed.
- Project templates where repeated project types emerge.

## Candidate Domain Model

- `projects`: tenant-owned project header, code, name, type, owner, customer/internal context, dates and status.
- `project_members`: users or teams associated with project responsibility and visibility.
- `project_budgets`: approved budget header, version, date range, status and approval metadata.
- `project_budget_lines`: budget category, expected revenue/cost, quantity, unit, margin target and notes.
- `project_allocations`: links from operational records or lines to a project and optional budget category.
- `project_revenue_events`: derived revenue evidence from sales/fiscal/commercial documents.
- `project_cost_events`: derived cost evidence from purchases, payroll allocations, inventory issues, treasury expenses or accounting lines.
- `project_milestones`: optional delivery/billing checkpoints.
- `project_status_events`: lifecycle and status history.
- `project_forecasts`: optional forecast snapshots for expected cost-to-complete or revenue-to-complete.

This is provisional. If MVP only needs a project dimension, start with `projects` and `project_allocations`, then derive reporting from source modules.

The committed target shape is in [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]], which resolves the project-vs-cost-center question by modeling both as types of a generic analytical-dimension layer (`analytical_dimensions` + `dimension_values` + polymorphic `dimension_tags`), with project profitability derived from tagged source events and the tagging capability present from day one so projects can be adopted later without destructive migration.

## Candidate State Machine

### Project State

- `draft`: project prepared but not active for allocations.
- `active`: operational and financial records can be linked.
- `on_hold`: temporarily paused, new allocations restricted by policy.
- `completed`: operational delivery complete, final financial effects may still arrive.
- `closed`: historical reporting protected from normal mutation.
- `cancelled`: project abandoned with reason and preserved history.

### Budget State

- `draft`: editable budget.
- `submitted`: awaiting approval.
- `approved`: used for budget-vs-actual reporting.
- `revised`: superseded by a new approved version.
- `closed`: final budget state preserved.

## Commercial Boundary

[[Compras e Vendas ERP]] should own commercial documents. Projects should consume references and line-level allocations.

Rules to preserve:

- a sales quote/order/invoice may be linked to a project, but the project does not issue fiscal documents;
- purchase orders, supplier invoices and expense documents may allocate lines to project cost categories;
- document correction, cancellation and transformation remain owned by commercial/fiscal modules;
- project revenue/cost reporting must follow source document state and correction lineage.

## Treasury Boundary

[[Tesouraria ERP]] owns receipts, payments, allocations, bank/cash movement and reconciliation. Projects may expose:

- cash received by project;
- cash paid by project;
- outstanding receivables/payables linked to project;
- advances and partial settlements where source records have project allocation.

Project cash flow should be derived from treasury allocations, not manually edited project totals.

## Accounting Boundary

[[Contabilidade ERP]] may support project or cost-center dimensions on journal lines. Projects should not post ledger entries directly.

Accounting should consume:

- approved project/cost-center dimensions on source events;
- accounting posting rules that preserve project allocation when relevant;
- manual accounting adjustments with explicit project dimension where permitted.

Project profitability can be reported from operational document totals before full accounting exists, but that must be labeled as operational profitability rather than statutory accounting profit.

## Payroll, Inventory And Asset Boundary

Potential future integrations:

- [[Processamento de Salarios ERP]] may allocate labor cost by project, employee, period or timesheet-like variable.
- [[Inventario ERP]] may allocate consumed stock/materials to project cost.
- [[Gestao de Ativos ERP]] may allocate depreciation or equipment usage to project where needed.

These should remain optional until each source module is deeply designed.

## Audit, Security And Tenancy

- Project records and allocations must be tenant-scoped.
- Project profitability, labor cost and margin visibility should be permissioned.
- Budget approval, revision, closure and reopening require audit logs.
- Project closure should prevent silent mutation of historical profitability.
- Source documents should not be edited through project screens.
- Allocations added after source document finalization require explicit permission and audit.

## Critical Domain Events

- `project.created`
- `project.activated`
- `project.status_changed`
- `project.budget_submitted`
- `project.budget_approved`
- `project.budget_revised`
- `project.allocation_added`
- `project.allocation_removed`
- `project.milestone_completed`
- `project.closed`
- `project.reopened`
- `project.forecast_updated`

## Cabo Verde Compliance Notes

No current source in the wiki establishes Cabo Verde-specific legal requirements for project accounting. Treat this as operational and analytical design unless later sources prove compliance relevance.

Fiscal caution:

- public works/State invoicing may create project-like accounting/reporting needs, but current rules remain unresolved in [[Fiscalidade Cabo Verde]];
- project profitability reports are management analytics, not statutory fiscal reports unless later legal/accounting sources define otherwise;
- any tax or public-contract-specific project logic requires current legal verification.

## MVP Acceptance Criteria

For the first sellable release, projects are acceptable only if scope is explicit:

- If projects are not MVP, core modules should still allow a future project/cost-center dimension without destructive migration.
- If projects are MVP, project records are tenant-scoped and permissioned.
- Source documents or lines can be linked to projects without duplicating commercial, treasury or accounting records.
- Project totals are derived from source records, not manually edited summary fields.
- Budget-vs-actual uses explicit budget lines and source-linked actuals.
- Project closure prevents casual mutation and preserves reporting history.
- Reports clearly distinguish operational profitability, cash flow and accounting profit.

## Non-MVP Until Confirmed

- Full project management with task boards, dependencies and resource scheduling.
- Timesheets and labor costing before payroll/HR design is ready.
- Construction/public-works-specific fiscal automation before current legal ingestion.
- Advanced revenue recognition.
- Automated cost-to-complete forecasting.
- Customer project portal.

## Open Questions

- Should projects ship as simple tags/dimensions first or as a full project management module?
- Which industries in Cabo Verde are the first target for project tracking?
- Should project profitability depend first on document totals, treasury cash flow or accounting postings?
- Should project allocation live at document header, line level or both?
- Should cost centers and projects be separate dimensions or a unified analytical dimension?
- Which users can see project labor cost and margin?

## Next Ingestion Targets

- `raw/assets/SSD/PRD.MD`
- `raw/assets/SSD/SSD.md`
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Current legal sources for public works/State invoicing if projects target construction or public-sector contracts.
