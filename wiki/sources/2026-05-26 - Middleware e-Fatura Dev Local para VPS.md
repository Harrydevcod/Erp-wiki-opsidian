---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/NOVA-ERP_Middleware_Dev_Local_para_VPS.md
source_type: middleware-deployment-guide
author:
published:
ingested: 2026-05-26
tags: [source, efatura, middleware, deployment, nova-erp]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[Contradiction - Middleware URL Scope]]"]
confidence: medium
---

# Middleware e-Fatura Dev Local para VPS

## Summary

This source describes how NOVA-ERP should run the DNRE `mwcore-efatura` middleware across development, staging, production and scale phases. Its central claim is that the same middleware software and same NOVA-ERP code can be used across environments, with environment-specific middleware endpoint configuration.

Evidence: `raw/assets/NOVA-ERP_Middleware_Dev_Local_para_VPS.md`

## Role In Source Hierarchy

This is an operational/deployment architecture source for e-Fatura. It should inform how NOVA-ERP deploys, tests and operates middleware integration, but it does not replace official DNRE documentation or legal/fiscal authority.

## Environment Model

The guide defines three main environments:

- local development: NOVA-ERP frontend locally, Supabase local or cloud dev, middleware at `https://localhost:3443`;
- staging/testing: staging app, staging Supabase, middleware on staging VPS/domain;
- production: production app, production Supabase, middleware on dedicated VPS/domain, ideally reachable through private networking.

The source later adds a scale phase with either multiple VPS instances/load balancing or a stronger VPS.

## Middleware Deployment Claim

The guide states the middleware executable is the same everywhere. The main environment difference is `application.properties`, which identifies:

- transmitter/software house;
- emitters/tenant NIFs;
- test or production mode.

## Configuration Model

The guide states NOVA-ERP needs one `MIDDLEWARE_URL` environment variable per environment:

- dev: local middleware URL;
- staging: staging middleware URL;
- production: production middleware URL.

This source therefore supports environment-level endpoint configuration.

## Tenant Onboarding Model

The guide also says production onboarding requires adding each tenant to middleware configuration:

- collect tenant NIF, credentials and certificate;
- append tenant NIF/name/client secret to middleware emitter groups;
- import tenant certificate into the keystore;
- update `application.properties`;
- restart middleware.

This means tenant-level configuration still exists, but primarily as middleware emitter/certificate configuration rather than necessarily one middleware URL per tenant.

## Edge Function Pattern

The guide proposes a `submit-dfe` Edge Function that:

- authenticates the user;
- derives tenant context;
- loads document and tenant data server-side;
- generates XML;
- generates IUD;
- packages payload;
- posts to middleware;
- records submission result;
- updates document status;
- falls back to contingency queue if middleware is unavailable.

## Contingency And Retry

The guide includes a contingency model:

- if middleware is unavailable, mark document as contingency;
- insert into contingency queue;
- retry periodically;
- update document status on success;
- escalate after repeated failures.

This is an important operational requirement for [[e-Fatura Cabo Verde]] and [[Faturacao Eletronica]].

## Security Notes

The guide mentions service keys, client secrets, certificates and keystores. These are sensitive and should never be stored in plain committed config or exposed in wiki pages beyond placeholders/summaries.

It also recommends firewalling production middleware so port 3443 is not public and is only reachable through a private network.

## Tensions

This source conflicts with [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] on middleware URL scope:

- official instructions: middleware URL configurable per tenant;
- this guide: one `MIDDLEWARE_URL` per environment.

Current reconciliation is captured in [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]: environment default endpoint, tenant e-Fatura settings/readiness and platform-admin-only tenant endpoint override. The original tension is preserved in [[Contradiction - Middleware URL Scope]].

## Open Questions

- Does DNRE middleware officially support multi-tenant emitter groups exactly as described here?
- Should tenant onboarding restart the middleware synchronously, or should this be queued/admin-approved?
- Does the hybrid model require a platform admin UI in MVP, or only migration/API-level support?
- What is the secure storage pattern for tenant certificates and client secrets before writing `application.properties`?
