---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-30
tags: [erp-module, tesouraria, financeiro, bancos, caixa]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Faturacao Eletronica]]", "[[Permissoes e Auditoria ERP]]", "[[2023 - Cegid Primavera Tesouraria (Legacy Reference)]]"]
related: ["[[NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Compras e Vendas ERP]]", "[[Faturacao Eletronica]]", "[[Fiscalidade Cabo Verde]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]"]
confidence: medium
---

# Tesouraria ERP

## Purpose

Tesouraria ERP is the treasury, cash, bank, receivables, payables and account-current control layer for NOVA-ERP.

## Role In NOVA-ERP

Treasury connects operational documents to financial reality. Sales and purchases create expected receivables and payables; treasury controls receipts, payments, cash, bank accounts, allocations, advances, compensations, retentions, reversals, credit exposure, overdue balances and reconciliation.

Treasury must not be reduced to a `paid` flag on a document. It needs independent financial movements that can be allocated to fiscal/commercial documents, audited, reversed and posted into [[Contabilidade ERP]].

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Contabilidade ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- ERP workflow reference: [[2023 - Cegid Primavera Tesouraria (Legacy Reference)]] (ingested; PT bank-export/cheque/letra workflows not authority)
- Exercises (raw): `docs/docsfiscal/Exercícios - Using - Tesouraria (2023-VC1-PT).docx`
- Fiscal/accounting boundary: [[Faturacao Eletronica]], [[Fiscalidade Cabo Verde]], [[Contabilidade ERP]]
- Security boundary: [[Permissoes e Auditoria ERP]]

## Design Gates Before Implementation

- Source authority gate: ingest treasury reference documents before finalizing full workflow depth.
- Document boundary gate: decide which fiscal/commercial documents create receivables/payables and when.
- Accounting boundary gate: define when treasury movements generate accounting entries and how they link to periods.
- Reconciliation gate: decide whether MVP uses manual reconciliation only or supports bank import/API.
- Security/audit gate: define permissions for receipts, payments, reversals, bank reconciliation and payment-status changes.

## Core Workflows

- Generate receivables from issued sales/fiscal documents.
- Generate payables from purchase/supplier documents.
- Register receipts and payments.
- Allocate payments/receipts to one or more documents.
- Manage partial payments, overpayments, advances and compensations.
- Manage cash accounts and bank accounts.
- Track customer and supplier account-current positions.
- Support credit limits and overdue visibility.
- Reverse or correct treasury movements through auditable flows.
- Prepare data for bank reconciliation and accounting integration.

## Required Master Data

- Cash accounts.
- Bank accounts.
- Payment methods.
- Payment terms.
- Customer and supplier financial profiles.
- Credit limits.
- Treasury document types and series.
- Reconciliation rules/import formats where applicable.
- Retention/statutory payment profiles where confirmed.

## Candidate Domain Model

- `financial_accounts`: tenant-owned cash/bank accounts, currency, active state and accounting mapping.
- `payment_methods`: cash, bank transfer, card, cheque, mobile/payment provider or other configured methods.
- `payment_terms`: due date rules, installments, grace periods and default terms by entity/document.
- `receivables`: amounts expected from customers, source document, due date, open/settled status.
- `payables`: amounts owed to suppliers/others, source document, due date, open/settled status.
- `treasury_movements`: receipts, payments, transfers, advances, compensations, reversals and adjustments.
- `treasury_allocations`: allocation of one movement to one or more receivables/payables/documents.
- `bank_statement_imports`: imported bank statement file/API batch metadata.
- `bank_statement_lines`: bank line items awaiting match/reconciliation.
- `reconciliation_matches`: links between bank lines and treasury movements.
- `credit_exposure_snapshots`: customer/supplier current balance and overdue exposure snapshots.

The provisional target schema is now consolidated in [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]: `receivables`/`payables` unify into a single `obligations` table (with `direction`); `treasury_movements` are append-only; `allocations` is the many-to-many settlement join that makes payment status derived; reversals are compensating rows; overpayments become `on_account` balances. This model is provisional until the treasury source documents and current banking/statutory requirements are ingested.

## Candidate State Machine

### Receivable/Payable State

