---
type: log
status: active
created: 2026-05-26
updated: 2026-05-29
---

# LLM Wiki Log

Append-only chronological record. New entries go at the top.

## [2026-05-30] tooling | Storage buckets migration drafted (e-Fatura evidence finding 4)

- Drafted `nova-erp/supabase/migrations/20260530120000_storage_buckets.sql` closing finding 4 of the Edge/storage security review. Creates the three **private** buckets from the e-Fatura evidence ADR — `fiscal-evidence` (signed XML/ZIP/responses), `fiscal-renders` (PDF/DFA), `efatura-onboarding-temp` (cert uploads, 10 MB) — with size + MIME limits, idempotent (`on conflict do nothing`). The app/functions reference no storage today, so it is purely additive.
- **Access model:** no client policies on `storage.objects` → deny-by-omission; only service-role (Edge Functions) reads/writes; reads via short-lived server-generated signed URLs. Documents the `<bucket>/<tenant_id>/…` path convention. Tenant-scoped client-read policy deferred (customer-facing PDF/DFA access is still an open ADR question).
- **NOT committed, NOT run** (no `supabase`/`psql` CLI). The `FORCE RLS` + `TO authenticated` DB hardening was **deliberately deferred** — breakage risk for anon/role flows, needs testing not a blind migration.
- Files created (nova-erp): `supabase/migrations/20260530120000_storage_buckets.sql`
- Files updated (wiki): `wiki/syntheses/2026-05-30 - Edge Function and Storage Security Review.md`, `log.md`

## [2026-05-30] tooling | Remediation drafted for Edge Function cross-tenant authz (create-user/audit-log/numbering)

