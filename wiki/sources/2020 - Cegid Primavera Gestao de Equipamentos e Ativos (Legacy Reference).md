---
type: source
status: active
created: 2026-05-30
updated: 2026-05-30
tags: [source, cegid-primavera, ativos, depreciacao, imobilizado, legacy-reference, workflow]
sources: []
related: ["[[Cegid Primavera]]", "[[Gestao de Ativos ERP]]", "[[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]]", "[[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]]", "[[Contabilidade ERP]]", "[[Projetos ERP]]"]
confidence: medium
---

# Cegid Primavera — Gestão de Equipamentos e Ativos (Legacy Workflow Reference)

## What this is

The Cegid Primavera "Using — Gestão de Equipamentos e Ativos" training deck (FPG006, 2020-VC1-PT, 89 pp.), `docs/docsfiscal/FPG006 - Using - Gestão de Equipamentos e Ativos (2020-VC1-PT).pdf`. **Legacy ERP workflow reference**, not legal authority and not target architecture. Portugal-oriented (its Mapas Fiscais target the PT Autoridade Tributária). Value: the full fixed-asset lifecycle — criteria, depreciation, impairment, revaluation, disposal — which strongly corroborates [[2026-05-29 - Schema Decision - Fixed Assets and Depreciation]] and answers several of its open questions.

## Legacy workflow (as documented)

- **Two sub-domains:** *Ativos* (patrimonial/financial lifecycle: aquisição, depreciação, reavaliação, manutenção, alienação/abate/sinistro) and *Equipamentos* (physical/organic location cadastre, user assignment, dependencies). Lifecycle phases: Início de Vida → Operações Diárias → Fim de Ano → Fim de Vida.
- **Critérios de Depreciação — multi-level inheritance:** criteria resolve across **Planos → Classes → Classificações Fiscais → Ficha**.
  - **Planos de Depreciação:** a **Plano Contabilístico** (accounting, NIC/IAS-adapted) **and** a **Plano Fiscal** (each country's tax scenario) run **in parallel**, any currency, both can integrate to accounting, valid for all assets. (Dual book/tax depreciation.)
  - **Classes:** optional grouping of fiscal classifications (used for IAS class-wide revaluation).
  - **Classificações Fiscais:** structured **Diploma → Tabela → Divisão → Grupo → Classificação Fiscal**, per-classification + per-exercise criteria, free structure adaptable to fiscal change.
  - Variables: reduced-value, periodicidade, método, valor residual, taxa de processamento, variação, nº de turnos, norma de exceção fiscal, tratamento individual.
  - **Cascade changes:** periodicity/method/rate changes apply in cascade; "Aplicar a…" scope = período atual / atual+subsequentes / atual+subs.+exercícios subs. Locked when ficha is in certain states.
- **Ficha do Bem:** Código/Descrição, "Ativo Fixo" flag, Classificação Fiscal, Política de amortização, Tipo de Investimento, Conta do plano de contas. Asset kinds: Máquinas, Terrenos, Prédios, Edificações, Veículos, Outros.
- **Aquisição:** valued at acquisition/production **cost including all costs to make it operational** (seguros, transporte, impostos de compra não dedutíveis). Document carries Plano, Ficha, Base de Incidência, IVA + dedutível %. Every asset operation is a **document** with `Alteração` (patrimonial-change type) + `Exercício` + `Numerador`.
- **Depreciação Regular:**
  - Methods: **Linha Reta** (straight-line, constant) and **Saldos Decrescentes** (declining balance) with coefficients **1.5** (pvu<5y) / **2** (=5–6y) / **2.5** (>6y). Rates from the Classificações Fiscais table. *(Matches [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]] exactly.)*
  - **Periodicidade:** Anual / **Duodecimal** (12ths, prorated first/last) / **Diária** (acquisition day relevant) — with worked proration examples.
  - **Taxa de Processamento:** Máxima (from fiscal tables) / Mínima (= máx/2) / Variável (manual) / Zero. **Taxa Perdida** = difference between minimum and used rate; rate use is split **Aceite Fiscal / Não Aceite Fiscal**.
  - **Elemento de Reduzido Valor:** low-value assets fully written off in one exercise.
