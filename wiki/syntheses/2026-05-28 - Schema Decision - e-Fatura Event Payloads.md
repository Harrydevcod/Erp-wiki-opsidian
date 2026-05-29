---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, efatura, events, compliance]
sources: ["[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]"]
related: ["[[NOVA-ERP]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[Permissoes e Auditoria ERP]]"]
confidence: high
---

# Schema Decision - e-Fatura Event Payloads

## Decision

NOVA-ERP should model e-Fatura events as their own signed XML payload and transmission lifecycle, separate from ordinary DFE issuance payloads.

The current official XSD package exposes an `Event` root alongside `Dfe`. In the package inspected on 2026-05-28, the event type vocabulary is:

- `FDC` - Fiscal Document Cancellation, used for cancelamento/anulacao de DFE.
- `UDN` - Unused Document Number, used for inutilizacao de numero de documento.

This means cancellation/anulation and unused-number flows are not just internal document state changes. They require an official e-Fatura event payload, XSD validation, signature, repository context, transmission attempt history and audit evidence.

Source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]

## Scope

- Module: [[Faturacao Eletronica]] / [[e-Fatura Cabo Verde]].
- Workflows affected: cancellation/anulation of authorized or submitted DFEs, inutilization of unused fiscal numbers, audit history, fiscal sequence integrity and operator permissions.
- Tenancy boundary: every event request, payload, validation result, transmission attempt and response must be tenant-scoped.
- Legal boundary: this decision captures the current technical event schema. It does not by itself resolve all legal conditions for when cancellation, anulation or number inutilization is allowed.

## Source Basis

The XSD package contains:

- `CV_EFatura_MainElements_v1.0.xsd`, which declares `Dfe` and `Event` as root elements.
- `CV_EFatura_MainTypes_v1.0.xsd`, which defines `ctEvent`.
- `CV_EFatura_Types_v1.0.xsd`, which defines `stEventTypeCode` with `FDC` and `UDN`.
- `99 Event.xml`, an official event example.

The v11.0 manual states that event submission follows a DFE-like flow: generate XML, compress with ZIP Deflate and submit through the `event` resource.

Source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]

## Event XML Contract

The event root has required attributes:

- `Id`: event id, structurally distinct from DFE IUD.
- `Version`: document version.
- `EventTypeCode`: official event type code, currently `FDC` or `UDN`.

The event body requires:

- `EmitterTaxId`;
- `IssueDateTime`;
- `IssueReasonDescription`;
- either one or more `IUD` values, or a sequence-range structure for unused numbers;
- `Transmission`;
- `RepositoryCode`;
- signature, depending on enveloped or internally detached signature mode.

The sequence-range branch includes:

- optional `Year`;
- `LedCode`;
- `Serie`;
- `DocumentTypeCode`;
- `DocumentNumberStart`;
- `DocumentNumberEnd`.

Implementation implication: NOVA-ERP needs first-class event payload generation, not a boolean `cancelled` flag on the fiscal document.

## FDC Semantics

`FDC` is the technical event type for cancelamento/anulacao de DFE.

The current XSD allows the event to carry one or more `IUD` values. The package changelog records that `FDC` was updated to allow more than one IUD.

Implementation implication:

- cancellation/anulation requests should be represented as event records linked to the affected fiscal documents;
- multiple IUDs may be technically valid in one event, but NOVA-ERP should decide whether the UI permits bulk cancellation or only creates one event per operator action;
- original fiscal documents must remain immutable and linked to the event result;
- business state should move only through an auditable event outcome, not direct mutation.

## UDN Semantics

`UDN` is the technical event type for inutilizacao de numero de documento.

The current XSD branch for unused numbers identifies a range by year, LED, series, document type, start number and end number. The XSD changelog records that `DocumentTypeCode` was added to `UDN` events.

Implementation implication:

- unused-number handling must be modeled as a fiscal number event/range, not as deletion of documents or silent series counter changes;
- fiscal series counters need enough metadata to prove which numbers were issued, unused, reserved, failed or officially inutilized;
- number-range inutilization should require elevated permission and operator justification.

## Data Model Additions

Add or reserve these objects beside the DFE payload/transmission model:

### `dfe_event_requests`

