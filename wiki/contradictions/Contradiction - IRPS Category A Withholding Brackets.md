---
type: contradiction
status: superseded
created: 2026-05-29
updated: 2026-05-30
tags: [contradiction, fiscalidade, irps, payroll, resolved]
sources: ["[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]", "[[2014-12-31 - Lei 78-2014 Codigo do IRPS]]", "[[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]", "[[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]]", "[[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]"]
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]"]
confidence: high
---

> **RESOLVED 2026-05-30 by primary law.** The operative monthly IRPS Category A withholding is the formula in [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] (Art. 5.º): `RI = 0,15·Rm − 5.500` (Rm ≤ 80.000$); `0,21·Rm − 10.300` (80.000–150.000$); `0,25·Rm − 16.300` (> 150.000$); rounded down to ten escudos, 100$ minimum. This **supersedes** the IUR-2013 scale. The annual *englobamento* assessment scale (isenção 220.000$ / 16,5 / 23,1 / 27,5%) is a separate final-assessment table. See the source page; the section below is kept as the resolution trail.

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

This **resolves the scale for the IUR era** and shows Positions A and B were both inaccurate. The earlier [[2008-12-29 - Tabela de Retencao IUR 2009]] corroborates it: identical marginal rates (11.67–35%) with only the brackets/parcelas re-indexed between 2009 and 2013, confirming the rate scale is stable while bands are re-indexed by each year's OE. Caveat: **IUR was replaced by IRPS** (Lei nº 78/VIII/2014); Portaria 5/2013 may have been superseded by an IRPS-era withholding portaria.

## Position D — IRPS reform scale corroborated with explicit brackets (2nd source)

A second, independent source — [[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]] — restates the IRPS progressive scale **with explicit bracket boundaries**, matching Position A's 16.5–27.5% band:

- Isenção (0%) **até 220.000$00/ano**;
- **16,5%** até 960.000$00/ano;
- **23,1%** > 960.000$00 e até 1.800.000$00/ano;
- **27,5%** > 1.800.000$00/ano.

Same source confirms **Category A** monthly retention is **progressivo e liberatório, from 420.000$/yr (35.000$/mo)**, and gives the other categories' flat retention (B 15%, C 10%, D 20%/10%, E 1%/20%).

Two independent sources (S&D Consultoria + this 2017 síntese) now agree on the 16.5–27.5% IRPS structure with bracket detail. This **shifts the direction of resolution**: the IUR scale was **replaced**, not carried forward.

## Current best interpretation

**The IUR-2013 scale (11.67%–35%, 5 bands) is superseded by the IRPS regime (Lei nº 78/VIII/2014).** The IRPS progressive/assessment scale is **isenção ≤ 220.000$; 16,5% ≤ 960.000$; 23,1% ≤ 1.800.000$; 27,5% > 1.800.000$** (annual), corroborated by two independent sources. Category A monthly withholding is **progressive + liberatório from 420.000$/yr (35.000$/mo)**.

For the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] withholding engine: encode the **IRPS 3-band scale** as the rule-versioned default (not the IUR 5-band scale), keyed to an effective-period so the IUR-2013 config remains available for historical recomputation. The exact **monthly Category A retention band table** (taxa + parcela a abater per bracket, as used for `Retenção = base × taxa − parcela a abater`) is set by the **Regime de Retenções na Fonte** decree and is the one remaining numeric gap — until obtained, derive monthly bands from the annual scale ÷ 12 as a provisional approximation and flag payslip IRPS as provisional.

Positions A and D agree (correct direction); Position B (0–27%, Rivermate) and the IUR-2013 numeric scale (Position C) are both **discarded as current IRPS withholding rates** (C remains valid only for IUR-era / pre-2015 recomputation).

## Resolution (2026-05-30, primary law)

Obtained the official **[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]** (B.O. I Série nº 7, 23-01-2015) from the DNRE legislation library. Art. 5.º gives the **operative monthly Category A formula** on monthly gross income `Rm`: **`0,15·Rm − 5.500`** (Rm ≤ 80.000$), **`0,21·Rm − 10.300`** (80.000–150.000$), **`0,25·Rm − 16.300`** (> 150.000$) — i.e. marginal **15/21/25%** with parcela a abater **5.500/10.300/16.300**; rounded down to ten escudos; 100$ minimum; mínimo de existência safeguarded (no retention below ≈36.667$/month). Subsídios férias/Natal/prémio = autonomous retention (Art. 6.º). This is the operative payslip table and **supersedes the IUR-2013 scale**.

It also **corrects** the category rates: the primary decree sets **B = 20% (4% REMPE), C = 20%, D = 20%/10%, E = 1%/20%** — the 2017 síntese's "B 15% / C 10%" was inaccurate (now further confirmed by the parent statute [[2014-12-31 - Lei 78-2014 Codigo do IRPS]] arts. 47º/48º = 20%). The annual *englobamento* assessment scale is now **primary-confirmed** by CIRPS **art. 45º** (isenção do colectável até 220.000$; 16,5% ≤960.000$; 23,1% ≤1.800.000$; 27,5% >1.800.000$) — a **distinct** year-end assessment table, not the monthly retention formula.

## Confidence

High. The operative withholding mechanism is now anchored in primary law.

## Residual (minor, non-blocking)

- A **Retificação** to DL 6/2015 is listed in the DNRE library but the linked file returned an unrelated B.O. page — confirm it does not amend the 15/21/25% + 5.500/10.300/16.300 values before production.
- Whether later **Orçamento de Estado** years re-indexed the 80.000$/150.000$ thresholds (2015 baseline).
- The current **Mínimo de Existência (ME)** value embedded in the referential annual Portaria tables.

## Resolution attempt log

- 2026-05-29: fetched the primary Lei 78/VIII/2014 PDF, but it is compressed/non-machine-readable in this environment — the escalão table could not be extracted programmatically. Needs an OCR/manual pass on the official text or the DNRE withholding table.
- 2026-05-29 (2nd attempt): confirmed the withholding uses a formula `Retenção = (base × taxa) − parcela a abater` with a practical table up to ~68,235$ and formulas above; threshold annual 420,000$ / monthly 35,000$ reconfirmed. Beware: vendus.cv "Tabelas de retenção" is actually **Portugal IRS** (euros, Continente/Regiões), not Cabo Verde — do not use it for CV brackets. The CV `taxa` / `parcela a abater` values per band still require the official DNRE table.
- 2026-05-30 (3rd attempt, resolved direction): parsed [[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]] (pypdf, 19 pp.) — a **second independent source** giving the IRPS scale with explicit brackets (isenção 220.000$; 16,5% ≤960.000$; 23,1% ≤1.800.000$; 27,5% >1.800.000$) plus per-category retention. Confirmed **IUR scale was replaced by IRPS**.
- 2026-05-30 (4th attempt, **RESOLVED with primary law**): located the **Decreto-Lei nº 6/2015** PDF in the DNRE legislation library (folder 64542) and parsed it directly (preserved at `raw/assets/irps/`). Art. 5.º gives the exact monthly Category A formula (15/21/25% with parcela a abater 5.500/10.300/16.300, thresholds 80.000$/150.000$). Also corrected B/C rates to 20% (decree) vs the 2017 síntese's 15%/10%. Contradiction closed; remaining residuals are minor (retificação check, OE-year re-indexing, ME value). See [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]].
