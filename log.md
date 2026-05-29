---
type: log
status: active
created: 2026-05-26
updated: 2026-05-29
---

# LLM Wiki Log

Append-only chronological record. New entries go at the top.

## [2026-05-29] ingest | Cabo Verde payroll and depreciation legal sources

- Researched and ingested current Cabo Verde statutory parameters to unblock the payroll and fixed-assets ADRs (figures from secondary web sources; primary-law verification flagged throughout).
- Payroll: INPS 24.5% (16% employer + 8.5% employee; self-employed 19.5%; domestic 23%), due by the 15th, with a contribution ceiling (value to confirm); IRPS Category A final withholding via the official DNRE table/formula, threshold annual >420,000$ (monthly >35,000$), employee INPS deductible; minimum wage 17,000$ private / 19,000$ public from 2025-01-01 (Lei 78/VIII/2014 + Código Laboral + governo.cv).
- Depreciation: Portaria 42/2015 under IRPC Code art. 43º; quotas constantes default (decrescentes alt), low-value ≤20,000$ single-period expensing, light-vehicle cost cap 4,000,000$, pre-2015 assets keep Portaria 2/84; per-class rate annex still to obtain; IRPC base rate 25%.
- Preserved the unresolved IRPS bracket scale as a contradiction rather than guessing (16.5%–27.5% vs a wider illustrative 0%–27% table; neither is the official DNRE table).
- Updated the Payroll ADR (new "Cabo Verde Statutory Parameters" section, source basis, open questions) and the Fixed Assets ADR (depreciation method enum extended with declining_balance/low_value_expense, cost_cap + acquisition_date_rule fields, source basis, open questions).
- Files created:
  - `wiki/sources/2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources.md`
  - `wiki/sources/2026-05-29 - Cabo Verde Depreciation and Amortization Sources.md`
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md`
- Files updated:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md`
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Official DNRE IRPS withholding table/formula and current bracket scale?
  - INPS contribution ceiling value?
  - Código Laboral subsidy/overtime formulas and required payroll maps?
  - Portaria 42/2015 per-asset-class rate/useful-life annex; any post-2015 budget-law changes to thresholds/caps?

## [2026-05-29] lint | Vault health check (clean) + helper script

- Added `tools/lint.py` and ran a full cross-reference lint: frontmatter, orphans, broken wikilinks, index coverage and un-ingested sources across 85 markdown files.
- Result: vault is healthy. Index coverage 0 gaps; raw/inbox empty; every maintained `wiki/` page has frontmatter and an inbound link. All flagged frontmatter/orphan items are `raw/assets/*` (immutable sources cited by path) or `templates/*` (not graph nodes) — correct by design. 9 of 11 "broken" links are placeholder examples inside `CLAUDE.md`/templates.
- Fixed the only real finding: two stale forward-ref wikilinks in [[NOVA-ERP Knowledge Architecture]] (`[[Entidades ERP]]`, `[[Produtos e Servicos ERP]]`) repointed to where that knowledge now lives ([[Compras e Vendas ERP]] entities, [[Inventario ERP]] items).
- Files created:
  - `tools/lint.py`
- Files updated:
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `log.md`
- Open questions:
  - None from lint; standing gaps remain the Supabase artifact validation and payroll/asset legal ingestion.

## [2026-05-29] maintain | Consolidated downstream permission keys into the catalog

- Closed the loop on the permission catalog: the projects, reporting and AI ADRs each flagged new permission keys that were never folded into the canonical catalog, leaving it incomplete as the single source of truth.
- Added Projects/dimensions (`project.*`, `dimension.manage`), Reporting (`report.*`, `kpi.manage`, `dashboard.manage`, `reporting.dataset_manage`) and AI (`ai.*`) groups to the catalog seed; added `projects` to the `permission_groups` enum; extended the audit event taxonomy with project, reporting and AI event categories.
- Files updated:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Same as the permission-catalog ADR (launch role mapping for the new keys, second-approver for critical permissions).

## [2026-05-29] schema | Added AI assistant governance schema decision (module sequence complete)

