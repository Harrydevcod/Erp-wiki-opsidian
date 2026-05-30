---
type: index
status: active
created: 2026-05-26
updated: 2026-05-30
---

# NOVA-ERP Cabo Verde Wiki Index

This is the navigation layer for the NOVA-ERP Cabo Verde knowledge base. Read this file first before answering questions or updating the wiki.

## Operating Files

- [[CLAUDE]] - Primary schema and operating contract for maintaining this wiki.
- [[AGENTS]] - Codex bridge that points agents back to the schema.
- [[log]] - Chronological record of ingests, queries, lint passes, and maintenance.
- [[Bem-vindo]] - Human-facing entry point for the vault.

## Source Pipeline

- `raw/inbox/` - New sources waiting to be processed.
- `raw/archive/` - Sources already ingested. Keep originals unchanged.
- `raw/assets/` - Local images, PDFs, screenshots, audio, video, and clipped article assets.

## Templates

- `templates/source-summary.md` - Source ingest template with authority, currency, implementation impact and fiscal uncertainty sections.
- `templates/concept.md` - Concept template with source basis, implementation implications and uncertainty register.
- `templates/entity.md` - Entity template with NOVA-ERP role, authority/interfaces and timeline.
- `templates/module.md` - ERP module template with design gates, candidate model/state/events, permissions and acceptance criteria.
- `templates/synthesis.md` - Cross-source synthesis template with evidence strength, decision boundary and maintenance notes.
- `templates/question-answer.md` - Durable answer template with known/inferred/unresolved separation and implementation impact.
- `templates/contradiction.md` - Contradiction template for conflicting, superseded or uncertain claims with implementation risk and resolution criteria.
- `templates/schema-decision.md` - Schema/architecture decision template for implementation-grade data model and state/event decisions.

## Wiki Areas

### Sources

