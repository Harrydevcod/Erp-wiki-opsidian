---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, efatura, faturacao, compliance]
sources: ["[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - SSD NOVA-ERP]]"]
related: ["[[NOVA-ERP]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[Fiscalidade Cabo Verde]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: high
---

# Schema Decision - e-Fatura DFE Payload and Transmission

## Decision

NOVA-ERP should model e-Fatura as a fiscal-document integration subsystem with separate records for fiscal documents, immutable fiscal snapshots, generated DFE payloads, XSD validation results, transmission batches, transmission attempts, references, contingency, self-billing and signed XML/archive storage. It must not collapse e-Fatura into a single status column on `documents`.

This is a provisional schema decision for implementation planning. It is strong enough to guide table boundaries, but not yet a final migration spec.

Companion decision: [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]] covers official event payloads for cancellation/anulation (`FDC`) and unused-number inutilization (`UDN`).

Companion decision: [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] covers where signed XML, ZIP archives, raw responses, certificate metadata and private-key material should live.

## Scope

- Module: [[Faturacao Eletronica]] / [[e-Fatura Cabo Verde]].
- Tables/objects: fiscal documents, series, snapshots, DFE payloads, validations, batches, attempts, references, contingency, self-billing, certificates, storage references.
- Workflows affected: issuing, numbering, XML generation, local validation, signature, submission, authorization, rejection, contingency, retry, correction references and audit.
- Tenancy boundary: every business/fiscal/integration record must be tenant-scoped except controlled global reference tables.

## Source Basis

- Product source: [[2026-05-26 - SSD NOVA-ERP]], [[Faturacao Eletronica]].
- Compliance source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[Fiscalidade Cabo Verde]].
- Technical source: [[2026-05-28 - Current Database Snapshot Classification]], [[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]].
- Inference: the v11.0/XSD contract requires several durable integration artifacts that the current ER snapshot does not model explicitly.

## Context

The current ER snapshot has `documents`, `document_items`, `document_series`, `efatura_logs`, `efatura_settings` and an `efatura-certificates` bucket. Those are useful signals, but they are not enough for the official v11.0 e-Fatura contract.

The official contract requires XML generation, XSD validation, digital signature, IUD/LED/repository identifiers, Deflate ZIP packaging, synchronous authorization attempts, middleware/API headers, contingency fields, references, self-billing and correction/rappel structures. These concerns have different lifecycles, access rules and audit requirements, so they need separate records.

## Data Model

### `fiscal_documents`

- Key fields: `id`, `tenant_id`, `document_type_code`, `business_document_type`, `series_id`, `document_number`, `iud`, `issue_date`, `issue_time`, `business_state`, `fiscal_state`, `technical_state`, `customer_id`, `currency`, totals, `created_by`.
- Relationships: has many lines, snapshots, references, payloads, transmission attempts and audit events.
- Constraints: unique fiscal number by tenant/emitter/year/LED/type/number; immutable after issue except controlled correction flows.
- Indexes: tenant/date, tenant/state, tenant/document number, IUD.
- RLS/security: tenant isolation; issue/correct/cancel/reprocess require explicit permissions.

### `fiscal_series`

- Key fields: `id`, `tenant_id`, `led_code`, `series_code`, `document_type_code`, `year`, `current_number`, `repository_code`, `active`.
- Relationships: belongs to tenant/emitter configuration; used by fiscal documents.
- Constraints: no silent reset or reuse; annual sequence boundary; controlled deactivation.
- RLS/security: tenant admin/fiscal admin only.

### `fiscal_document_snapshots`

- Key fields: `id`, `tenant_id`, `fiscal_document_id`, `snapshot_version`, `payload_json`, `totals_json`, `hash`, `created_at`.
- Relationships: one or more per fiscal document, with final issue snapshot immutable.
- Constraints: final snapshot immutable; hash required.
- RLS/security: read restricted to fiscal/audit roles; no normal update path.

### `dfe_payloads`

- Key fields: `id`, `tenant_id`, `fiscal_document_id`, `schema_version`, `xsd_package_version`, `xml_storage_path`, `xml_hash`, `signature_mode`, `signed_at`, `iud`, `document_type_code`.
- Relationships: belongs to fiscal document; has validation results; can be included in transmission batches.
- Constraints: preserve generated/signed XML; do not mutate submitted payloads.
- RLS/security: raw XML is sensitive fiscal data; ordinary operators should see summarized status, not unrestricted payload.

### `dfe_validation_results`

- Key fields: `id`, `tenant_id`, `dfe_payload_id`, `validator`, `xsd_package_version`, `status`, `errors_json`, `warnings_json`, `validated_at`.
- Relationships: belongs to DFE payload.
- Constraints: validation result is append-only.
- RLS/security: fiscal/integration operators only.

### `dfe_transmission_batches`

- Key fields: `id`, `tenant_id`, `repository_code`, `transport`, `endpoint_base_url`, `zip_storage_path`, `zip_hash`, `file_manifest_json`, `created_at`.
- Relationships: has many payloads/attempts.
- Constraints: ZIP archive metadata is immutable after submission.
- RLS/security: service role writes; fiscal operators see summarized metadata.

### `dfe_transmission_attempts`

