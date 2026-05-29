---
type: schema
status: active
created: 2026-05-29
updated: 2026-05-29
decision_status: provisional
tags: [schema, architecture, ai, assistant, governance, security, nova-erp]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]", "[[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]", "[[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]]", "[[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]]"]
related: ["[[NOVA-ERP]]", "[[IA Assistente ERP]]", "[[Dashboards e Relatorios ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]"]
confidence: medium
---

# Schema Decision - AI Assistant Governance and Action Boundary

## Decision

The NOVA-ERP AI assistant is a **governed consumer inside the existing trust boundary**, never a privileged side channel. It executes every read with the **acting user's own permissions** (via the same `has_permission`/`current_user_tenant_ids` predicates), reads only `ai_safe` reporting datasets and explicit tool endpoints from [[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]] — never raw operational tables, never `service_role` bypass. It may answer, summarize, explain and **suggest**, but it never mutates durable ERP state directly: any proposed change becomes a normal module command requiring explicit human confirmation, the command's own permission check, and an `audit_log` entry. Every prompt, retrieval, tool call, suggestion, confirmation and block is recorded with a correlation id and grounded `ai_context_references`, so answers are auditable and traceable to records/source pages. Sensitive material (payroll, raw e-Fatura payloads, certificates, secrets, security logs) is redacted/excluded before model egress per the permissions-ADR evidence tiers, and the assistant is gated by a per-tenant/plan kill switch. For MVP it is either not shipped or shipped strictly read-only; action tools are schema-ready but off until the underlying command has permission, audit, confirmation UX and reversal behavior.

## Scope

- Module: [[IA Assistente ERP]].
- Tables/objects: `ai_conversations`, `ai_messages`, `ai_context_references`, `ai_retrieval_events`, `ai_suggestions`, `ai_action_confirmations`, `ai_tool_calls`, `ai_safety_events`, `ai_feedback`, plus `ai_tenant_settings` (kill switch, provider posture, retention).
- Workflows affected: NL questions over authorized data, indicator/anomaly explanation, suggested next actions, drafting, and the suggest→confirm→execute action path.
- Tenancy boundary: every row carries `tenant_id` under [[2026-05-28 - Schema Decision - Tenant Foundation and RLS]]; cross-tenant summarization is forbidden unless a separately designed platform-support/aggregate mode exists.

## Source Basis

- Module source: [[IA Assistente ERP]] defines the permission/data/audit/safety/fiscal/provider gates, the candidate model, the suggestion and risk-level state machines, and the read-first action boundary.
- Product source: PRD/SSD/Instruções position AI as a later intelligence layer atop reliable modules, reporting, permissions, audit and fiscal correctness — not foundation infrastructure.
- Reporting source: [[2026-05-29 - Schema Decision - Reporting Semantic Layer and Dashboards]] supplies the `ai_safe` dataset contract and KPI definitions/caveats the assistant consumes.
- Security source: [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]] supplies permission keys, evidence tiers, audit taxonomy and service-role attribution reused here.
- Entitlement source: [[2026-05-29 - Schema Decision - SaaS Subscriptions Billing and Entitlements]] gates AI as a plan capability.
- Compliance source: [[Fiscalidade Cabo Verde]] — fiscal/legal answers must cite current verified sources or be blocked.

## Context

This is the last module ADR and deliberately the thinnest in new mechanism: the reporting `ai_safe` contract, the permission evidence tiers and the module command/audit boundaries already exist, so the AI layer mostly *composes* them and adds provenance + an action gateway. The decisive risk is that an AI assistant becomes an over-privileged data/action path. The decision neutralizes that by binding AI to the acting user's permissions and forcing all mutations back through the same module services a human would use.

## Data Model

- Entity/table: `ai_tenant_settings`
  - Key fields: `id`, `tenant_id`, `enabled` (kill switch), `mode` (`read_only|read_plus_draft|with_actions`), `provider`, `data_retention_days`, `redaction_policy` (jsonb), `allowed_dataset_keys` (jsonb), `updated_by`.
  - Purpose: per-tenant/plan enablement, provider posture and retention; default `enabled=false`.

