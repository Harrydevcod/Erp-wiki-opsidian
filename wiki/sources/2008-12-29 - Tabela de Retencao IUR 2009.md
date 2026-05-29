---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, iur, payroll, retencao-fonte, primary-law, historical, needs-review]
sources: []
related: ["[[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]", "[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Contradiction - IRPS Category A Withholding Brackets]]"]
confidence: high
---

# Tabela de Retenção IUR — 2009 (Portaria, B.O. 29-12-2008)

## What this is

The Cape Verde IUR withholding regulation in force **from 1 January 2009** (Boletim Oficial, I Série nº 48, 2º Suplemento, 29 December 2008; Minister Cristina Duarte). It is the **predecessor of [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]** and confirms the structure and the stability of the IUR marginal-rate scale.

Evidence: `docs/docsfiscal/Tabela de Retenção IUR - 2009.pdf` (Boletim Oficial, primary source).

> **Historical / currency caution:** this is a **2009 IUR** table, superseded by Portaria 5/2013 (which re-indexed the brackets) and by the later **IRPS** regime (Lei 78/VIII/2014). Use it as historical evidence of structure and rate-scale stability, not as current law.

## Anexo II — practical income-tax table (art. 7º), 2009

| Rendimento colectável (annual) | Taxa | Parcela a abater |
| :-- | :-- | :-- |
| up to 385.000$ | 11.67% | 0$ |
| 385.000$ – 810.000$ | 15.56% | 14.977$ |
| 810.000$ – 1.620.000$ | 21.39% | 62.289$ |
| 1.620.000$ – 2.430.000$ | 27.22% | 156.654$ |
| over 2.430.000$ | 35.00% | 345.789$ |

## Anexo I — monthly withholding table (art. 5º), 2009 (selected)

- 0% up to **22.288$/month**; withholding starts at 22.289$ (0.5%).
- Rises in 0.5% steps to **26%** above **384.314$/month**.

## Other categories (art. 8º)

- Own-account service provision (not dependent, not liberal-profession independent): **10%** withholding, for continuous work or occasional amounts ≥ 5.000$; falls only on the **labour (mão-de-obra)** portion. (This is the independent-worker withholding rule.)
- No withholding below **100$** (art. 9º).

## Why it matters (rate-scale stability)

Comparing 2009 vs the 2013 Portaria 5/2013:

- **Marginal rates are identical** across both years: 11.67% / 15.56% / 21.39% / 27.22% / 35%.
- **Brackets and parcelas a abater were re-indexed** (2009: 385.000/810.000/1.620.000/2.430.000$, PA 0/14.977/62.289/156.654/345.789; 2013: 408.843/860.163/1.720.327/2.580.490$, PA 0/15.904/66.051/166.347/367.109).
- The monthly 0% floor moved up (22.288$ in 2009 → 30.701$ in 2013).

This strongly validates the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] decision to model withholding as **effective-dated, rule-versioned config**: the rate scale is stable but the brackets/parcelas/monthly-floor are re-indexed by each year's OE. NOVA-ERP must hold these as versioned parameter sets, not constants.

## Verification needs

- This is historical (2009/2013 IUR). Confirm the current **IRPS-era** withholding parameters before production (see [[Contradiction - IRPS Category A Withholding Brackets]]).
