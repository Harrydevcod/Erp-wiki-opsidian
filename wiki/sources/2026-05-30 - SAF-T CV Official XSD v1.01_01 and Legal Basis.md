---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, saft, cabo-verde, dnre, xsd, fiscalidade, primary-law, web-research]
sources: []
related: ["[[SAF-T CV]]", "[[DNRE]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[Contabilidade ERP]]", "[[Inventario ERP]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]"]
confidence: high
---

# SAF-T (CV) — Official XSD v1.01_01 and Legal Basis

## What this is

The **official Cabo Verde SAF-T schema**, obtained from the DNRE e-Fatura platform on 2026-05-30 and parsed directly. This closes the long-standing "official SAF-T CV schema/XSD not ingested" gate in [[SAF-T CV]]. The schema file is preserved at `raw/assets/saft-cv/saftcv1.01_01.xsd`.

- **Schema identity (from the XSD itself):** namespace `urn:OECD:StandardAuditFile-Tax:CV_1.01_01`, `version="1.01_01"`, `id="SAF-T_CV"`, author **Direção Nacional das Receitas de Estado (DNRE)**, `ModificationDate 2020-05-29`. Title: "Standard Audit File - Cape Verde version". It is an **OECD SAF-T 2.0-derived** schema.
- **Source URLs:**
  - XSD listing: https://efatura.cv/docs/xsd/ — lists "SAF-T CV XSD v1.01_01" and the e-Fatura DFE package "2024-05-27-XML-XSD".
  - DNRE FAQ base (image-slide PDF, not text-extractable): https://www.mf.gov.cv/documents/54571/4624142/SAFT_CV__FAQs_BASE_DNRE.pdf
  - Legal index: https://efatura.cv/docs/legislacao (Decretos-Lei, Despachos, Portarias).

## Authoritative schema structure (parsed from v1.01_01)

`AuditFile` root has four blocks:

1. **Header** (fixed sequence): `AuditFileVersion`, `CompanyID`, `TaxRegistrationNumber`, **`FileContentType`**, `CompanyName`, `BusinessName?`, `CompanyAddress`, `FiscalYear`, `StartDate`, `EndDate`, `CurrencyCode`, `DateCreated`, `TaxEntity`, `ProductCompanyTaxID`, **`SoftwareCertificateNumber`**, `ProductID`, `ProductVersion`, `HeaderComment?`, `Telephone?`, `Fax?`, `Email?`, `Website?`, **`NumberOfParts`**, **`PartNumber`**.
2. **MasterFiles**: `GeneralLedgerAccounts?`, `Customer*`, `Supplier*`, `Product*`, `TaxTable`.
3. **GeneralLedgerEntries?** — accounting journal (debit/credit lines).
4. **SourceDocuments?**: `WorkingDocuments?`, `Payments?`, `PhysicalStock?`.

