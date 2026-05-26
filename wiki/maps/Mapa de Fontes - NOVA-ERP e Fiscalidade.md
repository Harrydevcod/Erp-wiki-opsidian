---
type: map
status: active
created: 2026-05-26
updated: 2026-05-26
tags: [map, sources, nova-erp, fiscalidade]
sources: ["[[2026-05-26 - Captura Raw e Docs]]"]
related: ["[[NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]", "[[ERP SaaS Multi-Tenant]]"]
confidence: high
---

# Mapa de Fontes - NOVA-ERP e Fiscalidade

## Main Clusters

### Product And Architecture

- `raw/assets/SSD/PRD.MD` - strategic product definition for [[NOVA-ERP]].
- `raw/assets/SSD/SSD.md` - system/software specification; needs deep ingestion.
- `raw/assets/SSD/PROMPT.MD` - implementation prompt and engineering constraints.
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD` - detailed backlog with epics, features, stories and acceptance criteria.
- `raw/assets/SSD/BACKLOG SCRUM — NOVA-ERP.MD` - compressed Scrum backlog.
- `raw/assets/DATABASE_ER_DIAGRAM.md` - current database map.
- `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` - SaaS subscription architecture.
- `raw/assets/SUPABASE_DEPLOY.md` - deploy process for Supabase.
- `raw/assets/LOCAL_SETUP.md` and `raw/assets/LOCAL_SETUP-Arydson.md` - local development process.

### Fiscal And Legal Domain

- `docs/docsfiscal/Código IVA.pdf`
- `docs/docsfiscal/MANUAL DE FATURAS.pdf`
- `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`
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

1. `raw/assets/SSD/PRD.MD`
2. `raw/assets/SSD/SSD.md`
3. `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
4. `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`
5. `docs/docsfiscal/MANUAL DE FATURAS.pdf`
6. `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`
7. `docs/docsfiscal/FPG003 - Using - Contabilidade e Fiscalidade (2022-VC1-PT).pdf`
8. `docs/docsfiscal/FPG001 - Using - Tesouraria (2023-VC1-PT).pdf`
9. `docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf`
10. `docs/docsfiscal/LPG018- Configuring - Logística (2022-v1.0-GB).pdf`

## Maintenance Notes

- Treat Cegid/Primavera docs as domain reference, not as architecture authority.
- Verify legal/fiscal requirements against current Cabo Verde law before implementation.
- Deduplicate the two Cegid fiscalidade decks in a later lint pass.

