---
type: concept
status: active
created: 2026-05-28
updated: 2026-05-28
tags: [erp-module, configuration, tenancy, fiscalidade, setup]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[e-Fatura Cabo Verde]]", "[[Subscricoes SaaS ERP]]", "[[Supabase Deployment]]", "[[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]", "[[2026-05-28 - Schema Decision - e-Fatura Evidence Storage and Secrets]]"]
confidence: high
---

# Configuracao ERP

## Purpose

Configuracao ERP is the tenant setup and parameterization module for [[NOVA-ERP]]: company identity, fiscal profile, base currency, timezone, active modules, document series, tax setup, e-Fatura readiness, default operational policies and controlled setup completion.

It is not a miscellaneous settings drawer. It is the control plane that determines whether a tenant is allowed to operate, issue fiscal documents, calculate taxes, use modules, send e-Fatura payloads and expose data safely.

## Role In NOVA-ERP

The product sources make configuration part of the foundation layer. A company starts in `setup_pending`, must define country, base currency, fiscal regime and minimum operational settings, and only becomes usable after its required setup gates are satisfied.

Configuration must be tenant-scoped, permissioned, auditable and version-aware. In a Cabo Verde fiscal ERP, changing fiscal regime, document series, tax rates, middleware/e-Fatura readiness or certificate references can alter legal behavior and must never be a casual update.

Source: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Execution decomposition: [[2026-05-26 - Backlog Estruturado NOVA-ERP]], [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- Fiscal/e-Fatura posture: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]
- Middleware operations: [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]], [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]]
- Current database evidence: [[2026-05-28 - DATABASE ER Diagram Snapshot]], [[2026-05-28 - Current Database Snapshot Classification]]
- Security boundary: [[Permissoes e Auditoria ERP]], [[ERP SaaS Multi-Tenant]]

## Design Gates Before Implementation

- Tenant setup gate: define tenant lifecycle, required setup checklist and activation criteria before business modules create operational records.
- Versioning gate: decide which settings are effective-dated or versioned before fiscal documents, tax calculations or accounting postings depend on them.
- Permission gate: separate view settings, edit company profile, edit fiscal settings, edit e-Fatura settings, manage certificates, activate modules and complete setup.
- Audit gate: all high-risk setting changes must record actor, tenant, old value, new value, reason and effective date.
- Fiscal gate: tax regime, document series, tax rates and e-Fatura repository/middleware settings must be valid before final fiscal document issuance.
- Secret gate: certificates, client secrets, transmitter keys and keystore references must not live in ordinary configuration rows as plaintext.
- UX gate: setup should be a guided operational readiness workflow, not a long unstructured admin form.

## Core Workflows

- Create tenant/company with name, NIF, country, base currency and fiscal regime.
- Create initial owner/admin and register audit event.
- Complete onboarding checklist before tenant activation.
- Configure company identity and fiscal identity.
- Configure base currency, timezone, language and numbering defaults.
- Configure modules, feature flags and SaaS entitlements.
- Configure tax regimes, tax rates, exemptions and fiscal periods.
- Configure document types and fiscal series before sales/fiscal issuance.
- Configure e-Fatura readiness: repository, emitter identity, middleware linkage and certificate metadata.
- Test e-Fatura middleware/network health without exposing secrets.
- Lock or version settings already used by issued fiscal documents.
- Review setting change history and readiness status.

## Required Master Data

- Tenant/company identity: legal name, trade name, NIF, country, address, contacts and status.
- Localization defaults: base currency, timezone, locale/language and date/number formatting.
- Fiscal profile: tax regime, IVA/REMPE posture, fiscal periods and tax profile status.
- Module catalog: enabled modules, rollout stage, plan entitlement and tenant-level overrides.
- Document setup: document types, fiscal series, LED mapping, numbering policy and active periods.
- e-Fatura setup: repository code, emitter identifiers, integration readiness, certificate metadata references and middleware health status.
- Operational defaults: default warehouse, default payment terms, default bank/cash account, default accounts or posting profiles where applicable.
- Security metadata: roles allowed to mutate each configuration area and audit event types.

## Candidate Domain Model

