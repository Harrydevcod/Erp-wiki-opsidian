---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [erp-module, ia, assistant, automation, analytics]
sources: ["[[2026-05-26 - Captura Raw e Docs]]", "[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Dashboards e Relatorios ERP]]", "[[Fiscalidade Cabo Verde]]"]
related: ["[[NOVA-ERP]]", "[[Dashboards e Relatorios ERP]]", "[[Permissoes e Auditoria ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Tesouraria ERP]]", "[[Inventario ERP]]", "[[Contabilidade ERP]]", "[[2026-05-29 - Schema Decision - AI Assistant Governance and Action Boundary]]"]
confidence: medium
---

# IA Assistente ERP

## Purpose

IA Assistente ERP is the governed AI layer for [[NOVA-ERP]]: a permission-aware assistant that helps users query ERP data, understand indicators, detect exceptions, summarize operations and receive explainable suggestions.

## Role In NOVA-ERP

The assistant should amplify operational judgment without becoming an uncontrolled actor. It must answer from authorized tenant data, separate facts from inference, cite the underlying records where possible and avoid mutating critical data automatically.

The product sources position AI as a later intelligence layer, not as foundation infrastructure. That means NOVA-ERP should first build reliable modules, reporting views, permissions, audit logs and fiscal correctness. AI then sits on top of that governed substrate.

Source: [[2026-05-26 - Captura Raw e Docs]], [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Backlog Estruturado NOVA-ERP]], [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog evidence: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- Implementation prompt: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- Official project direction: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]
- Security boundary: [[Permissoes e Auditoria ERP]]
- Reporting substrate: [[Dashboards e Relatorios ERP]]
- Fiscal caution: [[Fiscalidade Cabo Verde]], [[Faturacao Eletronica]]

## Design Gates Before Implementation

- Permission gate: define what AI can read and propose per role, tenant and module before connecting it to ERP data.
- Data gate: expose curated reporting/query views instead of unrestricted table access.
- Audit gate: define prompt, response, tool-call, data-access and action-confirmation logs before enabling action tools.
- Safety gate: separate read-only assistance from commands that mutate fiscal, accounting, treasury, inventory or payroll state.
- Fiscal/legal gate: define how AI cites sources and marks uncertainty for Cabo Verde fiscal, payroll and compliance answers.
- Model/provider gate: define data-retention, residency, encryption and vendor-risk posture before sending sensitive business data to any AI provider.

## Core Workflows

- Answer natural-language questions about authorized ERP data.
- Summarize sales, treasury, inventory, accounting, e-Fatura and dashboard indicators.
- Explain anomalies such as overdue receivables, rejected DFE submissions, low stock, margin drift, unusual discounts or audit events.
- Generate suggested next actions, such as review, follow-up, correction, reconciliation or investigation.
- Draft operational text, such as customer follow-up notes, payment reminders or internal summaries, when permitted.
- Support module-specific guided analysis for sales, treasury, inventory, fiscality, accounting and reporting.
- Require explicit human confirmation before any command that changes durable ERP state.

## Required Foundations

- Tenant-scoped authorization and tested RLS.
- Action-level permissions from [[Permissoes e Auditoria ERP]].
- Stable reporting views from [[Dashboards e Relatorios ERP]].
- Audit logs with correlation IDs across prompts, retrieved data, tool calls and confirmed actions.
- Clear distinction between facts, calculations, inferences, recommendations and unsupported claims.
- Redaction or exclusion rules for payroll, certificates, raw DFE payloads, secrets, financial credentials and other sensitive evidence.
- Current fiscal source pages for compliance-sensitive answers.

## Candidate Domain Model

- `ai_conversations`: tenant, user, module context, title, status and retention policy.
- `ai_messages`: user/assistant/system messages with timestamps, sensitivity classification and token/provider metadata where useful.
- `ai_context_references`: links from responses to records, reports, documents, source pages or immutable evidence used.
- `ai_retrieval_events`: query/view/tool used, filters applied, permission result and returned record summary.
- `ai_suggestions`: suggested actions with target module, target record, rationale, confidence and required permission.
- `ai_action_confirmations`: human confirmation/rejection for a suggested command.
- `ai_tool_calls`: tool/command execution request, input hash, output summary, actor, tenant and result.
- `ai_safety_events`: blocked prompt, blocked data access, blocked action, policy reason and reviewer status.
- `ai_feedback`: user rating, correction, escalation or usefulness signal.

This model is provisional. It should not be implemented before the provider/security posture and reporting/query substrate are defined. The committed target shape and invariants are in [[2026-05-29 - Schema Decision - AI Assistant Governance and Action Boundary]]: AI runs with the acting user's own permissions, reads only `ai_safe` datasets/tool endpoints (never raw tables or `service_role`), suggests but never directly mutates (suggest→confirm→execute through normal module commands), records full prompt/retrieval/tool/suggestion provenance with citations, redacts sensitive evidence before model egress, and is gated by a per-tenant kill switch and plan entitlement.

## Candidate State Machine

### Suggestion State

- `drafted`: suggestion generated but not shown as actionable.
- `presented`: user can review the suggestion.
- `confirmed`: authorized user approved execution.
- `executed`: command completed through a normal module service.
- `rejected`: user rejected the suggestion.
- `blocked`: policy, permission or safety rule prevented action.
- `expired`: suggestion is no longer valid because source data changed.

### AI Action Risk Level

