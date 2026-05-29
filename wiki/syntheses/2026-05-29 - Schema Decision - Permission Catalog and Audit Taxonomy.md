---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, security, permissions, rbac, audit, nova-erp]
sources: ["[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]"]
related: ["[[NOVA-ERP]]", "[[Permissoes e Auditoria ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]]", "[[Faturacao Eletronica]]", "[[Contabilidade ERP]]", "[[Supabase Deployment]]"]
confidence: medium
---

# Schema Decision - Permission Catalog and Audit Taxonomy

## Decision

NOVA-ERP layers a concrete **permission catalog**, a **per-user override mechanism**, **graduated sensitive-evidence access tiers** and an **audit event taxonomy** on top of the foundation defined in [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]. Permission keys follow a stable `module.action` convention in the global `permissions` catalog; a launch role→permission matrix maps the initial role set; `user_permission_overrides` allow controlled, reason-bound, expiring per-user grants/revocations where revoke always wins over grant. Reading raw fiscal/certificate evidence is a *distinct* permission from reading document status, so ordinary operators never see raw XML, ZIP archives, DNRE/middleware response bodies or certificate material by default. The single append-only `audit_log` from the foundation is kept; this ADR commits the typed event catalog, the rule that sensitive payloads are referenced by hash/evidence link rather than duplicated, and the requirement that every service-role/Edge-Function write attributes an initiating user plus correlation id. This ADR adds no second isolation mechanism — RLS and tenancy remain exactly as the foundation defines them.

## Scope

- Module: [[Permissoes e Auditoria ERP]] (extends, does not replace, [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]).
- New tables/objects: `permission_groups` (catalog grouping), `user_permission_overrides`, `audit_event_types`; plus the committed contents of the foundation's `permissions` catalog and `roles`/`role_permissions` seed.
- Reused unchanged: `tenants`, `tenant_members`, `roles`, `permissions`, `role_permissions`, `audit_log`, `platform_admins`, and the helper functions (`has_permission`, `is_tenant_member`, `is_platform_admin`, `current_user_tenant_ids`).
- Workflows affected: permission evaluation, role seeding, exceptional access grants, sensitive-evidence access, audit-event emission and attribution of background/service work.
- Tenancy boundary: unchanged — membership-keyed default-deny RLS. Overrides are tenant-scoped and never widen cross-tenant scope.

## Source Basis

- Foundation source: [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] defines `permissions`/`role_permissions`/`audit_log` shape and the `has_permission` gating predicate; it explicitly left the *catalog contents*, *override mechanism* and *audit event keys* open.
- Module source: [[Permissoes e Auditoria ERP]] enumerates the high-risk permission groups, the audit event model and the fiscal/accounting event lists synthesized here.
- Fiscal/evidence source: [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] and [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] require separate access to raw payloads, response bodies and certificate material.
- Accounting source: [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] requires distinct post/reverse/period-close/export permissions.
- Entitlement boundary: [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] — plan entitlement gates tenant capability; this ADR gates user actions. Both must pass.
- Product source: PRD/SSD require RBAC, least privilege and durable audit; the Prompt sets RLS/seed/security posture.

## Context

The foundation ADR committed the RBAC *tables* and the RLS *predicate* but deliberately stopped short of the catalog and audit content ("Which exact action keys are MVP-mandatory?", "first launch role set?"). Implementing modules now need a stable, shared key vocabulary so every module's RLS write predicate (`has_permission(tenant_id, '<key>')`) refers to the same catalog. Without a committed convention, each module would invent its own keys and the audit timeline would fragment. This ADR fixes the vocabulary and the audit taxonomy so all prior and future module ADRs share one authorization and traceability surface.

## Data Model

- Entity/table: `permission_groups`
  - Key fields: `id`, `key` (`tenant_admin|fiscal_config|fiscal_issue|efatura_ops|efatura_raw|secrets|accounting|treasury|inventory|payroll|assets|subscriptions|audit|reports|ai`), `name`, `risk_level` (`standard|high|critical`), `display_order`.
  - Purpose: organizes the global `permissions` catalog into reviewable risk groups; not tenant-scoped.

