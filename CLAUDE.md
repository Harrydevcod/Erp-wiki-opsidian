# NOVA-ERP Cabo Verde Wiki Operating Schema

This file is the primary operating contract for this vault. Any LLM agent working here must treat the vault as the persistent product, domain and engineering memory for [[NOVA-ERP]]: raw sources are immutable evidence, and the wiki is the maintained knowledge layer used to design, build and audit an ERP SaaS for Cabo Verde.

## Mission

Maintain a compounding knowledge base for the NOVA-ERP project.

The agent does not merely answer from raw documents. The agent reads product specs, fiscal documents, ERP references and implementation notes; extracts durable knowledge; updates interlinked markdown pages; records contradictions; maintains indexes; and files valuable decisions back into the wiki.

The human is the founder/CTO and sets product direction, architectural judgment and quality bar. The agent maintains the knowledge system, writes synthesis, preserves evidence and turns scattered material into operational clarity.

## Project Identity

The vault is dedicated to [[NOVA-ERP]], a modern multi-tenant ERP SaaS for Cabo Verde with native fiscal compliance, electronic invoicing, SAF-T CV readiness, accounting, treasury, inventory, HR/payroll, assets, subscriptions, dashboards and future AI assistance.

The wiki must help answer practical build questions:

- What should NOVA-ERP do?
- Why should it do it that way?
- Which Cabo Verde fiscal or operational evidence supports the decision?
- Which legacy ERP behavior is useful reference, and which should not be copied?
- What is uncertain, outdated, legally sensitive or implementation-blocking?

## Domain Priority

When maintaining or querying this vault, prioritize knowledge in this order:

1. Product direction for [[NOVA-ERP]].
2. Cabo Verde fiscal compliance: [[Fiscalidade Cabo Verde]], [[e-Fatura Cabo Verde]], [[SAF-T CV]], DNRE, invoice rules and IVA.
3. Core ERP operating modules: sales, purchases, inventory, treasury, accounting, HR/payroll and assets.
4. SaaS platform architecture: tenancy, auth, permissions, auditability, billing/subscriptions and deployment.
5. UX and workflow quality that lets NOVA-ERP surpass legacy ERP systems.
6. Future extensions: AI assistant, analytics, multi-country expansion and integrations.

## Non-negotiable Principles

1. Raw sources are the source of truth.
2. The wiki is LLM-maintained, but every durable claim must be traceable to a source or clearly marked as inference.
3. Never silently overwrite uncertainty. Preserve disagreement, contradiction, and weak evidence.
4. Every useful interaction should improve the wiki unless the human explicitly asks for chat-only exploration.
5. Cross-links are infrastructure. Add them whenever a page references a meaningful entity, concept, person, place, project, question, or source.
6. Prefer small, focused pages over giant undifferentiated notes.
7. Prefer durable synthesis over transient summaries.
8. Keep the system operable with plain files, Obsidian, shell search, and git. Add tools only when the wiki outgrows the simple workflow.
9. Maintain the highest standard: clear structure, strong reasoning, explicit uncertainty, and no lazy bookkeeping.
10. Never treat a legacy ERP training flow as target architecture without first translating it into a NOVA-ERP design rationale.
11. Never treat old fiscal material as current law without marking the need for verification against current Cabo Verde authority.
12. Security, auditability, tenant isolation and fiscal correctness are design constraints, not later cleanup tasks.

## Directory Contract

```text
raw/
  inbox/          New sources waiting for ingestion.
  archive/        Sources already ingested. Originals remain unchanged.
  assets/         Local images, PDFs, screenshots, audio, video, attachments.

wiki/
  sources/        One page per ingested source.
  entities/       Organizations, products, systems, institutions, objects.
  concepts/       Abstract ideas, principles, patterns, mechanisms.
  syntheses/      Higher-level analyses that combine multiple sources.
  questions/      Valuable answers filed back into the wiki.
  projects/       Active initiatives, decisions, plans, outcomes.
  people/         People profiles when useful.
  places/         Locations when useful.
  maps/           Navigation pages, taxonomies, relationship maps.
  contradictions/ Claims in tension, superseded beliefs, disputed evidence.

templates/        Page templates.
tools/            Optional helper scripts.
docs/             Meta documentation about this wiki system.

index.md          Content-oriented catalog. Read first.
log.md            Chronological append-only activity record.
CLAUDE.md         Primary schema and operating contract.
AGENTS.md         Codex bridge back to this contract.
```

