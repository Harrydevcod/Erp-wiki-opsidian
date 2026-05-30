---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, cegid-primavera, compras, vendas, documentos, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Compras e Vendas ERP]]", "[[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]]", "[[Inventario ERP]]", "[[Tesouraria ERP]]", "[[Faturacao Eletronica]]"]
confidence: medium
---

# Cegid Primavera — O Processo de Gestão de Compras e Vendas (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — O Processo de Gestão de Compras e Vendas" training deck (2022-v2.0-GB / LPG015, 73 pp.), `docs/docsfiscal/Using - O Processo de Gestão de Compras e Vendas (2022-v2.0-GB) LPG015.pdf`. **Legacy ERP workflow reference**, not legal authority and not target architecture. It is a **Portugal-oriented** product: its entire fiscal-obligations half is PT law (SAF-T PT, AT communication, Working Documents / Portaria 302/2016) and must be **rejected as authority** for Cabo Verde. The value is the commercial-circuit workflow primitives, which strongly corroborate [[2026-05-28 - Schema Decision - Commercial and Fiscal Document Core]].

## Legacy workflow (as documented)

- **Three axes:** *Entidades* (to whom I buy/sell), *Artigos* (what), *Documentos* (how I register operations). Entities span **Clientes / Fornecedores / Outros Terceiros** in one master.
- **Entidades:** regular parties get a *Ficha* (Código, Nome Comercial vs **Nome Fiscal**, Moradas, Dados Fiscais = Espaço Fiscal + Número Fiscal, Dados Comerciais = Condição/Modo de Pagamento, Moeda). **Occasional/indiferenciados** use a "cliente/fornecedor tipo" code (`VD`/`FVD`) with address + NIF typed at document time. NIF **cannot be changed** once certified documents were emitted; NIF on a document is validated against the entity ficha; mapas/documents print the **fiscal** name, not the commercial one.
- **Artigos:** auxiliary tables (Taxas de IVA, Moedas, Famílias/Subfamílias, Marcas/Modelos, **Tipo de Artigo**); types distinguish system vs user, flex the accounting link, and restrict which documents an article is usable in.
- **Circuito Documental** (compras and vendas, symmetric): Orçamento/Proposta → Pedido Cotação → Cotação → **Encomenda** → **Guia** → **Fatura**, threaded across three effect tracks: **Stock**, **Transporte**, **Financeiro**.
- **Editor** (compras/vendas): cabeçalho + grelha de linhas + totalizadores + barra de operações; select Documento + Série + Entidade, insert lines, gravar.
- **Gestão de Reservas de stock:** *cativar stock atual* and **Back-to-Back orders** — link a client order to a supplier order so stock is reserved automatically on receipt.
- **Reprodução de conteúdos entre documentos** — five distinct mechanisms with a shared capability matrix:
  - **Duplicação** — copy a whole document into a new identical one (1→1).
  - **Conversão** — full header + all lines to the next level, in bulk, same module, N→1, with origin reference.
  - **Transformação** — partial lines/quantities to another document, same module, with **line closing**.
  - **Cópia de Linhas** — copy lines **across modules** (Vendas/Compras/Internos/Inventário).
  - All three latter mechanisms **share line-quantity traceability**: quantidades transformadas / convertidas / copiadas, with *controlo das quantidades satisfeitas* per origin line.
- **Anulação de Documentos:** marks a document `Anulado` (data + motivo) and posts the **inverse** of the original movement (CBL/CC edit-inverse; TES/STK movement removed). Restrictions: not in a **closed period**, **not transformed**, user has permission, not **manually settled** in Contas Correntes, not itself an estorno nor already estornado, **not exported to Assets**, not already e-transmitted. (In PT SAF-T the anulado document is still exported, marked anulado.)
- **Estorno / Crédito:** since documents cannot be deleted, correction = creating a document of **contrary nature**; original + estornado get **locked for edit**. A **Nota de Crédito** must identify the origin (Tipo/Série/Número Doc Original + Motivo) in the *Transação* tab.
- **Reimpressão:** reprint any document / second copies / receipts.
- **Obrigações Fiscais [PT] — REJECT as authority:** SAF-T (PT) generation, **AT** communication of invoices and transport documents via Web Service, **Working Documents** (Portaria 302/2016: orçamentos/pró-formas now in SAF-T, communicated monthly).
- **Séries emissíveis vs não emissíveis:** *emissível* = printed, delivered to third parties, **signed for software certification**, collected for SAF-T; *não emissível* = internal only and allowed only for Pedido Cotação, Cotação, Encomendas, Stock/Trans.
- **Mapas de Análise:** documentos emitidos, resumo/análise de encomendas pendentes, explorador e resumo de compras/vendas.