- `tenants`: company/account boundary, lifecycle status, legal identity and operational status.
- `tenant_profiles`: commercial/legal profile, address, contacts, country, base currency, timezone and locale.
- `tenant_setup_checklists`: required setup steps, completion status, blocker messages and activation readiness.
- `tenant_module_settings`: enabled modules, rollout state, entitlement source and overrides.
- `tenant_feature_flags`: tenant-level feature switches, origin, expiry and audit metadata.
- `tenant_fiscal_profiles`: fiscal regime, effective period, IVA/REMPE flags, declaration cadence and verification status.
- `tax_rates`: country/tax code/rate definitions, effective dates and source reference.
- `tenant_tax_settings`: tenant-specific applicability, defaults and exemptions.
- `fiscal_periods`: tenant fiscal periods, open/locked/closed state and reporting boundaries.
- `document_types`: official/internal document type catalog and fiscal behavior.
- `document_series`: tenant series, fiscal year, document type, LED code, current counter, status and no-reuse guardrails.
- `tenant_efatura_settings`: repository code, emitter onboarding status, middleware mode/linkage and readiness checks.
- `tenant_certificate_refs`: certificate metadata, secure storage reference, validity dates and rotation status; no raw secret material.
- `tenant_integration_settings`: non-secret integration endpoints, health status, last check and configuration scope.
- `configuration_change_requests`: proposed sensitive changes, approval state, reason and effective date.
- `configuration_versions`: immutable snapshots used by fiscal documents, accounting postings, payroll runs or reports.
- `configuration_audit_events`: append-only setting changes linked to actor, source module and affected records.

## Candidate State Machine

### Tenant Setup State

- `draft`: tenant record exists but required identity is incomplete.
- `setup_pending`: tenant has owner/admin but required configuration is incomplete.
- `ready_for_activation`: required gates are satisfied and pending activation.
- `active`: tenant can operate according to enabled modules and permissions.
- `suspended`: tenant access is restricted by SaaS/admin/compliance rule.
- `archived`: tenant is no longer operational but retained for audit/history.

### Configuration Change State

- `draft`: change is being prepared.
- `pending_approval`: change affects fiscal/security/integration behavior and needs approval.
- `scheduled`: approved change has a future effective date.
- `effective`: change is active.
- `superseded`: newer effective configuration replaced it.
- `rejected`: proposed change was denied.
- `rolled_back`: change was reversed through an auditable corrective action.

## Configuration Readiness Gates

A tenant should not issue fiscal documents until these gates pass:

- company legal identity and NIF are present;
- country, base currency and timezone are defined;
- fiscal regime is defined and effective;
- required tax rates or exemptions are configured;
- at least one valid fiscal document type and series exists for the document being issued;
- e-Fatura settings are ready for document types requiring transmission;
- certificate/reference and middleware readiness checks pass where production e-Fatura is enabled;
- user has explicit permissions for the operation;
- no fiscal/accounting period lock prevents the action.

Source: [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]], [[Faturacao Eletronica]]

## Fiscal Configuration Boundary

Fiscal configuration belongs here as tenant setup, but fiscal interpretation belongs to [[Fiscalidade Cabo Verde]] and document execution belongs to [[Faturacao Eletronica]].

Configuracao ERP should store and validate:

- tenant fiscal regime;
- applicable tax profiles;
- tax rates and effective dates;
- fiscal periods;
- document type availability;
- fiscal series/LED mapping;
- minimum readiness status for fiscal issuing.

It should not hardcode legal conclusions without current authority. Tax rules, REMPE treatment, public works special series, reverse-charge wording and legal retention requirements remain compliance-sensitive and must be verified against current Cabo Verde authority before production claims.

## e-Fatura Configuration Boundary

The v11.0 technical manual requires explicit modeling of repository, LED, DFE identifiers, middleware configuration and secure certificate/secret handling. NOVA-ERP should separate:

- environment-level middleware endpoint or platform integration setting;
- tenant-level emitter identity and e-Fatura readiness;
- repository code and DNRE environment context;
- certificate metadata/reference from secret material;
- health checks and onboarding status from actual DFE transmissions.

The middleware topology decision is now: environment-level default endpoint, tenant-level e-Fatura emitter/readiness configuration, and tenant endpoint override only as a platform-admin controlled exception. Implementation should preserve this layered abstraction so ordinary tenant admins cannot redirect fiscal traffic, while future multi-middleware deployments remain possible.

Related: [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]], [[Contradiction - Middleware URL Scope]], [[2026-05-28 - Manual Tecnico da Fatura Eletronica v11.0]], [[2026-05-26 - Middleware e-Fatura Dev Local para VPS]]

## Permission Boundaries

Minimum permissions:

- view configuration;
- edit company identity;
- edit localization/defaults;
- manage setup checklist;
- manage module activation;
- manage feature flags;
- manage fiscal profile;
- manage tax rates/settings;
- manage document series;
- manage e-Fatura settings;
- upload/rotate certificate references;
- test integration health;
- approve sensitive configuration changes;
- view configuration audit history.

These must be tenant-scoped and separated from SaaS platform-owner permissions.

## Audit, Security And Tenancy

