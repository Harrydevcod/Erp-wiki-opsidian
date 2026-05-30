---
type: synthesis
status: active
created: 2026-05-30
updated: 2026-05-30
scope: NOVA-ERP Supabase Edge Functions + storage policy security review
decision_status: security-finding
tags: [security, edge-functions, supabase, rls, authorization, multi-tenant, storage, implementation-review, needs-review]
sources: ["nova-erp/supabase/functions/create-user/index.ts", "nova-erp/supabase/functions/audit-log/index.ts", "nova-erp/supabase/functions/numbering/index.ts", "nova-erp/supabase/functions/_shared/cors.ts", "nova-erp/supabase/functions/_shared/fiscal-payload.ts", "nova-erp/supabase/config.toml", "nova-erp/supabase/migrations/00010_rls_policies.sql"]
related: ["[[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]]", "[[Contradiction - DB-Layer Authorization and RLS Permission Gating]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[Permissoes e Auditoria ERP]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# Edge Function and Storage Security Review

## Thesis

All three NOVA-ERP Edge Functions (`create-user`, `audit-log`, `numbering`) run on the **service-role key** (which **bypasses RLS**) and **trust the request-body `tenant_id` without ever deriving or verifying the caller's identity, tenant membership, or permission.** `config.toml` sets `verify_jwt = true`, so a caller must present *some* valid platform JWT — but nothing ties the privileged action to *that* user or checks their rights in the **target** tenant.

Because [[Contradiction - DB-Layer Authorization and RLS Permission Gating]] already showed RLS gates only *tenant*, not *permission*, and these functions bypass RLS entirely, the net result is: **for these privileged operations there is currently no enforced per-tenant authorization at any layer — neither database nor Edge.** This partially falsifies the optimistic hypothesis that "permission enforcement must live in the app/Edge layer."

This is the kind of finding a buy-side or compliance audit would flag immediately. Reported as evidence, not yet fixed (review was read-only).

## Findings

| # | Function | Severity | Issue | Exploit |
|---|----------|----------|-------|---------|
| 1 | `create-user` | **Critical** | Service-role client; reads `tenant_id` + `role_code` from body; never checks the caller is an admin/member of `tenant_id`. | Any authenticated platform user can `POST` `{tenant_id: <victim>, role_code: 'admin', email}` and **mint an admin membership in any tenant** → cross-tenant takeover/privilege escalation. |
| 2 | `audit-log` | **High** | Service-role client; inserts `audit_logs` straight from the body — including the acting `user_id`, `tenant_id`, `action`, `before_data`/`after_data`. | Audit attribution is **forgeable**: any caller can write audit rows attributing any action to any user in any tenant, or pollute another tenant's trail. DB append-only (REVOKE update/delete) protects against tampering *after* insert, not against forged inserts. Undermines the audit log's value as fiscal/legal evidence. |
| 3 | `numbering` | **High** | Service-role client; trusts body `tenant_id`/`series_id`; no caller membership check. | Any authenticated user can increment another tenant's fiscal series, **injecting gaps in a gapless invoice sequence** — a Cabo Verde fiscal-compliance problem the victim must justify to [[DNRE]]. |
| 4 | Storage | **Medium/Gap** | **No `storage.buckets` / `storage.objects` policies defined in any migration.** | The e-Fatura/secrets ADR ([[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]) requires **private** buckets for fiscal XML, certificates/keys and payroll artifacts. None are provisioned in migrations; bucket creation/policy is undefined here (may be configured manually in the Supabase dashboard — unverified). |

### Secondary notes

- `numbering` concurrency: the optimistic compare-and-swap (`UPDATE … .eq('current_seq', expected)` → 409 on conflict) **is** race-safe, but a single atomic `UPDATE series SET current_seq = current_seq + 1 … RETURNING` would be simpler and avoid client retry storms. The fiscal-year-reset branch is correct.
- `create-user` does compensate (deletes the auth user) if the membership insert fails — good. But its `audit_logs` write records **no acting `user_id`** (only the created user as `entity_id`), so even the legitimate path loses actor attribution.
- `_shared/cors.ts` is headers only; `_shared/fiscal-payload.ts` is a payload builder — neither performs auth (expected).

## Root Cause

A privileged Edge Function on the service-role key must **re-establish the caller's identity and authorization itself**, because it has stepped outside RLS. The correct pattern (per [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]):

1. Read the caller JWT (`Authorization` header) with an anon/user-scoped client → `auth.getUser()`.
2. Verify an **active membership** of that user in the body's `tenant_id` (mirror of `set_tenant_context`).
3. Verify the required **permission** (`has_permission(tenant_id, 'iam.user.create' | 'fiscal.numbering.issue' | …)`), honoring `user_permission_overrides`.
4. Derive the acting `user_id` **from the verified JWT**, never from the body, for audit writes.
5. Only then use the service-role client for the privileged write.

## Current Interpretation

- **Known (high confidence):** the three functions, read directly, contain no caller-authorization logic; storage policies are absent from migrations.
- **Inferred:** the app/frontend likely only ever calls these for the "right" tenant, so the gap may not be exploited in normal use — but that is a client-side convention, not an enforced control. Any authenticated user with the function URL can bypass it.
- **Unresolved:** whether storage buckets/policies exist in the Supabase project outside migrations (dashboard-configured); whether any API gateway / additional auth sits in front of the functions.

## Implementation Consequence / Recommended Fix Order

1. **`create-user`** (critical): add caller membership + `iam.user.create` permission check before provisioning; reject if caller is not an admin of the target tenant.
2. **`audit-log`** (high): derive `user_id` from the verified JWT; verify caller membership in `tenant_id`; treat body `user_id` as untrusted.
3. **`numbering`** (high): verify caller membership + numbering permission in `tenant_id`; consider the atomic-increment SQL form.
4. **Storage** (gap): define private buckets + RLS-equivalent storage policies for fiscal XML, certificates and payroll artifacts in a migration; confirm none are public.
5. Add `FORCE ROW LEVEL SECURITY` + `TO authenticated` policy targeting (from [[Contradiction - DB-Layer Authorization and RLS Permission Gating]]) so even accidental service-role/owner queries stay constrained where intended.

## Remediation drafted 2026-05-30 (code-level findings 1–3)

A shared guard `nova-erp/supabase/functions/_shared/auth.ts` was added and wired into all three functions:

- `callerClient(req)` builds a **caller-JWT-scoped** client (ANON key + forwarded `Authorization`), so `auth.uid()` in the SECURITY DEFINER RPCs resolves to the real caller.
- `requireTenantPermission(req, tenantId, code)` → calls `get_user_permissions(tenantId)`; passes if the caller holds `code` or `core.admin`.
- `requireTenantMember(req, tenantId)` → calls `get_user_tenants()`; passes if the caller has an active membership in the target tenant.
- **create-user**: gated on `admin.users`; audit `user_id` now derived from the verified JWT.
- **audit-log**: gated on membership; `user_id` forced from the JWT (body `user_id` ignored); header doc updated to say server-to-server callers write `audit_logs` directly with the service key.
- **numbering**: gated on active membership in the target tenant.
- Unit test `_shared/auth.test.ts` covers the guard decision logic with a mock client.

**Finding 4 (storage)** also drafted: migration `20260530120000_storage_buckets.sql` creates the three **private** buckets from the e-Fatura evidence ADR (`fiscal-evidence`, `fiscal-renders`, `efatura-onboarding-temp`) with size/MIME limits, and intentionally adds **no client policies** on `storage.objects` (deny-by-omission → only service-role via Edge Functions; signed URLs generated server-side). Documents the `<bucket>/<tenant_id>/…` path convention. Customer-facing PDF/DFA read access stays an open ADR question, so no tenant-scoped read policy yet.

**Verification status:** all drafted in the working tree, **NOT committed**, and **NOT yet run** — the environment has no `deno`/`supabase`/`psql` CLI. Founder/CI must run `deno test supabase/functions/_shared/auth.test.ts`, `deno check`, apply the storage migration against a branch DB, and an integration pass (`supabase functions serve`) before merge. The `FORCE RLS` + `TO authenticated` hardening (DB-layer) remains open — **deliberately deferred**: it carries breakage risk for `anon`/role-dependent flows and needs testing, not a blind migration.

## Maintenance Notes

- Completes the implementation-grade pass started in [[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]] (Edge Functions + storage were the outstanding items).
- Original review was read-only; the remediation above modifies `nova-erp/supabase/functions/*`. Re-review after the fixes are run/verified and after storage policies land.