- Produced the final module ADR, closing the NOVA-ERP module schema-decision sequence. Designed the AI layer as a thin governed consumer that composes the existing reporting/permission/audit/entitlement mechanisms rather than introducing a new privileged path.
- Decided that AI runs with the acting user's own permissions (no AI role, no service-role data path), reads only `ai_safe` reporting datasets/tool endpoints, and can suggest but never directly mutate — durable changes go through suggest→confirm→execute on normal module commands with human confirmation and audit.
- Committed `ai_tenant_settings` (kill switch/mode/provider/retention), `ai_conversations`/`ai_messages`, full provenance (`ai_context_references`/`ai_retrieval_events`/`ai_tool_calls`), `ai_suggestions`+`ai_action_confirmations`, `ai_safety_events`, `ai_feedback`; the suggestion state machine and the read_only→forbidden risk-level gate; sensitive-evidence redaction before model egress; grounding/uncertainty rules for fiscal/legal answers.
- New permission keys (`ai.use`, `ai.suggest`, `ai.action_confirm`, `ai.config`, `ai.logs_view`) flagged for the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]].
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - AI Assistant Governance and Action Boundary.md`
- Files updated:
  - `IA Assistente ERP.md`
  - `index.md`
  - `log.md`
- Module ADR sequence now complete (foundation, document core, e-Fatura, treasury, inventory, accounting, payroll, fixed-assets, subscriptions, permissions/audit, projects/dimensions, reporting/dashboards, AI). Standing gap: validate all ADRs against real Supabase migrations/RLS once the implementation repo/export is available.
- Open questions:
  - First AI use case and whether launch is strictly read-only?
  - Acceptable provider/residency/retention posture for Cabo Verde ERP data?
  - Are AI logs visible to tenant admins, platform admins or both?
  - Which fiscal answer classes are blocked until current legal sources are ingested?

## [2026-05-29] schema | Added reporting semantic layer and dashboards schema decision

- Continued the schema ADR sequence after projects/dimensions with the dashboards/reporting module. Designed reporting as a governed semantic layer instead of ad-hoc per-screen SQL, resolving the entry page's "operational tables vs curated views vs service APIs" question in favor of curated datasets.
- Decided versioned `kpi_definitions`/`report_definitions`/`dashboard_definitions`/`dashboard_widgets`/`reporting_datasets` as metric-meaning source of truth; dashboards and AI read only tenant-scoped, permission-filtered `reporting_datasets` (never operational tables); per-value freshness state (`live|cached|snapshot|stale|blocked`) driven by `data_quality_flags`; async `report_runs` and separate audited `report_exports`; `kpi_snapshots` for trend/history.
- Established gates: every read passes user-permission AND (where plan-gated) tenant-entitlement; sensitive payroll/fiscal-raw tiers reuse the permissions-ADR evidence tiers; statutory (SAF-T/IVA) reports stay owned/validated by fiscal/accounting modules and are labeled distinctly from management analytics; an `ai_safe` dataset flag is the only surface the AI layer may consume — the contract the next ADR builds on.
- New permission keys (`report.*`, `kpi.manage`, `dashboard.manage`, `reporting.dataset_manage`) flagged for the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]].
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards.md`
- Files updated:
  - `Dashboards e Relatorios ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - First post-login dashboard and the launch value-proving KPIs?
  - Live vs cached vs daily-snapshot freshness per metric; which exports are MVP?
  - Which dashboards are plan-gated; which datasets are approved `ai_safe` for launch?
  - Tenant-defined custom KPIs in scope or system-defined only?

## [2026-05-29] schema | Added project and analytical-dimensions schema decision

- Continued the schema ADR sequence after permissions/audit with the projects module. Resolved the entry page's open project-vs-cost-center question by modeling both as types of one generic analytical-dimension layer rather than a standalone projects subsystem.
- Decided `analytical_dimensions` (typed catalog), `dimension_values`, polymorphic `dimension_tags` (source_type/source_id/line, split allocation by full/percent/amount), `projects` registered as a project-type dimension value with `project_budgets`/`project_budget_lines`/milestones/status events, and derived `project_cost_events`/`project_revenue_events`/`project_forecasts` with no stored totals.
- Established invariants: projects never issue documents or post journal entries; all figures derive from tagged source records following each source's correction lineage; operational profitability, cash flow and accounting profit are labeled distinctly; the `dimension_tags` capability ships from day one so projects/cost-centers are a feature toggle, not a destructive migration.
- New permission keys (`project.*`, `dimension.manage`) flagged to feed the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]].
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Project and Analytical Dimensions.md`
- Files updated:
  - `Projetos ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Projects as a first-release dimension or a later full module?
  - Header-level cascading tags or line-level only?
  - Which dimensions are mandatory per module (`is_required_for`)?
  - Do profitability projections need materialization at launch scale?

## [2026-05-29] schema | Added permission catalog and audit taxonomy schema decision

- Continued the schema ADR sequence after SaaS subscriptions, taking the next maintenance-queue item (permissions/audit). Designed it to extend, not duplicate, [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]], which already owns the RBAC tables and the default-deny membership-keyed RLS pattern.
- Committed the `module.action` permission key convention and launch catalog, a `permission_groups` risk grouping, `user_permission_overrides` (tenant-scoped, reason-bound, expiring, revoke-wins), `audit_event_types` (typed catalog with `payload_policy` full/reference/hash_only), graduated status/raw/secret evidence access tiers, a provisional launch role→permission matrix, and the rule that every service-role/Edge-Function write attributes an initiating user plus correlation id.
- Resolved the foundation's open questions on the launch role set, MVP audit keys and service-role attribution; reaffirmed that entitlement (SaaS plan) and permission (user action) are independent gates.
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy.md`
- Files updated:
  - `Permissoes e Auditoria ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Is `payroll_officer` a launch role or folded into admin/accountant?
  - Which audit event keys are hard release gates vs best-effort in MVP?
  - Do critical-risk permissions require a second-approver override workflow?
  - Membership/permission resolved via helper functions or denormalized into a JWT claim?

## [2026-05-29] schema | Added SaaS subscriptions billing and entitlements schema decision

- Continued the schema ADR sequence (the explicit "Next: subscription architecture" maintenance-queue item) after payroll and fixed-assets, grounding the decision in `raw/assets/SUBSCRIPTION_ARCHITECTURE.md` and the [[Subscricoes SaaS ERP]] entry page.
- Decided a platform-owned catalog (`saas_plans`/`saas_plan_prices`/`saas_plan_entitlements` + add-on trio) plus tenant-scoped contracts (`saas_subscriptions`/`saas_subscription_items`/`saas_subscription_entitlements`/`saas_subscription_snapshots`/`saas_subscription_events`/billing/usage), with **computed** effective entitlements frozen into immutable snapshots, a platform-admin-write/tenant-read RLS split specializing the tenant-foundation pattern, treasury-derived payment status, and deferred fiscal SaaS-invoicing scope. Preserved the legacy `saas_*` namespace.
- Established the key invariant: entitlement is a tenant access gate that never bypasses RBAC/RLS, never grants cross-tenant access and never deletes tenant data; payment status comes from treasury/provider evidence, not editable flags.
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements.md`
- Files updated:
  - `Subscricoes SaaS ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Does NOVA-ERP invoice its own SaaS via the fiscal module, an external provider, or platform-billing-only, and what is the Cabo Verde IVA/e-Fatura treatment?
  - Which launch plans/add-ons/limits, hard vs soft, and what grace/suspension model?
  - How is platform-admin access separated from tenant-admin at the auth/RLS layer, and who approves entitlement overrides?

## [2026-05-29] schema | Added payroll and fixed-assets schema decisions

- Continued schema work after the Supabase implementation artifact gap by producing provisional ADRs that do not depend on missing SQL artifacts.
- Created payroll schema decision for period-based payroll runs, rule-versioned components, immutable payslips, controlled reprocessing, privacy-specific permissions, treasury payment batches and accounting events.
- Created fixed-assets schema decision separating assets from inventory and modeling capitalization, depreciation policies/runs, transfers, maintenance, revaluation, disposal and accounting events.
- Updated payroll and assets module entry pages, index and log.
- Files created:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md`
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md`
- Files updated:
  - `Processamento de Salarios ERP.md`
  - `Gestao de Ativos ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which current Cabo Verde payroll, INPS, tax and labor sources govern statutory deductions and reports?
  - Which Cabo Verde depreciation methods, useful-life rules and tax limits must ship?
  - Are payroll and assets first-release modules or phase-two modules?

## [2026-05-29] maintain | Filed Supabase implementation artifact gap

- Continued from the financial-core schema ADR sequence by inspecting whether the vault contains actual Supabase implementation artifacts.
- Confirmed the vault has no `supabase/migrations`, `supabase/functions`, `supabase/seed.sql` or `.sql` migration files; current SQL/RLS/storage/Edge Function review is therefore blocked by missing implementation artifacts.
- Created an artifact-gap synthesis and updated Supabase deployment, the database snapshot contradiction, the database classification, and the index.
- Files created:
  - `wiki/syntheses/2026-05-29 - Supabase Implementation Artifact Gap.md`
