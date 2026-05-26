---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/; docs/
source_type: mixed-folder-capture
author:
published:
ingested: 2026-05-26
tags: [source, inventory, nova-erp, fiscalidade, primavera]
related: ["[[NOVA-ERP]]", "[[Mapa de Fontes - NOVA-ERP e Fiscalidade]]", "[[ERP SaaS Multi-Tenant]]", "[[Fiscalidade Cabo Verde]]", "[[e-Fatura Cabo Verde]]"]
confidence: high
---

# Captura Raw e Docs

## Summary

Esta captura integrou duas colecoes de fontes:

- `raw/assets/`: documentacao de produto, arquitetura, deploy e backlog do [[NOVA-ERP]].
- `docs/docsfiscal/`: documentacao fiscal, formacao Cegid Primavera, IVA, fatura eletronica, SAF-T CV, tesouraria, contabilidade, inventario, salarios, ativos, logistica, instalacao e extensibilidade.

O padrao dominante e claro: o vault contem a base conceitual e operacional para construir um ERP SaaS multi-tenant para Cabo Verde, com enfase em fiscalidade, faturacao, e-Fatura, SAF-T CV, contabilidade, tesouraria, compras/vendas, inventario e RH.

## Key Claims

- O [[NOVA-ERP]] pretende ser um ERP SaaS multi-tenant moderno para Cabo Verde, com fiscalidade nativa, faturacao eletronica, integracao DNRE/e-Fatura/SAF-T CV, dashboards, auditoria e base para IA.
  Evidence: `raw/assets/SSD/PRD.MD`
  Confidence: high

- A arquitetura tecnica existente assume React, TypeScript, Vite, Tailwind, Supabase PostgreSQL, Supabase Auth, migrations, Edge Functions e RLS/policies.
  Evidence: `raw/assets/LOCAL_SETUP.md`, `raw/assets/SUPABASE_DEPLOY.md`, `raw/assets/DATABASE_ER_DIAGRAM.md`
  Confidence: high

- A camada SaaS de subscricoes precisa cobrir catalogo de planos, add-ons, contrato, entitlements, ciclo de vida, faturacao recorrente, integracao financeira, auditoria e enforcement de acesso.
  Evidence: `raw/assets/SUBSCRIPTION_ARCHITECTURE.md`
  Confidence: high

- Os documentos fiscais em `docs/docsfiscal/` funcionam como base de dominio para replicar e superar fluxos comuns do Cegid Primavera no contexto cabo-verdiano.
  Evidence: `docs/docsfiscal/*.pdf`, `docs/docsfiscal/*.docx`
  Confidence: medium

- A fiscalidade de Cabo Verde exige atencao especifica a IVA, emissao de faturas, Modelo 106, regularizacoes, notas de credito, fatura eletronica e SAF-T CV.
  Evidence: `docs/docsfiscal/Código IVA.pdf`, `docs/docsfiscal/MANUAL DE FATURAS.pdf`, `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`, `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf`
  Confidence: high

## Raw Assets Captured

| Source | Captured Information |
|---|---|
| `raw/assets/SSD/PRD.MD` | Strategic PRD for [[NOVA-ERP]]: product vision, Cabo Verde fiscal scope, SaaS multi-tenant architecture, ERP modules, compliance, IA, analytics and execution strategy. |
| `raw/assets/SSD/SSD.md` | Software/system specification for NOVA-ERP. Needs deeper second-pass ingestion. |
| `raw/assets/SSD/PROMPT.MD` | Implementation prompt defining the target stack, engineering role, architecture expectations and scope for the first usable ERP base. |
| `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD` | Full backlog organized by epics, features, user stories and acceptance criteria. |
| `raw/assets/SSD/BACKLOG SCRUM — NOVA-ERP.MD` | Scrum-oriented compressed backlog with epic/feature/story identifiers and MVP emphasis. |
| `raw/assets/DATABASE_ER_DIAGRAM.md` | Database ER documentation covering users/profiles, e-commerce, documents/faturacao, finance, inventory, communication, configuration, enums and storage buckets. |
| `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` | SaaS subscription architecture: plans, prices, add-ons, subscription contracts, billing runs, invoices, usage metrics, access enforcement, lifecycle and overdue handling. |
| `raw/assets/SUPABASE_DEPLOY.md` | Supabase deployment procedure: link project, push schema/RLS/policies/triggers/storage, configure webhook SQL, secrets, Edge Functions and frontend env vars. |
| `raw/assets/LOCAL_SETUP.md` | Local setup guide for React + Supabase app with Node/npm/Git, Supabase CLI/Docker, `.env`, `.env.local`, Vite server and commands. |
| `raw/assets/LOCAL_SETUP-Arydson.md` | Local setup variant with additional e-Fatura OAuth local callback and Edge Functions serving notes. |

## Docs Fiscal Captured

