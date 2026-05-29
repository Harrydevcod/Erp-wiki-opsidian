---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp, saas, multi-tenant, architecture]
sources: ["raw/assets/SSD/PRD.MD", "raw/assets/SSD/PROMPT.MD", "raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD", "raw/assets/SUBSCRIPTION_ARCHITECTURE.md", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]"]
related: ["[[NOVA-ERP]]", "[[Supabase Deployment]]", "[[Permissoes e Auditoria ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]"]
confidence: high
---

# ERP SaaS Multi-Tenant

## Definition

An ERP SaaS multi-tenant architecture supports multiple companies/tenants in one platform while strictly isolating data, permissions, configuration, billing and operational context per tenant.

## Current Synthesis

For [[NOVA-ERP]], multi-tenancy is not a UI switch. It is a foundational constraint: tenant creation, onboarding, user membership, permissions, audit logs, fiscal setup, series, taxes, documents, inventory, treasury and reporting must all be evaluated inside tenant context.

The backlog explicitly requires:

- unique `tenant_id`;
- initial admin user;
- setup state before operational activation;
- user invitations tied to tenant;
- switching between companies without new login;
- no data leakage between tenants;
- tenant-aware permissions;
- audit logging of critical actions.

[[2026-05-28 - DATABASE ER Diagram Snapshot]] shows a current schema centered on profiles, user roles/permissions, products, orders, reservations, documents, financial transactions, inventory and e-Fatura settings/logs. That snapshot is useful current-state evidence, but [[2026-05-28 - Current Database Snapshot Classification]] concludes it is not target architecture: the target NOVA-ERP foundation still needs explicit tenants, tenant memberships, tenant-scoped permissions, audit logs, RLS posture, subscriptions/entitlements and fiscal/e-Fatura structures aligned with official contracts.

## Evidence

- Evidence: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Evidence: `raw/assets/SSD/PRD.MD`
- Evidence: `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`
- Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]]
- Source: [[2026-05-28 - Current Database Snapshot Classification]]

## Implementation Implications

- Product: current e-commerce/POS tables should not define the ERP-first product model.
- Architecture: target schema must begin with tenant, membership, permissions and audit primitives.
- Data model: current user-centered RBAC must be adapted into tenant-scoped RBAC.
- Security/audit: RLS policies and storage policies need direct inspection before reuse.
- Compliance: current document/e-Fatura tables must be reconciled with v11.0 schema/API requirements before reuse.

## Target Foundation Decision

The provisional target foundation is now specified in [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]: single-DB with default-deny, membership-keyed RLS; explicit `tenants`/`tenant_members`/`roles`/`permissions`/`role_permissions`/`profiles`/`audit_log`/`platform_admins`; SECURITY DEFINER membership helpers; append-only audit; platform-admin as an out-of-band allowlist. Every later module schema inherits this pattern.

## Open Questions

- Should tenant isolation be enforced primarily through Supabase RLS, backend service functions, or both? (Provisionally resolved as RLS-primary + service-role for privileged paths in the foundation ADR; revisit if performance requires JWT-claim denormalization.)
- Which entities are global catalog data versus tenant-owned data?
- Which current database tables are production data that must be migrated instead of discarded?

