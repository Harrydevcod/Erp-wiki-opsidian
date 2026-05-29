---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, inventory, stock, valuation, nova-erp]
sources: ["[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]"]
related: ["[[NOVA-ERP]]", "[[Inventario ERP]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[SAF-T CV]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: medium
---

# Schema Decision - Inventory Movements and Valuation

## Decision

NOVA-ERP models stock as the **derived sum of an append-only movement ledger**, never a mutable quantity column on `items`. Every stock change — receipt, delivery, return, adjustment, transfer, count reconciliation — is a `stock_movement` row tied to a source document (from [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]) and a warehouse. On-hand balance per item/warehouse is a projection over movements. Cost is tracked through explicit `valuation_layers` so the chosen method (weighted-average for MVP, FIFO-capable) is auditable and SAF-T-ready. Reservations are a separate soft-allocation ledger that reduces *available* without moving *on-hand*. Reversals are compensating movements, never deletes. All tenant-scoped under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]].

## Scope

- Module: [[Inventario ERP]].
- Tables/objects: `items`, `warehouses`, `stock_movements`, `stock_reservations`, `stock_counts`, `stock_count_lines`, `valuation_layers`, `lots`, `serials`; `stock_on_hand` and `stock_available` as projections.
- Workflows affected: goods receipt, delivery, sales/purchase returns, adjustments, transfers, physical counts, valuation, SAF-T inventory readiness.
- Tenancy boundary: all rows carry `tenant_id`; RLS per foundation ADR; adjustments/counts/valuation gated by `has_permission` keys (`inventory.adjust`, `inventory.count`, `inventory.valuation_admin`).

## Source Basis

- Product source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]].
- Compliance source: SAF-T CV inventory readiness ([[SAF-T CV]]) requires movement-grade history and valuation.
- Technical source: [[2026-05-28 - DATABASE ER Diagram Snapshot]] (`inventory_movements`, `inventory_counts`, `inventory_count_items` as adapt candidates; `products` → `items`).
- Inference: the valuation-layer and reservation-vs-on-hand split are architecture inferences grounded in standard perpetual-inventory practice.

## Context

[[2026-05-28 - Current Database Snapshot Classification]] flagged `inventory_movements`/`inventory_counts`/`inventory_count_items` as adapt candidates and [[Inventario ERP]] already asserts "stock is derived from movements, not a mutable field." The snapshot lacks explicit valuation layers and a reservation ledger, both needed for SAF-T inventory and for the document-core ADR's stock-boundary rules (which documents reserve vs move stock). This ADR fixes the inventory core so [[Compras e Vendas ERP]] triggers, [[Contabilidade ERP]] valuation postings and [[SAF-T CV]] export all read from one defined ledger.

## Data Model

- Entity/table: `items`
  - Key fields: `id`, `tenant_id`, `sku`, `name`, `kind` (`stockable|service|non_stock`), `unit_id`, `tax_rate_id`, `valuation_method` (`weighted_avg|fifo`), `tracking` (`none|lot|serial`), `status`.
  - Note: **no** `quantity_on_hand` column — on-hand is derived.
  - Shared with the document-core ADR's line `item_id`.

- Entity/table: `warehouses`
  - Key fields: `id`, `tenant_id`, `code`, `name`, `is_default`, `status`.
  - MVP: multiple warehouses supported in schema; UI may default to one. Resolves the multi-warehouse gate at schema level (model many, ship simple).

- Entity/table: `stock_movements`
  - Key fields: `id`, `tenant_id`, `item_id`, `warehouse_id`, `direction` (`in|out`), `qty`, `unit_cost` (for valuation), `movement_type` (`receipt|delivery|sales_return|purchase_return|adjustment|transfer_in|transfer_out|count_reconcile`), `source_document` (polymorphic + id, nullable for adjustments), `lot_id`/`serial_id` (nullable), `value_date`, `reversed_by` (nullable), `created_at`, `created_by`.
  - Constraints: append-only; reversal = new opposite movement referencing original.
  - Indexes: (`tenant_id`, `item_id`, `warehouse_id`, `value_date`).

- Entity/table: `stock_reservations`
  - Key fields: `id`, `tenant_id`, `item_id`, `warehouse_id`, `qty`, `source_document` (e.g. sales_order), `status` (`active|fulfilled|released`), `created_at`.
  - Rationale: reduces `stock_available` without touching `stock_on_hand`; fulfilled when the delivery movement is committed. Resolves "should sales orders reserve stock" — **yes, via reservations, not movements**.

