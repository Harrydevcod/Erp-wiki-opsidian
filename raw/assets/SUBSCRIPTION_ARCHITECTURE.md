# Subscription Architecture

## Scope

This module implements the enterprise subscription core for the ERP SaaS layer with a multi-tenant design.

The current repository already had a legacy `saas_*` model. The new implementation keeps that namespace for compatibility, but introduces a stronger domain model around:

- plan catalog and price matrix
- flexible entitlements
- subscription lifecycle
- billing runs and recurring invoicing
- financial integration
- access enforcement
- audit and event history

## Core Domains

### Plan Catalog

- `saas_plans`
  Commercial identity and lifecycle of the plan.
- `saas_plan_prices`
  Price matrix per billing frequency and contract rule.
- `saas_plan_entitlements`
  Flexible features, modules, limits, integrations and permissions.

### Add-ons

- `saas_addons`
  Catalog identity for extras.
- `saas_addon_prices`
  Recurring or one-shot pricing.
- `saas_addon_entitlements`
  Extra modules, limits or features unlocked by the add-on.

### Subscription Contract

- `saas_subscriptions`
  Contract header for the tenant.
- `saas_subscription_items`
  Contracted commercial items: base plan, add-ons, extras, discounts.
- `saas_subscription_entitlements`
  Per-subscription overrides for modules, features and limits approved as contractual exceptions.
- `saas_subscription_snapshots`
  Immutable commercial snapshots kept per relevant change.
- `saas_subscription_events`
  Timeline of lifecycle and billing events.

### Billing

- `saas_billing_runs`
  One billing execution per subscription period.
- `saas_billing_run_lines`
  Detailed billed lines.
- `saas_invoices`
  Customer-facing recurring invoice record, linked to financial pending items.

### Usage and Enforcement

- `saas_usage_metrics`
  Periodic usage snapshot per tenant.
- `saas_get_tenant_access`
  Backend access contract for frontend and services.
- `saas_assert_limit`
  Hard/soft limit enforcement entry point.

## Lifecycle

Detailed lifecycle:

- `draft`
- `pending_activation`
- `trialing`
- `active`
- `past_due`
- `suspended`
- `canceled`
- `expired`

Compatibility status for legacy UI:

- `draft` -> `pending`
- `pending_activation` -> `pending`
- `trialing` -> `trial`
- `active` -> `active`
- `past_due` -> `past_due`
- `suspended` -> `suspended`
- `canceled` -> `cancelled`
- `expired` -> `expired`

## Main Flows

### 1. Create Subscription

1. Validate tenant, plan and billing rule.
2. Resolve plan price.
3. Create contract header.
4. Create initial contract item for the plan.
5. Capture commercial snapshot.
6. Record subscription event.
7. Optionally generate the initial billing run.

### 2. Recurring Billing

1. Find subscriptions due for renewal.
2. Resolve active recurring items.
3. Create billing run and lines.
4. Create recurring invoice.
5. Create financial pending transaction.
6. Advance subscription period.
7. Record billing and renewal events.

### 3. Overdue Handling

1. Detect unpaid recurring invoices past due.
2. Move subscription to `past_due` during grace period.
3. Move subscription to `suspended` after grace expiry.
4. Create admin notifications and audit events.

### 4. Reactivation

1. Mark invoice as paid.
2. Mark linked financial transaction as paid.
3. If overdue debt is normalized, restore subscription to `active`.
4. Record payment and reactivation events.

## Central Services

- `saas_create_subscription`
- `saas_generate_billing_run`
- `saas_process_due_renewals`
- `saas_apply_overdue_actions`
- `saas_mark_invoice_paid`
- `saas_get_effective_entitlements`
- `saas_get_tenant_access`
- `saas_assert_limit`
- `saas_refresh_usage_metrics`

## Integrations

### Finance / Treasury

- recurring invoices create entries in `saas_invoices`
- recurring charges also create `financial_transactions` receivables

### Permissions / ERP Access

- frontend consumes `saas_get_tenant_access`
- backend triggers enforce critical hard limits

### Audit

- every relevant lifecycle or billing change creates `saas_subscription_events`
- legacy `saas_subscription_history` is also populated for compatibility

## Phase Delivery

### Phase 1 in this implementation

- plan catalog
- flexible features and limits
- base subscription contract
- recurring billing core
- renewal
- suspension by overdue
- basic access enforcement
- basic KPIs and operational UI
- subscription-level entitlement overrides for enterprise exceptions

### Reserved for next phases

- proration
- downgrade scheduling rules
- add-on commercial automation
- coupons and campaigns
- gateway integrations
- approval workflows for advanced enterprise exceptions
