---
type: question
status: active
created: 2026-05-28
updated: 2026-05-28
tags: [question, fiscalidade, faturacao, efatura, cabo-verde]
sources: ["[[2026-05-28 - Manual de Faturas em Cabo Verde]]", "[[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]", "https://efatura.cv/docs/manual/", "https://efatura.cv/docs/about/e-fatura/", "https://efatura.cv/docs/faqs/conceitos/", "https://efatura.cv/assets/files/Despacho_Requisitos_Processamento-aa4a4bba5dc084bf078533632bfdbea5.pdf", "https://efatura.cv/assets/files/Portaria_FE-20df5972f7b92958738c47c3787cd714.pdf"]
related: ["[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[DNRE]]"]
confidence: mixed
---

# Vigencia do Manual de Faturas 2018 apos e-Fatura

## Question

Which rules from `docs/docsfiscal/MANUAL DE FATURAS.pdf` still govern NOVA-ERP after Cabo Verde's modern e-Fatura regime?

## Short Answer

The 2018 manual should now be treated as an orientative invoice-rule map, not as the current implementation authority.

Rules that describe the fiscal substance of invoices mostly survive: invoice issuance duty, required business content, tax treatment, correction/rectification, REMPE treatment, reverse-charge wording, transport-document concepts, and archive/audit duties.

Rules that describe the old processing mechanism are superseded or narrowed by the modern e-Fatura regime: paper/PDF equivalence, paper-first storage, old authorization model for electronic invoicing, typographic fallback as the default contingency path, and software-process details that conflict with DFE XML/XSD, digital signature, IUD and DNRE authorization.

## Current Authority Found On 2026-05-28

- The official e-Fatura manual page lists `Manual Técnico da Fatura Eletrónica v11.0` as the latest version, superseding the vault's earlier v10.0 currency check from 2026-05-27.
  Source: https://efatura.cv/docs/manual/

- The modern e-Fatura concept says the electronic invoice, including invoice-receipt, is a purely digital document, emitted, archived and conserved electronically, with legal validity guaranteed by the issuer's digital signature and real-time authorization by the tax administration.
  Source: https://efatura.cv/docs/about/e-fatura/

- Official FAQs say electronic fiscal documents include sale ticket/service ticket, debit note, credit note, receipt and transport document; they also say all obligated taxpayers must be previously credentialed by the tax administration.
  Source: https://efatura.cv/docs/faqs/conceitos/

- The processing-requirements despacho says electronic invoices and relevant fiscal documents must be XML with Cabo Verde-specific structure, submitted electronically for prior authorization, digitally signed under ICP-CV, assigned an IUD, and governed structurally by the technical manual available at `efatura.cv`.
  Source: https://efatura.cv/assets/files/Despacho_Requisitos_Processamento-aa4a4bba5dc084bf078533632bfdbea5.pdf

- The e-Fatura portaria regulates credentialing, contingency and recipient manifestation. It requires DNRE credentialing before issuing, allows offline/off contingency modes, requires later submission to DNRE for authorization within five working days, and makes recipient manifestation mandatory in some rectification cases reducing taxable value.
  Source: https://efatura.cv/assets/files/Portaria_FE-20df5972f7b92958738c47c3787cd714.pdf

## Survives As Product Rule

### Invoice Trigger And Timing

The 2018 rule that fiscal documents are triggered by goods/services, advance payments and taxable-value/tax changes remains a valid design assumption because the e-Fatura FAQ still says processing requirements include the CIVA and REMPE. NOVA-ERP should continue to model issue deadlines, but the exact timing should be checked against current CIVA and e-Fatura regulations before production certification.

Status: survives with legal verification.

### Required Business Content

Supplier, recipient, NIF, goods/services, totals, taxes, non-taxation reason and series remain conceptually valid. Modern e-Fatura translates these into XML field groups: document identification, emitter, receiver, transport, payment, items, totals and software.

Status: survives, but implementation authority moves to DFE XML/XSD and the latest technical manual.

### Sequential Numbering And No Deletion

The 2018 rule that fiscal numbers are sequential, chronological, non-repeating and not physically deleted survives. Modern e-Fatura strengthens this through IUD, LED, document type, document number uniqueness, XML validation and number-invalidation events in the technical manual history.

Status: survives as a core invariant.

