---
type: entity
status: active
created: 2026-05-26
updated: 2026-05-26
entity_type: backend platform
tags: [supabase, postgres, auth, edge-functions]
sources: ["raw/assets/SUPABASE_DEPLOY.md", "raw/assets/LOCAL_SETUP.md", "raw/assets/DATABASE_ER_DIAGRAM.md"]
related: ["[[Supabase Deployment]]", "[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# Supabase

## Snapshot

Supabase is the selected backend platform for NOVA-ERP, covering PostgreSQL, Auth, migrations, RLS/policies, storage and Edge Functions.

## Known Facts

- The setup and deploy guides assume Supabase CLI, database migrations, seed data, Edge Functions and frontend environment variables.
  Source: `raw/assets/SUPABASE_DEPLOY.md`, `raw/assets/LOCAL_SETUP.md`
  Confidence: high

## Relationships

- Related to: [[NOVA-ERP]]
  Nature of relationship: backend platform.