- Every configuration row must be tenant-scoped unless it is an explicitly global catalog.
- Fiscal, e-Fatura, security and module-entitlement changes must be audited.
- Settings used by issued fiscal documents, accounting entries, payroll runs or reports should be snapshotted or version-linked.
- Tenant admins should not see raw secrets, private keys, keystore contents or service-role tokens.
- Storage for certificates and sensitive integration artifacts must be private and governed by [[Permissoes e Auditoria ERP]].
- Raw PFX/private keys/passphrases must not be stored in ordinary configuration tables; use metadata/references and controlled onboarding artifacts only.
- Platform-level defaults must not mutate tenant behavior silently after activation.

## Critical Domain Events

- `tenant.created`
- `tenant.owner_created`
- `tenant.setup_step_completed`
- `tenant.activated`
- `tenant.suspended`
- `tenant.module_enabled`
- `tenant.feature_flag_changed`
- `tenant.fiscal_profile_changed`
- `tenant.tax_setting_changed`
- `tenant.document_series_created`
- `tenant.document_series_changed`
- `tenant.efatura_settings_changed`
- `tenant.efatura_middleware_binding_changed`
- `tenant.efatura_onboarding_requested`
- `tenant.efatura_onboarding_completed`
- `tenant.certificate_ref_uploaded`
- `tenant.certificate_ref_rotated`
- `tenant.certificate_onboarding_artifact_created`
- `tenant.certificate_onboarding_artifact_deleted`
- `tenant.integration_health_checked`
- `configuration.change_approved`
- `configuration.version_effective`

## Cabo Verde Compliance Notes

Configuration is compliance-sensitive in Cabo Verde because tenant fiscal regime, tax rates, fiscal series, LED, NIF, repository code and e-Fatura certificate/readiness directly influence fiscal document validity.

Known from current sources:

- the product requires company-level configuration for base currency, country, fiscal regime, series, taxes and modules;
- the SSD requires fiscal settings, series, documents, accounts, warehouses and taxes per tenant;
- e-Fatura v11.0 requires explicit repository, LED, document type, numbering and secure certificate/middleware boundaries;
- the XSD package includes ISO country/currency tables that should constrain localization where relevant.

Verification status: product and technical implementation evidence is strong; legal/fiscal rule freshness still needs current Cabo Verde authority for production compliance.

## MVP Acceptance Criteria

For the first sellable release, the module is acceptable only if:

- tenant creation records legal identity, NIF, country, base currency and fiscal regime;
- tenant starts as `setup_pending` and cannot issue fiscal documents until required setup gates pass;
- setup checklist exposes blockers for fiscal, series, e-Fatura and operational readiness;
- all configuration is tenant-scoped and protected by RLS/permissions;
- fiscal profile, tax settings and document series are auditable and effective-dated or versioned where needed;
- changing series, tax regime, e-Fatura settings or certificate references requires explicit permission and audit;
- settings used by issued documents cannot be destructively changed without controlled replacement/versioning;
- e-Fatura configuration stores readiness metadata and certificate references without plaintext secrets;
- certificate/private-key material is excluded from ordinary application tables and tenant UI;
- middleware/integration URL handling follows the layered topology decision: environment default endpoint, tenant readiness/configuration and platform-admin-only endpoint override;
- module activation/feature flags cannot bypass subscription entitlements or role permissions;
- dashboard/reporting/AI access only reads configuration through permission-aware views.

## Non-MVP Until Confirmed

- Fully automated production middleware reconfiguration without platform approval.
- Self-service certificate rotation or PFX escrow without approved secret-manager, deletion and audit policy.
- Multi-country legal rule engine beyond Cabo Verde-ready abstractions.
- Complex approval workflows for every low-risk setting.
- Tenant-custom formula language for taxes or accounting.
- Automatic retroactive recalculation of historical fiscal/accounting data after setting changes.

## Open Questions

- Which setup steps are mandatory for the first login-to-first-invoice path?
- Should document series be configured manually by tenant admins, generated by onboarding, or both?
- Who can approve sensitive fiscal/e-Fatura configuration changes: tenant owner, accountant, platform support or all of them?
- Should tenant onboarding sync to middleware be automatic after platform approval or handled through a supervised runbook?
- Should NOVA-ERP retain uploaded PFX after middleware keystore import, or delete it after successful onboarding?
- Which settings need effective dates versus immutable snapshots?
- Should SaaS plan changes automatically enable modules or only expose activation options?

## Next Ingestion Targets

- Actual SQL migrations/RLS/storage policies behind `raw/assets/DATABASE_ER_DIAGRAM.md`.
- Current official Cabo Verde legal sources for fiscal regime, IVA rates, REMPE and document-series requirements.
- Current official Cabo Verde/DNRE operational evidence for tenant middleware onboarding, certificate handling and production emitter groups.
- Current official/legal evidence for fiscal artifact retention periods.