- Entity/table: `ai_conversations`
  - Key fields: `id`, `tenant_id`, `user_id`, `module_context`, `title`, `status`, `retention_policy`, `created_at`.

- Entity/table: `ai_messages`
  - Key fields: `id`, `tenant_id`, `conversation_id`, `role` (`user|assistant|system`), `content`, `sensitivity_class`, `provider_meta` (jsonb), `created_at`.
  - Constraints: content stored under retention policy; sensitive content may be hashed/redacted rather than retained verbatim.

- Entity/table: `ai_context_references`
  - Key fields: `id`, `tenant_id`, `message_id`, `ref_kind` (`dataset|kpi|record|report|source_page|evidence`), `ref_id`, `permission_checked`.
  - Purpose: grounds each answer in the exact records/datasets used; enables citation and audit.

- Entity/table: `ai_retrieval_events`
  - Key fields: `id`, `tenant_id`, `conversation_id`, `dataset_or_tool`, `filters` (jsonb), `acting_user_id`, `permission_result` (`allowed|denied`), `record_summary`, `created_at`.
  - Constraints: retrieval runs as the acting user; a `denied` result is logged and never silently widened.

- Entity/table: `ai_suggestions`
  - Key fields: `id`, `tenant_id`, `conversation_id`, `target_module`, `target_record_ref`, `rationale`, `confidence`, `risk_level` (`read_only|draft_only|low_risk_command|high_risk_command|forbidden`), `required_permission`, `status`.

- Entity/table: `ai_action_confirmations`
  - Key fields: `id`, `tenant_id`, `suggestion_id`, `decision` (`confirmed|rejected`), `decided_by`, `reason`, `decided_at`.
  - Constraints: a human with the command's `required_permission` must confirm before execution.

- Entity/table: `ai_tool_calls`
  - Key fields: `id`, `tenant_id`, `suggestion_id` (nullable), `tool_key`, `input_hash`, `output_summary`, `acting_user_id`, `permission_result`, `result_status`, `correlation_id`, `created_at`.
  - Constraints: executes through a normal module service, not a direct DB write; input/output hashed.

- Entity/table: `ai_safety_events`
  - Key fields: `id`, `tenant_id`, `conversation_id`, `event_kind` (`blocked_prompt|blocked_data|blocked_action|policy_violation`), `policy_reason`, `reviewer_status`, `created_at`.

- Entity/table: `ai_feedback`
  - Key fields: `id`, `tenant_id`, `message_id`, `rating`, `correction`, `escalated`, `created_at`.

## State And Events

- State: `ai_suggestions.status`: `drafted -> presented -> confirmed -> executed`; alternatives `rejected`, `blocked`, `expired` (source data changed).
- State: AI action risk level (gate, not lifecycle): `read_only | draft_only | low_risk_command | high_risk_command | forbidden`. `high_risk_command` (fiscal/accounting/treasury/inventory/payroll/security/tenant-admin) needs strong permission + reason + audit; `forbidden` covers cross-tenant, secret extraction and unsupported legal/fiscal claims.
- Events (to `audit_log`, taxonomy in the permissions ADR): `ai.conversation_started`, `ai.prompt_received`, `ai.context_retrieved`, `ai.response_generated`, `ai.suggestion_created`, `ai.suggestion_confirmed`, `ai.suggestion_rejected`, `ai.tool_call_requested`, `ai.tool_call_blocked`, `ai.tool_call_executed`, `ai.safety_policy_triggered`, `ai.feedback_recorded`.
- Transition rule: a suggestion can reach `executed` only through `ai_action_confirmations` by an authorized human and an `ai_tool_calls` row that passed the same permission check as a manual command.

## Access, Permission And Action Boundary

