---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, cegid-primavera, inventario, stock, valorizacao, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Inventario ERP]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[SAF-T CV]]"]
confidence: medium
---

# Cegid Primavera — Gestão de Inventário (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — Gestão de Inventário" training deck (LPG003, 2022-v1.0-GB, 64 pp.), `docs/docsfiscal/Using - Gestão de Inventário (2022-v1.0-GB - LPG003).pdf`. **Legacy ERP workflow reference**, not legal authority and not target architecture. Portugal-oriented (its "Comunicação de Inventário à AT" is PT law). Value: the stock-movement / valuation / lot-serial / counting workflow, which strongly corroborates [[2026-05-28 - Schema Decision - Inventory Movements and Valuation]].

## Legacy workflow (as documented)

- **Stock movements** are either **with external entities** (Compras → *entrada* VFA/VGR; Vendas → *saída* FA/GR/NC) or **internal** (*Documentos Internos*: Entrada SI / Saída SS with global-stock impact; *Transferência*: out of origin warehouse + in to destination). Three movement natures: **Entrada, Saída, Transferência**.
- **Dados Mestre — Artigos:** auxiliary tables (Taxas IVA, Moedas, Famílias/Subfamílias, Marcas/Modelos, **Tipo de Artigo**); **reorder fields** Stock Mínimo / Máximo / de Reposição / Quantidade Económica; barcodes.
- **Editors:** *Documentos Internos* (Entrada/Saída) and *Transferência* (origin lines + destination lines).
- **Operações de Expedição e Receção** (warehouse orchestration):
  - *Expedição* (Encomendas de Cliente, Transferências, Devoluções a Fornecedor): **Monitor** (pending list) → **Processamento** (define qty, split lines per lot/unit, add articles) → **Resumo** (finalize → generates the stock-movement document).
  - *Receção* (Encomendas de Fornecedor, Transferências, Devoluções de Clientes): Monitor → Processamento (qty received + **rejected**) → Resumo.
