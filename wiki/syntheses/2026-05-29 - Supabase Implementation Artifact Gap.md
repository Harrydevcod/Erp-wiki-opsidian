---
type: synthesis
status: active
created: 2026-05-29
updated: 2026-05-29
scope: Supabase implementation artifact availability
decision_status: evidence-gap
tags: [supabase, database, rls, storage, edge-functions, implementation-gap]
sources: ["[[2026-05-28 - Supabase Deploy]]", "raw/assets/LOCAL_SETUP.md", "raw/assets/LOCAL_SETUP-Arydson.md", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]"]
related: ["[[Supabase Deployment]]", "[[Contradiction - Current Database Snapshot vs Target ERP Architecture]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]"]
confidence: high
---

# Supabase Implementation Artifact Gap

## Thesis

The vault does not currently contain the actual Supabase implementation artifacts required for security and migration review: SQL migrations, RLS policies, storage policies, Edge Functions or seed files.

`raw/assets/SUPABASE_DEPLOY.md`, `raw/assets/LOCAL_SETUP.md` and `raw/assets/LOCAL_SETUP-Arydson.md` all assert that the implementation repository has `supabase/migrations`, `supabase/functions` and `supabase/seed.sql`, but those paths are not present in this vault.

## Evidence

- Workspace inspection on 2026-05-29 found no `.sql` files and no `supabase/` implementation directory in the vault.
- The local setup guides say migrations live in `supabase/migrations` and Edge Functions live in `supabase/functions`.
  Evidence: `raw/assets/LOCAL_SETUP.md`, `raw/assets/LOCAL_SETUP-Arydson.md`
- The deployment guide says schema, RLS, policies, triggers and storage are applied with Supabase migrations.
  Source: [[2026-05-28 - Supabase Deploy]]
- The ER diagram is only a documentation snapshot; it is not executable DDL and does not expose actual RLS/storage policies.
  Source: [[2026-05-28 - DATABASE ER Diagram Snapshot]], [[2026-05-28 - Current Database Snapshot Classification]]

## Current Interpretation

- What is known: the vault has enough evidence to classify the current schema conceptually and produce provisional target ADRs.
- What is inferred: the implementation artifacts probably live outside this wiki, likely in the application repository that was separated from Lovable.
- What remains unresolved: whether the real migrations match the ER diagram, whether RLS is enabled on every tenant-owned table, whether storage policies are private where required, and whether Edge Functions preserve actor/tenant attribution.

## Implementation Consequence

Do not mark SQL/RLS/storage review as complete from this vault alone. The next implementation-grade review requires at least one of:

- the application repository containing `supabase/migrations`, `supabase/functions` and `supabase/seed.sql`;
- a Supabase schema dump plus policies/functions/storage metadata;
- a migration bundle exported from the current implementation project.

## Minimum Review Checklist Once Artifacts Arrive

- Enumerate every migration in timestamp order.
- Confirm RLS is enabled for tenant-owned tables and disabled only with explicit rationale.
- Inspect every policy for tenant membership, role and service-role bypass behavior.
- Inspect storage bucket creation and policies, especially fiscal, certificate, payroll, payment and private tenant artifacts.
- Inspect Edge Functions for authentication, tenant derivation, permission checks, service-role use and audit writes.
- Compare real table/enum/function names against the provisional schema ADRs.
- Produce a migration/reuse decision: keep, adapt, replace/split, archive or delete.

## Maintenance Notes

- This page should be superseded or updated once the implementation repository or SQL dump is available.
- This evidence gap keeps [[Contradiction - Current Database Snapshot vs Target ERP Architecture]] active for implementation review, even though the main target-schema ADR sequence has started.
