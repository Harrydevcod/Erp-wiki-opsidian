---
type: synthesis
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [synthesis, saft, cabo-verde, schema-mapping, fiscalidade, nova-erp]
sources: ["[[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]]"]
related: ["[[SAF-T CV]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy]]"]
confidence: high
---

# SAF-T (CV) Field Map to NOVA-ERP Schema

Maps the official **SAF-T (CV) v1.01_01** elements (parsed from `raw/assets/saft-cv/saftcv1.01_01.xsd`) to NOVA-ERP target tables, so SAF-T becomes a consequence of consistent source data rather than a late repair job. Field facts are **primary** (from the XSD); the accounting taxonomy currency is open per [[Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy]].

## MasterFiles → NOVA-ERP

### `Customer` / `Supplier` → unified `entities` ([[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]])
- `CustomerID`/`SupplierID` ← `entities.id` (tenant-stable code); `CustomerTaxID`/`SupplierTaxID` ← `entities.tax_id`; `CompanyName` ← `entities.legal_name` (fiscal name, not commercial); `Contact`, `Telephone`, `Fax`, `Email`, `Website` ← entity contact fields.
- **`AccountID`** (`SAFTCVAccountID`) — the customer/supplier **control account** in the chart; NOVA-ERP must link each entity to its GL control account (third-party account). New capture requirement on `entities` or category default.
- `BillingAddress` + `ShipToAddress`/`ShipFromAddress` (repeatable) ← `entities.address` jsonb must carry the full `AddressStructure` (BuildingNumber, StreetName, AddressDetail, City, PostalCode, Region, **Country** ISO). Confirms address must be structured, not free text.

### `Product` → `items` ([[2026-05-28 - Schema Decision - Inventory Movements and Valuation]])
- `ProductCode` ← `items.sku`; `ProductDescription` ← name; `ProductType` (`SAFTCVProductType`) ← `items.kind` (mapped to the SAF-T product-type code list); `ProductGroup` ← family/category; `UOMBase` ← `items.unit_id` (UoM **code**); `Tax` (TaxType+TaxCode, repeatable) ← `items.tax_rate_id`.
- **`ProductNumberCode`** (mandatory) and **`CVProductCode`** (optional) and `CustomsDetails/UNNumber` — capture an item's barcode/standard code and a CV product code; new optional fields on `items`.

### `TaxTable` / `TaxTableEntry` → `tax_rates` + accounting `tax_maps` ([[2026-05-28 - Schema Decision - Accounting Ledger and Posting]])
- `TaxType` + `TaxCode` + `TaxCountryRegion` + `Description` + `TaxExpirationDate` ← versioned `tax_rates`. The `(TaxType, TaxCode)` pair is the **canonical fiscal identity** of a rate; NOVA-ERP `tax_rates` must store both and the SAF-T code so document lines emit them.