- Files updated:
  - `wiki/concepts/Supabase Deployment.md`
  - `wiki/contradictions/Contradiction - Current Database Snapshot vs Target ERP Architecture.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/syntheses/2026-05-28 - Current Database Snapshot Classification.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Where is the application repository containing `supabase/migrations`, `supabase/functions` and `supabase/seed.sql`?
  - Should the next schema work proceed with payroll/assets ADRs while implementation artifacts are missing?
  - Should a Supabase schema/policy/storage export be requested if the repo cannot be attached?

## [2026-05-28] schema | Added accounting ledger and posting schema decision (financial core complete)

- Produced the fifth and final financial-core target schema ADR from [[2026-05-28 - Current Database Snapshot Classification]]: accounting as an immutable double-entry journal driven by posting rules over upstream events.
- Decided `chart_of_accounts`/`journals`/`accounting_periods`/`journal_entries`/`journal_entry_lines` (balanced, immutable, reversal-only), `posting_rules` (versioned event→debit/credit templates), `tax_maps` (IVA↔account↔SAF-T), projection-based balances/trial balance, period locks, and auto-draft + manual-post as MVP default. New build — no snapshot ledger to migrate.
- Accounting consumes the defined outputs of the three prior ADRs (fiscal snapshots, treasury allocations, inventory valuation), never raw DFE XML/ZIP/middleware/certificates; feeds [[SAF-T CV]].
- Fixed a malformed frontmatter line and a typo ("systown" → "system") in [[Contabilidade ERP]].
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Accounting Ledger and Posting.md`
- Files updated:
  - `index.md`
  - `Contabilidade ERP.md`
  - `log.md`
- Open questions:
  - Which Cabo Verde PNC chart-of-accounts standard/version seeds the default?
  - Full accounting in MVP or SAF-T-ready data first?
  - When is per-event auto-post enabled beyond MVP auto-draft/manual-post?

## [2026-05-28] schema | Added inventory movements and valuation schema decision

- Produced the fourth target schema ADR from [[2026-05-28 - Current Database Snapshot Classification]]: stock as the derived sum of an append-only movement ledger.
- Decided `items` with no stored quantity (on-hand derived), append-only source-linked `stock_movements`, `stock_reservations` (available vs on-hand split), `valuation_layers` (weighted-avg MVP, FIFO-capable), count reconciliation via movements, reversal-by-compensation, lot/serial schema-ready-but-off. Replaces snapshot `inventory_movements`/`products` stored quantity.
- Anchored to [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] and [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]; feeds the accounting ADR (COGS) and [[SAF-T CV]].
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Inventory Movements and Valuation.md`
- Files updated:
  - `index.md`
  - `Inventario ERP.md`
  - `log.md`
- Open questions:
  - FIFO in first release or deferred?
  - Materialized vs computed-on-read balance projections?
  - Negative on-hand (oversell) allowed or hard-blocked?

## [2026-05-28] schema | Added treasury receivables/payables/settlement schema decision

- Produced the third target schema ADR from [[2026-05-28 - Current Database Snapshot Classification]]: treasury as an obligation/movement/allocation ledger.
- Decided `obligations` (unified receivable/payable), append-only `treasury_movements`, a many-to-many `allocations` settlement join, derived (never hand-edited) payment status, reversal-by-compensation, `on_account` advances, and manual-first bank reconciliation. Replaces the snapshot's flat `financial_transactions`/`bank_accounts`.
- Anchored to [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]] and [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; feeds the upcoming accounting ADR.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement.md`
- Files updated:
  - `index.md`
  - `Tesouraria ERP.md`
  - `log.md`
- Open questions:
  - Single-currency MVP or FX gain/loss handling from day one?
  - Is `obligations.status` a maintained cache or a pure view?
  - Which bank import format (CSV/CAMT/API) ships first?

## [2026-05-28] schema | Added commercial and fiscal document core schema decision

- Produced the second target schema ADR from [[2026-05-28 - Current Database Snapshot Classification]]: the document core that the existing e-Fatura ADRs attach to.
- Split the snapshot's single `documents`/`document_items`/`document_series` into `commercial_documents` (operational intent) and `fiscal_documents` (immutable legal record with fiscal series + e-Fatura obligation); unified customers/suppliers into `entities` with a `kind` flag; connected transformations/corrections/one→many invoicing via a `document_links` graph; independent commercial vs fiscal numbering; no hard delete after number assignment.
- Resolved standing open questions in [[Compras e Vendas ERP]] (unify customers/suppliers) and [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] (header naming = split commercial/fiscal).
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Commercial and Fiscal Document Core.md`
- Files updated:
  - `index.md`
  - `Compras e Vendas ERP.md`
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission.md`
  - `log.md`
- Open questions:
  - Which commercial/fiscal document types are MVP-mandatory? (Needs backlog MVP cut.)
  - Should `document_links` integrity be trigger-enforced, app-enforced, or both?
  - How are partial delivery/invoice quantities tracked?

## [2026-05-28] schema | Added tenant foundation and RLS schema decision

