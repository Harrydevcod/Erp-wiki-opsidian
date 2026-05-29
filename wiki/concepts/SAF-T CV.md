---
type: concept
status: active
created: 2026-05-26
updated: 2026-05-28
tags: [saft, cabo-verde, fiscalidade, reporting, export]
sources: ["[[2026-05-26 - PRD NOVA-ERP]]", "[[2026-05-26 - SSD NOVA-ERP]]", "[[2026-05-26 - Backlog Estruturado NOVA-ERP]]", "[[2026-05-26 - Prompt Implementacao NOVA-ERP]]", "[[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]", "[[Fiscalidade Cabo Verde]]", "[[Contabilidade ERP]]", "[[Inventario ERP]]", "docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf", "docs/docsfiscal/SV_Documentacao_Fiscalidade_ERP_Cegid_Primavera.pdf"]
related: ["[[Fiscalidade Cabo Verde]]", "[[NOVA-ERP]]", "[[Contabilidade ERP]]", "[[Inventario ERP]]", "[[Faturacao Eletronica]]", "[[Compras e Vendas ERP]]", "[[Supabase Deployment]]", "[[Permissoes e Auditoria ERP]]", "[[IA Assistente ERP]]"]
confidence: medium
---

# SAF-T CV

## Purpose

SAF-T CV is the Cabo Verde fiscal audit/export domain for generating structured audit files from NOVA-ERP data, especially fiscal documents, accounting movements and inventory records.

For [[NOVA-ERP]], SAF-T must not be treated as a late XML formatter. It is a data-readiness constraint across fiscal documents, accounting, inventory, entities, tax profiles, periods, audit logs and export jobs.

## Role In NOVA-ERP

SAF-T CV belongs to the fiscal core. Product sources require SAF-T readiness in the MVP/foundation path, while also making clear that full legal completion can wait if the underlying domain shape, job structure, validation states and export history are correct.

The critical interpretation: build the ERP so valid SAF-T becomes a consequence of consistent source data. Do not build SAF-T as a detached report that tries to repair bad fiscal, accounting or stock data at export time.

Source: [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[NOVA-ERP Product Authority Synthesis]]

## Source Basis

- Product intent: [[2026-05-26 - PRD NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]
- Backlog scope: [[2026-05-26 - Backlog Estruturado NOVA-ERP]]
- Foundation release: [[2026-05-26 - Prompt Implementacao NOVA-ERP]]
- Operating posture: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]]
- Fiscal boundary: [[Fiscalidade Cabo Verde]], [[Faturacao Eletronica]]
- Accounting/inventory dependencies: [[Contabilidade ERP]], [[Inventario ERP]]
- ERP workflow reference: `docs/docsfiscal/Fiscalidade_ERP_Cegid_Primavera.pdf`, `docs/docsfiscal/SV_Documentacao_Fiscalidade_ERP_Cegid_Primavera.pdf`

## Design Gates Before Implementation

- Official schema gate: obtain and ingest the current official SAF-T CV schema/XSD/specification before production export claims.
- Scope gate: decide first-release scope across SAF-T Faturacao, SAF-T Contabilidade, SAF-T Inventario, SAF-T Completo and any "Outros" categories.
- Source-data gate: define which source tables/records become export authority for each file type.
- Accounting gate: do not finalize accounting SAF-T until chart, periods, journal entries, postings and reversals are implementation-grade.
- Inventory gate: do not finalize inventory SAF-T until stock movements, warehouses, items, counts and valuation posture are coherent.
- Fiscal gate: invoice/fiscal-document exports must derive from immutable fiscal snapshots and official numbering, not editable commercial drafts.
- Validation gate: local validation against configured XSD/schema must produce blocking errors, warnings and export history.
- Performance gate: export generation must run asynchronously and handle large tenant datasets without blocking the UI.
- Audit gate: every export, validation, reprocess and download must be tenant-scoped and logged.

## SAF-T Export Types

Current product sources reference the following export territory:

- SAF-T Faturacao;
- SAF-T Contabilidade;
- SAF-T Inventario;
- SAF-T Completo;
- SAF-T Outros.

The official instructions mention three obligatory types: Faturacao, Contabilidade and Inventario. The SSD additionally names Completo and Outros. This page should preserve both until current official SAF-T CV source material resolves exact production categories.

