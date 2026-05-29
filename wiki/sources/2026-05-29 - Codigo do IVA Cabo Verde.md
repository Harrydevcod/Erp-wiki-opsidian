---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, fiscalidade, iva, primary-law, needs-review]
sources: []
related: ["[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]", "[[SAF-T CV]]", "[[Compras e Vendas ERP]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]"]
confidence: high
---

# Código do IVA — Cabo Verde

## What this is

The Cape Verde Value-Added Tax code (Código do Imposto sobre o Valor Acrescentado), read from the primary text in `docs/docsfiscal/Código IVA.pdf` (48 pages). This page captures the **structure and the durable rules** relevant to NOVA-ERP fiscal/document/accounting design; it is not a full article-by-article transcription.

> **Currency caution:** the law identity/version and any later OE amendments are not established from this copy. The 15% rate and regime mechanics are durable, but **rates, exemptions and regime thresholds must be confirmed against the current consolidated IVA code and the annual OE** before production.

## Standard rate and base

- **Standard IVA rate: 15%** (art. 17º — Taxa do imposto). No reduced-rate scale is evident in this copy beyond the simplified-regime mechanism below.
- Taxable base on internal operations (art. 15º) and on imports (art. 16º); foreign-currency operations converted at the Banco de Cabo Verde selling rate.
- Facto gerador / exigibilidade (art. 7º–8º) define when tax becomes due.

## Structure (chapters)

- **I — Incidência** (art. 1º–8º): scope, taxable persons, supply of goods, services, imports, place of supply, chargeable event.
- **II — Isenções** (art. 9º–14º): exempt supplies/services, non-profit bodies, **renúncia à isenção** (art. 11º), exempt imports, special customs regimes.
- **III — Valor tributável** (art. 15º–16º).
- **IV — Taxas** (art. 17º): 15%.
- **V — Liquidação e pagamento / dedução** (art. 18º–24º): input tax (`imposto suportado`), conditions for deduction (art. 19º), **exclusions from deduction** (art. 20º), birth/exercise of the deduction right (art. 21º), **partial deduction / pro-rata** (art. 22º), self-assessed payment (art. 23º).
- **Obrigações** (art. 25º–46º): **invoice/equivalent-document issuance (art. 32º)**, repercussão do imposto (art. 33º), faturação com imposto incluído for retail (art. 35º), dispensa de faturação (art. 36º), **periodic declaration (art. 37º) — monthly**, accounting organization and registers (art. 39º–46º).
- **Regime de isenção** (art. 47º–53º): small-taxpayer exemption regime (no deduction right; option for normal regime art. 49º).
- **Regime simplificado** (art. 54º–63º): tax computed by **applying 5% to the value of sales/services** rather than full input/output; options to switch regimes; the **volume-de-negócios threshold for the regime is fixed by despacho** of the Finance minister (not hard-coded in the code).
- **VI — Fiscalização** (art. 68º–69º); **VII — Determinação oficiosa** (art. 71º+): missing declaration, omissions/inaccuracies, presumptions.

## Regimes (summary)

- **Regime normal:** full output IVA (15%) minus deductible input IVA; monthly periodic declaration and payment.
- **Regime de isenção:** exempt small taxpayers, no input-tax deduction; can opt into normal regime.
- **Regime simplificado:** tax = **5% × sales/services value**; thresholds set by ministerial despacho; switch rules on crossing the limit (art. 54º).

## Implementation impact for NOVA-ERP

- **Tax model:** the document/accounting layers must support at least the **15% standard rate plus exempt (0/isento) and the 5% simplified-regime computation**, with the tenant's IVA regime (normal / isenção / simplificado) as configuration. This feeds the `tax_maps` (IVA↔account↔SAF-T) in [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] and the IVA fields on [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]].
- **Deduction engine:** input-tax deductibility with exclusions (art. 20º) and **pro-rata partial deduction** (art. 22º) is real logic the accounting/fiscal layer must model, not a flat credit.
- **Periodicity:** IVA is a **monthly** self-assessed declaration (art. 37º/23º) — the fiscal calendar and SAF-T/reporting cadence should assume monthly IVA.
- **Invoices:** issuance is a legal obligation (art. 32º); retail may use tax-inclusive pricing (art. 35º) — relevant to document totals and e-Fatura payloads.
- **Regime as config:** exemption/simplified thresholds are set by despacho, so model the tenant IVA regime and thresholds as **versioned configuration**, consistent with how payroll/depreciation parameters are handled.

## Verification needs

- Confirm the **current consolidated IVA code** (law number + amendments) and whether the **15% rate**, the **5% simplified rate** and any **reduced/exempt categories** changed via later OE.
- Capture the current **volume-de-negócios thresholds** (set by despacho) for the isenção and simplificado regimes.
