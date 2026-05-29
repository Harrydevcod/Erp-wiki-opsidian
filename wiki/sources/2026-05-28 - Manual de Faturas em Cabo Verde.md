---
type: source
status: active
created: 2026-05-28
updated: 2026-05-28
tags: [source, fiscalidade, faturacao, cabo-verde, dnre]
sources: ["docs/docsfiscal/MANUAL DE FATURAS.pdf", "[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]"]
related: ["[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Compras e Vendas ERP]]", "[[DNRE]]", "[[e-Fatura Cabo Verde]]"]
confidence: mixed
---

# Manual de Faturas em Cabo Verde

## Source Profile

`docs/docsfiscal/MANUAL DE FATURAS.pdf` is a DNRE/SITA guide titled "Manual de Faturas em Cabo Verde", version 1.0, dated May 2018.

The source explicitly says it is orientative and non-normative, and does not replace consultation of current legislation and amendments. For [[NOVA-ERP]], it is useful as an invoice-rule map and implementation checklist, but not enough by itself for a production compliance claim.

Current-status check: [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] classifies the manual's rules after modern e-Fatura. Fiscal substance such as invoice content, numbering, rectification, REMPE and audit obligations largely survives; old electronic-invoice/paper-era processing mechanisms are superseded or narrowed by modern DFE XML, digital signature, IUD, DNRE authorization and credentialing.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 1-2.

## Summary

The manual consolidates Cabo Verde invoice rules around IVA, invoice issuance, required invoice content, invoice timing, invoice-processing methods, authorized printers, retail sale tickets, REMPE, state/public works invoicing, reverse-charge wording, rectification documents, transport documents, electronic invoice requirements and sanctions.

For NOVA-ERP, the durable value is not the paper-era UI examples. The durable value is the domain shape:

- invoice issuance is tied to goods/services, advance payments and changes in taxable value;
- invoice and rectification documents require sequence, date, series and identity fields;
- numbering must be chronological and non-deletable;
- voided/unused numbers remain in sequence;
- rectification must reference the original invoice and the altered fields;
- special regimes change required wording, tax deductibility and treasury/accounting behavior;
- electronic records must preserve integrity, availability, authenticity, non-repudiation and audit access.

## Key Claims

### Invoice Issuance And Timing

The manual presents invoice issuance as required for each transfer of goods, service provision and advance payment under IVA, with additional invoice obligation when taxable value or tax changes.

It states that, as a general rule, invoices or equivalent documents must be issued by the fifth working day after the taxable event. Advance payments require invoice/equivalent issuance at receipt; global invoices and consignments have specific timing rules.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 5-6.

### Required Invoice Fields

The manual lists invoice elements including supplier/customer identity and NIF, quantity and usual description of goods/services, taxable price and taxable-value components, tax rate and amount, justification for non-application of tax where applicable, and the issuing series.

Rectification documents must include date, sequential number, party identification, reference to the original invoice, and the invoice mentions being altered.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 7 and 35.

### Sequential Numbering And Immutability

For invoices processed by software or authorized printers, numbering should start at 01 for each fiscal period and remain sequential and chronological, without interruption or repetition. If an invoice is inutilized, it remains annulled in the chronological sequence and cannot be deleted.

Implementation implication: NOVA-ERP should not implement invoice deletion after number assignment. It needs explicit void/inutilization and correction flows.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 11-12 and 17.

### Software-Processed Invoices

The manual says taxpayers using computer-generated invoice output should use programs that guarantee sequential/chronological numbering and no deletion of numbers. It also describes prior communication of the software to the tax administration, original/copy markings, software identification text, contingency use of authorized typographic invoices during system outage, and archival of analysis/programming/execution records for the legally established period.

Implementation implication: NOVA-ERP needs software/version traceability, audit-grade numbering controls, outage/contingency behavior and retention of fiscal processing evidence.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 11-12.

### Retail Tickets And Dispensa De Faturacao

The manual describes limited cases where invoice issuance is dispensed for particular cash retail/service operations with private consumers, but the taxpayer must document operations through numbered sale/service tickets. Tickets require supplier identity/NIF, usual goods/service description and price with tax included.

Implementation implication: NOVA-ERP should model sale tickets separately from full invoices where e-Fatura/DFE type scope requires it, rather than treating them as generic receipts.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 8, 17-18 and 24-26.

### REMPE

