---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-30
decision_status: provisional
tags: [schema, architecture, documents, sales, purchases, fiscal, nova-erp]
sources: ["[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2022 - Cegid Primavera Compras e Vendas (Legacy Reference)]]"]
related: ["[[NOVA-ERP]]", "[[Compras e Vendas ERP]]", "[[Faturacao Eletronica]]", "[[Inventario ERP]]", "[[Tesouraria ERP]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: medium
---

# Schema Decision - Commercial and Fiscal Document Core

## Decision

NOVA-ERP separates **commercial documents** (quote, order, delivery, return — operational intent) from **fiscal documents** (legally regulated invoices and corrective documents that own a fiscal series, number and e-Fatura obligation). They share a common line/total structure and are connected by an explicit `document_links` graph rather than by mutating one row through every stage. Commercial numbering is independent from fiscal series numbering. A fiscal document is the single business header that the existing e-Fatura decisions hang off: it points to its DFE payload, transmission state, references and evidence, but never embeds signed XML or transmission columns. The snapshot's single `documents`/`document_items`/`document_series` triple is **split**, not adapted as-is. Every table is tenant-scoped under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]].

## Scope

- Module: [[Compras e Vendas ERP]] (commercial), [[Faturacao Eletronica]] (fiscal header).
- Tables/objects: `entities`, `commercial_documents`, `commercial_document_lines`, `fiscal_documents`, `fiscal_document_lines`, `document_series`, `document_links`, plus shared `tax_rates`, `units`, `price_lists`.
- Workflows affected: quote→order→delivery→invoice transformation; fiscal issuance; stock and treasury triggers; corrective documents.
- Tenancy boundary: all rows carry `tenant_id`; RLS per the foundation ADR. Catalogs (`tax_rates`, `units`) may be system + tenant-overridable.

## Source Basis

- Product source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]].
- Compliance source: [[2026-05-28 - Manual de Faturas em Cabo Verde]] (numbering, no-deletion-after-assignment, rectification documents), [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] (fiscal document/DFE shape).
- Technical source: [[2026-05-28 - DATABASE ER Diagram Snapshot]] (`documents`, `document_items`, `document_series` as adapt/split candidates).
- Legacy workflow reference: [[2022 - Cegid Primavera Compras e Vendas (Legacy Reference)]] — corroborates the entity unification, the commercial/fiscal split (its *séries emissíveis vs não emissíveis*), the `document_links` graph (its five reproduction mechanisms over one quantity-traceable graph) and the no-deletion/two-correction-paths model (anulação vs estorno/crédito). PT fiscal obligations in that deck are explicitly **not** authority here.
- Inference: the commercial/fiscal split, the `document_links` graph and the entity unification are architecture inferences grounded in those sources.

## Context

[[2026-05-28 - Current Database Snapshot Classification]] flagged `documents`/`document_items`/`document_series` as "fiscal document core, heavily refactored." The e-Fatura payload, event, middleware and evidence ADRs already exist but assume a clean `fiscal_documents` header to attach to — that header was never specified. [[Compras e Vendas ERP]]'s standing open questions ("which commercial types ship MVP", "one commercial doc → multiple fiscal docs?", "returns commercial or fiscal?") and [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]'s open question ("should the header be `fiscal_documents`, `sales_documents`, or split?") both resolve here. This ADR fixes the header so downstream stock/treasury/accounting/e-Fatura boundaries have a stable anchor.

## Data Model

- Entity/table: `entities`
  - Key fields: `id`, `tenant_id`, `kind` (`customer|supplier|both`), `name` (commercial), `legal_name` (fiscal — printed on documents/maps when set, else falls back to `name`), `tax_id` (NIF), `country`, `address` jsonb, `email`, `status`, `is_generic` (sentinel for occasional/indiferenciados parties).
  - Rationale: customers and suppliers unify into one party master with a role flag; a party is frequently both. Resolves the "unify customers/suppliers?" open question as **yes, unified with role kind**. The commercial-vs-fiscal name split and the generic-party sentinel come from [[2022 - Cegid Primavera Compras e Vendas (Legacy Reference)]] (Nome Comercial vs Nome Fiscal; `VD`/`FVD` occasional codes).
  - Constraints: unique (`tenant_id`, `tax_id`) where tax_id not null and not generic. **`tax_id` is immutable once a certified/issued fiscal document references the entity** (legacy-validated); the NIF on a fiscal document is validated against the entity's `tax_id`. Generic parties carry `name`/`tax_id` inline on the document instead.

- Entity/table: `commercial_documents`
  - Key fields: `id`, `tenant_id`, `type` (`sales_quote|sales_order|delivery_note|sales_return|purchase_order|goods_receipt|purchase_return`), `direction` (`sales|purchase`), `entity_id`, `number` (commercial series), `status`, `currency`, `issue_date`, `totals` (net/tax/gross), `notes`.
  - Constraints: commercial `number` independent of fiscal series.

- Entity/table: `commercial_document_lines`
  - Key fields: `id`, `document_id`, `line_no`, `item_id` (nullable for free text), `description`, `qty`, `unit_id`, `unit_price`, `discount`, `tax_rate_id`, `net`, `tax`, `gross`.

- Entity/table: `fiscal_documents`
  - Key fields: `id`, `tenant_id`, `dfe_type` (per v11.0 vocabulary: FT/FR/NC/ND/etc.), `series_id` (fk `document_series`), `number` (assigned from series, immutable once set), `entity_id`, `issue_date`, `status`, `currency`, totals snapshot (net/tax/gross), `tax_breakdown` jsonb, `issue_reason_code`, `created_at`.
  - Relationships: 1:1 with a DFE payload (see e-Fatura ADR); 0:N references via `document_links`.
  - Constraints: number assignment is gap-controlled per series; no hard delete after number assignment ([[2026-05-28 - Manual de Faturas em Cabo Verde]]) — voiding/anulation goes through the e-Fatura event ADR, not row deletion.
  - RLS/security: issuing and viewing raw fiscal detail gated by `has_permission` keys (`invoice.issue`, `fiscal.view`) per foundation ADR.

