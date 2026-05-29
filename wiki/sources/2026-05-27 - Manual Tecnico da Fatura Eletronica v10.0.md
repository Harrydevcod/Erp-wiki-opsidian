---
type: source
status: superseded
created: 2026-05-27
updated: 2026-05-28
source_path: docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf
source_type: technical-manual
author: Direcao Nacional de Receitas do Estado / Grupo de Trabalho FE
published:
ingested: 2026-05-27
tags: [source, efatura, cabo-verde, dfe, dnre, compliance]
related: ["[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Fiscalidade Cabo Verde]]", "[[DNRE]]", "[[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]"]
confidence: high
---

# Manual Tecnico da Fatura Eletronica v10.0

## Summary

This DNRE technical manual specifies the technical functionality of the Cabo Verde electronic invoice platform and the structure of Documentos Fiscais Eletronicos (DFEs). It is the strongest current source in this vault for DFE XML structure, document types, IUD composition, validation rules, transmission modes, signature requirements, OAuth/API access, event submission, autofaturacao and middleware behavior.

Supersession note: on 2026-05-28, the official e-Fatura manual page listed [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] as the latest version. This v10.0 page remains historical/technical evidence but should not be treated as current implementation authority.

Evidence: `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`

External currency check: the DNRE e-Fatura manual page was found on 2026-05-27 listing `Manual Tecnico da Fatura Eletronica v10.0` as the latest version.

Official web evidence:

- `https://j.dnre.gov.cv/docs/manual/`
- `https://j.dnre.gov.cv/assets/files/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`

## Role In Source Hierarchy

For [[NOVA-ERP]], this source should govern the technical contract of e-Fatura integration. It does not replace legal review of Decreto-Lei, despachos or current DNRE operational guidance, but it is implementation-authoritative for the DFE technical structure unless superseded by a newer official manual.

## Manual Version History

Important changes recorded by the manual:

- v3.2 removed draft status and made the written content stable for implementation.
- v5.0 added XML generation and changed IUD composition to 45 characters.
- v8.0 defined event structures for DFE cancellation/anulation and document number invalidation.
- v9.0 added information line type and integrated middleware documentation.
- v10.0 added autofaturacao, made emitter email mandatory, made emitter phone or mobile mandatory, and added a withholding tax totalizer.

## Conceptual Model

The manual describes five technical pillars:

- XML format with Cabo Verde-specific structure.
- Secure communication to the tax administration over HTTPS/TLS.
- Digital signature with a certificate valid under ICP-CV.
- Platform validation and authorization.
- Tools/ecosystem access for taxpayers and consumers.

The manual states that validation/authorization by the electronic platform is synchronous: the taxpayer system waits for the process to finish. This creates a design tension with NOVA-ERP's internal preference for asynchronous queues; see [[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]].

## Supported DFE Types

The manual defines these DFE document types:

| Code | Element | DFE |
| --- | --- | --- |
| 1 | `Invoice` | FTE - Fatura Eletronica |
| 2 | `InvoiceReceipt` | FRE - Fatura Recibo Eletronica |
| 3 | `SalesReceipt` | TVE - Talao de Venda Eletronico |
| 4 | `Receipt` | RCE - Recibo Eletronico |
| 5 | `CreditNote` | NCE - Nota de Credito Eletronica |
| 6 | `DebitNote` | NDE - Nota de Debito Eletronica |
| 7 | `Transport` | DTE - Documento de Transporte Eletronico |
| 8 | `ReturnNote` | DVE - Nota de Devolucao |
| 9 | `RegistrationNote` | NLE - Nota de Lancamento |

Implementation implication: NOVA-ERP's "supported document type" table should not be hard-coded only around invoice, invoice-receipt and credit note. It needs a DFE type layer even if MVP exposes only a subset.

## Required DFE Field Groups

The manual groups DFE data into:

- document identification;
- emitter;
- receiver/destination;
- transporter where applicable;
- payment;
- items/products/services;
- totals;
- software;
- contingency;
- custom fields.

Not every group applies to every DFE type. The validation chapter defines which structures are required by type.

## IUD And Numbering

The IUD is exactly 45 characters and includes country, repository, date, emitter NIF, LED, document type, document number, random code and verification digit. The combination of NIF, year, LED, document type and document number must be unique in SFECV.

Document number rules include:

- document number is mandatory;
- it must be an integer greater than or equal to 1;
- it should be sequential without gaps within NIF/year/LED/document type;
- numbering restarts each year within that combination.

Some sequence checks are deferred by SFECV rather than validated at transmission time. NOVA-ERP should still treat them as product constraints because deferred validation can become audit/compliance exposure.

## Validation And Authorization

The platform validates:

- XML structure and XSD conformance;
- digital signature;
- data types;
- NIF correctness and fiscal registration;
- codes and enumerations;
- tax rates;
- calculations and totals.

If all validations succeed, the DFE is stored in the electronic platform and authorized for taxpayer use.

## Transmission Modes

The manual defines three issue/transmission modes:

- `ONLINE`: normal mode when emitter has power, own system, internet and other conditions to transmit to the tax administration.
- `OFFLINE`: contingency mode when the emitter's own system works, but transmission is unavailable because of connectivity or platform/service outage.
- `OFF`: contingency mode when the emitter cannot efficiently use the own electronic system, for example due to power outage, and uses a non-electronic mechanism.

