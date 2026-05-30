---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, payroll, hr, privacy, accounting, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]"]
related: ["[[NOVA-ERP]]", "[[Processamento de Salarios ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]"]
confidence: medium
---

# Schema Decision - Payroll Runs and Payslips

## Decision

NOVA-ERP models payroll as a period-based, privacy-restricted calculation subsystem. Employee master data, employment terms, payroll variables, rule versions, payroll runs, computed lines, approvals, payslips, payment batches and accounting events are separate objects. Approved payroll lines become immutable evidence for payslips, treasury payment obligations and accounting posting events. Legal deductions are rule-versioned configuration, not hard-coded constants, because current Cabo Verde payroll/tax/social-security sources are not yet ingested.

## Scope

- Module: [[Processamento de Salarios ERP]].
- Tables/objects: `employees`, `employment_terms`, `payroll_periods`, `payroll_components`, `payroll_component_rules`, `payroll_variables`, `payroll_runs`, `payroll_run_lines`, `payslips`, `payroll_approvals`, `payroll_recalculations`, `payroll_payment_batches`, `payroll_accounting_events`.
- Workflows affected: employee setup, monthly variables, batch/individual payroll processing, review, approval, payslip generation, payment preparation, accounting integration, cancellation/reprocessing.
- Tenancy boundary: every business row carries `tenant_id`; RLS follows [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] with payroll-specific permissions.

## Source Basis

- Product source: PRD requires employee records, remuneration, deductions, absences, overtime, subsidies, individual/batch payroll, receipts, payments, maps and accounting integration.
- Product source: SSD requires a rubric-based payroll engine, country-parametrizable labor rules, sensitive data separated by permissions, remuneration history and sequential period processing.
- Backlog source: employee records must include personal, fiscal, contractual and payment data; payroll must run by period, calculate remuneration/discounts, generate receipts and block improper reprocessing.
- Compliance source: the **IRPS withholding is now resolved by primary law** — [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] gives the exact monthly Category A formula (15/21/25% with parcela 5.500/10.300/16.300) and supersedes the IUR scale (see [[Contradiction - IRPS Category A Withholding Brackets]]). INPS contributions and minimum wage remain provisional in [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]; statutory subsidy/overtime formulas (Código Laboral) are still uncaptured.
- Technical source: payroll inherits tenant/RLS/audit foundation and posts to accounting only through approved source events.
- Legacy workflow reference: [[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]] confirms the employee master-data decomposition, batch+individual processing, monthly-variable set, autonomous subsidy runs and retroactives/anulação — adopted as domain coverage, not as architecture (legacy editable/UI patterns rejected in favor of immutable approved runs).

## Context

The financial-core ADRs define document, treasury, inventory and accounting boundaries. Payroll now needs its own boundary so it can feed accounting and treasury without turning salary results into editable spreadsheet-like rows. The PRD also says full HR is not MVP, so this ADR defines a safe schema shape even if payroll ships later.

## Data Model

- Entity/table: `employees`
  - Key fields: `id`, `tenant_id`, `employee_no`, `full_name`, `tax_id`, `status`, `personal_data_classification`, `created_at`.
  - Constraints: unique active `employee_no` per tenant; restricted read permissions.

- Entity/table: `employment_terms`
  - Key fields: `id`, `tenant_id`, `employee_id`, `effective_from`, `effective_to`, `contract_type`, `role_title`, `department_id`, `base_salary`, `payment_method`, `bank_account_ref`, `status`.
  - Constraints: non-overlapping effective periods per employee unless explicitly allowed; salary changes are append-only via new terms.

- Entity/table: `payroll_periods`
  - Key fields: `id`, `tenant_id`, `period_key`, `start_date`, `end_date`, `status` (`open|processing|approved|paid|closed|reopened`), `closed_at`, `closed_by`.
  - Constraints: one period per tenant and period key; closed periods block normal mutation.

- Entity/table: `payroll_components`
  - Key fields: `id`, `tenant_id`, `code`, `name`, `kind` (`earning|deduction|employer_charge|allowance|absence|overtime|adjustment`), `taxability_profile`, `account_role`, `status`.
  - Purpose: defines payroll rubrics/components without embedding formulas in employee records.

- Entity/table: `payroll_component_rules`
  - Key fields: `id`, `tenant_id`, `component_id`, `effective_from`, `effective_to`, `rule_kind`, `formula_json`, `legal_source_ref`, `status`, `version`.
  - Constraints: versioned/effective-dated; statutory rules require legal source references before production use.