- `read_only`: answer, summarize or explain authorized data.
- `draft_only`: create non-final draft text or draft document for later human review.
- `low_risk_command`: non-fiscal/non-accounting convenience action with explicit confirmation.
- `high_risk_command`: fiscal, accounting, treasury, inventory, HR/payroll, security or tenant-admin action requiring strong permission, reason and audit.
- `forbidden`: unsupported action, cross-tenant request, secret extraction or legal/fiscal claim without evidence.

## Integration Points

- [[Dashboards e Relatorios ERP]] provides governed metrics, KPI definitions and reporting views.
- [[Permissoes e Auditoria ERP]] controls what the assistant can see, retrieve, suggest and execute.
- [[Fiscalidade Cabo Verde]] constrains fiscal/compliance answers and requires uncertainty to be visible.
- [[Faturacao Eletronica]] can expose document status, rejection reasons, contingency state and next operational steps.
- [[Tesouraria ERP]] can expose overdue balances, reconciliation gaps and cash-flow exceptions.
- [[Inventario ERP]] can expose low stock, reservations, movement anomalies and count variances.
- [[Contabilidade ERP]] can expose posting status, period locks, journals and SAF-T/accounting readiness when permissions allow.

## Data Access Boundary

The assistant should not query arbitrary operational tables directly in production. Preferred access path:

1. user asks a question within tenant context;
2. permission layer resolves allowed modules/actions/records;
3. assistant queries curated views, reports or explicit tool endpoints;
4. response cites records, reports or source pages used;
5. any proposed mutation becomes a normal module command requiring confirmation and audit.

This keeps AI inside the same trust boundary as the ERP rather than creating a privileged side channel.

## Action Boundary

AI may draft or suggest, but durable state changes must be executed by normal module services. The assistant should never bypass:

- fiscal issue and e-Fatura authorization rules;
- accounting posting, reversal or period-close controls;
- treasury allocation/reversal controls;
- inventory adjustment/count approval controls;
- HR/payroll permission and privacy controls;
- tenant administration, role assignment or secret/certificate management controls.

For MVP, AI action tools should remain out of scope unless the underlying command already has permission checks, audit logging, confirmation UX and rollback/reversal behavior.

## Audit, Security And Tenancy

- AI access must respect tenant membership, RLS and action-level permissions.
- Prompt and output logs may contain sensitive commercial, financial, payroll or fiscal data and need explicit retention/security policy.
- Responses over sensitive areas should cite the data basis or clearly mark uncertainty.
- Raw e-Fatura XML/ZIP, certificate material, payroll data and security logs require stricter access than ordinary status summaries.
- Tool calls must preserve actor, tenant, permission result, target record, input/output hashes and execution result.
- Cross-tenant summarization is forbidden unless an explicit platform-support or aggregate analytics mode is designed separately.

## Critical Domain Events

- `ai.conversation_started`
- `ai.prompt_received`
- `ai.context_retrieved`
- `ai.response_generated`
- `ai.suggestion_created`
- `ai.suggestion_confirmed`
- `ai.suggestion_rejected`
- `ai.tool_call_requested`
- `ai.tool_call_blocked`
- `ai.tool_call_executed`
- `ai.safety_policy_triggered`
- `ai.feedback_recorded`

## Cabo Verde Compliance Notes

AI must not present fiscal, payroll or legal guidance as legal authority unless grounded in current verified sources. For compliance-sensitive answers, the assistant should cite source pages, distinguish law/manual evidence from inference and recommend human review when the evidence is incomplete or stale.

High-risk areas:

- fiscal document issue, correction, cancellation and e-Fatura rejection handling;
- IVA, REMPE, public-sector/public-works invoicing and reverse-charge answers;
- SAF-T CV readiness and export interpretation;
- payroll deductions and statutory reports after payroll is ingested;
- accounting period close, reversals and official reports.

## MVP Acceptance Criteria

For the first sellable release, the AI assistant is acceptable only if it is either not shipped or shipped as a constrained read-only layer with:

- tenant-scoped access;
- permission-aware retrieval;
- curated data sources instead of unrestricted SQL/table access;
- visible source references for factual answers;
- no automatic fiscal/accounting/treasury/inventory/payroll mutation;
- prompt/output retention policy;
- audit logs for sensitive prompts, retrieval and suggestions;
- clear uncertainty markers for fiscal/legal/compliance answers;
- kill switch or feature flag per tenant/plan.

## Non-MVP Until Confirmed

- Autonomous execution of fiscal, accounting, treasury, inventory, HR/payroll or security actions.
- Direct database write tools.
- Cross-tenant benchmarking or aggregate insights.
- Fine-tuned models on tenant data.
- AI access to raw certificates, secrets, payroll details or raw e-Fatura payloads without a dedicated security design.
- Legal/fiscal advice mode.

## Open Questions

- Which AI use case should be first: natural-language reporting, anomaly explanation or guided operations?
- Should the first version be strictly read-only?
- Which reporting views must exist before AI is useful?
- What prompt/output retention policy should apply by default?
- Which AI provider/security posture is acceptable for sensitive Cabo Verde ERP data?
- Should AI logs be visible to tenant admins, platform admins or both?
- Which fiscal answers should be blocked unless current legal sources are ingested?

## Next Ingestion Targets

- `raw/assets/SSD/PRD.MD`
- `raw/assets/SSD/SSD.md`
- `raw/assets/SSD/PROMPT.MD`
- `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`
- Provider/security documentation before selecting an AI runtime.