- Implemented the fix-order from the security review (code-level findings 1–3). Added a shared guard `nova-erp/supabase/functions/_shared/auth.ts`: `callerClient` (caller-JWT-scoped), `requireTenantPermission` (via `get_user_permissions`, passes on `admin.users` or `core.admin`), `requireTenantMember` (via `get_user_tenants`). The relevant seeded permission is `admin.users`.
- **create-user** → gated on `admin.users`, audit actor from JWT; **audit-log** → gated on membership, `user_id` forced from JWT (body ignored); **numbering** → gated on active membership. Added `_shared/auth.test.ts` (mock-client unit tests of the decision logic).
- **NOT committed, NOT run** — no `deno`/`supabase` CLI in the environment. Founder/CI must `deno test` + `deno check` + integration-serve before merge. Storage buckets (finding 4) + `FORCE RLS` hardening still open. These changes live in the nova-erp repo working tree (separate from the user's existing `web/` WIP).
- Files created (nova-erp repo): `supabase/functions/_shared/auth.ts`, `supabase/functions/_shared/auth.test.ts`
- Files updated (nova-erp repo): `supabase/functions/create-user/index.ts`, `audit-log/index.ts`, `numbering/index.ts`
- Files updated (wiki): `wiki/syntheses/2026-05-30 - Edge Function and Storage Security Review.md` (Remediation section), `log.md`

## [2026-05-30] lint | Edge Function + storage security review — cross-tenant authorization gap

- Completed the implementation-grade pass outstanding from the reconciliation: read all four Edge Functions (`create-user`, `audit-log`, `numbering`, `_shared/*`) and checked storage policies in migrations + `config.toml`. Read-only; no implementation files modified.
- **Headline finding (high/critical):** all three functions run on the **`SERVICE_ROLE_KEY` (bypassing RLS)** and **trust the request-body `tenant_id` with no caller identity/membership/permission check.** `verify_jwt = true` only proves the caller is *some* authenticated platform user, not a member of the target tenant. Combined with the RLS finding (gates tenant, not permission), **there is no enforced per-tenant authorization at any layer** for these privileged ops.
  - `create-user` — **CRITICAL**: any authenticated user can POST `{tenant_id: victim, role_code: 'admin'}` and mint an admin membership in any tenant (cross-tenant takeover). Also writes audit with no acting `user_id`.
  - `audit-log` — **HIGH**: inserts `audit_logs` straight from the body incl. acting `user_id` → audit attribution forgeable; DB append-only protects post-insert tampering only, not forged inserts.
  - `numbering` — **HIGH**: lets any user increment another tenant's fiscal series → gap injection in a gapless invoice sequence (DNRE compliance problem). CAS optimistic lock itself is race-safe.
  - **Storage** — **GAP**: no `storage.buckets`/`storage.objects` policies in any migration, though the e-Fatura secrets ADR requires private buckets for fiscal XML/certificates/payroll.
- Documented the correct service-role authorization pattern (derive caller from JWT → verify membership → verify `has_permission` → derive actor `user_id` from JWT, never body) and a fix order.
- Files created:
  - `wiki/syntheses/2026-05-30 - Edge Function and Storage Security Review.md`
- Files updated:
  - `wiki/contradictions/Contradiction - DB-Layer Authorization and RLS Permission Gating.md` (Edge layer does NOT compensate — hypothesis partially falsified)
  - `wiki/syntheses/2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations.md` (Edge/storage review done), `index.md`, `log.md`
- Open questions: do private storage buckets exist outside migrations (dashboard-configured)? is there an API gateway / extra auth in front of the functions? Founder decision: fix the three functions (recommended) and/or move authorization firmly to one enforced layer.

## [2026-05-30] maintain | ADR-vs-implementation reconciliation (Supabase migrations) — artifact gap closed

- The **nova-erp implementation repo** appeared in the workspace, closing the long-standing [[2026-05-29 - Supabase Implementation Artifact Gap]]. Read the **13 migrations** (`00001_core`…`00009_hr`, `00010_rls_policies`, `00011_seeds`, + `align_domain` and `fiscal_documents_base`) in the sandbox and reconciled them against the full target-schema ADR sequence. Migrations read read-only; no implementation files modified.
- **Verdict pattern:** tenant isolation **MATCHES** design — `tenant_id = get_active_tenant_id()` is membership-validated (`set_tenant_context` + `get_active_tenant_id` both re-check active membership), so it is *not* an isolation hole. The recurring **DIVERGENCE** is philosophical: the implementation prefers **stored accumulators maintained by triggers/procedures** over the ADRs' **derived-from-immutable-ledger** stance.
- **Three material contradictions opened (high confidence):** (1) inventory `stock_items` stored `qty_on_hand`/`avg_cost` + trigger vs the ADR's derived no-stored-quantity ledger (the explicitly-rejected alternative; biggest SAF-T/COGS risk); (2) `documents.status` stores `paid/partial_paid/overdue` written by `settle_document()` vs treasury ADR's derived-from-allocations; (3) RLS gates only *tenant* not *permission* — 41 `FOR ALL` policies give any active member full CRUD, no `user_permission_overrides`, no evidence tiers, no `FORCE RLS`/service-role hardening.
- **GAPS (designed, not built):** fixed assets (0 tables), generic analytical dimensions (only concrete `cost_centers`), reporting/AI layers, SaaS entitlement computation/snapshots, per-user permission overrides. **PARTIAL MATCH:** accounting (projection balances + periods ✓, no immutability trigger, concrete cost center), treasury (allocation substrate ✓, no `obligations` table), e-Fatura (transmission/events/settings/cert present, granularity differs), audit (append-only ✓).
- Files created:
  - `wiki/syntheses/2026-05-30 - ADR vs Implementation Reconciliation - Supabase Migrations.md` (the reconciliation matrix + per-area conform-vs-amend decisions)
  - `wiki/contradictions/Contradiction - Inventory Stored Stock vs Derived Movement Ledger.md`
  - `wiki/contradictions/Contradiction - Stored Payment Status vs Derived from Allocations.md`
  - `wiki/contradictions/Contradiction - DB-Layer Authorization and RLS Permission Gating.md`
- Files updated:
  - `wiki/syntheses/2026-05-29 - Supabase Implementation Artifact Gap.md` (status → resolved; resolution banner pointing to the reconciliation), `index.md` (syntheses + 3 contradictions + Maintenance Queue), `log.md`
- Open questions: are the stored-accumulator choices intentional MVP posture or drift (decides conform-vs-amend)? is DB-layer permission gating intended or is app/Edge the accepted boundary? **Next:** review the 4 Edge Functions (`audit-log`, `create-user`, `numbering`, `_shared`) + storage policies — the only implementation-grade pass still outstanding.

## [2026-05-30] ingest | Código Laboral payroll parameters + INPS base correction

- Closed the payroll non-fiscal gaps (provisionally, secondary sources). Web-researched the **Código Laboral** (Decreto-Legislativo 5/2007, overtime amended by **DL 1/2016, de 3 fev**) via the Vendus employer guide + INPS pages.
- **Captured:** normal time 8h/day·44h/week; **overtime** ≤2h/day·160h/yr (300h with consent), rate **disputed +35% (search) vs +50% (Vendus)** — flagged for primary verification; **night work 22h–06h = +25%**; **férias 22 dias úteis/yr**; salary deductions capped at 1/3. **Subsídio de Natal/13.º** formula still uncaptured (CV-specific — don't assume the PT model).
- **Correction:** the INPS "ceiling" assumption was wrong — the **base de incidência is a minimum floor tracking the minimum wage** (13.000$→14.000$ Jan-2023; rising with the 2025 17.000$ minimum), with no clearly-documented upper cap. Model base as `max(gross, floor)`.
- Also refreshed the payroll-sources page: IRPS section flipped to **resolved by primary law** (DL 6/2015 + CIRPS), superseding the IUR scale note.
- Files updated:
  - `wiki/sources/2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources.md` (Código Laboral section added; INPS base corrected; IRPS resolved; sources +DL6/2015, +CIRPS)
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md` (subsidies/overtime now parametrized), `index.md`, `log.md`
- Open questions: the +35%/+50% overtime dispute and the subsídio de Natal/13.º formula — resolve against the **primary Código Laboral / DL 1/2016**; confirm any INPS upper cap.

## [2026-05-30] ingest | Imposto de Selo — Tabela de verbas (from CIRPC B.O.)

- Extracted the **Imposto de Selo (IS) Anexo — Tabela de verbas** from the same `raw/assets/irpc/Lei_82_2015_Codigo_IRPC.pdf` (B.O. I Série nº 3, 8-01-2015, which carries the tail of the IS code + the CIRPC). Rates: operações de crédito 0,5%; juros/serviços financeiros 3,5%; garantias 0,5%; seguros 3,5%; letras/livranças/títulos 0,5%; operações societárias 0,5%; **actos notariais/registo/processuais 15%**; actos administrativos & escritos de contratos **1.000$00 fixo**.
- Partial capture: this PDF starts at art. 27º, so the IS incidence/exemption arts. 1–26 remain to ingest from the earlier B.O. issue.
- Also fixed a **stale citation** left by the dedup: removed the deleted `SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf` path from the [[Fiscalidade Cabo Verde]] sources and added the four new tax-code sources.
- Files created:
  - `wiki/sources/2015-01-08 - Imposto de Selo Cabo Verde Tabela de Verbas.md`
- Files updated:
  - `wiki/concepts/Fiscalidade Cabo Verde.md` (sources refreshed: +IRPS/IRPC/DL 6-2015/IS, −deleted SV deck), `index.md`, `log.md`
- Open questions: ingest the full Código do Imposto de Selo (incidence/exemptions/territoriality); per-verba computation base; OE-year rate changes.

## [2026-05-30] ingest | Código do IRPC (Lei 82/2015) primary law

- Ingested the corporate-tax code: **Lei nº 82/VIII/2015, de 7 de Janeiro** (Código do IRPC), B.O. I Série nº 3, 8-01-2015, from the DNRE library; preserved at `raw/assets/irpc/Lei_82_2015_Codigo_IRPC.pdf` (35 pp.). Completes the corporate axis alongside the IRPS axis.
- **Primary parameters:** Art. 84º taxa **25%** (contabilidade organizada) / **4%** sobre volume de negócios (REMPE simplificado, art. 95º) refazendo o **tributo especial unificado (TEU)** — ties to the SAF-T `TaxType` TEU. Art. 89º **tributação autónoma** 40% (despesas não documentadas), 10% (encargos de viaturas ligeiras/motos incl. depreciações), 10% (despesas de representação). Art. 59º **dedução de prejuízos fiscais**: até 7 períodos posteriores, dedução anual ≤ 50% do lucro tributável; opção pelo regime simplificado extingue o direito. **Imparidade de créditos** 25/50/75/100% por mora (6–24 meses). Art. 43º = enabling article da Portaria 42/2015. Same B.O. carries the Imposto de Selo annex (crédito 0,5%, serviços financeiros/seguros 3,5%, actos notariais/registo 15%).
- Files created:
  - `wiki/sources/2015-01-07 - Lei 82-2015 Codigo do IRPC.md`, `raw/assets/irpc/Lei_82_2015_Codigo_IRPC.pdf`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Accounting Ledger and Posting.md` (IRPC rate/loss-carryforward/impairment now primary-sourced for tax_maps)
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md` (10% vehicle tributação autónoma noted), `index.md`, `log.md`
- Open questions: exact ajudas-de-custo autonomous-tax rate (art. 89º d); OE-year changes to 25%/4% or the 7yr/50% loss params; REMPE special-law TEU mechanics.

## [2026-05-30] ingest | Código do IRPS (Lei 78/2014) primary law — annual scale confirmed

- Ingested the parent statute of the withholding regime: **Lei nº 78/VIII/2014 (Código do IRPS)**, B.O. I Série nº 81, 31-12-2014, from the DNRE library; preserved at `raw/assets/irps/Lei_78_2014_Codigo_IRPS.pdf` (16 pp.).
- **Primary confirmations:** categories **A** trabalho dependente/pensões, **B** empresariais/profissionais, **C** prediais, **D** capitais, **E** ganhos patrimoniais (Art. 2–3). **Art. 45º** annual *englobamento* scale **16,5% (≤960.000$) / 23,1% (≤1.800.000$) / 27,5% (>1.800.000$)**, **isenção do rendimento colectável até 220.000$** (mínimo de existência) — upgrades this scale from the secondary 2017 síntese to **primary**. Art. 46º Cat. A = liberatório/progressivo per art. 70º (the DL 6/2015 formula); **Art. 47º Cat. B = 20%** (REMPE simplificado in own diploma), **Art. 48º Cat. C = 20%** — primary confirmation that the 2017 síntese's 15%/10% were wrong. Art. 52º deduction structure (withholding refundable, deductions arts. 53–56 non-refundable, fraccionados creditable over 4 yr).
- Files created:
  - `wiki/sources/2014-12-31 - Lei 78-2014 Codigo do IRPS.md`, `raw/assets/irps/Lei_78_2014_Codigo_IRPS.pdf`
- Files updated:
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md` (annual scale now primary-confirmed; B/C 20% double-confirmed), `index.md`, `log.md`
- Open questions: ME as a distinct indexed value vs. the 220.000$ isenção; OE-year re-indexing of the 960.000$/1.800.000$ brackets; deduction amounts in arts. 53–56 (extract when annual-reconciliation feature is built). Sibling **Lei 82/2015 (CIRPC)** still available in the same DNRE folder for future ingest.

## [2026-05-30] ingest | Portaria 42/2015 depreciation rate annex captured

- Closed the long-standing "per-class depreciation rate annex" gap. Located the official **B.O. I Série nº 52, 28-08-2015** (the Rectificação republication of Portaria 42/2015, which carries the full Anexo the original BO nº 50 omitted), downloaded and pypdf-parsed it; preserved at `raw/assets/irpc/Portaria_42_2015_Tabelas_Taxas_Depreciacao.pdf` (+ the 20-article regime at `Portaria_42_2015_Depreciacoes_Amortizacoes.pdf`).
- Parsed **310 rated rows** into `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv` (`setor_or_tabela, grupo, subcategoria, designacao, taxa`): **Tabela I** taxas específicas by economic sector (Agricultura/Pesca, Electricidade/Água/Gás, Serviços, Hotelaria, Transportes/Comunicações, Construção Civil, Indústrias transformadoras G1–9) + **Tabela II** taxas genéricas by asset nature (Imóveis, Instalações, Máquinas, Material de transporte, Elementos diversos, Intangível). Distinct rates 2,5–50% (each = 100 ÷ useful-life years).
- Key generics now sourced: edifícios habitacionais 3% / industriais 5% / ligeiras 10%; instalações 6,66–10%; veículos ligeiros 14,28% (7 yr) / pesados 20% / motociclos 25%; aeronaves 20%; computadores·telemóveis·programas·intangível 33,33%; mobiliário 12,5%; ar condicionado 12,5%; televisores 25%.
- Files created:
  - `wiki/maps/Portaria 42-2015 Tabelas de Taxas de Depreciacao.md`
  - `raw/assets/irpc/Portaria_42_2015_Tabelas_Taxas_Depreciacao.pdf`, `raw/assets/irpc/Portaria_42_2015_Depreciacoes_Amortizacoes.pdf`, `raw/assets/irpc/Portaria_42_2015_Tabela_taxas.csv`
- Files updated:
  - `wiki/sources/2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes.md` (gap closed)
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md` (rate seed now sourced)
  - `index.md`, `log.md`
- Open questions: verify heuristically de-wrapped CSV designations against the PDF before legal display (rates/sectors reliable); whether later OE laws re-indexed the 20.000$/4.000.000$ thresholds.

## [2026-05-30] ingest | Decreto-Lei 6/2015 — IRPS withholding primary law (contradiction resolved)

- Closed the IRPS-withholding gap with **primary law**. Navigated the DNRE Liferay legislation library (folder 64542), resolved the real document download URL, and pypdf-parsed the official **Decreto-Lei nº 6/2015, de 23 de Janeiro** (B.O. I Série nº 7) — preserved at `raw/assets/irps/Decreto-Lei_6_2015_Retencao_na_Fonte.pdf` (4 pp.).
- **Operative result (Art. 5.º) — monthly Category A withholding** on gross monthly income `Rm`: **`0,15·Rm − 5.500`** (Rm ≤ 80.000$), **`0,21·Rm − 10.300`** (80.000–150.000$), **`0,25·Rm − 16.300`** (> 150.000$); round **down to ten escudos**; **100$ minimum**; no retention below ≈36.667$/mo. **Subsídios férias/Natal/prémio = retenção autónoma** (Art. 6.º). Other categories (Art. 8+): **B 20% (4% REMPE), C 20%, D 20%/10%, E 1%/20%**, non-resident PE 20%/10%, general declaration 25%.
- **Corrections:** supersedes the IUR-2013 scale for periods ≥2015; corrected the 2017 síntese's B=15%/C=10% to the decree's 20%/20%. Clarified that the annual *englobamento* scale (220.000$/16,5/23,1/27,5%) is a distinct final-assessment table, not the monthly retention formula.
- The DNRE folder also exposes the primary **Lei 78/2014 (CIRPS)** and **Lei 82/2015 (CIRPC)** for future ingest. A listed DL 6/2015 *Retificação* link returned an unrelated B.O. page — flagged unverified, artifact discarded.
- Files created:
  - `wiki/sources/2015-01-23 - Decreto-Lei 6-2015 Regime de Retencoes na Fonte IRPS.md`
  - `raw/assets/irps/Decreto-Lei_6_2015_Retencao_na_Fonte.pdf` (preserved primary law)
- Files updated:
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md` (**status → superseded/resolved, confidence high**)
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md` (withholding engine now uses the exact DL 6/2015 formula)
  - `wiki/sources/2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese).md` (B/C rates corrected against primary law)
  - `index.md`, `log.md`
- Residuals (minor, non-blocking): DL 6/2015 retificação check; OE-year re-indexing of 80.000$/150.000$ thresholds; ME value; INPS ceiling; Código Laboral subsidy/overtime formulas; Portaria 42/2015 per-class depreciation rate annex.

## [2026-05-30] ingest | IRPS-era withholding regime confirmed (IUR superseded)

- Tackled the standing legal gap "current IRPS-era withholding portaria vs the IUR scale." Web research → located and pypdf-parsed the **Sistema Fiscal de Cabo Verde** síntese (CVTradeInvest, 2017, 19 pp.; the context-mode fetch only indexed compressed PDF bytes, so direct sandbox extraction was used as with the Cegid/SAF-T PDFs).
- **Key finding:** the IRPS regime (Lei nº 78/VIII/2014) **replaced the IUR scale**. IRPS progressive scale = **isenção ≤ 220.000$; 16,5% ≤ 960.000$; 23,1% ≤ 1.800.000$; 27,5% > 1.800.000$** (annual). Category A monthly retention = **progressive + liberatório from 420.000$/yr (35.000$/mo)**; other categories flat (B 15%, C 10%, D 20%/10%, E 1%/20%). This is a **second independent source** agreeing with the consultancy's 16.5–27.5% band, now with explicit brackets — so the IUR 5-band 11.67–35% scale is superseded, not carried forward.
- Discarded vendus.cv "Tabelas de retenção" again (it is **Portugal IRS**, euros — wrong jurisdiction).
- Files created:
  - `wiki/sources/2017-10-25 - Sistema Fiscal de Cabo Verde (CI Sintese).md`
- Files updated:
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md` (Position D added; best interpretation flipped to IRPS; status needs-review; resolution log appended)
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md` (withholding engine default flipped to the IRPS 3-band scale, IUR config retained effective-period-keyed for pre-2015 recompute)
  - `index.md`, `log.md`
- Open questions (carried):
  - The **Regime de Retenções na Fonte** decree monthly band table (taxa + parcela a abater) — the operative payslip table; provisional approach = annual scale ÷ 12.
  - OE-year currency of the 220.000$/420.000$ thresholds and 16,5/23,1/27,5% rates (sources are 2014–2017).
  - Still standing: Portaria 42/2015 per-class depreciation rate annex; Mínimo de Existência value; INPS ceiling; Código Laboral subsidy/overtime formulas.

## [2026-05-30] maintain | Cegid fiscalidade decks deduplicated

- Closed the twice-carried dedup item. Compared the two `docs/docsfiscal/` decks in the sandbox: `Fiscalidade_ERP_Cegid_Primavera.pdf` vs `SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf`.
- **Proven identical content:** both 103 pages, same full-text md5 (`bb9aef08b8f007c358d762d4f4fb7e6d`), same author (Romane Garcia) and `CreationDate` (2023-06-12 15:31). Only the binary differed (different file md5 + a later `ModDate` on the short-named copy) — a re-export of the same PowerPoint, not a content variant.
- Removed the redundant `SV_Documentação_...pdf` via `git rm` (both were git-tracked, so fully recoverable); kept the cleaner-named `Fiscalidade_ERP_Cegid_Primavera.pdf` as canonical.
- The deck itself remains uningested and **optional** — its content overlaps the already-ingested [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]] (FPG003). Ingest only if an ADR needs deeper fiscal-config detail.
- Files updated:
  - `index.md` (Maintenance Queue dedup item marked resolved), `log.md`
- Files removed:
  - `docs/docsfiscal/SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf` (exact duplicate)
- Outstanding (carried): standing legal gaps — current IRPS-era withholding portaria vs the IUR scale, and the Portaria 42/2015 per-class depreciation rate annex.

## [2026-05-30] lint | Post-SAF-T health-check + stale-citation cleanup

- Ran a vault-wide health-check in the sandbox (87 wiki+root pages). **Healthy baseline:** no duplicate filenames, **no orphan pages**, **100% index coverage** of `wiki/` pages, **0 frontmatter value issues** (type/status/confidence all within allowed sets; only AGENTS/Bem-vindo/CLAUDE lack frontmatter — expected entry points).
- **Broken wikilinks:** 8 found, all benign — 6 are illustrative examples inside CLAUDE.md (`[[Page A]]`, `[[LLM Wiki]]`, etc.); 2 (`[[Entidades ERP]]`, `[[Produtos e Servicos ERP]]`) are stale aspirational mentions in the append-only log (those concepts are covered inside the Document-Core/Inventory ADRs). Left log untouched (append-only).
- **Fixed genuine stale raw-path citations** — module/concept pages pointing at raw decks that now have source pages:
  - `Contabilidade ERP.md` → [[2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference)]]; SAF-T targets marked ingested.
  - `Processamento de Salarios ERP.md` → [[2021 - Cegid Primavera Processamento de Salarios (Legacy Reference)]].
  - `wiki/concepts/Fiscalidade Cabo Verde.md` → replaced raw `Código IVA.pdf` Evidence with [[2026-05-29 - Codigo do IVA Cabo Verde]] + added the Portaria 47/2021 source.
  - `wiki/places/Cabo Verde.md` → frontmatter sources upgraded to source-page wikilinks.
  - `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md` → ERP-functional-reference and fiscal sections refreshed to ingested status; added a SAF-T (CV) cluster section.
- Files updated:
  - `Contabilidade ERP.md`, `Processamento de Salarios ERP.md`, `wiki/concepts/Fiscalidade Cabo Verde.md`, `wiki/places/Cabo Verde.md`, `wiki/maps/Mapa de Fontes - NOVA-ERP e Fiscalidade.md`, `log.md`
- Outstanding (carried):
  - **Dedup** the two Cegid fiscalidade decks (`Fiscalidade_ERP_Cegid_Primavera.pdf` vs `SV_Documentação_Fiscalidade_ERP_Cegid_Primavera.pdf`) — both still uningested duplicates.
  - Standing legal gaps unchanged: Portaria 42/2015 per-class rate annex; current IRPS-era withholding portaria.

## [2026-05-30] maintain | SAF-T (CV) Anexo II — SNCRF account taxonomy extracted

- Parsed Anexo II (pp. 35–67) of the preserved Portaria 47/2021 PDF into structured data: **660 taxonomy codes** (1–660, no gaps) → SNCRF account code(s) + description, across classes 1 Meios financeiros líquidos (10), 2 Contas a receber/pagar (230), 3 Inventários e ativos biológicos (25), 4 Investimentos (95), 5 Capital/reservas (24), 6 Gastos (148), 7 Rendimentos (128).
- Saved `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv` and wrote a concise reference page (no 660-row inline dump, per the small-pages rule). This is the seed for `chart_of_accounts.taxonomy_code`.
- Resolved the Accounting ADR's open "which CV chart standard (PNC)?" question → **SNCRF**, seeded from Anexo II; added `taxonomy_code`/`taxonomy_reference` to the `chart_of_accounts` model. Closed the residual on the SAF-T taxonomy contradiction.
- Files created:
  - `wiki/maps/SAF-T CV Anexo II - SNCRF Account Taxonomy.md`
  - `raw/assets/saft-cv/Anexo_II_SNCRF_taxonomia.csv`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Accounting Ledger and Posting.md`
  - `wiki/syntheses/2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema.md`
  - `wiki/sources/2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV.md`
  - `wiki/contradictions/Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy.md`
  - `index.md`, `log.md`
- Open questions:
  - Which SNCRF chart edition ships as the tenant default; do NRF-PE small-entity variants need a separate seed?
  - Descriptions were de-wrapped heuristically — verify exact wording per account against the PDF before legal display (codes + classes are reliable).

## [2026-05-30] ingest | Portaria 47/2021 SAF-T (CV) primary law — code values + taxonomy resolved

- Located, downloaded and **pypdf-extracted** the official **Portaria nº 47/2021, de 7 de outubro** (Boletim Oficial I Série nº 97; efatura.cv legislation), preserved at `raw/assets/saft-cv/Portaria_47_2021_SAF_T_CV.pdf`. The ctx fetch returned only PDF object bytes, so direct sandbox extraction was used (as with the Cegid decks).
- **Resolved the convention-confirm code values** from Anexo I field definitions (primary): ProductType (P/S/O/E/I), TaxType (IVA/IS/NS/**TEU = Tributo Especial Unificado**), TaxCode IVA (NOR/RED/ISE/ESP/NS), PSProductType 4.3.1.2.1.5 (M=Mercadorias, **AB=Ativos biológicos**, MP, PCI=Produtos acabados e intermédios, SP, PC=Produtos e trabalhos em curso), ProductStatus 4.3.1.2.1.6 (A=Ativo, D=Danificado, DS=Descontinuado, O=Obsoleto, Q=Quarentena). Upgraded all rows in [[SAF-T CV Code Lists]] from convention to authoritative.
- **Resolved the accounting-taxonomy contradiction:** Art. 4.º binds account codes to the **taxonomies in Anexo II** (SNCRF Base / NIC); Anexo I = the same `AuditFile` structure as XSD v1.01_01 (consistent, not competing); Art. 5.º in force **1 Jan 2022** (exercises 2022+). Marked the contradiction superseded/resolved.
- **Confirmed legal scope against Boletim Oficial:** obligated = art. 107.º nº1 CIRPC + Category B organized accounting (art. 78.º nº1 CIRPS); **Category B exempt if annual turnover ≤ 5.000.000$**; REMPE may voluntarily adhere.
- Files created:
  - `wiki/sources/2021-10-07 - Portaria 47-2021 Estrutura SAF-T CV.md`
  - `raw/assets/saft-cv/Portaria_47_2021_SAF_T_CV.pdf` (preserved primary law)
- Files updated:
  - `wiki/maps/SAF-T CV Code Lists.md` (all values now authoritative)
  - `wiki/contradictions/Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy.md` (resolved)
  - `wiki/concepts/SAF-T CV.md`
  - `wiki/sources/2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis.md`
  - `index.md`, `log.md`
- Open questions:
  - Extract **Anexo II** account-code taxonomy list (SNCRF Base / NIC) to seed `chart_of_accounts.taxonomy_code`.
  - Confirm the exact inventory-submission-deadline article (secondary sources say 31 January following year).

## [2026-05-30] maintain | SAF-T (CV) code lists decoded into seed reference

- Extracted all 14 enumerated `simpleType` code lists from the saved XSD with their in-schema documentation, into a seed-reference catalog.
- Authoritative (documented in the schema): FileContentType (F/C/I/O), TaxonomyReference (S/N/P/O = SNCRF/NIRF/NRF-PE/Outros), WorkType, WorkStatus, SourceBilling, PaymentType, PaymentStatus, SourcePayment, PaymentMechanism (13 means of payment), WithholdingTaxType (IRPS/IRPC), TransactionType (N/R/A/J).
- Values present but undocumented in the schema (flagged convention-confirm): ProductType (P/S/O/E/I), TaxType (IVA/IS/NS/TEU), PSProductType (M/AB/MP/PCI/SP/PC), ProductStatus (A/D/DS/O/Q).
- Files created:
  - `wiki/maps/SAF-T CV Code Lists.md`
- Files updated:
  - `wiki/syntheses/2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema.md`
  - `wiki/concepts/SAF-T CV.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Resolve the convention-confirm rows (ProductType, TaxType TEU, PSProductType AB, ProductStatus D/DS/Q) against the DNRE manual.

## [2026-05-30] maintain | SAF-T (CV) field map to NOVA-ERP schema

- Parsed the saved official XSD (`raw/assets/saft-cv/saftcv1.01_01.xsd`) element-by-element and produced a field-mapping synthesis tying every MasterFiles/GeneralLedgerEntries/SourceDocuments block to the existing module ADRs.
- Key cross-validations surfaced: account `TaxonomyReference`/`TaxonomyCode` confirm the **SNCRF taxonomy** binding (feeds the accounting-taxonomy contradiction); `Payment.WithholdingTax` **confirms** the withholding-to-State pattern from the Tesouraria deck; `PhysicalStock` is a **valued snapshot** with `LocationID` (validates the inventory `locations` addition and valuation design); GL account opening/closing balances are export-derived (validates projection-based balances).
- Produced a **capture-at-transaction-time checklist** (entities GL control account + structured ISO address; chart taxonomy_code; tax_rates (TaxType,TaxCode); docs SystemEntryDate/SourceBilling/WorkType/TaxPointDate/exemption codes/serials; journal Period/GLPostingDate/DocArchivalNumber/TransactionType; treasury PaymentMechanism/SourcePayment/WithholdingTax; inventory warehouse+location+valued stock) plus header software-certificate + multi-part splitting needs.
- Files created:
  - `wiki/syntheses/2026-05-30 - SAF-T CV Field Map to NOVA-ERP Schema.md`
- Files updated:
  - `wiki/concepts/SAF-T CV.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Decode the remaining SAF-T code-list enumerations (ProductType, TaxType/TaxCode, WorkType, PaymentType/Mechanism, TransactionType, WorkStatus, SourceBilling, WithholdingTaxType) into seed tables.
  - Confirm the SNCRF taxonomy code-list source (Portaria 47/2021).

## [2026-05-30] ingest | SAF-T (CV) official XSD v1.01_01 + legal basis (web research)

- The vault had **no** official SAF-T CV schema (the standing gate). Web research located the authoritative DNRE source; downloaded and **parsed the official XSD directly** in the sandbox, and preserved it at `raw/assets/saft-cv/saftcv1.01_01.xsd`.
- Primary facts (from the XSD itself): namespace `urn:OECD:StandardAuditFile-Tax:CV_1.01_01`, version 1.01_01, author DNRE, ModificationDate 2020-05-29. `AuditFile` = Header / MasterFiles / GeneralLedgerEntries? / SourceDocuments?. **One schema, four content types** via `FileContentType` enum **F/C/I/O** (Faturação/Contabilidade/Inventário/Outros) — "Completo" is **not** official. Header carries `SoftwareCertificateNumber` + `ProductID`/`ProductVersion` (software certification) and `NumberOfParts`/`PartNumber` (multi-part splitting). MasterFiles = GeneralLedgerAccounts/Customer/Supplier/Product/TaxTable; SourceDocuments = WorkingDocuments/Payments/PhysicalStock.
- Legal basis (secondary web, needs Boletim Oficial confirmation): **Portaria 47/2021** (SNCRF-aligned accounting/inventory SAF-T; inventory due 31 Jan); e-Fatura under **DL 79/2020** + Portarias 62/2020, 74/2020, 16/2022 + Despacho 43/2022.
- Opened a contradiction: v1.01_01 (2020) structure is primary/safe, but whether the **Contabilidade** file needs a newer **SNCRF taxonomy/version** under Portaria 47/2021 is unresolved.
- Flipped the SAF-T CV concept page's "official schema not ingested" gate to **ingested**, corrected the export-types section to F/C/I/O, and mapped MasterFiles to the existing chart/entities/items/tax ADRs.
- Files created:
  - `wiki/sources/2026-05-30 - SAF-T CV Official XSD v1.01_01 and Legal Basis.md`
  - `wiki/contradictions/Contradiction - SAF-T CV Schema Version vs Portaria 47-2021 Taxonomy.md`
  - `raw/assets/saft-cv/saftcv1.01_01.xsd` (preserved official schema)
- Files updated:
  - `wiki/concepts/SAF-T CV.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Is v1.01_01 current for the accounting (`C`) file, or did Portaria 47/2021 publish a newer SNCRF taxonomy version?
  - Element-by-element field map of Customer/Supplier/Product/WorkDocument/GeneralLedgerEntries/PhysicalStock → NOVA-ERP columns (available in the saved XSD when implementation starts).
  - DNRE FAQ Q&A (deadlines/penalties/submission channel) — slide PDF is image-based, needs OCR or the HTML FAQ.

## [2026-05-30] ingest | Cegid Gestão de Equipamentos e Ativos (legacy workflow reference)

- Read the 89-page Cegid Primavera "Using — Gestão de Equipamentos e Ativos" deck (FPG006, 2020) via bounded sandbox PDF extraction and captured the full fixed-asset lifecycle.
- Translated to a NOVA-ERP adopt/adapt/reject rationale and **resolved three Fixed Assets ADR open questions**: (1) tax vs accounting depreciation are tracked as **separate plan-scoped schedules** — Cegid runs a Plano Contabilístico and a Plano Fiscal in parallel; (2) depreciation periodicity is **configurable** (anual/duodecimal/diária); (3) cost-center/function allocation is **optional via Repartições** mapped to analytical dimensions.
- Folded new structure into the ADR: `asset_depreciation_plans` (plan_kind fiscal/accounting/ias) as parent of policies/schedules/runs/lines; `periodicity` + `rate_mode` (máxima/mínima/variável/zero) on policies; `accepted_amount`/`lost_amount` (taxa perdida, aceite fiscal) on lines; `asset_extraordinary_depreciations`; richer `asset_revaluations.kind` (market-value/replacement-cost revaluation, impairment loss/reversal with cap); excess-amortization-correction-on-disposal posting rule; optional insurance policies. Confirmed straight-line/declining-balance ×1.5/×2/×2.5 against [[2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes]].
- Upgraded the Gestão de Ativos module page's raw-path citation to the new source page; marked the ingestion target done. This closes the Cegid "Using" module-workflow validation pass.
- Files created:
  - `wiki/sources/2020 - Cegid Primavera Gestao de Equipamentos e Ativos (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md`
  - `Gestao de Ativos ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - How many depreciation plans ship in MVP — just `fiscal`, or `accounting` + `fiscal`?
  - Are impairment and free/extraordinary revaluation (IAS) in MVP scope or deferred?
  - Is the criteria-inheritance hierarchy (class/fiscal-classification cascade) worth building vs per-asset policy?

## [2026-05-30] ingest | Cegid Gestão de Inventário (legacy workflow reference)

- Read the 64-page Cegid Primavera "Using — Gestão de Inventário" deck (LPG003, 2022) via bounded sandbox PDF extraction and captured the stock-movement / valuation / lot-serial / counting workflow.
- Translated to a NOVA-ERP adopt/adapt/reject rationale: **adopt/validate** the derived-from-movements ledger (stock at any date, no stored quantity), **PCM weighted-average** valuation with cost-adjustment movement types, the reservation/previsional split and physical-count→adjustment reconciliation — all corroborating the Inventory ADR; **new inputs** folded in: `transfer_in_transit` (PTS→TST→RST in-transit state), `cost_adjustment`/`composition`/`decomposition` movement types, warehouse `locations`, the available/reserved/in-transit/blocked state framing, BOM/kits, and an inventory period lock (Fechos de Inventário); **reject** PT "Comunicação de Inventário à AT" as authority — CV uses SAF-T CV Inventário.
- Upgraded the Inventário module page's raw-path citation to the new source page and marked the ingestion target done.
- Files created:
  - `wiki/sources/2022 - Cegid Primavera Gestao de Inventario (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Inventory Movements and Valuation.md`
  - `Inventario ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Stored per-unit/per-layer stock state vs derived from reservations + in-transit movements?
  - BOM / composed articles / kits in MVP or deferred?
  - Inter-warehouse transfer costing across the in-transit leg?
  - Inventory period lock (quantity-only vs quantity+costing) aligned with accounting locks?

## [2026-05-30] ingest | Cegid Tesouraria (legacy workflow reference)

- Read the 123-page Cegid Primavera "Using — Tesouraria" deck (FPG001, 2023) via bounded sandbox PDF extraction and captured the contas-correntes + caixa/bancos workflow.
- Translated to a NOVA-ERP adopt/adapt/reject rationale: **adopt/validate** the obligation (*pendente*) / movement / allocation split, derived payment status (no stored `paid` flag), reversal via anulação/estorno and manual+automatic bank reconciliation — all corroborating the Treasury ADR; **new inputs** folded in: `treasury_items` rubric dimension (*Itens de Tesouraria*, budget-vs-actual), `cash_sessions` caixa lifecycle (open/close diário, operator, balance gate), the allocation operation taxonomy (total/parcial/encontro de valores/valores em excesso/liq. c/ novo pendente + contra-settlement of entidades associadas), credit-limit guard, withholding-to-State pattern, payable approval (`AGP→APR`) and doubtful-debtor transfer; **reject** PT electronic bank-export formats and cheque/letra-centric workflows as authority pending CV verification.
- Upgraded the Tesouraria module page's raw-path citation to the new source page and marked the ingestion target done.
- Files created:
  - `wiki/sources/2023 - Cegid Primavera Tesouraria (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Treasury Receivables Payables and Settlement.md`
  - `Tesouraria ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Should *Itens de Tesouraria* reuse the generic analytical-dimension layer or a treasury-local catalog?
  - Is a full cash-session (caixa) model needed for MVP, or bank/DO accounts first?
  - How is withholding-to-State modeled — treasury obligation, accounting tax map, or both?
  - Are letras / pre-dated cheques / payment plans in CV scope or deferred?

## [2026-05-30] ingest | Cegid Compras e Vendas (legacy workflow reference)

- Read the 73-page Cegid Primavera "Using — O Processo de Gestão de Compras e Vendas" deck (LPG015, 2022) via bounded sandbox PDF extraction (structure + body, not dumped into context) and captured the legacy commercial circuit.
- Translated to a NOVA-ERP adopt/adapt/reject rationale: **adopt/validate** unified entities, the commercial-vs-fiscal split (its *séries emissíveis vs não emissíveis*), the `document_links` graph (its five reproduction mechanisms — duplicação/conversão/transformação/cópia de linhas — over one quantity-traceable graph) and the no-deletion / two-correction-paths model (anulação vs estorno/crédito with mandatory origin reference); **adapt** the anulação guard list into void preconditions reconciled with the e-Fatura FDC event; **reject** all PT fiscal obligations (SAF-T PT, AT Web Service, Working Documents/Portaria 302/2016) as authority — CV uses DNRE e-Fatura + SAF-T CV.
- Folded new inputs into the Document Core ADR: `entities` gains commercial-vs-fiscal name split, NIF-immutability-after-issuance, and an `is_generic` occasional-party sentinel; sharpened the partial-quantity, returns, occasional-party and anulation-guard open questions with legacy evidence.
- Upgraded the Compras e Vendas module page's raw-path citation to the new source page and marked the ingestion target done.
- Files created:
  - `wiki/sources/2022 - Cegid Primavera Compras e Vendas (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Commercial and Fiscal Document Core.md`
  - `Compras e Vendas ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Occasional/indiferenciados parties: `is_generic` sentinel entity vs inline name+NIF on a null-entity document?
  - Fulfilled/satisfied quantity on `*_document_lines`, on `document_links` edges, or a fulfilment table?
  - Which reproduction behaviors are MVP (likely transformação + conversão) vs later (cópia de linhas across modules)?

## [2026-05-29] ingest | Cegid Contabilidade e Fiscalidade (legacy workflow reference)

- Read the 101-page Cegid Primavera "Contabilidade e Fiscalidade" manual via bounded sandbox extraction and captured the legacy accounting/fiscal workflow.
- Translated it into a NOVA-ERP adopt/adapt/reject rationale: adopt the chart hierarchy (movement-only posting), integration-driven postings, periodic IVA apuramento, period open/close + year-end result apportionment, and SAF-T (SVAT) audit; adapt stored "Acumulados"/"Reconstrução de Acumulados" → projection-based computed balances (validating the ADR choice); reject editable postings and file-import as the primary path.
- Linked to the Accounting Ledger ADR (source basis) and upgraded the Contabilidade module page citations to the new source page + the IVA code.
- Files created:
  - `wiki/sources/2022 - Cegid Primavera Contabilidade e Fiscalidade (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-28 - Schema Decision - Accounting Ledger and Posting.md`
  - `Contabilidade ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which CV PNC version seeds the default chart and its digit structure?
  - Which Mapas Legais/Fiscais (Balanço, DR, IVA apuramento, SAF-T) are statutorily required and in what cadence/format?
  - Year-end Apuramento de Resultados posting rules.

## [2026-05-29] ingest | Cegid Processamento de Salários (legacy workflow reference)

- Read the 118-page Cegid Primavera payroll training manual via bounded sandbox extraction (TOC/structure, not dumped into context) and captured the legacy workflow.
- Translated it into a NOVA-ERP adopt/adapt/reject rationale per the module-design contract: adopt the employee master-data decomposition, batch+individual processing, monthly-variable set, autonomous subsidy runs and retroativos/anulação; adapt anulação→superseding/reversing runs and INPS/IRPS→rule-versioned config; reject UI-editable processed values and legacy fiscal maps as authority.
- Linked it to the Payroll ADR (source basis) and upgraded the Payroll module page's raw-path citations to the new source page + the CV legal sources.
- Files created:
  - `wiki/sources/2021 - Cegid Primavera Processamento de Salarios (Legacy Reference).md`
- Files updated:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md`
  - `Processamento de Salarios ERP.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Which statutory mapas de análise / obrigações fiscais (INPS FOS, IRPS maps) must NOVA-ERP produce?
  - Subsídio de turno/alimentação: statutory vs discretionary and their tax/INPS treatment?
  - Annual rollover (abertura de ano): what payroll state carries over?

## [2026-05-29] ingest | Código do IVA Cabo Verde (primary law)

- Read the 48-page `docs/docsfiscal/Código IVA.pdf` via bounded sandbox text extraction (not dumped into context) and captured its structure and durable rules.
- Key facts: standard rate **15%** (art. 17º); **monthly** periodic self-assessed declaration (art. 37º/23º); deduction with exclusions (art. 20º) and pro-rata partial deduction (art. 22º); invoice issuance obligation (art. 32º) and tax-inclusive retail pricing (art. 35º); three regimes — **normal**, **isenção** (no deduction), and **simplificado** (tax = 5% × sales/services), with volume-de-negócios thresholds set by ministerial despacho (not hard-coded).
- Implementation impact: tenant IVA regime + rates modeled as versioned config; feeds the accounting `tax_maps` (IVA↔account↔SAF-T), the document-core IVA fields, e-Fatura payloads and a monthly fiscal cadence.
- Replaced the raw `docs/docsfiscal/Código IVA.pdf` citation in [[Fiscalidade Cabo Verde]] with the new source page.
- Files created:
  - `wiki/sources/2026-05-29 - Codigo do IVA Cabo Verde.md`
- Files updated:
  - `wiki/concepts/Fiscalidade Cabo Verde.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Current consolidated IVA code identity (law nº) and any OE amendments to the 15%/5% rates and exempt categories?
  - Current volume-de-negócios thresholds (by despacho) for the isenção/simplificado regimes?

## [2026-05-29] ingest | IUR 2009 table + Portaria 42/2015 depreciation (primary law)

- The founder supplied two more official Boletim Oficial PDFs (`Tabela de Retenção IUR - 2009.pdf`, `Portaria nº 42 - 2015 -Depreciações e Amortização.pdf`), both machine-readable; read directly and ingested.
- IUR 2009: captured Anexo I monthly table (0% to 22.288$ … 26%), Anexo II practical income table (same 11.67/15.56/21.39/27.22/35% rates with 2009 brackets/parcelas), and the 10% own-account/independent withholding (art. 8º). Confirms the IUR marginal scale is stable across 2009→2013 with only brackets/parcelas re-indexed — strong support for the rule-versioned, effective-dated payroll design.
- Portaria 42/2015: captured all 20 articles — straight-line default, declining-balance coefficients ×1.5/×2/×2.5 with eligibility filter and 2015 cutoff, low-value ≤20.000$ single-period, vehicle/boat/aircraft cost cap 4.000.000$, minimum quota = half, multi-shift +25%/+50%, real-estate construction-only + 25% land split, non-deductible IVA capitalized, intangibles vs non-amortizable goodwill, financial-leasing lessee depreciation.
- **Correction:** primary text art. 19º **revokes Portaria 2/84** and art. 20º applies from 2015 tax periods — superseding the earlier secondary claim that pre-2015 assets keep Portaria 2/84. Fixed in the secondary depreciation source and the Fixed Assets ADR.
- Folded precise rules into the Fixed Assets ADR data model; corroborated the IRPS-brackets contradiction with the 2009 source.
- Files created:
  - `wiki/sources/2008-12-29 - Tabela de Retencao IUR 2009.md`
  - `wiki/sources/2015-08-24 - Portaria 42-2015 Depreciacoes e Amortizacoes.md`
- Files updated:
  - `wiki/syntheses/2026-05-29 - Schema Decision - Fixed Assets and Depreciation.md`
  - `wiki/sources/2026-05-29 - Cabo Verde Depreciation and Amortization Sources.md`
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Per-asset-class depreciation rate annex (not in the supplied PDF) — still needed to seed rates.
  - Current IRPS-era withholding portaria vs the IUR scale; Mínimo de Existência; INPS ceiling; Código Laboral subsidy/overtime.

## [2026-05-29] ingest | Portaria 5/2013 — primary IUR withholding regulation

- The founder supplied the official `docs/docsfiscal/Portaria nº5 -2013 - Retenção IUR trabalho dependente.pdf` (Boletim Oficial, I Série, 10 Jan 2013); read it directly (machine-readable) and extracted the full withholding model.
- Captured the exact monthly withholding formula (with income-splitting for single-titular couples), the 5-bracket marginal scale **11.67% / 15.56% / 21.39% / 27.22% / 35%** with parcelas a abater (0 / 15.904$ / 66.051$ / 166.347$ / 367.109$), the `α` family-charges table (5%–10%), `EF = 640.000$`, the 35% monthly cap, autonomous holiday/Christmas subsidy withholding, the 100$ no-withhold floor, and the full Anexo I monthly table (0% up to 30.701$ … 26% above 399.567$).
- Resolved [[Contradiction - IRPS Category A Withholding Brackets]] for the **IUR era** with primary law (Positions A/B were inaccurate); flagged the open question of whether the IRPS regime (Lei 78/VIII/2014) superseded these rates. Marked IUR→IRPS currency caution throughout.
- Folded the formula/scale into the Payroll ADR statutory-parameters section as rule-versioned config keyed to Portaria 5/2013.
- Files created:
  - `wiki/sources/2013-01-10 - Portaria 5-2013 Retencao IUR Trabalho Dependente.md`
- Files updated:
  - `wiki/contradictions/Contradiction - IRPS Category A Withholding Brackets.md`
  - `wiki/syntheses/2026-05-29 - Schema Decision - Payroll Runs and Payslips.md`
  - `wiki/sources/2026-05-29 - Cabo Verde Payroll and Personal Income Tax Sources.md`
  - `index.md`
  - `log.md`
- Open questions:
  - Did an IRPS-era portaria (post-2014) replace the Portaria 5/2013 IUR scale, and what are the current rates/α/PA/threshold?
  - Mínimo de Existência (ME) value and any OE updates to EF/brackets?
  - Still pending: INPS ceiling, Código Laboral subsidy/overtime formulas, Portaria 42/2015 depreciation rate annex.

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