### Rectification Documents

The 2018 rule that rectification documents reference the original invoice survives, and the modern portaria adds recipient manifestation rules for rectifying documents that reduce taxable value.

Status: survives, with stronger e-Fatura event/manifestation requirements.

### REMPE

REMPE remains relevant because the e-Fatura FAQ says processing requirements include CIVA and REMPE. NOVA-ERP should preserve REMPE as a tax-regime dimension affecting wording, deductibility and document behavior.

Status: survives, pending current REMPE detail verification.

### Sale Tickets, Receipts And Transport Documents

The 2018 sale-ticket and transport-document concepts survive as electronic document types. Modern e-Fatura explicitly includes electronic sale/service tickets, receipts and transport documents as relevant electronic fiscal documents.

Status: survives, but mapped to DFE types and XML structures.

### Reverse Charge And Special Tax Wording

The 2018 reverse-charge rule is still plausible because e-Fatura processing remains tied to CIVA. NOVA-ERP should keep a tax-rule mechanism that can require legal wording such as "IVA - autoliquidacao", but this exact wording and scope should be verified against current CIVA/regulations.

Status: likely survives, requires legal verification.

### Archive, Integrity And Audit

The 2018 archival principles survive but are modernized. The current regime requires digital existence, electronic archive/conservation, digital signature, authorization and access through the electronic platform. NOVA-ERP should preserve immutable XML, signatures, IUD, authorization response, event history and readable/exportable audit views.

Status: survives, with modern digital mechanism.

## Superseded Or Narrowed

### PDF, Email, Scan Or Paper Image As Electronic Invoice

The 2018 electronic-invoice chapter predates the modern DFE model. Current guidance says PDFs, Word files, images, HTML/email invoices, OCR scans and faxed images are not electronic invoices/fiscally relevant electronic documents.

Status: superseded for modern e-Fatura.

### Old Electronic-Invoice Authorization Workflow

The 2018 chapter's older request/authorization model should not drive NOVA-ERP implementation. Current authority points to DNRE credentialing, XML/XSD, ICP-CV digital signature, IUD and prior/real-time authorization through the Plataforma Eletrónica.

Status: superseded by Decreto-Lei n.º 79/2020 ecosystem and implementing guidance.

### Typographic Fallback As Primary Contingency

The 2018 manual's paper/authorized-printer fallback is not the default modern path. Current e-Fatura contingency distinguishes offline mode through own system/middleware when communication fails and off mode through non-electronic auxiliary provisional documents when power/equipment failure prevents electronic access.

Status: narrowed to exceptional off-mode contingency if current rules allow.

### Visual Invoice Layout Examples

The 2018 paper examples are not implementation authority for NOVA-ERP UI or print layout. Current e-Fatura emphasizes structured XML, IUD, QR code, digital authorization and document auxiliary representation.

Status: historical reference only.

### v10.0 As Latest Manual

The v10.0 manual remains useful already-ingested evidence, but the current official manual page lists v11.0 as the latest. NOVA-ERP implementation must verify against v11.0 before schema/API work.

Status: superseded for current technical authority.

## Unresolved

- Whether public works/State invoicing rules from the 2018 manual remain unchanged under the modern e-Fatura regime.
- Exact current wording/scope for reverse charge.
- Exact current penalties and sanction amounts.
- Whether all paper-era typographic rules remain relevant outside e-Fatura obligation scope.
- Schema-level handling of cancellation/anulation, number invalidation and rectification manifestation under v11.0.

## NOVA-ERP Decision

For now, implement the fiscal-document domain with these invariants:

- no physical deletion after fiscal number/IUD assignment;
- immutable issued snapshot and XML payload;
- explicit correction, cancellation/anulation and number-invalidation events;
- tax-regime rule engine for CIVA, REMPE, reverse charge and non-taxation reasons;
- DFE type layer for invoice, invoice-receipt, sale ticket, receipt, credit note, debit note, transport document, return note and registration note;
- e-Fatura credentialing/readiness before production issue;
- contingency modeled as official online/offline/off issue mode plus internal retry/audit workflow;
- recipient manifestation support where legally required, especially rectifications reducing taxable value.

Do not claim production fiscal compliance until the latest v11.0 technical manual, current CIVA/REMPE texts, Portaria FE and despacho requirements are ingested at schema level.
