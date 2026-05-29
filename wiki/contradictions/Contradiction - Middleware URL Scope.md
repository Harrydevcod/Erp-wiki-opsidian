---
type: contradiction
status: superseded
created: 2026-05-26
updated: 2026-05-28
tags: [contradiction, efatura, middleware, configuration]
sources: ["[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Configuracao ERP]]", "[[Revisao Raw Assets - 2026-05-26]]"]
confidence: medium
---

# Contradiction - Middleware URL Scope

## Resolution

Superseded by [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]].

Current decision: use a hybrid model with one default middleware endpoint per environment, tenant-scoped e-Fatura emitter/readiness configuration, and tenant endpoint override only as a platform-admin controlled exception.

The original tension remains useful history, but should no longer block first-pass schema design.

## Disputed Claim

Whether NOVA-ERP should configure the e-Fatura middleware URL per tenant or as one environment-level `MIDDLEWARE_URL`.

## Position A

- Claim: middleware URL should be dynamic, persistent and tenant-scoped, stored in settings/system config and editable from the ERP integration configuration UI.
- Evidence: official NOVA-ERP project instructions describe tenant-aware middleware configuration.
- Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]
- Strength: medium; project direction is authoritative for desired product behavior but may predate operational middleware constraints.

## Position B

- Claim: NOVA-ERP only needs one environment variable, `MIDDLEWARE_URL`, and the same code works across dev, staging and production by changing the environment value.
- Evidence: middleware deployment guide describes environment-level endpoint selection.
- Source: [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]
- Strength: high for deployment simplicity; incomplete for multi-tenant emitter/certificate governance.

## Current Best Interpretation

Use a hybrid model as the current working interpretation:

- Environment-level `MIDDLEWARE_URL` defines the shared middleware endpoint for dev, staging and production.
- Tenant-level configuration defines emitter identity, NIF, credentials, certificate metadata, certificate onboarding state, health/status and operational readiness.
- Middleware-side `application.properties`/keystore contains tenant emitter groups and certificates.
- The ERP should not hardcode URLs; it should have an environment default and preserve a tenant-aware configuration model for future override or multi-middleware deployments.

The source conflict is therefore not a pure either/or. It is likely "environment endpoint plus tenant emitter configuration."

This inference has now been promoted into a provisional schema decision in [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]. It still requires operational verification against the real DNRE middleware behavior before production rollout.

## Implementation Risk

- Product: tenant admin UI may expose misleading URL controls if the endpoint is actually environment-owned.
- Architecture: hardcoding either per-tenant URL or global-only URL too early can block multi-middleware deployments.
- Data model: tenant configuration should separate endpoint override, emitter identity, certificate status and readiness.
- Security/audit: tenant operators should not be able to redirect fiscal traffic to arbitrary middleware without controlled approval.
- Compliance: wrong emitter/middleware routing could submit DFEs under the wrong operational context.

## Resolution Criteria

- Verify actual DNRE middleware deployment constraints.
- Decide whether production uses one shared middleware per environment, one middleware per tenant, or a hybrid model.
- Record the decision as an architecture decision before e-Fatura implementation.
- Safe temporary posture: environment default endpoint plus tenant-scoped e-Fatura configuration, with endpoint override disabled or admin-only until production topology is decided.

## Suggested ADR Direction

Proposed decision to validate: "NOVA-ERP uses one default middleware endpoint per environment, while storing tenant e-Fatura configuration per tenant and syncing tenant emitters/certificates into the middleware."

## Status History

- Date: 2026-05-28
  Change: Superseded by provisional schema decision using environment default endpoint plus tenant e-Fatura settings and platform-controlled override.
  Source: [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]

- Date: 2026-05-28
  Change: Normalized contradiction with implementation risk and resolution criteria.
  Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]
