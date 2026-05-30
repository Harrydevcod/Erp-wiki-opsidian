---
type: synthesis
status: active
created: 2026-05-30
updated: 2026-05-30
scope: NOVA-ERP target schema ADRs vs actual Supabase migrations
decision_status: reconciliation
tags: [schema, architecture, supabase, migrations, rls, implementation-review, nova-erp]
sources: ["nova-erp/supabase/migrations/00001_core_schema.sql", "nova-erp/supabase/migrations/00002_iam_schema.sql", "nova-erp/supabase/migrations/00003_crm_schema.sql", "nova-erp/supabase/migrations/00004_documents_schema.sql", "nova-erp/supabase/migrations/00005_fiscal_schema.sql", "nova-erp/supabase/migrations/00006_inventory_schema.sql", "nova-erp/supabase/migrations/00007_accounting_schema.sql", "nova-erp/supabase/migrations/00008_treasury_schema.sql", "nova-erp/supabase/migrations/00009_hr_schema.sql", "nova-erp/supabase/migrations/00010_rls_policies.sql", "nova-erp/supabase/migrations/00011_seeds.sql", "nova-erp/supabase/migrations/20260404100000_align_domain_schema.sql", "nova-erp/supabase/migrations/20260422100000_fiscal_documents_base.sql"]
related: ["[[2026-05-29 - Supabase Implementation Artifact Gap]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]", "[[2026-05-29 - Schema Decision - Project and Analytical Dimensions]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[Contradiction - Inventory Stored Stock vs Derived Movement Ledger]]", "[[Contradiction - Stored Payment Status vs Derived from Allocations]]", "[[Contradiction - DB-Layer Authorization and RLS Permission Gating]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: high
---

# ADR vs Implementation Reconciliation — Supabase Migrations

## Thesis

The NOVA-ERP implementation repository is now available in the workspace (`nova-erp/supabase/migrations`, `nova-erp/supabase/functions`), closing [[2026-05-29 - Supabase Implementation Artifact Gap]]. Reading the **13 migrations** against the provisional target-schema ADR sequence shows the implementation is a **simpler, accumulator-and-procedure shaped schema** than the ADRs designed. Tenant isolation is sound; several ADR core principles — derived-not-stored ledgers, the commercial/fiscal document split, DB-layer permission gating, the generic dimension layer — are **not** implemented, and three modules (fixed assets, analytical dimensions, reporting/AI) are absent.

This is a reconciliation map, not a verdict on which side is right. Each divergence is a decision the founder must take per area: **conform the implementation to the ADR**, or **amend the ADR to match the shipped reality**.

## Implementation Inventory (evidence)

13 migrations, 42 RLS-enabled tables, 44 policies. Tables by domain:

- **Core (00001):** `countries, currencies, tenants, tenant_settings, saas_plans, subscriptions, series, jobs, audit_logs, notifications`
- **IAM (00002):** `profiles, roles, permissions, role_permissions, memberships` + fns `get_user_tenants, get_user_permissions, get_active_tenant_id, set_tenant_context, handle_new_user`
- **CRM (00003):** `entities, entity_addresses, entity_contacts` (+ enums `entity_kind, entity_role`)
- **Documents (00004):** `document_types, documents, document_lines, document_relations`
- **Fiscal (00005):** `tax_regimes, vat_rates, vat_transactions, efatura_transmissions, certificates, saft_exports, efatura_settings, self_billing_agreements`
- **Inventory (00006):** `product_families, products, services, warehouses, stock_items, stock_movements` (+ trigger fn `update_stock_on_movement`)
- **Accounting (00007):** `chart_of_accounts, cost_centers, journals, ledger_entries, accounting_periods`
- **Treasury (00008):** `bank_accounts, cash_accounts, payments, payment_allocations, advances, bank_reconciliations`
- **HR (00009):** `employees, employee_contracts, payroll_runs, payroll_run_lines, hr_legal_params, employee_absences`
- **RLS (00010):** 44 policies / 42 tables
- **Seeds (00011)**; **align_domain (2026-04-04):** fns `receive_purchase_document, settle_document`; **fiscal_documents_base (2026-04-22):** `efatura_type_mappings, fiscal_document_events, fiscal_document_errors` + `fn_block_doc_type_code_change`.

## Reconciliation Matrix

| Area | ADR design intent | Implementation reality | Verdict |
|---|---|---|---|
| **Tenant isolation** ([[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]) | default-deny, **membership-keyed** RLS, never raw `auth.uid()` | `tenant_id = get_active_tenant_id()`; `get_active_tenant_id()` **re-validates active membership** every call; `set_tenant_context` validates membership before setting the `app.tenant_id` GUC | **MATCH (principle)** via active-tenant indirection — isolation is sound, not a hole |
| **DB-layer authorization** ([[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]) | `has_permission()`-gated writes; `user_permission_overrides` (revoke-wins); graduated evidence tiers; FORCE/service-role boundary | 41 `FOR ALL` policies check **only tenant** → any active member has full CRUD; permissions **not** enforced in RLS; **no `user_permission_overrides`**; no evidence tiers; **no `FORCE ROW LEVEL SECURITY`**, policies untargeted (`service_role`/owner bypass) | **DIVERGENCE** → [[Contradiction - DB-Layer Authorization and RLS Permission Gating]] |
| **Audit** | single append-only `audit_log`; hash/reference payloads | `audit_logs` append-only (UPDATE/DELETE revoked) ✓; stores full `before_data`/`after_data` JSONB | **MATCH** (minor variance: full JSONB vs hash/reference) |
| **Document core** ([[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]) | **split** `commercial_documents` / `fiscal_documents`; `document_links` graph; independent numbering | **single `documents`** table for all types; `document_relations` (= links graph, renamed; enum `converted_to/corrected_by/paid_by/grouped_in`); single `series` | **DIVERGENCE**: one-table model; no commercial/fiscal split |
| **Payment status** (doc + [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]) | **derived** from allocations, never a stored boolean; no `paid` flag on documents | `documents.status` includes `paid/partial_paid/overdue`; `settle_document()` locks the doc and **writes status back** (stored) | **DIVERGENCE** → [[Contradiction - Stored Payment Status vs Derived from Allocations]] |
| **Treasury** | `obligations` + `treasury_movements` + m:n `allocations`; reversals = compensating rows | `payments` + `payment_allocations` + `advances` + `bank/cash_accounts` + `bank_reconciliations`; **no `obligations` table** (the document is the implicit obligation) | **PARTIAL**: movement+allocation present; obligation layer collapsed into the document |
| **Inventory** ([[2026-05-28 - Schema Decision - Inventory Movements and Valuation]]) | stock **derived** from append-only movement ledger; **no stored quantity**; `valuation_layers`; reservations ledger; `stock_counts`; lots/serials | `stock_items` with **stored `qty_on_hand`/`qty_reserved`/`avg_cost`** mutated by `update_stock_on_movement` trigger (INSERT-only); no valuation layers; no reservation ledger; no counts/lots/serials | **MAJOR DIVERGENCE** (ships the ADR's explicitly-rejected snapshot alternative) → [[Contradiction - Inventory Stored Stock vs Derived Movement Ledger]] |
| **Accounting** ([[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]) | immutable double-entry journal; projection-based balances (no stored balance); period locks; tax maps | `ledger_entries` (debit/credit, **no stored balance** ✓), `journals.status`, `accounting_periods` ✓; **concrete `cost_center_id`** FK; **no immutability trigger** | **PARTIAL MATCH**: projection balances + periods ✓; immutability unenforced; cost via concrete cost center |
| **Analytical dimensions** ([[2026-05-29 - Schema Decision - Project and Analytical Dimensions]]) | generic `analytical_dimensions` + `dimension_values` + polymorphic `dimension_tags`; projects extend; tag from day one | only concrete `cost_centers`; **no generic dimension layer**; **no projects** | **DIVERGENCE / GAP** |
| **Fixed assets** ([[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]) | lifecycle register separate from inventory; depreciation runs; accounting events | **absent entirely** (0 tables, 0 references) | **GAP (not built)** |
| **SaaS subscriptions** | platform catalog + tenant contracts + computed entitlements + immutable snapshots | `saas_plans` + `subscriptions` in core; minimal | **PARTIAL / GAP**: no entitlement computation or snapshots |
| **e-Fatura** (DFE/events/middleware/evidence ADRs) | separated DFE payload / transmission / validation / events / contingency / cert secrets | `efatura_transmissions, certificates, efatura_settings, self_billing_agreements` + `efatura_type_mappings, fiscal_document_events, fiscal_document_errors` | **PARTIAL MATCH**: transmission/events/settings/cert present; granularity differs |
| **Reporting / AI** | `reporting_datasets`, KPI defs, `ai_safe` contract | absent (0) | **GAP (future layer, expected)** |

## Current Interpretation

- **Known (high confidence):** the table/function/policy facts above are read directly from the migrations.
- **Pattern:** the implementation consistently prefers **stored accumulators maintained by triggers/procedures** (stock_items, documents.status via settle_document) over the ADRs' **derived-from-immutable-ledger** stance. This is the single recurring philosophical split and the root of the three contradiction pages.
- **Authorization:** tenant isolation is genuinely enforced; **role/permission authorization is not at the DB layer** — it must be enforced in the application/Edge layer, which is unverified here.
- **Unresolved:** whether the divergences are deliberate MVP simplifications (ship-now, harden-later) or drift to be corrected. That is a founder decision per area.

## Implementation Consequence

- The provisional ADRs remain the **design target**; they are not invalidated, but each now has a concrete `implementation_status`: MATCH / PARTIAL / DIVERGENCE / GAP (above).
- **SAF-T CV risk:** the stored-stock and single-document-table choices are the two most likely to break SAF-T inventory/audit-trail expectations (see [[SAF-T CV]] and [[2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema]]); flagged for the founder.
- Three contradiction pages track the material conflicts; gaps (assets, dimensions, reporting/AI, entitlements) are tracked in the index Maintenance Queue.

## Open Questions

- Are the stored-accumulator choices an intentional MVP posture, or drift? (decides conform-vs-amend for inventory, payment status)
- Is DB-layer permission gating intended, or is app/Edge-layer enforcement the accepted boundary? If the latter, the foundation/permission ADRs should be amended and the Edge Functions audited for it.
- Should `FORCE ROW LEVEL SECURITY` + `TO authenticated` targeting be added to harden the service-role boundary?
- When do fixed assets, analytical dimensions and the reporting/AI layers enter the build roadmap?

## Maintenance Notes

- Supersedes the "artifacts unavailable" state of [[2026-05-29 - Supabase Implementation Artifact Gap]] (now updated to reference this reconciliation).
- Edge Functions (`audit-log`, `create-user`, `numbering`, `_shared`) and storage policies **have now been reviewed** in [[2026-05-30 - Edge Function and Storage Security Review]] — finding: all three functions run on the service-role key and trust body `tenant_id` with **no caller authorization check** (critical for `create-user`); no storage bucket policies in migrations. This sharpens the DB-layer authorization contradiction: authorization is missing at *both* layers for these operations.
- Migrations were read read-only; no implementation files were modified.
