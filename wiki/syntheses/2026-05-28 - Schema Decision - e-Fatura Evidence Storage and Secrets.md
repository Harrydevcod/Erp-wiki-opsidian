---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, efatura, storage, secrets, security]
sources: ["[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]", "[[2026-05-28 - Supabase Deploy]]", "[[Supabase Deployment]]", "[[Configuracao ERP]]"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Configuracao ERP]]", "[[Supabase Deployment]]", "[[Permissoes e Auditoria ERP]]"]
confidence: medium
---

# Schema Decision - e-Fatura Evidence Storage and Secrets

## Decision

NOVA-ERP should split e-Fatura storage into three security classes:

1. Metadata in PostgreSQL tables: hashes, paths, status, timestamps, actor, tenant, schema version, repository and response summaries.
2. Fiscal evidence artifacts in private object storage: signed DFE/event XML, submitted ZIP archives and raw DNRE/middleware response bodies.
3. Secret/private-key material outside normal domain tables and ordinary UI access: PFX/private keys, keystores, transmitter keys, client secrets and service-role credentials.

For MVP, use private Supabase Storage for fiscal evidence artifacts, store only metadata/references in tables, and access raw artifacts only through server-side Edge Functions or short-lived signed URLs after permission checks.

Raw certificate/private-key material should not be stored as normal tenant data. Tenant certificate tables should store metadata and secure references only. The operational target is an approved secret manager, Supabase Vault/Edge Function secrets where appropriate, or middleware-managed keystore state. If NOVA-ERP needs upload/onboarding before that target is implemented, treat uploaded PFX as a temporary encrypted onboarding artifact with restricted platform-admin handling and explicit deletion/retention policy.

Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Supabase Deploy]], Supabase official docs via Context7 on 2026-05-28.

## Source Basis

The e-Fatura v11.0 manual and XSD package require signed XML, XSD validation, ZIP submission, certificate-backed digital signature and preserved transmission evidence.

The Supabase deployment source says fiscal payloads, certificate storage and legal retention are not solved by deployment alone. Supabase documentation says Storage works with Postgres RLS access policies, private files can be served through short-lived signed URLs, and service-role keys are safe only in server/Edge Function contexts and must never be used in the browser.

Evidence: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[2026-05-28 - Supabase Deploy]]

## Storage Classes

### Class A - Queryable Metadata

Store in tenant-scoped PostgreSQL tables:

- DFE/event ids;
- document id;
- schema/XSD package version;
- XML hash;
- ZIP hash;
- storage path/reference;
- response status and response summary;
- repository code;
- validation status;
- attempt number;
- actor/system origin;
- timestamps;
- retention status.

Rationale: metadata must be queryable for workflow, audit, dashboards, retries and support without exposing raw fiscal payloads.

### Class B - Fiscal Evidence Artifacts

Store in private object storage:

- signed DFE XML;
- signed event XML;
- submitted Deflate ZIP archives;
- raw middleware/DNRE response bodies;
- generated PDFs/DFA print artifacts if legally retained as evidence;
- validation reports if large or sensitive.

Access model:

- service role or equivalent server-side access only;
- user access through Edge Function permission checks;
- short-lived signed URLs only for authorized download/view cases;
- no public buckets;
- no raw artifact access from ordinary frontend database reads.

Rationale: these artifacts are sensitive, can be large, must be immutable/auditable and should not bloat operational tables.

### Class C - Secrets And Private-Key Material

Do not store in ordinary application tables:

- PFX/private keys;
- middleware keystore files;
- e-Fatura transmitter keys;
- OAuth client secrets;
- Supabase service role key;
- webhook secrets;
- certificate passphrases.

Store only metadata/reference in domain tables:

- certificate fingerprint;
- issuer/subject where safe;
- validity period;
- emitter NIF;
- status;
- rotation due date;
- secure storage reference;
- onboarding job id.

Operational storage target:

- approved secret manager;
- Supabase Vault/Edge Function secrets for secret values that Edge Functions must read;
- middleware keystore for signing/runtime material;
- private temporary upload storage only during supervised onboarding, with deletion/retention rules.

Rationale: certificate/private-key material can authorize fiscal signatures. It is materially more sensitive than signed XML evidence.

## Candidate Data Model

### `fiscal_artifact_refs`

