---
type: contradiction
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [contradiction, fiscalidade, irps, payroll, needs-review, open-question]
sources: ["[[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]"]
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]"]
confidence: low
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

## Current best interpretation

Treat both as **non-authoritative orientation**. For NOVA-ERP, IRPS Category A withholding must be implemented as a **rule-versioned, source-linked table/formula** ([[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]) populated from the **official DNRE withholding table or formula**, not from either summary above. The only figure used consistently across sources is the **withholding threshold: annual > 420,000$ / monthly > 35,000$**.

## Confidence

Low. The operative bracket scale is unresolved from current evidence.

## What would resolve it

- The current **official DNRE IRPS withholding table and/or retention formula** for the applicable year.
- The consolidated current text of **Lei nº 78/VIII/2014** with any budget-law (OE) amendments to the IRPS rate scale.

## Resolution attempt log

- 2026-05-29: fetched the primary Lei 78/VIII/2014 PDF, but it is compressed/non-machine-readable in this environment — the escalão table could not be extracted programmatically. Needs an OCR/manual pass on the official text or the DNRE withholding table.
- 2026-05-29 (2nd attempt): confirmed the withholding uses a formula `Retenção = (base × taxa) − parcela a abater` with a practical table up to ~68,235$ and formulas above; threshold annual 420,000$ / monthly 35,000$ reconfirmed. Beware: vendus.cv "Tabelas de retenção" is actually **Portugal IRS** (euros, Continente/Regiões), not Cabo Verde — do not use it for CV brackets. The CV `taxa` / `parcela a abater` values per band still require the official DNRE table.