- [[2026-05-26 - Captura Raw e Docs]] - Consolidated capture of `raw/` and `docs/` source folders, including NOVA-ERP product docs and fiscal/Cegid Primavera documents.
- [[2026-05-26 - PRD NOVA-ERP]] - Product requirements document defining NOVA-ERP identity, scope, MVP, roadmap and product principles.
- [[2026-05-26 - SSD NOVA-ERP]] - Spec-driven development document defining functional/technical module requirements and implementation constraints.
- [[2026-05-26 - Backlog Estruturado NOVA-ERP]] - Structured backlog with epics, features, user stories, acceptance criteria and suggested prioritization.
- [[2026-05-26 - Prompt Implementacao NOVA-ERP]] - Implementation prompt defining the foundation release stack, schema, screens, seed, RLS, modules and execution order.
- [[2026-05-28 - Supabase Deploy]] - Project-specific Supabase deployment guide for migrations, RLS/policies, Edge Function webhooks, secrets, function deployment and frontend variables.
- [[2026-05-28 - DATABASE ER Diagram Snapshot]] - Current database ER snapshot; useful implementation evidence but not target architecture authority.
- [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]] - Official project instructions defining fiscal-first posture, enterprise quality, e-Fatura middleware expectations and UX direction.
- [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]] - Middleware deployment guide for local, staging, production, tenant onboarding, contingency and retry.
- [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]] - DNRE technical manual for DFE XML, IUD, document types, validation, authorization, contingency, APIs and middleware.
- [[2026-05-28 - Manual de Faturas em Cabo Verde]] - DNRE/SITA orientative guide for invoice issuance, required fields, numbering, rectification, special regimes, transport documents, archival and sanctions.
- [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]] - Current official e-Fatura technical manual found on 2026-05-28, superseding v10.0 for schema/API implementation authority.
- [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]] - Current official XML/XSD package listed on 2026-05-28, including DFE schemas, signatures, field map and examples.
- [[2008-12-29 - Tabela de Retencao IUR 2009]] - Primary law (Boletim Oficial, in force 2009): IUR withholding tables (Anexo I monthly, Anexo II practical) and the 10% own-account/independent withholding; predecessor to Portaria 5/2013, confirms the 11.67–35% rate scale is stable with re-indexed brackets.
- [[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]] - Primary law (Boletim Oficial): the exact monthly withholding formula and IUR-era scale (11.67%/15.56%/21.39%/27.22%/35% with parcelas a abater, α table, EF 640.000$, 35% cap); IUR predates IRPS, so confirm against the current IRPS-era portaria.
- [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] - Primary law (Boletim Oficial): full 20-article depreciation/amortization regime under IRPC art. 43º (straight-line default, declining-balance ×1.5/2/2.5, low-value ≤20.000$, vehicle cap 4.000.000$, real-estate land 25% split, goodwill non-amortizable, revokes Portaria 2/84); per-class rate annex still to obtain.
- [[2026-05-29 - Codigo do IVA Cabo Verde]] - Primary law (48-page IVA code): 15% standard rate, monthly self-assessed declaration, deduction with exclusions/pro-rata, invoice obligations, and the normal / isenção / simplificado-5% regimes (thresholds set by despacho); feeds tax_maps, document IVA and SAF-T.
- [[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]] - Legacy Cegid payroll workflow (employee ficha, batch/individual runs, monthly variables, autonomous subsidy runs, retroativos, anulação) translated into NOVA-ERP adopt/adapt/reject rationale; workflow reference only, not authority.
- [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]] - Legacy Cegid accounting workflow (chart hierarchy with movement-only posting, integration vs manual entries, IVA apuramento, period open/close, SVAT/SAF-T) translated to NOVA-ERP; validates projection-based balances over stored accumulators. Reference only.
- [[2022 - Cegid Primavera Compras e Vendas (Legacy Reference)]] - Legacy Cegid commercial-circuit workflow (unified entities, Orçamento→Encomenda→Guia→Fatura circuit, five reproduction mechanisms with line-quantity traceability, anulação vs estorno/crédito, séries emissíveis vs não emissíveis) translated to NOVA-ERP; corroborates the unified `entities`, commercial/fiscal split and `document_links` graph in the Document Core ADR. PT fiscal obligations explicitly not authority.
- [[2023 - Cegid Primavera Tesouraria (Legacy Reference)]] - Legacy Cegid treasury workflow (contas correntes pendentes, settlement taxonomy total/parcial/encontro/excesso/novo-pendente, anulação vs estorno, planos de pagamento, retenção, caixa session lifecycle, bancos, reconciliação manual/automática, Itens de Tesouraria) translated to NOVA-ERP; corroborates the obligation/movement/allocation ledger and derived payment status in the Treasury ADR, and adds the rubric, cash-session and withholding-to-State inputs. PT bank-export/cheque/letra workflows not authority.
- [[2022 - Cegid Primavera Gestao de Inventario (Legacy Reference)]] - Legacy Cegid inventory workflow (entrada/saída/transferência movements, PCM weighted-average valuation with cost adjustments, lots/serials with FIFO/LIFO, PTS/TST/RST in-transit transfers, expedição/receção monitors, BOM composição/decomposição, physical-count→adjustment reconciliation, blind/block counts, inventory close locks) translated to NOVA-ERP; corroborates the derived-from-movements ledger, weighted-average valuation and reservation/count model in the Inventory ADR, and adds in-transit state, locations, BOM and period-lock inputs. PT inventory-to-AT communication not authority.
- [[2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference)]] - Legacy Cegid fixed-asset lifecycle (parallel accounting+fiscal depreciation plans, straight-line/declining-balance ×1.5/×2/×2.5, periodicity anual/duodecimal/diária, taxa máxima/mínima/perdida, extraordinary depreciation, impairment loss+reversal, market-value/replacement-cost revaluation, transfers/decomposition/copy, conservation, alienação/abate/sinistro with excess-amortization correction, Repartições to cost centers, insurance, exercise close) translated to NOVA-ERP; corroborates the Fixed Assets ADR and resolves its separate-book/fiscal-schedule, periodicity and cost-center-allocation questions. PT Mapas Fiscais not authority.
- [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]] - **Now primary-anchored (2026-05-30):** INPS 24.5% (16%+8.5%); IRPS Cat. A final withholding (DL 6/2015 formula, threshold 420,000$/yr); mínimo de existência = 220.000$ isenção (CIRPS art. 45º nº2); Código Laboral (preserved DL 5/2007) overtime **+35%** (art. 207º, DL 1/2016; old +50% superseded), rest-day +100% (208º), night ≥+25% (169º), **Natal/13º discretionary & attendance-scaled (art. 206º — not a mandatory 13th)**; 2025 minimum wage 17,000$/19,000$. Residual: INPS teto value.
- [[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]] - **Primary law** (Lei 33/VII/2008, republished B.O. I Série nº 3, 8-01-2015; preserved at `raw/assets/selo/`): the IS code **incidence/general part (arts 1–26)** completing the rate Tabela. Art. 1º objectiva (financial/societária/documental ops) with the **§2 IVA non-cumulation gate** (IVA-subject ops are outside IS); art. 2º repercussão; art. 3º territoriality; arts 8–22 special part by category; arts 23–26 liquidação/arredondamento/pagamento/caducidade.
- [[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]] - Web-research capture of Portaria 42/2015 under the IRPC Code: quotas constantes default, 20,000$ low-value expensing, 4,000,000$ light-vehicle cap, pre-2015 Portaria 2/84 transition; per-class rate annex still to obtain.
- [[2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV]] - **Primary law** (Boletim Oficial I Série nº 97, 7 out 2021): defines the SAF-T (CV) data structure (Anexo I) + SNCRF/NIC taxonomies (Anexo II) under IRPC art. 107.º nº6; in force 1 Jan 2022 (exercises 2022+); obligated = organized-accounting IRPC + Category B organized (exempt ≤ 5.000.000$). Confirms the XSD structure and all previously-unconfirmed code values (ProductType, TaxType TEU=Tributo Especial Unificado, PSProductType incl. AB=Ativos biológicos, ProductStatus). Saved at `raw/assets/saft-cv/`.
- [[2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas]] - **Primary law** (Tabela de verbas, B.O. I Série nº 3, 8-01-2015): stamp-duty rates — operações de crédito 0,5%, serviços financeiros/seguros 3,5%, garantias/letras/societárias 0,5%, actos notariais/registo/processuais 15%, actos administrativos/contratos 1.000$00 fixo. Treasury/financial-document tax. **Incidence (arts 1–26) now captured** in [[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]].
- [[2015-01-07 - Lei 82-2015 Codigo do IRPC]] - **Primary law** (B.O. I Série nº 3, 8-01-2015): the IRPC Code. Taxa **25%** (contabilidade organizada) / **4% TEU** (REMPE simplificado, art. 84º); **tributação autónoma** 40% despesas não documentadas, 10% viaturas/representação (art. 89º); **dedução de prejuízos** 7 períodos, máx 50%/ano (art. 59º); imparidade de créditos 25/50/75/100% por mora; art. 43º = base da Portaria 42/2015. Carries the Imposto de Selo annex too. Saved at `raw/assets/irpc/`.
- [[2014-12-31 - Lei 78-2014 Codigo do IRPS]] - **Primary law** (B.O. I Série nº 81, 31-12-2014): the IRPS Code. Categories A–E (A trabalho/pensões, B empresariais/profissionais, C prediais, D capitais, E ganhos patrimoniais); **Art. 45º** annual englobamento scale **16,5% (≤960.000$) / 23,1% (≤1.800.000$) / 27,5% (>1.800.000$)** with **isenção do colectável até 220.000$**; Art. 46–48º confirm Cat. A liberatório-progressivo (DL 6/2015), **B 20%, C 20%**. Parent statute of DL 6/2015; saved at `raw/assets/irps/`.
- [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]] - **Primary law** (B.O. I Série nº 7, 23-01-2015): the operative IRPS withholding regime. Art. 5.º monthly **Category A** formula on gross `Rm` — **0,15·Rm−5.500** (≤80.000$), **0,21·Rm−10.300** (80–150.000$), **0,25·Rm−16.300** (>150.000$); round down to ten escudos; 100$ min; subsídios férias/Natal = retenção autónoma. Other categories B 20%/4%, C 20%, D 20%/10%, E 1%/20%. **Supersedes the IUR-2013 scale**; saved at `raw/assets/irps/`. Resolves the IRPS-withholding contradiction.
- [[2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese)]] - Secondary síntese (CVTradeInvest) giving the **IRPS-era progressive scale with explicit brackets** (isenção ≤220.000$; 16,5% ≤960.000$; 23,1% ≤1.800.000$; 27,5% >1.800.000$) and per-category retention (A progressive/liberatório from 420k/35k; B 15%; C 10%; D 20%/10%; E 1%/20%), plus IRPC 25%/4%. Second independent source confirming **IUR was replaced by IRPS**; resolves the IRPS-bracket contradiction in direction. Rate currency/monthly retention table still need primary law.
- [[2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis]] - **Official DNRE SAF-T (CV) schema** parsed directly (namespace `urn:OECD:StandardAuditFile-Tax:CV_1.01_01`, v1.01_01, 2020-05-29; saved at `raw/assets/saft-cv/`): `AuditFile` = Header/MasterFiles/GeneralLedgerEntries/SourceDocuments, one schema with `FileContentType` F/C/I/O (no "Completo"), software-certification + multi-part header fields. Legal basis Portaria 47/2021 (SNCRF) + e-Fatura DL 79/2020. Primary structure; portaria numbers need Boletim Oficial confirmation.

