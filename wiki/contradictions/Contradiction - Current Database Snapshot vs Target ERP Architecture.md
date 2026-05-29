---
type: contradiction
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [contradiction, database, architecture, nova-erp]
sources: ["[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[Revisao Raw Assets - 2026-05-26]]", "[[Faturacao Eletronica]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
confidence: high
---

# Contradiction - Current Database Snapshot vs Target ERP Architecture

## Disputed Claim

Whether `raw/assets/DATABASE_ER_DIAGRAM.md` should be treated as the target database architecture for NOVA-ERP.

## Position A

- Claim: the ER diagram is useful implementation evidence.
- Evidence: it documents a real/current schema with users, profiles, documents, financial transactions, inventory movements, e-Fatura settings/logs and storage buckets.
- Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]]
- Strength: high for current-state inventory, low for target architecture authority.

## Position B

- Claim: canonical product sources require a multi-tenant ERP domain with tenant-scoped modules, permissions, audit logs, sales, purchases, inventory, treasury, fiscality, accounting, SAF-T, e-Fatura, HR, assets, projects, subscriptions, dashboards and AI.
- Evidence: PRD, SSD and backlog define broader ERP architecture; the ER diagram contains e-commerce/POS concepts such as orders, reservations, wishlist, reviews, promotional banners and shipping costs that do not map cleanly to the target ERP core.
- Source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- Strength: high for target product direction.

## Current Best Interpretation

Treat `DATABASE_ER_DIAGRAM.md` as current-state implementation evidence, not target architecture. It can inform migration and reuse, but the target schema should be derived from PRD, SSD, backlog, implementation prompt, domain module pages and official fiscal/e-Fatura contracts.

The first classification is now filed in [[2026-05-28 - Current Database Snapshot Classification]].

The actual SQL/RLS/storage review remains blocked because this vault does not contain the referenced `supabase/migrations`, `supabase/functions` or `supabase/seed.sql` artifacts. That artifact gap is filed in [[2026-05-29 - Supabase Implementation Artifact Gap]].

## Implementation Risk

- Product: copying the current schema could preserve e-commerce/POS behavior instead of ERP workflows.
- Architecture: target modules, tenant isolation and audit boundaries could be constrained by accidental legacy shape.
- Data model: tables must be classified as keep, adapt, migrate, archive or delete before schema implementation.
- Security/audit: current RLS/audit posture must be verified instead of assumed.
- Compliance: fiscal/e-Fatura tables must be reconciled with v11.0 and XSD contracts before reuse.

## Resolution Criteria

- Deep-ingest `DATABASE_ER_DIAGRAM.md`. Done: [[2026-05-28 - DATABASE ER Diagram Snapshot]].
- Compare every table against the target module model.
- Classify tables as keep, adapt, migrate, archive or delete. First pass done: [[2026-05-28 - Current Database Snapshot Classification]].
- Produce a target schema ADR before implementation. Financial core target ADR sequence done through [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]].
- Obtain the actual Supabase implementation artifacts or schema/policy dump before claiming implementation review is complete. Blocked by [[2026-05-29 - Supabase Implementation Artifact Gap]].
- Safe temporary posture: use current schema only as evidence; do not treat it as target architecture.

## Status History

- Date: 2026-05-28
  Change: Normalized contradiction with implementation risk and resolution criteria.
  Source: `raw/assets/DATABASE_ER_DIAGRAM.md`, [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Date: 2026-05-28
  Change: Deep-ingested the database ER snapshot and added first table classification synthesis.
  Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]], [[2026-05-28 - Current Database Snapshot Classification]]
- Date: 2026-05-28
  Change: Produced the first target schema ADR (tenant foundation, RBAC, audit log, RLS pattern) from the classification. Remaining gap is now actual SQL/RLS inspection plus per-module target schemas.
  Source: [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]
- Date: 2026-05-29
  Change: Inspected the vault for implementation artifacts and confirmed the actual Supabase migrations/functions/seed are not present here; the SQL/RLS/storage review is blocked until the implementation repository or export is available.
  Source: [[2026-05-29 - Supabase Implementation Artifact Gap]]
