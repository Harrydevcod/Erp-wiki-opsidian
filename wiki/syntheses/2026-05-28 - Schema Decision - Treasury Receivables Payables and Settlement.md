---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-30
decision_status: provisional
tags: [schema, architecture, treasury, receivables, payables, settlement, nova-erp]
sources: ["[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2023 - Cegid Primavera Tesouraria (Legacy Reference)]]"]
related: ["[[NOVA-ERP]]", "[[Tesouraria ERP]]", "[[Compras e Vendas ERP]]", "[[Faturacao Eletronica]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: medium
---

# Schema Decision - Treasury Receivables, Payables and Settlement

## Decision

NOVA-ERP models treasury as an **obligation-and-movement ledger**, not a `paid` flag on documents. A fiscal document with payment terms creates one or more `obligations` (receivable or payable). Money entering or leaving a cash/bank account is a `treasury_movement`. Settlement is an explicit many-to-many `allocations` table linking movements to obligations, so partial payments, overpayments, advances and one-payment-covers-many-invoices are all representable. Payment status of any document is **derived** from the sum of its allocations, never stored as a mutable boolean. Reversals are new compensating rows, never deletes. Bank reconciliation matches imported statement lines to treasury movements. Everything is tenant-scoped under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] and anchors to the headers from [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]].

## Scope

- Module: [[Tesouraria ERP]].
- Tables/objects: `treasury_accounts`, `obligations`, `treasury_movements`, `allocations`, `bank_statements`, `bank_statement_lines`, `reconciliations`, `current_account_entries` (view/projection).
- Workflows affected: receivable/payable generation, receipt/payment registration, settlement allocation, reversal, reconciliation, current-account statements.
- Tenancy boundary: all rows carry `tenant_id`; RLS per foundation ADR; treasury actions gated by `has_permission` keys (`treasury.pay`, `treasury.reverse`, `treasury.reconcile`, `treasury.account_admin`).

## Source Basis

- Product source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]].
- Technical source: [[2026-05-28 - DATABASE ER Diagram Snapshot]] (`financial_transactions`, `bank_accounts` as adapt candidates).
- Legacy workflow reference: [[2023 - Cegid Primavera Tesouraria (Legacy Reference)]] — corroborates the obligation (*pendente*) / movement / allocation split, the derived (no stored `paid` flag) settlement model, reversal via anulação/estorno, and bank reconciliation; supplies the allocation operation taxonomy (total/partial/encontro/excesso/novo-pendente), the *Itens de Tesouraria* rubric dimension, the caixa session lifecycle and the withholding-to-State pattern. PT bank-export formats and cheque/letra workflows are not authority here.
- Inference: the obligation/movement/allocation split is an architecture inference grounded in standard double-entry treasury practice and the snapshot's flat `financial_transactions`.

## Context

[[2026-05-28 - Current Database Snapshot Classification]] flagged `financial_transactions` and `bank_accounts` as adapt candidates and [[Tesouraria ERP]]'s MVP criteria already demand "payment status is derived, not hand-edited" and "reversals preserve evidence." The snapshot's flat `financial_transactions` cannot express partial settlement or one-payment-many-invoices cleanly. This ADR fixes the treasury core so the document-core ADR's "payment status derived from Tesouraria allocations" rule has a concrete home, and so [[Contabilidade ERP]] receives settlement postings from a defined source.

## Data Model

- Entity/table: `treasury_accounts`
  - Key fields: `id`, `tenant_id`, `kind` (`cash|bank`), `name`, `currency`, `iban`/`account_number` (nullable), `opening_balance`, `status`.
  - Note: current balance is derived from movements, not stored authoritative.