- Catalog seed: `permissions` (foundation table) — committed `module.action` keys
  - Convention: lowercase `module.action`; one capability per key; never collapse into a single `admin` flag.
  - Tenant admin: `tenant.manage`, `member.invite`, `member.role_assign`, `member.disable`, `permission.override`.
  - Fiscal config: `fiscal.config_series`, `fiscal.config_doctypes`, `fiscal.config_tax`.
  - Fiscal issue: `invoice.draft`, `invoice.issue`, `invoice.corrective`, `invoice.cancel`.
  - e-Fatura ops: `efatura.payload_generate`, `efatura.view_status`, `efatura.reprocess`, `efatura.contingency_manage`.
  - e-Fatura raw evidence: `efatura.view_raw`, `efatura.view_response`, `efatura.view_archive`.
  - Secrets: `secret.cert_upload`, `secret.cert_rotate`, `secret.credential_manage`.
  - Accounting: `accounting.post`, `accounting.reverse`, `accounting.rule_manage`, `accounting.tax_profile_manage`, `accounting.period_close`, `accounting.period_reopen`, `accounting.export`.
  - Treasury: `treasury.record`, `treasury.reconcile`, `treasury.allocate`, `treasury.reverse`.
  - Inventory: `inventory.adjust`, `inventory.count_approve`, `inventory.valuation_manage`.
  - Payroll: `payroll.employee_view`, `payroll.salary_view`, `payroll.process`, `payroll.approve`, `payroll.payslip_publish`, `payroll.payment_export`.
  - Assets: `assets.manage`, `assets.depreciation_run`, `assets.dispose`.
  - Subscriptions: `saas.subscription_view`, `saas.subscription_manage`, `saas.entitlement_override`, `saas.billing_run`, `saas.invoice_view`.
  - Audit: `audit.view`, `audit.export`.

- Entity/table: `user_permission_overrides`
  - Key fields: `id`, `tenant_id`, `user_id`, `permission_id`, `effect` (`grant|revoke`), `reason`, `granted_by`, `effective_from`, `effective_to` (nullable = no expiry), `created_at`.
  - Constraints: tenant-scoped; requires `permission.override` capability + reason; unique active (`tenant_id`, `user_id`, `permission_id`); every row audited.
  - Resolution: effective permission = (role grants via `role_permissions`) applied with overrides, where a `revoke` override always wins over any grant.

- Entity/table: `audit_event_types`
  - Key fields: `id`, `key` (e.g. `accounting.journal_entry_posted`), `category`, `severity` (`info|notice|critical`), `requires_reason` (bool), `payload_policy` (`full|reference|hash_only`).
  - Purpose: typed catalog that governs how each event populates `audit_log` (before/after vs evidence reference vs hash only).

- Reused unchanged: `audit_log` (foundation) — `actor_user_id`, `action`, `entity_type`, `entity_id`, `before`, `after`, `request_id`, `created_at`. This ADR adds the convention that `actor_kind` (`user|service|platform_admin`) and a correlation/`job_id` are carried in the event (via `request_id` or a small extension) for background attribution.

- Helper function extension: `has_permission(tenant_id, key)` resolves role grants then applies `user_permission_overrides` (revoke-wins) before returning.

## State And Events

- State: `user_permission_overrides` is effectively dated; an expired or deleted override reverts the user to role-derived permissions.
- Audit event taxonomy (committed keys, drawn from the module page):
  - Security/RBAC: `tenant.created`, `member.invited`, `member.activated`, `member.role_changed`, `member.disabled`, `permission.override_granted`, `permission.override_revoked`.
  - Fiscal: `fiscal_document.number_assigned`, `fiscal_document.issued`, `fiscal_document.corrective_document_created`, `dfe.payload_generated`, `dfe.validation_completed`, `dfe.transmission_attempted`, `dfe.authorized`, `dfe.rejected`, `dfe.contingency_entered`, `dfe.retry_scheduled`, `efatura.certificate_uploaded`, `efatura.certificate_rotated`, `efatura.middleware_config_changed`.
  - Accounting: `accounting.journal_entry_posted`, `accounting.journal_entry_reversed`, `accounting.posting_rule_changed`, `accounting.tax_profile_changed`, `accounting.period_closed`, `accounting.period_reopened`, `accounting.saft_export_generated`.
