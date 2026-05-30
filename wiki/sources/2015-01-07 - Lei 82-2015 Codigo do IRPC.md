---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, irpc, accounting, depreciacao, primary-law]
sources: []
related: ["[[Fiscalidade Cabo Verde]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]", "[[SAF-T CV]]", "[[Cabo Verde]]"]
confidence: high
---

# 2015-01-07 - Lei nº 82/VIII/2015 — Código do IRPC

## Provenance

- **Primary law.** Lei nº **82/VIII/2015, de 7 de Janeiro** — Código do Imposto sobre o Rendimento das Pessoas Colectivas (CIRPC). Published in **Boletim Oficial I Série nº 3, 8 de Janeiro de 2015**. Part of the 2015 fiscal reform; in force for periods from 2015.
- **Source:** official DNRE legislation library (`mf.gov.cv`, folder 64542). Downloaded and pypdf-parsed in the sandbox; preserved at `raw/assets/irpc/Lei_82_2015_Codigo_IRPC.pdf` (35 pp.; the same B.O. compilation also carries the **Imposto de Selo** annex — Tabela de verbas: crédito 0,5%, serviços financeiros/seguros 3,5%, actos notariais/registo/processuais 15%).
- **Authority:** **primary/operative** for corporate income tax. Parent of the depreciation regime [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] (issued under CIRPC art. 43º) and the IRPC withholding rates referenced by [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]].

## Why it matters

Completes the corporate-tax primary-law axis to match the IRPS axis. Supplies the IRPC rate, autonomous-taxation rates, fiscal-loss carryforward and impairment-provision rules that the accounting and fixed-asset ADRs need, and ties the **TEU (Tributo Especial Unificado)** SAF-T tax type to the REMPE simplified regime.

## Key claims

### Art. 84º — Taxas

- **25%** general IRPC rate, for taxpayers under the **regime de contabilidade organizada**.
- **4%** on **volume de negócios** for the **micro/pequenas empresas (REMPE)** simplified regime (art. 95º) — this "refaz a colecta do **tributo especial unificado**" (the **TEU** seen in the SAF-T `TaxType` code list, [[SAF-T CV Code Lists]]).

### Art. 89º — Taxas de tributação autónoma (contabilidade organizada)

- **40%** — despesas **não documentadas** (also disallowed as a cost, art. 29º).
- **10%** — encargos com **viaturas ligeiras de passageiros/mistas, motos e motociclos** (depreciações, rendas/alugueres, seguros, manutenção, combustíveis, impostos de posse/uso).
- **10%** — despesas de **representação** (recepções, refeições, viagens, espectáculos a clientes/fornecedores).
- Ajudas de custo / compensação por deslocação em viatura própria (further rate, to confirm).

### Art. 59º — Dedução de prejuízos fiscais (loss carryforward)

- Fiscal losses are deductible from taxable profits of **up to 7 (sete) períodos de tributação posteriores**.
- The deduction in each period **cannot exceed 50%** of that period's taxable profit.
- Opting into the REMPE simplified regime **extinguishes** the right to deduct prior fiscal losses (art. ~19/95).

### Impairment — créditos de cobrança duvidosa (perdas por imparidade)

Maximum accumulated impairment as a % of overdue credits by age of arrears:

| Mora | % |
|---|---|
| > 6 e ≤ 12 meses | 25% |
| > 12 e ≤ 18 meses | 50% |
| > 18 e ≤ 24 meses | 75% |
| > 24 meses | 100% |

Excludes credits on the State and similar.

### Other

- **Art. 43º** — depreciações e amortizações (the enabling article for [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]).
- **Art. 85º** — retention rates for residents / non-residents with permanent establishment (capitais, per CIRPS definitions).
- Pagamentos fraccionados; REMPE quarterly 4% of prior-quarter turnover (definitive).

## Implementation impact

- **Accounting ADR / tax maps:** encode the 25% (organized) / 4% TEU (REMPE) rate split; the 7-year / 50%-cap loss-carryforward engine; the 25/50/75/100% impairment schedule as a provisioning rule over overdue receivables (ties to the Treasury obligation ledger).
- **Fixed Assets ADR:** the **10% autonomous taxation on light-vehicle/moto charges** is a posting consequence of vehicle assets — a fiscal add-on beyond the depreciation cap (4.000.000$, Portaria 42/2015 art. 10º).
- **SAF-T:** confirms **TEU** as the REMPE corporate levy in the tax table.

## Open questions

- Confirm the exact **B.O. issue/date** of Lei 82/2015 (PDF header not yet parsed) and rename this page.
- The ajudas-de-custo autonomous-taxation rate (art. 89º d) — extract when needed.
- Whether later OE laws changed the 25%/4% rates or the loss-carryforward 7yr/50% parameters (2015 baseline).
- Sibling regime detail: the REMPE special law (regime jurídico especial das micro e pequenas empresas) defining TEU mechanics.
