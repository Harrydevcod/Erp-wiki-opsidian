---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-29
tags: [supabase, deployment, edge-functions, database, security, rls]
sources: ["[[2026-05-28 - Supabase Deploy]]", "raw/assets/LOCAL_SETUP.md", "raw/assets/LOCAL_SETUP-Arydson.md", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
related: ["[[NOVA-ERP]]", "[[Supabase]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[Configuracao ERP]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: high
---

# Supabase Deployment

## Purpose

Supabase Deployment is the operational architecture for running the NOVA-ERP backend stack on [[Supabase]]: PostgreSQL schema, migrations, RLS policies, Auth, storage, triggers, Edge Functions, secrets, webhook configuration, frontend environment variables, verification gates and rollback discipline.

## Role In NOVA-ERP

This is a foundation architecture concept. NOVA-ERP's fiscal, commercial, treasury, inventory, reporting and AI workflows depend on Supabase enforcing tenant isolation, permission boundaries, audit logging and secret separation at runtime.

The deployment guide is useful, but it is not enough by itself. A production deployment must prove that migrations apply cleanly, tenant RLS is enforced, storage is private where required, Edge Functions are authorized, secrets are scoped correctly and sensitive service-role operations are attributable to the initiating user and tenant.

Source: [[2026-05-28 - Supabase Deploy]], [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[ERP SaaS Multi-Tenant]], [[Permissoes e Auditoria ERP]]

## Source Basis

- Deployment procedure: [[2026-05-28 - Supabase Deploy]]
- Local setup: `raw/assets/LOCAL_SETUP.md`, `raw/assets/LOCAL_SETUP-Arydson.md`
- Product/runtime intent: [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[NOVA-ERP Product Authority Synthesis]]
- Current database evidence: [[2026-05-28 - DATABASE ER Diagram Snapshot]], [[2026-05-28 - Current Database Snapshot Classification]]
- Security/tenancy boundary: [[ERP SaaS Multi-Tenant]], [[Permissoes e Auditoria ERP]]
- Fiscal/e-Fatura boundary: [[Faturacao Eletronica]], [[e-Fatura Cabo Verde]]

## Deployment Spine

The local source defines this deployment sequence:

1. Authenticate and link the repository to the target Supabase project.
2. Push schema, RLS, policies, triggers and storage with migrations.
3. Optionally include seed data.
4. Configure SQL webhooks that call Edge Functions through `pg_net`.
5. Set Edge Function secrets.
6. Deploy Edge Functions.
7. Configure frontend environment variables with publishable client credentials.

Source: [[2026-05-28 - Supabase Deploy]]

## Design Gates Before Production

- Migration gate: migrations must apply from an empty project and from the expected current release state.
- Drift gate: target project must not contain manual tables/policies/functions outside migrations unless explicitly classified and migrated.
- RLS gate: every tenant-owned table in exposed schemas must have RLS and tenant-aware policies.
- Storage gate: buckets for certificates, fiscal payloads, payroll, payment proofs and attachments must have explicit private policies.
- Edge Function gate: service-role functions must authenticate caller, derive tenant context server-side and preserve actor attribution.
- Secret gate: service role key, webhook secret, AI key, SISP credentials, e-Fatura secrets and certificate material must never reach frontend env vars or committed files.
- Webhook gate: SQL-triggered webhooks must use a dedicated private secret and must target the correct project URL.
- Observability gate: critical background work must have logs, status tables or audit events that are queryable without exposing raw secrets.
- Rollback gate: release procedure must define whether rollback is database migration rollback, feature flag disablement, Edge Function redeploy or tenant-level suspension.

## Environment Model

Minimum environments:

- local: Supabase CLI, Docker Desktop, `.env.local`, local API URL and anon key from `supabase status`;
- staging: clean Supabase project for migration rehearsal, OAuth redirect validation, Edge Function testing and e-Fatura test/homologation paths;
- production: dedicated Supabase project with controlled secrets, migrations only, private storage posture, monitored Edge Functions and explicit release approvals.

The current raw setup confirms the app is intended to run as a normal React + Supabase application outside Lovable.

Evidence: `raw/assets/LOCAL_SETUP.md`

## Artifact Availability Status

As of 2026-05-29, this vault does not contain the actual `supabase/migrations`, `supabase/functions` or `supabase/seed.sql` artifacts referenced by the deployment and local setup guides.

This means Supabase Deployment can be specified and gated here, but implementation-grade SQL/RLS/storage/Edge Function review is blocked until the application repository, a migration bundle or a Supabase schema/policy dump is available.

Filed in [[2026-05-29 - Supabase Implementation Artifact Gap]].

## Key Boundary

Frontend configuration should use:

- `VITE_SUPABASE_URL`;
- `VITE_SUPABASE_PUBLISHABLE_KEY`;
- `VITE_SUPABASE_PROJECT_ID`.

Server/Edge Function secrets may include:

- `SUPABASE_SERVICE_ROLE_KEY`;
- `EDGE_FUNCTION_WEBHOOK_SECRET`;
- `CRON_SECRET`;
- AI provider keys;
- payment/SISP credentials;
- e-Fatura/middleware credentials where applicable.

The deployment source states that legacy anon JWT keys may still be needed for some Edge Function compatibility flows, but the frontend should prefer publishable keys. NOVA-ERP must keep that compatibility detail from becoming a confused security model.

Source: [[2026-05-28 - Supabase Deploy]]

## RLS And Tenant Isolation Release Gate

For NOVA-ERP, Supabase RLS is a release blocker, not a later hardening task.

Required posture:

- all tenant-owned domain tables include `tenant_id`;
- tenant membership drives policy access;
- permissions are evaluated in tenant context;
- policies are tested for positive and negative cases;
- tenant A cannot read, update, delete or infer tenant B records;
- views exposed through the API must not bypass tenant isolation;
- service-role bypasses are isolated behind Edge Functions and audited.

Related: [[ERP SaaS Multi-Tenant]], [[Permissoes e Auditoria ERP]]

## Edge Function Boundary

Edge Functions are expected for tasks that should not run in the browser:

- e-Fatura payload generation/submission and middleware calls;
- webhook receivers and SQL-triggered notifications;
- AI calls;
- payment/SISP interactions;
- cron-like background jobs;
- service-role operations that require database privileges beyond the user session.

Every Edge Function that touches tenant data should:

- authenticate the user or verify the webhook/cron secret;
- derive tenant context server-side;
- verify membership/permission/entitlement;
- write domain status and audit events;
- avoid returning raw secrets, raw fiscal payloads or privileged error details to the frontend.

## Storage Boundary

Supabase Storage is implementation evidence in the current database snapshot, but actual bucket policies still require inspection.

High-risk storage classes:

- e-Fatura certificates and keystore artifacts;
- signed DFE XML and Deflate ZIP archives;
- DNRE/middleware raw response bodies;
- payment proofs and bank documents;
- payroll artifacts and payslips;
- company assets and logos.

The default posture should be private buckets with explicit signed-access or server-mediated retrieval. Public buckets should be limited to deliberate non-sensitive assets.

For e-Fatura specifically, [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] chooses private fiscal evidence storage for signed XML, submitted ZIPs and raw responses, with metadata/hashes in PostgreSQL. PFX/private keys/passphrases remain outside ordinary tables and normal tenant UI.

## Secrets And Rotation Boundary

Production deployment needs a secrets inventory, owner and rotation policy before go-live.

Minimum classes:

- Supabase service role key;
- legacy anon JWT key where compatibility requires it;
- publishable key for frontend;
- Edge Function webhook secret;
- cron secret;
- Resend/API email key;
- AI provider key and base URL;
- SISP payment credentials;
- e-Fatura middleware/transmitter credentials;
- certificate storage/keystore secrets.

Secrets should be stored in Supabase secrets or an approved secret manager, not in wiki pages, committed env files or frontend-exposed variables.

## Database Drift And Migration Boundary

[[2026-05-28 - Current Database Snapshot Classification]] says the current schema is useful evidence but not target architecture. Deployment must therefore avoid promoting accidental current tables as final product architecture.

Rules:

- target schema changes must be migration-controlled;
- current tables are classified before reuse;
- manual dashboard edits in Supabase are treated as drift;
- database deploy rehearsal should run against a clean project;
- production data migration requires a separate migration plan, not just `db push`.

## Fiscal And e-Fatura Deployment Notes

Fiscal/e-Fatura workloads make deployment higher risk:

- e-Fatura requires secure handling of certificates, client secrets, transmitter keys and raw XML/ZIP evidence;
- DFE payloads and response bodies should be stored with restricted access and audit-grade references;
- retry/contingency jobs need observable state and duplicate prevention;
- middleware endpoint strategy follows [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]: environment default endpoint, tenant readiness/configuration and platform-admin-only override;
- production e-Fatura rollout must be tested against the correct DNRE repository/middleware environment before legal use.

Related: [[Faturacao Eletronica]], [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]

## Candidate Deployment Checklist

- Supabase project linked to the correct environment.
- Migrations applied successfully from a clean state.
- Seed strategy selected intentionally: demo seed only outside production unless approved.
- RLS enabled and tested on tenant-owned tables.
- Storage buckets created with reviewed policies.
- Edge Function webhook URL/key/secret configured and validated.
- Edge Function secrets set in the target project.
- Edge Functions deployed and smoke-tested.
- Frontend env vars use publishable key, not service role key.
- OAuth redirect URLs configured for the environment.
- Critical background functions have logs/status/audit records.
- e-Fatura/payment/AI functions disabled by feature flag unless their secrets and policies are ready.
- e-Fatura Edge Functions resolve middleware endpoint server-side and ignore frontend-provided endpoint values.
- Rollback/disable plan documented for the release.

## MVP Acceptance Criteria

For the first sellable release, Supabase Deployment is acceptable only if:

- a fresh Supabase project can be provisioned from migrations and documented secrets without manual database reconstruction;
- tenant isolation is enforced by RLS and covered by negative tests;
- service-role usage exists only in Edge Functions/server paths with explicit authorization checks;
- storage policies prevent public access to fiscal, certificate, payment, payroll and private tenant artifacts;
- frontend receives only publishable/public-safe variables;
- Edge Function webhook secrets match SQL-side and function-side configuration;
- deployment can identify the running project/environment and avoid sending jobs to the wrong project;
- critical Edge Function failures are visible to operators;
- production seed/demo data cannot accidentally pollute a customer tenant;
- rollback or feature-disablement exists for e-Fatura, AI and payment integrations.

## Non-MVP Until Confirmed

- Fully automated production tenant certificate deployment into middleware/keystore.
- Multi-region Supabase architecture.
- Self-hosted Supabase production topology.
- Full external SIEM integration.
- Automated database rollback for every migration class.
- Public tenant admin access to raw Edge Function logs, raw e-Fatura payloads or secret metadata.

## Open Questions

- Which command set becomes the canonical release script?
- Which Supabase advisors/security checks must run before production?
- Which RLS test suite proves cross-tenant isolation?
- Which functions truly require service-role access?
- Should webhook secret configuration be automated as a repeatable deployment step?
- Which legal retention period applies to e-Fatura XML, ZIP, response bodies and customer-facing renders?
- Which production secret manager or keystore flow is approved for certificate private-key material?
- How should Supabase deployment interact with SaaS plan entitlements and tenant suspension?

## Next Ingestion Targets

- Actual SQL migrations, RLS policies, storage policies and Edge Functions in the implementation repository. Current status: blocked by [[2026-05-29 - Supabase Implementation Artifact Gap]].
- Supabase security/changelog docs before real implementation.
- `raw/assets/LOCAL_SETUP-Arydson.md` for e-Fatura OAuth callback details.
- Current production operations plan for secrets rotation and incident response.
