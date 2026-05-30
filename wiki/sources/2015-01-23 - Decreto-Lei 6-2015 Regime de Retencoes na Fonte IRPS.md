---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, irps, payroll, retencao-fonte, primary-law]
sources: []
related: ["[[Processamento de Salarios ERP]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Contradiction - IRPS Category A Withholding Brackets]]", "[[Fiscalidade Cabo Verde]]", "[[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]]"]
confidence: high
---

# 2015-01-23 - Decreto-Lei nº 6/2015 — Regime de Retenções na Fonte (IRPS)

## Provenance

- **Primary law.** Decreto-Lei **nº 6/2015, de 23 de Janeiro**, Conselho de Ministros. Published in **Boletim Oficial I Série nº 7, 23 de Janeiro de 2015** (pp. 372–373).
- **Legal basis:** art. 47.º nº2 + art. 70.º nº3 of [Lei nº 78/VIII/2014, de 31 de dezembro] (Código do IRPS).
- **In force:** 1 January 2015 (alongside the IRPS reform).
- **Source:** official DNRE legislation library — `mf.gov.cv/web/dnre/legislacao` (folder 64542). Downloaded and pypdf-parsed in the sandbox; preserved at `raw/assets/irps/Decreto-Lei_6_2015_Retencao_na_Fonte.pdf` (4 pp., text-extractable, INCV kiosk watermark).
- **Authority:** **operative** for IRPS withholding mechanics. This is the regulation the payroll engine implements. Sibling primary texts in the same DNRE folder (to ingest if needed): Lei 78/2014 (CIRPS), Lei 82/2015 (CIRPC).

## Why it matters

This closes the long-standing payroll gap: it gives the **exact monthly IRPS Category A withholding formula** — the operative table for payslip retention — and the flat retention rates for all other categories. It **supersedes the IUR-era [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]** for any period from 2015 onward and corrects the category rates reported by the secondary [[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]]. Resolves [[Contradiction - IRPS Category A Withholding Brackets]] with primary law.

## Key claims

### Category A — trabalho dependente e pensões (Secção I, Arts. 1–7)

- **Art. 2.º** — retention takes the taxpayer's **family condition** into account; it is **liberatório e progressivo**, converting to "por conta do imposto" only if the taxpayer opts for **englobamento**.
- **Art. 5.º — Aplicação da retenção:**
  - **5.1** Retention is computed by **applying the formulas** to the income paid/made available **each month**.
  - **5.2** A reference **tabela de retenção** may be used, **approved by Portaria** of the Finance Minister (the published annual tables are a referential built from these formulas).
  - **5.3** Amounts from tables are **rounded down to the lower ten escudos**.
  - **5.4** If the formula yields **< 100$00**, the **100$00** minimum is due.
  - **5.5** The formulas safeguard a **mínimo de existência isento**.
  - **5.6 — The official monthly withholding formula** (`RI` = retenção na fonte; `Rm` = rendimento bruto mensal):

    | Monthly gross income `Rm` | Formula `RI` |
    |---|---|
    | `Rm ≤ 80.000$` | `0,15 × Rm − 5.500` |
    | `80.000$ < Rm ≤ 150.000$` | `0,21 × Rm − 10.300` |
    | `Rm > 150.000$` | `0,25 × Rm − 16.300` |

    Marginal rates **15% / 21% / 25%**; effective `parcela a abater` **5.500 / 10.300 / 16.300**; bracket thresholds **80.000$ / 150.000$**. (Below ≈36.667$/month the result is ≤ 0 → no retention, consistent with the ~35.000$/month floor = 1/12 of 420.000$.) **Pensioners** (5.6 b) use the same formula applied to the pensioner's monthly gross.

- **Art. 6.º — Regras especiais:** subsídios de **férias, Natal e prémio de produtividade** → **retenção autónoma**, not added to the month's ordinary income (fractioned payments → proportional retention); **back-pay** (rendimentos em atraso) → autonomous retention dividing income by the months it relates to; payer-side errors corrected on the next retention within the annual period.
- **Art. 7.º — Deveres de informação:** employer must collect the employee's personal/family data at start of functions / before the first payment; employee must declare and update on any change.

### Other categories (Secção II, Arts. 8+)

- **Categoria B** (empresariais/profissionais, prestação de serviços): **20%** por conta; **4%** under the REMPE / non-organized-accounting regime.
- **Categoria C** (prediais): **20%** por conta.
- **Categoria D** (capital/incrementos): **20%**, except art. 14.º nº2 f)/j) income at **10%**, liberatório.
- **Categoria E** (art. 17.º): **1%** (nº1 a–d) or **20%** (nº2), liberatório.
- **Non-residents with permanent establishment:** **20%** or **10%**; **general/declaration rate 25%**.

## Corrections to prior wiki claims

- **Supersedes** the IUR-2013 monthly model (formula `[(V_m·p·N − PA) − α·(ME + EF)]/p`, 5-band 11.67–35%, `EF` 640.000$, 35% cap) for periods from 2015. The IUR config is retained only for pre-2015 historical recomputation.
- **Corrects** the secondary [[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]] which reported **Categoria B = 15%** and **Categoria C = 10%**; the primary decree sets **both at 20%** (B has a 4% REMPE variant). The 2017 síntese's annual *englobamento* assessment scale (isenção 220.000$ / 16,5% / 23,1% / 27,5%) is a **different table** (final annual assessment) from this monthly *retention* formula (15/21/25%) — do not conflate.

## Open questions

- A **Retificação** to this decree is listed in the DNRE library; the file at that link returned an unrelated B.O. page, so whether it amends any formula number is **unverified** — confirm before treating the 15/21/25% + 5.500/10.300/16.300 values as final for production.
- Whether later **Orçamento de Estado** years re-indexed the 80.000$/150.000$ thresholds or the parcelas (this text is the 2015 baseline).
- The current **Mínimo de Existência** value embedded in the "referential" annual Portaria tables.
