---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, iur, irps, payroll, retencao-fonte, primary-law, needs-review]
sources: []
related: ["[[Processamento de Salarios ERP]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]", "[[2026-05-29 - Schema Decision - Payroll Runs and Payslips]]", "[[Contradiction - IRPS Category A Withholding Brackets]]"]
confidence: high
---

# Portaria nº 5/2013 — Retenção do IUR sobre Trabalho Dependente

## What this is

The official Cape Verde regulation governing **monthly withholding on dependent-work income**, published in the Boletim Oficial, I Série nº 3, 10 January 2013, signed by the Minister of Finance (Cristina Duarte). It regulates withholding under the **IUR** (Imposto Único sobre os Rendimentos) regime, per Lei nº 23/VIII/2012 (OE 2013) and the Regulamento do IUR.

Evidence: `docs/docsfiscal/Portaria nº5 -2013 - Retenção IUR trabalho dependente.pdf` (Boletim Oficial, primary source).

> **Currency caution (high-stakes):** this is the **IUR** withholding regime. The **IRPS** (Imposto sobre o Rendimento das Pessoas Singulares, Lei nº 78/VIII/2014) later replaced IUR for individuals. The withholding *mechanism* below is authoritative and likely carried forward in form, but the **rates, brackets and parameters must be reconfirmed against the current IRPS-era withholding portaria** before production use. Treat the values here as the precise IUR-2013 baseline, not as confirmed current IRPS figures.

## Withholding mechanism (Articles 1–6)

- Withholding is computed by a **monthly formula**, optionally replaced by the **practical table (Anexo I)** in the cases foreseen; entities with **computerized payroll must use the formula, not the table** (art. 5º nº3).
- **Cap:** monthly withholding may not exceed **35%** of the income paid in the period (art. 2º nº3).
- **Monotonicity:** an income increase can never reduce the withheld amount, nor drop net-of-tax income below the prior bracket's limit (art. 2º nº4–5).
- **Holiday/Christmas subsidies** (subsídios de férias e Natal) are **always withheld autonomously** — never added to the month's salary; if paid fractionally, withhold the proportional part (art. 2º nº6–7).
- **Rounding:** the formula result is adjusted down to the nearest ten escudos (art. 4º nº4).
- **No withholding** when the resulting amount is below **100$** (art. 9º).
- Family/marital data drives the formula; if the employee does not provide it, the **"não casado"** (single) formula applies (art. 3º nº3–4).

## Monthly formula (Article 3)

Three variants (glyphs OCR-approximate; structure faithful):

- **Não casado / Casados dois titulares:** `I_R = [ (V_m · p · N_i − PA_i) − α_i · (ME + EF) ] / p`
- **Casado único titular:** `I_R = [ ( (V_m · p / 2) · N_i − PA_i ) · 2 − α_i · (ME + EF) ] / p`, with `N` resolved from `V_m · p / 2` (income splitting).

Where:
- `I_R` = tax to withhold; `V_m` = total monthly remuneration; `p` = number of annual salary payments (period).
- `N` = normal rate from the Article 7 table, indexed by annualized income `V_m · p` (or `V_m · p / 2` for single-titular couples).
- `PA_i` = parcela a abater (Article 7 table).
- `α_i` = family-charges percentage (Article 3 nº2 table).
- `ME` = Mínimo de Existência (set by law — value not in this Portaria).
- `EF` = Encargos Familiares, fixed at **640.000$00** for withholding purposes.

## Article 3 nº2 — family-charges coefficient α (2013)

| Escalão | Annualized income (`V_m·p`) | α |
| :-- | :-- | :-- |
| 1 | up to 408.843$ | 5.00% |
| 2 | 408.843$ – 860.163$ | 6.00% |
| 3 | 860.163$ – 1.720.327$ | 6.50% |
| 4 | 1.720.327$ – 2.580.490$ | 8.00% |
| 5 | over 2.580.490$ | 10.00% |

## Article 7 — taxable-income rate scale and parcela a abater

| Escalão | Rendimento colectável (annual) | Taxa normal | Taxa média | Parcela a abater (PA_i) |
| :-- | :-- | :-- | :-- | :-- |
| 1 | up to 408.843$ | 11.67% | 11.67% | 0$ |
| 2 | 408.843$ – 860.163$ | 15.56% | 13.71% | 15.904$ |
| 3 | 860.163$ – 1.720.327$ | 21.39% | 17.55% | 66.051$ |
| 4 | 1.720.327$ – 2.580.490$ | 27.22% | 20.77% | 166.347$ |
| 5 | over 2.580.490$ | 35.00% | — | 367.109$ |

This is the **IUR-2013 progressive marginal scale: 11.67% / 15.56% / 21.39% / 27.22% / 35%** — the precise figures that resolve the historical bracket question for the IUR era (see [[Contradiction - IRPS Category A Withholding Brackets]]).

## Anexo I — practical monthly withholding table (selected)

Maps monthly remuneration to a rate and a withheld amount; full table runs from 18.333$ to over 399.567$:

| Monthly remuneration | Rate | Tax to withhold |
| :-- | :-- | :-- |
| 18.333$ – 30.701$ | 0.0% | 0$ |
| 30.702$ – 32.224$ | 0.5% | 100$–177$ |
| 51.093$ – 53.523$ | 5.0% | 2.326$–2.703$ |
| 85.833$ – 89.617$ | 10.0% | 8.198$–9.006$ |
| 154.662$ – 161.015$ | 15.0% | 22.504$–24.233$ |
| 244.396$ – 252.569$ | 20.0% | 47.780$–50.640$ |
| 361.331$ – 379.488$ | 25.0% | 88.707$–95.062$ |
| over 399.567$ | 26.0% | 102.090$–109.902$ |

- **IUR-2013 monthly withholding floor: 0% up to 30.701$/month; withholding starts at 30.702$.** (Secondary sources report a later IRPS-era monthly threshold of 35.000$ — an evolution to reconcile.)

## Other categories (Article 8)

- Predial income and own-account service provision (not dependent/independent liberal work): **10%** withholding, for continuous work or occasional amounts ≥ 5.000$.
- Service provisions: withholding falls only on the **labour (mão-de-obra)** portion of the invoice.

## Implementation impact for NOVA-ERP

- Gives the [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] payroll engine a **concrete, source-linked withholding model**: `payroll_component_rules` for IUR/IRPS withholding can encode this exact formula, the α table, the rate/PA table and the 35% cap, with `legal_source_ref = Portaria 5/2013` and a successor reference once the IRPS-era portaria is obtained.
- Confirms specific design choices: autonomous withholding for holiday/Christmas subsidies; the 100$ no-withhold floor; rounding to the lower ten escudos; income-splitting for single-titular couples; the requirement that computerized payroll use the formula, not the table.
- `EF = 640.000$` and `ME` (Mínimo de Existência) are parameters the engine must hold as versioned config; `ME`'s value is set elsewhere by law and still needs capture.

## Verification needs

- **Confirm the current IRPS-era withholding portaria** (post-Lei 78/VIII/2014) and whether it superseded Portaria 5/2013; refresh the α / rate / PA tables and the monthly table accordingly.
- Capture the current **Mínimo de Existência (ME)** value and any OE-year updates to `EF`, brackets and the monthly threshold.