Key structural facts:
- **`FileContentType` selects the SAF-T type within one schema** — it is an enumeration with exactly **four values: `F` (Faturação), `C` (Contabilidade), `I` (Inventário), `O` (Outros)** (read from the XSD `simpleType`). There are **not** separate XSDs per type; one `AuditFile` carries `FileContentType` + the relevant blocks. **Note:** the product docs' "SAF-T **Completo**" is **not** an official `FileContentType` value — the official set is F/C/I/O. (Resolves the concept-page ambiguity; see contradiction note below.)
- **Software certification is in the Header**: `SoftwareCertificateNumber`, `ProductCompanyTaxID`, `ProductID`, `ProductVersion` — NOVA-ERP must carry a DNRE software-certificate number and emit it.
- **`NumberOfParts` / `PartNumber`** support splitting large files into parts — confirms the async/chunked export design in [[SAF-T CV]].
- **MasterFiles maps cleanly to NOVA-ERP**: `GeneralLedgerAccounts` ← chart of accounts ([[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]); `Customer`/`Supplier` ← the unified `entities` ([[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]); `Product` ← `items` ([[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]); `TaxTable` ← `tax_rates`/`tax_maps`.
- **SourceDocuments** in this version exposes `WorkingDocuments` (commercial documents), `Payments` (treasury) and `PhysicalStock` (inventory counts). `GeneralLedgerEntries` carries posted accounting movements.

## Legal basis (from web research — verify against Boletim Oficial)

- **SAF-T (CV) for accounting/inventory: Portaria nº 47/2021, de 7 de outubro** — establishes the SAF-T (CV) accounting-reporting model aligned with the **SNCRF** (Sistema de Normalização Contabilística e de Relato Financeiro). Inventory data must be reported for the annual taxation period and **submitted by 31 January** of the following year (art. 2 lists the obligated taxpayers).
- **Obligated:** entities using computer applications for accounting/billing must deliver the XML file to the Tax Administration whenever requested; **non-resident entities with permanent establishment** in CV; **Category B self-employed with income > 5,000,000$** under the organized-accounting regime.
- **e-Fatura (one facet of SAF-T):** mandatory since 2020 under **Decreto-Lei nº 79/2020**, regulated by **Portarias nº 62/2020, 74/2020, 16/2022** and **Despacho nº 43/2022**. (Already tracked under [[e-Fatura Cabo Verde]] and the DFE technical manual.)

## Open questions / reconciliation needed

- **Version provenance:** the efatura.cv XSD is `v1.01_01`, `ModificationDate 2020-05-29` — i.e. the **e-Fatura-era** schema. **Portaria 47/2021** (SNCRF accounting SAF-T) is later; the Primavera "Ficheiro SAF-T (CV) da Contabilidade e Taxonomias" reference implies the accounting SAF-T uses **SNCRF taxonomy codes**. Confirm whether v1.01_01 is still the current schema for all content types, or whether a newer accounting taxonomy/version was published under Portaria 47/2021. (Tracked as a contradiction.)
- The full field-level definitions of `Customer`, `Supplier`, `Product`, `Invoice`/`WorkDocument`, `GeneralLedgerEntries` and `PhysicalStock` (element-by-element) — available in the saved XSD for a deeper field-mapping pass when implementation needs it.
- The DNRE FAQ PDF is image-based; its Q&A content (deadlines, penalties, submission channel) needs an OCR pass or the HTML FAQ at https://efatura.cv/docs/faqs.

## Verification needs

- **Confirmed (2026-05-30):** the legal basis is now verified against the **Boletim Oficial** — see [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]] (Portaria nº 47/2021, de 7 de outubro; I Série nº 97; in force 1 Jan 2022; Category-B exempt ≤ 5.000.000$). The portaria's Anexo I matches this XSD structure and Anexo II carries the SNCRF account taxonomies. The previously open taxonomy question is **resolved**.
- Remaining: extract Anexo II's account-taxonomy list to seed `chart_of_accounts.taxonomy_code`; confirm the exact inventory-submission-deadline article.

Sources:
- [efatura.cv XML-XSD listing](https://efatura.cv/docs/xsd/)
- [DNRE SAF-T (CV) FAQ base](https://www.mf.gov.cv/documents/54571/4624142/SAFT_CV__FAQs_BASE_DNRE.pdf)
- [INFORPRESS — Cabo Verde adopta ficheiro SAF-T](https://www.inforpress.cv/cabo-verde-adopta-ficheiro-saf-t-para-tornar-a-administracao-fiscal-mais-eficiente/)
- [INOVE — Nota Técnica SAFT-CV](https://inove.cv/nota-tecnica-faturacao-eletronica-e-standard-audit-file-for-tax-purposes-cabo-verde-saft-cv-tudo-o-que-deve-saber/)
- [Primavera ROA — Ficheiro SAF-T (CV) da Contabilidade e Taxonomias](https://roa.primaverabss.com/pt/pagina/ficheiro-saft/)
