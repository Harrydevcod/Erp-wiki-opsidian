---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, faturacao, e-fatura, cabo-verde]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]", "[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[DNRE]]", "[[SAF-T CV]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[Contradiction - Middleware URL Scope]]", "[[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]]"]
confidence: high
---

# Faturacao Eletronica

## Purpose

Faturacao Eletronica is the NOVA-ERP module area for issuing, controlling, communicating and auditing fiscal documents in Cabo Verde.

## Role In NOVA-ERP

This module should be treated as part of the fiscal core, not as a sales screen with an export button. For [[NOVA-ERP]], invoice generation, document series, tax calculation, document states, correction flows, e-Fatura communication and audit history must be designed together.

Source: [[2026-05-26 - Captura Raw e Docs]]

## Source Basis

- Product intent: `raw/assets/SSD/PRD.MD`
- Compliance authority: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Manual de Faturas em Cabo Verde]]
- ERP workflow reference: `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
- Middleware operations: [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]
- Related concepts: [[e-Fatura Cabo Verde]], [[Fiscalidade Cabo Verde]], [[SAF-T CV]]

## Core Workflows

- Configure fiscal document types, series and numbering.
- Issue invoices and corrective documents.
- Calculate IVA and fiscal totals before document finalization.
- Generate or prepare DFE/XML payloads for e-Fatura.
- Communicate documents to DNRE/e-Fatura through a secure integration path.
- Track technical status, rejection reasons, retries and contingency states.
- Preserve immutable audit history for issued fiscal documents.

## e-Fatura Technical Flow

The official manual confirms that the platform validation/authorization process is synchronous after the taxpayer system submits the DFE. NOVA-ERP should still use internal queues and technical states for resilience, but the worker's call to PE/middleware must be treated as a synchronous authorization attempt.

1. User issues/authorizes document in NOVA-ERP.
2. Edge Function authenticates user and tenant context.
3. Server-side process loads document, lines and tenant fiscal configuration.
4. System generates XML/DFE payload, IUD, signature and transmission metadata.
5. Payload is validated locally against XSD before submission where possible.
6. Payload is sent to middleware/PE using server-resolved middleware endpoint, HTTPS/TLS, OAuth/middleware credentials and repository context.
7. The authorization attempt returns success or validation/technical failure synchronously.
8. Request/response and technical status are stored.
9. On outage or unavailable transmission, document enters an official contingency mode plus NOVA-ERP retry queue.
10. Retry job resubmits pending contingency documents and preserves every attempt.

Source: [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

## Audit, Security And Tenancy

- Document numbering must be tenant-scoped and controlled.
- Finalized fiscal documents should be immutable except through explicit corrective flows.
- Every communication attempt and status change should be auditable.
- Access to issue, cancel, correct or reprocess documents should be permissioned.

## Cabo Verde Compliance Notes

The technical manual confirms Cabo Verde e-Fatura requirements around DFE/XML, HTTPS/TLS, IUD, LED, repository codes, certificate-backed signature, validation, authorization, contingency, APIs and middleware. [[2026-05-28 - Manual de Faturas em Cabo Verde]] adds the invoice-rule layer around issuance timing, required fields, series, sequential numbering, rectification, REMPE, State/public works invoicing, reverse charge, transport documents and archival. [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] classifies the 2018 manual: fiscal substance largely survives, but paper-era/electronic-invoice processing mechanisms are superseded or narrowed by modern e-Fatura. Because that manual is from 2018 and explicitly orientative/non-normative, current law and e-Fatura guidance still need verification before implementation is treated as complete compliance.

## Open Questions

- Which legal/despacho sources must be read alongside the v11.0 technical manual before production compliance claims?
- Which document types must be supported in the first sellable release?
- What UX should NOVA-ERP use around the synchronous authorization attempt and internal async queue?
- Should tenant middleware onboarding be an automated Edge Function, a back-office operation, or a supervised admin job?
- Which public works/State invoicing, reverse-charge and penalty rules from the 2018 manual remain current?

## Next Ingestion Targets

- `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`

## Next Ingestion Sequence

The next pass should not treat these files as generic references. They should be ingested in the order needed to turn [[Faturacao Eletronica]] from a concept page into an implementation-grade fiscal design.

1. `docs/docsfiscal/MANUAL DE FATURAS.pdf` - ingested as [[2026-05-28 - Manual de Faturas em Cabo Verde]]

   Follow-up result: [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] classifies surviving, superseded and unresolved rules. Event payload structure is now captured in [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]; remaining work is current legal texts and product scope for `FDC`/`UDN`.

2. `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`

   Primary goal: use Cegid Primavera as workflow reference, not as target architecture. Extract useful operational flows around document issuance, IVA maps, credit notes, fiscal reports and SAF-T preparation, then translate them into NOVA-ERP design implications.

   Expected output:

   - source page under `wiki/sources/`;
   - update [[Cegid Primavera]] with invoicing/fiscality workflow reference;
   - update this page with legacy workflow lessons that are worth keeping or improving;
   - avoid copying screen structure or terminology unless it maps cleanly to NOVA-ERP.

## Design Gates Before Implementation

NOVA-ERP should not implement production e-Fatura behavior until these gates are resolved:

- authoritative source gate: pair the deep-ingested v11.0 technical manual and current XSD package with current legal/despacho sources and the invoice manual;
- schema/API gate: implement from [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] and [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], including XSD validation, XML signature, Deflate ZIP upload and API/middleware headers;
- document model gate: define supported first-release document types, series rules, fiscal numbering, correction flows and immutability rules;
- technical state gate: define the canonical state machine from draft to issued, submitted, authorized, rejected, contingency, retried and corrected;
- integration gate: implement [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]] and verify the real DNRE middleware emitter-group behavior before production;
- security gate: define storage and rotation rules for certificates, client secrets, keystores and service-role access;
- audit gate: define immutable fiscal events, communication logs, before/after audit payloads and tenant-visible status history;
- failure gate: define retry policy, escalation, manual intervention, duplicate prevention and reconciliation after middleware/DNRE outage.

## Schema Decisions

- [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] - provisional decision that e-Fatura must be modeled through separate fiscal document, snapshot, DFE payload, validation, batch, attempt, reference, contingency, self-billing and certificate-reference records; not as a single `efatura_status` column.
- [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]] - provisional decision that cancellation/anulation (`FDC`) and unused-number inutilization (`UDN`) require separate event requests, targets, signed event XML payloads, validation results, transmission attempts and audit history.
- [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]] - provisional decision that middleware endpoint resolution uses an environment default, tenant e-Fatura readiness/configuration and platform-admin-only tenant override.
- [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] - provisional decision splitting queryable metadata, private fiscal evidence artifacts and secret/private-key material.

## Implementation Shape To Preserve

Even before all legal conditions are confirmed, the product sources, v11.0 technical contract and current XSD package support a conservative implementation shape:

- UI creates and validates draft fiscal documents, but finalization runs server-side.
- Finalization should be transactional: numbering, fiscal totals, audit event and submission job must not drift apart.
- NOVA-ERP's internal e-Fatura submission orchestration should be asynchronous, observable and retryable, while each PE/middleware authorization attempt is synchronous.
- Middleware endpoint resolution should happen server-side from environment default plus approved tenant binding, never from frontend input.
- Fiscal document records should separate business state from technical communication state.
- DNRE/middleware request and response payloads should be stored with retention and privacy controls, not exposed as casual UI data.
- Corrective documents should be modeled explicitly rather than allowing mutation of finalized documents.
- Voided or inutilized invoice numbers should remain in the chronological sequence and be auditable; no issued/numbered fiscal document should be physically deleted.
- Cancellation/anulation and unused-number inutilization should produce official e-Fatura event records/payloads where applicable, not only internal state changes.
- Rectification documents should reference the original invoice and the mentions being altered.
- All tables involved in issuing, submitting or auditing fiscal documents must be tenant-scoped and protected by RLS.

Source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]], [[2026-05-28 - Manual de Faturas em Cabo Verde]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]

## Uncertainty Register

- Legal currency: current manuals and DNRE guidance must be verified before implementation claims are treated as production compliance.
- Document type scope: the PRD names e-Fatura as MVP/base scope, but the exact first-release fiscal document set remains unresolved.
- Middleware topology: resolved provisionally as environment-level default endpoint plus tenant-level emitter/readiness configuration and platform-admin-only override. Production still needs operational verification against the real DNRE middleware.
- Certificate handling: domain tables store metadata/reference only; raw PFX/private keys/keystores require approved secret-manager or middleware-keystore operations before production.
- Synchronous authorization: resolved at technical-contract level; PE authorization is synchronous, while NOVA-ERP internal orchestration may be asynchronous. UX still needs product decision.
- 2018 invoice manual currency: fiscal substance largely survives, but electronic-invoice processing mechanics are superseded/narrowed; public works, reverse charge and penalty rules remain open for current legal verification.

## Candidate Domain Model

This is a provisional model for implementation planning. It is now constrained by the v11.0 manual, the official XSD package and the first event-level XSD pass. Legal conditions for cancellation/anulation/inutilization still require current authority before production claims.

### Core Records

- `fiscal_document_types`: tenant-available document classes, fiscal behavior, stock impact, treasury impact and e-Fatura eligibility.
- `fiscal_series`: tenant-scoped series, numbering policy, active period, branch/establishment scope where applicable, current counter and no-delete/no-reuse guarantees.
- `sales_documents`: business header for customer-facing documents, including customer, dates, currency, totals, document state and fiscal state.
- `sales_document_lines`: product/service lines, tax profile, quantities, unit price, discounts and fiscal totals.
- `fiscal_document_snapshots`: immutable final payload snapshot used for printing, audit, SAF-T and e-Fatura generation.
- `fiscal_transmissions`: submission attempts to middleware/DNRE, with request metadata, technical status, response codes and retry counters.
- `dfe_payloads`: generated DFE XML payloads, schema version, signature mode, signed XML storage reference and hash.
- `dfe_validation_results`: local XSD/manual-rule validation result, package version, errors and warnings before submission.
- `dfe_transmission_batches`: Deflate ZIP submission unit, repository code, endpoint/middleware base URL, archive hash and file manifest.
- `dfe_references`: structured references to original fiscal documents, IUDs, old documents, payment amounts or tax references.
- `dfe_rappel_periods`: typed start/end period for NCE with `IssueReasonCode=DRP`.
- `dfe_self_billing_authorizations`: authorization id/code, parties, request/response status and expiry/validity metadata for autofaturacao.
- `dfe_contingency_records`: official issue mode, reason code, IUC, LED, issue date/time and DFA state.
- `dfe_event_requests`: cancellation/anulation or unused-number event request, event type, reason, operator, lifecycle state and audit link.
- `dfe_event_targets`: `FDC` IUD targets or `UDN` fiscal number ranges.
- `dfe_event_payloads`: generated/signed event XML, event id, schema/package version, storage reference and hash.
- `dfe_event_validation_results`: XSD/local validation result for event payloads.
- `dfe_event_transmission_attempts`: event ZIP submission attempts, repository, endpoint, response evidence and retry status.
- `fiscal_artifact_refs`: metadata references for signed XML, ZIP archives, raw responses and validation artifacts stored outside ordinary tables.
- `fiscal_artifact_access_events`: audit trail for raw fiscal artifact reads/downloads.
- `secret_refs`: references to secret-manager or middleware-keystore entries without exposing secret values.
- `dfe_transport_routes`: DTE route locations, load/unload ordering, transport mode and vehicle/service-provider data.
- `fiscal_transmission_logs`: append-only event history for each communication attempt and state transition.
- `contingency_queue`: retryable work queue for documents that could not be submitted or authorized normally.
- `digital_certificates`: certificate metadata and secure storage references only; never raw secrets in normal application tables.
- `integration_configs`: tenant e-Fatura readiness, emitter identifiers, mode, onboarding status and middleware linkage.
- `tenant_efatura_middleware_bindings`: tenant binding to environment default middleware or approved platform-controlled endpoint override.
- `tenant_efatura_onboarding_jobs`: controlled jobs for middleware emitter/certificate registration and readiness sync.
- `fiscal_number_events`: append-only record for number assignment, void/inutilization, correction linkage and replacement reference.
- `tax_regime_rules`: tenant/customer/document rule matrix for IVA normal, REMPE, reverse charge, State/public works and non-taxed justification text.

Source: [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]], [[2026-05-28 - Manual de Faturas em Cabo Verde]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]

See also: [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]

### Deliberate Separations

- Business document state is not the same as e-Fatura technical state.
- Document numbering is not the same as middleware submission.
- Certificate metadata is not the same as certificate secret material.
- Printable invoice rendering is not the same as the signed/transmitted DFE payload.
- Fiscal evidence metadata is not the same as raw signed XML/ZIP/response artifacts.
- User-visible rejection explanation is not the same as raw middleware/DNRE response.

These separations prevent the first implementation from collapsing fiscal, operational and integration concerns into one brittle table.

## Candidate State Machine

The first implementation should model two linked state axes. Only part of this vocabulary is official e-Fatura contract; the rest is NOVA-ERP internal orchestration.

### Business State

- `draft`: editable document, no fiscal number consumed.
- `ready_to_issue`: validated document awaiting final issue action.
- `issued`: finalized, numbered and immutable except through corrective flows.
- `settled`: issued and fully paid, where the document type combines invoice and receipt or treasury allocation completes it.
- `cancelled`: cancelled only through an allowed legal/operational path.
- `corrected`: linked to a corrective document such as credit/debit note, without mutating the original fiscal record.

### e-Fatura Technical State

- `not_applicable`: document does not require e-Fatura submission.
- `pending`: document is issued and waiting for DFE generation/submission.
- `queued`: submission job exists but has not completed.
- `submitted`: middleware accepted the submission request for processing.
- `authorized`: document received positive authorization/acceptance.
- `rejected`: document was refused or failed validation and requires controlled action.
- `contingency`: document was issued under outage/failure conditions and must be transmitted later.
- `retrying`: automatic retry is in progress.
- `failed`: retries exhausted or manual intervention required.

Source: [[2026-05-26 - Backlog Estruturado NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

## Official Contract Validation

Validated from [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] and [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]:

- Official DFE types: FTE, FRE, TVE, RCE, NCE, NDE, DTE, DVE and NLE.
- Official issue modes: `ONLINE`, `OFFLINE` and `OFF`.
- Official repository codes: Principal, Homologacao and Teste.
- Official technical identifiers: IUD, LED, document type code, document number, repository code and transmission metadata.
- XML root contract: namespace `urn:cv:efatura:xsd:v1.0`, `Version=1.0`, required `Id`/IUD and required `DocumentTypeCode`.
- Numbering contract: sequential numbering without gaps by `(NIF, year, LED, document type)`, with document number up to 9 digits and series up to 20 allowed characters.
- Official authorization model: PE validates and authorizes synchronously after DFE submission.
- Official contingency model: non-online issue modes require contingency fields and can produce an auxiliary fiscal document pending authorization.
- Official correction contract: `IssueReasonCode` is required for NCE/NDE/DVE; `DRP` is desconto por rappel and uses `RappelPeriod` on NCE.
- Official event contract: `Event` is a first-class XML root; current event type codes are `FDC` for cancelamento/anulacao de DFE and `UDN` for inutilizacao de numero de documento.
- Official API contract: DFE XMLs are submitted as Deflate ZIP in `multipart/form-data` field `file`, with XML filename `IUD.xml` and repository header `cv-ef-repository-code`.
- Official middleware contract: middleware calls use middleware base URL and header `cv-ef-mw-core-transmitter-key`.
- Official/project middleware topology: NOVA-ERP resolves middleware endpoint server-side from environment default plus tenant readiness/binding; tenant endpoint override is platform-admin controlled.
- Official/project evidence storage: signed XML, submitted ZIP and raw responses are private fiscal artifacts with table references/hashes; certificate private-key material stays outside ordinary domain tables.
- Official OAuth contract: Authorization Code Flow with PKCE; v11.0 includes scopes `cv_ef_dfe_self_billing_authorize` and `cv_ef_opacc_read_accountant_list`.
- Official correction/event territory: the event schema supports `FDC` and `UDN`; current legal rules still need verification before NOVA-ERP finalizes when operators may use each flow.
- v11.0 is the latest official manual found on 2026-05-28; v10.0 is no longer the current implementation authority.

Survives as NOVA-ERP internal state, not official PE state:

- `draft`;
- `ready_to_issue`;
- `queued`;
- `submitted`;
- `retrying`;
- `failed`;
- `settled`.

Needs rename or stricter semantics:

- `issued` should mean "finalized and numbered inside NOVA-ERP"; it does not imply PE authorization.
- `authorized` should mean PE/DNRE authorization returned successfully.
- `rejected` should store validation/technical failure response, but the manual should be checked at response schema level before this becomes final enum naming.
- `contingency` should preserve the official issue mode and reason code, not just mean "background job failed".

## State Transition Rules

- `draft` to `issued` must happen only through a server-side command that validates tenant, permissions, document type, series, taxes, customer constraints and line totals.
- Consuming a fiscal number should be atomic with final document snapshot creation and audit event recording.
- A numbered document can be voided/inutilized only through an auditable event that preserves the number in sequence.
- `issued` documents cannot return to `draft`.
- `issued` documents cannot be edited in place; changes require cancellation or corrective documents, depending on the legal rule confirmed later.
- e-Fatura submission failure should not erase the issued document; it should move the technical state to `contingency`, `rejected` or `failed`.
- Reprocessing must create a new transmission attempt record and preserve the prior response.
- A rejection cannot be fixed by mutating the immutable original payload unless the confirmed legal/technical flow explicitly allows a controlled replacement before authorization.

## Critical Domain Events

These events should be audit-grade and tenant-scoped:

- `fiscal_document.draft_created`
- `fiscal_document.validated`
- `fiscal_document.issued`
- `fiscal_document.number_assigned`
- `fiscal_document.snapshot_created`
- `fiscal_document.submission_queued`
- `fiscal_document.sent_to_efatura`
- `fiscal_document.middleware_endpoint_resolved`
- `fiscal_artifact.stored`
- `fiscal_artifact.accessed`
- `fiscal_document.authorized`
- `fiscal_document.rejected`
- `fiscal_document.contingency_entered`
- `fiscal_document.retry_scheduled`
- `fiscal_document.retry_exhausted`
- `fiscal_document.corrective_document_created`
- `fiscal_document.cancel_requested`
- `fiscal_document.cancelled`
- `dfe_event.request_created`
- `dfe_event.payload_generated`
- `dfe_event.transmission_attempted`
- `dfe_event.accepted`
- `dfe_event.rejected`
- `fiscal_number.range_inutilization_requested`

The SSD already names sale document creation, certification, e-Fatura sending, authorization and rejection as relevant domain events. The event names above are a proposed NOVA-ERP vocabulary, not yet a final schema contract.

Source: [[2026-05-26 - SSD NOVA-ERP]]

## Permission Boundaries

Minimum permission boundaries for the module:

- create and edit drafts;
- issue fiscal documents;
- issue invoice-receipts or documents with immediate treasury impact;
- create corrective documents;
- cancel documents where legally allowed;
- view e-Fatura technical responses;
- reprocess rejected or contingency documents;
- configure fiscal series and document types;
- configure e-Fatura credentials/certificate metadata;
- view/export audit logs.

Issuing, cancelling, reprocessing and configuring certificates should not be bundled into the same generic "sales admin" permission. They carry different fiscal and security risk.

Related: [[Permissoes e Auditoria ERP]]

## MVP Acceptance Criteria

For the first sellable release, the module is acceptable only if:

- every fiscal document belongs to exactly one tenant;
- users cannot read, issue, reprocess or configure documents outside their tenant;
- fiscal series are tenant-scoped and cannot silently skip or reuse numbers without an auditable reason;
- issued fiscal documents become immutable in the normal edit path;
- document totals are calculated server-side and stored in an immutable issued snapshot;
- e-Fatura submission is represented by real domain records/jobs, not fake UI buttons;
- XML generation is validated against the official XSD package before submission;
- signed XML and submitted Deflate ZIP metadata are preserved with audit-grade hashes/storage references;
- raw signed XML, ZIP archives and response bodies are kept in private storage with server-mediated access;
- `IssueReasonCode`, `RappelPeriod`, DFE references, official contingency fields and repository code are represented as structured data;
- every submission attempt stores status, timestamp, actor/system origin, retry count and response summary;
- contingency documents are visible, retryable and auditable;
- rejection reasons are preserved and surfaced in a usable operator workflow;
- certificate and credential handling stores only metadata/reference in normal domain tables;
- raw PFX/private keys/passphrases are not stored in ordinary tables or exposed to tenant UI;
- destructive changes to customers, NIFs, products or tax settings are blocked or controlled when certified/issued documents depend on them.

Source: [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]

## Non-MVP Until Legal Confirmation

These should not be improvised in the foundation release:

- full legal certification claim for all e-Fatura document types;
- autofaturacao unless the product flow, seller authorization lifecycle and `SelfBilling` XML contract are explicit;
- automatic tenant certificate onboarding that mutates middleware production configuration without approval;
- complex cancellation/replacement flows before v11.0 event schemas and current legal rules are ingested;
- public exposure of raw DNRE/middleware payloads to ordinary operators;
- accounting finalization rules that depend on unresolved fiscal/legal interpretation.

The foundation release can still be "e-Fatura-ready" if it preserves the correct domain shape, state machine, secure configuration boundary, transmission logs and retry architecture.