### `GeneralLedgerAccounts` → `chart_of_accounts` ([[2026-05-28 - Schema Decision - Accounting Ledger and Posting]])
- **`TaxonomyReference`** (file-level) + per-account **`TaxonomyCode`** — the **SNCRF taxonomy** binding. `chart_of_accounts` needs a `taxonomy_code` column and the tenant chart a `taxonomy_reference`. The 660-code taxonomy is extracted and ready to seed: [[SAF-T CV Anexo II - SNCRF Account Taxonomy]] (`raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv`).
- `Account`: `AccountID` ← account code; `AccountDescription`; `OpeningDebitBalance`/`OpeningCreditBalance`/`ClosingDebitBalance`/`ClosingCreditBalance` ← **derived from the journal projection** (validates the ADR's projection-based balances — these are computed, not stored); `GroupingCategory`/`GroupingCode` ← the razão/integradora/movement hierarchy from the Cegid accounting deck.

## GeneralLedgerEntries → accounting journal ([[2026-05-28 - Schema Decision - Accounting Ledger and Posting]])
- `Journal` (JournalID, Description) ← `journals`; `Transaction` ← `journal_entries` with `TransactionID`, `Period` (`SAFTCVAccountingPeriod`), `TransactionDate`, `GLPostingDate`, `SourceID`, **`DocArchivalNumber`**, `TransactionType`; `Lines/DebitLine`+`CreditLine` ← `journal_entry_lines`.
- **Capture-now:** `Period`, `GLPostingDate` distinct from `TransactionDate`, `DocArchivalNumber`, `TransactionType` — the journal entry must store all four to be SAF-T-exportable.

## SourceDocuments

### `WorkingDocuments`/`WorkDocument` → fiscal/commercial documents ([[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]])
- `DocumentNumber` ← fiscal `number`; `DocumentStatus` (`WorkStatus`, `WorkStatusDate`, `Reason`, `SourceID`, **`SourceBilling`**) ← document status + how it was produced; `Period`, `WorkDate`, `WorkType` (doc-type code), **`SystemEntryDate`** (immutable creation timestamp), `CustomerID`.
- `Line`: `LineNumber`, `OrderReferences` (OriginatingON/OrderDate ← the `document_links` graph), `ProductCode`, `Quantity`, `UnitOfMeasure`, `UnitPrice`, `TaxBase`, `TaxPointDate`, `References` (corrective-doc reference), **`ProductSerialNumber/SerialNumber*`** (← inventory serials), `Tax` (TaxType/Region/Code), `TaxExemptionReason`/`TaxExemptionCode`, `SettlementAmount`.
- `DocumentTotals`: `TaxPayable`, `NetTotal`, `GrossTotal`, `Currency` (CurrencyCode/Amount/ExchangeRate) ← fiscal document totals + multicurrency.
- **Capture-now:** `SourceBilling` (produced/integrated/manual), `SystemEntryDate`, `WorkType`/`EACCode`, `TaxPointDate`, structured `TaxExemptionReason`+`TaxExemptionCode`, serial numbers on lines.

### `Payments` → treasury obligations/allocations ([[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]])
- `Payment` (PaymentRefNo, PaymentType, `DocumentStatus`/PaymentStatus/`SourcePayment`, `SystemEntryDate`) ← a treasury settlement document; `PaymentMethod*` (PaymentMechanism, Amount, Date) ← `treasury_movements` (method/amount/value_date); `Line/SourceDocumentID` (OriginatingON, InvoiceDate) + `SettlementAmount` ← `allocations` (movement↔obligation); `DocumentTotals` + `Settlement`.
- **`WithholdingTax`** (WithholdingTaxType, Description, Amount) — **confirms** the withholding-to-State pattern surfaced in [[2023 - Cegid Primavera Tesouraria (Legacy Reference)]]; NOVA-ERP must capture withholding on payments and feed both the payee obligation and the State withholding map.
- **Capture-now:** `PaymentMechanism` (cash/transfer/cheque code), `SourcePayment`, `SystemEntryDate`, withholding per payment.

### `PhysicalStock` → inventory projection at a date ([[2026-05-28 - Schema Decision - Inventory Movements and Valuation]])
- `PhysicalStockDate` + `PhysicalStockEntry*`: `WarehouseID`, **`LocationID`** (← the `locations` sub-table added from the Inventário deck), `ProductCode`, `StockAccountNo`, `ProductType`, `ProductStatus`, `UnitPrice`, `StockQuantity`, **`StockValue`**, `StockCharacteristics`.
- Confirms inventory SAF-T is a **valued snapshot at a date** — `stock_on_hand` projection × valuation (`UnitPrice`/`StockValue`) per warehouse+location. Validates the ADR's derived-quantity + valuation-layer design and the `location_id` addition.

## Cross-cutting capture-at-transaction-time checklist

To avoid impossible exports later, NOVA-ERP must persist from day one:
1. `entities`: structured address (ISO country), fiscal name, `tax_id`, and the **GL control account** (`AccountID`).
2. `chart_of_accounts`: `taxonomy_code` + tenant `taxonomy_reference` (SNCRF).
3. `tax_rates`: SAF-T `(TaxType, TaxCode)` pair + `TaxCountryRegion`.
4. fiscal documents: `SystemEntryDate`, `SourceBilling`, `WorkType`, `TaxPointDate`, structured tax-exemption reason+code, line serial numbers, currency/exchange.
5. journal entries: `Period`, `GLPostingDate`, `DocArchivalNumber`, `TransactionType`.
6. treasury: `PaymentMechanism`, `SourcePayment`, per-payment `WithholdingTax`.
7. inventory: warehouse+`location_id`, valued stock (`UnitPrice`/`StockValue`), product status.

## Header obligations (all content types)
`CompanyID`, `TaxRegistrationNumber`, `FileContentType` (F/C/I/O), `FiscalYear`, `StartDate`/`EndDate`, `CurrencyCode`, `TaxEntity`, `SoftwareCertificateNumber` + `ProductCompanyTaxID`/`ProductID`/`ProductVersion`, `NumberOfParts`/`PartNumber`. NOVA-ERP needs a per-tenant **DNRE software-certificate number** and a multi-part export splitter.

## Code lists
All 14 enumerated code lists are decoded in [[SAF-T CV Code Lists]] (FileContentType, TaxonomyReference, ProductType, TaxType, WorkType/WorkStatus/SourceBilling, PaymentType/Status/SourcePayment/PaymentMechanism, WithholdingTaxType, TransactionType, PSProductType, ProductStatus). Seed these as system code tables and validate at write time.

## Open follow-ups
- Resolve the **(convention — confirm)** rows in [[SAF-T CV Code Lists]] (ProductType, TaxType `TEU`, PSProductType `AB`, ProductStatus `D`/`DS`/`Q`) against the DNRE manual.
- Confirm the SNCRF `TaxonomyReference`/`TaxonomyCode` list source (Portaria 47/2021) — the accounting-taxonomy contradiction.