- Entity/table: `obligations`
  - Key fields: `id`, `tenant_id`, `direction` (`receivable|payable`), `entity_id` (fk `entities`), `source_document` (polymorphic: fiscal_document/commercial_document + id), `currency`, `amount_total`, `due_date`, `status` (derived: `open|partially_settled|settled|written_off|reversed`), `created_at`.
  - Relationships: created from a fiscal document (issued invoice → receivable; supplier invoice → payable); N allocations.
  - Constraints: `amount_total` immutable; status is a computed projection from allocations, not a hand-set column (may be a maintained cache refreshed on allocation change, but never directly editable).

- Entity/table: `treasury_movements`
  - Key fields: `id`, `tenant_id`, `account_id` (fk), `direction` (`in|out`), `amount`, `currency`, `value_date`, `method` (`cash|transfer|card|cheque|other`), `reference`, `counterparty_entity_id` (nullable), `treasury_item_id` (nullable — *Item de Tesouraria* / rubric for budget-vs-actual, see below), `cash_session_id` (nullable — set for cash-account movements), `reversed_by` (nullable self-fk), `created_at`, `created_by`.
  - Constraints: append-only; a reversal is a new movement with opposite direction referencing the original via `reversed_by`.

- Entity/table: `treasury_items` (rubrics) — legacy *Itens de Tesouraria*
  - Key fields: `id`, `tenant_id`, `name`, `kind` (`receipt|payment|both`), optional `budget` link.
  - Rationale: groups movement values for budget-vs-actual treasury analysis (Painel de Bordo, Acumulados por Item). Open question below: whether to reuse the generic analytical-dimension layer instead of a treasury-local catalog.

- Entity/table: `cash_sessions` (caixa) — for `treasury_accounts.kind = cash`
  - Key fields: `id`, `tenant_id`, `account_id`, `opened_at`, `opened_by`, `opening_balance`, `closed_at`, `closed_by`, `closing_balance`, `status` (`open|closed`).
  - Rationale: legacy caixa lifecycle — open creates a session/diário assigned to all movements until close; close is gated on balance reconciliation; operator is attributed. Powers POS-style cash control and the Estado das Caixas history.

- Entity/table: `allocations`
  - Key fields: `id`, `tenant_id`, `movement_id` (fk), `obligation_id` (fk), `amount`, `created_at`, `created_by`, `reversed_by` (nullable).
  - Constraints: unique active (`movement_id`, `obligation_id`); sum of active allocations on a movement cannot exceed the movement amount; sum on an obligation cannot exceed `amount_total` (overpayment handled as an explicit `on_account` obligation, see below).
  - Rationale: this is the join that makes settlement many-to-many and partial-safe.

- Overpayment / advance handling: an unallocated inflow stays as a movement with remaining balance; an explicit `on_account` obligation (direction inverted) can absorb advances so the customer current account stays correct. Resolves the "over/underpayment" open question. Legacy-corroborated by Cegid's auto-generated *valores em excesso* (VEC) document.
- Allocation operation taxonomy (legacy-validated): an `allocations` row, or a small set of allocation operations over it, covers Cegid's settlement modes — *total*, *partial*, **encontro de valores** (offset two opposite-nature obligations to net zero via paired allocations), **valores em excesso** (overpayment → `on_account`), **liquidação com novo pendente** (carry remaining balance into a new obligation, e.g. letra), and contra-settlement across **entidades associadas** (a party that is both customer and supplier). All are representable as allocations + (optionally) a new obligation, with no stored status mutation.

- Entity/table: `bank_statements`, `bank_statement_lines`
  - Key fields (lines): `id`, `tenant_id`, `statement_id`, `value_date`, `amount`, `direction`, `description`, `matched_movement_id` (nullable).
  - Purpose: import target for reconciliation; manual-first, import/API-ready later.

- Entity/table: `reconciliations`
  - Key fields: `id`, `tenant_id`, `account_id`, `period`, `status` (`open|reconciled`), `reconciled_balance`, `reconciled_at`, `reconciled_by`.

- Projection: `current_account_entries`
  - A per-`entity` ledger derived from obligations + allocations (not a hand-maintained table). Powers customer/supplier statements.