- Produced the first target schema ADR from [[2026-05-28 - Current Database Snapshot Classification]]: the multi-tenant foundation that every other module schema depends on.
- Decided single-DB + default-deny, membership-keyed RLS; `tenants`/`tenant_members`/`roles`/`permissions`/`role_permissions`/`profiles`/`audit_log`/`platform_admins`; SECURITY DEFINER helper functions; append-only audit; platform-admin as an out-of-band allowlist rather than an in-tenant super-role.
- Advanced [[Contradiction - Current Database Snapshot vs Target ERP Architecture]]: first foundation ADR now exists; remaining gap is actual SQL/RLS inspection plus per-module target schemas.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Tenant Foundation and RLS.md`
- Files updated:
  - `index.md`
  - `wiki/contradictions/Contradiction - Current Database Snapshot vs Target ERP Architecture.md`
  - `log.md`
- Open questions:
  - What is the first launch role set beyond owner/admin/accountant/operator/viewer?
  - Should tenant membership be denormalized into a JWT claim for RLS performance, or resolved via helper functions?
  - How is tenant context propagated to Edge Functions and the e-Fatura middleware?

## [2026-05-28] maintain | Added e-Fatura evidence storage and secrets decision

- Created a provisional schema decision splitting e-Fatura storage into PostgreSQL metadata, private fiscal evidence artifacts and secret/private-key material.
- Used current Supabase documentation via Context7 on 2026-05-28 for private Storage, RLS, signed URLs and service-role/Edge Function secret boundaries.
- Updated e-Fatura, faturacao, configuration, Supabase deployment and prior e-Fatura schema decisions to use private fiscal evidence storage and metadata/reference-only certificate tables.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets.md`
- Files updated:
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `Faturacao Eletronica.md`
  - `Configuracao ERP.md`
  - `wiki/concepts/Supabase Deployment.md`
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission.md`
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura Event Payloads.md`
  - `wiki/sources/2026-05-28 - Supabase Deploy.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which legal retention period applies to DFE XML, event XML, ZIP archives, DFA/PDF renders and DNRE responses?
  - Which production secret manager or middleware keystore process is approved for PFX/private-key/passphrase material?
  - Should NOVA-ERP retain uploaded PFX after middleware keystore import or delete it after successful onboarding?

## [2026-05-28] maintain | Resolved e-Fatura middleware URL scope as hybrid topology

- Promoted the middleware URL scope contradiction into a provisional schema decision: environment default middleware endpoint, tenant-scoped e-Fatura readiness/settings and platform-admin-only tenant endpoint override.
- Marked [[Contradiction - Middleware URL Scope]] as superseded while preserving it as decision history.
- Updated e-Fatura, faturacao, configuration and Supabase deployment pages so middleware endpoint resolution is server-side and tenant operators cannot redirect fiscal traffic through arbitrary URLs.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration.md`
- Files updated:
  - `wiki/contradictions/Contradiction - Middleware URL Scope.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `Faturacao Eletronica.md`
  - `Configuracao ERP.md`
  - `wiki/concepts/Supabase Deployment.md`
  - `wiki/sources/2026-05-26 - Middleware e-Fatura Dev Local para VPS.md`
  - `wiki/sources/2026-05-26 - Instrucoes Oficiais NOVA-ERP.md`
  - `wiki/sources/2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0.md`
  - `wiki/sources/2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0.md`
  - `wiki/maps/Revisao Raw Assets - 2026-05-26.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Does DNRE middleware support emitter groups in production exactly as described by the project middleware guide?
  - Should onboarding sync to middleware be automatic after approval or operated through a supervised runbook?
  - Which secret manager/storage pattern is approved for PFX certificates, keystores, transmitter keys and client secrets?

## [2026-05-28] maintain | Added e-Fatura event payload schema decision

- Deep-inspected the official 2024-05-27 e-Fatura XSD package event files and captured the current event model.
- Created a schema decision for official event payloads: `FDC` for cancelamento/anulacao de DFE and `UDN` for inutilizacao de numero de documento.
- Updated e-Fatura and faturacao module pages so cancellation/anulation and unused-number handling are modeled as signed XML event workflows, not simple document-state mutations.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura Event Payloads.md`
- Files updated:
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `Faturacao Eletronica.md`
  - `wiki/sources/2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27.md`
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which current legal rules decide when a DFE can be cancelled/anulated with `FDC` versus corrected by NCE/NDE/DVE?
  - Should NOVA-ERP allow multi-IUD `FDC` events in the UI or restrict the first release to one IUD per event request?
  - Should `UDN` ship in MVP, or only after fiscal series administration is mature?

## [2026-05-28] maintain | Hardened SAF-T CV as audit export readiness domain

- Reworked [[SAF-T CV]] from a short export note into an audit/export readiness domain spanning fiscal documents, accounting, inventory, async jobs, validation, private artifacts, inconsistency reports, audit events and performance posture.
- Preserved uncertainty around the current official SAF-T CV schema/XSD and blocked production compliance claims until that source is ingested.
- Files created:
  - None
- Files updated:
  - `wiki/concepts/SAF-T CV.md`
  - `index.md`
  - `log.md`
- Open questions:
  - What is the current official SAF-T CV schema/XSD version?
  - Which SAF-T types are mandatory in production?
  - Should the first release ship full SAF-T or only SAF-T-ready data/jobs until accounting/inventory maturity?

## [2026-05-28] maintain | Hardened Supabase Deployment as production runtime boundary

- Ingested `raw/assets/SUPABASE_DEPLOY.md` as [[2026-05-28 - Supabase Deploy]].
- Reworked [[Supabase Deployment]] from a short deploy note into an operational runtime boundary covering migration gates, drift control, RLS/tenant isolation, Edge Functions, storage, secrets, e-Fatura deployment implications, rollout checklist, MVP acceptance criteria and non-MVP cautions.
- Updated [[Supabase]] with the security/runtime role of Supabase for NOVA-ERP.
- Files created:
  - `wiki/sources/2026-05-28 - Supabase Deploy.md`
- Files updated:
  - `wiki/concepts/Supabase Deployment.md`
  - `wiki/entities/Supabase.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which command set becomes the canonical release script?
  - Which RLS/security checks must run before production?
  - What is the approved storage model for e-Fatura certificates and signed XML/ZIP evidence?

## [2026-05-28] maintain | Created Configuracao ERP as tenant setup control plane

- Created [[Configuracao ERP]] as the tenant setup and parameterization module for company identity, fiscal profile, base currency, modules, document series, e-Fatura readiness, secure certificate references and controlled activation.
- Added design gates, candidate configuration domain model, tenant/setup state machines, fiscal and e-Fatura configuration boundaries, readiness gates, permission boundaries, audit events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - `Configuracao ERP.md`
- Files updated:
  - `index.md`
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `Bem-vindo.md`
  - `log.md`
- Open questions:
  - Which setup steps are mandatory for the first login-to-first-invoice path?
  - Should document series be generated during onboarding, configured manually, or both?
  - Who approves sensitive fiscal/e-Fatura configuration changes?

## [2026-05-28] maintain | Updated Dashboards e Relatorios ERP with governed reporting boundaries

- Reworked [[Dashboards e Relatorios ERP]] as the governed visibility layer for KPI definitions, curated reporting datasets, dashboards, exports, asynchronous report jobs and AI-safe analytics.
- Added design gates, candidate reporting domain model, report/freshness state machines, source/KPI/permission/export/AI boundaries, heavy report job posture, audit events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Dashboards e Relatorios ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which dashboard is the first screen after login?
  - Which KPIs prove product value in the first sellable release?
  - Which reporting views should be approved for [[IA Assistente ERP]]?

## [2026-05-28] maintain | Updated Gestao de Ativos ERP with fixed-asset lifecycle boundaries

- Reworked [[Gestao de Ativos ERP]] as a fixed-asset lifecycle module for acquisition, capitalization, depreciation, transfer, maintenance, revaluation, disposal and accounting evidence.
- Added design gates, candidate domain model, asset/depreciation state machines, acquisition/accounting/treasury/project boundaries, audit posture, domain events, MVP acceptance criteria and non-MVP legal cautions.
- Files created:
  - None
