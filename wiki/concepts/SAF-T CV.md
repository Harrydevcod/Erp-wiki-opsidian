---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [saft, cabo-verde, fiscalidade, reporting]
sources: ["docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf", "docs/docsfiscal/SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf", "raw/assets/SSD/PRD.MD", "raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD"]
related: ["[[Fiscalidade Cabo Verde]]", "[[NOVA-ERP]]"]
confidence: medium
---

# SAF-T CV

## Definition

SAF-T CV is the Cabo Verde fiscal reporting/export domain for structured audit files, especially accounting and inventory exports.

## Current Synthesis

The source set indicates NOVA-ERP should prepare for SAF-T CV from the data model upward. Backlog items call for generating accounting and inventory SAF-T XML, selecting period/exercise, validating structure, detecting blocking errors and producing inconsistency reports.

## Evidence

- Evidence: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Evidence: `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`

## Open Questions

- What is the current official SAF-T CV schema version?
- Which fields must be captured at transaction time to avoid impossible exports later?