## NOVA-ERP Knowledge Architecture

Use this domain taxonomy when creating or updating pages:

- `wiki/projects/` - product direction, milestones, architecture decisions and implementation plans for NOVA-ERP.
- `wiki/concepts/` - fiscal, technical and ERP domain concepts such as tenancy, e-Fatura, SAF-T CV, payroll processing and inventory valuation.
- `wiki/entities/` - institutions, vendors, systems and authorities such as DNRE, Supabase and Cegid Primavera.
- `wiki/syntheses/` - cross-source decisions, module designs and reconciliations between PRD, SSD, backlog and fiscal references.
- `wiki/questions/` - durable answers to questions asked during product and engineering work.
- `wiki/maps/` - navigation maps, module maps, source maps and knowledge architecture.
- `wiki/contradictions/` - stale legal assumptions, conflicting source claims, unresolved implementation tensions and superseded decisions.

Root-level notes should be entry points only. Durable generated knowledge belongs under `wiki/` unless the root note already exists as an Obsidian navigation page.

## Required Startup Ritual For Every Interaction

At the beginning of every task in this vault:

1. Read `index.md`.
2. Read the latest relevant entries in `log.md`.
3. Classify the user request as one or more of:
   - `ingest`
   - `query`
   - `maintain`
   - `lint`
   - `schema`
   - `tooling`
   - `chat-only`
   - `product-design`
   - `architecture`
   - `compliance`
   - `module-design`
4. Search or inspect relevant files before answering or editing.
5. Decide whether the interaction should update the wiki.
6. If the wiki changes, update `index.md` and append `log.md`.

Only skip this ritual when the user explicitly asks a narrow operational question such as "what folder are you in?".

## Interaction Response Structure

For normal wiki work, the final response should be concise and follow this shape:

```text
Done.

Updated:
- file
- file

Key result:
- durable takeaway

Next:
- recommended next action
```

For pure queries, answer first, then include citations and any pages updated.

For uncertain answers, say what is known, what is inferred, and what remains unresolved.

## File Naming

Use readable Obsidian-friendly names.

- Source pages: `wiki/sources/YYYY-MM-DD - Source Title.md`
- Concept pages: `wiki/concepts/Concept Name.md`
- Entity pages: `wiki/entities/Entity Name.md`
- People pages: `wiki/people/Person Name.md`
- Place pages: `wiki/places/Place Name.md`
- Synthesis pages: `wiki/syntheses/Synthesis Title.md`
- Question pages: `wiki/questions/YYYY-MM-DD - Question Summary.md`
- Contradiction pages: `wiki/contradictions/Contradiction - Short Name.md`
- Map pages: `wiki/maps/Map Name.md`

Use title case for page titles unless the source or proper noun uses different casing.

## Frontmatter Standard

Every maintained wiki page should start with YAML frontmatter.

Minimum fields:

```yaml
---
type:
status:
created:
updated:
tags: []
sources: []
related: []
confidence:
---
```

Allowed `type` values:

- `source`
- `entity`
- `concept`
- `synthesis`
- `question`
- `project`
- `person`
- `place`
- `map`
- `contradiction`
- `index`
- `log`
- `schema`

Allowed `status` values:

- `draft`
- `active`
- `needs-review`
- `superseded`
- `archived`

Allowed `confidence` values:

- `low`
- `medium`
- `high`
- `mixed`
- `unknown`

## Linking Rules

1. Use Obsidian wikilinks: `[[Page Name]]`.
2. Link the first meaningful mention of any important page in a section.
3. Create missing pages when a concept or entity is important enough to recur.
4. Do not create pages for throwaway mentions.
5. Update backlinks manually through related sections when they matter for navigation.
6. Prefer explicit relation labels over vague lists.

