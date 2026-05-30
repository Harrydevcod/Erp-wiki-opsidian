---
type: source
status: active
created: 2026-05-29
updated: 2026-05-30
tags: [source, fiscalidade, payroll, inps, irps, codigo-laboral, salario-minimo, cabo-verde, needs-review]
sources: []
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Contradiction - IRPS Category A Withholding Brackets]]", "[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]", "[[2014-12-31 - Lei 78-2014 Codigo do IRPS]]"]
confidence: medium
---

# Cabo Verde Payroll and Personal Income Tax Sources

## What this is

A 2026-05-29 web-research capture of the statutory parameters governing Cabo Verde payroll: INPS social-security contributions, IRPS (personal income tax) withholding on dependent work, and the national minimum wage. This consolidates **secondary web sources** plus pointers to the **primary law**. It is reference evidence to unblock the payroll schema design ([[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]); it is **not** primary legal authority. Every production figure must be confirmed against the current official text (Lei nº 78/VIII/2014 do IRPS, the DNRE withholding tables, and INPS regulation) before being shipped in payroll calculations.

## INPS — Social Security Contributions

- General employees (trabalhadores por conta de outrem): total **24.5%** of gross salary = **16% employer** + **8.5% employee**.
- Self-employed (conta própria): **19.5%**.
- Domestic service (serviço doméstico): **23%** = 15% employer + 8% employee.
- Contributions are due by the **15th of the month following** the reference month; declared via Folha de Ordenados e Salários (FOS) / e-FOS.
- **Contribution base (correction):** what earlier sources called a "ceiling" is in practice a **minimum base floor** tied to the national minimum wage — the **base de incidência contributiva** tracks the minimum wage (e.g. raised from 13.000$ to 14.000$ in Jan 2023, and rising again with the 2025 minimum of 17.000$). Contributions are computed on the actual gross with that floor; **no clearly-documented upper maximum cap** was found. ⚠️ Confirm with INPS whether any upper ceiling exists; otherwise model the base as `max(gross, statutory_floor)` with no cap.

Evidence: [INPS — Contribuições](https://inps.cv/contribuicoes/); [INPS — Obrigações](https://inps.cv/obrigacoes/); [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes) (states 16% / 8.5% / 24.5% expected for 2026, with a monthly ceiling).

## IRPS — Personal Income Tax on Dependent Work (Category A)

- Legal authority: **Lei nº 78/VIII/2014** (Código do IRPS).
- Category A (trabalho dependente) is taxed by **retenção na fonte com caráter final** (final withholding), not the declarative method.
- The employer withholds monthly using the **official DNRE withholding tables or the withholding formula**; the source guidance recommends using the **formula, not the practical tables**, to avoid rounding errors.
- Withholding threshold: applies from annual income **> 420,000$** (i.e. monthly income **> 35,000$**, = 1/12 of 420,000$).
- Progressive rates: **RESOLVED by primary law (2026-05-30).** The operative monthly Category A withholding is the [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] formula — `RI = 0,15·Rm − 5.500` (Rm ≤ 80.000$), `0,21·Rm − 10.300` (80.000–150.000$), `0,25·Rm − 16.300` (> 150.000$), rounded down to ten escudos, 100$ minimum. The annual englobamento scale (16,5/23,1/27,5%, isenção 220.000$) is confirmed by [[2014-12-31 - Lei 78-2014 Codigo do IRPS]] art. 45º. The IUR-2013 scale (11.67–35%) is **superseded** (retained only for pre-2015 recompute). See [[Contradiction - IRPS Category A Withholding Brackets]] (resolved).
- Deductions/allowances: personal allowance, dependents (spouse/children), documented health/education/housing within limits, and the employee's 8.5% INPS share is typically deductible from the IRPS base.

Evidence: [Flyer IRPS — Ministério das Finanças](https://www.mf.gov.cv/documents/54571/273413/Flyer%20IRPS.pdf); [Código do IRPS — Lei 78/VIII/2014](https://www.ministeriopublico.cv/index.php/ministerio-publico/legislacao/category/13-ministerio-publico-na-jurisdicao-fiscal-e-aduaneira?download=229:codigo-de-irps); [S&D Consultoria — Regime Fiscal de Cabo Verde](https://consultoria.cv/en/regime-fiscal-de-cabo-verde-estrategias-essenciais-para-a-diaspora-e-investidores-estrangeiros/); [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes).

## National Minimum Wage

- From **2025-01-01**: **17,000$/month** in the private sector (up from 15,000$); **19,000$/month** in public administration.

Evidence: [Governo de Cabo Verde — Ajuste salário mínimo 2025](https://www.governo.cv/ajuste-salario-minimo-2025/); [Expresso das Ilhas — Novo salário mínimo nacional já vigora](https://expressodasilhas.cv/economia/2025/01/07/novo-salario-minimo-nacional-ja-vigora/95036).

## Código Laboral — working time, overtime, subsidies (2026-05-30 capture)

Cabo Verde employment is governed by the **Código Laboral** (Decreto-Legislativo 5/2007, republished/amended; overtime remuneration changed by **Decreto-Legislativo 1/2016, de 3 de fevereiro**). Secondary-source parameters relevant to payslip computation:

- **Working time:** normal **8h/day, 44h/week** (extendable to 4h/day extra, 60h/week by collective agreement; youth 7h/38h). Salary period ≤ 31 days, paid on the **last working day**, in national currency.
- **Overtime (trabalho extraordinário):** capped at **2h/day, 160h/year** (up to 300h/year with written consent). **Rate is disputed across secondary sources:** the Vendus employer guide states overtime is paid at **not less than +50%** of normal pay; an earlier search result cited a **+35% minimum** (possibly the pre-2016 figure or a first-tier rate). ⚠️ **Flag — verify against the primary Código Laboral / DL 1/2016 before production.** Typically tiered (higher on rest days/holidays).
- **Night work (trabalho noturno):** night = **22h–06h**; compensation **+25%** of basic salary (also due during annual/sick leave); night workers' overtime ≤ 7h/week.
- **Vacation (férias):** **22 dias úteis/year**, proportional if contract < 1 year; transferable/splittable by agreement; paid as if working normally.
- **Subsídio de Natal / 13.º:** referenced as a statutory right but the **CV-specific formula/timing was not captured** — still an open question (do not assume the Portuguese 13th/14th model).
- **Salary deductions** capped at **1/3** of pay; lawful: INPS, court decisions, indemnities, disciplinary fines, on-site meals, company services, advances.

Evidence: [Código Laboral CV — guia Vendus](https://www.vendus.cv/blog/codigo-laboral-de-cabo-verde-guia-pratico-para-empregadores/); [INPS — Código Laboral Cabo-verdiano (PDF)](https://inps.cv/download/codigo-laboral-cabo-verdiano/); republicação BO 2016-02-04 (DL 1/2016).

## Implementation impact for NOVA-ERP

- Confirms the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] choice to model deductions as **rule-versioned, source-linked configuration** rather than hard-coded constants: rates change by law (e.g. minimum wage jumped 41.6% in 2025) and the IRPS bracket scale is itself unresolved.
- `payroll_component_rules.legal_source_ref` should point at: Lei 78/VIII/2014 (IRPS), the current DNRE withholding table/formula, INPS contribution regulation, and the Código Laboral for subsidies/overtime.
- INPS 16%/8.5% split and the 24.5% total can seed the employer-charge and employee-deduction components, flagged provisional pending the ceiling value.

## Currency and verification needs (high-stakes)

- **Primary-law verification required** before production: ~~IRPS withholding~~ (done — DL 6/2015 + CIRPS); the INPS contribution-base floor/cap; and the **Código Laboral overtime rate (+35% vs +50% dispute) and the subsídio de Natal/13.º formula** against the primary Código Laboral / DL 1/2016.
- Most figures here are from **secondary web sources** (consultancies, an EOR guide, news); treat as orientation, confirm against DNRE/INPS official publications.
- Attempted on 2026-05-29 to extract the IRPS bracket scale directly from the primary [Código do IRPS — Lei 78/VIII/2014 PDF](https://www.ministeriopublico.cv/index.php/ministerio-publico/legislacao/category/13-ministerio-publico-na-jurisdicao-fiscal-e-aduaneira?download=229:codigo-de-irps); the PDF is compressed/non-machine-readable in this environment, so the exact escalão table could not be lifted. A human/OCR pass on the official text (or the DNRE withholding table) is needed to close [[Contradiction - IRPS Category A Withholding Brackets]].