- Entity/table: `payroll_variables`
  - Key fields: `id`, `tenant_id`, `period_id`, `employee_id`, `component_id`, `quantity`, `amount`, `source_kind`, `source_ref`, `notes`, `status`.
  - Constraints: variables are locked once included in an approved run.

- Entity/table: `payroll_runs`
  - Key fields: `id`, `tenant_id`, `period_id`, `scope` (`all|department|employee_list|single_employee`), `status` (`draft|calculated|pending_review|approved|cancelled|superseded`), `calculation_version`, `created_by`, `approved_by`, `approved_at`.
  - Constraints: approved runs are immutable; corrections create recalculation lineage.

- Entity/table: `payroll_run_lines`
  - Key fields: `id`, `tenant_id`, `run_id`, `employee_id`, `gross_amount`, `deduction_amount`, `employer_charge_amount`, `net_amount`, `details_json`, `status`.
  - Constraints: details snapshot the component/rule results used for reproducibility.

- Entity/table: `payslips`
  - Key fields: `id`, `tenant_id`, `run_line_id`, `employee_id`, `period_id`, `document_no`, `status` (`generated|published|corrected|voided`), `artifact_ref`, `published_at`.
  - Constraints: generated from approved run lines only; corrections create replacement evidence.

- Entity/table: `payroll_payment_batches`
  - Key fields: `id`, `tenant_id`, `period_id`, `run_id`, `status`, `total_net_amount`, `treasury_obligation_batch_id`, `created_at`.
  - Relationship: creates payable/payment preparation evidence for [[Tesouraria ERP]].

- Entity/table: `payroll_accounting_events`
  - Key fields: `id`, `tenant_id`, `run_id`, `event_type` (`payroll_approved|payroll_reversed|payroll_paid`), `source_ref`, `status`, `journal_entry_id`.
  - Relationship: consumed by [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] posting rules.

## State And Events

- State: `payroll_periods.status`: `open -> processing -> approved -> paid -> closed`; `closed -> reopened` only with permission and audit.
- State: `payroll_runs.status`: `draft -> calculated -> pending_review -> approved`; correction paths are `cancelled` or `superseded`.
- State: `payslips.status`: `generated -> published`; correction paths are `corrected` or `voided`.
- Events: `payroll.employee_created`, `payroll.employment_terms_changed`, `payroll.variable_recorded`, `payroll.run_calculated`, `payroll.run_approved`, `payroll.run_cancelled`, `payroll.payslip_generated`, `payroll.payslip_published`, `payroll.payment_batch_created`, `payroll.accounting_event_created`, `payroll.period_closed`, `payroll.period_reopened`.
- Transition rule: approved payroll is not edited in place; reprocessing creates a new run that supersedes or reverses prior evidence.

## Cabo Verde Statutory Parameters (provisional, source-linked)

These seed `payroll_components` / `payroll_component_rules`; each rule carries a `legal_source_ref` and stays rule-versioned so a rate change is config, not code. Figures are from secondary web sources and **require primary-law confirmation** before production (see [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]).

- INPS (general employees): total **24.5%** = **16% employer-charge** + **8.5% employee-deduction**; due by the 15th of the following month; a contribution **ceiling** applies (value to confirm). Self-employed 19.5%; domestic 23% (15%+8%).
- Income-tax withholding: **operative primary law obtained** — [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] (Art. 5.º). Monthly **Category A** retention on gross monthly income `Rm`: **`RI = 0,15·Rm − 5.500`** (`Rm ≤ 80.000$`), **`0,21·Rm − 10.300`** (`80.000–150.000$`), **`0,25·Rm − 16.300`** (`> 150.000$`); **round down to ten escudos**; **100$ minimum** if positive; no retention below ≈36.667$/mo (mínimo de existência). **Subsídios de férias/Natal/prémio de produtividade = retenção autónoma** (Art. 6.º), not added to the month's ordinary income; back-pay split over the months it relates to. Encode this as the rule-versioned default (`legal_source_ref = DL 6/2015`), effective-period-keyed so the superseded **IUR-2013** model (`I_R = [(V_m·p·N − PA) − α·(ME + EF)]/p`, 11.67–35%, from [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]) stays available only for pre-2015 recompute. Other categories (for supplier/withholding-agent flows): **B 20% (4% REMPE), C 20%, D 20%/10%, E 1%/20%**. The annual *englobamento* assessment scale (isenção 220.000$ / 16,5 / 23,1 / 27,5%) is a distinct final-assessment table, not the monthly retention. Employee INPS 8.5% is deductible from the base; **`ME` (mínimo de existência) confirmed = 220.000$ isenção** (CIRPS art. 45º nº2); only OE-year re-indexing of the 80.000$/150.000$ thresholds still warrants an annual check (see [[Contradiction - IRPS Category A Withholding Brackets]]).
- National minimum wage: **17,000$/month** private, **19,000$/month** public administration (from 2025-01-01) — a validation floor, not a deduction.
- Subsidies/overtime (Código Laboral, now **primary-sourced** from the preserved DL 5/2007 text in [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]): normal time **8h/day, 44h/week**; **overtime +35%** (art. 207º as amended by DL 1/2016; old +50% superseded), capped 2h/day·160h/yr (300h with consent) — model as a configurable multiplier; **rest-day work +100%** (art. 208º); **night work ≥+25%** (art. 169º); **férias 22 dias úteis/yr**. The **gratificação de Natal/13.º (art. 206º) is discretionary — NOT a mandatory 13th** — and when granted is **attendance-scaled** (≤3 faltas 100% / 4–6 75% / 7–10 50% / >10 none; injustified count double): model as an **optional, off-by-default** component, not a guaranteed accrual. Each is a rule-versioned component with `legal_source_ref = Código Laboral DL 5/2007 / DL 1/2016`.

