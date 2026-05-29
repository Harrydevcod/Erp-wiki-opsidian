---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [efatura, cabo-verde, dnre, dfe, compliance]
sources: ["[[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]", "[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]", "raw/assets/SSD/PRD.MD", "raw/assets/LOCAL_SETUP-Arydson.md", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]"]
related: ["[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[NOVA-ERP]]", "[[Supabase Deployment]]", "[[Contradiction - Middleware URL Scope]]", "[[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]]"]
confidence: high
---

# e-Fatura Cabo Verde

## Definition

e-Fatura Cabo Verde is the electronic invoice domain for Cabo Verde fiscal documents, involving DNRE-compatible document generation, communication, security, processing, status handling and contingency/retry flows.

## Current Synthesis

For [[NOVA-ERP]], e-Fatura should be designed with strong auditability around an official synchronous authorization contract. Internally, NOVA-ERP can use asynchronous queues, workers, retries and technical states, but the DNRE manual states that the platform validation/authorization process itself is synchronous once the taxpayer system submits the DFE.

The latest official manual found on 2026-05-28 is [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], not v10.0. The current official XSD package listed on the e-Fatura schema page is [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]. Existing v10.0 synthesis remains useful historical evidence but is no longer implementation authority.

The local setup notes also indicate an OAuth callback through Supabase Edge Functions for e-Fatura integration.

Source: [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-26 - SSD NOVA-ERP]]

[[2026-05-28 - Manual de Faturas em Cabo Verde]] contains older electronic-invoice legal background around equivalence to paper invoices, authorization to use electronic invoice systems, readable access, conservation and integrity controls. Because current e-Fatura public guidance describes a real-time, tax-authority-authorized digital DFE regime, the 2018 manual should be treated as background for retention/audit principles, not as the final modern DFE implementation contract. See [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] for the surviving/superseded rule classification.

Evidence: [[2026-05-28 - Manual de Faturas em Cabo Verde]], https://efatura.cv/docs/about/e-fatura/, https://efatura.cv/docs/manual/

## Official Technical Contract

The v11.0 manual and current XSD package confirm these implementation anchors:

- DFEs are represented in XML with Cabo Verde-specific structure and XSD validation.
- Communication uses HTTPS/TLS.
- DFEs and events require digital signature using XMLDSig and XAdES-BES.
- Production legal validity depends on an ICP-CV certificate chain for the signature key.
- The DFE root declares namespace `urn:cv:efatura:xsd:v1.0`.
- IUD identifies the DFE and has exactly 45 characters.
- The combination of NIF, year, LED, document type and document number must be unique.
- The platform validates XML structure, signature, data types, NIFs, codes, taxes, calculations and totals before authorization.
- Repository code distinguishes Principal, Homologacao and Teste.
- v11.0 adds/updates correction territory through `IssueReasonCode=DRP` and `RappelPeriod` for NCE discount by rappel.
- The XSD package confirms `SelfBilling`, `RappelPeriod`, `Transmission`, `RepositoryCode`, `Signature`, optional withholding totals and the field-level DFE map.
- The XSD package declares an `Event` root beside `Dfe`; current event type codes are `FDC` for cancelamento/anulacao de DFE and `UDN` for inutilizacao de numero de documento.

Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]

## Schema/API Contract Highlights

- Root XML namespace: `urn:cv:efatura:xsd:v1.0`.
- Root attributes: `Version`, `Id`/IUD and `DocumentTypeCode`.
- IUD must be exactly 45 characters.
- Numbering is unique and sequential by `(NIF, year, LED, document type)`.
- `IssueReasonCode` is required for NCE/NDE/DVE; `DRP` means desconto por rappel and is valid for NCE.
- `RappelPeriod` is a typed period for NCE and should be modeled explicitly.
- DFE submission sends Deflate ZIP in `multipart/form-data`, field `file`, with XML files named `IUD.xml`.
- DFE API calls include repository context through `cv-ef-repository-code`.
- Middleware calls use the middleware base URL and header `cv-ef-mw-core-transmitter-key`.
- OAuth uses Authorization Code Flow with PKCE; v11.0 adds `cv_ef_dfe_self_billing_authorize` and `cv_ef_opacc_read_accountant_list`.
- Autofaturacao has a specific authorization API and should not be collapsed into ordinary invoice issuance.

