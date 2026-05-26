---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [supabase, deployment, edge-functions, database]
sources: ["raw/assets/SUPABASE_DEPLOY.md", "raw/assets/LOCAL_SETUP.md", "raw/assets/LOCAL_SETUP-Arydson.md", "raw/assets/DATABASE_ER_DIAGRAM.md"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[e-Fatura Cabo Verde]]"]
confidence: high
---

# Supabase Deployment

## Definition

Supabase Deployment is the operational process for running the NOVA-ERP backend stack: database schema, migrations, RLS, policies, triggers, storage, Edge Functions, secrets and frontend environment variables.

## Current Synthesis

The project is intended to run as a normal React + Supabase application outside Lovable. Local setup uses Node.js, npm, Git, Docker Desktop and Supabase CLI. Remote deployment links a Supabase project, pushes migrations and seed data, configures SQL webhooks for Edge Functions, sets function secrets, deploys functions, and configures frontend variables.

Important deployment distinction: frontend should use the Supabase publishable key, while some Edge Function flows still require the legacy anon JWT key for compatibility.

## Evidence

- Evidence: `raw/assets/SUPABASE_DEPLOY.md`
- Evidence: `raw/assets/LOCAL_SETUP.md`
- Evidence: `raw/assets/LOCAL_SETUP-Arydson.md`

## Open Questions

- Which secrets are production-critical and need rotation policy?
- Should webhook secret configuration be automated as a repeatable deploy script?