- Read path: question in tenant context → permission layer resolves allowed modules/records for the acting user → assistant queries only `ai_safe` datasets/tools (filtered to `allowed_dataset_keys`) → response cites `ai_context_references` → any mutation becomes a confirmed module command.
- AI inherits the acting user's permissions; it has no role of its own and no `service_role` path to data.
- Sensitive exclusion: payroll detail, raw e-Fatura XML/ZIP/responses, certificates/secrets and security logs are excluded/redacted before egress (status-tier summaries only), per the permissions-ADR evidence tiers.
- New permission keys (feed the catalog in [[2026-05-29 - Schema Decision - Permission Catalog and Audit Taxonomy]]): `ai.use`, `ai.suggest`, `ai.action_confirm`, `ai.config`, `ai.logs_view`.
- Entitlement: AI availability and mode are plan-gated via `saas_get_tenant_access`.

## Provider, Privacy And Grounding

- Provider posture (`ai_tenant_settings.provider`, retention, residency) is explicit before sensitive business data leaves the tenant boundary; no fine-tuning on tenant data without a dedicated design.
- Prompt/output logs may hold commercial/financial/payroll/fiscal data → retention policy and access via `ai.logs_view`; verbatim sensitive content may be hashed/redacted.
- Grounding: answers separate fact, calculation, inference and recommendation; compliance-sensitive answers cite current source pages or are blocked with an uncertainty marker — the assistant never presents fiscal/legal guidance as authority without verified current evidence.

## Alternatives Considered

- Alternative: give AI a service-role/read-all data path for convenience.
  Why not: creates a privileged side channel that bypasses RLS/permissions and can leak cross-tenant or sensitive data.
- Alternative: let AI execute mutations directly when confident.
  Why not: removes human accountability for fiscal/accounting/treasury actions and the module's own controls; suggest→confirm→execute preserves them.
- Alternative: let AI query operational tables with NL→SQL.
  Why not: unstable, unsafe and ungoverned; the `ai_safe` dataset contract gives stable, permission-filtered access.
- Alternative: store only final answers, not retrieval/tool provenance.
  Why not: defeats auditability and grounding; provenance is required for trust in an ERP.

## Consequences

- Positive: AI sits inside the same trust boundary as the ERP; no new privilege escalation surface.
- Positive: every answer is grounded and every action is human-confirmed and audited.
- Positive: thin layer — composes existing reporting/permission/audit/entitlement mechanisms.
- Tradeoff: read-only-first limits early automation value; action tools wait on per-command readiness.
- Tradeoff: provenance/redaction logging adds storage and policy overhead.
- Migration impact: new build; depends on reporting `ai_safe` datasets and the permission catalog existing first.

## Validation Plan

- Test: AI retrieval as user X returns only what user X may read; a denied retrieval is logged, not widened.
- Test: AI cannot read another tenant's data through any conversation or tool.
- Test: payroll detail, raw e-Fatura XML and certificate material are never returned to the model; only status-tier summaries.
- Test: a suggested fiscal/accounting action cannot execute without an `ai_action_confirmations` row by a user holding the command's permission.
- Test: every prompt, retrieval, suggestion, tool call and block writes an `audit_log` row with correlation id.
- Test: a fiscal/legal question without current verified source evidence is answered with an explicit uncertainty/block, not an authoritative claim.
- Test: disabling `ai_tenant_settings.enabled` (kill switch) blocks all AI activity for the tenant.
- Test: AI is unavailable when the tenant entitlement is absent, independent of user permission.

## Open Questions

- First use case: NL reporting, anomaly explanation, or guided operations?
- Strictly read-only at launch, or read + draft?
- Default prompt/output retention and which provider/residency posture is acceptable for Cabo Verde ERP data?
- Are AI logs visible to tenant admins, platform admins, or both?
- Which fiscal answer classes are blocked until current legal sources are ingested?
- Which `ai_safe` datasets are the minimum useful set for launch?

## Maintenance Notes

- Update when actual Supabase migrations/RLS and the provider/security posture are decided (see [[2026-05-29 - Supabase Implementation Artifact Gap]]).
- Depends on tenant foundation, permissions/audit, reporting semantic layer and subscriptions ADRs; new `ai.*` keys must be added to the permission catalog. This closes the module schema-decision sequence for NOVA-ERP.
