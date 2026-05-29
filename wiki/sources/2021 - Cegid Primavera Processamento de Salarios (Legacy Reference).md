---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, cegid-primavera, payroll, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Processamento de Salarios ERP]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]"]
confidence: medium
---

# Cegid Primavera — Processamento de Salários (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — Processamento de Salários" training manual (2021-VC1, 118 pp.), `docs/docsfiscal/RPG001 - Using - Processamento de Salários (2021-VC1).pdf`. It is **legacy ERP workflow reference**, not legal authority and **not target architecture**. Per the vault contract, the value is in translating its operational flow into a NOVA-ERP design rationale — adopting good domain coverage, rejecting editable/UI-driven patterns that break auditability.

## Legacy workflow (as documented)

- **Employee admission / ficha do funcionário** with tabs: Identificação, Dados Fiscais, Processamento, Pagamento, **Regimes de Proteção** (Segurança Social/INPS, Seguro de Acidentes de Trabalho, Sindicato), Carreira, **Agregado Familiar**.
- **Processing:** individual and **batch** (em lote); **anulação do processamento** (cancel a run).
- **Monthly variables** (per employee and batch): Faltas, Horas Extra, Remunerações e Descontos, Subsídio de Alimentação, Subsídio de Turno, Ausências Temporárias e Prolongadas, Registo de Férias.
- **Outputs:** Emissão de Recibos (payslips), Pagamentos.
- **Special runs:** Processamento Extraordinário, **Subsídio de Férias**, **Subsídio de Natal**, Vencimento com **Retroativos**.
- **Closing/compliance:** Obrigações Fiscais, Cadastro do Funcionário, Mapas de Análise, **Abertura de Ano**.

## Translation to NOVA-ERP

**Adopt (good domain coverage):**
- The employee master-data decomposition (identity, fiscal data, payment data, protection regimes, family aggregate, career) maps cleanly to `employees` + `employment_terms` in [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]; **Agregado Familiar** and **Regimes de Proteção** directly feed the IRPS family-charges (`α`, marital status) and INPS inputs from [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]].
- **Batch + individual processing** and the **monthly-variables** set (faltas, horas extra, subsídios, ausências, férias) confirm the `payroll_variables` and `payroll_components` design.
- **Autonomous holiday/Christmas subsidy runs** match the legal requirement (Portaria 5/2013 art. 2º nº6) for autonomous withholding — model them as distinct `payroll_runs` scopes, not lines added to a monthly run.
- **Retroativos** and **anulação** confirm the need for recalculation lineage and run cancellation states.

**Adapt:**
- Legacy "anulação do processamento" should become **superseding/reversing runs** with audit lineage, not destructive edits, per the ADR's immutable-approved-run rule.
- INPS/IRPS handling should be **rule-versioned config** (Portaria-linked), not the manual's embedded tables.

**Do not copy:**
- UI-centric editing of processed values; NOVA-ERP keeps approved runs immutable and privacy-restricted (salary fields gated by `payroll.salary_view`).
- Treating the legacy fiscal maps as current authority — Cabo Verde statutory maps must be confirmed against current law.

## Open questions surfaced

- Which statutory **mapas de análise / obrigações fiscais** (e.g., INPS FOS, IRPS withholding maps) must NOVA-ERP produce, and in what format?
- Subsídio de Turno / Subsídio de Alimentação: which are statutory vs employer-discretionary, and their tax/INPS treatment?
- "Abertura de Ano" — what annual rollover state does payroll need (carry-over of férias, accumulated bases)?

## Verification needs

- This is a Portugal-oriented Cegid product manual; **Cape Verde-specific statutory behavior** (INPS, IRPS maps, labour subsidies) must come from CV law, not this manual.
