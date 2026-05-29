---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, vendas, compras, documentos, faturacao]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[Faturacao Eletronica]]", "[[Fiscalidade Cabo Verde]]", "[[Tesouraria ERP]]", "[[Inventario ERP]]", "[[Permissoes e Auditoria ERP]]", "docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]"]
related: ["[[NOVA-ERP]]", "[[Faturacao Eletronica]]", "[[Inventario ERP]]", "[[Tesouraria ERP]]", "[[Contabilidade ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]"]
confidence: medium
---

# Compras e Vendas ERP

## Purpose

Compras e Vendas ERP is the commercial document circuit for NOVA-ERP: customers, suppliers, quotations/orders where relevant, sales documents, purchase documents, goods reception, delivery, corrective documents and operational-to-fiscal transitions.

## Role In NOVA-ERP

This module is a core operating spine. Sales and purchases drive stock, treasury, accounting and fiscal obligations. The design must therefore treat commercial documents as structured business events, not just printable forms.

The key boundary: a commercial order, quote or request is not automatically a fiscal document. Fiscal issuance belongs to [[Faturacao Eletronica]], treasury settlement belongs to [[Tesouraria ERP]], stock movement belongs to [[Inventario ERP]], and accounting postings belong to [[Contabilidade ERP]]. Compras/Vendas orchestrates the business circuit and creates controlled source events for those modules.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[Faturacao Eletronica]], [[Tesouraria ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- ERP workflow reference: `docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf`
- Exercises: `docs/docsfiscal/Exercícios-Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015 .pdf`
- Fiscal/invoice rules: [[2026-05-28 - Manual de Faturas em Cabo Verde]], [[Fiscalidade Cabo Verde]]
- Integration modules: [[Faturacao Eletronica]], [[Tesouraria ERP]], [[Inventario ERP]], [[Contabilidade ERP]], [[Permissoes e Auditoria ERP]]

## Design Gates Before Implementation

- Document taxonomy gate: define which documents are commercial, stock-moving, treasury-generating, fiscal or purely internal.
- Fiscal boundary gate: define when a sales flow becomes an issued fiscal document and whether PE authorization is required before downstream effects.
- Stock boundary gate: define which documents reserve, commit or move stock.
- Treasury boundary gate: define which documents create receivables/payables and when invoice-receipts create settlement movements.
- Correction gate: define cancellation, return, credit/debit and rectification flows without mutating finalized fiscal evidence.
- Security/audit gate: define permissions for draft creation, approval, transformation, fiscal issue, cancellation and price/discount overrides.

## Core Workflows

- Manage customers, suppliers and commercial terms.
- Create sales quotes, orders or draft documents where relevant.
- Create purchase orders or supplier document records where relevant.
- Transform documents through controlled flows, such as quote to order, order to invoice, purchase order to goods receipt.
- Create sales fiscal documents through [[Faturacao Eletronica]] when the flow reaches fiscal issuance.
- Create purchase evidence and supplier obligations.
- Create corrective documents for returns, credit, debit and rectification where legally/operationally allowed.
- Update inventory when stock-moving documents are finalized.
- Generate receivables/payables for [[Tesouraria ERP]].
- Preserve origin relationships across transformed documents.

## Required Master Data

- Customers and suppliers.
- Products/services/items.
- Units, prices, discounts and tax profiles.
- Warehouses and stock behavior.
- Commercial document types.
- Fiscal document types and series, owned by [[Faturacao Eletronica]].
- Payment terms and commercial conditions.
- Delivery addresses and transport data where applicable.

## Candidate Domain Model

The provisional target schema is now consolidated in [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]. Key points: customers/suppliers unify into `entities` (with a `kind` role flag); `commercial_documents`/`commercial_document_lines` hold operational intent; `fiscal_documents`/`fiscal_document_lines` hold the immutable legal record; `document_series` is scoped `commercial|fiscal` with independent numbering; `document_links` replaces scattered transformation FKs.

- `entities`: customers, suppliers and mixed parties with NIF/tax and commercial profile.
- `items`: products/services with unit, tax profile, stock behavior and pricing metadata.
- `commercial_document_types`: quote, order, proforma, purchase order, goods receipt, delivery note and other non-fiscal operational types.
- `commercial_documents`: tenant-owned business document header, party, dates, currency, state, totals and source/target references.
- `commercial_document_lines`: item/service lines, quantity, price, discounts, tax profile and stock behavior.
- `document_links`: explicit relationship graph between source and target documents (transforms_into, invoices, corrects, returns, references).
- `approval_records`: approval/rejection/reason for high-risk documents, discounts or overrides.
- `commercial_terms`: payment terms, delivery terms, credit limits and default pricing policies.
- `purchase_receipts`: supplier/goods receipt evidence where inventory is affected.
- `return_authorizations`: controlled return/devolution source before fiscal/stock effects.

Fiscal document payloads, DFE transmissions and official fiscal numbering remain under [[Faturacao Eletronica]] and [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]].

## Candidate State Machine

### Commercial Document State

- `draft`: editable, no external fiscal/stock/treasury effect.
- `pending_approval`: requires approval for discount, credit, stock, value or policy reason.
- `approved`: ready for transformation or finalization.
- `converted`: transformed into another document.
- `fulfilled`: operational obligation completed.
- `cancelled`: cancelled before irreversible fiscal/stock/treasury effects or through controlled path.

### Purchase/Reception State

- `ordered`: supplier order exists.
- `partially_received`: some quantities received.
- `received`: quantities received.
- `invoiced`: supplier invoice/evidence exists.
- `closed`: purchase flow complete.

## Integration Points

- [[Faturacao Eletronica]] owns fiscal issuance, numbering, immutable fiscal snapshots, e-Fatura status and corrective fiscal documents.
- [[Inventario ERP]] receives reservations, commitments, deliveries, receipts, returns and stock adjustments.
- [[Tesouraria ERP]] receives receivables/payables and later settlement allocations.
- [[Contabilidade ERP]] receives posting evidence from fiscal, treasury, purchase and inventory events.
- [[Fiscalidade Cabo Verde]] constrains tax treatment, document rules, corrections and special regimes.
- [[Permissoes e Auditoria ERP]] controls approval, transformation, issuing, cancellation and override permissions.

## Fiscal Boundary

Commercial documents should not become fiscal evidence by accident.

Rules to preserve:

- draft quotes/orders do not consume fiscal numbering;
- fiscal number assignment happens server-side in [[Faturacao Eletronica]];
- issued fiscal documents become immutable except through corrective flows;
- rectification documents reference original invoice and altered mentions;
- returns/devolutions must preserve relationship to original sale/purchase where required;
- invoice-receipts and immediate-settlement documents must coordinate fiscal issuance and treasury movement atomically or through a clearly audited saga.

Source: [[2026-05-28 - Manual de Faturas em Cabo Verde]], [[Faturacao Eletronica]], [[Tesouraria ERP]]

## Stock Boundary

Commercial documents can have different stock effects:

- quote/proposal: no stock movement; optional reservation only if explicitly designed.
- sales order: may reserve stock.
- delivery note/guide: may move or commit stock depending on document type.
- invoice: may or may not move stock depending on whether delivery already occurred.
- purchase order: no stock movement.
- goods receipt: increases stock.
- return/devolution: reverses or adjusts stock through controlled inventory events.

Final stock policy belongs with [[Inventario ERP]].

## Treasury Boundary

Sales and purchase documents should create receivables/payables through explicit rules:

- quote/proposal: no receivable/payable.
- order: usually no receivable/payable unless advance is required.
- issued invoice: creates receivable.
- invoice-receipt: creates receivable and settlement movement or equivalent controlled treasury transaction.
- supplier invoice: creates payable.
- credit/debit notes: adjust receivables/payables through explicit allocation/correction logic.

Payment status should be derived from [[Tesouraria ERP]] allocations, not manually edited on the commercial document.

## Audit, Security And Tenancy

- Commercial documents must be tenant-scoped.
- Transformations must preserve source/target relationship.
- Finalized fiscal documents cannot be edited through commercial screens.
- Cancellation, transformation and correction must preserve audit history.
- Permissions should distinguish draft creation, approval, fiscal issuance, cancellation, price override, discount override and document-type configuration.
- Destructive changes to customers, NIFs, products, tax settings or prices should be blocked or controlled when issued documents depend on them.

## Critical Domain Events

- `commercial_document.draft_created`
- `commercial_document.approval_requested`
- `commercial_document.approved`
- `commercial_document.converted`
- `commercial_document.cancelled`
- `sales_order.confirmed`
- `purchase_order.confirmed`
- `goods_receipt.confirmed`
- `sales_return.requested`
- `purchase_return.requested`
- `receivable.source_created`
- `payable.source_created`

Fiscal issue, e-Fatura, stock movement, treasury settlement and accounting posting events remain owned by their respective modules.

## Cabo Verde Compliance Notes

The Cabo Verde fiscal layer affects invoice requirements, numbering, IVA, corrective documents, transport documents and e-Fatura. [[2026-05-28 - Manual de Faturas em Cabo Verde]] strengthens three product constraints:

- numbered fiscal documents are not deleted;
- corrections happen through explicit rectification/corrective documents;
- tax regime/public-sector context can change required wording and downstream accounting/tax behavior.

The exact implementation must still be verified against current fiscal sources before production.

## MVP Acceptance Criteria

For the first sellable release, the module is acceptable only if:

- commercial drafts are separated from fiscal issued documents;
- fiscal issue is delegated to [[Faturacao Eletronica]] and consumes fiscal numbering only through controlled server-side flow;
- receivables/payables are generated through explicit rules, not direct status mutation;
- stock effects are explicit per document type;
- document transformations preserve source lineage;
- issued fiscal document data cannot be silently edited from the commercial module;
- corrections/returns preserve original-document references;
- tenant/RLS and action permissions apply to create, approve, issue, cancel and override flows.

## Non-MVP Until Confirmed

- Fully generalized document transformation engine for every legacy ERP document type.
- Advanced pricing/promotions engine.
- Complex public works/State invoicing behavior before current legal ingestion.
- Reverse-charge automation before current legal verification.
- Automated customer portal order flow unless intentionally scoped.
- Transport document depth beyond the first confirmed inventory/logistics scope.

## Open Questions

- Should customers and suppliers be unified into one entity model? (Provisionally resolved **yes** — unified `entities` with `kind` in [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]].)
- Which sales document types are required in MVP? (Still open — needs backlog MVP cut.)
- Which purchase flow depth is necessary before accounting integration?
- Should document transformation be generalized from day one or limited to critical flows? (Provisionally via the `document_links` graph; trigger vs app integrity still open.)
- Should transport documents ship with the first inventory/logistics release or remain after MVP?
- Should invoice-receipt create fiscal issue and treasury settlement in one transaction or via a controlled saga?
- Which commercial documents should reserve stock in the first release?

## Next Ingestion Targets

- `docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf`
- `docs/docsfiscal/Exercícios-Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015 .pdf`
- Current legal sources for reverse charge, State/public works invoicing and transport documents.

