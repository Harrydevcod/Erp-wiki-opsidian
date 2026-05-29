---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, payroll, inps, irps, salario-minimo, cabo-verde, needs-review]
sources: []
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Contradiction - IRPS Category A Withholding Brackets]]"]
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
- A **contribution ceiling** applies (salary above the ceiling is contributed only up to the ceiling). The exact ceiling value was **not captured** and requires confirmation.

Evidence: [INPS — Contribuições](https://inps.cv/contribuicoes/); [INPS — Obrigações](https://inps.cv/obrigacoes/); [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes) (states 16% / 8.5% / 24.5% expected for 2026, with a monthly ceiling).

## IRPS — Personal Income Tax on Dependent Work (Category A)

- Legal authority: **Lei nº 78/VIII/2014** (Código do IRPS).
- Category A (trabalho dependente) is taxed by **retenção na fonte com caráter final** (final withholding), not the declarative method.
- The employer withholds monthly using the **official DNRE withholding tables or the withholding formula**; the source guidance recommends using the **formula, not the practical tables**, to avoid rounding errors.
- Withholding threshold: applies from annual income **> 420,000$** (i.e. monthly income **> 35,000$**, = 1/12 of 420,000$).
- Progressive rates: reported by one source as ranging **16.5%–27.5%**. A different illustrative bracket table circulates (see contradiction). The exact current bracket scale is **unresolved** — see [[Contradiction - IRPS Category A Withholding Brackets]].
- Deductions/allowances: personal allowance, dependents (spouse/children), documented health/education/housing within limits, and the employee's 8.5% INPS share is typically deductible from the IRPS base.

Evidence: [Flyer IRPS — Ministério das Finanças](https://www.mf.gov.cv/documents/54571/273413/Flyer%20IRPS.pdf); [Código do IRPS — Lei 78/VIII/2014](https://www.ministeriopublico.cv/index.php/ministerio-publico/legislacao/category/13-ministerio-publico-na-jurisdicao-fiscal-e-aduaneira?download=229:codigo-de-irps); [S&D Consultoria — Regime Fiscal de Cabo Verde](https://consultoria.cv/en/regime-fiscal-de-cabo-verde-estrategias-essenciais-para-a-diaspora-e-investidores-estrangeiros/); [Rivermate — Taxes in Cabo Verde](https://rivermate.com/guides/cabo-verde/taxes).

## National Minimum Wage

- From **2025-01-01**: **17,000$/month** in the private sector (up from 15,000$); **19,000$/month** in public administration.

Evidence: [Governo de Cabo Verde — Ajuste salário mínimo 2025](https://www.governo.cv/ajuste-salario-minimo-2025/); [Expresso das Ilhas — Novo salário mínimo nacional já vigora](https://expressodasilhas.cv/economia/2025/01/07/novo-salario-minimo-nacional-ja-vigora/95036).

## Labor framework (context)

- Cabo Verde employment is governed by the **Código Laboral**, which sets working hours, leave, holiday/Christmas subsidies, overtime and termination rules. Specific statutory subsidy and overtime formulas were **not captured** here and remain a payroll open question.

## Implementation impact for NOVA-ERP

- Confirms the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] choice to model deductions as **rule-versioned, source-linked configuration** rather than hard-coded constants: rates change by law (e.g. minimum wage jumped 41.6% in 2025) and the IRPS bracket scale is itself unresolved.
- `payroll_component_rules.legal_source_ref` should point at: Lei 78/VIII/2014 (IRPS), the current DNRE withholding table/formula, INPS contribution regulation, and the Código Laboral for subsidies/overtime.
- INPS 16%/8.5% split and the 24.5% total can seed the employer-charge and employee-deduction components, flagged provisional pending the ceiling value.

## Currency and verification needs (high-stakes)

- **Primary-law verification required** before production: official IRPS withholding table/formula and current brackets; INPS contribution ceiling value; Código Laboral subsidy/overtime formulas.
- Most figures here are from **secondary web sources** (consultancies, an EOR guide, news); treat as orientation, confirm against DNRE/INPS official publications.
