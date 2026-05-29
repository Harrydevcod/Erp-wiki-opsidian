---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, saas, subscriptions, billing, entitlements, nova-erp]
sources: ["raw/assets/SUBSCRIPTION_ARCHITECTURE.md", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]"]
related: ["[[NOVA-ERP]]", "[[Subscricoes SaaS ERP]]", "[[Permissoes e Auditoria ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Tesouraria ERP]]", "[[Faturacao Eletronica]]", "[[Fiscalidade Cabo Verde]]"]
confidence: medium
---

# Schema Decision - SaaS Subscriptions Billing and Entitlements

## Decision

NOVA-ERP models its own SaaS commercial layer as a platform-owned catalog plus tenant-scoped contracts, with **effective entitlement** computed (not stored) from `plan + add-ons + approved overrides` and frozen into immutable commercial snapshots. Plan catalogs, prices and catalog entitlements are platform-admin-owned global records. Subscriptions, billing runs, invoices, usage metrics and lifecycle events are tenant-scoped but **platform-admin-writable, tenant-read-only**: a tenant can read its effective access but cannot edit its own plan, price, entitlement or billing state. Entitlement is an access *gate* that never bypasses [[Permissoes e Auditoria ERP]] (membership + RBAC + RLS) and never deletes tenant data. Payment status is derived from [[Tesouraria ERP]] or external-provider evidence, never from a hand-edited access flag. The legacy `saas_*` namespace is preserved for compatibility while the domain model is strengthened.

## Scope

- Module: [[Subscricoes SaaS ERP]].
- Tables/objects: `saas_plans`, `saas_plan_prices`, `saas_plan_entitlements`, `saas_addons`, `saas_addon_prices`, `saas_addon_entitlements`, `saas_subscriptions`, `saas_subscription_items`, `saas_subscription_entitlements`, `saas_subscription_snapshots`, `saas_subscription_events`, `saas_billing_runs`, `saas_billing_run_lines`, `saas_invoices`, `saas_usage_metrics`.
- Service contracts (logic, not tables): `saas_get_effective_entitlements`, `saas_get_tenant_access`, `saas_assert_limit`, `saas_create_subscription`, `saas_generate_billing_run`, `saas_process_due_renewals`, `saas_apply_overdue_actions`, `saas_mark_invoice_paid`, `saas_refresh_usage_metrics`.
- Workflows affected: catalog management, subscription creation, recurring billing, renewal, overdue/grace/suspension, reactivation, entitlement evaluation, usage-limit enforcement.
- Tenancy boundary: catalog is global/platform-owned; contracts carry `tenant_id` and follow a modified RLS pattern (see Security) layered on [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]].

## Source Basis

- Architecture source: `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` defines the `saas_*` domain, the eight-state lifecycle, the four main flows (create, recurring billing, overdue, reactivation), the central services and the phase split.
- Product source: PRD/SSD position NOVA-ERP as a multi-tenant SaaS; the subscription layer is the platform business model, not customer ERP billing.
- Official direction: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] requires enterprise quality, tenant isolation and auditability as design constraints.
- Security source: [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] provides the membership-keyed default-deny RLS pattern and the platform-admin boundary this ADR specializes.
- Financial sources: [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]] owns collection/payment status; [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] owns any platform revenue postings.
- Compliance source: current Cabo Verde fiscal rules for SaaS service invoicing, IVA and e-Fatura are **not yet ingested**; fiscal SaaS invoicing scope is unresolved.

## Context

The financial-core, payroll and fixed-assets ADRs cover what tenants do *inside* NOVA-ERP. This ADR covers how NOVA-ERP sells *itself*. The decisive distinction: a tenant is the *subject* of its subscription but not its *owner* — pricing, entitlements and lifecycle are controlled by the platform. This inverts the default tenant-foundation write rule (members manage their own tenant rows) and demands an explicit platform-admin-write / tenant-read RLS split. The source already ships a working `saas_*` model; this ADR commits the target shape and the invariants that keep entitlement from becoming a security or fiscal bypass.

