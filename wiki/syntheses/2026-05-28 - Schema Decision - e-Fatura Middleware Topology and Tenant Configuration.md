---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, efatura, middleware, tenancy, security]
sources: ["[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[Supabase Deployment]]", "[[Configuracao ERP]]", "[[Contradiction - Middleware URL Scope]]"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Configuracao ERP]]", "[[Supabase Deployment]]", "[[Permissoes e Auditoria ERP]]"]
confidence: medium
---

# Schema Decision - e-Fatura Middleware Topology and Tenant Configuration

## Decision

NOVA-ERP should use a hybrid e-Fatura middleware topology:

- one default middleware endpoint per runtime environment;
- tenant-scoped e-Fatura emitter configuration, readiness state, credential metadata and certificate references;
- optional tenant endpoint override only as a platform-admin controlled exception, not as a normal tenant setting.

This resolves the apparent conflict between "tenant-scoped middleware URL" and "one `MIDDLEWARE_URL` per environment" as a layered configuration model:

- environment owns network endpoint defaults;
- tenant owns fiscal emitter identity and readiness;
- platform operations owns middleware registration, certificate/keystore sync and endpoint override approval.

Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

## Scope

- Module: [[Configuracao ERP]], [[Faturacao Eletronica]], [[e-Fatura Cabo Verde]].
- Runtime: Supabase Edge Functions and the DNRE/e-Fatura middleware.
- Workflows affected: tenant onboarding, e-Fatura readiness checks, certificate upload/rotation, DFE/event submission, contingency retry and middleware health checks.
- Tenancy boundary: tenant configuration is tenant-scoped; endpoint defaults and override approval are platform-scoped.

## Source Basis

[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] says NOVA-ERP should never hardcode the middleware URL and should keep dynamic, persistent, tenant-aware middleware configuration.

[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] says the same middleware executable runs in dev/staging/production and NOVA-ERP can switch environments by changing `MIDDLEWARE_URL`. The same source also says each tenant/emitter must be added to middleware configuration and certificate/keystore state.

The strongest interpretation is not either/or. URL routing and tenant fiscal identity have different ownership and risk profiles.

## Configuration Layers

### Environment Integration Defaults

Environment-owned, platform-controlled configuration:

- `environment`: local, staging, production;
- `default_middleware_url`;
- `repository_mode`: test, homologacao or production context where applicable;
- network reachability policy;
- TLS/self-signed handling policy;
- health-check endpoint;
- active/disabled flag.

Storage location: Supabase Edge Function secrets for the runtime default, plus an internal platform configuration table if the product needs visibility.

Security rule: tenant users cannot edit these values.

### Tenant e-Fatura Settings

Tenant-owned fiscal/integration readiness configuration:

- tenant id;
- emitter NIF;
- emitter legal name;
- repository code;
- e-Fatura onboarding status;
- emitter registration status in middleware/PE;
- allowed DFE/event capabilities;
- last health check status;
- certificate metadata reference;
- current readiness blocker list.

Storage location: tenant-scoped configuration tables with RLS and explicit permissions.

Security rule: tenant admins can manage allowed business inputs and request onboarding, but cannot view raw secrets or directly mutate production middleware config.

### Tenant Middleware Override

Exception-only configuration:

- `middleware_endpoint_override`;
- override reason;
- approved by platform actor;
- effective period;
- status;
- audit evidence.

Storage location: restricted platform-admin table or tenant integration table fields hidden from ordinary tenant admins.

Security rule: ordinary tenant admins must not be able to redirect fiscal traffic to arbitrary middleware URLs.

## Candidate Data Model

### `efatura_middleware_environments`

- Key fields: `id`, `environment`, `default_endpoint_ref`, `repository_context`, `network_policy`, `tls_policy`, `status`, `last_health_check_at`.
- Ownership: platform.
- Notes: actual secrets stay in Supabase secrets or approved secret manager; table may store references/labels, not secret values.

### `tenant_efatura_settings`

- Key fields: `id`, `tenant_id`, `emitter_tax_id`, `emitter_name`, `repository_code`, `onboarding_status`, `middleware_registration_status`, `certificate_ref_id`, `readiness_status`, `last_ready_at`.
- Ownership: tenant-scoped, but sensitive transitions require elevated permission.
- Notes: used by issue/submit readiness gates.

### `tenant_efatura_middleware_bindings`