Source: [[2026-05-26 - Instrucoes Oficiais NOVA-ERP]], [[2026-05-26 - SSD NOVA-ERP]]

## Core Workflows

- Select tenant, fiscal period/exercise and export type.
- Run pre-export consistency checks.
- Generate export asynchronously.
- Validate generated XML against configured SAF-T CV XSD/schema.
- Surface blocking errors and warnings.
- Store export file metadata, hash, schema version and source-data snapshot references.
- Allow controlled reprocessing when source data or schema changes.
- Download/export only by authorized users.
- Preserve export history for audit.
- Feed AI/error-assistant workflows only through permission-aware summaries.

## Required Source Data

### Fiscal/Faturacao Data

- tenant legal identity, NIF, country, fiscal regime and base currency;
- document types, fiscal series, document numbers, dates and source references;
- immutable fiscal document snapshots;
- customers/suppliers/entities and NIFs;
- tax rates, exemptions, IVA/REMPE/non-taxed reasons and totals;
- credit/debit/correction references;
- e-Fatura IUD/LED/repository/authorization metadata where relevant;
- void/inutilization/cancellation evidence once legally modeled.

### Accounting Data

- chart of accounts;
- fiscal/accounting periods and exercise;
- journals;
- posted journal entries and lines;
- debit/credit totals;
- reversal/adjustment links;
- tax posting profiles;
- source links to fiscal, treasury, inventory, payroll and asset events.

### Inventory Data

- item master;
- warehouses/locations;
- stock movements;
- stock counts and variances;
- lots/serials where enabled;
- valuation/cost evidence where required;
- source links to purchases, sales, returns, transfers and adjustments.

## Candidate Domain Model

- `saft_schema_versions`: configured SAF-T CV schema/XSD version, source reference, active status and validation rules.
- `saft_export_profiles`: tenant export configuration by type, fiscal regime, period and enabled sections.
- `saft_export_jobs`: asynchronous export job, tenant, type, period/exercise, status, requested_by, timestamps and progress.
- `saft_export_sources`: immutable manifest of source record ids/ranges used by an export.
- `saft_export_files`: generated XML/storage path, hash, size, encoding, schema version and download metadata.
- `saft_validation_results`: validation status, blocking errors, warnings, schema version and validator output.
- `saft_inconsistency_reports`: normalized data-quality findings before or after generation.
- `saft_export_events`: append-only lifecycle/audit events for generation, validation, download, failure and reprocess.
- `saft_export_permissions`: optional explicit policy mapping for who can generate/download/reprocess.

This model is provisional until official SAF-T CV schema/source ingestion.

## Candidate State Machine

### Export Job State

- `draft`: export request being prepared.
- `queued`: job accepted for background generation.
- `generating`: XML generation in progress.
- `generated`: file created but not yet validated.
- `validating`: schema/business validation in progress.
- `valid`: generated export passed validation.
- `invalid`: blocking errors prevent safe use.
- `warning`: export generated with non-blocking warnings.
- `failed`: generation or validation failed technically.
- `superseded`: newer export replaced this file for the same scope.
- `cancelled`: job cancelled before completion.

### Data Readiness State

- `not_ready`: required source data missing.
- `ready_with_warnings`: export possible, but inconsistencies exist.
- `ready`: export prerequisites satisfied.
- `locked`: period/source scope locked for export or fiscal close.

## Consistency Checks

SAF-T should run checks before generation, not only after XML validation:

- tenant has required fiscal identity and period setup;
- fiscal period/exercise exists and is not internally inconsistent;
- document numbering has no unexplained gaps/reuse;
- issued fiscal documents have immutable snapshots;
- corrective documents reference original documents where required;
- tax totals reconcile with document lines;
- accounting entries balance debit/credit;
- posted entries belong to open/closed/locked periods according to policy;
- inventory movements reconcile with stock counts/valuation posture;
- source records are tenant-scoped and not cross-linked to another tenant;
- required entity/item/tax fields are present.

## Integration Boundaries

- [[Faturacao Eletronica]] provides fiscal document snapshots, numbering, tax breakdowns, correction links and e-Fatura identifiers.
- [[Contabilidade ERP]] provides chart, periods, journals, posted entries, reversals and accounting balances.
- [[Inventario ERP]] provides item, warehouse, stock movement, count and valuation evidence.
- [[Compras e Vendas ERP]] provides commercial source lineage for documents and stock/treasury/accounting events.
- [[Supabase Deployment]] provides asynchronous job, storage, secrets and RLS deployment posture.
- [[Permissoes e Auditoria ERP]] governs export/download/reprocess permissions and audit events.
- [[IA Assistente ERP]] may explain inconsistencies but must not alter fiscal/accounting data without human confirmation.