- Files updated:
  - `Gestao de Ativos ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which depreciation methods and statutory/tax rules are required for Cabo Verde companies?
  - Should asset management ship before or after full accounting?
  - Should purchase documents create draft assets automatically or require manual capitalization?

## [2026-05-28] maintain | Updated Subscricoes SaaS ERP with entitlement and billing boundaries

- Reworked [[Subscricoes SaaS ERP]] as the platform business layer for plan catalog, add-ons, subscription contracts, entitlements, billing runs, usage limits, lifecycle and access enforcement.
- Added design gates, candidate `saas_*` domain model, subscription/billing state machines, entitlement/permission boundaries, treasury/fiscal boundaries, access enforcement, audit posture, domain events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Subscricoes SaaS ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should NOVA-ERP use its own fiscal module to invoice SaaS subscriptions?
  - Which launch plans, modules and hard limits are required?
  - What grace period and suspension model should apply to overdue tenants?

## [2026-05-28] maintain | Updated Projetos ERP with analytical project boundaries

- Reworked [[Projetos ERP]] as an operational/analytical project dimension for budgets, allocations, profitability, cash effects and accountability.
- Added design gates, candidate domain model, project/budget state machines, commercial/treasury/accounting boundaries, payroll/inventory/assets integration notes, audit posture, domain events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Projetos ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should projects ship first as simple analytical dimensions or as a full project module?
  - Should project profitability depend first on document totals, treasury cash flow or accounting postings?
  - Should cost centers and projects be separate dimensions or a unified analytical dimension?

## [2026-05-28] maintain | Updated Processamento de Salarios ERP with payroll control boundaries

- Reworked [[Processamento de Salarios ERP]] as a controlled payroll subsystem with period-based runs, versioned calculations, payslip evidence, payment/accounting boundaries and strict privacy controls.
- Added design gates, candidate domain model, state machines, accounting/treasury boundaries, permission boundaries, audit posture, domain events, MVP acceptance criteria and non-MVP legal cautions.
- Files created:
  - None
- Files updated:
  - `Processamento de Salarios ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should payroll ship in the first sellable release or later?
  - Which current Cabo Verde payroll deductions, employer obligations and reports must be supported?
  - What launch roles can view salary data?

## [2026-05-28] maintain | Updated IA Assistente ERP with governed AI boundaries

- Reworked [[IA Assistente ERP]] as a governed, permission-aware AI layer instead of an unconstrained chatbot over ERP data.
- Added design gates, candidate AI domain model, suggestion/action state machines, data-access boundary, action boundary, audit/security posture, domain events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `IA Assistente ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should the first AI release be strictly read-only?
  - Which reporting views must exist before AI is useful?
  - Which provider/security posture is acceptable for sensitive Cabo Verde ERP data?

## [2026-05-28] maintain | Updated Inventario ERP with stock movement boundary

- Reworked [[Inventario ERP]] so stock is derived from auditable movements, reservations, receipts, deliveries, returns, adjustments and counts rather than a single product stock field.
- Added design gates, candidate domain model, state machines, commercial/accounting boundaries, audit posture, critical events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Inventario ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should sales orders reserve stock in MVP?
  - Should MVP support multiple warehouses or one warehouse per tenant?
  - Which valuation method should ship first?

## [2026-05-28] maintain | Updated Compras e Vendas ERP with commercial-to-fiscal boundaries

- Reworked [[Compras e Vendas ERP]] so commercial documents, fiscal documents, stock movements, treasury obligations and accounting postings are separated by explicit module boundaries.
- Added design gates, candidate domain model, state machines, fiscal/stock/treasury boundaries, audit events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Compras e Vendas ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which commercial document types ship in MVP?
  - Should invoice-receipt create fiscal issue and treasury movement atomically or through a controlled saga?

## [2026-05-28] maintain | Updated Tesouraria ERP with allocation and reconciliation boundary

- Reworked [[Tesouraria ERP]] so receipts/payments are treasury movements with allocations, reversals and reconciliation evidence, not direct `paid` flag changes.
- Added design gates, candidate domain model, state machines, accounting boundary, audit/security posture, domain events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Tesouraria ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should invoice-receipts create fiscal document and treasury movement in one transaction?
  - Should bank reconciliation be manual-first or import/API-ready in MVP?

## [2026-05-28] maintain | Updated Permissoes e Auditoria ERP as cross-module security boundary

- Reworked [[Permissoes e Auditoria ERP]] around tenant membership, RBAC, RLS, audit logs, fiscal/e-Fatura evidence access, certificate/secret handling and accounting controls.
- Added design gates, permission boundaries, audit event model, fiscal/e-Fatura audit requirements, accounting audit requirements, RLS posture, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Permissoes e Auditoria ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - What is the first launch role model?
  - Which RLS tests become mandatory release gates?
  - Who may view raw e-Fatura XML/ZIP/response bodies?

## [2026-05-28] maintain | Updated Contabilidade ERP with fiscal/e-Fatura accounting boundary

- Reworked [[Contabilidade ERP]] to reflect the new e-Fatura schema decision and fiscal-document boundary.
- Clarified that accounting consumes immutable fiscal snapshots and operational events, not raw DFE XML, ZIP archives, middleware headers or certificate material.
- Added design gates, candidate accounting domain model, state machines, domain events, MVP acceptance criteria and non-MVP cautions.
- Files created:
  - None
- Files updated:
  - `Contabilidade ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should accounting post fiscal documents immediately, after PE authorization, or by configurable policy?
  - What current Cabo Verde accounting/SAF-T sources must be ingested before final accounting schema?

## [2026-05-28] schema | Added e-Fatura DFE payload and transmission schema decision

- Created the first fiscal schema decision page for e-Fatura DFE payload and transmission boundaries.
- Defined provisional records for fiscal documents, series, snapshots, DFE payloads, validation results, transmission batches/attempts, references, contingency, self-billing, rappel periods and certificate references.
- Linked the decision from [[Faturacao Eletronica]], [[e-Fatura Cabo Verde]], [[Fiscalidade Cabo Verde]] and `index.md`.
- Files created:
  - `wiki/syntheses/2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission.md`
