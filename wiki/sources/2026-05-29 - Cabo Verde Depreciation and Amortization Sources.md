---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, ativos, depreciacao, amortizacao, irpc, cabo-verde, needs-review]
sources: []
related: ["[[Gestao de Ativos ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[Contabilidade ERP]]"]
confidence: medium
---

# Cabo Verde Depreciation and Amortization Sources

## What this is

A 2026-05-29 web-research capture of Cabo Verde's fiscal depreciation/amortization regime, to unblock the fixed-assets schema design ([[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]). It points at the **primary regulation (Portaria 42/2015)** and the **IRPC Code**, summarized via secondary commentary. The per-asset-class **rate table lives in the Portaria annex and was not extracted here** — it must be obtained from the official text before production depreciation runs.

## Legal framework

- The **Código do IRPC** (Lei nº 82/VIII/2015) governs corporate income tax; its **article 43º** mandated a depreciation/amortization regulation.
- **Portaria nº 42/2015, de 24 de Agosto** (republished September 2015 to correct an inexact August publication), in force from **1 January 2015**, is the **Regulamento das Depreciações e Amortizações dos Elementos do Activo**. It carries the per-class rate tables.

## Key rules

- **Default method: quotas constantes** (straight-line) — cost spread equally over the asset's fiscal useful life; the **quotas decrescentes** (declining-balance) method exists as an alternative for eligible assets.
- **Low-value assets (art. 15º)**: elements subject to wear whose **unit acquisition/production cost does not exceed 20,000$** may be **fully depreciated/amortized in a single tax period**.
- **Light vehicles (art. 10º)**: depreciation is **not accepted as a cost on the portion of acquisition cost above 4,000,000$00**.
- **Transition**: corrected against the primary text in [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] — art. 19º **revokes Portaria 2/84** outright and art. 20º applies the new portaria to tax periods from 1 Jan 2015; the only date carve-out is that the **declining-balance method** is limited to assets entering service from 1 Jan 2015 (art. 18º). The earlier "pre-2015 assets keep Portaria 2/84" framing below was secondary-commentary and is superseded by the primary source.
- Per-class rates/useful lives (buildings, equipment, vehicles, furniture, intangibles, etc.) are defined in the **Portaria 42/2015 annex** — **not captured**, obtain from the official text.
- IRPC nominal base rate: **25%** (context for the accounting/tax boundary).

Evidence: [Fisco Cabo Verde — Nova Portaria de Depreciações e Amortizações](https://fiscocaboverde.wordpress.com/2017/06/23/nova-portaria-de-amortizacao-e-reintegracao-de-activo-imobilizado/); [Portaria 42/2015 — Boletim Oficial (INCV)](https://boe.incv.cv/Bulletins/View?id=26358); [Sistema Fiscal Cabo Verde — cvTradeInvest](https://www.cvtradeinvest.cv/assets/files/Sistema-Fiscal-Cabo-Verde.cleaned.pdf).

## Implementation impact for NOVA-ERP

- Confirms the [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]] design of **versioned depreciation policies** keyed to legal sources: the regime is rule-table-driven, has a low-value expensing shortcut, a vehicle cost cap, and a pre/post-2015 split that depends on acquisition date.
- The fixed-assets `depreciation_policies` should carry: `method` (`straight_line` default / `declining_balance`), `useful_life`/`rate` (from the Portaria 42/2015 annex), a **low-value threshold of 20,000$** for single-period expensing, a **vehicle cost cap of 4,000,000$**, and an **acquisition-date rule** selecting Portaria 42/2015 vs 2/84.
- Tax depreciation (Portaria limits) and accounting depreciation may diverge; the asset schema must keep them separable.

## Currency and verification needs (high-stakes)

- **Obtain the Portaria 42/2015 annex rate table** (per asset class) from the official Boletim Oficial before configuring depreciation rates.
- Confirm whether any post-2015 budget law (e.g. OE amendments) altered thresholds/caps; the 20,000$ and 4,000,000$ figures and the 2/84 transition should be re-validated against the current consolidated text.
- 2026-05-29: the founder supplied the official Boletim Oficial PDF; the full **20 articles are now captured** in [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]. The only remaining gap is the **per-class rate annex** (the actual percentages by asset type), which is not in that PDF copy and still needs an OCR/manual pass on the annexed table.