| Source | Pages/Size | Captured Information |
|---|---:|---|
| `docs/docsfiscal/Código IVA.pdf` | 48 pages | Legal source for Cabo Verde IVA regulation. |
| `docs/docsfiscal/MANUAL DE FATURAS.pdf` | 60 pages | DNRE/SITA guide for invoice rules in Cabo Verde; orientative, not a substitute for current law. |
| `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf` | 83 pages | DNRE technical manual for Cabo Verde electronic invoice v10.0; conceptual model, format, communication, security, processing and DFE structure. |
| `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf` | 103 pages | Fiscalidade with ERP Cegid Primavera: invoices, Modelo 106, IVA regularizations, credit notes, SAF-T CV accounting and inventory. |
| `docs/docsfiscal/SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf` | 103 pages | Duplicate or variant of the Cegid Primavera fiscalidade deck for Sao Vicente. |
| `docs/docsfiscal/FPG001 - Using - Tesouraria (2023-VC1-PT).pdf` | 123 pages | Treasury training: accounts receivable/payable, pendentes, advances, liquidations, compensations, transfers, cash and bank movement management. |
| `docs/docsfiscal/FPG003 - Using - Contabilidade e Fiscalidade (2022-VC1-PT).pdf` | 101 pages | Accounting and fiscal training: chart of accounts, journals/documents, accounting movements, integration, reports, IVA apuramento and fiscal maps. |
| `docs/docsfiscal/FPG006 - Using - Gestão de Equipamentos e Ativos (2020-VC1-PT).pdf` | 89 pages | Asset management training: asset record, acquisition, depreciation, transfers, conservation, revaluation, disposal, insurance and closing. |
| `docs/docsfiscal/FPG032 - Configuring - Financeira (2022-v1.0-PT).pdf` | 52 pages | Finance configuration: company properties, parameters, accounting movement config, cancellation reasons, account transfers, IVA apuramento, opening/closing and sales-accounting integration. |
| `docs/docsfiscal/LPG018- Configuring - Logística (2022-v1.0-GB).pdf` | 92 pages | Logistics configuration: warehouses, articles, units, serial numbers, lots, entities, document series, purchase/sales/internal documents and stock initialization. |
| `docs/docsfiscal/Using - Gestão de Inventário (2022-v1.0-GB - LPG003).pdf` | 64 pages | Inventory usage training; first pages indicate agenda and stock/inventory module training. |
| `docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf` | 73 pages | Purchases and sales process: entities, articles, documents, document circuit, editors, reservations, duplication, transformation, conversion and line copying. |
| `docs/docsfiscal/RPG001 - Using - Processamento de Salários (2021-VC1).pdf` | 118 pages | Payroll processing: employee admission, employee record, individual/batch payroll, cancellations, monthly changes, absences, overtime, subsidies, receipts and payments. |
| `docs/docsfiscal/Configuring - Recursos Humanos (2023-v1.0-PT).pdf` | 49 pages | HR configuration training. |
| `docs/docsfiscal/Exercícios - Configuring - Recursos Humanos (2023-v1.0-PT) .docx` | 143 paragraphs | HR configuration exercises: employee record, remunerations, discounts and absences with discounts. |
| `docs/docsfiscal/Exercícios - Using - Tesouraria (2023-VC1-PT).docx` | 472 paragraphs | Treasury exercises: account-current pendentes, pendentes via other modules, credit limits, operations on pendentes, reversals, payment plans, retentions, cash, bank movements and periodic bank operations. |
| `docs/docsfiscal/Exercícios - Using - Contabilidade e Fiscalidade (2022-v0.1-PT).pdf` | 22 pages | Accounting/fiscal exercises using a MIP case study. |
| `docs/docsfiscal/Exercícios - Using - Gestão de Inventário (2022-v1.0-GB - LPG003).pdf` | 18 pages | Inventory exercises using a MIP case study. |
| `docs/docsfiscal/Exercícios - Using - Processamento Salarios (2023-v0.1-PT).pdf` | 22 pages | Payroll exercises using a MIP case study. |
| `docs/docsfiscal/Exercícios-Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015 .pdf` | 21 pages | Purchases and sales exercises: entities, articles, purchase documents, sales documents, reservations, duplication, conversion, transformation, cancellation, credit/return and fiscal obligations. |
| `docs/docsfiscal/TPG036 - Implementing - Instalação e Administração.pdf` | 71 pages | Installation and administration: installation, company creation, data maintenance, users/security, licensing and administration. |
| `docs/docsfiscal/TPG037 - PRIMAVERA Extensibility - Configuration (2022-v1.0-GB).pdf` | 55 pages | PRIMAVERA extensibility: screen customization, desktop background, user functions/processes/menus, scheduler, user fields/tables, lists, maps and import/export config. |

## Entities Mentioned

- [[NOVA-ERP]]
- [[Cegid Primavera]]
- [[DNRE]]
- [[Supabase]]
- [[Cabo Verde]]

## Concepts Mentioned

- [[ERP SaaS Multi-Tenant]]
- [[Fiscalidade Cabo Verde]]
- [[e-Fatura Cabo Verde]]
- [[SAF-T CV]]
- [[Supabase Deployment]]
- [[Faturacao Eletronica]]
- [[Tesouraria ERP]]
- [[Contabilidade ERP]]
- [[Inventario ERP]]
- [[Processamento de Salarios ERP]]
- [[Gestao de Ativos ERP]]

## Contradictions Or Tensions

- The NOVA-ERP docs describe a product vision and implementation intent, while the Cegid/Primavera docs describe training material and existing ERP behavior. They should be used as domain references, not copied as target architecture.
- Some fiscal documents are older than 2026 and may be stale. Legal/fiscal claims must be verified before being treated as current compliance requirements.
- `Fiscalidade_ERP_Cegid_Primavera.pdf` and `SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf` appear to contain the same or near-identical deck and should be deduplicated in a later lint pass.

## Follow-up Questions

- Which source should become the canonical product source for NOVA-ERP: `PRD.MD`, `SSD.md`, or a synthesized product specification?
- Should `docs/docsfiscal/` remain as raw source material, or should it be moved under `raw/archive/fiscal/` to match the vault convention?
- Which fiscal requirements require current legal verification before implementation?

