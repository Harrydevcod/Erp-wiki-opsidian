# LLM Wiki Operating Schema

This file is the primary operating contract for this vault. Any LLM agent working here must treat the vault as a persistent, compounding second brain: raw sources are immutable evidence, and the wiki is the maintained knowledge layer built from them.

## Mission

Maintain a personal knowledge base where knowledge compounds over time.

The agent does not merely answer from raw documents. The agent reads sources, extracts durable knowledge, updates interlinked markdown pages, records contradictions, maintains indexes, and files valuable answers back into the wiki.

The human curates sources, asks questions, and directs emphasis. The agent does the maintenance work.

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

## Current Initial State

This vault has been initialized as an LLM Wiki on 2026-05-26.

No sources have been ingested yet.

The next best action is to place the first source in `raw/inbox/` and ask:

```text
Ingest the source in raw/inbox/<filename>.
```

