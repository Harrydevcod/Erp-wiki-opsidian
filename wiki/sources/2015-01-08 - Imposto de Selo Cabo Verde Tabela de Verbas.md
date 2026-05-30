---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, imposto-de-selo, treasury, primary-law]
sources: []
related: ["[[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]]", "[[Fiscalidade Cabo Verde]]", "[[Tesouraria ERP]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[Cabo Verde]]"]
confidence: medium
---

# 2015-01-08 - Imposto de Selo (Cabo Verde) — Tabela de Verbas

## Provenance

- **Primary law (partial capture).** The **Código do Imposto de Selo (IS)** and its **Anexo — Tabela de verbas**, as carried in **Boletim Oficial I Série nº 3, 8 de Janeiro de 2015** (the same compilation that publishes the [[2015-01-07 - Lei 82-2015 Codigo do IRPC]]).
- **Source:** parsed from `raw/assets/irpc/Lei_82_2015_Codigo_IRPC.pdf` in the sandbox. **This PDF starts mid-code** (from art. 27º — Garantias / art. 28º — Declaração anual) and ends with the Anexo Tabela.
- **Incidence now captured separately (2026-05-30):** the full incidence/general part (arts. 1–26) of **Lei 33/VII/2008** is documented in [[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]] (preserved at `raw/assets/selo/`). This page now holds the **rate Tabela**; that page holds the **incidence rules** (incl. the art. 1º §2 IVA non-cumulation gate).
- **Authority:** the rate **Tabela is operative** (subject to OE-year re-indexing checks).

## Why it matters

Stamp duty applies to credit operations, financial-service fees, insurance, guarantees and notarial/registration acts — all of which surface in NOVA-ERP **treasury** and **document** flows (loan drawdowns, bank fees, insurance postings, contracts). The rate table lets the tax engine compute IS where applicable, alongside IVA and ICE.

## Key claims — Anexo: Tabela de verbas

| Verba | Incidência | Taxa |
|---|---|---|
| 1 | Operações de crédito | **0,5%** |
| 2 | Juros, prémios, comissões ou contraprestações de serviços financeiros | **3,5%** |
| 3 | Garantias | **0,5%** |
| 4 | Seguros | **3,5%** |
| 5 | Letras, livranças, títulos de crédito, ordens de pagamento | **0,5%** |
| 6 | Operações societárias | **0,5%** |
| 7 | Actos notariais, do registo e processuais | **15%** |
| 8 | Actos administrativos | **1.000$00** (fixed) |
| 9 | Escritos de contratos | **1.000$00** (fixed) |

- **Art. 27º:** taxpayer guarantees follow the Código Geral Tributário / Código do Processo Tributário.
- **Art. 28º:** annual discriminative IS declaration obligation for commercial/industrial/service taxpayers and State/autarquia bodies that are IS taxpayers.

## Implementation impact

- Add an **IS verba taxonomy** to `tax_maps` (percentage verbas 1–6, the 15% verba 7, and the two **fixed 1.000$00** verbas 8–9). Stamp duty is largely a **treasury/financial-document** tax, not an invoice-line tax like IVA — model it as a posting rule on the relevant treasury/contract events.
- Fixed-escudo verbas (8, 9) need a non-percentage rate mode (a flat amount), distinct from IVA/IS percentage rates.

## Open questions

- ~~Ingest the full Código do Imposto de Selo (incidence arts. 1–26)~~ **Done 2026-05-30** → [[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]].
- Whether later **Orçamento de Estado** years changed any verba rate.
- Exact base of computation per verba (e.g., IS on credit = on principal vs. on interest; verba 2 vs verba 1 interaction with bank financing).
