---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, fiscalidade, imposto-de-selo, primary-law, cabo-verde]
sources: ["raw/assets/selo/Imposto_de_Selo_Lei_33_Republicacao.pdf"]
related: ["[[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-29 - Codigo do IVA Cabo Verde]]", "[[Tesouraria ERP]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]"]
confidence: high
---

# Lei 33/VII/2008 — Código do Imposto de Selo (Cabo Verde)

## What this is

The **Código do Imposto de Selo** of Cabo Verde — **Lei nº 33/VII/2008, de 24 de Novembro** (signed by President Pedro Pires; AN President Aristides Lima), in the **republicação** carried by **B.O. I Série nº 3, 8 de Janeiro de 2015** (the same Boletim issue as the CIRPC). This closes the gap left by [[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]], which captured only the rate table (the tail starting at art. 27º): this page documents the **incidence / general part / exemptions, arts 1–26**, parsed from the preserved PDF (`raw/assets/selo/`, 7 pp.; the IS articulado follows an agricultural-tariff annex from the same B.O.).

## Structure (Parte Geral + Parte Especial)

**PARTE I — Parte Geral**
- **Art. 1º Incidência objectiva** — IS incides on *operações financeiras, operações societárias e actos jurídicos documentados* listed in the special part. **§2 (non-cumulation): operations subject to IVA and not exempt are OUTSIDE the scope of IS.** → IS and [[2026-05-29 - Codigo do IVA Cabo Verde|IVA]] are mutually exclusive on the same operation.
- **Art. 2º Incidência subjectiva** — sujeitos passivos = those obliged to liquidate/pay; the tax is passed through (**repercussão**) to the economic bearer where the special part provides; solidary responsibility per the Código Geral Tributário.
- **Art. 3º Incidência territorial** — acts/operations/transmissions occurring in national territory (celebrated, practised, issued or formalised in Cabo Verde), **plus** acts occurring abroad in the cases the special part specifies.
- **Art. 4º Facto gerador** — the chargeable event.
- **Art. 5º Isenções comuns** — common exemptions.
- **Art. 6º Valor tributável** — the taxable value follows the special part; for **contratos de valor indeterminado**, value is determined by a fallback rule.
- **Art. 7º Taxas** — rates per the special part (= the Tabela documented in [[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]]).

**PARTE ESPECIAL** — each category repeats incidência objectiva / subjectiva / repercussão / facto gerador / isenções:
- **Arts. 8º–12º — Operações financeiras** (crédito, juros, serviços financeiros, garantias).
- **Arts. 13º–17º — Operações societárias** — e.g. art. 13º taxes the **constituição de sociedades comerciais** on the *valor real dos bens entregues pelos sócios* (after deducting assumed obligations/charges); plus aumentos de capital, etc.
- **Arts. 18º–22º — Actos jurídicos documentados** (notariais, registo, processuais, contratos).

**Liquidação e pagamento**
- **Art. 23º Liquidação**; **Art. 24º Arredondamento e valor mínimo**; **Art. 25º Pagamento**; **Art. 26º Caducidade, prescrição e juros**.

## Implementation impact for NOVA-ERP

- **Non-cumulation gate (art. 1º §2) is the key rule:** the document/treasury engine must not apply IS to an operation already within IVA scope (and not IVA-exempt). Tax determination should check IVA applicability first; IS applies to the financial/societária/documental operations that IVA does not reach (credit, interest, financial services, guarantees, insurance, corporate acts, notarial/registry acts). Aligns with [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]] (financial-document taxes) and the SAF-T `TaxType`.
- **Repercussão** means IS is often borne by the counterparty but liquidated/paid by the sujeito passivo — model the obligation and its pass-through separately.
- **Territoriality (art. 3º)** + the per-verba **valor tributável** and rates (Tabela) feed the `tax_maps` IS rules. Rates: see [[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]] (crédito 0,5%; serviços financeiros/seguros 3,5%; garantias/letras/societárias 0,5%; actos notariais/registo/processuais 15%; actos administrativos/contratos 1.000$00 fixo).
- **Art. 24º arredondamento e valor mínimo** must be encoded in IS computation (mirrors the DL 6/2015 rounding discipline for IRPS).

## Open questions / verification

- Subsequent **OE-year amendments** to rates or exemptions (the code is 2008, republished 2015) — re-check current rates before production IS computation.
- Exact **valor tributável** bases and per-verba exemptions inside arts 8º–22º (extract per verba when an IS-bearing feature is built — financial-document or notarial-act flows).
- Whether any IS verbas were absorbed/repealed by later IVA or financial-sector legislation.