### Entities

- [[Cegid Primavera]] - ERP reference corpus for fiscal, accounting, treasury, logistics, HR, asset and extensibility workflows.
- [[DNRE]] - Cabo Verde tax authority context behind invoice and electronic invoice materials.
- [[Supabase]] - Backend platform for NOVA-ERP: PostgreSQL, Auth, RLS, storage and Edge Functions.

### Concepts

- [[ERP SaaS Multi-Tenant]] - Tenant-isolated ERP SaaS architecture model for NOVA-ERP.
- [[Configuracao ERP]] - Tenant setup and parameterization control plane for company identity, fiscal profile, base currency, modules, document series, e-Fatura readiness and controlled activation.
- [[Fiscalidade Cabo Verde]] - Tax/compliance domain for IVA, invoices, declarations, e-Fatura, SAF-T CV and fiscal implementation boundaries.
- [[e-Fatura Cabo Verde]] - Electronic invoice domain and DNRE integration context.
- [[SAF-T CV]] - Cabo Verde fiscal audit/export domain for SAF-T Faturacao, Contabilidade and Inventario readiness, asynchronous export jobs, validation, private artifacts and consistency gates.
- [[Supabase Deployment]] - Operational deployment and runtime boundary for Supabase migrations, RLS, storage, Edge Functions, secrets, verification gates and rollback posture.
- [[Faturacao Eletronica]] - ERP module entry point for fiscal document issuance, e-Fatura/DNRE communication, ingestion sequence, design gates and audit states.
- [[Compras e Vendas ERP]] - Commercial document circuit for customers, suppliers, sales, purchases, document transformations, stock/treasury/fiscal boundaries and downstream impacts.
- [[Contabilidade ERP]] - Accounting module entry point for ledger, fiscal maps, postings, period locks and operational/fiscal source links.
- [[Inventario ERP]] - Inventory module entry point for items, warehouses, reservations, stock movements, counts, lots/serials, valuation and audit/export readiness.
- [[Tesouraria ERP]] - Treasury module entry point for receivables, payables, cash, banks, allocations, reversals, current accounts and reconciliation.
- [[Processamento de Salarios ERP]] - HR/payroll module entry point for employee records, period-based payroll runs, payslips, deductions, salary payments, privacy controls and accounting integration.
- [[Gestao de Ativos ERP]] - Fixed assets module entry point for acquisition, capitalization, depreciation, transfers, maintenance, revaluation, disposal and accounting evidence.
- [[Subscricoes SaaS ERP]] - NOVA-ERP SaaS business model layer for plan catalog, add-ons, subscription contracts, entitlements, billing runs, lifecycle and access enforcement.
- [[Permissoes e Auditoria ERP]] - Security governance layer for tenant membership, permissions, RLS, sensitive fiscal/accounting actions and audit logs.
- [[Projetos ERP]] - Project and cost-tracking module entry point for analytical dimensions, budgets, allocations, profitability, cash effects and operational accountability.
- [[Dashboards e Relatorios ERP]] - Governed visibility layer for executive dashboards, KPI definitions, curated reporting datasets, exports, heavy report jobs and AI-safe analytics.
- [[IA Assistente ERP]] - Governed AI layer for permission-aware questions, reporting context, anomaly explanation, auditable suggestions and constrained action boundaries.