- **Depreciação Extraordinária:** extra depreciation outside the normal schedule; separate processing type; separate accounting accounts; fields Depreciação/Rendimento/Excedente.
- **Transferências:** proportionally move values from one asset to another (fix a mis-created asset that already has ledger entries; capitalize an asset-in-progress into a definitive asset). Destination assets must already exist; by value or %.
- **Decomposição:** split a complex asset into smaller fichas (to later dispose); **creates new fichas** and may terminate the original — buttons divide "/" and duplicate "+".
- **Conservação:** maintenance/conservation costs **not** subject to depreciation, recorded in conservation documents (total-cost tracking).
- **Imparidade:** *Perda de Imparidade* (reduce book value to **recoverable amount** = max of net realizable value and value-in-use); *Reversão* (later gain, **capped** at the would-have-been value).
- **Revalorização** (Reavaliações Livres/Extraordinárias, at justo valor): **Valor de Mercado** (market value net of accumulated depreciation — land/buildings) and **Custo de Reposição** (replacement cost, gross adjusted proportionally); produces a revaluation excedente.
- **Análises/Extratos/Balancetes:** Extratos da Ficha/Documentos; Balancete Contabilístico; **Balancete por Centros de Custo / Funções / Projetos**; Análises Fiscais; Depreciações (Taxas, Conferência, Variação); Património.
- **Mapas Fiscais [PT] — REJECT as authority:** amortizações/reavaliações maps for the PT Tax Authority. CV fiscal maps follow CV law.
- **Fim de Vida:** **Alienação** (sale; gain/loss = net proceeds vs net book value), **Abate** (write-off/scrap), **Sinistro** (casualty; value = indemnity, 0 if none). All **correct excess amortization** already taken in periods beyond the disposal date.
- **Encerramento do Exercício:** Fecho / Anulação do Fecho — done after the accounting close; an asset period lock.
- **Repartições do Bem:** imputation to **Centros de Custo** and **Funções** — **Fixa** (systematic fixed %) or **Variável** (daily rigorous afetações, only main cost center needed).
- **Tratamento de Seguros:** insurance policies linked to assets (capital seguro, valor segurado, prémios, prazos, vencimentos, alertas).
- **Cópia de Ativos:** create new fichas from an existing one, inheriting characteristics, with an optional ascendente (parent).

## Translation to NOVA-ERP

**Adopt / strongly validates the ADR:**
- **Asset register separate from inventory** — Cegid's dedicated Ativos module corroborates the ADR's core separation.
- **Every asset event is a document** (`Alteração` patrimonial-change type) → confirms the ADR's append-only, versioned `asset_*_events` and immutable depreciation runs; master-field edits never post.
- **Methods + coefficients (linha reta / saldos decrescentes ×1.5/×2/×2.5)** match the ADR's `asset_depreciation_policies` and Portaria 42/2015.
- **Capitalization at full operational cost** (incl. ancillary, non-deductible IVA) matches the ADR's acquisition/capitalization model.
- **Disposal types alienação/abate/sinistro with gain/loss** match `asset_disposals.kind`.

**Answers ADR open questions:**
- *"Track tax and accounting depreciation as separate schedules?"* → **Yes.** Cegid runs a **Plano Contabilístico and a Plano Fiscal in parallel**. NOVA-ERP should make `asset_depreciation_policies`/`schedules`/`runs` **plan-scoped** (`plan_kind = accounting|fiscal`, extensible to IAS plans), so one asset has parallel book and tax schedules; only the chosen plan integrates to a given accounting/tax map.
- *"Should depreciation run monthly/yearly/configurable?"* → **Configurable periodicity:** Anual / Duodecimal / Diária, with proration. Add a `periodicity` to the policy.
- *"Should project/cost-center allocation be mandatory?"* → **Optional, available:** via **Repartições** (Fixa/Variável) to Centros de Custo / Funções. Maps to [[2026-05-29 - Schema Decision - Project and Analytical Dimensions]] — tag asset depreciation lines with dimension values; not mandatory.

**New inputs to fold into the ADR:**
- **Depreciation plans as a first-class scope** (`asset_depreciation_plans`: accounting / fiscal / IAS), parent of policies and schedules. Biggest structural addition.
- **Criteria inheritance hierarchy** (plan → class → fiscal classification → asset) with cascade scope — a configuration-layering concept for defaults.
- **`taxa máxima / mínima (= máx/2) / perdida` and `aceite fiscal` vs `não aceite fiscal`** — track fiscally-accepted vs lost depreciation per line for the tax plan (minimum quota = half, already in the ADR from Portaria art. 14º).
- **Extraordinary depreciation, impairment (loss + reversal with cap), revaluation (market value + replacement cost)** — concrete `asset_revaluations.kind` values and a separate extraordinary-depreciation event with its own accounts.
- **Decomposição / Cópia de Ativos** — asset restructuring operations (`asset_components` already exists; add split/copy events).
- **Conservação** — maintenance costs not capitalized (the ADR's `asset_maintenance_events`, confirmed non-depreciable).
- **Excess-amortization correction on disposal** — disposal must reverse depreciation taken beyond the disposal date (duodecimal/anual) — a posting rule, not just a status change.
- **Asset exercise close (Fecho do Exercício)** — period lock aligned with accounting period locks.
- **Insurance policies** linked to assets — optional `asset_insurance_policies`.

**Adapt / Reject:**
- *Equipamentos* physical-cadastre half (locations, user assignment, dependencies) is largely an asset-tracking concern; adopt only `location_id`/custodian already in the ADR.
- **Reject** PT Mapas Fiscais as authority; CV asset fiscal maps follow CV law and [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]].

## Open questions surfaced

- How many depreciation plans does MVP need — just `fiscal` (Portaria 42/2015), or `accounting` + `fiscal` from day one?
- Are impairment and free/extraordinary revaluation (IAS) in MVP scope, or deferred after statutory straight-line depreciation?
- Is the criteria-inheritance hierarchy (class/classification config) worth building, or is per-asset policy enough for the first release?

## Verification needs

- PT Mapas Fiscais are not CV authority; CV asset fiscal maps and the **per-class rate annex** must come from current Cabo Verde law (the Portaria 42/2015 rate annex is still uncaptured per the ADR).