## Security And Privacy

- Permission keys should separate at least: `payroll.employee_view`, `payroll.salary_view`, `payroll.employee_manage`, `payroll.variable_manage`, `payroll.process`, `payroll.approve`, `payroll.payslip_publish`, `payroll.payment_export`, `payroll.accounting_export`, `payroll.period_manage`.
- Salary, bank/payment and personal identifiers require restricted RLS policies and private storage for artifacts.
- AI access to payroll should be disabled by default until a dedicated privacy and permission design exists.

## Accounting And Treasury Boundary

Payroll does not write ledger lines directly. It emits approved accounting events that posting rules convert into draft/posted journal entries. Typical event legs include salary expense, employee deduction liabilities, employer-charge liabilities and payment clearing.

Payroll also does not mark payments as settled by itself. It creates treasury payment batches or obligations; final payment state is derived from [[Tesouraria ERP]] movements and allocations.

## Alternatives Considered

- Alternative: store one editable monthly salary row per employee.
  Why not: cannot reproduce calculations, audit changes, block improper reprocessing or support payslip corrections.
- Alternative: hard-code Cabo Verde deduction formulas now.
  Why not: current legal sources are not ingested; rule versions must be configurable and source-linked.
- Alternative: payroll writes directly to `journal_entries`.
  Why not: accounting ADR centralizes posting rules and review/period controls.

## Consequences

- Positive: deterministic payroll runs, immutable payslip evidence, privacy boundaries and clean accounting/treasury integration.
- Positive: statutory rules can evolve through versioned rules rather than code rewrites.
- Tradeoff: requires a calculation engine and strong permissions before production use.
- Migration impact: current database snapshot has no payroll tables; this is new-build schema.
- Operational impact: closed periods, recalculation and payslip publication need operator workflows, not just tables.

## Validation Plan

- Test: tenant A cannot read employee/payroll rows from tenant B.
- Test: user with `payroll.employee_view` but without `payroll.salary_view` cannot read remuneration fields.
- Test: approved run lines cannot be edited; recalculation creates lineage.
- Test: payslips can only be generated from approved run lines.
- Test: closed periods block new variables and reprocessing except via audited reopen.
- Test: payroll accounting events generate balanced draft entries through posting rules.
- Test: treasury payment batch total equals approved net payroll total.

## Open Questions

- Resolved: the withholding formula and scale are now captured from primary law ([[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]], IUR-era); governing sources are Lei 78/VIII/2014 (IRPS), INPS regulation and the Código Laboral ([[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]). Still open: the current **IRPS-era** withholding portaria (does it supersede Portaria 5/2013?), the `ME` (Mínimo de Existência) value, the INPS contribution ceiling, and statutory subsidy/overtime formulas and required payroll maps.
- Is minimal payroll in first sellable release, or phase two/three?
- Which launch roles may view salary data?
- Should payslips be employee-facing in the first release?
- What accounting granularity is required: per employee, department, cost center or summarized batch?
- What payroll maps/reports are legally required in Cabo Verde?

## Maintenance Notes

- Update after legal/payroll source ingestion and after actual Supabase migrations/RLS are available.
- Depends on tenant foundation and accounting ADRs; feeds [[Tesouraria ERP]], [[Contabilidade ERP]] and future SAF-T/readiness work if payroll data becomes export-relevant.