## Translation to NOVA-ERP

**Adopt / strongly validates the ADR:**
- **Unified entities.** Clientes + Fornecedores + Outros Terceiros in one master corroborates the ADR's `entities` with a `kind` role flag. **New input:** add a **commercial-name vs fiscal-name** split and a **NIF-immutability-after-certified-issuance** rule to `entities`; model occasional/indiferenciados either as a sentinel "generic party" type or as null-entity documents that carry name+NIF inline (Cegid's `VD`/`FVD`).
- **Commercial vs fiscal split = emissível vs não emissível.** Cegid's "não emissível only for Pedido Cotação/Cotação/Encomendas/Stock" vs "emissível = signed + in fiscal export" is exactly NOVA-ERP's `commercial_documents` (internal) vs `fiscal_documents` (certified) split and the `document_series.scope` field. Strong validation.
- **`document_links` generalizes the five reproduction mechanisms.** Duplicação/Conversão/Transformação/Cópia de Linhas are four UI tools over one underlying graph of origin→destination edges with quantity traceability. NOVA-ERP's single `document_links` graph + `relation` enum is the right generalization. The matrix axes (em bloco, 1→1, N→1, N→N, múltiplas entidades, parcial, entre módulos) are the capability checklist this graph must satisfy.
- **No deletion; two correction paths.** Anulação (inverse movement under guard conditions) and Estorno/Crédito (contrary-nature document, both locked, mandatory origin reference) corroborate the ADR's "no hard delete after number assignment" and the corrective `document_links` relation, and feed [[2026-05-28 - Schema Decision - e-Fatura Event Payloads]] (FDC anulation).
- **Back-to-Back / reservation** feeds the reservation-vs-on-hand split in [[2026-05-28 - Schema Decision - Inventory Movements and Valuation]].

**Answers / advances ADR open questions:**
- *"How are partial deliveries and partial invoicing quantities tracked?"* → Cegid tracks **satisfied quantities at the line level** across transform/convert/copy ("controlo das quantidades satisfeitas", "fecho de linhas"). NOVA-ERP should track fulfilled quantity per source line (on lines or on link edges), not only at header level.
- *"Returns as negative documents or distinct types?"* → Cegid uses a **distinct contrary-nature document with a mandatory origin reference**, supporting the ADR's leaning toward a distinct corrective/return document + reference over negative lines.

**Adapt:**
- The **anulação guard list** (closed period / transformed / settled / exported-to-assets / e-transmitted) is a ready-made set of **precondition checks** for NOVA-ERP's void/anulation command — but reconciled with [[Faturacao Eletronica]]: once a fiscal number is assigned, anulation is an **e-Fatura event (FDC)**, not a row edit.
- Software-certification series-signing is **PT-specific**; CV certification follows the DNRE e-Fatura regime.

**Do not copy:**
- All PT fiscal obligations: SAF-T (PT), AT Web Service communication, Portaria 302/2016 Working Documents. NOVA-ERP communicates to **DNRE via e-Fatura** (see [[Faturacao Eletronica]], [[e-Fatura Cabo Verde]]) and exports **SAF-T CV** ([[SAF-T CV]]).
- File/manual-upload-to-portal communication paths.

## Open questions surfaced

- How should NOVA-ERP model **occasional/indiferenciados** parties — sentinel generic entity, or inline name+NIF on a document with null `entity_id`?
- Should fulfilled/satisfied quantity live on `*_document_lines`, on `document_links` edges, or a dedicated fulfilment table? (ADR open question, now sharpened.)
- Which of the five reproduction behaviors are MVP (likely: transformação + conversão) vs later (cópia de linhas across modules)?

## Verification needs

- Every "Obrigações Fiscais" rule here is **Portuguese** and must not be treated as Cabo Verde authority; CV invoice communication, certification and transport-document rules come from DNRE / [[2026-05-28 - Manual de Faturas em Cabo Verde]] and the e-Fatura technical manual.