## Data Model

### Catalog (platform-owned, global, no `tenant_id`)

- Entity/table: `saas_plans`
  - Key fields: `id`, `code`, `name`, `status` (`draft|active|retired`), `market`, `display_order`, `created_at`.
  - Constraints: unique `code`; platform-admin write only; readable by authenticated tenants for plan selection.

- Entity/table: `saas_plan_prices`
  - Key fields: `id`, `plan_id`, `billing_frequency` (`monthly|quarterly|annual`), `currency`, `amount`, `contract_term`, `effective_from`, `effective_to`, `status`.
  - Constraints: append-only/effective-dated; price changes never mutate historical rows.

- Entity/table: `saas_plan_entitlements`
  - Key fields: `id`, `plan_id`, `entitlement_key`, `entitlement_kind` (`module|feature|limit|integration`), `limit_value`, `effective_from`, `effective_to`.
  - Purpose: declares what the plan grants without embedding entitlements in subscription rows.

- Entity/table: `saas_addons` / `saas_addon_prices` / `saas_addon_entitlements`
  - Mirror the plan trio for commercial extras: identity, recurring/one-shot pricing, and extra module/feature/limit grants.

### Contract (tenant-scoped)

- Entity/table: `saas_subscriptions`
  - Key fields: `id`, `tenant_id`, `plan_id`, `status` (lifecycle), `billing_frequency`, `currency`, `current_period_start`, `current_period_end`, `trial_ends_at`, `grace_until`, `activated_at`, `canceled_at`, `created_at`.
  - Constraints: at most one non-terminal subscription per tenant unless multi-contract is explicitly enabled; status transitions are guarded (see State).

- Entity/table: `saas_subscription_items`
  - Key fields: `id`, `tenant_id`, `subscription_id`, `item_kind` (`plan|addon|discount|extra`), `ref_id`, `price_id`, `quantity`, `unit_amount`, `recurring`, `effective_from`, `effective_to`.
  - Purpose: the contracted commercial lines that recurring billing resolves.

- Entity/table: `saas_subscription_entitlements`
  - Key fields: `id`, `tenant_id`, `subscription_id`, `entitlement_key`, `entitlement_kind`, `limit_value`, `override_reason`, `approved_by`, `effective_from`, `effective_to`.
  - Constraints: approved enterprise exceptions only; require reason + approver; never widen cross-tenant scope.

- Entity/table: `saas_subscription_snapshots`
  - Key fields: `id`, `tenant_id`, `subscription_id`, `snapshot_reason`, `effective_entitlements_json`, `items_json`, `captured_at`, `captured_by`.
  - Constraints: immutable; captured on every material commercial change for reproducible entitlement history.

- Entity/table: `saas_subscription_events`
  - Key fields: `id`, `tenant_id`, `subscription_id`, `event_type`, `payload_json`, `actor`, `created_at`.
  - Constraints: append-only timeline; legacy `saas_subscription_history` may be populated for UI compatibility but is not the source of truth.

### Billing and usage (tenant-scoped)

- Entity/table: `saas_billing_runs`
  - Key fields: `id`, `tenant_id`, `subscription_id`, `period_start`, `period_end`, `status` (`draft|calculated|issued|settled|past_due|voided`), `total_amount`, `currency`, `created_at`.
  - Constraints: one run per subscription period; idempotent generation keyed by `(subscription_id, period_start)`.

- Entity/table: `saas_billing_run_lines`
  - Key fields: `id`, `tenant_id`, `billing_run_id`, `subscription_item_id`, `description`, `quantity`, `unit_amount`, `line_amount`.
  - Constraints: snapshot pricing at billing time for reproducibility.

