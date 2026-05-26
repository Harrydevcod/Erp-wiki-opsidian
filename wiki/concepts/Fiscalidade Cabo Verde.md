---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [fiscalidade, cabo-verde, iva, compliance]
sources: ["docs/docsfiscal/Código IVA.pdf", "docs/docsfiscal/MANUAL DE FATURAS.pdf", "docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf", "docs/docsfiscal/SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf", "raw/assets/SSD/PRD.MD"]
related: ["[[NOVA-ERP]]", "[[e-Fatura Cabo Verde]]", "[[SAF-T CV]]"]
confidence: medium
---

# Fiscalidade Cabo Verde

## Definition

Fiscalidade Cabo Verde, in this wiki, means the legal and operational tax requirements an ERP must support for companies operating in Cabo Verde, especially IVA, invoice rules, fiscal declarations, electronic invoice flows and SAF-T CV reporting.

## Current Synthesis

The source set indicates that [[NOVA-ERP]] must treat fiscality as a product core, not as a later reporting module. The ERP must model fiscal rules at document creation time, preserve document auditability/immutability, support IVA calculation and reporting, and prepare data for e-Fatura/DNRE and SAF-T CV.

The Cegid Primavera fiscality materials show the expected operational territory: invoice emission, IVA Modelo 106, regularization annexes, credit note scenarios, and SAF-T CV accounting/inventory files.

## Evidence

- Evidence: `docs/docsfiscal/Código IVA.pdf`
- Evidence: `docs/docsfiscal/MANUAL DE FATURAS.pdf`
- Evidence: `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
- Evidence: `raw/assets/SSD/PRD.MD`

## Caution

Some fiscal sources are older than the current date. Before implementation, legal claims must be checked against current Cabo Verde law and DNRE guidance.

## Related Pages

- [[e-Fatura Cabo Verde]]
- [[SAF-T CV]]
- [[NOVA-ERP]]

## Open Questions

- Which IVA rules have changed since the included sources were published?
- What is mandatory for first production release versus later compliance depth?