- Payload rule: events on raw fiscal/secret evidence use `payload_policy = reference` or `hash_only` — `audit_log` links to the immutable evidence row or stores a hash, never copies XML/ZIP/keys/response bodies.
- Attribution rule: every `service_role`/SECURITY DEFINER/Edge-Function write sets `actor_user_id` to the initiating user and carries a correlation/`job_id`; unattributable system writes are marked `actor_kind = service` explicitly.

## Sensitive-Evidence Access Tiers

Three graduated read tiers prevent over-exposure:

1. **Status tier** (`*.view_status`): ordinary operators see document state, rejection summaries and KPIs — never raw payloads.
2. **Raw-evidence tier** (`efatura.view_raw`/`view_response`/`view_archive`, `accounting.export`, `payroll.salary_view`): restricted roles see raw XML, response bodies, archives and sensitive financial/personal fields, backed by private storage policies.
3. **Secret tier** (`secret.*`): certificate material, keystores, transmitter keys and client secrets — narrowest access, always audited, separated per [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]].

UI gating is UX only; the tier boundary is enforced server-side via `has_permission` and private storage policies.

## Provisional Launch Role → Permission Matrix

- `owner`: all tenant capabilities including `permission.override`, `tenant.manage`, secret tier.
- `admin`: tenant admin + config + most ops; secret tier optional/audited.
- `accountant`: accounting full, fiscal config + issue, `efatura.view_status`/`view_raw`, `audit.view`; no secret rotation.
- `operator`: `invoice.draft`/`issue`, `treasury.record`, `inventory.adjust`, `efatura.view_status`; no raw/secret/accounting-post.
- `viewer`: read/status only across permitted modules; no mutations.
- `payroll_officer` (optional launch role): payroll process/approve/payslip; salary view gated separately.

Platform-admin remains out-of-band per the foundation, not a role in this matrix.

## Alternatives Considered

- Alternative: define per-module permission keys ad hoc inside each module ADR.
  Why not: fragments the catalog and the audit timeline; a shared `module.action` convention keeps `has_permission` consistent.
- Alternative: per-user permission rows instead of role-based with overrides.
  Why not: unmanageable at scale; roles + bounded overrides give least privilege with auditability.
- Alternative: grant-wins override precedence.
  Why not: a revoke must be able to lock out a compromised/over-privileged user even if a role grants the capability.
- Alternative: duplicate sensitive payloads into `audit_log` for completeness.
  Why not: copies secrets/PII into the audit timeline; hash/reference preserves traceability without leakage.

## Consequences

- Positive: one shared permission vocabulary and one audit taxonomy across every module ADR.
- Positive: graduated tiers stop raw fiscal/secret exposure to ordinary operators; overrides give controlled, expiring exceptions.
- Positive: background/service work is attributable to an initiating user, closing the foundation's attribution open question.
- Tradeoff: `has_permission` now resolves overrides too — must stay indexed/stable to avoid per-query cost.
- Migration impact: snapshot `user_roles`/`user_permissions` already replaced by the foundation; this ADR only seeds catalog + override + event-type tables (new build).
- Operational impact: override approval, expiry sweeps and audit review need operator workflows.

## Validation Plan

- Test: a `revoke` override denies an action even when the user's role grants it.
- Test: an expired override no longer affects resolution.
- Test: an `operator` cannot read raw e-Fatura XML/response/certificate material; an `accountant` can read raw but cannot rotate certificates.
- Test: every override change and every committed audit event key writes an `audit_log` row with actor, tenant, target and timestamp.
- Test: a sensitive-evidence audit event stores a reference/hash, not the raw payload.
- Test: a background/service-role write records the initiating user and a correlation id.
- Test: SaaS entitlement denial and permission denial are independent — neither bypasses the other.

## Open Questions

- Is `payroll_officer` a launch role or folded into `admin`/`accountant` initially?
- Which audit event keys are hard release gates vs best-effort in MVP?
- Should `audit.export` be tenant-admin-visible or platform-support-only for raw fiscal/secret categories?
- Do overrides require a second-approver workflow for `critical` risk_level permissions?
- Is membership/permission denormalized into a JWT claim for performance, or always resolved via helper functions? (inherited from the foundation)

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS and storage policies are inspected (see [[2026-05-29 - Supabase Implementation Artifact Gap]]).
- Depends on [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; consumed by every module ADR's write predicates and by [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] for the entitlement-vs-permission boundary.
- Align audit retention and `audit.export` scope with current Cabo Verde fiscal/accounting requirements before production.