Example:

```text
[[Retrieval-Augmented Generation]] is contrasted with [[LLM Wiki]] because...
```

## Evidence And Citation Rules

Durable claims must be attached to evidence.

Use one of these citation forms:

- `Source: [[YYYY-MM-DD - Source Title]]`
- `Evidence: raw/inbox/file-name.md`
- `Inference from: [[Page A]], [[Page B]]`

When a source has not yet been summarized into a source page, cite the raw path and create the source page during ingestion.

Never present an inference as if it were directly stated in a source.

## Evidence Hierarchy For NOVA-ERP

Use the strongest available evidence for each claim:

1. Current Cabo Verde law, DNRE guidance or official technical manuals for compliance-sensitive claims.
2. NOVA-ERP source documents: PRD, SSD, backlog, implementation prompt, database and deployment docs.
3. Cegid Primavera and other ERP training material as workflow/domain reference.
4. Agent synthesis, clearly marked as inference.

If a claim affects taxes, invoices, SAF-T, payroll deductions, legal retention, certification, signatures or regulatory reporting, mark it as requiring current legal verification unless the cited source is current and authoritative.

## Ingest Workflow

When the user asks to ingest a source:

1. Locate the source in `raw/inbox/` unless the user gives a different path.
2. Read the source fully enough to understand structure, claims, evidence, author, date, and context.
3. If the source references images or attachments that matter, inspect them separately when possible.
4. Create a source page in `wiki/sources/`.
5. Extract:
   - summary
   - key claims
   - entities
   - concepts
   - methods or mechanisms
   - data points
   - contradictions or tensions
   - open questions
6. Update existing entity, concept, person, place, project, synthesis, and contradiction pages.
7. Create new pages only when they are likely to matter later.
8. Update `index.md`.
9. Append `log.md`.
10. Move the raw source to `raw/archive/` only if doing so is safe and the source path is stable. If uncertain, leave it in place and mark it ingested in the source page.

### Ingest Discussion Mode

When the source is important or ambiguous, pause after the first read and present:

- top takeaways
- suggested pages to update
- unresolved interpretation choices

Then proceed unless the user redirects.

## Query Workflow

When the user asks a question:

1. Read `index.md`.
2. Search the wiki for relevant pages.
3. Read the most relevant pages.
4. If needed, inspect raw sources behind disputed or important claims.
5. Answer with synthesis, not just excerpts.
6. Cite wiki pages and raw sources.
7. If the answer is durable, create or update a page in `wiki/questions/` or `wiki/syntheses/`.
8. Update `index.md` and `log.md` when a page is filed or changed.

Default assumption: valuable answers should be filed back into the wiki.

## Lint Workflow

When asked to lint or health-check the wiki, inspect for:

- orphan pages
- missing backlinks
- stale claims
- contradictions not tracked in `wiki/contradictions/`
- important concepts without pages
- duplicate pages
- pages without frontmatter
- pages with weak or missing sources
- index entries that are missing, stale, or misleading
- unanswered questions that deserve investigation
- raw sources in `raw/inbox/` that are not ingested

Create a lint report under `wiki/maps/` or `docs/` when the findings are substantial.

## Contradiction Handling

Contradictions are first-class knowledge.

Create a contradiction page when:

- two sources make incompatible claims
- a newer source supersedes an older claim
- the wiki has an internal inconsistency
- a claim is plausible but weakly supported
- the human flags disagreement or uncertainty

Contradiction pages should include:

- the disputed claim
- position A
- position B
- sources for each position
- current best interpretation
- confidence
- what evidence would resolve it

Do not erase old claims. Mark them as superseded or contextual.

## Index Maintenance

`index.md` is the agent's map.

Update it whenever:

- a page is created
- a page is renamed
- a page becomes central to the wiki
- a source is ingested
- a synthesis changes
- a contradiction is opened or resolved

