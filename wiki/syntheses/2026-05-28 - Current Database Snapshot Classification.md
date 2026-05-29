---
type: synthesis
status: active
created: 2026-05-28
updated: 2026-05-29
scope: current database snapshot vs target NOVA-ERP architecture
decision_status: provisional
tags: [database, schema, architecture, nova-erp]
sources: ["[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Faturacao Eletronica]]", "[[Permissoes e Auditoria ERP]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
confidence: high
---

# Current Database Snapshot Classification

## Thesis

`raw/assets/DATABASE_ER_DIAGRAM.md` is current-state implementation evidence, not target architecture. NOVA-ERP should mine it for reusable concepts and migration risk, while deriving the target schema from product authority, multi-tenant requirements and fiscal/e-Fatura contracts.

## Context

This synthesis resolves the first resolution criterion in [[Contradiction - Current Database Snapshot vs Target ERP Architecture]]: deep-ingest the database snapshot and classify tables before schema implementation decisions.

## Supporting Evidence

- Evidence: the database snapshot includes useful ERP-adjacent tables for profiles, permissions, documents, document series, financial transactions, inventory, suppliers, e-Fatura settings/logs and private certificate storage.
  Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]]
  Strength: high for current state.

- Evidence: PRD and SSD require a broader multi-tenant ERP with tenant isolation, audit logs, permissions, sales, purchases, inventory, treasury, fiscality, accounting, SAF-T, e-Fatura, HR, assets, projects, subscriptions, dashboards and AI.
  Source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
  Strength: high for target architecture.

- Evidence: e-Fatura v11.0 requires schema/API objects beyond the current `efatura_logs`/`efatura_settings` shape, including DFE payloads, XSD validation, transmission batches, references, contingency, self-billing, rappel periods and signed XML handling.
  Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]], [[Faturacao Eletronica]]
  Strength: high for fiscal integration.

## Counterevidence

- Evidence: the snapshot already has documents, series, financial transactions, inventory movements, e-Fatura logs/settings and certificate bucket, so replacing everything blindly would waste implementation evidence.
  Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]]
  Strength: medium.

## Current Interpretation

- What is known: the current snapshot mixes ERP-adjacent structures with e-commerce/POS structures.
- What is inferred: the safest path is selective adaptation, not wholesale reuse or wholesale deletion.
- What remains unresolved: actual SQL, RLS policies, migrations, production usage and storage policies still need inspection.
- Artifact status: as of 2026-05-29, the vault does not contain the referenced Supabase implementation artifacts. The gap is filed in [[2026-05-29 - Supabase Implementation Artifact Gap]].

## Classification

### Adapt Into Target Core

- `profiles` -> user profiles plus tenant membership boundary.
- `user_roles`, `user_permissions` -> tenant-scoped RBAC/permission model.
- `products` -> tenant-owned products/services/items.
- `suppliers` -> unified entities or supplier master data.
- `documents`, `document_items`, `document_series` -> fiscal document core, heavily refactored.
- `financial_transactions` -> receivables/payables/treasury.
- `inventory_movements`, `inventory_counts`, `inventory_count_items` -> inventory module.
- `bank_accounts` -> tenant-owned bank/treasury configuration.

### Replace Or Split For Compliance

- `efatura_settings` -> tenant e-Fatura configuration, emitter setup, repository, middleware readiness and certificate metadata.
- `efatura_logs` -> DFE payloads, validation results, transmission batches, attempts, responses and events.
- `efatura-certificates` bucket -> secure certificate/keystore storage with strict access policy and metadata-only domain references.

### Optional Or Non-Core

- `conversations`, `chat_messages`, `quick_replies` -> support/communication layer, not ERP foundation.
- `document_email_history`, `document_migration_logs` -> useful audit/operation concepts, but not substitutes for audit logs.

### Archive Or Reframe

- `orders`, `order_items`;
- `reservations`, `reservation_items`, `reservation_history`;
- `wishlist`;
- `product_reviews`;
- `promotional_banners`;
- `shipping_costs`.

These can exist later as optional commerce/customer-portal concepts, but should not shape the ERP foundation.

## Implications

- Product: target workflows should be ERP-first, not e-commerce-first.
- Architecture: `tenant_id`, tenant memberships, audit logs and RLS must be foundational, not bolted onto current tables.
- Data model: fiscal documents need a new model aligned with v11.0, not just `documents.efatura_status`.
- Security/audit: certificate storage and fiscal payload access require explicit policy review.
- Compliance: e-Fatura tables must be rebuilt or split around official schema/API contracts.

## Decision Boundary

- Safe to implement now: use this classification to plan migrations and target schema discussions.
- Do not implement yet: do not treat current table names/enums as final target schema.
- Requires human decision: whether e-commerce/POS tables become an optional commerce module, migration legacy, or deletion candidate.

## Open Questions

- Does the actual database include SQL policies or tables not shown in the diagram?
- Which current tables contain production data that must be migrated?
- Should target schema retain `documents` naming or move to explicit `fiscal_documents`/`commercial_documents` naming?
- What is the first schema decision page: tenant foundation, fiscal documents, or e-Fatura payload/transmission?

## Maintenance Notes

- Update when actual Supabase SQL/migrations/RLS are available and inspected.
- Related artifact-gap entry: [[2026-05-29 - Supabase Implementation Artifact Gap]].
- Related log entry: 2026-05-28 database snapshot ingest/classification.
