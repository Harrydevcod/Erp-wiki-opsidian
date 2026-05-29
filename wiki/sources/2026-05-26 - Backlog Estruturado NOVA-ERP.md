---
type: source
status: active
created: 2026-05-26
updated: 2026-05-26
source_path: raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD
source_type: structured-backlog
author:
published:
ingested: 2026-05-26
tags: [source, backlog, nova-erp, execution, epics]
related: ["[[NOVA-ERP]]", "[[NOVA-ERP Product Authority Synthesis]]", "[[NOVA-ERP Module Priority Map]]"]
confidence: high
---

# Backlog Estruturado NOVA-ERP

## Summary

The structured backlog decomposes NOVA-ERP into epics, features, user stories and acceptance criteria. It is the best source for execution sequencing and story-level scope.

Source: `raw/assets/SSD/Backlog Estruturado — NOVA-ERP.MD`

## Epics

1. Plataforma Base Multi-Tenant.
2. Entidades.
3. Produtos e Serviços.
4. Vendas.
5. Compras.
6. Inventário / Logística.
7. Tesouraria / Contas Correntes / Bancos.
8. Contabilidade.
9. Fiscalidade.
10. e-Fatura / Middleware / DNRE.
11. SAF-T CV.
12. RH.
13. Ativos.
14. Projetos.
15. Subscrições SaaS.
16. Dashboards e Relatórios.
17. IA / Assistente ERP.

## Suggested Prioritization

MVP phase 1:

- epics 1, 2, 3, 4, 5, 6, 7, 9, 10 and 11.

Phase 2:

- epics 8, 16 and 15.

Phase 3:

- epics 12, 13, 14 and 17.

## Execution-Level Signals

- Platform foundation includes tenant creation, onboarding, users, permissions and audit.
- Sales includes invoices, invoice-receipts, POS/tickets, credit/debit notes, document immutability and document circuit.
- Treasury includes pendings, full/partial liquidation, credit limits and bank reconciliation.
- e-Fatura includes certificate/credential configuration, DFE generation/sending, contingency and response handling.
- SAF-T includes accounting export, inventory export and structural validation.
- AI assistant stories explicitly require permission-aware answers and human confirmation before executing suggestions.

## Acceptance Criteria Pattern

The backlog repeatedly encodes:

- tenant context;
- auditability;
- clear document states;
- controlled cancellation/correction;
- permission validation;
- no data deletion when limits or subscription changes apply.

## Open Questions

- Should the backlog's MVP phase 1 be treated as the actual build order, or should accounting be partially advanced because fiscal/SAF-T depends on accounting data?
- Are epics 15 and 16 truly phase 2, or should essential dashboards and basic SaaS entitlements ship earlier?
- Which acceptance criteria need to become automated test requirements?

