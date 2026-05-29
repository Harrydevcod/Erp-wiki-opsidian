---
type: schema
status: active
created: 2026-05-28
updated: 2026-05-28
decision_status: provisional
tags: [schema, architecture, multi-tenant, rls, security, audit, nova-erp]
sources: ["[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Supabase Deploy]]"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[Configuracao ERP]]", "[[Supabase Deployment]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: high
---

# Schema Decision - Tenant Foundation and RLS

## Decision

NOVA-ERP adopts a single-database, RLS-enforced multi-tenant foundation. Every business row carries a non-null `tenant_id`. Tenant membership, roles and granular permissions are first-class tenant-scoped tables resolved from the authenticated Supabase session. Row-level security is default-deny on every business table and keys on membership in the row's tenant, never on raw `auth.uid()` ownership. A single append-only `audit_log` records sensitive fiscal, accounting, permission and configuration actions. Platform-admin access is a narrow, explicit, audited capability that lives outside tenant RLS rather than a magic role inside it. This foundation is a hard dependency for every other target schema decision (fiscal documents, treasury, inventory, accounting, payroll, assets, subscriptions) and must exist before they are implemented.

## Scope

- Module: [[Permissoes e Auditoria ERP]], [[ERP SaaS Multi-Tenant]], [[Configuracao ERP]] foundation.
- Tables/objects: `tenants`, `tenant_members`, `roles`, `permissions`, `role_permissions`, `profiles`, `audit_log`, `platform_admins`, plus helper functions and the RLS policy pattern applied to all business tables.
- Workflows affected: every authenticated read/write in the product; tenant onboarding; user invitation; sensitive-action auditing.
- Tenancy boundary: the `tenant_id` column plus membership-based RLS is the isolation boundary. No client-facing path may cross tenants.

## Source Basis

- Product source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]] require multi-tenant ERP with tenant isolation, RBAC and audit logs.
- Compliance source: fiscal/accounting data isolation and immutable audit are compliance constraints, not features (see [[Fiscalidade Cabo Verde]]).
- Technical source: [[2026-05-26 - Prompt Implementacao NOVA-ERP]] (RLS/seed/security posture), [[2026-05-28 - Supabase Deploy]] (RLS, service-role boundary, Edge Functions).
- Inference: the membership-keyed RLS pattern and `platform_admins`-outside-RLS choice are agent design inferences grounded in those sources, not verbatim source claims.

## Context

[[2026-05-28 - Current Database Snapshot Classification]] established that the current snapshot bolts ERP-adjacent tables onto an e-commerce/POS base where `tenant_id`, memberships, audit and RLS are not foundational. The snapshot's `profiles`, `user_roles` and `user_permissions` are adapt candidates, but the target needs a tenant root and membership join the snapshot lacks. This decision resolves the classification's open question "first schema decision page: tenant foundation, fiscal documents, or e-Fatura payload/transmission?" — the e-Fatura payload/transmission, event, middleware and evidence decisions already exist; the foundation they all sit on does not. Without it, every other table's RLS would be ad hoc.

## Data Model

- Entity/table: `tenants`
  - Key fields: `id` (uuid pk), `name`, `slug` (unique), `status` (`active|suspended|archived`), `created_at`.
  - RLS/security: readable only by members; writable only by platform-admin or tenant owner role.

- Entity/table: `profiles`
  - Key fields: `id` (= `auth.users.id`), `full_name`, `email`, `default_tenant_id` (nullable fk).
  - Relationships: 1:1 with Supabase `auth.users`; 1:N with `tenant_members`.
  - Note: profile is global (a user identity); tenant scoping lives in `tenant_members`, not here.

- Entity/table: `tenant_members`
  - Key fields: `id`, `tenant_id` (fk), `user_id` (fk profiles), `role_id` (fk roles), `status` (`invited|active|disabled`), `created_at`.
  - Constraints: unique (`tenant_id`, `user_id`).
  - This is the row RLS policies join against to decide membership.

- Entity/table: `roles`
  - Key fields: `id`, `tenant_id` (nullable — null = system/template role), `key` (`owner|admin|accountant|operator|viewer` initial set), `name`.
  - Constraints: unique (`tenant_id`, `key`).

- Entity/table: `permissions`
  - Key fields: `id`, `key` (e.g. `invoice.issue`, `efatura.view_raw`, `accounting.post`, `payroll.view`), `description`.
  - Global catalog, not tenant-scoped.

- Entity/table: `role_permissions`
  - Key fields: `role_id` (fk), `permission_id` (fk).
  - Constraints: unique (`role_id`, `permission_id`).