Each index entry should include:

- link
- one-line summary
- optional date, source count, or status

Keep the index scannable. It is not a dumping ground.

## Log Maintenance

`log.md` is append-only. New entries go at the top under the intro.

Entry format:

```markdown
## [YYYY-MM-DD] type | Short title

- What happened.
- Files created:
- Files updated:
- Open questions:
```

Allowed log types:

- `setup`
- `ingest`
- `query`
- `maintain`
- `lint`
- `schema`
- `tooling`

## Source Integrity Rules

1. Do not edit raw sources.
2. Do not delete raw sources unless the human explicitly asks.
3. If a source is moved from `raw/inbox/` to `raw/archive/`, preserve its filename unless there is a clear reason to rename.
4. If converting a source format, keep the original and store the converted version beside it or in `raw/archive/`.
5. If a source cannot be read, log the failure and explain what is needed.

## Search Strategy

Use this order:

1. `index.md`
2. `log.md`
3. filename search
4. full-text search across `wiki/`
5. raw source inspection
6. optional helper tools in `tools/`
7. web search only when the user asks, when the wiki has a gap that requires current information, or when high-stakes accuracy requires verification

Prefer `rg` for search when available.

## Module Design Workflow

When asked about an ERP module such as invoicing, inventory, accounting, treasury, HR/payroll or assets:

1. Read `index.md` and the relevant module/concept pages.
2. Search PRD, SSD and backlog for module intent.
3. Search fiscal/legal docs if compliance is involved.
4. Search Cegid Primavera material for legacy workflow reference.
5. Produce a NOVA-ERP design synthesis instead of copying a legacy flow.
6. Record assumptions, required entities, core workflows, integration points, edge cases, audit needs, open questions and source citations.
7. Update the relevant module page, `index.md` and `log.md`.

## Page Quality Bar

A good page has:

- clear title
- valid frontmatter
- concise summary or definition
- sourced claims
- links to related pages
- explicit uncertainty
- open questions where appropriate
- no generic filler

A bad page:

- copies a source without synthesis
- contains unsourced claims
- hides disagreement
- repeats content already better expressed elsewhere
- has no links
- uses vague tags as a substitute for structure

## Tags

Use tags sparingly. Links and folders are the primary structure.

Recommended starter tags:

- `#source`
- `#concept`
- `#entity`
- `#synthesis`
- `#question`
- `#contradiction`
- `#needs-review`
- `#open-question`

Add domain-specific tags only after repeated patterns emerge.

## Git Expectations

This vault should be safe to version.

Recommended:

- Initialize git if the vault is not already a repository.
- Commit after meaningful ingests, schema changes, and lint passes.
- Use commits as historical checkpoints for the second brain.

Do not run destructive git commands unless the human explicitly asks.

## Tooling Roadmap

Start simple. The index plus full-text search is enough at small scale.

Add tools only when friction appears:

1. `tools/search.ps1` or equivalent full-text helper.
2. Markdown link checker.
3. Frontmatter validator.
4. qmd or another local markdown search tool.
5. MCP integration if the workflow benefits from native tool access.

## Human Collaboration Rules

The human sets direction. The agent maintains structure.

Ask questions only when:

- the source meaning is genuinely ambiguous
- a taxonomy choice would have long-term consequences
- the user requested a collaborative review
- proceeding would risk corrupting the knowledge base

Otherwise, use judgment and continue.

## Current Project State

This vault has been initialized and adapted as the NOVA-ERP Cabo Verde knowledge base on 2026-05-26.

The first source capture exists and identifies the primary corpus:

- NOVA-ERP PRD, SSD, backlog and implementation/deployment notes in `raw/assets/`.
- Cabo Verde fiscal, invoice, e-Fatura, accounting, treasury, inventory, payroll and Cegid Primavera reference material in `docs/docsfiscal/`.

The next best action is to deep-ingest the canonical product and compliance sources, starting with `raw/assets/SSD/PRD.MD`, `raw/assets/SSD/SSD.md` and the e-Fatura technical manual.
