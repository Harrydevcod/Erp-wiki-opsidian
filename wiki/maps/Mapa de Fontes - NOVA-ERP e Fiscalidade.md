---
type: map
status: active
created: 2026-05-26
updated: 2026-05-29
tags: [map, sources, nova-erp, fiscalidade]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]", "[[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Manual de Faturas em Cabo Verde]]"]
related: ["[[NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]", "[[ERP SaaS Multi-Tenant]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[2026-05-29 - Supabase Implementation Artifact Gap]]"]
confidence: high
---

# Mapa de Fontes - NOVA-ERP e Fiscalidade

## Main Clusters

### Product And Architecture

- [[2026-05-26 - PRD NOVA-ERP]] - strategic product definition for [[NOVA-ERP]].
- [[2026-05-26 - SSD NOVA-ERP]] - system/software specification and module contract.
- [[2026-05-26 - Backlog Estruturado NOVA-ERP]] - detailed backlog with epics, features, stories and acceptance criteria.
- [[2026-05-26 - Prompt Implementacao NOVA-ERP]] - implementation prompt and engineering constraints for the foundation release.
- `raw/assets/SSD/BACKLOG SCRUM — NOVA-ERP.MD` - compressed Scrum backlog.
- [[2026-05-28 - DATABASE ER Diagram Snapshot]] - current database map ingested as implementation evidence, not target architecture authority.
- `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` - SaaS subscription architecture.
- `raw/assets/SUPABASE_DEPLOY.md` - deploy process for Supabase.
- `raw/assets/LOCAL_SETUP.md` and `raw/assets/LOCAL_SETUP-Arydson.md` - local development process.
- [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] - official project instructions, fiscal-first rules and middleware requirements.
- [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] - local/VPS e-Fatura middleware deployment and contingency flow.
- [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]] - DNRE e-Fatura technical contract for DFE XML, IUD, document types, authorization, contingency, APIs and middleware.
- [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] - latest official e-Fatura technical manual found on 2026-05-28, deep-ingested for schema/API implementation gates.
- [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]] - official XSD package listed on 2026-05-28, including schemas, field map and XML examples.
- [[2026-05-28 - Manual de Faturas em Cabo Verde]] - DNRE/SITA orientative guide for invoice issuance, required fields, numbering, rectification, special regimes, transport documents, archival and sanctions.
- `raw/assets/NOVA_ERP_PRD.md` and `raw/assets/NOVA_ERP_PRD_AVANCADO.pdf` - earlier/compact PRD variants and audit-oriented PRD note.

### Fiscal And Legal Domain

- `docs/docsfiscal/Código IVA.pdf`
- `docs/docsfiscal/MANUAL DE FATURAS.pdf` - ingested as [[2026-05-28 - Manual de Faturas em Cabo Verde]]
- `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf` - ingested as [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]]; superseded for current implementation by [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]
- `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
- `docs/docsfiscal/SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf`

These support [[Fiscalidade Cabo Verde]], [[e-Fatura Cabo Verde]], [[SAF-T CV]] and invoice compliance.

### ERP Functional Reference

- Treasury: `FPG001 - Using - Tesouraria`, `Exercícios - Using - Tesouraria`.
- Accounting/fiscal: `FPG003 - Using - Contabilidade e Fiscalidade`, accounting exercises.
- Finance configuration: `FPG032 - Configuring - Financeira`.
- Logistics/inventory: `LPG018- Configuring - Logística`, `Using - Gestão de Inventário`, inventory exercises.
- Purchases/sales: `Using - O Processo de Gestão de Compras e Vendas`, purchases/sales exercises.
- Payroll/HR: `RPG001 - Using - Processamento de Salários`, HR configuration and exercises.
- Assets: `FPG006 - Using - Gestão de Equipamentos e Ativos`.
- Administration/extensibility: `TPG036`, `TPG037`.

## Suggested Ingestion Order

1. `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`
2. `raw/assets/DATABASE_ER_DIAGRAM.md` - ingested as [[2026-05-28 - DATABASE ER Diagram Snapshot]]
3. `raw/assets/SUPABASE_DEPLOY.md`
4. `raw/assets/LOCAL_SETUP-Arydson.md`
5. `raw/assets/NOVA_ERP_PRD_AVANCADO.pdf`
6. `raw/assets/NOVA_ERP_PRD.md`
7. `docs/docsfiscal/MANUAL DE FATURAS.pdf` - ingested
8. `https://efatura.cv/assets/files/manual-tecnico-da-fatura-eletronica-v11.0-be67e62c7fb34552fbcc8eeea966e217.pdf` - ingested
9. `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
10. `docs/docsfiscal/FPG003 - Using - Contabilidade e Fiscalidade (2022-VC1-PT).pdf`

## Maintenance Notes

- Treat Cegid/Primavera docs as domain reference, not as architecture authority.
- Verify legal/fiscal requirements against current Cabo Verde law before implementation.
- Deduplicate the two Cegid fiscalidade decks in a later lint pass.
- See [[Revisao Raw Assets - 2026-05-26]] for source-authority risks and contradictions found in `raw/assets/`.
- `raw/assets/DATABASE_ER_DIAGRAM.md` is now ingested and classified in [[2026-05-28 - Current Database Snapshot Classification]]; target financial-core ADRs exist, but actual SQL/RLS/storage inspection is blocked by [[2026-05-29 - Supabase Implementation Artifact Gap]] until the implementation repository or exported schema/policy bundle is available.
- e-Fatura technical manual v11.0 and the official 2024-05-27 XSD package are now schema/API-ingested; event payloads for `FDC` cancellation/anulation and `UDN` unused-number inutilization are captured in [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]]. Current legal conditions and MVP scope still need resolution before implementation.
- [[Fiscalidade Cabo Verde]] now synthesizes invoice-rule substance, modern e-Fatura technical authority and database reuse boundaries; it should be the entry page before fiscal schema decisions.
- The 2018 invoice manual has a surviving/superseded rule classification in [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]].