Implementation implication: NOVA-ERP should treat XSD validation, XML signature, ZIP packaging, OAuth/middleware authentication, repository selection and response persistence as first-class fiscal infrastructure, not as UI-side export logic.

## Supported DFE Types

The manual-defined DFE types are:

- FTE - Fatura Eletronica;
- FRE - Fatura Recibo Eletronica;
- TVE - Talao de Venda Eletronico;
- RCE - Recibo Eletronico;
- NCE - Nota de Credito Eletronica;
- NDE - Nota de Debito Eletronica;
- DTE - Documento de Transporte Eletronico;
- DVE - Nota de Devolucao;
- NLE - Nota de Lancamento.

Implementation implication: NOVA-ERP should model the full DFE type vocabulary even if MVP exposes only the commercial subset.

## Middleware Operating Model

[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] supports a shared middleware endpoint per environment:

- local development middleware on localhost;
- staging middleware on a staging endpoint;
- production middleware on a VPS/private network endpoint.

Tenant-specific e-Fatura data still exists, but mostly as emitter configuration, credentials, certificate metadata/onboarding and middleware `application.properties`/keystore state.

Current decision: use an environment-level default middleware endpoint with tenant-level e-Fatura configuration and readiness status. Tenant endpoint overrides are allowed only as platform-admin controlled exceptions, not ordinary tenant settings. See [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]].

## Contingency Model

The manual defines `ONLINE`, `OFFLINE` and `OFF` issue modes. The contingency structure is mandatory when the issue mode is not online and includes LED, issue date, reason type, and in some cases IUC and issue time.

The middleware guide adds an operational queue/retry model around this official contingency contract. This means NOVA-ERP should distinguish official contingency fields from its own retry job state.

## Event Model

The current XSD package confirms that e-Fatura events are signed XML payloads with their own root, identifiers, reason description, targets, transmission metadata and repository code.

The current official event type vocabulary captured from the package is:

- `FDC` - Fiscal Document Cancellation, for cancelamento/anulacao de DFE.
- `UDN` - Unused Document Number, for inutilizacao de numero de documento.

For NOVA-ERP, this means cancellation/anulation and unused-number handling must not be implemented as direct document deletion or a simple `cancelled` flag. They need event requests, event targets, signed event XML payloads, validation results, transmission attempts, responses and audit history. See [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]].

Source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]

## Evidence Storage And Secrets

e-Fatura evidence storage is split into three security classes:

- metadata in tenant-scoped PostgreSQL tables;
- signed XML, ZIP archives, raw responses and validation artifacts in private fiscal evidence storage;
- PFX/private keys, keystores, transmitter keys, client secrets and passphrases outside normal domain tables and ordinary UI access.

For MVP, signed/submitted fiscal evidence should live in private storage with hashes and references in tables, accessed only through server-side permission checks. Certificate tables store metadata/reference only; raw certificate/private-key material requires an approved secret manager or middleware keystore flow. See [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]].

Source: [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]], [[2026-05-28 - Supabase Deploy]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]

## Implementation Boundary

Production e-Fatura implementation should not start from a generic invoice table alone. Minimum foundation objects should include fiscal document snapshots, DFE payloads, XSD validation results, DFE transmission batches, DFE transmission attempts, DFE references, DFE contingency records, self-billing authorizations, rappel periods and signed XML/archive storage references.

[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] turns this boundary into the first provisional schema decision: separate fiscal documents, snapshots, DFE payloads, validation results, batches, attempts, references, contingency, self-billing, rappel periods and certificate references instead of using a single `efatura_status` field.

## Evidence

- Source: [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]
- Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]
- Source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]
- Source: [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]
- Source: [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]
- Source: [[2026-05-28 - Manual de Faturas em Cabo Verde]]
- Source: [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]
- Evidence: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Evidence: `raw/assets/LOCAL_SETUP-Arydson.md`
- Source: [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]
- Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]

## Open Questions

- Which endpoint and middleware details require production credential testing beyond the manual?
- Should tenant onboarding update middleware configuration automatically, or require admin approval?
- Which legal retention period applies to DFE XML, event XML, ZIP archives, DFA/PDF renders and DNRE responses?
- Which legal rules decide when a DFE can be cancelled/anulated through `FDC` versus corrected by NCE/NDE/DVE?
- Should NOVA-ERP permit multi-IUD `FDC` in the product UI or restrict the first release to one IUD per event request?
- Should `UDN` ship in MVP, or only after full fiscal series administration is mature?
