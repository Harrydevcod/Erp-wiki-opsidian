---
type: source
status: active
created: 2026-05-28
updated: 2026-05-28
source_path: raw/assets/DATABASE_ER_DIAGRAM.md
source_type: database-snapshot
author:
published: 2026-01
ingested: 2026-05-28
tags: [source, database, schema, supabase, nova-erp]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]", "[[2026-05-28 - Current Database Snapshot Classification]]"]
confidence: high
---

# DATABASE ER Diagram Snapshot

## Source Role

This source documents the current database snapshot for NOVA-ERP-related work. It is useful implementation evidence, but not target architecture authority.

Source: `raw/assets/DATABASE_ER_DIAGRAM.md`

## Summary

The ER diagram describes a current Supabase/PostgreSQL schema centered on users/profiles, e-commerce orders, reservations, products, POS clients, fiscal documents, financial transactions, inventory counts/movements, reviews, wishlist, chat/support, suppliers, company settings, e-Fatura settings/logs and storage buckets.

The schema contains useful foundations for identity, documents, inventory, financial transactions, certificates and support workflows. It also contains strong e-commerce/POS concepts that do not map cleanly to the target NOVA-ERP ERP architecture.

## Authority And Currency

- Authority level: high as current-state schema evidence.
- Date/currency: source says last updated January 2026.
- Compliance sensitivity: medium/high because it includes fiscal documents, e-Fatura logs/settings and certificate storage.
- Supersedes: no known source.
- Superseded by: not superseded, but constrained by [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]] and official e-Fatura sources.

## Tables Captured

Core identity and access:

- `profiles`;
- `user_roles`;
- `user_permissions`;
- `pos_clients`.

Commercial/e-commerce:

- `products`;
- `orders`;
- `order_items`;
- `reservations`;
- `reservation_items`;
- `reservation_history`;
- `wishlist`;
- `product_reviews`;
- `promotional_banners`;
- `shipping_costs`.

Fiscal documents:

- `documents`;
- `document_items`;
- `document_series`;
- `document_email_history`;
- `document_migration_logs`;
- `efatura_logs`;
- `efatura_settings`.

Finance and banking:

- `financial_transactions`;
- `bank_accounts`.

Inventory and suppliers:

- `inventory_movements`;
- `inventory_counts`;
- `inventory_count_items`;
- `suppliers`.

Communication:

- `conversations`;
- `chat_messages`;
- `quick_replies`.

Configuration:

- `company_settings`.

## Enums Captured

- `app_role`: `admin`, `user`;
- `document_type`: `invoice`, `proforma`, `proposal`, `receipt`, `credit_note`, `return_note`, `tve`, `transport_guide`, `simple_receipt`, `work_order`, `delivery_note`, `purchase_order`;
- `document_status`: `draft`, `pending`, `confirmed`, `cancelled`, `paid`;
- `transaction_type`: `receivable`, `payable`;
- `transaction_status`: `pending`, `partial`, `paid`, `overdue`, `cancelled`;
- `recurrence_type`: `none`, `weekly`, `monthly`, `quarterly`, `yearly`.

## Storage Buckets Captured

Public:

- `product-images`;
- `avatars`;
- `company-assets`.

Private:

- `payment-proofs`;
- `chat-attachments`;
- `service-attachments`;
- `efatura-certificates`.

## Implementation-Relevant Details

- The schema has no explicit `tenants`, `tenant_memberships`, `audit_logs`, `subscriptions`, `feature_flags`, accounting, payroll, assets, projects or SAF-T entities in the diagram.
- `profiles`, `user_roles` and `user_permissions` are user-centered, not clearly tenant-membership-centered.
- `documents`, `document_items` and `document_series` are the closest current fiscal-document base, but do not yet reflect the v11.0 DFE/IUD/LED/transmission model.
- `efatura_logs`, `efatura_settings` and `efatura-certificates` are useful signals, but too coarse for the v11.0 e-Fatura schema/API contract.
- `financial_transactions` can inspire receivable/payable modeling, but target treasury needs tenant, document, payment, allocation and bank reconciliation boundaries.
- `inventory_movements`, `inventory_counts` and `suppliers` are useful ERP seeds, but need warehouse, valuation, lot/serial and tenant ownership decisions.
- E-commerce/POS objects (`orders`, `reservations`, `wishlist`, `product_reviews`, `promotional_banners`, `shipping_costs`) should not drive the target ERP core.

## Domain Implications

- Product: do not let current e-commerce/POS workflows define the ERP product surface.
- Architecture: use the snapshot as migration/current-state evidence, not as canonical schema.
- Security/audit: every reusable table must be checked for tenant isolation, RLS, auditability and secret handling.
- Data model: classify tables as keep, adapt, migrate, archive or delete before implementation.
- UX/workflow: customer ordering/reservation UX should be separated from ERP sales, purchases, fiscal documents and treasury.

## Table Classification Draft

Keep/adapt candidates:

- `profiles` - adapt into user profile plus tenant membership model.
- `user_roles` and `user_permissions` - adapt into tenant-scoped RBAC/permissions.
- `products` - adapt into tenant-owned items/products/services.
- `suppliers` - adapt into unified entities or supplier master data.
- `documents`, `document_items`, `document_series` - adapt heavily for fiscal document core.
- `financial_transactions` - adapt into receivables/payables/treasury.
- `inventory_movements`, `inventory_counts`, `inventory_count_items` - adapt into inventory module.
- `bank_accounts` - adapt into tenant-owned treasury/bank configuration.
- `efatura_logs`, `efatura_settings`, `efatura-certificates` - replace or split into implementation-grade e-Fatura objects.
- `conversations`, `chat_messages`, `quick_replies` - optional support/communication module; not ERP core.

Archive/delete candidates unless product direction reintroduces them:

- `orders`;
- `order_items`;
- `reservations`;
- `reservation_items`;
- `reservation_history`;
- `wishlist`;
- `product_reviews`;
- `promotional_banners`;
- `shipping_costs`.

Needs investigation:

- `company_settings` - may become tenant/company settings, but current shape is unknown.
- `document_email_history` and `document_migration_logs` - useful, but need audit/security review.
- storage buckets - public/private posture must be checked against privacy, certificate and fiscal retention requirements.

## Contradictions Or Tensions

See [[Contradiction - Current Database Snapshot vs Target ERP Architecture]].

## Legal/Fiscal Uncertainty

- `documents`, `document_series`, `efatura_logs`, `efatura_settings` and `efatura-certificates` cannot be assumed compliant with v11.0 e-Fatura.
- Evidence needed: actual SQL schema, RLS policies, storage policies, Edge Functions and current migrations.

## Follow-up Questions

- Does the real database include tables omitted from the diagram?
- Which tables are currently in production use?
- Are RLS policies already tenant-safe?
- Should current e-commerce/POS tables be migrated into optional commerce modules or removed from the ERP target?

