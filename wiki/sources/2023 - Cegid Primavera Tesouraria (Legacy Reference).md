---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, cegid-primavera, tesouraria, contas-correntes, bancos, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Tesouraria ERP]]", "[[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]]", "[[Compras e Vendas ERP]]", "[[Processamento de Salarios ERP]]", "[[Contabilidade ERP]]"]
confidence: medium
---

# Cegid Primavera — Tesouraria (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — Tesouraria" training deck (FPG001, 2023-VC1-PT / cover 2020-vc2, 123 pp.), `docs/docsfiscal/FPG001 - Using - Tesouraria (2023-VC1-PT).pdf`. **Legacy ERP workflow reference**, not legal authority and not target architecture. Portugal-oriented (electronic bank export, cheque/letra workflows are PT practice). Its value is the open-item / settlement / cash-and-bank workflow, which strongly corroborates [[2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement]].

## Legacy workflow (as documented)

Two halves: **Gestão de Contas Correntes** (open items / receivables-payables) and **Gestão de Bancos** (cash & bank).

### Contas Correntes (CC)

- **Purpose:** control *pendentes* (open items) for Clientes / Fornecedores / Outros Terceiros. Values originate from **Vendas, Compras, Recursos Humanos** and direct CC entry.
- **CC document types:** *Adiantamento* (advance; IVA mandatory), *Pendente* (open item, e.g. FSE invoices), *Liquidação* (settlement; value always > 0; nature receive/pay irrelevant — e.g. Recebimento, Nota de Pagamento), *Compensação*, *Liq. c/ Novo Pendente* (settle and create a new open item in another account — e.g. letra), *Valores em excesso* (overpayment, **auto-generated** by the ERP), *Transferência de Conta/Estado*.
- Pendentes are mostly generated from sales/purchase invoices (FA→CC Clientes, VFA→CC Fornecedores), with optional **per-line vs per-document** pendente generation.
- **Gestão de Limite de Crédito:** on save, **Bloquear / Ignorar / Avisar** when a party exceeds credit limit — by max value, by age of balance, or a combination.
- **Operações sobre Pendentes** (the settlement core):
  - *Liquidação Total* — pendente fully settled, disappears.
  - *Liquidação Parcial* — pendente stays with remaining balance.
  - *Liquidação com encontro de valores* — offset opposite-nature docs of equal value (FA receivable vs NC payable → REG regularização, nets to 0).
  - *Liquidação com valores em excesso* — overpayment generates an excess document (VEC).
  - *Liquidação com novo pendente* — remaining debt carried into a new pendente (e.g. letra).
  - *Transferência de Estado* — change a pendente's state (e.g. `AGP` aguarda aprovação → `APR` aprovada); does **not** alter the Extrato, only the Consulta de Pendentes (approval workflow).
  - *Transferência de Conta* — move a pendente between accounts (e.g. Clientes → **Clientes Duvidosos**).
  - *Distribuição Automática* — apply a received amount to pendentes top-down, remainder to next.
  - *Entidades associadas* — integrated settlement across related parties (a client who is also a supplier → contra-settlement).
- **Estorno / Anulação:** *Anulação* marks the settlement doc `Anulado` and the liquidated docs return to pendente; *Estorno* creates a contrary-nature document.
- **Planos de Pagamento:** reorganize a portfolio of pendentes (same entity, same currency) into installments; auto-calculated, editable; can attach pre-dated cheques.
- **Tratamento de Retenção (withholding):** types *Estado* (services purchase/sale, e.g. category B rendimentos empresariais), *Garantia* (retention to self), *Outras*. On saving a CC-integrating document the system computes retentions and shows a "Resumo das Retenções" grouped by entity/type/percentage; the user can edit value/percentage/incidência/entidade or disable. Retention can settle into the **State entity** CC. *Mapa de Retenções* reports by type.
- **Mapas de Análise CC:** Mapa de Pendentes, Consulta de Liquidações, Extrato de Conta, **Balancete de CC** (saldo acumulado/transitado/período/final), Saldos/Avisos de Vencimento, Análise de CC, Histórico, Documentos emitidos. **Rastreabilidade** drills from a pendente to its origin document and the documents generated from it.

### Gestão de Bancos (Caixa e Bancos)