- Key fields: `id`, `tenant_id`, `event_type_code`, `requested_by`, `reason_description`, `business_status`, `fiscal_status`, `technical_status`, `created_at`.
- Relationships: has many target documents or number ranges; has payloads, validation results and transmission attempts.
- Constraints: append-only status history; cannot silently delete after submission.
- RLS/security: tenant-scoped; create requires explicit fiscal cancellation/inutilization permission.

### `dfe_event_targets`

- Key fields for `FDC`: `id`, `tenant_id`, `event_request_id`, `fiscal_document_id`, `iud`.
- Key fields for `UDN`: `id`, `tenant_id`, `event_request_id`, `year`, `led_code`, `serie`, `document_type_code`, `document_number_start`, `document_number_end`.
- Constraints: target shape must match `event_type_code`; prevent overlapping UDN ranges for the same tenant/emitter/year/LED/type.

### `dfe_event_payloads`

- Key fields: `id`, `tenant_id`, `event_request_id`, `schema_version`, `xsd_package_version`, `event_id`, `event_type_code`, `artifact_ref_id`, `xml_hash`, `signature_mode`, `signed_at`.
- Constraints: preserve final signed XML; do not mutate submitted payloads.

### `dfe_event_validation_results`

- Key fields: `id`, `tenant_id`, `event_payload_id`, `validator`, `xsd_package_version`, `status`, `errors_json`, `warnings_json`, `validated_at`.
- Constraints: append-only.

### `dfe_event_transmission_attempts`

- Key fields: `id`, `tenant_id`, `event_request_id`, `event_payload_id`, `attempt_number`, `repository_code`, `endpoint_base_url`, `request_headers_json`, `zip_storage_path`, `zip_hash`, `response_status`, `response_body_storage_path`, `response_summary`, `technical_status`, `started_at`, `finished_at`.
- Constraints: retries create new attempts and never overwrite prior response evidence.

## State And Events

Recommended event request states:

- `draft`: operator has prepared a cancellation/anulation or UDN request.
- `validated`: XML and local business constraints passed.
- `signed`: signed event XML exists.
- `submitted`: middleware/PE submission attempt was made.
- `accepted`: event was accepted/authorized by the platform.
- `rejected`: platform or local validation rejected the event.
- `failed`: technical failure requiring retry or manual action.

Recommended audit events:

- `dfe_event.request_created`
- `dfe_event.target_added`
- `dfe_event.payload_generated`
- `dfe_event.validation_completed`
- `dfe_event.signed`
- `dfe_event.transmission_attempted`
- `dfe_event.accepted`
- `dfe_event.rejected`
- `fiscal_number.range_inutilization_requested`
- `fiscal_document.cancellation_requested`

## Security And UX Implications

- Cancellation/anulation and UDN require separate permissions from ordinary document issuance.
- Operators should see readable status and reason history, while raw XML, signatures and response bodies remain restricted.
- Bulk `FDC` should be treated as a riskier workflow than single-document cancellation because one event can target multiple IUDs.
- `UDN` should require strong validation against local fiscal series state before event XML is generated.

## Consequences

- Positive: prevents deletion-style cancellation, preserves fiscal evidence, supports official event XML and keeps number-sequence integrity auditable.
- Tradeoff: adds event-specific tables and UI flows before cancellation can be considered production-grade.
- Migration impact: current coarse `documents.cancelled`/`efatura_logs` style fields are not enough for official event handling.

## Validation Plan

- Test: generate an `FDC` XML fixture using the official event example shape and validate against the XSD package.
- Test: generate a `UDN` XML fixture with year, LED, series, document type and number range and validate against the XSD package.
- Test: `FDC` cannot be requested by a user without cancellation permission.
- Test: `UDN` cannot overlap already issued or already inutilized numbers.
- Test: retrying an event creates a new transmission attempt without overwriting the first response.

## Open Questions

- Which current legal rules decide when a DFE can be cancelled versus corrected by NCE/NDE/DVE?
- Should NOVA-ERP permit multi-IUD `FDC` events in the product UI or restrict the first release to one IUD per request?
- Which PE/middleware response fields should become structured columns versus archived response body?
- Should `UDN` be available in MVP, or only after full fiscal series administration is mature?
