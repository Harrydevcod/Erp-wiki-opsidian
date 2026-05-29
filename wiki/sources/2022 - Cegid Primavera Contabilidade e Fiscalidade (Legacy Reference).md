---
type: source
status: active
created: 2026-05-29
updated: 2026-05-29
tags: [source, cegid-primavera, contabilidade, fiscalidade, iva, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Contabilidade ERP]]", "[[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]", "[[2026-05-29 - Codigo do IVA Cabo Verde]]", "[[SAF-T CV]]"]
confidence: medium
---

# Cegid Primavera — Contabilidade e Fiscalidade (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — Contabilidade e Fiscalidade" training manual (2022-VC1-PT, 101 pp.), `docs/docsfiscal/FPG003 - Using - Contabilidade e Fiscalidade (2022-VC1-PT).pdf`. **Legacy ERP workflow reference**, not legal authority and not target architecture. Value is in translating the operational flow into a NOVA-ERP design rationale for [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]].

## Legacy workflow (as documented)

- **Elementos base:** Plano de Contas (hierarchy — **Contas Razão / Contas Integradoras / Contas de Movimento**; integradoras = 2 digits, movement = 3+ digits), Diários e Documentos.
- **Registo de movimentos:** (a) registo **direto** na contabilidade; (b) **por integração de outros módulos**; (c) por **importação de ficheiro**.
- **Report financeiro:** Extratos, Balancetes, **Acumulados**.
- **Validação:** Conferência de Movimentos, Diagnósticos, **Auditoria SVAT** (SAF-T audit), Análise de Contrapartidas, **Reconstrução de Acumulados**.
- **Fiscal:** **Apuramentos de IVA**, Mapas Fiscais (PRIMAVERA Fiscal Reporting), Mapas Legais, **Balanço**, **Demonstração de Resultados**.
- **Abertura/Fecho de Exercício:** Criação de Exercício, **Apuramento de Resultados**, Registo de Documento de Abertura.
- **Operações:** Diárias, Periódicas, Arranque/Abertura de Ano, Fecho de Ano.

## Translation to NOVA-ERP

**Adopt (good domain coverage):**
- The **chart-of-accounts hierarchy** (razão / integradoras / movement; only **movement accounts post**) maps to `chart_of_accounts` with a parent hierarchy and a postable flag in [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]]. (Which CV PNC standard seeds the default chart remains the ADR's open question.)
- **"Registo por integração de outros módulos"** is exactly NOVA-ERP's **posting-rules-over-upstream-events** design; "registo direto" = manual journal entries (the ADR's manual-post default).
- **Apuramento de IVA** confirms a **periodic (monthly) IVA settlement** consuming `tax_maps`, consistent with [[2026-05-29 - Codigo do IVA Cabo Verde]].
- **Abertura/Fecho de Exercício + Apuramento de Resultados** confirm **accounting periods with locks** and a year-end close/result-apportionment step.
- **Auditoria SVAT** confirms SAF-T audit/export readiness ([[SAF-T CV]]); Balanço and Demonstração de Resultados as legal report outputs.

**Adapt:**
- Legacy **"Acumulados" + "Reconstrução de Acumulados"** (stored balance accumulators that must be rebuilt) → NOVA-ERP uses **projection-based balances computed from immutable journal lines**, eliminating the rebuild step. This validates the ADR's computed-balances choice over stored mutable accumulators.
- Conferência/Diagnósticos/Análise de Contrapartidas → the ADR's balanced-entry constraints and validation gates, enforced at write time rather than as after-the-fact cleanup.

**Do not copy:**
- Editable posted movements; NOVA-ERP keeps journal entries **immutable, reversal-only**.
- File-import-driven posting as a primary path; integration events + posting rules are the spine.
- Legacy fiscal maps as current authority — CV statutory maps/SAF-T must follow current law.

## Open questions surfaced

- Which **CV PNC (Plano Nacional de Contabilidade)** version seeds the default chart, and its account-digit structure?
- Which **Mapas Legais / Mapas Fiscais** (Balanço, DR, IVA apuramento, SAF-T) are statutorily required, and in what cadence/format?
- Year-end **Apuramento de Resultados** posting rules (which accounts, how results roll to equity).

## Verification needs

- Portugal-oriented Cegid product; CV-specific chart, fiscal maps, IVA apuramento format and SAF-T must come from current Cabo Verde law/DNRE, not this manual.
