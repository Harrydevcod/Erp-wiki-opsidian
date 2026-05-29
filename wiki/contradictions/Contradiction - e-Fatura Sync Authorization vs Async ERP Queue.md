---
type: contradiction
status: active
created: 2026-05-27
updated: 2026-05-28
tags: [contradiction, efatura, architecture, integration]
sources: ["[[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]"]
related: ["[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[NOVA-ERP]]"]
confidence: high
---

# Contradiction - e-Fatura Sync Authorization vs Async ERP Queue

## Disputed Claim

Should NOVA-ERP treat e-Fatura authorization as synchronous or asynchronous?

## Position A: Official Platform Authorization Is Synchronous

- Claim: official platform validation/authorization is synchronous.
- Evidence: the technical manual line states that after a taxpayer system sends a DFE, it waits until validation/authorization finishes; the v11.0 ingest preserves the same interpretation.
- Source: [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]
- Strength: high for the PE authorization attempt itself.

## Position B: NOVA-ERP Should Use Async Queues And Technical State Tracking

- Claim: NOVA-ERP should use asynchronous queues, technical state tracking, contingency handling and retry jobs.
- Evidence: product/architecture sources require resilient integration and observable retries.
- Source: [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]
- Strength: high for NOVA-ERP internal orchestration.

## Current Best Interpretation

This is an architecture tension, not a fatal contradiction.

NOVA-ERP should model internal orchestration asynchronously while treating the official PE/middleware authorization call itself as a synchronous operation when the worker performs it. The user-facing product can issue a document into a controlled state, queue the technical submission, and then update the document when the synchronous authorization attempt returns.

## Implementation Risk

- Product: UI copy must not imply authorization is complete while a queued worker has not performed the synchronous attempt.
- Architecture: internal queue state and PE authorization outcome must be separate axes.
- Data model: keep `queued`, `retrying` and `failed` as NOVA-ERP technical states; keep authorization, rejection/failure response and contingency as e-Fatura contract outcomes.
- Security/audit: every queued attempt and every synchronous response must be logged separately.
- Compliance: do not claim the DNRE platform itself processes authorization asynchronously unless a newer official source says so.

## Resolution Criteria

- Official DNRE guidance describing allowed timeout/retry/user-experience behavior for integrated software.
- Middleware endpoint documentation showing exact response semantics.
- A NOVA-ERP ADR deciding user-facing issuance semantics around pending authorization and contingency.
- Safe temporary posture: asynchronous internal job, synchronous PE/middleware attempt inside the worker, explicit pending/authorized/rejected/contingency status in product.

## Status History

- Date: 2026-05-28
  Change: Updated source basis to include v11.0 and normalized risk/resolution sections.
  Source: [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]
