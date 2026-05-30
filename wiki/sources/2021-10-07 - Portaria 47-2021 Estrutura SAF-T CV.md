---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, saft, cabo-verde, primary-law, boletim-oficial, sncrf, fiscalidade]
sources: []
related: ["[[SAF-T CV]]", "[[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]]", "[[SAF-T CV Code Lists]]", "[[2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema]]", "[[Contabilidade ERP]]", "[[DNRE]]"]
confidence: high
---

# Portaria nº 47/2021, de 7 de outubro — Estrutura de Dados do SAF-T (CV) (Primary Law)

## What this is

**Primary law.** Boletim Oficial da República de Cabo Verde, **I Série nº 97, 7 de outubro de 2021** (Ministério das Finanças; signed 27 Sept 2021). Defines the **data structure (Anexo I)** and **taxonomies (Anexo II)** of the data-export file required by **art. 107.º nº 6 do Código do IRPC**. This is the legal authority behind the SAF-T (CV) XSD; preserved at `raw/assets/saft-cv/Portaria_47_2021_SAF_T_CV.pdf` (68 pp.). It confirms and supersedes the secondary-web claims in [[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]].

## Legal articles (confirmed against Boletim Oficial)

- **Art. 2.º — Âmbito subjetivo:** the export file is submitted by the passive subjects of **art. 107.º nº1 CIRPC** and by **Category B taxpayers under the organized-accounting regime** (art. 78.º nº1 CIRPS). **Exempt: Category B taxpayers with annual turnover ≤ 5.000.000$00 CVE** (≤ 5 million escudos). (Resolves the "> 5,000,000$" threshold — it is an *exemption ceiling*, not an obligation floor.)
- **Art. 3.º — Delimitação especial:** **REMPE** (micro/small enterprise) taxpayers may **voluntarily** adhere to organized accounting and thereby become subject to art. 107.º nº6 and this portaria.
- **Art. 4.º — Taxonomias:** account-classification codes are filled **by reference to the taxonomies in Anexo II**, per the chart referential used — **SNCRF Base** or **Normas Internacionais de Contabilidade**. (This is the SNCRF taxonomy code list; resolves the accounting-taxonomy contradiction.)
- **Art. 5.º — Entrada em vigor: 1 de janeiro de 2022**, applying to accounting records for **exercises 2022 and following**.

## File structure (Anexo I) — confirms the XSD

`AuditFile` tables, by index, match the v1.01_01 XSD: `1` Header, `2.2` Customer, `2.3` Supplier, `2.4` Product, `2.5` TaxTable, `3` GeneralLedgerEntries, `4.1` WorkingDocuments, `4.2` Payments, `4.3` PhysicalStock. **File type `O` (Outros)** omits GeneralLedgerEntries and PhysicalStock. Dates `AAAA-MM-DD`; timestamps `AAAA-MM-DDThh:mm:ss`. The Portaria Anexo I and the efatura.cv XSD describe the **same structure** — they are consistent, not competing.

## Code lists confirmed from Anexo I (primary)

- **ProductType (2.4.1):** `P` Produtos · `S` Serviços · `O` Outros · `E` Impostos Especiais de Consumo · `I` Impostos, taxas e encargos parafiscais (exceto IVA, IS e TEU).
- **TaxType (2.5.1.1):** `IVA` · `IS` Imposto do Selo · `NS` não sujeição a IVA/IS/TEU · **`TEU` Tributo Especial Unificado**.
- **TaxCode for IVA (2.5.1.3):** `NOR` taxa normal · `RED` taxa reduzida · `ISE` isento · `ESP` regimes especiais de IVA · `NS` …
- **PSProductType / Tipologia de inventário (4.3.1.2.1.5):** `M` Mercadorias · **`AB` Ativos biológicos** · `MP` Matérias-primas, subsidiárias e de consumo · `PCI` Produtos acabados e intermédios · `SP` Subprodutos, desperdícios e refugos · `PC` Produtos e trabalhos em curso.
- **ProductStatus (4.3.1.2.1.6):** `A` Ativo · `D` Danificado · `DS` Descontinuado · `O` Obsoleto · `Q` Quarentena.
- `TaxonomyCode (2.1.2.9)`: account taxonomy code from Anexo II; banking/insurance entities (no specific taxonomy) use single code **«1»**.

All of these were flagged "convention — confirm" in [[SAF-T CV Code Lists]] and are now **authoritative**.

## Implementation impact for NOVA-ERP

- The SAF-T (CV) obligation applies to **organized-accounting** IRPC subjects and Category-B-organized subjects > 5,000,000$ turnover, for **exercises from 2022** — NOVA-ERP's target tenants are squarely in scope.
- `chart_of_accounts` must carry **Anexo II SNCRF taxonomy codes** (`taxonomy_code`) and the tenant a `taxonomy_reference` (SNCRF Base / NIC / NRF-PE / Outros→«1»). This is the next concrete artifact to ingest: **Anexo II** itself (the account-code → taxonomy table; partially visible, e.g. `341/342` subprodutos, `35` produtos e trabalhos em curso, `3611–3622` matérias-primas).
- The convention rows in [[SAF-T CV Code Lists]] should be upgraded to authoritative and the [[Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy]] marked resolved.

## Open questions

- ~~**Anexo II** full taxonomy account list~~ — **extracted** (660 codes) to `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv`; see [[SAF-T CV Anexo II - SNCRF Account Taxonomy]].
- Exact **inventory submission deadline** (secondary sources say 31 January following year) — confirm the precise article/number in the Portaria, not captured verbatim here.
- Whether a SAF-T (CV) XSD version newer than v1.01_01 was published to align field indices with this 2021 Anexo I (structure matches; version label unconfirmed).

## Verification

Primary text from the official Boletim Oficial PDF hosted by DNRE/efatura.cv and parsed directly. Safe as production legal authority for the structure, code lists, obligation scope and entry-into-force; reconfirm the inventory deadline article.

Sources:
- [Portaria nº 47/2021 — SAF-T (CV) (efatura.cv / Boletim Oficial)](https://efatura.cv/assets/files/Portaria_n_47_2021_SAF_T_CV-f4cd9d8072a3875ab16872008bf5aa8f.pdf)