The transmission structure is mandatory in all DFEs. The contingency structure is mandatory when issue mode is not online.

## Contingency Rules

The contingency structure includes:

- LED;
- IUC, mandatory for `OFF`;
- contingency issue date;
- contingency issue time, mandatory for `OFFLINE`;
- reason type code;
- reason description when reason is "other".

Reason codes include authorization service unavailability, electricity outage, taxpayer system unavailability, internet connection unavailability, timestamp service unavailability and other.

The auxiliary fiscal document for contingency explicitly indicates that it is pending authorization and does not confer deduction right until the associated document is transmitted and authorized.

## Signature And Repository

All DFEs and events require a signature structure. The signature must comply with XMLDSig and XAdES-BES.

The repository code is mandatory:

- `1` Principal;
- `2` Homologacao;
- `3` Teste.

DFEs in the Principal repository have legal validity in Cabo Verde when signed with an RSA private key whose corresponding public key is certified by an ICP-CV certificate authority.

## APIs And OAuth

The manual documents REST endpoints under `https://services.efatura.cv/{version}/{resource}` over HTTPS. Authentication/authorization uses OpenID Connect/OAuth, with Authorization Code Flow and PKCE.

Relevant scopes include:

- LED create/read/update/delete/all;
- DFE create/read list/read by IUD/read stats/delete in homologation-test/all;
- EVENT create/read/all;
- CERTIFICATE read/all;
- TAXPAYER search/all;
- SOFTWARE group/transmitter/customer permissions;
- `offline_access` for refresh token.

DFE emission requires the taxpayer system to generate XML, place XML files inside a Deflate ZIP, send multipart/form-data to the DFE endpoint and include repository header `cv-ef-repository-code`. XML filenames inside the ZIP must be the IUD plus `.xml`.

## DFE Reading And Events

The manual supports reading DFEs by filters and by IUD. A single DFE can be read through an endpoint that returns the XML by IUD.

Event emission is done similarly to DFE emission, but against the `event` resource. The manual history says events cover DFE cancellation/anulation and document number invalidation, but the extracted text needs deeper schema-level reading before NOVA-ERP treats cancellation transitions as fully specified.

## Autofaturacao

Version 10.0 adds autofaturacao. The buyer first requests an authorization code from the seller through a self-billing authorization endpoint. The code is sent to the seller's phone and/or email. The authorization code must then be indicated in the emitted DFE.

Implementation implication: autofaturacao should remain non-MVP until NOVA-ERP explicitly designs buyer/seller authorization, evidence retention and operational support.

## Middleware

The manual says the middleware is a free intermediary system provided by the tax administration to be installed on the taxpayer network to significantly facilitate integration with the electronic platform.

Middleware details include:

- installers for Windows, GNU/Linux and macOS;
- local service installation and execution;
- GUI for emitter authorization and resources;
- mandatory `transmitter-key` for requests from taxpayer software to middleware;
- configuration in `MW_HOME/config/application.properties`;
- transmitter configuration with NIF, fiscal name, OAuth client ID and client secret;
- emitter configuration via file or GUI;
- middleware base URL replacing `https://services.efatura.cv`, often `https://localhost:3443`;
- required header `cv-ef-mw-core-transmitter-key`.

This supports the hybrid interpretation now captured in [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]: the endpoint can be environment-level while emitter configuration is tenant/contributor-specific.

## NOVA-ERP Implementation Consequences

- Treat DFE XML and XSD validation as a first-class backend concern.
- Model `repository_code`, `led_code`, `document_type_code`, `document_number`, `iud`, `issue_mode`, transmitter NIF and software metadata explicitly.
- Keep business document state separate from official e-Fatura authorization and contingency details.
- Generate IUD only when enough final data exists to guarantee uniqueness and immutability.
- Preserve SFECV responses and event submissions as audit evidence.
- Support Principal, Homologacao and Teste repositories as environment/configuration dimensions.
- Keep middleware and direct PE API concepts separate in architecture, even if product policy chooses middleware-only for production.

## Validated Against Previous Candidate Design

Survives as official contract:

- DFE/XML generation.
- HTTPS/TLS communication.
- ICP-CV certificate-backed digital signature.
- IUD.
- LED/series-like emission logic.
- document number uniqueness and sequence constraints.
- explicit contingency.
- authorization after platform validation.
- middleware as supported integration component.
- event submission for cancellation/anulation and number invalidation.

Needs adjustment:

- NOVA-ERP's internal `submitted`, `queued`, `retrying` and `failed` states are implementation states, not official DFE states from the manual.
- `settled` is an ERP treasury/business state, not an e-Fatura state.
- "asynchronous e-Fatura" must be reframed: NOVA-ERP may queue work internally, but the official platform authorization process is synchronous once the request is made.

Needs further verification:

- exact event XML structures for cancellation/anulation and invalidation;
- legal correction/cancellation rules outside the technical event schema;
- current production onboarding practice for middleware, certificates and transmitters;
- whether direct PE API use is permitted/desired for NOVA-ERP production, given project instructions favor middleware.