- Movements originate from **Vendas, Compras, CC, Contabilidade**.
- **Account types:** Contas Caixa, Caixa POS, Depósitos à Ordem, Depósitos a Prazo, Cartões de Crédito, Contas Correntes Caucionadas.
- **Movimentos Bancários** are the base record; **Itens de Tesouraria** (rubricas) group movement values for budget comparison — one or many per movement.
- Bank document types: Entrada/Abertura/Fecho de Caixa, Aplicações Financeiras + Liquidação/Capitalização, Transferência de Cheques, Pagamento Cartão de Crédito, transferência entre contas internas.
- **Caixa session lifecycle:** *Abertura* creates a *diário* assigned to all movements until close → *Movimentos* → *Talões de depósito* (cash+cheques → DO account) → *Fecho* (blocked if balance ≠ 0 when so configured). Reopen via "Anular fecho de caixa". *Estado das Caixas* + diário history records opening/closing balance, datetime and **operator**.
- **Emissão de Cheques:** cheque series (letra, nº inicial/final, validade); manual or sequential; on anulação the cheque number is released (`Por Emitir`).
- **Operações Bancárias Periódicas:** scheduled recurring movements (leasings, rendas, débitos automáticos), automatic or queued to "Movimentos a Ocorrer"; pre-dated cheques.
- **Exportação para formato eletrónico:** bank-integration file (magnético) with NIB destino, histórico/reexportação. **PT-format specific.**
- **Reconciliação Bancária:** *Manual* (limit date, enter bank final balance, "pick" movements, optional Movimentos de Diferença adjustments); *Automática* (import digital statement, match ERP vs bank, unmapped lines can be launched directly into tesouraria).
- **Mapas:** Extrato (multi-account, alerts), Painel de Bordo (consolidated position), Consulta/Acumulados por Item de Tesouraria (vs orçamento), Saldos Médios, Análise de Receitas e Despesas, Mapa de Controlo Bancário.

## Translation to NOVA-ERP

**Adopt / strongly validates the ADR:**
- The **obligation / movement / allocation** core is exactly Cegid's *pendente* / *movimento bancário* / *operação de liquidação* split. The ADR's `obligations` + `treasury_movements` + `allocations` is the right generalization.
- **Derived payment status:** Cegid pendentes disappear or remain by settlement, never a stored `paid` flag — corroborates `obligations.status` as a projection from allocations.
- **Reversal-by-compensation:** Anulação (return to pendente) and Estorno (contrary-nature doc) corroborate the ADR's append-only `reversed_by` model over deletes.
- **Allocation operation taxonomy** is a ready-made enum for the `allocations`/settlement layer: total, partial, **encontro de valores** (offset), **valores em excesso** (overpayment → the ADR's `on_account`), **liq. c/ novo pendente** (carry-forward, e.g. letra). The overpayment and contra-settlement cases directly validate the ADR's `on_account` and many-to-many design.
- **Bank reconciliation** (manual + automatic, with launch-from-statement) matches the ADR's `bank_statements`/`reconciliations` and answers its "manual-first MVP" question.

**New inputs to fold into the ADR:**
- **Itens de Tesouraria (rubricas):** a treasury category/rubric dimension on movements enabling budget-vs-actual analysis. Add an optional `treasury_item_id` (rubric) to `treasury_movements` and a rubric catalog — not currently in the ADR.
- **Caixa session lifecycle:** open/close *diário*, operator attribution, balance-zero close gate, reopen. NOVA-ERP cash accounts need a `cash_session` concept (open→movements→close, operator, opening/closing balance) layered over `treasury_accounts` of `kind=cash`.
- **State transfer / approval workflow:** `AGP→APR` payable-approval and **Clientes Duvidosos** (doubtful-debtor) transfer are obligation **sub-states / account transfers** — informs `obligations.status` side states (the ADR has `written_off`; add an `approval`/`doubtful` dimension or a status transfer log).
- **Credit-limit management** (block/ignore/warn; by value/age) is a commercial-document guard sourced from treasury balances — belongs at the document-save boundary with [[Compras e Vendas ERP]].
- **Withholding (retention) treatment** integrated at document save links treasury to fiscal withholding and to the **State entity** current account — connects to [[Processamento de Salarios ERP]] IRPS/INPS and to a withholding map. Model as a `withholding`/`retention` line + an obligation to the State entity.
- **Payment plans (installments)** reorganize pendentes into scheduled obligations — a later-scope feature.
- **Periodic bank operations** (recurring rendas/leasings/débitos) — a scheduling layer over `treasury_movements`.

**Adapt:**
- RH-origin pendentes (payroll net pay, INPS, IRPS) confirm the [[Processamento de Salarios ERP]] → treasury payment-batch boundary.

**Do not copy:**
- PT electronic bank export formats and PT cheque/letra-centric workflows as authority — verify Cabo Verde payment instruments, bank file formats and the relevance of letras before scoping.
- PT withholding categories/rates — CV withholding follows CV law ([[2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente]], current IRPS regime).

## Open questions surfaced

- Should *Itens de Tesouraria* (rubrics) be a generic analytical dimension reusing [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]], or a treasury-local catalog?
- Does NOVA-ERP need a full **cash-session** (caixa) model for POS-style use in MVP, or only bank/DO accounts first?
- How are withholdings to the State modeled — a treasury obligation to a State entity, an accounting-only tax map, or both?
- Are letras / pre-dated cheques / payment plans in CV scope, or deferred?

## Verification needs

- Cabo Verde bank integration file formats, payment instruments (letras relevance), and withholding categories/rates must come from CV banks and CV law, not this PT deck.