- **Transferências de armazém com trânsito:** **PTS** (Pedido de Transferência) → **TST** (Transferência stock em trânsito — stock goes to an *indisponível/trânsito* state) → **RST** (Receção). Goods-in-circulation document + in-transit state machine.
- **Valorização — Preço de Custo Médio (PCM, moving weighted-average):** `PCM = (Valor em Stock + Valor entrado) / (Qt. em Stock + Qt. entrada)`; recomputed on each entry; outbound costed at current PCM. (Documented as the valuation method.)
- **Atributos dos Artigos:**
  - **Números de Série** — per-article toggle; auto/manual generation; entrada/saída; full **rastreabilidade** (where a serial is + its movement path).
  - **Lotes** — entrada/saída/transferência/**reativação**; suggestion methods **FIFO/LIFO by Data de Validade or Data de Fabrico**; consulta lotes por artigo; rastreabilidade.
  - **Dimensões** — parent/child articles (e.g. size × colour); parent edits propagate to children.
  - **Gestão Singular** (max 1 unit), **Artigo Substituto** (suggested when out of stock), **Artigo Associado** (auto-adds a linked line).
  - **Conjunto de artigos** (kit/bundle): no stock control on the set — controlled on components; price individualized.
  - **Artigos Compostos** (BOM): parent = sum of children; **Composição** (build: +parent, −components) / **Decomposição** (inverse); `QtComponente = QtComposto × QtComponentePadrão`.
- **Processo de Inventariação:**
  - *Inventário Físico* — physical count → **positive/negative adjustments** to align system to reality.
  - *Inventário Permanente* — perpetual inventory (cost of purchases/sales recorded for continuous valuation); mandatory for some companies; ≥ 1 physical count per exercício.
  - Phases: **Preparação** (create doc identifying articles; print/export to data-collection terminals) → **Contagem Física** (enter real counts per warehouse; import from terminals) → **Fecho**.
  - Preparation options: **Bloquear Stock** (block articles from moving until close), **Inventário às cegas** (blind — no existing-qty column), **Inventário fixo** (no new count lines after prep).
  - **Fechos de Inventário** — set a date after which no quantity (or quantity+costing) movements are allowed (inventory period lock).
- **Obrigações Fiscais [PT] — REJECT as authority:** Comunicação de Inventário à AT (XML). CV uses **SAF-T CV Inventário**.
- **Mapas:** Extrato de Artigos (Custo) — Entrada / Saída / **Ajuste de Custo (+/−)** / **Encargos** / **Descontos** + Variações de Custo; Extrato de Artigos (Movimentos) — Entrada/Saída/**Previsional/Reserva** with detail tabs (state movements, Reservas, Nºs de Série); **Consulta de Inventário** (stock at any date/time by Artigo/Armazém/**Localização**/Lote/**Estado**); Explorador, Consumos (BOM usage), Controlo de Stocks, Lotes por Artigos, Rastreabilidades.

## Translation to NOVA-ERP

**Adopt / strongly validates the ADR:**
- **Append-only movement ledger.** Cegid never stores a quantity on the article — *Consulta de Inventário* derives stock at any date/time. Direct corroboration of the ADR's "no `quantity_on_hand` column; on-hand is a projection."
- **PCM = weighted-average** is the documented valuation method → confirms the ADR's `weighted_avg` MVP default and the running-cost recompute; the *Extrato de Custo* with **Ajuste de Custo / Encargos / Descontos** confirms cost adjustments are first-class movement types feeding `valuation_layers`.
- **Reservation vs on-hand split.** *Previsional / Reserva* movement views corroborate `stock_available = on_hand − reservations`.
- **Count reconciliation.** Inventário Físico → positive/negative adjustments matches `count_reconcile` movements; blind-count and block-stock are concrete count controls.
- **Lots & serials** with FIFO/LIFO suggestion and traceability corroborate `lots`/`serials` + `items.tracking`.

**New inputs to fold into the ADR:**
- **In-transit stock state machine (PTS→TST→RST).** Transfers are not instantaneous in↔out; stock sits in an *in-transit/unavailable* state. Add `transfer_in_transit` to the movement/transfer model and an explicit **stock state** so `stock_available` excludes in-transit and reserved quantities. This sharpens the ADR's transfer handling and its open question on transfer costing.
- **Stock state as a first-class dimension.** Consulta by **Estado** and "movimentações de estados" imply quantities move between states (available / reserved / in-transit / blocked), not only between warehouses. Consider a `state` on movements/projections beyond on-hand vs available.
- **Warehouse location (`Localização`)** sub-dimension below warehouse — add an optional `location_id`.
- **Composed articles / BOM (composição-decomposição)** and **kits (conjunto)** — a bill-of-materials concept producing paired movements (+parent / −components by `QtComposto × QtComponentePadrão`). Likely **post-MVP**, but the movement ledger already supports it as paired movements.
- **Reorder fields** (min/max/reposição/qty económica) on `items` — planning support.
- **Inventory period lock (Fechos de Inventário)** — a date-based lock analogous to accounting period locks; add to the count/valuation lifecycle.
- **Rejected quantity** on reception — receipts can split accepted vs rejected.

**Adapt:**
- Substituto / Associado / Gestão Singular are commercial/UX behaviors that belong with [[Compras e Vendas ERP]] item config, not the stock ledger.

**Do not copy:**
- PT "Comunicação de Inventário à AT"; CV uses [[SAF-T CV]] Inventário.

## Open questions surfaced

- Should NOVA-ERP model an explicit **stock state** (available/reserved/in-transit/blocked) on the projection, or keep only on-hand vs available + a separate in-transit ledger?
- Is **BOM / composed articles / kits** in MVP scope or deferred? (Movement ledger supports it; UI/master-data is the cost.)
- Inter-warehouse **transfer costing** with an in-transit leg — source-layer cost held in transit until receipt? (ADR open question, now sharpened by PTS/TST/RST.)
- Is warehouse **Localização** in MVP or post-MVP?

## Verification needs

- The PT inventory-communication obligation is not CV authority; CV inventory reporting follows [[SAF-T CV]]. Valuation-method statutory requirements (is PCM mandatory? is FIFO allowed?) must be confirmed against current Cabo Verde accounting law.
