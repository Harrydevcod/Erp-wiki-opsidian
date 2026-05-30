---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, irps, irpc, iva, needs-review]
sources: []
related: ["[[Fiscalidade Cabo Verde]]", "[[Contradiction - IRPS Category A Withholding Brackets]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Cabo Verde]]"]
confidence: medium
---

# 2017-10-25 - Sistema Fiscal de Cabo Verde (CI Síntese)

## Provenance

- **Title:** "Sistema Fiscal de Cabo Verde" — overview of the post-2015-reform tax system.
- **Author (PDF metadata):** CI / Assessor Jurídico — Marlon Chantre. Produced in Microsoft Word 2013, CreationDate `2017-10-25`.
- **Host:** Cabo Verde TradeInvest — `https://www.cvtradeinvest.cv/assets/files/Sistema-Fiscal-Cabo-Verde.cleaned.pdf` (also mirrored at cvtradeinvest.com).
- **Extraction:** fetched and parsed with pypdf in the sandbox (19 pages, clean text).
- **Authority:** **secondary** — an investment-promotion legal summary, not statute. Useful because it independently restates the IRPS/IRPC rate structure of the 2015 reform with exact bracket values. Rate values still need confirmation against the current statute and OE-year updates.

## Why it matters

This is the first source in the vault that gives the **IRPS-era progressive rate scale with explicit bracket boundaries**, corroborating the 16.5%–27.5% band previously attributed to a single consultancy. It is the key evidence that the **IUR withholding scale (11.67%–35%, [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]]) was superseded by IRPS** (Lei nº 78/VIII/2014). Directly feeds the withholding engine in [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] and resolves [[Contradiction - IRPS Category A Withholding Brackets]].

## Key claims

### IRPS (Imposto sobre o Rendimento das Pessoas Singulares)

- **Categories of income:** A (trabalho dependente e pensões), B, C, D, E.
- **Progressive scale on aggregated/englobamento income** (taxa de imposto aplicável aos rendimentos objeto de englobamento):
  - Isenção (0%) **até 220.000$00** anuais.
  - **16,5%** para rendimentos **até 960.000$00** anuais.
  - **23,1%** para rendimentos **> 960.000$00 e até 1.800.000$00** anuais.
  - **27,5%** para rendimentos **> 1.800.000$00** anuais.
- **Retention at source by category:**
  - **Categoria A** (trabalho dependente/pensões): subject to **progressive + liberatório** withholding **from 420.000$00/year or 35.000$00/month**. (Exact monthly band table = the Regime de Retenções decree, not in this doc.)
  - **Categoria B**: **15%** por conta. ⚠️ **Corrected by primary law:** [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] Art. 8.º sets B at **20%** (4% REMPE) — treat the 15% here as inaccurate.
  - **Categoria C**: **10%** liberatória. ⚠️ **Corrected:** the decree sets C at **20%** (Art. 9.º).
  - **Categoria D**: **20%** liberatória (10% for art. 14 nº2 f)/j) income), sem englobamento. *(matches the decree)*
  - **Categoria E**: **1%** (art. 17 nº1 a–d) or **20%** (art. 17 nº2), liberatória, sem englobamento. *(matches the decree)*

### IRPC (collective income) — context

- General rate **25%**; **4%** for taxpayers under the simplified (non-organized-accounting) regime.
- Non-resident with permanent establishment: 20% capital income / 10% interest etc.
- Autonomous taxation (tributação autónoma): **40%** undocumented expense; **10%** other listed items.

### Other taxes (context only)

- **ICE** (special consumption) headline **15%**; Anexo I items **10%**.
- **Imposto de Selo (IS):** variable per verba, max **15%**; property transmissions **1,5%**.
- Mortgage/health/education interest deductibility caps (1ª habitação limit 9.000.000$).

## Contradictions / tensions

- The IRPS scale here (3 bands + exemption, **27,5% ceiling**) is fundamentally different from the IUR scale (5 bands, **35% ceiling**) — see [[Contradiction - IRPS Category A Withholding Brackets]]. This doc resolves the direction (IRPS replaced IUR) but is secondary.
- Note two distinct thresholds: **englobamento exemption ≤ 220.000$/yr** vs **Category A retention floor 420.000$/yr (35.000$/mo)**. Do not conflate them.

## Open questions

- The **exact monthly Category A retention band table** (taxa + parcela a abater per bracket) — set by the Regime de Retenções na Fonte decree, still to obtain.
- Whether the 16,5/23,1/27,5% values and the 220.000$/420.000$ thresholds have been updated by a later Orçamento de Estado (this doc is 2017).
- Current **Mínimo de Existência** value.
