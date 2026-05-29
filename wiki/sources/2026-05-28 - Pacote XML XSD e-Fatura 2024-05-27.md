---
type: source
status: active
created: 2026-05-28
updated: 2026-05-28
source_path: https://efatura.cv/assets/files/2024-05-27-XML-XSD-497f4b5a8e89ac2a3f766bb0cb85f9d9.zip
source_page: https://efatura.cv/docs/xsd
source_type: schema-package
author: Direcao Nacional de Receitas do Estado / e-Fatura Cabo Verde
published: 2024-05-27
ingested: 2026-05-28
tags: [source, efatura, cabo-verde, xsd, xml, schema, dfe]
related: ["[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[DNRE]]"]
confidence: high
---

# Pacote XML XSD e-Fatura 2024-05-27

## Summary

Pacote XSD oficial listado em 2026-05-28 na pagina de schemas da e-Fatura Cabo Verde como `2024-05-27-XML-XSD`.

Este pacote e contrato executavel complementar ao [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]. Para implementacao, o manual explica regras e fluxo; o XSD define estrutura XML, tipos, obrigatoriedade estrutural e exemplos.

Official page: https://efatura.cv/docs/xsd

## Package Contents

Arquivos principais observados:

- `Read Me.txt`;
- `XML Fields Map.txt`;
- `EnvelopedSignature.xsd`;
- `InternallyDetachedSignature.xsd`;
- `common/CV_EFatura_Elements_v1.0.xsd`;
- `common/CV_EFatura_Types_v1.0.xsd`;
- XSDs por documento fiscal;
- `W3C_XMLDSig.xsd`;
- XSDs ETSI XAdES;
- tabelas ISO de pais/moeda;
- tabela UNECE de meios de pagamento;
- exemplos XML para Invoice, InvoiceReceipt, SalesReceipt, Receipt, CreditNote, DebitNote, Transport, ReturnNote, RegistrationNote e Event.

## Changelog Captured

O `Read Me.txt` registra:

- 2023-12-15: adicionada estrutura `SelfBilling` aos DFEs;
- 2024-05-27: adicionado `IssueReasonCode=DRP` para Desconto por Rappel e `RappelPeriod` a NCE.

## Field Map Highlights

O `XML Fields Map.txt` confirma:

- `Dfe@Version` obrigatorio;
- `Dfe@Id` obrigatorio;
- `Dfe@DocumentTypeCode` obrigatorio;
- `Transmission` obrigatorio;
- `RepositoryCode` obrigatorio;
- `Signature` obrigatoria;
- `SelfBilling` opcional e aplicavel apenas a FTE, FRE, RCE, NCE, NDE e DVE;
- `SelfBilling.AuthorizationId` e UUID obrigatorio quando `SelfBilling` existe;
- `SelfBilling.AuthorizationCode` e string obrigatoria quando `SelfBilling` existe;
- `RappelPeriod` e opcional, tipo `DatePeriod`, e aplicavel apenas a NCE;
- `Tax` permite exatamente um entre `TaxPercentage`, `TaxAmount` e `TaxExemptionReasonCode`;
- `Totals.WithholdingTaxTotalAmount` e opcional;
- `DatePeriod` contem `StartDate` e `EndDate`.

## Schema-Level Implementation Notes

Para NOVA-ERP:

- implementar validacao XSD local como gate antes de submissao;
- manter versao do pacote XSD usada em cada validacao/transmissao;
- gerar fixtures por tipo DFE usando os exemplos oficiais como base de testes;
- separar constraints XSD de regras fiscais adicionais do manual;
- tratar `SelfBilling` e `RappelPeriod` como subestruturas tipadas, nao texto livre;
- modelar assinatura XML como parte do payload fiscal, nao como metadado externo;
- preservar XML final assinado e ZIP submetido com retencao/auditoria apropriada.

## Event Schema Highlights

O pacote confirma que `Event` e raiz XML oficial ao lado de `Dfe`.

Arquivos relevantes:

- `CV_EFatura_MainElements_v1.0.xsd` declara `Event`.
- `CV_EFatura_MainTypes_v1.0.xsd` define `ctEvent`.
- `CV_EFatura_Types_v1.0.xsd` define `stEventTypeCode`.
- `99 Event.xml` fornece exemplo oficial.

Tipos de evento no pacote atual:

- `FDC` - Fiscal Document Cancellation, cancelamento/anulacao de DFE.
- `UDN` - Unused Document Number, inutilizacao de numero de documento.

Estrutura capturada:

- atributos obrigatorios: `Id`, `Version`, `EventTypeCode`;
- corpo com `EmitterTaxId`, `IssueDateTime`, `IssueReasonDescription`, alvo do evento, `Transmission` e `RepositoryCode`;
- alvo por `IUD` para `FDC`, admitindo mais de um IUD segundo o changelog;
- alvo por intervalo fiscal para `UDN`, com `Year`, `LedCode`, `Serie`, `DocumentTypeCode`, `DocumentNumberStart` e `DocumentNumberEnd`.

Implementacao: ver [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]].

## Open Questions

- Deve o MVP suportar `FDC`, `UDN`, ambos, ou apenas preservar o modelo para eles?
- Quais exemplos oficiais devem virar fixtures automatizadas de regressao?
- Como versionar futuras atualizacoes de XSD sem invalidar documentos historicos ja emitidos?