- `open`: expected amount exists and is unpaid.
- `partially_settled`: some amount is allocated.
- `settled`: fully paid/received.
- `overdue`: due date passed with open balance.
- `cancelled`: source document or obligation is cancelled through a controlled path.
- `written_off`: intentionally written off with approval/audit.

### Treasury Movement State

- `draft`: prepared but not confirmed.
- `confirmed`: affects cash/bank/account-current.
- `allocated`: linked to receivable/payable/document.
- `reconciled`: matched to bank/cash evidence.
- `reversed`: neutralized by reversal movement.

## Integration Points

- [[Compras e Vendas ERP]] creates commercial/fiscal obligations.
- [[Faturacao Eletronica]] provides issued fiscal documents and invoice-receipt cases.
- [[Contabilidade ERP]] consumes confirmed treasury movements for accounting postings.
- [[Fiscalidade Cabo Verde]] may affect retentions, document status or fiscal reporting.
- [[Permissoes e Auditoria ERP]] controls who can receive, pay, reconcile, reverse or alter financial status.
- Dashboards should expose liquidity, overdue balances, cash flow and credit exposure.

## Accounting Boundary

Treasury provides accounting source events such as:

- receipt confirmed;
- payment confirmed;
- bank transfer confirmed;
- movement reversed;
- reconciliation completed;
- write-off approved;
- advance applied;
- compensation applied.

Accounting should post from confirmed/auditable treasury events, not from casual UI changes to a document's payment status.

## Audit, Security And Tenancy

- Treasury movements must be tenant-scoped and auditable.
- Reversals should preserve the original movement and reason.
- Bank and cash operations require role-based permissions.
- Changing a document's settled status should happen through allocation/reversal, not direct mutation.
- Bank reconciliation should preserve import/match evidence.
- Closed accounting periods should protect historical financial data from silent mutation.
- Payment proofs and bank attachments should live in private storage with explicit access rules.

## Critical Domain Events

- `treasury.receivable_created`
- `treasury.payable_created`
- `treasury.receipt_confirmed`
- `treasury.payment_confirmed`
- `treasury.movement_allocated`
- `treasury.movement_reversed`
- `treasury.bank_statement_imported`
- `treasury.reconciliation_matched`
- `treasury.writeoff_approved`
- `treasury.credit_limit_changed`

## Cabo Verde Compliance Notes

Current wiki evidence is mostly product intent and ERP workflow reference. Any tax retention, statutory payment, banking integration or official reporting claim requires deeper Cabo Verde-specific verification.

Fiscal caution:

- invoice-receipts and immediate-settlement documents should be aligned with [[Faturacao Eletronica]];
- retention/reverse-charge/statutory payment behavior needs current legal verification;
- treasury data may feed IVA, accounting and SAF-T outputs, but exact current requirements remain unresolved.

## MVP Acceptance Criteria

For the first sellable release, treasury is acceptable only if:

- receivables/payables are tenant-scoped and linked to source documents;
- receipts/payments are recorded as treasury movements, not direct status edits;
- partial settlement is possible or explicitly out of scope;
- reversals preserve original movement and reason;
- current account balance can be derived from movements/allocations;
- payment status on documents is derived from allocations;
- permissions separate receiving, paying, reversing and reconciling;
- confirmed movements can be linked to accounting later even if full accounting is deferred.

## Non-MVP Until Confirmed

- Automatic bank API integration.
- Complex cash-flow forecasting.
- Multi-bank reconciliation automation.
- Statutory retention/payment automation without current legal ingestion.
- Advanced credit-risk scoring.
- Foreign exchange gains/losses unless multi-currency is in first-release scope.

## Open Questions

- Which treasury workflows are mandatory for the first sellable release?
- Should bank reconciliation be manual-first or designed for import/API from day one? (Provisionally manual-first MVP in the treasury ADR; import format still open.)
- Which retentions or statutory payments apply in Cabo Verde and must be modeled?
- Should invoice-receipts create both fiscal document and treasury movement in one transaction?
- What minimum account-current view is required for customers and suppliers?

## Next Ingestion Targets

- ~~FPG001 — Using — Tesouraria~~ — **ingested** as [[2023 - Cegid Primavera Tesouraria (Legacy Reference)]].
- `docs/docsfiscal/Exercícios - Using - Tesouraria (2023-VC1-PT).docx` (exercises — only if concrete workflow data is still needed).
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`