- Key fields: `id`, `tenant_id`, `environment_id`, `endpoint_mode`, `endpoint_override_ref`, `override_status`, `approved_by`, `approved_at`, `reason`.
- Ownership: platform-controlled.
- Notes: `endpoint_mode` defaults to `environment_default`; `tenant_override` is exceptional.

### `tenant_efatura_onboarding_jobs`

- Key fields: `id`, `tenant_id`, `requested_by`, `job_type`, `status`, `middleware_environment_id`, `input_summary_json`, `result_summary_json`, `started_at`, `finished_at`.
- Ownership: platform/service.
- Notes: represents controlled sync into middleware `application.properties`, emitter groups and keystore.

### `tenant_certificate_refs`

- Key fields: `id`, `tenant_id`, `emitter_tax_id`, `storage_ref`, `fingerprint`, `valid_from`, `valid_to`, `status`, `rotation_due_at`.
- Ownership: tenant-scoped with restricted write/read.
- Notes: never store raw PFX/private key material in ordinary tables.

## State Model

Recommended tenant e-Fatura readiness states:

- `not_configured`: tenant has no e-Fatura setup.
- `configured`: required metadata exists but not verified.
- `pending_platform_onboarding`: tenant requested middleware/certificate setup.
- `onboarding_in_progress`: platform/service is updating middleware and keystore.
- `ready_test`: tenant can submit in test/homologation context.
- `ready_production`: tenant can submit in production context.
- `blocked`: readiness gate failed.
- `suspended`: platform disabled e-Fatura for the tenant.

Recommended middleware binding modes:

- `environment_default`;
- `tenant_override_pending_approval`;
- `tenant_override_active`;
- `tenant_override_disabled`.

## Edge Function Runtime Rule

DFE/event submission Edge Functions should:

1. authenticate the user or system job;
2. derive tenant context server-side;
3. load tenant e-Fatura readiness and fiscal settings;
4. resolve middleware endpoint from the environment default unless an approved tenant override exists;
5. verify the tenant is registered/ready for the selected repository;
6. submit to middleware using server-side secrets/headers;
7. persist request/response evidence and audit events.

The frontend should never send a middleware URL, transmitter key, client secret or certificate material to the submission path.

## Security Consequences

- Avoids tenant-controlled endpoint injection for fiscal traffic.
- Allows shared middleware per environment while keeping tenant-level emitter governance.
- Supports future per-tenant/per-region middleware deployments without rewriting fiscal modules.
- Requires platform operations workflow for onboarding, certificate import and middleware restart/sync.
- Requires clear separation between tenant-visible readiness status and platform-only secret/configuration state.

## Alternatives Considered

- Alternative: one URL field editable by each tenant.
  Why not: creates endpoint-injection risk and lets ordinary tenant admins redirect fiscal traffic outside approved infrastructure.

- Alternative: hardcoded `MIDDLEWARE_URL` only.
  Why not: prevents tenant-aware onboarding/readiness and creates future migration pain if production topology needs multiple middleware instances.

- Alternative: one middleware instance per tenant from day one.
  Why not: operationally heavier than current evidence requires; preserve this as future topology, not MVP default.

## MVP Boundary

MVP should implement:

- environment default endpoint secret;
- tenant e-Fatura readiness/settings table;
- certificate metadata/reference table;
- service-side endpoint resolution;
- readiness gates before DFE/event submission;
- health-check status and audit events;
- platform-admin-only override shape, even if UI is not exposed.

MVP should not expose:

- tenant self-service endpoint URL editing;
- raw client secrets/private keys;
- automatic production middleware mutation without platform approval;
- public middleware port or browser-side middleware calls.

## Validation Plan

- Test: tenant user cannot update environment middleware endpoint.
- Test: tenant A cannot read tenant B e-Fatura settings/certificate refs.
- Test: submission uses environment default when no approved override exists.
- Test: pending/unapproved override is ignored by submission.
- Test: tenant without `ready_test` or `ready_production` cannot submit DFE/event payloads.
- Test: Edge Function logs/audit preserve actor, tenant, endpoint mode and readiness decision without exposing secrets.

## Open Questions

- Does the DNRE middleware support emitter groups for production exactly as described in the project middleware guide?
- Should tenant onboarding sync to middleware be automatic after approval, or a supervised platform runbook?
- Which secret manager/storage pattern is approved for PFX certificates, keystores, transmitter keys and client secrets?
- Should the first release include a platform admin UI for endpoint overrides or keep it migration/API-only?
