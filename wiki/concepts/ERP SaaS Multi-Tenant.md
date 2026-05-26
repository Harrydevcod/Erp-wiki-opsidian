---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [erp, saas, multi-tenant, architecture]
sources: ["raw/assets/SSD/PRD.MD", "raw/assets/SSD/PROMPT.MD", "raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD", "raw/assets/SUBSCRIPTION_ARCHITECTURE.md"]
related: ["[[NOVA-ERP]]", "[[Supabase Deployment]]"]
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

## Evidence

- Evidence: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Evidence: `raw/assets/SSD/PRD.MD`
- Evidence: `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`

## Open Questions

- Should tenant isolation be enforced primarily through Supabase RLS, backend service functions, or both?
- Which entities are global catalog data versus tenant-owned data?

