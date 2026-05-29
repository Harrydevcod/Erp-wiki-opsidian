---
type: index
status: active
created: 2026-05-26
updated: 2026-05-29
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
- [[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]] - Web-research capture of INPS contributions (24.5% = 16%+8.5%), IRPS Category A final withholding (threshold 420,000$/yr) and the 2025 minimum wage (17,000$ private / 19,000$ public); secondary sources, primary-law verification required.
- [[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]] - Web-research capture of Portaria 42/2015 under the IRPC Code: quotas constantes default, 20,000$ low-value expensing, 4,000,000$ light-vehicle cap, pre-2015 Portaria 2/84 transition; per-class rate annex still to obtain.

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
- [[2026-05-29 - Supabase Implementation Artifact Gap]] - Confirms this vault lacks the referenced Supabase migrations/functions/seed artifacts; SQL/RLS/storage/Edge Function review requires the application repository or exported schema/policy bundle.
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

### Contradictions

- [[Contradiction - Current Database Snapshot vs Target ERP Architecture]] - Tracks the mismatch between the current ER diagram and target NOVA-ERP architecture.
- [[Contradiction - Middleware URL Scope]] - Superseded tension between tenant-scoped middleware URL config and environment-level `MIDDLEWARE_URL`; resolved by the middleware topology schema decision.
- [[Contradiction - e-Fatura Sync Authorization vs Async ERP Queue]] - Tracks official synchronous PE authorization versus NOVA-ERP internal async queue/retry architecture.
- [[Contradiction - IRPS Category A Withholding Brackets]] - Conflicting IRPS bracket scales (16.5%–27.5% vs a wider 0%–27% illustrative table); operative scale must come from the official DNRE withholding table/formula.

## Maintenance Queue

- Produce target schema decisions from [[2026-05-28 - Current Database Snapshot Classification]] before database implementation. The module schema-decision sequence is complete: foundation, document core, e-Fatura, treasury, inventory, accounting, payroll, fixed-assets, SaaS-subscriptions, permissions/audit, projects/analytical-dimensions, reporting/dashboards and AI-assistant ADRs all exist, and the `project.*`/`dimension.*`/`report.*`/`kpi.*`/`dashboard.*`/`ai.*` keys are now folded into the canonical catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]. Payroll and depreciation legal parameters are captured provisionally and folded into their ADRs. SQL/RLS/storage inspection remains blocked by [[2026-05-29 - Supabase Implementation Artifact Gap]]. Next: obtain implementation repository/export to validate ADRs against real migrations/RLS, and obtain the official DNRE IRPS withholding table and the Portaria 42/2015 rate annex.
- Verify actual DNRE middleware emitter-group behavior before production tenant onboarding automation.
- Verify legal retention periods for e-Fatura XML, event XML, ZIP archives, responses and DFA/PDF renders.
- Payroll/asset legal sources captured provisionally ([[2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources]], [[2026-05-29 - Cabo Verde Depreciation and Amortization Sources]]). Remaining: obtain the official DNRE IRPS withholding table/formula and INPS ceiling value (resolves [[Contradiction - IRPS Category A Withholding Brackets]]), the Código Laboral subsidy/overtime formulas, and the Portaria 42/2015 per-class depreciation rate annex.
- Deep-ingest treasury and purchase/sales workflows before building financial document circuits.
- Deep-ingest `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` as a full source page; the provisional [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] cites it directly until then.
- Verify current Cabo Verde fiscal treatment (IVA/e-Fatura) for SaaS service invoicing before enabling fiscal SaaS invoices.
- Inspect actual SQL migrations/RLS/storage policies behind `raw/assets/DATABASE_ER_DIAGRAM.md` before reuse decisions.
- Verify legal conditions and product scope before implementing `FDC` cancellation/anulation and `UDN` unused-number inutilization workflows.
- Verify current public works/State invoicing, reverse-charge and penalty rules before finalizing invoice business rules.
- Verify current Cabo Verde fiscal rules before treating old fiscal documents as implementation authority.
- Deduplicate the two Cegid Primavera fiscalidade decks.
