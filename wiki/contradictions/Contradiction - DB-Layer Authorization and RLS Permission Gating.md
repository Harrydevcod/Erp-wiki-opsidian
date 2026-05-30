---
type: contradiction
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [contradiction, security, rls, permissions, authorization, schema, implementation-review, needs-review]
sources: ["[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]", "nova-erp/supabase/migrations/00002_iam_schema.sql", "nova-erp/supabase/migrations/00010_rls_policies.sql"]
related: ["[[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]]", "[[Permissoes e Auditoria ERP]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# Contradiction — DB-Layer Authorization and RLS Permission Gating

## Disputed Claim

At the database layer, is access gated by **tenant membership + per-action permission** (`has_permission`, `user_permission_overrides`), or by **tenant membership alone**?

> Note: this is **not** a tenant-isolation hole. Isolation is sound — see "What is NOT in dispute" below. The dispute is about *authorization granularity* and the service-role boundary.

## Position A — Permission-gated at the DB (design / ADRs)

[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] specifies default-deny RLS plus helpers including **`has_permission(tenant_id, permission_key)`** for sensitive actions, and platform-admin outside RLS. [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]] adds **`user_permission_overrides`** (reason-bound, expiring, **revoke-wins**) and **graduated evidence tiers** so ordinary operators cannot read raw fiscal/certificate evidence.

- Source: [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]], [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]

## Position B — Membership-only at the DB (implementation)

`00010_rls_policies.sql`: **41 `FOR ALL` policies** whose predicate is only `tenant_id = get_active_tenant_id()`. There is **no `has_permission` call in any policy** → any active member of a tenant has **full CRUD on every business table** at the DB layer. Additional gaps vs the ADRs:

- **No `user_permission_overrides`** table (per-user revoke-wins absent); authorization is role-only via `memberships → role_id → role_permissions` (`get_user_permissions` exists but is consumed by the app, not RLS).
- **No graduated evidence tiers** (certificates/XML/payroll readable by any active member subject only to tenant scope).
- **No `FORCE ROW LEVEL SECURITY`** and policies are **untargeted** (no `TO authenticated`) → table owner / `service_role` bypasses RLS. Edge Functions using the service key operate unconstrained.

- Source: `nova-erp/supabase/migrations/00010_rls_policies.sql`, `.../00002_iam_schema.sql`

## What is NOT in dispute (tenant isolation is sound)

`set_tenant_context(p_tenant_id)` raises unless the caller has an **active membership** in that tenant; `get_active_tenant_id()` returns the tenant **only if** an active membership for `auth.uid()` matches the session GUC. So `tenant_id = get_active_tenant_id()` is **effectively membership-keyed** — a spoofed `app.tenant_id` yields NULL and matches nothing. The ADR's "never trust raw `auth.uid()` ownership; key on membership" principle is satisfied, just via an active-tenant indirection rather than an all-tenants subselect.

## Current Best Interpretation

Tenant isolation: **matches** design. Authorization granularity: **diverges** — the DB enforces *tenant*, not *permission*. This pushes all role/permission enforcement into the application/Edge layer (unverified here). For a fiscal/accounting SaaS the missing pieces that matter most are: per-action gating of sensitive operations, the revoke-wins override mechanism, evidence-tier protection of certificates/keys/XML, and the `FORCE`/service-role hardening.

## Confidence

High (read directly from the policy and IAM migrations).

## Update 2026-05-30 — Edge layer does NOT compensate

The Edge Function review ([[2026-05-30 - Edge Function and Storage Security Review]]) tested the "app/Edge layer enforces it" hypothesis and **partially falsified it**: `create-user`, `audit-log` and `numbering` all run on the **service-role key (bypassing RLS)** and **trust body `tenant_id` with no caller membership/permission check**. So for these privileged operations there is **no enforced per-tenant authorization at any layer** — `create-user` allows cross-tenant admin creation (critical). Authorization gating is therefore genuinely missing, not merely relocated.

## What Would Resolve It

- Confirm where authorization is meant to live. If **DB layer**: add `has_permission()` to sensitive-table policies, create `user_permission_overrides`, split evidence-read permissions, enable `FORCE ROW LEVEL SECURITY` and target policies `TO authenticated`.
- If **app/Edge layer is the accepted boundary**: the three reviewed functions must first be fixed to derive the caller identity from the JWT and verify membership + permission against the target tenant (see [[2026-05-30 - Edge Function and Storage Security Review]] root-cause pattern), then amend the foundation/permission ADRs to document the Edge layer as the enforcement point.
