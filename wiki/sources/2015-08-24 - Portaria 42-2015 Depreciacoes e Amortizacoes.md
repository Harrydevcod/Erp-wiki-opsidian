---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, ativos, depreciacao, amortizacao, irpc, primary-law, needs-review]
sources: []
related: ["[[Gestao de Ativos ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]]", "[[Contabilidade ERP]]"]
confidence: high
---

# Portaria nº 42/2015 — Depreciações e Amortizações (primary text)

## What this is

The official Cape Verde regulation of asset depreciation/amortization for IRPC purposes (Boletim Oficial, I Série nº 50, 24 August 2015; Minister Cristina Duarte), issued under **art. 43º nº5 of the Código do IRPC**, in force for tax periods starting **on/after 1 January 2015**. The full **20 articles** are captured here from the primary text.

Evidence: `docs/docsfiscal/Portaria nº 42 - 2015 -Depreciações e Amortização.pdf` (Boletim Oficial, primary source).

> **Gap CLOSED (2026-05-30):** the per-asset-class **rate annex (tabela anexa, art. 2º nº1)** has been obtained from the official **B.O. I Série nº 52, 28-08-2015** (Rectificação republication) and extracted to **310 rated rows** — see [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] and `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv`. Tabela I (sector-specific) + Tabela II (generic by asset nature). Key generics: edifícios habitacionais 3%, industriais 5%, veículos ligeiros 14,28% (7 yr), pesados 20%, computadores/intangível 33,33%, mobiliário 12,5%.

## Core rules (by article)

- **Art. 2º** — Annual rates come from the annexed table. Used assets / opening-balance valuations / big repairs / works on third-party buildings: rate = 1 / expected-useful-years. Elements without a fixed rate: reasonable rate per Tax Administration based on expected useful life.
- **Art. 3º (valorimetria)** — Base = acquisition cost (price + accessory costs to entry into service) or production cost; **non-deductible IVA is included** in the base. **Real estate: only the construction value depreciates, not land.** Land with no express value → **25% of the global value** attributed to land.
- **Art. 4º (vida útil)** — Min useful life is derived from the max straight-line quota; max useful life from half that quota. No depreciation accepted beyond max useful life (save inactivity / special accepted cases).
- **Art. 5º — Quotas constantes (straight-line):** max annual quota = rate × depreciable value (new assets). Default method.
- **Art. 6º — Quotas decrescentes/degressivas (declining-balance):** optional, for tangible assets **not** acquired used and **not** buildings, light passenger/mixed vehicles (except public transport/rental), furniture or social equipment. Coefficients on the straight-line rate: **×1.5** (useful life <5y), **×2** (5–6y), **×2.5** (>6y).
- **Art. 7º — Intensive use (multi-shift):** +25% quota for two shifts, +50% for more than two.
- **Art. 8º** — Other methods need prior Tax Administration recognition.
- **Art. 9º** — Same method applied uniformly per asset from entry into service until full depreciation/disposal.
- **Art. 10º — Light passenger/mixed vehicles, recreational boats, tourism aircraft:** depreciation **not accepted on the cost portion above 4.000.000$** (except public-transport/rental assets).
- **Art. 11º** — Financial leasing: the lessee depreciates (general regime).
- **Art. 12º** — Spare parts/components: depreciable over the host asset's useful life when exclusively identifiable.
- **Art. 13º — Intangibles:** development-project expenses and limited-life industrial property (patents, trademarks, licences) are amortizable; **trespasses (goodwill) are NOT amortizable** except proven impairment; development expenses may be expensed in-period.
- **Art. 14º — Quotas mínimas:** = half the art. 2º rates; minimum quotas not booked in their period cannot be deducted later.
- **Art. 15º — Low-value assets ≤ 20.000$:** may be fully depreciated in a single tax period (unless part of a set that must be depreciated as a whole).
- **Art. 16º** — Revertible (concession) assets: depreciate over remaining concession years when shorter than min useful life.
- **Art. 17º** — Excess depreciation over the max is accepted in later periods up to the max quota.
- **Art. 18º (transitória)** — The declining-balance method applies only to tangible assets entering service from **1 January 2015**.
- **Art. 19º (revogatória)** — **Revokes Portaria nº 2/84, de 28 de Janeiro.**
- **Art. 20º** — In force from 1 January 2015, applying to tax periods starting after that date.

## Correction of an earlier secondary claim

A secondary commentary (captured in [[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]]) stated that pre-2015 assets "keep Portaria 2/84." The **primary text revokes Portaria 2/84 outright (art. 19º)** and applies to tax periods from 2015 (art. 20º); the only date-based carve-out is that the **declining-balance method** is limited to assets entering service from 1 Jan 2015 (art. 18º). The straight-line regime under this portaria applies generally from 2015.

## Implementation impact for NOVA-ERP

Confirms and sharpens the [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]] design:

- `asset_depreciation_policies.method`: `straight_line` (default), `declining_balance` (with eligibility filter + coefficient 1.5/2/2.5 by useful life), `low_value_expense` (≤20.000$).
- Real-estate handling: depreciate **construction value only**; model a **land split** (default 25% of global value when not stated).
- `cost_cap` = 4.000.000$ for light vehicles/boats/aircraft.
- Minimum-quota rule (half the rate) and the multi-shift uplifts (+25%/+50%) are policy parameters.
- Non-deductible IVA capitalized into the asset base.
- Intangibles: separate amortizable classes; goodwill not amortizable by default.
- Leasing: lessee depreciates.

## Verification needs

- ~~Obtain the annexed per-class rate table~~ **Done** — extracted to [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] (`raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv`, 310 rows) to seed `asset_depreciation_policies.rate`.
- Confirm no post-2015 OE amendments altered the 20.000$ / 4.000.000$ thresholds or the coefficients.
