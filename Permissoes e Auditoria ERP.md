---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, security, permissions, audit, tenancy]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-28 - DATABASE ER Diagram Snapshot]]", "[[2026-05-28 - Current Database Snapshot Classification]]", "[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Contabilidade ERP]]"]
related: ["[[NOVA-ERP]]", "[[ERP SaaS Multi-Tenant]]", "[[Supabase]]", "[[Subscricoes SaaS ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Contabilidade ERP]]", "[[e-Fatura Cabo Verde]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]"]
confidence: high
---

# Permissoes e Auditoria ERP

## Purpose

Permissoes e Auditoria ERP is the security governance layer for NOVA-ERP: tenant membership, roles, permissions, RLS boundaries, audit logs, sensitive action control and traceability of fiscal, accounting and operational changes.

## Role In NOVA-ERP

This is a foundation module. In a multi-tenant ERP, permissions and auditability are not administrative polish; they are part of the product's safety model. Every module should assume tenant-scoped authorization, least privilege, durable audit evidence and defense against cross-tenant data leakage.

The recent fiscal/e-Fatura work raises the bar: issuing documents, changing series, viewing raw DFE payloads, submitting to middleware, handling certificates, posting accounting entries and reopening periods are not generic "admin" actions. They require distinct permissions, auditable events and database-level isolation.

