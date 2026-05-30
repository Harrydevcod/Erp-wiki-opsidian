---
type: contradiction
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [contradiction, treasury, documents, payment-status, schema, implementation-review, needs-review]
sources: ["[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "nova-erp/supabase/migrations/00004_documents_schema.sql", "nova-erp/supabase/migrations/00008_treasury_schema.sql", "nova-erp/supabase/migrations/20260404100000_align_domain_schema.sql"]
related: ["[[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]]", "[[Tesouraria ERP]]", "[[Compras e Vendas ERP]]"]
confidence: high
---

# Contradiction — Payment Status: Stored vs Derived from Allocations

## Disputed Claim

Is a document's payment status (`paid` / `partial_paid` / `overdue`) a **stored, mutable field** on the document, or a value **derived** from the sum of treasury allocations?

## Position A — Derived (design / ADR)

[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]] models treasury as an **obligation-and-movement ledger, "not a `paid` flag on documents."** A document with payment terms creates `obligations`; money is a `treasury_movement`; settlement is an m:n `allocations` table; **"payment status of any document is *derived* from the sum of its allocations, never stored as a mutable boolean."** Reversals are compensating rows. [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]] aligns: the fiscal document "never embeds … transmission columns" and payment is external.

- Source: [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]

## Position B — Stored (implementation)

`00004_documents_schema.sql` gives `documents.status` an enum that **includes `paid`, `partial_paid`, `overdue`**. The `settle_document()` function (migration `20260404100000_align_domain_schema.sql`) loads the document `FOR UPDATE`, computes `v_new_paid`/`v_new_status`, and **writes the payment status back onto the document row**. There is **no `obligations` table**; the document is the implicit obligation. Settlement does exist as `payments` + `payment_allocations` (00008), so the allocation ledger is present — but status is **stored** on the document, not projected from allocations.

- Source: `nova-erp/supabase/migrations/00004_documents_schema.sql`, `.../00008_treasury_schema.sql`, `.../20260404100000_align_domain_schema.sql`

## Current Best Interpretation

A **partial** divergence. The settlement substrate (`payments`/`payment_allocations`) matches the ADR's movement/allocation intent, so partial/advance/bulk payments are representable. But the *payment status* is denormalized onto `documents.status` and maintained procedurally by `settle_document()`, which is exactly the "mutable boolean" the ADR forbade — risking drift if allocations are reversed/edited outside `settle_document`, and mixing operational state with payment state in one enum. The obligation layer is collapsed into the document (defensible for single-installment terms; weaker for payment plans / multi-obligation documents).

## Confidence

High (read directly from the migrations and the `settle_document` body).

## What Would Resolve It

- **Conform to ADR:** derive payment status from `payment_allocations` (a view/computed read), keep `documents.status` for operational lifecycle only; reconcile any reversal path through `settle_document`.
- **Amend ADR:** accept stored `documents.status` payment values for MVP, and require **all** payment mutations to route through `settle_document()` (no out-of-band allocation edits), documenting the drift risk and how payment plans are handled.