For micro and small companies under REMPE, the manual says sale tickets are required even where invoice issuance is dispensed; invoices/receipts must be issued when requested by the acquirer. REMPE documents should mention "Tributo Especial Unificado" and do not confer IVA deduction rights to the acquirer.

Implementation implication: tax regime is not a cosmetic label. It affects required wording, deductibility, document type behavior and purchaser-side accounting.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 28-29.

### Faturacao Ao Estado

For public works contracts where the State is the owner of the works, the manual includes a special IVA exigibility regime. It states that invoices in this regime should use a special series and mention "IVA exigivel e dedutivel no pagamento"; receipts are tied to total or partial payments and must reference the invoice.

Implementation implication: NOVA-ERP needs special fiscal document rules for public-sector construction/public works before claiming full Cabo Verde fiscal coverage.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 30-32.

### Reverse Charge

For reverse-charge situations, including construction services described by the manual, invoices should contain the expression "IVA - autoliquidacao".

Implementation implication: tax profile/rule selection must be able to require legal wording and change tax-debtor semantics.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, page 34.

### Transport Documents

The manual includes goods-in-circulation rules for transport documents. The document should identify origin, destination/acquirer, sender, transport means and owner/operator, and departure time. It also describes transport document copies, archival periods and enforcement risk.

Implementation implication: inventory/logistics flows need transport-document support, not just stock movements and invoices.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 36-46.

### Electronic Invoice Requirements

The manual's older electronic invoice chapter says electronic invoices are legally equivalent to paper originals when digitally signed, and that taxpayers seeking electronic invoice systems must request authorization. It also requires readable access, chronological conservation, anomaly/correction lists and technical controls around integrity, availability, authenticity, non-repudiation and non-duplication.

Current e-Fatura public guidance is newer and frames the electronic invoice/document as a purely digital, authorized-in-real-time document with legal validity from digital signature and tax-authority authorization. Treat the 2006/2007 chapter as historical/legal background, and the v11.0 technical manual plus current e-Fatura portal as the stronger implementation authority for modern DFE behavior.

Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`, pages 47-52; https://efatura.cv/docs/about/e-fatura/; https://efatura.cv/docs/manual/.

## Implementation Implications For NOVA-ERP

- `fiscal_series` must enforce tenant, document type, fiscal period, series, chronological sequence, no reuse and no silent gaps.
- `fiscal_documents` need immutable issued snapshots after number assignment.
- Voided or inutilized numbers should remain auditable and linked to the replacement document where applicable.
- Corrective documents must reference the original fiscal document and the changed mentions.
- Tax regime and customer/public-sector context must influence document requirements, not just tax rates.
- REMPE, reverse charge and State/public works flows need explicit rule flags before MVP claims broad compliance.
- Sale tickets, receipts, credit notes, debit notes, return notes and transport documents should be modeled as related but distinct fiscal document types.
- Software version, emitter identity, document language, storage, audit access and anomaly tracking should be first-class evidence.
- Electronic document storage must preserve integrity, availability, authenticity, non-repudiation, chronological access and readable export.

## Product Decisions Suggested

For the foundation release, support the commercial subset with strong architecture:

- invoices;
- invoice-receipts;
- credit notes;
- debit notes;
- receipts;
- sale tickets if the MVP targets retail;
- transport documents if inventory/logistics shipment is in scope.

Do not claim complete support yet for REMPE, public works State invoicing, reverse charge or all transport enforcement rules until current law and e-Fatura schemas are verified.

## Tensions And Cautions

- The manual is dated May 2018 and explicitly non-normative.
- Its electronic invoice chapter predates the current e-Fatura technical architecture and should not override the v11.0 DFE manual.
- Some named authorities and old terminology such as DGCI may have been superseded by current DNRE/e-Fatura structures.
- Penalty amounts and legal references may have changed.
- The manual does not resolve current e-Fatura XML/event schema details for cancellation/anulation and number invalidation.

## Open Questions

- Which provisions of the 2018 manual remain current after Decreto-Lei n.º 79/2020 and current e-Fatura rollout?
- Which fiscal document types must be in the first sellable release: FTE/FRE/NCE/NDE/RCE only, or also TVE/DTE/DVE/NLE?
- What are the current authorized software, certification and e-Fatura onboarding requirements for SaaS/multi-tenant providers?
- How should NOVA-ERP represent voided/inutilized invoice numbers under the current e-Fatura event model?
- Which public-sector/State invoicing rules still apply unchanged?
