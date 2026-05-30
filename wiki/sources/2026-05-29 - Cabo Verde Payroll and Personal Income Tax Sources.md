---
type: source
status: active
created: 2026-05-29
updated: 2026-05-30
tags: [source, fiscalidade, payroll, inps, irps, codigo-laboral, salario-minimo, cabo-verde]
sources: ["raw/assets/laboral/Codigo_Laboral_CV.pdf", "raw/assets/irps/Lei_78_2014_Codigo_IRPS.pdf", "raw/assets/irps/Decreto-Lei_6_2015_Retencao_na_Fonte.pdf"]
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Contradiction - IRPS Category A Withholding Brackets]]", "[[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]", "[[2014-12-31 - Lei 78-2014 Codigo do IRPS]]"]
confidence: high
---

# Cabo Verde Payroll and Personal Income Tax Sources

## What this is

The statutory parameters governing Cabo Verde payroll: INPS social-security contributions, IRPS (personal income tax) withholding on dependent work, the national minimum wage, and Código Laboral working-time/overtime/subsidy rules. Originally a 2026-05-29 web-research capture; **as of 2026-05-30 the core figures are anchored in primary law** — IRPS withholding ([[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]), the IRPS scale + mínimo de existência ([[2014-12-31 - Lei 78-2014 Codigo do IRPS]] art. 45º), and Código Laboral overtime/night/leave/Natal (DL 5/2007 + DL 1/2016, preserved at `raw/assets/laboral/`). The only material residual is the **INPS contribution-base ceiling value**. Unblocks the payroll schema design ([[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]); OE-year re-indexing of thresholds should still be re-checked annually.

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
- **Mínimo de existência — RESOLVED (primary):** CIRPS **art. 45º** is titled *"Taxa de imposto e mínimo de existência"* and §2 reads *"Está isento de tributação o rendimento colectável até ao montante de 220.000$00."* So the **mínimo de existência IS the 220.000$ exemption of taxable income — not a separate indexed value.** (Confirmed in the preserved `raw/assets/irps/Lei_78_2014_Codigo_IRPS.pdf`.)
- Deductions/allowances: personal allowance, dependents (spouse/children), documented health/education/housing within limits, and the employee's 8.5% INPS share is typically deductible from the IRPS base.

Evidence: [Flyer IRPS — Ministério das Finanças](https://www.mf.gov.cv/documents/54571/273413/Flyer%20IRPS.pdf); [Código do IRPS — Lei 78/VIII/2014](https://www.ministeriopublico.cv/index.php/ministerio-publico/legislacao/category/13-ministerio-publico-na-jurisdicao-fiscal-e-aduaneira?download=229:codigo-de-irps); [S&D Consultoria — Regime Fiscal de Cabo Verde](https://consultoria.cv/en/regime-fiscal-de-cabo-verde-estrategias-essenciais-para-a-diaspora-e-investidores-estrangeiros/); [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes).

## National Minimum Wage

- From **2025-01-01**: **17,000$/month** in the private sector (up from 15,000$); **19,000$/month** in public administration.

Evidence: [Governo de Cabo Verde — Ajuste salário mínimo 2025](https://www.governo.cv/ajuste-salario-minimo-2025/); [Expresso das Ilhas — Novo salário mínimo nacional já vigora](https://expressodasilhas.cv/economia/2025/01/07/novo-salario-minimo-nacional-ja-vigora/95036).

## Código Laboral — working time, overtime, subsidies (PRIMARY LAW, 2026-05-30)

Cabo Verde employment is governed by the **Código Laboral — Decreto-Legislativo nº 5/2007** (B.O. I Série nº 37 Sup., 16-10-2007), with overtime remuneration **amended by Decreto-Legislativo nº 1/2016, de 3 de fevereiro**. The full DL 5/2007 text was obtained and parsed; preserved at `raw/assets/laboral/Codigo_Laboral_CV.pdf` (64 pp.). The article-level parameters below are now **primary-sourced** (the 2016 amendment to art. 207º is taken from the DL 1/2016 republication, since the preserved PDF is the original 2007 text).

- **Working time:** normal **8h/day, 44h/week**. Salary period ≤ 31 days, paid on the **last working day**, in national currency.
- **Overtime (trabalho extraordinário) — DISPUTE RESOLVED:** **art. 207º** originally read *"acréscimo não inferior a **50%** da retribuição normal"* (DL 5/2007, confirmed verbatim in the preserved PDF). **DL 1/2016 amended art. 207º to "não inferior a 35%".** So the **current rate is +35%**; the Vendus guide's +50% was the **pre-2016 (superseded) figure**. Caps: 2h/day, 160h/year (up to 300h with written consent). Rest-day work (**art. 208º**) = **+100%**.
- **Night work (trabalho noturno) — art. 169º:** night workers are entitled to a subsídio **não inferior a 25%** of basic salary; shift (turno) work = subsídio "a acordar". (Night period 22h–06h.)
- **Vacation (férias):** **22 dias úteis/year**, proportional if contract < 1 year; paid as if working normally.
- **Gratificação de Natal / 13.º mês — art. 206º (CV-SPECIFIC, NOT a mandatory 13th):** the Código frames it as *"Nos casos em que **seja concedido pelo empregador**, a gratificação de Natal, 13º mês ou prestação similar…"* — i.e. it is **discretionary** (granted by the employer or by contract/IRCT), **not a statutory entitlement** like the Portuguese 13th. **When granted, the amount is modulated by attendance** over the prior 12 months: **≤3 faltas → 100%; 4–6 → 75%; 7–10 → 50%; >10 → not granted**; each *falta injustificada* counts double (faltas under art. 186º nº2 a–c excluded). ⚠️ Do **not** hard-code a mandatory 13th — model it as an optional, attendance-scaled component.
- **Salary deductions** capped at **1/3** of pay.

Evidence: `raw/assets/laboral/Codigo_Laboral_CV.pdf` (DL 5/2007, arts. 169º, 206º, 207º, 208º); DL 1/2016 republication for the current art. 207º +35% — [republicação BO 2016-02-04](https://www.ministeriopublico.cv/index.php/ministerio-publico/legislacao/category/14-ministerio-publico-na-jurisdicao-laboral?download=235:republicacao); cross-checked [guia Vendus](https://www.vendus.cv/blog/codigo-laboral-de-cabo-verde-guia-pratico-para-empregadores/).

## Implementation impact for NOVA-ERP

- Confirms the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] choice to model deductions as **rule-versioned, source-linked configuration** rather than hard-coded constants: rates change by law (e.g. minimum wage jumped 41.6% in 2025) and the IRPS bracket scale is itself unresolved.
- `payroll_component_rules.legal_source_ref` should point at: Lei 78/VIII/2014 (IRPS), the current DNRE withholding table/formula, INPS contribution regulation, and the Código Laboral for subsidies/overtime.
- INPS 16%/8.5% split and the 24.5% total can seed the employer-charge and employee-deduction components, flagged provisional pending the ceiling value.

## Currency and verification needs (high-stakes)

- **Resolved against primary law (2026-05-30):** ~~IRPS withholding~~ (DL 6/2015 + CIRPS); ~~mínimo de existência~~ (= 220.000$ isenção, CIRPS art. 45º nº2); ~~Código Laboral overtime +35% vs +50%~~ (art. 207º → 35% via DL 1/2016, was 50%); ~~subsídio de Natal/13.º~~ (art. 206º — discretionary, attendance-scaled, **not** a mandatory 13th).
- **Still residual (minor):** the **INPS contribution-base upper ceiling (teto)** — inps.cv confirms the 24.5% (16%+8.5%) rate and a min-wage-tracking floor, and some sources reference an upper "teto", but **no numeric ceiling value was located**; confirm with INPS or model `max(gross, floor)` with no cap until confirmed. OE-year re-indexing of the IRPS thresholds (80.000$/150.000$ monthly; 960.000$/1.800.000$ annual) also still warrants a yearly check.
- The headline rate/scale figures are now **primary-sourced**; remaining secondary-source items (EOR/consultancy/news) are limited to orientation context.