- Entity/table: `saas_invoices`
  - Key fields: `id`, `tenant_id`, `billing_run_id`, `document_no`, `status`, `total_amount`, `currency`, `treasury_obligation_ref`, `fiscal_document_ref`, `issued_at`.
  - Constraints: platform billing evidence by default; `fiscal_document_ref` stays null until a fiscal SaaS-invoicing design exists; links to a treasury receivable obligation.

- Entity/table: `saas_usage_metrics`
  - Key fields: `id`, `tenant_id`, `metric_key`, `period_start`, `period_end`, `value`, `captured_at`.
  - Purpose: periodic usage snapshot feeding `saas_assert_limit`.

## State And Events

- State: `saas_subscriptions.status`: `draft -> pending_activation -> trialing -> active`; `active -> past_due -> suspended`; `suspended -> active` on reactivation; `* -> canceled` (intentional) and `active/past_due -> expired` (period end without renewal). Legacy UI may collapse `draft`/`pending_activation` to `pending`, `trialing` to `trial`, `canceled` to `cancelled`; the target vocabulary keeps the precise states.
- State: `saas_billing_runs.status`: `draft -> calculated -> issued -> settled`; `issued -> past_due` on overdue; `* -> voided` only through controlled reversal.
- Events: `saas.plan_created`, `saas.plan_price_changed`, `saas.entitlement_changed`, `saas.subscription_created`, `saas.subscription_activated`, `saas.subscription_changed`, `saas.subscription_snapshot_captured`, `saas.billing_run_created`, `saas.billing_run_issued`, `saas.invoice_created`, `saas.payment_recorded`, `saas.subscription_past_due`, `saas.subscription_suspended`, `saas.subscription_reactivated`, `saas.subscription_cancelled`, `saas.limit_asserted`, `saas.limit_exceeded`.
- Transition rule: lifecycle and billing transitions are driven by services (`saas_process_due_renewals`, `saas_apply_overdue_actions`, `saas_mark_invoice_paid`), each emitting an event and, where commercial terms change, a snapshot. No access flag is edited directly.

## Effective Entitlement Resolution

`saas_get_effective_entitlements(tenant)` resolves, at a point in time:

1. base `saas_plan_entitlements` for the active plan;
2. union with `saas_addon_entitlements` for active add-on items;
3. apply `saas_subscription_entitlements` overrides (approved exceptions win);
4. clamp by lifecycle state (a `suspended` subscription degrades module/feature access while preserving data).

`saas_get_tenant_access` exposes the resolved view to frontend and services; `saas_assert_limit` compares `saas_usage_metrics` against the resolved limit and returns hard-block or soft-warn. Resolution is deterministic and reproducible from the latest snapshot.

## Security, Privacy And Tenancy

- RLS split (specializes [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]):
  - Catalog tables: platform-admin write; read allowed to authenticated users for plan selection.
  - Contract/billing/usage tables: `tenant_id`-scoped read for tenant members with the right permission; **write restricted to platform admins** (and service roles), not tenant members.
- Entitlement is a tenant-level gate; it must not grant cross-tenant access, bypass RBAC/RLS, expose hidden modules to unauthorized users, bypass fiscal/e-Fatura requirements, or delete tenant data on limit breach.
- Access enforcement for critical limits happens server-side; UI gating is UX only.
- Permission keys (suggested): `saas.catalog_manage`, `saas.subscription_view`, `saas.subscription_manage`, `saas.entitlement_override`, `saas.billing_run`, `saas.invoice_view`, `saas.invoice_manage`, `saas.usage_view`. Override and catalog management are platform-admin scoped.
- Billing/commercial data is sensitive and permissioned; suspension affects access, never data integrity.

## Billing, Treasury And Accounting Boundary

- Recurring billing creates a `saas_billing_run` + lines + `saas_invoice`, and a matching receivable obligation in [[Tesouraria ERP]] (`treasury_obligation_ref`).
- Payment status is **derived** from treasury allocations or an external provider's settlement evidence; `saas_mark_invoice_paid` records evidence and lets reactivation read normalized billing state — it does not flip an access boolean by hand.
- Any platform revenue recognition posts through [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] posting rules over `saas.invoice_created` / `saas.payment_recorded` events, never by writing journal lines directly.