- Files updated:
  - `Faturacao Eletronica.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should the business header be named `fiscal_documents`, `sales_documents`, or split into commercial and fiscal documents?
  - Which event XSDs are needed before cancellation/anulation/inutilization workflows?
  - Where should raw XML/ZIP/response bodies and certificate material live operationally?

## [2026-05-28] maintain | Updated Fiscalidade Cabo Verde with v11/XSD and schema boundaries

- Reworked [[Fiscalidade Cabo Verde]] as the central fiscal synthesis page tying together invoice-rule substance, modern e-Fatura technical authority, XSD package constraints and current database reuse boundaries.
- Clarified the separation between fiscal rule layer, e-Fatura technical layer, database model boundary and legacy ERP workflow reference.
- Added implementation implications and an uncertainty register for current legal verification, public works/State invoicing, reverse charge, e-Fatura events and SQL/RLS/storage inspection.
- Files created:
  - None
- Files updated:
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `log.md`
- Open questions:
  - Which current CIVA/REMPE legal sources should be ingested next?
  - Should the first fiscal schema decision cover tenant fiscal configuration, fiscal documents, or DFE payload/transmission?

## [2026-05-28] ingest | Deep-ingested current database ER snapshot

- Deep-ingested `raw/assets/DATABASE_ER_DIAGRAM.md` as current database snapshot evidence, not target architecture authority.
- Created a classification synthesis separating adapt candidates, replace/split compliance areas, optional/non-core support areas and archive/reframe e-commerce/POS tables.
- Updated the database-vs-target contradiction: ER ingestion and first classification are now done; remaining work is actual SQL/RLS/storage inspection and target schema decisions.
- Files created:
  - `wiki/sources/2026-05-28 - DATABASE ER Diagram Snapshot.md`
  - `wiki/syntheses/2026-05-28 - Current Database Snapshot Classification.md`
- Files updated:
  - `wiki/contradictions/Contradiction - Current Database Snapshot vs Target ERP Architecture.md`
  - `wiki/concepts/ERP SaaS Multi-Tenant.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `log.md`
- Open questions:
  - Which real SQL migrations, RLS policies and storage policies exist behind the diagram?
  - Which current tables contain production data that must be migrated?
  - Should the first target schema decision page cover tenant foundation or fiscal/e-Fatura document payloads?

## [2026-05-28] maintain | Added contradiction and schema decision templates

- Added a contradiction template for source conflicts, superseded assumptions and unresolved implementation tensions.
- Added a schema decision template for data model, state/event, tenancy, RLS and validation decisions.
- Updated `index.md` so the new templates are discoverable.
- Normalized the existing middleware URL, e-Fatura sync/async and database-snapshot contradictions with implementation risk and resolution criteria.
- Files created:
  - `templates/contradiction.md`
  - `templates/schema-decision.md`
- Files updated:
  - `index.md`
  - `wiki/contradictions/Contradiction - Middleware URL Scope.md`
  - `wiki/contradictions/Contradiction - e-Fatura Sync Authorization vs Async ERP Queue.md`
  - `wiki/contradictions/Contradiction - Current Database Snapshot vs Target ERP Architecture.md`
  - `log.md`
- Open questions:
  - Should e-Fatura DFE payload/transmission model become the first schema decision page?

## [2026-05-28] maintain | Hardened wiki templates for implementation-grade ingests

- Updated source, concept, entity, module, synthesis and question templates so future pages capture authority, currency, uncertainty, implementation impact, security/audit concerns and decision boundaries by default.
- Added template descriptions to `index.md` so agents can find and use them during wiki work.
- Files created:
  - None
- Files updated:
  - `templates/source-summary.md`
  - `templates/concept.md`
  - `templates/entity.md`
  - `templates/module.md`
  - `templates/synthesis.md`
  - `templates/question-answer.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should the vault add a contradiction template and a schema/ADR template next?

## [2026-05-28] ingest | Deep-ingested e-Fatura technical manual v11.0 at schema/API level

- Deep-ingested the official `Manual Tecnico da Fatura Eletronica v11.0` and confirmed it supersedes v10.0 for current schema/API implementation authority.
- Added the official `2024-05-27-XML-XSD` package as a separate source because it is the executable schema contract for DFE XML, signatures, field map and examples.
- Captured implementation-critical rules: XML namespace/root attributes, IUD/LED/numbering, DFE type vocabulary, emitter/receiver constraints, tax/line/totals structure, `IssueReasonCode`, `RappelPeriod`, references, DTE route, contingency/DFA, OAuth scopes, DFE ZIP multipart submission, middleware headers and self-billing authorization.
- Updated the e-Fatura and Faturacao Eletronica pages with schema/API gates and candidate domain objects for DFE payloads, XSD validation results, transmission batches, references, contingency, self-billing, rappel periods and transport routes.
- Files created:
  - `wiki/sources/2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27.md`
- Files updated:
  - `wiki/sources/2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `Faturacao Eletronica.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `log.md`
- Open questions:
  - Which event XSDs/examples must ship first for cancellation, anulacao, inutilizacao and rectification?
  - Which official legal/despacho sources must be paired with v11.0 before production compliance claims?
  - How should middleware topology be resolved for multi-tenant production under [[Contradiction - Middleware URL Scope]]?

## [2026-05-28] query | Verified 2018 invoice manual against modern e-Fatura

- Checked current official e-Fatura sources and found the official manual page now lists v11.0 as latest, superseding the previous v10.0 implementation-authority assumption.
- Classified 2018 `MANUAL DE FATURAS.pdf` rules: fiscal substance survives, paper/electronic-invoice processing mechanics are superseded or narrowed, and public works/reverse-charge/penalty details remain unresolved.
- Created a durable question answer and a source stub for the v11.0 technical manual.
- Files created:
  - `wiki/questions/2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura.md`
  - `wiki/sources/2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0.md`
- Files updated:
  - `Faturacao Eletronica.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/sources/2026-05-28 - Manual de Faturas em Cabo Verde.md`
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `wiki/entities/DNRE.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `log.md`
- Open questions:
  - What v11.0 schema changes affect NOVA-ERP tables and Edge Functions?
  - Which current legal texts govern public works/State invoicing and reverse charge?
  - How should recipient manifestation be modeled for rectification documents reducing taxable value?

## [2026-05-28] ingest | Ingested Manual de Faturas em Cabo Verde

- Deep-ingested `docs/docsfiscal/MANUAL DE FATURAS.pdf` as an orientative DNRE/SITA invoice-rule map for issuance timing, required invoice fields, software numbering, authorized printers, rectification documents, REMPE, State/public works invoicing, reverse charge, transport documents, electronic invoice storage and sanctions.
- Marked the source as non-normative and dated May 2018; current law/e-Fatura guidance remains required before production compliance claims.
- Updated electronic invoicing, fiscality, purchases/sales, DNRE and source maps with implementation implications: no deletion after number assignment, explicit void/rectification flows, tax-regime-specific wording, transport document scope and audit-grade retention.
- Files created:
  - `wiki/sources/2026-05-28 - Manual de Faturas em Cabo Verde.md`