- Key fields: `id`, `tenant_id`, `artifact_type`, `owner_type`, `owner_id`, `storage_bucket`, `storage_path`, `content_hash`, `content_type`, `size_bytes`, `retention_class`, `created_at`.
- Owner examples: `dfe_payload`, `dfe_event_payload`, `transmission_attempt`, `validation_result`, `dfa_print`.
- Constraint: append-only after finalization.

### `fiscal_artifact_access_events`

- Key fields: `id`, `tenant_id`, `artifact_ref_id`, `actor_id`, `access_type`, `reason`, `granted_by`, `created_at`, `ip_context`.
- Purpose: audit raw artifact reads/downloads.

### `tenant_certificate_refs`

- Key fields: `id`, `tenant_id`, `emitter_tax_id`, `certificate_fingerprint`, `issuer_summary`, `valid_from`, `valid_to`, `status`, `secure_ref`, `rotation_due_at`, `onboarding_job_id`.
- Constraint: metadata only; no raw PFX/private key/passphrase columns.

### `secret_refs`

- Key fields: `id`, `tenant_id`, `secret_type`, `provider`, `secret_name_or_ref`, `status`, `last_rotated_at`, `rotation_due_at`.
- Purpose: reference secrets without exposing values.

### `certificate_onboarding_artifacts`

- Key fields: `id`, `tenant_id`, `certificate_ref_id`, `upload_artifact_ref`, `status`, `uploaded_by`, `approved_by`, `expires_at`, `deleted_at`.
- Purpose: temporary bridge if PFX upload is needed before middleware keystore import.
- Constraint: non-MVP unless a secure upload/delete process exists.

## Storage Buckets

Recommended buckets:

- `fiscal-evidence`: private; signed XML, ZIP, raw response bodies and validation artifacts.
- `fiscal-renders`: private by default; PDFs/DFA/print artifacts where retained.
- `efatura-onboarding-temp`: private, highly restricted and optional; temporary certificate onboarding uploads only.

Avoid using a generic attachments bucket for e-Fatura evidence. Fiscal artifacts need stricter retention, access logs and deletion rules.

## Edge Function Access Rule

Edge Functions that read/write e-Fatura artifacts must:

1. authenticate caller or verify system secret;
2. derive tenant context server-side;
3. check permission and artifact ownership;
4. use service role/secret access only server-side;
5. return summaries by default;
6. generate short-lived signed URLs only for explicit download/view actions;
7. write `fiscal_artifact_access_events` for raw artifact access;
8. never return service-role keys, transmitter keys, client secrets, PFX files or passphrases.

## Retention And Immutability

Default posture:

- submitted/signed XML and ZIP archives are immutable;
- raw responses are append-only;
- hashes are computed before/at storage write;
- deletion is disabled in normal app flows;
- retention status is explicit;
- legal retention duration remains unresolved until current Cabo Verde authority is ingested.

## MVP Boundary

MVP should implement:

- private fiscal evidence bucket;
- metadata/ref tables for signed XML, ZIP and response bodies;
- append-only validation/transmission references;
- certificate metadata table without raw secret columns;
- Edge Function mediated artifact access;
- storage/RLS tests proving tenant isolation;
- audit events for raw artifact access.

MVP should not implement:

- ordinary tenant self-service raw PFX storage;
- public bucket access to fiscal documents;
- browser-side direct service-role access;
- permanent certificate/private-key escrow without an approved secret manager and retention policy;
- deletion of signed/submitted fiscal evidence through normal UI.

## Validation Plan

- Test: tenant A cannot read tenant B fiscal artifact refs or storage objects.
- Test: frontend cannot obtain fiscal artifacts without a server permission check.
- Test: signed URL expiry is short and generated only after permission check.
- Test: raw artifact access creates `fiscal_artifact_access_events`.
- Test: certificate tables reject raw PFX/private key/passphrase columns in schema review.
- Test: Edge Function secrets/service-role keys are not exposed to frontend env vars.

## Open Questions

- Which legal retention period applies to DFE XML, event XML, ZIP archives, DFA/PDF renders and DNRE responses?
- Which secret manager is approved for production PFX/private-key/passphrase storage?
- Should NOVA-ERP retain uploaded PFX after middleware keystore import, or delete it after successful onboarding?
- Should customer-facing invoice PDF/DFA access use the same evidence bucket or a separate render bucket with narrower contents?
