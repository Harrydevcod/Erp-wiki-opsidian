---
type: contradiction
status: superseded
created: 2026-05-30
updated: 2026-05-30
tags: [contradiction, saft, cabo-verde, resolved]
sources: ["[[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]]", "[[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]"]
related: ["[[SAF-T CV]]", "[[Contabilidade ERP]]", "[[DNRE]]"]
confidence: medium
---

# Contradiction — SAF-T (CV) Schema Version vs Portaria 47/2021 Taxonomy

## Disputed point

What is the **current** authoritative SAF-T (CV) schema for the **Contabilidade** (accounting) file?

## Position A — v1.01_01 is the current schema

The DNRE e-Fatura platform publishes **SAF-T (CV) XSD v1.01_01** (`ModificationDate 2020-05-29`) as the listed schema, and its `FileContentType` already includes `C` (Contabilidade). Designing against this XSD is safe.

Evidence: parsed XSD at `raw/assets/saft-cv/saftcv1.01_01.xsd`; listing at https://efatura.cv/docs/xsd/. Source: [[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]].

## Position B — Portaria 47/2021 introduced a newer accounting taxonomy

**Portaria nº 47/2021, de 7 de outubro** established a SAF-T (CV) accounting-reporting model **aligned with the SNCRF**, and vendor documentation (Primavera "Ficheiro SAF-T (CV) da Contabilidade e **Taxonomias**") refers to SNCRF **taxonomy codes** for the accounting file. A 2020 schema may predate or have been superseded/extended for the accounting content type.

Evidence (secondary, web): INOVE nota técnica; Primavera ROA page; asemana.cv columns. Not yet confirmed against Boletim Oficial.

## Resolution (2026-05-30) — primary law obtained

**Resolved.** The full text of [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]] (Boletim Oficial I Série nº 97, 7 out 2021) was obtained and parsed:

- **Anexo I** (the portaria's data structure) describes the **same `AuditFile` shape** as the efatura.cv XSD v1.01_01 — Header / MasterFiles (Customer/Supplier/Product/TaxTable/GeneralLedgerAccounts) / GeneralLedgerEntries / WorkingDocuments / Payments / PhysicalStock, with matching field names. They are **consistent, not competing**: the XSD is the machine schema, the portaria is its legal source.
- **Art. 4.º (Taxonomias)** settles the open part: account-classification codes are filled by reference to the **taxonomies in Anexo II** of the portaria, per the chart referential (**SNCRF Base** or **Normas Internacionais**). So the "newer SNCRF taxonomy" is **Anexo II of Portaria 47/2021**, not a competing schema — it is an external account-code list the schema's `TaxonomyCode`/`TaxonomyReference` fields point to.
- **Art. 5.º:** in force **1 Jan 2022** for exercises 2022+.

**Outcome:** Position A (v1.01_01 structure is current/safe) and Position B (SNCRF taxonomy under Portaria 47/2021) are **both true and complementary** — there was no real conflict, only a missing piece (Anexo II). Design against v1.01_01 structure + seed account taxonomy codes from Anexo II.

## Residual (minor)

- ~~Extract the **Anexo II** account-code taxonomy list~~ — **done** (660 codes): [[SAF-T CV Anexo II - SNCRF Account Taxonomy]] / `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv`.
- Confirm whether an XSD *version label* newer than v1.01_01 was published to re-align field indices with the 2021 Anexo I (structure already matches; cosmetic).