## State And Events

- State: `obligations.status` (derived): `open -> partially_settled -> settled`; side states `written_off`, `reversed`.
- State: `treasury_movements`: effectively immutable; lifecycle expressed via `reversed_by`.
- State: `bank_statement_lines.matched_movement_id`: null → set on reconciliation.
- Event (to `audit_log`): `obligation.created`, `treasury_movement.recorded`, `allocation.created`, `allocation.reversed`, `treasury_movement.reversed`, `reconciliation.completed`. Align with treasury permissions in [[Permissoes e Auditoria ERP]].
- Transition rule: a settled obligation can only return to open via an explicit `allocation.reversed` (which also audits); documents are never mutated by treasury.

## Alternatives Considered

- Alternative: keep snapshot `financial_transactions` flat with a `document_id` + `paid` boolean.
  Why not: cannot express partial settlement, one payment across many invoices, advances, or reversal-with-evidence.
- Alternative: store running balance on `obligations`/`treasury_accounts`.
  Why not: authoritative stored balances drift; derive from immutable movements + allocations.
- Alternative: model settlement as a direct FK movement→obligation (1:1).
  Why not: breaks one-payment-many-invoices and partial allocations; the `allocations` join is necessary.

## Consequences

- Positive: derived payment status satisfies the document-core and Tesouraria MVP rules; partial/advance/bulk payments all representable; full audit via append-only movements.
- Positive: accounting receives clean settlement events from `allocations`.
- Tradeoff: more tables and computed-status logic than a `paid` flag; needs allocation-sum constraints (triggers or app-enforced + tested).
- Migration impact: snapshot `financial_transactions` splits into `obligations` + `treasury_movements` + `allocations`; `bank_accounts` → `treasury_accounts`.
- Operational impact: balances and current accounts become queries/projections, requiring sensible indexes.

## Validation Plan

- Test: one payment allocated across two invoices settles both correctly and sums match.
- Test: partial payment moves an obligation to `partially_settled`; remaining balance correct.
- Test: overpayment leaves an `on_account` balance, not a negative obligation.
- Test: reversing an allocation returns the obligation to the prior derived status and writes an audit row.
- Test: a treasury movement cannot be hard-deleted; reversal creates a compensating movement.
- Test: cross-tenant isolation on every treasury table (inherits foundation ADR gates).
- Fixture/source: payment scenarios from [[2026-05-26 - Backlog Estruturado NOVA-ERP]].

## Open Questions

- Multi-currency: are obligations and movements always same-currency, or does settlement need FX gain/loss handling in MVP? (Leaning: single-currency MVP, FX later.)
- Should `obligations.status` be a maintained cache column or a pure view? (Performance vs simplicity.)
- Should advances/`on_account` be a first-class obligation type or a separate `advances` table?
- Bank reconciliation: manual-first MVP confirmed (legacy corroborates manual + automatic), but which CV import format (CSV/CAMT/API) ships first?
- Should write-offs require accounting approval before treasury can close an obligation?
- Should *Itens de Tesouraria* (rubrics) reuse the generic [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]] layer, or be a treasury-local `treasury_items` catalog?
- Is a full **cash-session (caixa)** model needed for POS-style use in MVP, or only bank/DO accounts first?
- How is **withholding to the State** modeled — a treasury obligation to a State entity, an accounting-only tax map, or both? (Connects to [[Processamento de Salarios ERP]] IRPS/INPS and the document core.)
- Obligation side-states beyond `written_off`: do we need an **approval** state (legacy `AGP→APR` payable approval) and a **doubtful-debtor** transfer, as statuses or as an account-transfer log?
- Are **letras / pre-dated cheques / payment plans (installments)** in CV scope or deferred?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are inspected and when the backlog's MVP treasury scope is confirmed.
- Depends on [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] and [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]; feeds the upcoming accounting ADR.
- Related log entry: 2026-05-28 treasury schema decision.
