---
type: map
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [map, fiscalidade, irpc, depreciacao, ativos, reference, primary-law]
sources: ["[[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]"]
related: ["[[Gestao de Ativos ERP]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[Fiscalidade Cabo Verde]]"]
confidence: high
---

# Portaria 42/2015 — Tabelas de Taxas de Depreciação

The per-class depreciation/amortization **rate annex** of [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] — the long-standing missing piece for the [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]] default rates. Extracted from the official **Boletim Oficial I Série nº 52, 28 de Agosto de 2015** (the Rectificação republication of the portaria first published in B.O. nº 50, 24-08-2015).

- **Preserved source:** `raw/assets/irpc/Portaria_42_2015_Tabelas_Taxas_Depreciacao.pdf` (BO nº 52, 18 pp.) and the 20-article regime `raw/assets/irpc/Portaria_42_2015_Depreciacoes_Amortizacoes.pdf`.
- **Extracted data:** `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv` — **310 rated rows** parsed (`setor_or_tabela, grupo, subcategoria, designacao, taxa`). This seeds the tenant default `depreciation_rate` / `useful_life` per asset class.
- **Caveat:** rows were de-wrapped heuristically from a two-column PDF; **sector/grupo labels and rates are reliable**, but a few long designations are line-split and the Tabela I/Tabela II boundary is implicit. Verify exact wording against the PDF before legal display.

## Structure

The annex has two tables (straight-line **quota constante** maxima; declining-balance multipliers ×1.5/2/2.5 apply per the regime, see the source page):

- **Tabela I – taxas específicas:** rates by economic sector → Grupo. Sectors captured: *Agricultura/silvicultura/pecuária e Pesca* (G1–2), *Electricidade, Água e Gás* (G1–3), *Serviços* (G1,2,4), *Hotéis/Restaurantes/Similares* (G3), *Transportes e Comunicações* (G1–2), *Construção Civil e Obras Públicas*, *Indústrias transformadoras* (G1–9, 103 rows — the largest).
- **Tabela II – taxas genéricas:** rates by asset **nature** (the fallback when no specific sector rate applies) — *Activo Fixo Tangível* G1 Imóveis, G2 Instalações, G3 Máquinas/aparelhos/ferramentas, G4 Material de transporte, G5 Elementos diversos; plus *Activo Intangível*.

## Key generic defaults (Tabela II) — most-used for NOVA-ERP

| Asset class | Taxa (quota constante) | ≈ Vida útil |
|---|---|---|
| Edifícios habitacionais/comerciais/administrativos | **3%** | ~33 yr |
| Edifícios industriais | **5%** | 20 yr |
| Edificações ligeiras (fibrocimento, madeira, zinco) | **10%** | 10 yr |
| Instalações (ar comprimido, refrigeração, telefónicas, ascensores) | **10%** | 10 yr |
| Caldeiras / postos de transformação / reservatórios combustível | **6,66%** | ~15 yr |
| Veículos ligeiros e mistos | **14,28%** | 7 yr |
| Veículos pesados (passageiros / mercadorias) | **20%** | 5 yr |
| Motociclos / bicicletas | **25%** | 4 yr |
| Aeronaves | **20%** | 5 yr |
| Máquinas-ferramentas pesadas / motores | **12,5%** | 8 yr |
| Aparelhagem e máquinas electrónicas | **20%** | 5 yr |
| Computadores / aparelhos telemóveis / programas de computador | **33,33%** | 3 yr |
| Aparelhos de ar condicionado | **12,5%** | 8 yr |
| Televisores | **25%** | 4 yr |
| Mobiliário | **12,5%** | 8 yr |
| Moldes, matrizes, formas e cunhos | **25%** | 4 yr |
| Despesas de instalação/expansão e de I&D (intangível) | **33,33%** | 3 yr |

Distinct rates across the annex: 2,5 / 3 / 4 / 5 / 6,25 / 6,66 / 7,14 / 8,33 / 10 / 12,5 / 14,28 / 16,66 / 20 / 25 / 33,33 / 50% (each maps to a standard useful-life in years = 100 ÷ rate).

## Implementation note

Seed `asset_classes` (or the depreciation-policy defaults) from the CSV: a tenant picks the **Tabela I** sector rate when their activity matches, else the **Tabela II** generic rate. The regime articles (already in the source page) govern method (quota constante default; quotas decrescentes only for assets entering service from 2015-01-01, Art. 18), the 20.000$ low-value full-expensing (Art. 15), and the pre-2015 transition to old Portaria 2/84 rates (Art. 20).
