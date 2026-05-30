---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-30
tags: [erp-module, inventario, logistica]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[Permissoes e Auditoria ERP]]", "[[2022 - Cegid Primavera Gestao de Inventario (Legacy Reference)]]", "docs/docsfiscal/LPG018- Configuring - Logística (2022-v1.0-GB).pdf"]
related: ["[[NOVA-ERP]]", "[[Compras e Vendas ERP]]", "[[Faturacao Eletronica]]", "[[SAF-T CV]]", "[[Contabilidade ERP]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]"]
confidence: medium
---

# Inventario ERP

## Purpose

Inventario ERP is the stock, warehouse, item movement and logistics control layer for NOVA-ERP.

## Role In NOVA-ERP

Inventory supports operational control and fiscal/accounting traceability. Products, services, units, lots, serial numbers, warehouses, transfers, stock counts and document-driven stock movements need to be modeled as first-class ERP behavior.

Inventory must not be a single `stock` integer on products. Stock position is derived from auditable movements, reservations, commitments, receipts, deliveries, returns, adjustments and counts.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Compras e Vendas ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- ERP workflow reference: [[2022 - Cegid Primavera Gestao de Inventario (Legacy Reference)]] (ingested; PT inventory-to-AT communication not authority)
- Configuration reference (raw): `docs/docsfiscal/LPG018- Configuring - Logística (2022-v1.0-GB).pdf`
- Commercial boundary: [[Compras e Vendas ERP]]
- Accounting/reporting boundary: [[Contabilidade ERP]], [[SAF-T CV]]
- Security boundary: [[Permissoes e Auditoria ERP]]

## Design Gates Before Implementation

- Item master gate: define product/service/item taxonomy, units and stock behavior before document lines are finalized.
- Warehouse gate: define whether MVP supports one warehouse per tenant or multiple warehouses/locations.
- Movement gate: define which documents reserve, commit, move or value stock.
- Valuation gate: choose first valuation posture before accounting integration.
- Traceability gate: decide whether lots/serials are MVP or configurable by item category.
- SAF-T gate: confirm inventory export requirements before final stock schema.

## Core Workflows

- Configure warehouses, locations, items, units and stock behavior.
- Register stock initialization and adjustments.
- Reserve stock from sales orders where scoped.
- Receive goods from purchase/goods-receipt flows.
- Deliver or issue stock through sales/delivery flows.
- Transfer stock between warehouses/locations.
- Handle returns/devolutions with source references.
- Perform stock counts and reconcile differences.
- Track availability, reserved, committed, in-transit and on-hand quantities.
- Prepare inventory data for fiscal/audit exports where applicable.

## Required Master Data

- Items/products/services.
- Units of measure and conversions.
- Warehouses and optional locations/bins.
- Stock movement types.
- Item categories and stock behavior.
- Lot/serial configuration.
- Valuation method and costing configuration.
- Inventory document types.

## Candidate Domain Model

- `items`: tenant-owned products/services/materials, stock behavior, unit, category, tax/profile references.
- `warehouses`: tenant-owned warehouse/store/location roots.
- `warehouse_locations`: optional bins/locations inside warehouse.
- `stock_balances`: derived/current balance by tenant, item, warehouse/location, lot/serial where applicable.
- `stock_reservations`: reservation against sales/commercial source document.
- `stock_movements`: immutable movement ledger for receipts, issues, transfers, adjustments, returns and count differences.
- `stock_movement_lines`: item, quantity, unit, source, cost/valuation data and lot/serial references.
- `stock_counts`: count session header, warehouse, status, actor and date.
- `stock_count_lines`: expected vs counted quantities and variance.
- `lots`: lot/batch master where enabled.
- `serial_numbers`: serial tracking where enabled.
- `inventory_valuation_layers`: optional costing layers when valuation method requires it.

