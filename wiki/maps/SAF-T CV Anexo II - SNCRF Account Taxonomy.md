---
type: map
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [saft, cabo-verde, sncrf, taxonomy, chart-of-accounts, seed-data, reference]
sources: ["[[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]"]
related: ["[[SAF-T CV]]", "[[SAF-T CV Code Lists]]", "[[2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]"]
confidence: high
---

# SAF-T (CV) Anexo II — SNCRF Account Taxonomy (Seed Reference)

The **account-classification taxonomy** referenced by `GeneralLedgerAccounts.TaxonomyCode` (and the file-level `TaxonomyReference`) in the SAF-T (CV) file, per **Art. 4.º of [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]**. Extracted directly from the portaria's Anexo II (pp. 35–67) and saved as structured data:

- **Data file:** `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv` — columns `taxonomy_code, sncrf_account_codes, description`.
- **660 taxonomy codes** (sequential `1`–`660`, no gaps), each mapping a taxonomy line to one or more **SNCRF account codes** and the official account description. Some taxonomy codes group several accounts (e.g. `213 | 214 | 215 | 217`).

This is the seed for `chart_of_accounts.taxonomy_code` in [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]; the file is too large to inline — query the CSV.

## Referential (TaxonomyReference)

Per the XSD/portaria, the file declares which referential the chart uses (see [[SAF-T CV Code Lists]]): `S` SNCRF Base · `N` NIC/NIRF · `P` NRF-PE · `O` Outros (banking/insurance → use taxonomy code «1»). **Anexo II provides the SNCRF Base / NIC code list**; NRF-PE pequenas entidades reuse "Taxonomia S".

## Class distribution (SNCRF, first digit of account code)

| Classe | Name | Taxonomy codes |
|--------|------|----------------|
| 1 | Meios financeiros líquidos | 10 |
| 2 | Contas a receber e a pagar | 230 |
| 3 | Inventários e ativos biológicos | 25 |
| 4 | Investimentos | 95 |
| 5 | Capital, reservas e resultados transitados | 24 |
| 6 | Gastos | 148 |
| 7 | Rendimentos | 128 |
| **Total** | | **660** |

(Classe 8 — Resultados — has no Anexo II taxonomy entries.)

## Sample rows

| taxonomy_code | account(s) | description |
|---------------|-----------|-------------|
| 1 | 11 | Caixa |
| 2 | 12 | Depósitos à ordem |
| 3 | 13 | Depósitos a prazo |
| … | … | … |
| 256 | 341 | Subprodutos, desperdícios, resíduos e refugos – Subprodutos |
| 658 | 7928 | Ganhos de financiamento – Diferenças de câmbio favoráveis |
| 660 | 7988 | Outros ganhos de financiamento – Outros |

## Implementation note

- NOVA-ERP's default Cabo Verde chart should be **seeded from the SNCRF code set** and each account carries its `taxonomy_code` (1–660). On SAF-T export, `GeneralLedgerAccounts.TaxonomyCode` emits that value and `TaxonomyReference` emits the tenant's referential (`S`/`N`/`P`/`O`).
- The grouped rows (multiple accounts per taxonomy code) mean the mapping is **account → taxonomy_code is many-to-one**; store `taxonomy_code` on the account, not the reverse.
- Re-run the extractor (`pypdf` over the preserved portaria) if a corrected/typo-free pass is needed; descriptions were de-wrapped heuristically and a few long ones may be truncated — the **account code + class are reliable**, verify exact wording against the PDF for any account before legal display.
