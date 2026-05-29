---
type: entity
status: active
created: 2026-05-26
updated: 2026-05-28
entity_type: backend platform
tags: [supabase, postgres, auth, edge-functions, rls, storage]
sources: ["[[2026-05-28 - Supabase Deploy]]", "raw/assets/LOCAL_SETUP.md", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]"]
related: ["[[Supabase Deployment]]", "[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]"]
confidence: high
---

# Supabase

## Snapshot

Supabase is the selected backend platform for NOVA-ERP, covering PostgreSQL, Auth, migrations, RLS/policies, storage, triggers and Edge Functions.

## Known Facts

- The setup and deploy guides assume Supabase CLI, database migrations, seed data, Edge Functions and frontend environment variables.
  Source: [[2026-05-28 - Supabase Deploy]], `raw/assets/LOCAL_SETUP.md`
  Confidence: high

- For NOVA-ERP, Supabase is a security boundary: RLS, storage policies, service-role isolation and Edge Function authorization must enforce tenant isolation and auditability.
  Source: [[Supabase Deployment]], [[ERP SaaS Multi-Tenant]], [[Permissoes e Auditoria ERP]]
  Confidence: high

## Relationships

- Related to: [[NOVA-ERP]]
  Nature of relationship: backend platform.
- Related to: [[Supabase Deployment]]
  Nature of relationship: operational deployment and runtime boundary.
