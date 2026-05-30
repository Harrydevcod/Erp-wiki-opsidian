---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, irps, payroll, primary-law]
sources: []
related: ["[[Fiscalidade Cabo Verde]]", "[[Processamento de Salarios ERP]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]", "[[Contradiction - IRPS Category A Withholding Brackets]]", "[[Cabo Verde]]"]
confidence: high
---

# 2014-12-31 - Lei nº 78/VIII/2014 — Código do IRPS

## Provenance

- **Primary law.** Lei nº **78/VIII/2014, de 31 de dezembro** — Código do Imposto sobre o Rendimento das Pessoas Singulares (CIRPS). Published in **Boletim Oficial I Série nº 81, 31 de Dezembro de 2014**. In force from **1 January 2015** (the fiscal reform that replaced the IUR).
- **Source:** official DNRE legislation library (`mf.gov.cv`, folder 64542). Downloaded and pypdf-parsed in the sandbox; preserved at `raw/assets/irps/Lei_78_2014_Codigo_IRPS.pdf` (16 pp.).
- **Authority:** **primary/operative** for personal income tax. Parent statute of the withholding regime [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] (DL 6/2015 is issued under CIRPS arts. 47º/70º).

## Why it matters

Upgrades the IRPS rate scale and category structure from **secondary** ([[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]]) to **primary**, and confirms the per-category retention rates against the decree. Anchors the annual *englobamento* assessment used for year-end reconciliation in payroll and the IRPS exemption floor.

## Key claims

### Income categories (Arts. 2–3)

- **A** — rendimentos do **trabalho dependente e pensões**.
- **B** — rendimentos **empresariais e profissionais**.
- **C** — rendimentos **prediais**.
- **D** — rendimentos de **capitais**.
- **E** — **ganhos patrimoniais**.

Income in cash or kind, from licit or illicit acts, is taxable.

### Art. 45º — Taxa de imposto e mínimo de existência (annual englobamento scale)

The rate on income subject to englobamento (and on manifestações de fortuna, art. 42º):

| Annual taxable income | Rate |
|---|---|
| ≤ 960.000$00 | **16,5%** |
| > 960.000$00 e ≤ 1.800.000$00 | **23,1%** |
| > 1.800.000$00 | **27,5%** |

- **Mínimo de existência / isenção:** the **rendimento colectável is exempt up to 220.000$00** (art. 45º nº2).
- nº3: the scale does not override personal/family adjustment via the deductions (art. 52º) and the progressive **retention** scale.

### Retention by category (Arts. 46º–49º) — confirms the decree

- **Cat. A** (art. 46º): progressive + liberatório per art. 70º (i.e. the [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] formula); becomes "por conta" if the taxpayer opts for englobamento.
- **Cat. B** (art. 47º): **20%** por conta; the **micro/pequenas empresas (REMPE) simplified regime** retention is set in its own diploma (the 4% rate).
- **Cat. C** (art. 48º): **20%**.
- (D/E per the decree: 20%/10% and 1%/20%.)

> This **confirms B = 20% and C = 20% by primary law**, settling the discrepancy where the 2017 síntese had reported 15%/10%.

### Art. 52º — Deduções à colecta (structure)

- Deductions in arts. 53º–56º are deductible from that year's colecta, up to its amount, with **no refund** of excess.
- **Withholding** made "por conta" is deductible from the year's colecta, **with refund** of excess.
- **Pagamentos fraccionados** (art. 73º) are deductible that year or over the next four, generating a **crédito fiscal**.

## Implementation impact

- Encode the **annual englobamento scale (16,5/23,1/27,5%, isenção 220.000$)** as the year-end IRPS assessment table — distinct from the **monthly retention formula** (DL 6/2015, 15/21/25%). Payroll uses the monthly formula; an annual reconciliation (for englobamento opt-in) uses this scale.
- Category taxonomy A–E feeds the withholding-agent logic for non-payroll flows (suppliers, rents, capital).

## Open questions

- The **Mínimo de Existência** as a distinct indexed value vs. the 220.000$ isenção colectável — confirm whether later OE laws set a separate ME figure.
- Whether later **Orçamento de Estado** years re-indexed the 960.000$/1.800.000$ brackets or the 220.000$ floor (this is the 2014 baseline).
- Deduction amounts in arts. 53º–56º (personal/dependent/health/education) — extract when the payroll annual-reconciliation feature is built.