### Syntheses

- [[NOVA-ERP Module Priority Map]] - First-pass priority map for module sequencing and architectural dependency layers.
- [[NOVA-ERP Product Authority Synthesis]] - Reconciles PRD, SSD and structured backlog into product authority, sequencing and implementation implications.
- [[2026-05-28 - Current Database Snapshot Classification]] - Classifies current database tables as adapt, replace/split, optional or archive/reframe against target ERP architecture.
- [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] - Provisional foundation schema decision for tenants, memberships, RBAC, append-only audit log, platform-admin boundary and the default-deny membership-keyed RLS pattern; prerequisite for all other target schema decisions.
- [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]] - Provisional schema decision splitting commercial documents from fiscal documents, unifying customers/suppliers as `entities`, and connecting transformations via a `document_links` graph; defines the `fiscal_documents` header the e-Fatura decisions attach to.
- [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]] - Provisional schema decision modeling treasury as an obligation/movement/allocation ledger with derived payment status, reversal-by-compensation and bank reconciliation, replacing the snapshot's flat `financial_transactions`.
- [[2026-05-28 - Schema Decision - Inventory Movements and Valuation]] - Provisional schema decision modeling stock as the derived sum of an append-only movement ledger with valuation layers, reservation-vs-on-hand split and count reconciliation, SAF-T-ready and replacing any stored quantity field.
- [[2026-05-28 - Schema Decision - Accounting Ledger and Posting]] - Provisional schema decision modeling accounting as an immutable double-entry journal driven by posting rules over fiscal/treasury/inventory events, with projection-based balances, period locks and SAF-T-ready tax maps; closes the financial-core schema sequence.
- [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] - Provisional schema decision separating fiscal documents, DFE payloads, validations, transmissions, attempts, contingency, references and certificate metadata.
- [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]] - Provisional schema decision for official e-Fatura event payloads, including `FDC` cancellation/anulation and `UDN` unused-number inutilization.
- [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]] - Provisional schema decision resolving middleware topology as environment default endpoint plus tenant e-Fatura settings and platform-admin-only override.
- [[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]] - Provisional schema decision separating e-Fatura metadata, private fiscal evidence artifacts and certificate/private-key secrets.
- [[2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema]] - Element-by-element map of the official SAF-T (CV) v1.01_01 XSD to NOVA-ERP tables (entities/chart/items/tax/journal/documents/treasury/inventory), with a capture-at-transaction-time checklist (SNCRF taxonomy codes, GL control accounts, SystemEntryDate/SourceBilling, DocArchivalNumber, WithholdingTax, valued PhysicalStock) so valid SAF-T follows from consistent source data.
- [[2026-05-29 - Supabase Implementation Artifact Gap]] - **Resolved 2026-05-30**: the implementation repo is now in the workspace; this page is historical and points to the reconciliation below. Edge Functions + storage policies still unreviewed.
- [[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]] - Reads the **13 actual Supabase migrations** against the target-schema ADR sequence. Tenant isolation MATCHES (membership-validated active-tenant RLS); recurring DIVERGENCE = implementation prefers **stored accumulators maintained by triggers/procedures** over the ADRs' derived-from-immutable-ledger stance (stock_items, documents.status). GAPS: fixed assets, generic analytical dimensions, reporting/AI, entitlement computation, per-user permission overrides all unbuilt. Per-area conform-vs-amend decision matrix for the founder.
- [[2026-05-30 - Edge Function and Storage Security Review]] - **Security finding (high).** All three Edge Functions (`create-user`, `audit-log`, `numbering`) run on the **service-role key (bypass RLS)** and trust body `tenant_id` with **no caller membership/permission check** → `create-user` allows **cross-tenant admin creation** (critical); `audit-log` attribution is forgeable; `numbering` lets any user inject gaps in another tenant's fiscal sequence. No storage bucket policies in migrations (private fiscal/cert/payroll buckets required by the e-Fatura secrets ADR). Net: no enforced per-tenant authorization at DB *or* Edge for these ops. Includes root-cause fix pattern + fix order.
- [[2026-05-29 - Schema Decision - Payroll Runs and Payslips]] - Provisional payroll schema decision for employee terms, period-based runs, rule-versioned components, immutable payslips, treasury payment batches and accounting events.
- [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]] - Provisional fixed-assets schema decision separating assets from inventory and modeling capitalization, depreciation, transfers, revaluation, disposal and accounting events.
- [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] - Provisional SaaS commercial-layer schema decision: platform-owned catalog plus tenant-scoped contracts, computed effective entitlements with immutable snapshots, platform-admin-write/tenant-read RLS split, treasury-derived payment status and deferred fiscal SaaS-invoicing scope.
- [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]] - Provisional security-layer decision extending the tenant foundation: `module.action` permission catalog, per-user revoke-wins overrides, graduated status/raw/secret evidence access tiers, committed audit event taxonomy with hash/reference payload policy and service-role attribution, plus a launch role→permission matrix.
- [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]] - Provisional analytical-dimension decision modeling projects and cost centers as types of one generic dimension layer (`analytical_dimensions` + `dimension_values` + polymorphic `dimension_tags` with split allocation); project profitability is derived from tagged source events with no stored totals, and the tagging capability ships from day one to allow non-destructive adoption.
- [[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]] - Provisional reporting decision making dashboards a governed semantic layer: versioned KPI/report/dataset/dashboard definitions own metric meaning, dashboards and AI read only curated tenant-scoped `reporting_datasets` (never operational tables) with a per-value freshness state, dual permission+entitlement gates, async `report_runs`, audited exports, statutory-vs-management separation and an `ai_safe` dataset contract for the AI layer.
- [[2026-05-29 - Schema Decision - AI Assistant Governance and Action Boundary]] - Provisional AI-layer decision binding the assistant to the acting user's permissions inside the existing trust boundary: reads only `ai_safe` datasets/tools (no raw tables, no service-role bypass), suggests but never directly mutates (suggest→confirm→execute via normal module commands), records full prompt/retrieval/tool/suggestion provenance with citations and audit, redacts sensitive evidence before egress, and is gated by a per-tenant kill switch and plan entitlement. Closes the module schema-decision sequence.

