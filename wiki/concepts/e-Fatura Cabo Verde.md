---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [efatura, cabo-verde, dnre, dfe, compliance]
sources: ["docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf", "raw/assets/SSD/PRD.MD", "raw/assets/LOCAL_SETUP-Arydson.md"]
related: ["[[Fiscalidade Cabo Verde]]", "[[NOVA-ERP]]", "[[Supabase Deployment]]"]
confidence: high
---

# e-Fatura Cabo Verde

## Definition

e-Fatura Cabo Verde is the electronic invoice domain for Cabo Verde fiscal documents, involving DNRE-compatible document generation, communication, security, processing, status handling and contingency/retry flows.

## Current Synthesis

For [[NOVA-ERP]], e-Fatura should be designed as an asynchronous integration with strong auditability. The product backlog and setup notes point to digital credentials/certificates, XML/DFE generation, middleware communication, request/response history, document technical states, rejection reasons, controlled reprocessing and contingency mode.

The local setup notes also indicate an OAuth callback through Supabase Edge Functions for e-Fatura integration.

## Evidence

- Evidence: `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`
- Evidence: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Evidence: `raw/assets/LOCAL_SETUP-Arydson.md`

## Open Questions

- What exact DNRE endpoints, certificate formats and authentication methods are current in 2026?
- Should e-Fatura submission be modeled as a queue from the first release?