- Entity/table: `audit_log`
  - Key fields: `id`, `tenant_id`, `actor_user_id`, `action` (text key), `entity_type`, `entity_id`, `before` (jsonb null), `after` (jsonb null), `created_at`, `request_id` (nullable).
  - Constraints: append-only. No update/delete policy for any tenant role; writes via `service_role`/SECURITY DEFINER only.
  - Indexes: (`tenant_id`, `created_at`), (`tenant_id`, `entity_type`, `entity_id`).

- Entity/table: `platform_admins`
  - Key fields: `user_id` (fk), `created_at`.
  - Purpose: explicit allowlist consulted by a helper function; not a tenant role.

- Helper functions (SECURITY DEFINER, stable):
  - `current_user_tenant_ids()` -> set of tenant_ids the caller is an active member of.
  - `is_tenant_member(tenant_id)` -> boolean.
  - `has_permission(tenant_id, permission_key)` -> boolean (joins members→roles→role_permissions).
  - `is_platform_admin()` -> boolean.

- RLS policy pattern for every business table `X`:
  - Enable RLS; revoke default access (default-deny).
  - `SELECT`/`INSERT`/`UPDATE`/`DELETE` policy: `tenant_id IN (select current_user_tenant_ids())` and, for sensitive writes, `has_permission(tenant_id, '<key>')`.
  - Platform-admin bypass handled by a separate explicit policy `is_platform_admin()`, never by disabling RLS.

## State And Events

- State: `tenants.status`: `active -> suspended -> archived`.
- State: `tenant_members.status`: `invited -> active -> disabled`.
- Event: `tenant.created`, `member.invited`, `member.activated`, `member.role_changed`, `member.disabled`, `permission.granted`, `permission.revoked` — all written to `audit_log`.
- Transition rule: only `owner`/`admin` roles (or platform-admin) may change another member's role or status; role changes always audit before/after.

## Alternatives Considered

- Alternative: schema-per-tenant isolation.
  Why not: heavy operational cost for migrations, RLS, and Edge Functions at NOVA-ERP's stage; single-DB + RLS is the documented posture. Revisit only for exceptionally large tenants ([[ERP SaaS Multi-Tenant]] open question).
- Alternative: RLS keyed directly on `auth.uid()` ownership (snapshot style).
  Why not: ERP rows are tenant-owned, not user-owned; ownership-RLS cannot express "all accountants in this tenant see this invoice."
- Alternative: platform-admin as a super-role inside `roles`.
  Why not: a magic in-tenant role risks accidental cross-tenant leakage through normal policies; an out-of-band allowlist with explicit bypass policies is auditable and narrower.
- Alternative: per-module audit tables.
  Why not: a single append-only `audit_log` gives one tamper-evident timeline and one retention policy; module context lives in `entity_type`/`action`.

## Consequences

- Positive: every later schema decision inherits one isolation, permission and audit pattern instead of inventing its own.
- Positive: membership-keyed RLS matches ERP role semantics and supports multi-tenant users.
- Tradeoff: helper functions in RLS predicates must be performant (stable, indexed membership lookups) or every query pays a join.
- Migration impact: snapshot `profiles` adapts; `user_roles`/`user_permissions` are replaced by `tenant_members`+`roles`+`role_permissions`; a `tenant_id` backfill is required for any retained business table.
- Operational impact: audit writes and platform-admin actions must route through service-role/SECURITY DEFINER paths per [[Supabase Deployment]].

## Validation Plan

- Test: a member of tenant A cannot SELECT/INSERT/UPDATE/DELETE any row of tenant B (per business table). Failure mode: cross-tenant leak — release blocker.
- Test: default-deny — a table with RLS enabled but no policy returns zero rows to clients. Fixture: new business table.
- Test: `has_permission` gating — an `operator` cannot perform an `accountant`-only action; attempt is denied and not audited as success.
- Test: `audit_log` is append-only — no tenant role can UPDATE or DELETE an audit row.
- Test: platform-admin bypass is explicit and audited — a non-admin cannot assume bypass.
- Fixture/source: derive role/permission fixtures from [[2026-05-26 - Backlog Estruturado NOVA-ERP]] acceptance criteria.

## Open Questions

- What is the first launch role set beyond `owner|admin|accountant|operator|viewer`?
- Should `default_tenant_id` live on `profiles` or be resolved purely from a tenant switcher in the session?
- How is tenant context propagated to Edge Functions and the e-Fatura middleware (JWT claim vs explicit parameter)? Ties to [[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]] and middleware topology.
- Which exact action keys are MVP-mandatory in `audit_log`?
- Do helper functions belong in RLS predicates or should membership be denormalized into a JWT claim for performance?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are inspected (still the standing gap in [[Contradiction - Current Database Snapshot vs Target ERP Architecture]]).
- This is the prerequisite decision for upcoming target schema decisions on fiscal/commercial documents, treasury, inventory and accounting.
- Related log entry: 2026-05-28 tenant foundation schema decision.