### Questions

- [[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]] - Classifies which 2018 invoice manual rules survive, are superseded or remain unresolved under modern e-Fatura.

### Projects

- [[NOVA-ERP]] - Modern multi-tenant ERP SaaS for Cabo Verde with fiscal compliance and future AI layer.

### People

No people pages yet.

### Places

- [[Cabo Verde]] - Primary jurisdiction and market context for NOVA-ERP.

### Maps

- [[Mapa de Fontes - NOVA-ERP e Fiscalidade]] - Source map connecting product, architecture, fiscal and ERP reference materials.
- [[NOVA-ERP Knowledge Architecture]] - Operating map for organizing NOVA-ERP product, compliance, module and architecture knowledge.
- [[Revisao Raw Assets - 2026-05-26]] - Review of `raw/assets/` source corpus, including source authority, risks, contradictions and next ingestion order.
- [[Portaria 42-2015 Tabelas de Taxas de Depreciacao]] - The per-asset-class **depreciation rate annex** of Portaria 42/2015 (B.O. I Série nº 52, 28-08-2015): 310 rated rows, Tabela I sector-specific + Tabela II generic, extracted to `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv` to seed `asset_depreciation_policies.rate`. Key generics: edifícios 3%/5%, veículos ligeiros 14,28%, pesados 20%, computadores/intangível 33,33%.
- [[SAF-T CV Anexo II - SNCRF Account Taxonomy]] - The 660-code SNCRF/NIC account taxonomy (Anexo II of Portaria 47/2021) that `GeneralLedgerAccounts.TaxonomyCode` references; extracted to `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv` to seed `chart_of_accounts.taxonomy_code`. Classes 1–7, no gaps.
- [[SAF-T CV Code Lists]] - Seed reference of the 14 official SAF-T (CV) v1.01_01 enumerations (FileContentType, TaxonomyReference, ProductType, TaxType, WorkType/Status, PaymentType/Mechanism, WithholdingTaxType, TransactionType, PSProductType, ProductStatus); documented values are authoritative, a few flagged convention-confirm.

