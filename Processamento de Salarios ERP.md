---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-29
tags: [erp-module, rh, payroll, salarios, cabo-verde]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]]", "[[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]", "[[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]"]
related: ["[[NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Tesouraria ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Dashboards e Relatorios ERP]]", "[[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]]"]
confidence: medium
schema_decision: "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]"
---

# Processamento de Salarios ERP

## Purpose

Processamento de Salarios ERP is the HR/payroll module area for [[NOVA-ERP]], covering employee records, employment terms, remuneration, deductions, absences, overtime, subsidies, payroll runs, payslips, salary payments and accounting integration.

## Role In NOVA-ERP

Payroll is a controlled financial and privacy-sensitive subsystem. It connects HR master data, monthly variables, statutory/business calculation rules, employee payments, employer liabilities and accounting evidence.

Payroll must not be reduced to editable salary fields or ad hoc monthly spreadsheets. It needs period-based processing, deterministic calculations, review/approval, immutable payslip evidence, controlled reversal/recalculation and strict access boundaries.

Because this module touches employee privacy and legal deductions, NOVA-ERP must not make production compliance claims until current Cabo Verde payroll, tax, social-security and labor sources are ingested.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Permissoes e Auditoria ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- ERP workflow reference: [[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]] (ingested; PT fiscal maps not authority)
- HR configuration reference (raw): `docs/docsfiscal/Configuring - Recursos Humanos (2023-v1.0-PT).pdf`
- Exercises: `docs/docsfiscal/Exercícios - Using - Processamento Salarios (2023-v0.1-PT).pdf`
- Security boundary: [[Permissoes e Auditoria ERP]]
- Accounting/treasury boundary: [[Contabilidade ERP]], [[Tesouraria ERP]]

## Design Gates Before Implementation

- Legal source gate: ingest current Cabo Verde payroll, tax, social-security and labor obligations before implementing deduction formulas or statutory reports.
- Privacy gate: define salary/HR field visibility, manager access, payroll operator access and audit visibility before storing payroll data.
- Calculation gate: define deterministic calculation rules, versioning and effective dates before payroll runs.
- Period gate: define payroll periods, close/reopen behavior and recalculation rules.
- Accounting gate: define payroll cost, deduction, employer-liability and payment posting boundaries.
- Treasury gate: define how salary payment files/movements are created and reconciled.
- Audit gate: define immutable payroll run, payslip, approval, cancellation and recalculation evidence.

## Core Workflows

- Create and maintain employee records.
- Maintain employment terms, remuneration components and payment details.
- Configure earnings, deductions, employer charges, absences, overtime and subsidies.
- Register monthly variables such as absences, overtime, bonuses, allowances and one-off adjustments.
- Process payroll individually or in batch for a period.
- Review payroll results before approval.
- Approve, close, cancel or recalculate payroll runs through controlled flows.
- Generate payslips/receipts.
- Prepare salary payment obligations for [[Tesouraria ERP]].
- Produce payroll accounting evidence for [[Contabilidade ERP]].

## Required Master Data

- Employees and personal identifiers.
- Employment contracts or employment terms.
- Departments, cost centers or projects where applicable.
- Remuneration components.
- Deduction and employer-charge types.
- Absence, leave and overtime rules.
- Payroll calendars and periods.
- Payment methods and bank details.
- Calculation rule versions and effective dates.
- Payroll document/receipt templates.

## Candidate Domain Model

The schema boundary is now filed in [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]. That ADR makes payroll period-based, privacy-restricted and event-driven into treasury/accounting, while keeping legal formulas source-linked and unresolved until current Cabo Verde payroll sources are ingested.

- `employees`: tenant-owned employee profile, identifiers, contact/status and privacy classification.
- `employment_terms`: contract dates, role, department, base remuneration, schedule and payment method.
- `payroll_periods`: month/period, tenant, status, cutoff dates and close/reopen metadata.
- `payroll_components`: earnings, deductions, employer charges, allowances, overtime, absence impact and adjustment types.
- `payroll_component_rules`: calculation basis, formula version, effective dates and legal/business source reference.
- `payroll_variables`: monthly absences, overtime, bonuses, subsidies, advances and manual adjustments.
- `payroll_runs`: processing batch, period, scope, status, totals, actor and calculation version.
- `payroll_run_lines`: per-employee computed result, gross, deductions, employer charges, net and status.
- `payslips`: immutable employee-facing payroll receipt generated from approved run lines.
- `payroll_approvals`: review/approval/rejection records with actor and reason.
- `payroll_recalculations`: controlled recalculation/cancellation lineage.
- `payroll_payment_batches`: salary payment obligations exported or sent to treasury.
- `payroll_accounting_exports`: source events or posting batches for accounting.

This model is provisional until payroll legal/compliance sources are ingested.

## Candidate State Machine

### Payroll Period State

- `open`: variables can be entered.
- `processing`: payroll run is being calculated or reviewed.
- `approved`: reviewed and ready for payslips/payment/accounting.
- `paid`: salary payment evidence is linked.
- `closed`: period protected from normal mutation.
- `reopened`: controlled reopening with reason and audit.

### Payroll Run State

- `draft`: run prepared but not calculated.
- `calculated`: results generated.
- `pending_review`: results require review/approval.
- `approved`: results approved.
- `cancelled`: run cancelled before final effects or through controlled reversal.
- `superseded`: replaced by a recalculation run.

### Payslip State

- `generated`: payslip created from approved run result.
- `published`: available to employee/authorized role.
- `corrected`: superseded by a corrected payslip.
- `voided`: invalidated through controlled cancellation/recalculation path.

## Accounting Boundary

Payroll provides accounting source events, not direct ledger edits. [[Contabilidade ERP]] should consume approved payroll evidence such as:

- salary cost by employee/department/cost center;
- employee deduction liabilities;
- employer charges where legally/business applicable;
- payroll adjustments;
- reversal or correction events;
- payroll payment clearing information from [[Tesouraria ERP]].

Accounting postings should reference approved payroll run lines or summarized source batches. They should not read editable employee master data as if it were final payroll evidence.

## Treasury Boundary

Payroll creates payment obligations; [[Tesouraria ERP]] executes and reconciles payments.

Rules to preserve:

- approved payroll creates salary payable/payment batch evidence;
- actual payment status is derived from treasury movements or payment batch confirmation;
- bank/payment data is sensitive and access-controlled;
- cancellation after payment requires a controlled correction/reversal process, not silent payslip mutation.

## Permission And Privacy Boundary

Payroll requires stronger access control than ordinary operational modules:

- view employee profile;
- view salary/remuneration;
- edit HR master data;
- edit payroll variables;
- process payroll;
- approve payroll;
- publish payslips;
- export payment files;
- view payroll accounting summaries;
- view audit logs;
- reopen/cancel payroll periods.

These should be separate permissions. A generic tenant admin should not automatically see all salary details unless the launch role model intentionally grants it.

## Audit, Security And Tenancy

- Payroll data must be tenant-scoped and protected by RLS.
- Salary, bank and personal data require restricted access and private storage rules.
- Payroll calculations should be reproducible from stored rule versions and input variables.
- Payroll run approval, cancellation, recalculation and period reopening require explicit reason and audit trail.
- Payslips should be immutable once published; corrections should create replacement evidence.
- Closed periods should block silent mutation of variables, calculations and payslips.
- AI access to payroll data should be disabled or highly restricted until a dedicated security design exists.

## Critical Domain Events

- `payroll.employee_created`
- `payroll.employment_terms_changed`
- `payroll.variable_recorded`
- `payroll.run_started`
- `payroll.run_calculated`
- `payroll.run_approved`
- `payroll.run_cancelled`
- `payroll.run_recalculated`
- `payroll.payslip_generated`
- `payroll.payslip_published`
- `payroll.payment_batch_created`
- `payroll.accounting_batch_created`
- `payroll.period_closed`
- `payroll.period_reopened`

## Cabo Verde Compliance Notes

The current wiki has ERP workflow references for payroll, but it does not yet contain verified current Cabo Verde legal rules for payroll deductions, social security, income tax, statutory reports or labor obligations. Treat payroll compliance as unresolved.

Implementation caution:

- do not hard-code deduction rates or thresholds from memory;
- do not claim INPS/tax/reporting support until authoritative sources are ingested;
- do not expose payroll advice through [[IA Assistente ERP]] without current legal sources and uncertainty markers;
- design the schema so legal rule versions can change over time.

## MVP Acceptance Criteria

For the first sellable release, payroll is acceptable only if its scope is explicit:

- If payroll is not in MVP, employee/salary placeholders must not pretend to calculate statutory payroll.
- If payroll is in MVP, all employee/payroll data is tenant-scoped and permission-restricted.
- Payroll runs are period-based and auditable.
- Calculation results are reproducible from stored inputs and rule versions.
- Payslips are generated from approved results, not editable free text.
- Payment status is linked to treasury evidence or clearly out of scope.
- Accounting export/posting evidence references approved payroll runs.
- Legal deductions and statutory reports are implemented only from current verified sources.

## Non-MVP Until Confirmed

- Full Cabo Verde statutory payroll calculation without legal ingestion.
- Automated statutory report filing.
- Employee self-service portal.
- Manager approvals and leave workflow depth.
- Complex benefits administration.
- Multi-country payroll.
- AI payroll advice or autonomous payroll corrections.

## Open Questions

- Should payroll be phase two/three, or must minimal payroll ship in the first sellable release?
- Which current Cabo Verde payroll deductions, employer obligations and reports must be supported?
- What launch roles can view salary data?
- Should payslips be employee-accessible or HR/accountant-only in the first release?
- Should salary payments generate treasury batches automatically or remain manual-first?
- What accounting granularity is required: per employee, department, cost center or summarized batch?

## Next Ingestion Targets

- Current Cabo Verde legal/payroll sources for deductions, social security, income tax, labor obligations and statutory reporting.
- ~~RPG001 — Using — Processamento de Salários~~ — **ingested** as [[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]].
- `docs/docsfiscal/Configuring - Recursos Humanos (2023-v1.0-PT).pdf` (optional HR config detail).
- `docs/docsfiscal/Exercícios - Using - Processamento Salarios (2023-v0.1-PT).pdf`
- `docs/docsfiscal/Exercícios - Configuring - Recursos Humanos (2023-v1.0-PT) .docx`