- Key fields: `id`, `tenant_id`, `batch_id`, `fiscal_document_id`, `attempt_number`, `request_headers_json`, `response_status`, `response_body_storage_path`, `response_summary`, `started_at`, `finished_at`, `technical_status`.
- Relationships: belongs to batch and optionally fiscal document.
- Constraints: append-only; every retry creates a new attempt.
- RLS/security: no destructive updates; response body may contain sensitive fiscal/technical information.

### `dfe_references`

- Key fields: `id`, `tenant_id`, `fiscal_document_id`, `reference_type`, `referenced_iud`, `old_document_number`, `payment_amount`, `tax_json`, `reason_code`, `reason_description`.
- Relationships: belongs to fiscal document; may reference another fiscal document.
- Constraints: corrective/devolutive documents require valid references according to document type.
- RLS/security: tenant-scoped.

### `dfe_contingency_records`

- Key fields: `id`, `tenant_id`, `fiscal_document_id`, `issue_mode`, `reason_type_code`, `iuc`, `led_code`, `issue_date`, `issue_time`, `dfa_status`.
- Relationships: belongs to fiscal document.
- Constraints: required when issue mode is not online; preserve official fields separately from retry queue state.
- RLS/security: issue/reprocess permissions.

### `dfe_self_billing_authorizations`

- Key fields: `id`, `tenant_id`, `seller_tax_id`, `buyer_tax_id`, `authorization_id`, `authorization_code`, `request_payload_json`, `response_json`, `status`, `requested_at`.
- Relationships: referenced by eligible DFE payloads.
- Constraints: not part of MVP unless product flow is explicit.
- RLS/security: restricted; includes taxpayer identity and authorization evidence.

### `dfe_rappel_periods`

- Key fields: `id`, `tenant_id`, `fiscal_document_id`, `start_date`, `end_date`.
- Relationships: belongs to NCE with `IssueReasonCode=DRP`.
- Constraints: only valid for NCE/rappel.
- RLS/security: tenant-scoped.

### `digital_certificate_refs`

- Key fields: `id`, `tenant_id`, `emitter_tax_id`, `storage_ref`, `certificate_fingerprint`, `valid_from`, `valid_to`, `status`.
- Relationships: used by integration configuration/signing process.
- Constraints: metadata/reference only in domain table; raw secret material stays in controlled storage/secret system.
- RLS/security: fiscal integration admin only; no casual UI exposure.

## State And Events

- State: `draft`, `issued`, `authorized`, `rejected`, `contingency`, `retrying`, `failed` remain separated between business/fiscal/technical axes.
- Event: `fiscal_document.number_assigned`, `fiscal_document.snapshot_created`, `dfe.payload_generated`, `dfe.validation_completed`, `dfe.transmission_attempted`, `dfe.authorized`, `dfe.rejected`, `dfe.contingency_entered`.
- Transition rule: issuing consumes number and creates immutable snapshot; DFE generation and transmission happen after issue; each PE/middleware call creates an attempt; retries never overwrite prior attempts.

## Alternatives Considered

- Alternative: keep one `documents` table with `efatura_status`.
  Why not: cannot represent XML payload, XSD package version, signature, ZIP batch, multiple attempts, raw responses, official contingency fields or correction references.

- Alternative: one generic `efatura_logs` table with JSON blobs.
  Why not: too weak for audit, querying, retry logic, security policy and fiscal evidence.

- Alternative: direct mutation of document after rejection.
  Why not: conflicts with immutable snapshot and audit posture; corrective/replacement flows need explicit legal/technical confirmation.

## Consequences

- Positive: preserves fiscal evidence, supports retries, enables XSD validation, protects raw payloads and matches v11.0 concepts.
- Tradeoff: more tables and stricter lifecycle rules than a simple invoice module.
- Migration impact: current `documents`, `document_series`, `efatura_logs`, `efatura_settings` and `efatura-certificates` require classification/migration, not blind reuse.
- Operational impact: support/admin tooling must distinguish business status, fiscal authorization and integration attempt status.

## Validation Plan

- Test: generate official-example-inspired XML fixtures per DFE type and validate against the 2024-05-27 XSD package.
- Fixture/source: [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]].
- Failure mode: invalid XML never creates a submitted transmission batch.
- Test: retry creates a second `dfe_transmission_attempt`, preserving the first response.
- Failure mode: no retry may overwrite prior request/response evidence.
- Test: tenant A cannot read DFE payloads, validation results, transmissions or certificates for tenant B.
- Failure mode: RLS regression fails release gate.

## Open Questions

- Should first implementation name the business header `fiscal_documents`, `sales_documents`, or split commercial and fiscal documents? (Resolved in [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]: split — `commercial_documents` for intent, `fiscal_documents` for the legal record this ADR attaches to.)
- Which current legal rules determine when cancellation/anulation should use `FDC` versus correction through NCE/NDE/DVE?
- Which parts of the event payload model belong in MVP migrations: all `FDC`/`UDN` tables, or only reserved extensibility points?
- Which legal retention period applies to signed XML, ZIP archives and raw responses?
- Which production secret manager or middleware keystore process is approved for certificate private-key material?
- Which tables belong in MVP migrations versus later e-Fatura depth?