### Contradictions

- [[Contradiction - Current Database Snapshot vs Target ERP Architecture]] - Tracks the mismatch between the current ER diagram and target NOVA-ERP architecture.
- [[Contradiction - Middleware URL Scope]] - Superseded tension between tenant-scoped middleware URL config and environment-level `MIDDLEWARE_URL`; resolved by the middleware topology schema decision.
- [[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]] - Tracks official synchronous PE authorization versus NOVA-ERP internal async queue/retry architecture.
- [[Contradiction - IRPS Category A Withholding Brackets]] - **Resolved/superseded (2026-05-30) by primary law** [[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]: monthly Category A formula 15/21/25% (parcela 5.500/10.300/16.300), superseding the IUR-2013 scale. Residuals minor (retificação check, OE re-indexing, ME value).
- [[Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy]] - **Resolved/superseded** (2026-05-30): Portaria 47/2021 Anexo I = same structure as XSD v1.01_01 (consistent), Anexo II = the SNCRF/NIC account taxonomies; no real conflict, only a missing piece now obtained. Residual: extract Anexo II to seed `chart_of_accounts.taxonomy_code`.
- [[Contradiction - Inventory Stored Stock vs Derived Movement Ledger]] - **Open (2026-05-30, high confidence):** `00006` ships `stock_items` with stored `qty_on_hand`/`avg_cost` mutated by a trigger — the snapshot-accumulator the inventory ADR explicitly rejected. Highest-impact SAF-T/COGS divergence. Founder decision: conform (ledger = source of truth) or amend ADR (MVP accumulator).
- [[Contradiction - Stored Payment Status vs Derived from Allocations]] - **Open (2026-05-30, high confidence):** `documents.status` stores `paid/partial_paid/overdue` and `settle_document()` writes it back, vs the treasury ADR's "derived from allocations, never a stored boolean." Allocation substrate exists; only the status is denormalized.
- [[Contradiction - DB-Layer Authorization and RLS Permission Gating]] - **Open (2026-05-30, high confidence):** tenant isolation is sound (membership-validated), but RLS gates only *tenant*, not *permission* — 41 `FOR ALL` policies give any active member full CRUD; no `user_permission_overrides`, no evidence tiers, no `FORCE RLS`. Decide whether authorization belongs at DB or app/Edge layer.

## Maintenance Queue

- Produce target schema decisions from [[2026-05-28 - Current Database Snapshot Classification]] before database implementation. The module schema-decision sequence is complete: foundation, document core, e-Fatura, treasury, inventory, accounting, payroll, fixed-assets, SaaS-subscriptions, permissions/audit, projects/analytical-dimensions, reporting/dashboards and AI-assistant ADRs all exist, and the `project.*`/`dimension.*`/`report.*`/`kpi.*`/`dashboard.*`/`ai.*` keys are now folded into the canonical catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]. Payroll and depreciation legal parameters are captured provisionally and folded into their ADRs. **Implementation repo now in workspace and reconciled (2026-05-30):** [[2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations]] maps the 13 migrations to the ADRs. Material divergences opened as contradictions (inventory stored-stock, stored payment status, DB-layer authorization). **GAPS still unbuilt:** fixed assets, generic analytical dimensions, reporting/AI layers, SaaS entitlement computation, `user_permission_overrides`/evidence tiers. **Next implementation-grade pass:** review the four Edge Functions (`audit-log`, `create-user`, `numbering`, `_shared`) and storage bucket policies for auth/tenant derivation/permission/service-role discipline; then per-area founder decision conform-vs-amend on each contradiction.
- Verify actual DNRE middleware emitter-group behavior before production tenant onboarding automation.
- Verify legal retention periods for e-Fatura XML, event XML, ZIP archives, responses and DFA/PDF renders.
- Payroll/asset legal sources captured from primary law: withholding formula/scale ([[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]], [[2008-12-29 - Tabela de Retencao IUR 2009]]) and the full depreciation regime ([[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]). Resolved: the IRPS withholding regime is anchored in **primary law** ([[2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS]]) — monthly Category A formula 15/21/25% with parcela 5.500/10.300/16.300, superseding the IUR scale. **Payroll legal gaps now closed (2026-05-30) against primary law** ([[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]]): Mínimo de Existência = 220.000$ isenção (CIRPS art. 45º nº2); Código Laboral overtime **+35%** (art. 207º via DL 1/2016, old +50% superseded), rest-day +100% (208º), night ≥+25% (169º); subsídio de Natal/13.º = **discretionary, attendance-scaled (art. 206º)**, not a mandatory 13th (preserved DL 5/2007 at `raw/assets/laboral/`). The **Imposto de Selo incidence (arts 1–26)** is now captured ([[2008-11-24 - Lei 33-2008 Codigo do Imposto de Selo]]). **Minor residuals only:** the INPS contribution-base upper teto value, the DL 6/2015 retificação check, and OE-year re-indexing of the IRPS thresholds. The **per-class depreciation rate annex** of Portaria 42/2015 is captured ([[Portaria 42-2015 Tabelas de Taxas de Depreciacao]]).
- Cegid "Using" workflow decks for module ADRs are ingested: Compras e Vendas, Tesouraria, Inventário, Ativos, Contabilidade e Fiscalidade, Processamento de Salários. Remaining Cegid material is optional (Configuring decks: Financeira FPG032, Logística LPG018, RH; Implementing TPG036; Extensibility TPG037) — ingest only if a specific ADR needs deeper config detail.
- Deep-ingest `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` as a full source page; the provisional [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] cites it directly until then.
- Verify current Cabo Verde fiscal treatment (IVA/e-Fatura) for SaaS service invoicing before enabling fiscal SaaS invoices.
- Inspect actual SQL migrations/RLS/storage policies behind `raw/assets/DATABASE_ER_DIAGRAM.md` before reuse decisions.
- Verify legal conditions and product scope before implementing `FDC` cancellation/anulation and `UDN` unused-number inutilization workflows.
- Verify current public works/State invoicing, reverse-charge and penalty rules before finalizing invoice business rules.
- Verify current Cabo Verde fiscal rules before treating old fiscal documents as implementation authority.
- ~~Deduplicate the two Cegid Primavera fiscalidade decks.~~ **Resolved 2026-05-30:** proven byte-content-identical (same full-text hash, 103 pp., same author/CreationDate; differed only by a re-save ModDate); removed `SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf`, kept `Fiscalidade_ERP_Cegid_Primavera.pdf`. Deck itself still uningested (optional — overlaps [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]]).