## Fiscal Boundary

If NOVA-ERP invoices Cabo Verde customers for its own SaaS, billing may require IVA treatment and e-Fatura submission through [[Faturacao Eletronica]].

Until current fiscal design is explicit:

- `saas_invoices` is platform billing evidence, not automatically a legally issued fiscal document (`fiscal_document_ref` null);
- fiscal SaaS invoices, if required, route through the same fiscal-document engine as tenant business documents, with NOVA-ERP modeled as the seller tenant/config;
- no production claim of SaaS billing compliance without current Cabo Verde fiscal verification.

## Alternatives Considered

- Alternative: store the entitlement set denormalized on `saas_subscriptions`.
  Why not: cannot reproduce historical access, audit changes, or compose plan + add-on + override cleanly.
- Alternative: let tenant admins edit their own plan/entitlements/billing.
  Why not: turns the commercial layer into a self-service privilege-escalation path; platform must own pricing and access.
- Alternative: store payment status as an editable flag on the subscription.
  Why not: decouples access from real treasury/provider evidence; breaks reconciliation and audit.
- Alternative: treat `saas_invoices` as fiscal documents now.
  Why not: Cabo Verde SaaS fiscal treatment is unverified; conflating them risks non-compliant production billing.

## Consequences

- Positive: clean separation of platform commerce from tenant ERP data; reproducible, auditable entitlement history; entitlement cannot become a security or fiscal bypass.
- Positive: catalog evolves via effective-dated rows without rewriting history; lifecycle and billing are service-driven and event-sourced.
- Tradeoff: requires an entitlement resolver, snapshotting and a platform-admin/tenant RLS split beyond the default membership pattern.
- Migration impact: the snapshot already carries a legacy `saas_*` model; namespace preserved, but contracts gain snapshots, computed entitlements and derived payment status.
- Operational impact: overdue/grace/suspension and reactivation need operator workflows and notifications, not just tables.

## Validation Plan

- Test: a tenant member can read effective access but cannot UPDATE/INSERT into `saas_subscriptions`, `saas_subscription_entitlements` or `saas_invoices`.
- Test: tenant A cannot read tenant B's subscription, billing or usage rows.
- Test: catalog tables are platform-admin write only; non-admins get default-deny on write.
- Test: effective entitlements = plan ∪ add-ons with approved overrides winning, reproducible from the latest snapshot.
- Test: `saas_assert_limit` hard-blocks over a hard limit and soft-warns over a soft limit using `saas_usage_metrics`.
- Test: suspension degrades module/feature access while leaving tenant data intact and readable after reactivation.
- Test: marking an invoice paid requires treasury/provider evidence; reactivation only succeeds when billing state is normalized.
- Test: billing run generation is idempotent per `(subscription_id, period_start)`.

## Open Questions

- Should NOVA-ERP invoice its own SaaS subscriptions through its fiscal module, an external provider, or platform-billing-only?
- Which launch plans, modules, add-ons and limits are required, and which limits are hard-blocking vs soft-warning?
- What grace period and suspension model applies to overdue tenants?
- Should platform billing collection run through [[Tesouraria ERP]], an external gateway, or both?
- Who may approve subscription-level entitlement overrides, and what approval workflow is required?
- How is platform-admin access separated from tenant-admin access at the auth/RLS layer?
- Is multi-contract per tenant ever required, or is single active subscription sufficient for launch?

## Maintenance Notes

- Update after current Cabo Verde SaaS-invoicing/IVA/e-Fatura sources are ingested and after `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` is filed as a full source page.
- Depends on the tenant-foundation RLS pattern; integrates with [[Tesouraria ERP]] (collection) and [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] (revenue). Revisit when actual Supabase migrations/RLS for `saas_*` are available (see [[2026-05-29 - Supabase Implementation Artifact Gap]]).