Source: [[2026-05-26 - Captura Raw e Docs]], [[ERP SaaS Multi-Tenant]], [[Fiscalidade Cabo Verde]], [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Implementation prompt: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- Current database evidence: [[2026-05-28 - DATABASE ER Diagram Snapshot]]
- Target architecture classification: [[2026-05-28 - Current Database Snapshot Classification]]
- Fiscal/e-Fatura boundary: [[Fiscalidade Cabo Verde]], [[Faturacao Eletronica]], [[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]]
- Accounting boundary: [[Contabilidade ERP]]
- Related concept: [[ERP SaaS Multi-Tenant]]

## Design Gates Before Implementation

- Tenant gate: define `tenants`, tenant memberships, invitation lifecycle and company switching before module data tables are finalized.
- RLS gate: every tenant-owned table must have tested row-level isolation.
- Permission gate: define action-level permissions for fiscal, accounting, treasury, inventory, HR, assets, subscriptions and admin configuration.
- Audit gate: define immutable audit event shape before implementing sensitive workflows.
- Secret boundary gate: define where certificates, client secrets, keystores, transmitter keys and raw payloads live before e-Fatura production work.
- Entitlement gate: distinguish role/permission from SaaS plan entitlement.

## Core Workflows

- Create tenant/company and initial owner/admin.
- Invite users into a tenant.
- Assign tenant-scoped roles and permissions.
- Evaluate permissions within tenant context.
- Switch between companies without leaking data.
- Record audit logs for sensitive actions.
- Review and export audit trails where permitted.
- Restrict sensitive fiscal/accounting/e-Fatura actions by explicit permission.
- Support admin visibility into configuration and operational changes.
- Provide a foundation for AI access controls based on authorized data.

## Required Master Data

- `tenants`: company/account boundary for data ownership.
- `tenant_memberships`: user-to-tenant membership, status and invitation lifecycle.
- `roles`: tenant-scoped or system-defined role templates.
- `permissions`: action-level capability catalog.
- `role_permissions`: permission grants per role.
- `user_permission_overrides`: controlled exceptional grants/revocations.
- `audit_event_types`: typed sensitive actions.
- `audit_logs`: append-only/tamper-resistant event records.
- `security_policies`: RLS and service-role policy documentation where useful.
- `entitlement_links`: mapping between SaaS plan features and accessible modules/actions.

## Permission Boundaries

Minimum high-risk permission groups:

- tenant administration: manage company settings, invite users, assign roles;
- fiscal configuration: configure document types, series, tax regimes, e-Fatura readiness;
- fiscal issuing: create drafts, issue documents, create corrective documents, cancel where legally allowed;
- e-Fatura operations: generate payload, view technical status, reprocess, enter/resolve contingency;
- sensitive e-Fatura evidence: view raw XML, ZIP archives, raw DNRE/middleware responses and certificate metadata;
- certificate/secret administration: upload/rotate certificates, manage keystore references, client secrets and transmitter keys;
- accounting: configure chart/accounts/posting rules, post entries, reverse entries, close/reopen periods;
- treasury: record payments/receipts, reconcile banks, alter payment status;
- inventory: adjust stock, approve counts, change valuation-sensitive records;
- HR/payroll: view salaries, process payroll, alter deductions;
- audit: view/export audit logs and security events.

These should not collapse into a single `admin` flag.

## Audit Event Model

Every critical audit event should capture:

- `tenant_id`;
- actor user id and actor role/context;
- action;
- target type and target id;
- source module;
- timestamp;
- request/session context where available;
- before/after data or immutable payload hashes;
- reason/comment for exceptional actions;
- correlation id/job id for background work;
- result status and failure summary where relevant.

For high-risk fiscal and accounting events, audit records should link to immutable source evidence rather than duplicate sensitive payloads unnecessarily.

## Fiscal And e-Fatura Audit Requirements

[[2026-05-28 - Schema Decision - e-Fatura DFE Payload and Transmission]] implies separate access policies for:

- fiscal document snapshots;
- DFE payload XML;
- XSD validation results;
- transmission batches;
- transmission attempts;
- raw response bodies;
- contingency records;
- self-billing authorizations;
- certificate references.

Normal fiscal operators may need status and rejection summaries. Raw XML, ZIP archives, certificate metadata and middleware/DNRE response bodies require stricter access and audit logging.

Critical fiscal audit events:

- `fiscal_document.number_assigned`;
- `fiscal_document.issued`;
- `fiscal_document.corrective_document_created`;
- `dfe.payload_generated`;
- `dfe.validation_completed`;
- `dfe.transmission_attempted`;
- `dfe.authorized`;
- `dfe.rejected`;
- `dfe.contingency_entered`;
- `dfe.retry_scheduled`;
- `efatura.certificate_uploaded`;
- `efatura.certificate_rotated`;
- `efatura.middleware_config_changed`.

## Accounting Audit Requirements

[[Contabilidade ERP]] requires separate control for:

- posting entries;
- reversing entries;
- changing posting rules;
- changing tax posting profiles;
- closing periods;
- reopening periods;
- generating SAF-T/accounting exports.

Critical accounting audit events:

- `accounting.journal_entry_posted`;
- `accounting.journal_entry_reversed`;
- `accounting.posting_rule_changed`;
- `accounting.tax_profile_changed`;
- `accounting.period_closed`;
- `accounting.period_reopened`;
- `accounting.saft_export_generated`.

## RLS And Data Access Posture

Baseline posture:

- all tenant-owned operational tables carry `tenant_id`;
- tenant membership drives read/write visibility;
- service-role operations are isolated behind Edge Functions/server commands;
- UI permission checks improve UX but do not replace database policies;
- storage buckets for certificates, fiscal payloads, payment proofs, payroll and attachments must have explicit private policies;
- raw fiscal/accounting/security evidence is not exposed to ordinary operators by default.

The current ER snapshot contains `user_roles` and `user_permissions`, but [[2026-05-28 - Current Database Snapshot Classification]] says the target must adapt these into tenant-scoped RBAC and verify actual SQL/RLS/storage policies before reuse. The concrete target RBAC/audit/RLS shape is now specified provisionally in [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]] (`tenant_members` + `roles` + `role_permissions` replacing the snapshot's user-keyed RBAC; default-deny membership-keyed policies; append-only `audit_log`). The catalog contents, per-user overrides, graduated sensitive-evidence access tiers, audit event taxonomy and the provisional launch role→permission matrix are committed in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]].

## Integration Points

- Every ERP module uses authorization checks.
- [[Subscricoes SaaS ERP]] limits access by entitlement/plan, separate from role permission.
- [[Supabase]] provides Auth, PostgreSQL, RLS/policies, storage and Edge Functions.
- [[ERP SaaS Multi-Tenant]] defines isolation expectations.
- [[Faturacao Eletronica]] and [[e-Fatura Cabo Verde]] define fiscal/e-Fatura sensitive actions.
- [[Contabilidade ERP]] defines posting, reversal and period-close permissions.

## MVP Acceptance Criteria

For the first sellable release, the module is acceptable only if:

- every tenant-owned table has a tenant boundary and RLS plan;
- users cannot read or mutate another tenant's data;
- roles and permissions are evaluated in tenant context;
- issuing fiscal documents and configuring fiscal series are separate permissions;
- viewing raw e-Fatura payloads/responses is separate from viewing document status;
- certificate/secret management is restricted and audited;
- accounting posting/reversal/period close are separate permissions if accounting is in scope;
- critical actions write audit logs with actor, tenant, target, action and timestamp;
- audit logs are append-only in normal application paths;
- SaaS plan entitlements do not bypass security permissions.

## Non-MVP Until Confirmed

- Fine-grained field-level permissions for every module.
- Customer-facing audit export portal.
- Automated anomaly detection/AI audit summaries.
- Full SIEM integration.
- Self-service certificate rotation without supervised approval.
- Any AI action that mutates critical fiscal/accounting data without human confirmation.

## Cabo Verde Compliance Notes

Permissions and audit logs support fiscal accountability, but they are not a substitute for legal compliance. For fiscal documents, payroll, accounting and reporting, audit rules should be aligned with current Cabo Verde requirements.

Current high-risk areas:

- fiscal document issue/correction/cancellation;
- e-Fatura payload generation/submission/retry;
- certificate and credential handling;
- accounting posting/reversal/period close;
- SAF-T/export generation;
- payroll processing once ingested.

## Open Questions

- What is the first launch role model: owner, admin, accountant, salesperson, warehouse, HR, viewer?
- Which actions require immutable audit logs in MVP?
- Should audit logs be user-visible, admin-only or exportable?
- Should raw e-Fatura XML/ZIP/response bodies be visible to tenant admins, accountant role only, or platform support only?
- How should service-role actions be attributed to initiating users and background jobs?
- Which RLS tests become mandatory release gates?

## Next Ingestion Targets

- Actual SQL migrations and RLS policies behind `raw/assets/DATABASE_ER_DIAGRAM.md`.
- `raw/assets/SSD/PROMPT.MD`.
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`.
- Supabase deployment/security notes.