- Entity/table: `fiscal_document_lines`
  - Mirrors commercial lines but is an **immutable snapshot** at issuance (price, tax, description frozen for the legal record).

- Entity/table: `document_series`
  - Key fields: `id`, `tenant_id`, `scope` (`commercial|fiscal`), `dfe_type` (for fiscal), `prefix`, `current_number`, `year`, `status`.
  - Constraints: fiscal series enforce monotonic, gapless numbering with audited resets.

- Entity/table: `document_links`
  - Key fields: `id`, `tenant_id`, `from_document` (polymorphic: table + id), `to_document`, `relation` (`transforms_into|invoices|corrects|returns|references`).
  - Rationale: transformations (quote→order→invoice), one-commercial→many-fiscal, corrective documents and returns are all edges in one graph instead of FK columns scattered across tables.

## State And Events

- State: `commercial_documents.status`: `draft -> confirmed -> partially_fulfilled -> fulfilled -> cancelled`.
- State: `fiscal_documents.status`: `draft -> number_assigned -> issued -> (e-Fatura states owned by DFE/transmission ADR) -> anulled`.
- Transition rule: a fiscal document leaves `draft` only when a series number is assigned; after `number_assigned` it can never be deleted, only anulled via an e-Fatura event.
- Event (to `audit_log`): `commercial_document.created`, `commercial_document.transformed`, `fiscal_document.number_assigned`, `fiscal_document.issued`, `document.linked`. These align with the fiscal audit events already listed in [[Permissoes e Auditoria ERP]].

## Alternatives Considered

- Alternative: keep the snapshot's single `documents` table with a `type`/`efatura_status` column.
  Why not: conflates operational intent with the legal record; cannot freeze a fiscal snapshot while a commercial doc keeps evolving; forces e-Fatura columns onto non-fiscal rows.
- Alternative: separate `customers` and `suppliers` tables.
  Why not: duplicates parties that are both; complicates a unified statement of account. Unified `entities` with `kind` is leaner.
- Alternative: FK columns for transformations (`order.invoice_id`, etc.).
  Why not: cannot express one-order→many-invoices or corrective chains cleanly; `document_links` generalizes all relations.

## Consequences

- Positive: the existing e-Fatura payload/event/middleware/evidence ADRs now attach to a defined `fiscal_documents` header.
- Positive: immutable fiscal line snapshots satisfy the no-deletion / legal-record requirement.
- Tradeoff: a polymorphic `document_links` table needs careful integrity checks (no native FK across polymorphic targets — enforce via triggers/app + validation tests).
- Migration impact: snapshot `documents`→split into `commercial_documents` + `fiscal_documents`; `document_items`→two line tables; `document_series` gains a `scope`; legacy `efatura_status` on documents is dropped in favor of the DFE/transmission tables.
- Operational impact: stock movements ([[Inventario ERP]]) and receivables/payables ([[Tesouraria ERP]]) trigger off defined document types, not a generic flag.

## Validation Plan

- Test: a confirmed fiscal document with an assigned number cannot be deleted by any tenant role.
- Test: commercial and fiscal numbering are independent (advancing one does not touch the other).
- Test: a quote transformed into an order into an invoice produces a traceable `document_links` chain.
- Test: one commercial order can link to multiple fiscal documents (partial invoicing).
- Test: fiscal line snapshot is immutable after issuance even if the source commercial line changes.
- Test: cross-tenant isolation holds for every new table (inherits foundation ADR gates).
- Fixture/source: derive document-type fixtures from [[2026-05-26 - Backlog Estruturado NOVA-ERP]] and numbering rules from [[2026-05-28 - Manual de Faturas em Cabo Verde]].

## Open Questions

- Which commercial and fiscal document types are MVP-mandatory vs later? (Backlog ingestion needed for the exact cut.)
- Should `document_links` integrity be trigger-enforced, app-enforced, or both?
- How are partial deliveries and partial invoicing quantities tracked — on lines, on links, or a fulfilment table? (Legacy-informed by [[2022 - Cegid Primavera Compras e Vendas (Legacy Reference)]]: Cegid tracks **satisfied quantity per source line** ("controlo das quantidades satisfeitas", "fecho de linhas") — leaning toward fulfilled-qty on `*_document_lines` and/or `document_links` edges, still to fix.)
- Should returns be modeled as negative commercial documents plus corrective fiscal documents, or distinct types? (Leaning: distinct commercial type + corrective fiscal document — reinforced by the legacy estorno/crédito model that creates a **distinct contrary-nature document with a mandatory origin reference**.)
- How are occasional/indiferenciados parties modeled — `is_generic` sentinel entity vs inline name+NIF on a document with null `entity_id`? (Surfaced by the legacy `VD`/`FVD` pattern.)
- What are the precondition guards for voiding/anulation? (Legacy guard list: not in a closed period, not transformed, not manually settled, not exported to assets, not already e-transmitted — to be reconciled with the e-Fatura FDC event path.)
- Do `tax_rates`/`units` ship as system catalog, tenant catalog, or hybrid?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are inspected and when the backlog's exact MVP document-type cut is ingested.
- Depends on [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; feeds [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] and the upcoming treasury/inventory/accounting ADRs.
- Related log entry: 2026-05-28 commercial and fiscal document core schema decision.