The provisional target schema is now consolidated in [[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]: `items` has no stored quantity (on-hand is derived); `stock_movements` is append-only and source-document-linked; `stock_reservations` reduces *available* without moving *on-hand*; `valuation_layers` make cost (weighted-avg MVP, FIFO-capable) auditable and SAF-T-ready; counts reconcile via movements, never silent balance edits. This is provisional until inventory/logistics references and SAF-T CV requirements are ingested.

## Candidate State Machine

### Stock Count State

- `draft`: count prepared but not started.
- `in_progress`: counting underway.
- `pending_review`: variances require approval.
- `approved`: variances accepted.
- `posted`: adjustment movements created.
- `cancelled`: count abandoned with reason.

### Reservation State

- `active`: quantity reserved.
- `partially_consumed`: some reserved quantity fulfilled.
- `consumed`: reservation fully converted to stock movement.
- `released`: reservation removed without movement.
- `expired`: reservation invalidated by policy/date.

## Integration Points

- [[Compras e Vendas ERP]] creates source events for reservations, goods receipts, deliveries, returns and document transformations.
- [[Faturacao Eletronica]] may need transport/document context but should not own stock movements.
- [[Contabilidade ERP]] may consume valuation or movement summaries.
- [[SAF-T CV]] may require structured inventory export data.
- [[Permissoes e Auditoria ERP]] controls stock adjustments, count approvals, valuation changes and warehouse configuration.

## Commercial Boundary

Inventory reacts to commercial/fiscal flows through explicit events:

- quote/proposal: no stock effect unless reservation is explicitly designed.
- sales order: may reserve stock.
- delivery note/guide: may create issue/transfer movement.
- invoice: may create movement only if the stock effect was not already handled by delivery.
- purchase order: no stock movement.
- goods receipt: creates receipt movement.
- return/devolution: creates reversal/return movement with source reference.

This preserves the separation defined in [[Compras e Vendas ERP]] and prevents accidental stock mutation from fiscal or commercial status changes.

## Accounting Boundary

Inventory can feed accounting through:

- receipt valuation;
- issue/cost-of-goods movement;
- inventory adjustment;
- count variance;
- transfer where valuation/accounting requires it;
- write-off or shrinkage.

Accounting should post from approved/confirmed inventory events, not from direct edits to stock balances.

## Audit, Security And Tenancy

- Stock movements must be tenant-scoped and traceable to origin documents.
- Manual adjustments require explicit reason, permission and audit trail.
- Count variances should require approval above configured thresholds.
- Lot/serial tracking should preserve full movement history.
- Direct edits to stock balances should be avoided; use movements/adjustments.
- Warehouse, valuation and item stock behavior configuration changes are high-risk and should be audited.

## Critical Domain Events

- `inventory.item_created`
- `inventory.stock_initialized`
- `inventory.stock_reserved`
- `inventory.reservation_released`
- `inventory.goods_received`
- `inventory.stock_issued`
- `inventory.stock_transferred`
- `inventory.return_received`
- `inventory.adjustment_posted`
- `inventory.count_started`
- `inventory.count_approved`
- `inventory.count_posted`
- `inventory.valuation_changed`

## Cabo Verde Compliance Notes

Inventory is not only operational. The source capture links inventory to SAF-T CV and fiscal reporting concerns. Specific export and valuation requirements require deep ingestion before implementation.

Fiscal/logistics caution:

- transport documents and delivery flows may need current e-Fatura/event/XSD/legal verification;
- SAF-T CV inventory scope must be confirmed before final schema;
- stock movements linked to fiscal documents must preserve source references for audit.

## MVP Acceptance Criteria

For the first sellable release, inventory is acceptable only if:

- stock is derived from movements, not manually edited aggregate fields;
- items and warehouses are tenant-scoped;
- stock-moving document types are explicit;
- goods receipts and deliveries create auditable movements;
- manual adjustments require reason and permission;
- stock counts can record expected, counted and variance quantities;
- stock reservations are either implemented explicitly or declared out of scope;
- stock effects from commercial documents are deterministic and traceable;
- accounting/SAF-T needs are not blocked by missing source references.

## Non-MVP Until Confirmed

- Advanced warehouse locations/bins if one-warehouse MVP is chosen.
- Full lot/serial tracking for every item category.
- Advanced valuation layers and landed cost allocation.
- Barcode/RFID operations.
- Automated replenishment.
- Transport document depth beyond confirmed fiscal/logistics scope.

## Open Questions

- Which valuation method should NOVA-ERP support first? (Provisionally weighted-average MVP, FIFO-capable; FIFO timing still open.)
- Are lots and serial numbers mandatory for MVP or configurable by product category? (Provisionally schema-ready but off unless an item requires it.)
- Which inventory data is required for SAF-T CV in the first release?
- Should sales orders reserve stock in MVP? (Provisionally **yes**, via `stock_reservations`, not movements.)
- Should MVP support multiple warehouses or start with one warehouse per tenant? (Provisionally: schema models many, UI may default to one.)
- Which document types create stock movement versus only fiscal/treasury effect?
- Are negative on-hand balances (oversell) allowed or hard-blocked at delivery?

## Next Ingestion Targets

- ~~Using — Gestão de Inventário (LPG003)~~ — **ingested** as [[2022 - Cegid Primavera Gestao de Inventario (Legacy Reference)]].
- `docs/docsfiscal/LPG018- Configuring - Logística (2022-v1.0-GB).pdf` (optional — deeper warehouse/location config).
- `docs/docsfiscal/Exercícios - Using - Gestão de Inventário (2022-v1.0-GB - LPG003).pdf` (exercises — only if concrete data still needed).
- SAF-T CV official/current inventory requirements.

