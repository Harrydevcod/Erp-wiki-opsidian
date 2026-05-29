---
type: contradiction
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [contradiction, fiscalidade, irps, payroll, needs-review, open-question]
sources: ["[[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]", "[[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]"]
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]"]
confidence: medium
---

# Contradiction - IRPS Category A Withholding Brackets

## Disputed claim

What is the current progressive bracket scale and rates used to withhold IRPS at source on Cabo Verde dependent-work income (Category A)?

## Position A — narrow progressive band (16.5%–27.5%)

The IRPS progressive rates range **16.5% to 27.5%**, per the Código do IRPS (Lei nº 78/VIII/2014).

Source: [S&D Consultoria — Regime Fiscal de Cabo Verde](https://consultoria.cv/en/regime-fiscal-de-cabo-verde-estrategias-essenciais-para-a-diaspora-e-investidores-estrangeiros/) citing Lei 78/VIII/2014, via [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]].

## Position B — wider illustrative bracket table (0%–27%)

An illustrative annual-income bracket table circulates: 0% up to 300,000$; 10% 300,001–600,000; 15% 600,001–1,200,000; 20% 1,200,001–2,400,000; 25% 2,400,001–4,800,000; 27% above 4,800,000.

Source: [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes) — explicitly labeled "an example of potential brackets, subject to 2026 confirmation."

## Why they conflict

- The two scales disagree on both the **number of bands** and the **rate values** (16.5% floor vs 0%/10% floor; 27.5% vs 27% ceiling).
- Position B's source self-flags as unconfirmed; Position A is a consultancy summary, not the statute text.
- Neither is the **official DNRE withholding table/formula**, which is the operative authority for monthly retention.

## Position C — official IUR-2013 scale (primary source)

The official [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]] (Boletim Oficial, primary law) gives the exact withholding scale on taxable income for the **IUR regime**: marginal rates **11.67% / 15.56% / 21.39% / 27.22% / 35%** across five brackets (up to 408.843$ / …/ over 2.580.490$), each with a `parcela a abater` (0 / 15.904$ / 66.051$ / 166.347$ / 367.109$), plus a separate `α` family-charges coefficient table and a 35% monthly cap. IUR-2013 monthly withholding starts above 30.701$.

This **resolves the scale for the IUR era** and shows Positions A and B were both inaccurate. Caveat: **IUR was replaced by IRPS** (Lei nº 78/VIII/2014); Portaria 5/2013 may have been superseded by an IRPS-era withholding portaria.

## Current best interpretation

Use the **IUR-2013 formula and scale from [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]** as the source-linked baseline for the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] withholding engine, encoded as rule-versioned config. Do **not** treat the 11.67–35% IUR scale as confirmed current IRPS law: obtain the IRPS-era withholding portaria to confirm or replace the rates, the `α`/PA tables, `EF`/`ME`, and the monthly threshold (IUR 30.701$ vs the IRPS-era 35.000$ reported by secondary sources). Discard the earlier Positions A (16.5–27.5%) and B (0–27%) as inaccurate.

## Confidence

Medium. The scale is now precise for IUR-2013 (primary source); IRPS-era currency is the remaining unknown.

## What would resolve it

- The current **IRPS-era withholding portaria** (post-Lei 78/VIII/2014) confirming whether the Portaria 5/2013 IUR scale was carried forward or replaced, with the current `α`/rate/PA tables and the monthly threshold.
- The current **Mínimo de Existência (ME)** value and any OE-year updates to `EF` (640.000$) and the brackets.

## Resolution attempt log

- 2026-05-29: fetched the primary Lei 78/VIII/2014 PDF, but it is compressed/non-machine-readable in this environment — the escalão table could not be extracted programmatically. Needs an OCR/manual pass on the official text or the DNRE withholding table.
- 2026-05-29 (2nd attempt): confirmed the withholding uses a formula `Retenção = (base × taxa) − parcela a abater` with a practical table up to ~68,235$ and formulas above; threshold annual 420,000$ / monthly 35,000$ reconfirmed. Beware: vendus.cv "Tabelas de retenção" is actually **Portugal IRS** (euros, Continente/Regiões), not Cabo Verde — do not use it for CV brackets. The CV `taxa` / `parcela a abater` values per band still require the official DNRE table.
