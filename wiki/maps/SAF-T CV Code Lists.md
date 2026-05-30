---
type: map
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [saft, cabo-verde, code-lists, seed-data, reference, fiscalidade]
sources: ["[[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]]", "[[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]"]
related: ["[[SAF-T CV]]", "[[2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema]]", "[[Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy]]"]
confidence: high
---

# SAF-T (CV) Code Lists (Seed Reference)

The 14 enumerated `simpleType` code lists from the official **SAF-T (CV) v1.01_01** XSD (`raw/assets/saft-cv/saftcv1.01_01.xsd`). These are the canonical values NOVA-ERP must seed and emit. **All values are now authoritative** — the few that the XSD left undocumented were confirmed against the Anexo I field definitions in primary law [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]] (field indices noted inline).

## Header

### `FileContentType` — SAF-T file content type
| Code | Meaning |
|------|---------|
| `F` | Faturação |
| `C` | Contabilidade |
| `I` | Inventário |
| `O` | Outros |

(No official "Completo". See [[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]].)

### `TaxonomyReference` — chart-of-accounts taxonomy referential
| Code | Meaning (official) |
|------|--------------------|
| `S` | SNCRF base — Taxonomia S |
| `N` | Normas Internacionais de Contabilidade e Relato Financeiro (NIRF) — Taxonomia S |
| `P` | NRF-PE pequenas entidades — Taxonomia S |
| `O` | Outros referenciais (taxonomia não codificada — ex. banca/seguros; associar contas à taxonomia única «1» em `TaxonomyCode`) |

## MasterFiles

### `ProductType` — product type (MasterFiles, Anexo I 2.4.1)
| Code | Meaning (official) |
|------|--------------------|
| `P` | Produtos |
| `S` | Serviços |
| `O` | Outros |
| `E` | Impostos Especiais de Consumo |
| `I` | Impostos, taxas e encargos parafiscais (exceto IVA, IS e TEU) |

### `TaxType` — tax type (Anexo I 2.5.1.1)
| Code | Meaning (official) |
|------|--------------------|
| `IVA` | Imposto sobre o Valor Acrescentado |
| `IS` | Imposto do Selo |
| `NS` | Não sujeição a IVA, IS ou TEU |
| `TEU` | **Tributo Especial Unificado** |

### `TaxCode` — IVA tax code (Anexo I 2.5.1.3)
| Code | Meaning (official) |
|------|--------------------|
| `NOR` | Taxa normal |
| `RED` | Taxa reduzida |
| `ISE` | Isento |
| `ESP` | Regimes especiais de IVA |
| `NS` | Não sujeição |

## SourceDocuments — WorkingDocuments

### `WorkType` — working-document type (official)
| Code | Meaning |
|------|---------|
| `CC` | Créditos de consignação |
| `CM` | Consulta de mesa |
| `FC` | Faturas à consignação |
| `FO` | Folha de obra |
| `NE` | Nota de encomenda |
| `OR` | Orçamento |
| `PF` | Fatura pró-forma |
| `OU` | Outros documentos apresentáveis ao cliente |

### `WorkStatus` — working-document status (official)
| Code | Meaning |
|------|---------|
| `N` | Normal |
| `A` | Anulado |
| `F` | Faturado |

### `SourceBilling` — origin of the working document (official)
| Code | Meaning |
|------|---------|
| `P` | Produzido na aplicação |
| `I` | Integrado (produzido noutra aplicação) |
| `M` | Manual (recuperado de documento em papel) |

## SourceDocuments — Payments

### `PaymentType` — payment document type (official)
| Code | Meaning |
|------|---------|
| `RC` | Recibo de Cliente |
| `PF` | Pagamento a Fornecedor |
| `OU` | Outros |

### `PaymentStatus` (official)
| Code | Meaning |
|------|---------|
| `N` | Normal |
| `A` | Anulado |

### `SourcePayment` — origin of the payment (official)
| Code | Meaning |
|------|---------|
| `P` | Produzido na aplicação |
| `I` | Integrado (produzido noutra aplicação) |
| `M` | Manual |

### `PaymentMechanism` — means of payment (official)
| Code | Meaning |
|------|---------|
| `CC` | Cartão de crédito |
| `CD` | Cartão de débito |
| `CH` | Cheque bancário |
| `CI` | Crédito documentário internacional |
| `CO` | Cheque ou cartão oferta |
| `CS` | Compensação de saldos em conta corrente |
| `DE` | Dinheiro eletrónico (ex. cartões de fidelidade/pontos) |
| `LC` | Letra comercial |
| `MB` | Referências de pagamento Multibanco |
| `NU` | Numerário |
| `OU` | Outros meios não assinalados |
| `TB` | Transferência bancária ou débito direto autorizado |
| `TR` | Títulos de compensação extrassalarial (ex. refeição, educação) |

### `WithholdingTaxType` — withholding tax (official)
| Code | Meaning |
|------|---------|
| `IRPS` | Imposto sobre o Rendimento das Pessoas Singulares |
| `IRPC` | Imposto sobre o Rendimento das Pessoas Coletivas |

## GeneralLedgerEntries

### `TransactionType` — journal transaction type (official)
| Code | Meaning |
|------|---------|
| `N` | Normal |
| `R` | Regularizações do período de tributação |
| `A` | Apuramento de resultados |
| `J` | Movimentos de ajustamento |

## PhysicalStock

### `PSProductType` — Tipologia de inventário (Anexo I 4.3.1.2.1.5)
| Code | Meaning (official) |
|------|--------------------|
| `M` | Mercadorias |
| `AB` | Ativos biológicos |
| `MP` | Matérias-primas, subsidiárias e de consumo |
| `PCI` | Produtos acabados e intermédios |
| `SP` | Subprodutos, desperdícios e refugos |
| `PC` | Produtos e trabalhos em curso |

### `ProductStatus` — Situação do inventário (Anexo I 4.3.1.2.1.6)
| Code | Meaning (official) |
|------|--------------------|
| `A` | Ativo |
| `D` | Danificado |
| `DS` | Descontinuado |
| `O` | Obsoleto |
| `Q` | Quarentena |

## Implementation note

NOVA-ERP should seed these as system-owned code tables (tenant-read), validate document/line/entry codes against them at write time, and emit them verbatim in SAF-T exports. All values are confirmed against primary law [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]]; no convention-only rows remain. The **account taxonomy codes** (`TaxonomyCode`) are a separate, larger list in **Anexo II** of that portaria (SNCRF Base / NIC) — still to be extracted into a `chart_of_accounts.taxonomy_code` seed.
