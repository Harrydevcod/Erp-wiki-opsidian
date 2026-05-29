---
type: source
status: active
created: 2026-05-28
updated: 2026-05-28
source_path: raw/assets/SUPABASE_DEPLOY.md
source_type: deployment-guide
author: NOVA-ERP project
published: unknown
ingested: 2026-05-28
tags: [source, supabase, deployment, edge-functions, secrets]
related: ["[[Supabase]]", "[[Supabase Deployment]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]"]
confidence: high
---

# Supabase Deploy

## Source Role

This source defines the operational deployment path for the NOVA-ERP Supabase backend: linking a Supabase project, pushing migrations/seed data, configuring SQL-triggered Edge Function webhooks, setting function secrets, deploying Edge Functions and configuring frontend environment variables.

It is implementation evidence, not a complete production runbook. It must be combined with tenant isolation, RLS, storage, secret-management and rollback gates before production release.

## Summary

The guide assumes the repository already contains Supabase migrations, Edge Functions and seed data. Deployment links a new Supabase project with `supabase link`, applies schema/RLS/policies/triggers/storage with `supabase db push`, optionally includes seed data, configures database webhook helpers for Edge Function calls, sets Edge Function secrets from `.env.functions`, deploys all functions and configures frontend variables.

The source makes an important key distinction: the frontend should use the Supabase publishable key, while some Edge Function compatibility flows still require the legacy JWT-based anon key. The `EDGE_FUNCTION_WEBHOOK_SECRET` must match both SQL-side configuration and Edge Function secrets.

Evidence: `raw/assets/SUPABASE_DEPLOY.md`

## Authority And Currency

- Authority level: high for project-specific deployment procedure.
- Date/currency: source has no explicit publication date; ingested 2026-05-28.
- Compliance sensitivity: high because deployment touches database schema, RLS/policies, Edge Functions, service role key, webhook secrets, AI provider keys and payment credentials.
- Supersedes: none identified.
- Superseded by: none identified.

## Key Claims

- Claim: The project has schema in `supabase/migrations`, functions in `supabase/functions` and seed data in `supabase/seed.sql`.
  Evidence: source opening statement.
  Confidence: high for repository intent; actual file inspection still required before implementation.

- Claim: Remote deployment uses `supabase link`, then `supabase db push` or `supabase db push --include-seed`.
  Evidence: source steps 1 and 2.
  Confidence: high for described procedure.

- Claim: Some database triggers call Edge Functions through `pg_net` and require project URL, legacy anon JWT key and a private webhook secret.
  Evidence: source step 3.
  Confidence: high.

- Claim: The publishable key is preferred for frontend variables, while legacy anon key remains necessary for some Edge Function compatibility/fallback flows.
  Evidence: source step 6 and notes.
  Confidence: high.

- Claim: If a target Supabase project already has manual tables outside migrations, `supabase db push` will not clean them; a fresh empty project is preferred for true isolation.
  Evidence: source notes.
  Confidence: high.

## Implementation-Relevant Details

- `supabase db push --include-seed` applies schema and seed; `supabase db push` skips demo data.
- SQL helper functions configure Edge Function webhook URL/key and private webhook secret.
- `public.get_edge_function_webhook_status()` can validate webhook configuration.
- `.env.functions` is populated from `.env.functions.example` and pushed with `supabase secrets set --env-file .env.functions`.
- Edge Functions deploy with `supabase functions deploy`.
- Frontend variables include `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY` and `VITE_SUPABASE_PROJECT_ID`.
- Secrets listed include service role key, Resend API key, admin email, app URL, cron secret, webhook secret, AI provider configuration and SISP credentials.

## Domain Implications

- Product: NOVA-ERP can run outside Lovable as a normal React + Supabase app.
- Architecture: deployment depends on migrations, RLS/policies, Edge Functions, storage and secrets being source-controlled or reproducible.
- Security/audit: service role key, webhook secret, AI key and payment credentials must never be exposed to the frontend or committed plaintext.
- Data model: target Supabase project should be clean or migration-controlled; manual drift is a release risk.
- UX/workflow: e-Fatura, notifications, AI and payment flows depend on correct Edge Function secret/runtime configuration.

## Entities Mentioned

- [[Supabase]]
- NOVA-ERP

## Concepts Mentioned

- [[Supabase Deployment]]
- [[ERP SaaS Multi-Tenant]]
- [[Permissoes e Auditoria ERP]]

## Contradictions Or Tensions

- The guide is operationally useful but does not itself prove that all RLS, storage policies, Edge Function authorization checks or tenant-isolation tests are production-safe.
- The guide distinguishes publishable frontend key from legacy anon key compatibility, which means implementation must avoid accidentally treating the legacy anon key as a privileged server secret.

## Legal/Fiscal Uncertainty

- Deployment procedure does not resolve fiscal compliance, e-Fatura certificate storage, legal retention or DNRE production credential requirements.
- Evidence needed: current Supabase security docs/changelog before implementation and current Cabo Verde/e-Fatura operational rules before production fiscal deployment.

## Follow-up Questions

- Which migration/advisor/test command becomes the mandatory pre-production gate?
- Should webhook secret configuration be automated in a repeatable deployment script?
- Which Edge Functions require service-role access, and how is initiating user/tenant attribution preserved?
- Where should e-Fatura certificates and signed XML/ZIP artifacts live: Supabase Storage, external object storage, encrypted DB columns or middleware-managed storage?

Follow-up: [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] resolves the initial storage shape for implementation planning: private storage for fiscal evidence artifacts, metadata/hashes in PostgreSQL, and raw certificate/private-key material outside ordinary domain tables.