## Audit, Security And Tenancy

- Every SAF-T job/file/result must be tenant-scoped.
- Export generation and download require explicit permissions.
- Files can contain sensitive fiscal, accounting, inventory, customer and supplier information; storage must be private.
- Export history should preserve who requested, generated, validated, downloaded or reprocessed a file.
- Reprocessing should create a new export record, not overwrite historical evidence.
- Source-data manifests and hashes should support later audit/reproducibility.
- Service-role generation jobs must preserve initiating actor and tenant context.

## Performance And Runtime

SAF-T generation is a heavy report/export workload. It should run asynchronously, with:

- queued jobs;
- progress/status visibility;
- retry/failure state;
- pagination or streaming extraction where needed;
- generated file storage rather than browser-only generation;
- tenant and period indexes on source tables;
- guardrails for massive datasets.

Source: [[2026-05-26 - SSD NOVA-ERP]], [[2026-05-26 - Prompt Implementacao NOVA-ERP]], [[Supabase Deployment]]

## Cabo Verde Compliance Notes

Known from product sources:

- NOVA-ERP must support SAF-T CV as part of Cabo Verde fiscal compliance.
- Official instructions name SAF-T Faturacao, Contabilidade and Inventario.
- SSD requires XML UTF-8, current configured XSD, reproducible exports, period/exercise generation, offline validation, logs, reprocessing and inconsistency audit.
- The implementation prompt requires SAF-T export jobs and export history in the foundation model, even if full legal completion is not finished.

Compliance uncertainty:

- The current official SAF-T CV schema/XSD version is not yet ingested.
- Exact mandatory sections, field names, validation rules and submission process remain unresolved.
- Cegid Primavera material is workflow reference only, not production legal authority.

## Critical Domain Events

- `saft.export_requested`
- `saft.export_queued`
- `saft.export_generated`
- `saft.export_validated`
- `saft.export_invalid`
- `saft.export_downloaded`
- `saft.export_reprocessed`
- `saft.inconsistency_detected`
- `saft.export_superseded`

The SSD already names `saft.generated` as a domain event. The above expands it into an auditable lifecycle vocabulary.

Source: [[2026-05-26 - SSD NOVA-ERP]]

## MVP Acceptance Criteria

For the first sellable release, SAF-T is acceptable only if its scope is explicit:

- foundation release includes real `saft_export_jobs` and export history shape, not a fake UI button;
- export jobs are tenant-scoped and permissioned;
- export generation is asynchronous;
- generated files are stored privately with hash/schema/version metadata;
- validation results can distinguish blocking errors from warnings;
- inconsistency reports identify source records that must be fixed;
- fiscal document, accounting and inventory source data preserve enough structured evidence for later official SAF-T completion;
- production "valid SAF-T" claim is blocked until current official SAF-T CV schema/XSD/source is ingested and implemented.

## Non-MVP Until Confirmed

- Production legal claim that generated files satisfy all current DNRE/SAF-T CV requirements.
- Automatic submission to an external authority portal unless official process is ingested.
- Complete SAF-T Contabilidade before accounting implementation is sufficiently mature.
- Complete SAF-T Inventario before inventory valuation and movement rules are stable.
- AI auto-fixing fiscal/accounting inconsistencies.
- Retroactive data repair without auditable correction events.

## Open Questions

- What is the current official SAF-T CV schema/XSD version?
- Which SAF-T types are mandatory in production: Faturacao, Contabilidade, Inventario, Completo, Outros?
- Which fields must be captured at transaction time to avoid impossible exports later?
- Should base SAF-T ship before full accounting, or only as "SAF-T-ready" job/data structure?
- Which validation errors are blocking versus warning?
- Where should generated XML files live: Supabase Storage, external object storage or database-backed artifact storage?
- What retention policy applies to generated SAF-T files and validation reports?

## Next Ingestion Targets

- Current official SAF-T CV schema/XSD/specification.
- Cegid Primavera fiscalidade materials for workflow reference only.
- Accounting legal/source material for Cabo Verde chart/reporting requirements.
- Inventory SAF-T field requirements and valuation implications.