- Files updated:
  - `Faturacao Eletronica.md`
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `Compras e Vendas ERP.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/entities/DNRE.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which 2018 invoice-manual rules remain current after Decreto-Lei n.º 79/2020 and the current e-Fatura rollout?
  - Which fiscal document types must ship in the first sellable release?
  - How should NOVA-ERP represent voided/inutilized invoice numbers under current e-Fatura event schemas?

## [2026-05-27] ingest | Ingested e-Fatura technical manual v10.0

- Deep-ingested `docs/docsfiscal/manual-tecnico-da-fatura-eletronica-v10.0-81ac76da0d05ec36abdb626087cda762.pdf` as the DNRE technical contract for DFE XML, IUD, document types, validation, authorization, contingency, APIs and middleware.
- Verified via DNRE e-Fatura manual page that v10.0 is listed as the latest manual version on 2026-05-27.
- Reconciled candidate states in `Faturacao Eletronica.md`: official states/modes now distinguish PE/DNRE authorization and contingency from NOVA-ERP internal queue/retry states.
- Opened a contradiction/tension page for official synchronous PE authorization versus NOVA-ERP internal async orchestration.
- Files created:
  - `wiki/sources/2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0.md`
  - `wiki/contradictions/Contradiction - e-Fatura Sync Authorization vs Async ERP Queue.md`
- Files updated:
  - `Faturacao Eletronica.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/entities/DNRE.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which event XML structures for cancellation/anulation and number invalidation must ship in MVP?
  - Which invoice business rules from `MANUAL DE FATURAS.pdf` constrain correction/cancellation UX?
  - Should NOVA-ERP expose direct PE API as a fallback, or enforce middleware-only production policy?

## [2026-05-27] maintain | Expanded electronic invoicing domain model

- Continued `Faturacao Eletronica.md` with a candidate domain model, state machine, transition rules, audit events, permission boundaries, MVP acceptance criteria and non-MVP compliance cautions.
- Files created:
  - None
- Files updated:
  - `Faturacao Eletronica.md`
  - `log.md`
- Open questions:
  - Which candidate states survive once the official e-Fatura manual is fully ingested?
  - Which cancellation/correction transitions are legally valid in Cabo Verde?
  - Which event names should become the canonical domain event vocabulary in code?

## [2026-05-27] maintain | Continued electronic invoicing module note

- Expanded `Faturacao Eletronica.md` from a short ingestion target list into an implementation-oriented continuation with ingestion sequence, design gates, implementation shape and uncertainty register.
- Files created:
  - None
- Files updated:
  - `Faturacao Eletronica.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which e-Fatura and invoice manuals are current production authority for Cabo Verde?
  - Which document types and technical states must ship in the first sellable release?
  - What secure certificate/keystore operating model should NOVA-ERP adopt?

## [2026-05-26] ingest | Consolidated e-Fatura middleware guide

- Deep-ingested `raw/assets/NOVA-ERP_Middleware_Dev_Local_para_VPS.md` as the operational guide for local, staging and production middleware deployment.
- Created a source page covering environment model, shared middleware endpoint, tenant emitter/certificate onboarding, Edge Function submission, contingency queue, retry and security notes.
- Refined the middleware URL contradiction toward a hybrid working interpretation: environment-level middleware endpoint plus tenant-level e-Fatura configuration.
- Updated e-Fatura and electronic invoicing pages with the operational flow.
- Files created:
  - `wiki/sources/2026-05-26 - Middleware e-Fatura Dev Local para VPS.md`
- Files updated:
  - `wiki/contradictions/Contradiction - Middleware URL Scope.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `Faturacao Eletronica.md`
  - `wiki/syntheses/NOVA-ERP Product Authority Synthesis.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/maps/Revisao Raw Assets - 2026-05-26.md`
  - `log.md`
- Open questions:
  - Does DNRE middleware officially support multi-tenant emitter groups as described?
  - Should tenant middleware onboarding restart middleware automatically or require admin approval?
  - What is the secure storage pattern for tenant certificates and client secrets?

## [2026-05-26] ingest | Consolidated official project instructions

- Deep-ingested `raw/assets/NOVA-ERP_Instrucoes_Oficiais_1.md` as official project instructions for fiscal-first posture, enterprise quality, e-Fatura middleware expectations and UX direction.
- Updated product authority and module priority syntheses to include the official instructions as operating posture, not legal authority.
- Updated the middleware URL contradiction because the official instructions strengthen the tenant-scoped configuration position.
- Files created:
  - `wiki/sources/2026-05-26 - Instrucoes Oficiais NOVA-ERP.md`
- Files updated:
  - `wiki/contradictions/Contradiction - Middleware URL Scope.md`
  - `wiki/syntheses/NOVA-ERP Product Authority Synthesis.md`
  - `wiki/syntheses/NOVA-ERP Module Priority Map.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/maps/Revisao Raw Assets - 2026-05-26.md`
  - `log.md`
- Open questions:
  - Which fiscal claims in the official instructions remain current under Cabo Verde law and DNRE guidance?
  - Should middleware URL config be hybrid: environment default plus tenant override?
  - Should dark premium blue/orange become a binding design-system requirement?

## [2026-05-26] ingest | Consolidated implementation prompt

- Deep-ingested `raw/assets/SSD/PROMPT.MD` as the implementation prompt for the NOVA-ERP foundation release.
- Created a source page summarizing required stack, modules, data model signals, screens, components, RLS/security, seed and execution order.
- Updated product authority and module priority syntheses to distinguish product authority from foundation-release implementation authority.
- Files created:
  - `wiki/sources/2026-05-26 - Prompt Implementacao NOVA-ERP.md`
- Files updated:
  - `wiki/syntheses/NOVA-ERP Product Authority Synthesis.md`
  - `wiki/syntheses/NOVA-ERP Module Priority Map.md`
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/maps/Revisao Raw Assets - 2026-05-26.md`
  - `log.md`
- Open questions:
  - Which backlog acceptance criteria become tests for the foundation release?
  - Can the current database be reused safely, or should the foundation schema be rebuilt from the prompt/SSD?
  - Should official instructions or middleware guide be consolidated next?

## [2026-05-26] lint | Reviewed raw assets source corpus

- Reviewed `raw/assets/` without editing raw sources.
- Created a source review report covering inventory, authority, risks, sensitive-secret handling, encoding quality and next ingestion order.
- Opened contradiction pages for current database drift and middleware URL scope.
- Files created:
  - `wiki/maps/Revisao Raw Assets - 2026-05-26.md`
  - `wiki/contradictions/Contradiction - Current Database Snapshot vs Target ERP Architecture.md`
  - `wiki/contradictions/Contradiction - Middleware URL Scope.md`
- Files updated:
  - `index.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `log.md`
