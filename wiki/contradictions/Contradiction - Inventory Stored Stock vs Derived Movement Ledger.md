---
type: contradiction
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [contradiction, inventory, stock, valuation, schema, implementation-review, needs-review]
sources: ["[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]", "nova-erp/supabase/migrations/00006_inventory_schema.sql"]
related: ["[[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]]", "[[Inventario ERP]]", "[[SAF-T CV]]"]
confidence: high
---

# Contradiction — Inventory: Stored Stock vs Derived Movement Ledger

## Disputed Claim

How is on-hand stock (and its cost) represented: a **derived projection** over an immutable movement ledger, or a **stored quantity** mutated in place?

## Position A — Derived ledger (design / ADR)

[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]] decides stock is "the **derived sum of an append-only movement ledger**, never a mutable quantity column", with **no `quantity_on_hand` column**, explicit `valuation_layers` for cost, a separate `stock_reservations` ledger (reduces *available*, not *on-hand*), `stock_counts`/`stock_count_lines` for reconciliation, and reversals as compensating movements. The ADR **explicitly rejects** the stored-quantity alternative: *"keep a `products.quantity` column updated transactionally… Why not: destroys audit/valuation history, breaks SAF-T inventory, races under concurrency."*

- Source: [[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]

## Position B — Stored accumulator (implementation)

`00006_inventory_schema.sql` ships `stock_items` with **stored** `qty_on_hand`, `qty_reserved`, `avg_cost` (and a generated `qty_available = qty_on_hand − qty_reserved`). A trigger `update_stock_on_movement` **upserts and mutates** `qty_on_hand` (`+v_delta`) and recomputes `avg_cost` in place on each `stock_movements` insert. There are **no** `valuation_layers`, **no** `stock_reservations` ledger (reservation is a stored field), **no** `stock_counts` tables, and **no** `lots`/`serials`. The trigger handles INSERT only (no delete/reversal path observed).

- Source: `nova-erp/supabase/migrations/00006_inventory_schema.sql`

## Current Best Interpretation

The implementation ships exactly the snapshot-accumulator pattern the ADR rejected. It is simpler and adequate for a basic MVP, but it (a) keeps no auditable per-layer cost history, (b) recomputes weighted-average destructively, (c) has no reservation ledger or count-reconciliation trail, and (d) the INSERT-only trigger means corrections rely on new compensating movements being entered correctly or the accumulator drifts. The movement ledger (`stock_movements`) **does** exist, so on-hand could still be recomputed/audited from it — the divergence is that the *source of truth* is the stored `stock_items`, not the ledger.

This is the highest-impact divergence for [[SAF-T CV]] inventory readiness and accounting COGS auditability.

## Confidence

High (read directly from the migration).

## What Would Resolve It

A founder decision per [[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]]:

- **Conform to ADR:** treat `stock_items` as a cached projection (rebuildable from `stock_movements`), add `valuation_layers`, a reservation ledger and `stock_counts`; make the ledger the source of truth.
- **Amend ADR:** accept the stored accumulator for MVP and downgrade the inventory ADR's "no stored quantity" principle to a post-MVP target, documenting the SAF-T/COGS audit tradeoff explicitly.
- Either way: confirm reversal/delete handling and concurrency safety of the trigger.