- Entity/table: `valuation_layers`
  - Key fields: `id`, `tenant_id`, `item_id`, `warehouse_id`, `qty_remaining`, `unit_cost`, `source_movement_id`, `created_at`.
  - Purpose: FIFO consumes layers oldest-first; weighted-average recomputes a running cost. Outbound movements record the costed `unit_cost` taken from layers. Enables auditable COGS and SAF-T valuation.

- Entity/table: `stock_counts`, `stock_count_lines`
  - Key fields (lines): `id`, `tenant_id`, `count_id`, `item_id`, `warehouse_id`, `counted_qty`, `system_qty_snapshot`, `difference`, `reconciled_movement_id` (nullable).
  - Reconciliation posts difference as a `count_reconcile` movement, never a silent balance edit.

- Entity/table: `lots`, `serials`
  - Tenant-scoped; only enforced when `items.tracking` requires it. Off by default in MVP (resolves lot/serial gate: schema-ready, off unless needed).

- Projections: `stock_on_hand` (sum of committed movement qty by item/warehouse), `stock_available` (= on_hand − active reservations). Both are views/materialized projections, not hand-maintained tables.

## State And Events

- State: `stock_movements`: effectively immutable; lifecycle via `reversed_by`.
- State: `stock_reservations.status`: `active -> fulfilled | released`.
- State: `stock_counts`: `open -> counting -> reconciled -> closed`.
- Event (to `audit_log`): `stock.movement_committed`, `stock.movement_reversed`, `stock.reserved`, `stock.reservation_released`, `stock.count_opened`, `stock.count_reconciled`, `stock.valuation_changed`. Align with [[Permissoes e Auditoria ERP]] inventory events.
- Transition rule: an adjustment or count reconciliation requires permission + reason and always produces an audited movement.

## Alternatives Considered

- Alternative: keep a `products.quantity` column updated transactionally (snapshot style).
  Why not: destroys audit/valuation history, breaks SAF-T inventory, races under concurrency.
- Alternative: fold reservations into movements with a `reserved` type.
  Why not: reservations are not physical stock changes; conflating them corrupts on-hand and valuation.
- Alternative: single global valuation, no per-warehouse layers.
  Why not: per-warehouse cost is needed for transfers and accurate COGS; layers also enable FIFO later.

## Consequences

- Positive: auditable movement history + valuation layers satisfy SAF-T inventory and accounting COGS; available-vs-on-hand split supports order reservation.
- Positive: document-core stock-boundary rules now have a concrete ledger to write to.
- Tradeoff: balances/availability are queries needing good indexes/materialization; valuation logic (layer consumption) must be correct and tested.
- Migration impact: snapshot `inventory_movements` adapts into `stock_movements` (+ source-document link, + unit_cost); `inventory_counts`/`inventory_count_items` → `stock_counts`/`stock_count_lines`; `products` → `items` with valuation/tracking config; any stored quantity is dropped in favor of projections.
- Operational impact: receipts must capture `unit_cost` to feed valuation; deliveries cost out from layers.

## Validation Plan

- Test: on-hand equals the signed sum of committed movements per item/warehouse.
- Test: a sales-order reservation reduces `stock_available` but not `stock_on_hand`; delivery converts reservation to a committed out-movement.
- Test: weighted-average cost recomputes correctly across mixed-cost receipts; an out-movement records the costed unit_cost.
- Test: count reconciliation posts a `count_reconcile` movement equal to the difference; no silent balance edit.
- Test: reversing a movement restores prior on-hand and writes audit; no hard delete.
- Test: cross-tenant isolation on every inventory table (inherits foundation ADR gates).
- Fixture/source: stock scenarios from [[2026-05-26 - Backlog Estruturado NOVA-ERP]]; valuation cross-checked against [[SAF-T CV]] inventory needs once the official schema is ingested.

## Open Questions

- Weighted-average confirmed as MVP default — is FIFO needed in first sellable release or deferred?
- Should `stock_on_hand`/`stock_available` be materialized views (refresh cost) or computed on read (query cost)?
- Are negative on-hand balances ever allowed (oversell), or hard-blocked at delivery?
- How are inter-warehouse transfers costed — at source layer cost or a transfer price?
- Does MVP enable lot/serial for any item category, or is it strictly post-MVP?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are inspected, when the logistics reference (`MGP001`) is ingested, and when the official SAF-T CV inventory schema is confirmed.
- Depends on [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] and [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]; feeds the accounting ADR (COGS) and [[SAF-T CV]].
- Related log entry: 2026-05-28 inventory schema decision.