- Open questions:
  - Should the current ER diagram be migrated, replaced, or treated only as legacy-state evidence?
  - Should e-Fatura middleware configuration be environment-level, tenant-level, or hybrid?
  - Which raw asset should be deep-ingested next: `PROMPT.MD`, official instructions, or middleware deployment guide?

## [2026-05-26] ingest | Deep-ingested NOVA-ERP PRD, SSD and backlog

- Deep-ingested the canonical product sources for NOVA-ERP: PRD, SSD and structured backlog.
- Created source pages for each document and a synthesis that defines source authority: PRD for product intent, SSD for implementation requirements, backlog for execution.
- Updated the module priority map after ingestion and recorded the key tension between MVP SAF-T/fiscality and phase-2 full accounting.
- Files created:
  - `wiki/sources/2026-05-26 - PRD NOVA-ERP.md`
  - `wiki/sources/2026-05-26 - SSD NOVA-ERP.md`
  - `wiki/sources/2026-05-26 - Backlog Estruturado NOVA-ERP.md`
  - `wiki/syntheses/NOVA-ERP Product Authority Synthesis.md`
- Files updated:
  - `wiki/syntheses/NOVA-ERP Module Priority Map.md`
  - `wiki/projects/NOVA-ERP.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should partial accounting infrastructure be included in MVP because SAF-T/fiscality depends on accounting-grade data?
  - Which official Cabo Verde fiscal sources are current enough to govern e-Fatura, SAF-T, IVA and payroll implementation?
  - Which backlog acceptance criteria should become automated tests first?

## [2026-05-26] maintain | Added intelligence and priority layer

- Added module entry pages for projects, dashboards/reports and AI assistant.
- Created a first-pass module priority synthesis separating foundation, fiscal/commercial core, accounting/operational depth, platform business layer and intelligence layer.
- Updated the knowledge architecture map, main index and welcome page.
- Files created:
  - `Projetos ERP.md`
  - `Dashboards e Relatorios ERP.md`
  - `IA Assistente ERP.md`
  - `wiki/syntheses/NOVA-ERP Module Priority Map.md`
- Files updated:
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `index.md`
  - `Bem-vindo.md`
  - `log.md`
- Open questions:
  - Which dashboards must ship in the first usable release?
  - Should the AI assistant be read-only at launch?
  - Should project profitability depend on accounting, treasury cash flow or operational document totals?
  - How should the module priority map change after deep ingestion of PRD, SSD and backlog?

## [2026-05-26] maintain | Expanded NOVA-ERP module spine

- Continued adapting the vault from generic wiki into NOVA-ERP module knowledge architecture.
- Created first-pass module entry pages for treasury, purchases/sales, assets, SaaS subscriptions and permissions/audit.
- Updated the knowledge architecture map, main index and welcome page so the new modules are navigable.
- Files created:
  - `Tesouraria ERP.md`
  - `Compras e Vendas ERP.md`
  - `Gestao de Ativos ERP.md`
  - `Subscricoes SaaS ERP.md`
  - `Permissoes e Auditoria ERP.md`
- Files updated:
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `index.md`
  - `Bem-vindo.md`
  - `log.md`
- Open questions:
  - Which treasury workflows must ship in the first sellable release?
  - Should NOVA-ERP use its own invoicing module to bill SaaS subscriptions?
  - Which MVP actions require immutable audit logs?
  - Which Cabo Verde-specific treasury, asset and payroll legal requirements need authoritative verification?

## [2026-05-26] schema | Adapted wiki to NOVA-ERP Cabo Verde

- Adapted the operating schema from a generic LLM Wiki into a NOVA-ERP Cabo Verde product, fiscal, domain and engineering knowledge base.
- Added project-specific domain priority, evidence hierarchy, module design workflow and legal/fiscal caution rules.
- Created a knowledge architecture map and a reusable ERP module template.
- Filled previously empty module entry pages for electronic invoicing, accounting, inventory and payroll.
- Files created:
  - `wiki/maps/NOVA-ERP Knowledge Architecture.md`
  - `templates/module.md`
- Files updated:
  - `CLAUDE.md`
  - `AGENTS.md`
  - `Bem-vindo.md`
  - `index.md`
  - `Faturacao Eletronica.md`
  - `Contabilidade ERP.md`
  - `Inventario ERP.md`
  - `Processamento de Salarios ERP.md`
  - `log.md`
- Open questions:
  - Which source should become the canonical product authority: PRD, SSD, or a reconciled synthesis?
  - Which Cabo Verde payroll legal sources should be ingested before payroll implementation?
  - Should root-level module notes be migrated into `wiki/concepts/` later, or kept as Obsidian entry points?

## [2026-05-26] ingest | Captured raw and docs source folders

- Captured source information from `raw/` and `docs/`.
- Created consolidated source capture for NOVA-ERP product/architecture docs and fiscal/Cegid Primavera reference docs.
- Created project page for NOVA-ERP.
- Created concept pages for ERP SaaS multi-tenancy, Cabo Verde fiscality, e-Fatura Cabo Verde, SAF-T CV and Supabase deployment.
- Created entity/place pages for Cegid Primavera, DNRE, Supabase and Cabo Verde.
- Files created:
  - `wiki/sources/2026-05-26 - Captura Raw e Docs.md`
  - `wiki/projects/NOVA-ERP.md`
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`
  - `wiki/concepts/ERP SaaS Multi-Tenant.md`
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `wiki/concepts/e-Fatura Cabo Verde.md`
  - `wiki/concepts/SAF-T CV.md`
  - `wiki/concepts/Supabase Deployment.md`
  - `wiki/entities/Cegid Primavera.md`
  - `wiki/entities/DNRE.md`
  - `wiki/entities/Supabase.md`
  - `wiki/places/Cabo Verde.md`
- Files updated:
  - `index.md`
  - `log.md`
- Open questions:
  - Which NOVA-ERP source should be canonical: PRD, SSD, or synthesized spec?
  - Which fiscal requirements must be verified against current Cabo Verde law before implementation?

## [2026-05-26] setup | LLM Wiki initialized

- Created the core second-brain structure.
- Added `raw/` for immutable sources.
- Added `wiki/` for LLM-maintained knowledge pages.
- Added `index.md` as the content catalog.
- Added `log.md` as the chronological activity record.
- Added `CLAUDE.md` as the primary operating schema.
- Added `AGENTS.md` as the Codex bridge.
- Added `.gitignore` for OS/editor noise and local Obsidian workspace state.
- Initialized git for version history.
