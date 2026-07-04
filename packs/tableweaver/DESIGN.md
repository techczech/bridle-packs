# tableweaver — Script Pack design

Status: design (brainstormed 2026-07-05; reframed twice — rich-JSON model, then agent-driven-no-provider + data registry). A Bridle Script Pack that gives a host app's agent the tools to **capture structurally complex tables into a lossless JSON model, reshape them, and record every one in a data registry for global cross-table analysis.** The pack is deterministic tools + a schema + a registry. **The judgement lives in the host app's agent, not in the pack** — there is no model provider inside tableweaver.

Lineage:
- Deterministic HTML capture/conversion draws on Simon Willison's `html-table-extractor` (`simonw/tools`, **Apache-2.0**, verified 2026-07-05 — compatible with pack Apache/MIT per ADR-0010). Reimplement the approach with attribution + Apache-2.0 NOTICE; don't copy verbatim.
- Structural/semantic interpretation draws conceptually on `semantictableweaver`/TabWeaver — but that tool's baked-in Gemini call is **explicitly what we are NOT doing**. The agent replaces the provider.

## The core problem & the shape of the solution (Dominik, 2026-07-05)

Complex tables — merged cells, multiple header rows, multiple row-label columns, cells holding formatted text (bullet lists) or **nested tables** — lose their meaning when flattened to CSV. The canonical form is **lossless rich JSON**. Recovering that structure from real sources (PDF-extracted tables, images, messy pastes) needs judgement.

That judgement is the **host app's agent**, not a provider inside the pack. The user says *"import the tables from this page"* → the agent picks a tool (deterministic `capture-html`, or its own reading for a PDF/image) and produces a TableModel. The user says *"reformat this table"* → the agent applies the pack's tools plus its own judgement, **asking the user for feedback**. And **every table the agent captures or edits is recorded in a data registry** so the whole collection can be analysed globally.

## Key terms

- **TableModel** — the canonical **lossless JSON** table. Preserves: **hierarchical headers** (multi-level column groups + multi-column row labels), **spans** (merged cells as first-class structure), and **rich cell values** as a tagged union — `scalar` · `rich_text` (bullet/numbered lists) · `list` · **`table` (a nested TableModel, recursively)**. Carries registry metadata: stable `id`, provenance (source, capture method, timestamp), and a **schema fingerprint** (ordered leaf-column paths + types) for cross-table matching.
- **Data Registry** — *the most important component.* A persistent, OKF-shaped store of **every** TableModel the agent captures or edits, plus an index that makes the whole collection queryable and analysable **across tables** (by schema, column, provenance, and value). This is what turns one-off captures into a corpus you can reason over globally.
- **Deterministic tool** — a tier-1 script: pure, offline, reproducible. `capture-html`, `export`, `transform`, `validate`, and the registry's `register`/`query`/`analyse`.
- **Agent orchestration** — the host app's Bridle harness agent drives everything: interprets user intent, applies judgement to ambiguous structure, calls the deterministic tools, asks the user for feedback, and writes results to the registry. The pack exposes tools; it never calls a model (Bridle: *tools are code, the model is judgement*).

## Architecture

Three parts, one canonical **TableModel** (JSON). No provider, no model call anywhere in the pack.

### 1. TableModel contract + `validate` (tier-1)
The JSON schema (hierarchical headers, spans, tagged-union cells, registry metadata) and a `validate` tool the agent calls to confirm any TableModel it produces (including ones it reasons out from a PDF/image) is well-formed before registering.

### 2. Deterministic table tools (tier-1, locked env, offline)
- `capture-html` — HTML string / local `.html` → TableModel[]. DOM-faithful: multi-row headers, rowspan/colspan → spans, nested `<table>` → nested TableModel, cell formatting → `rich_text`/`list`. (Ports the html-table-extractor approach, extended to preserve structure.)
- `export` — TableModel → JSON (lossless) / Markdown (middle) / CSV / TSV (lossy, **with an explicit loss report**); JSON → TableModel (round-trip).
- `transform` — transpose, group-by, aggregate, filter, sort, reorder/rename, split a list-cell, promote/demote a header level, flatten/unnest.

### 3. Data Registry (tier-1, the centrepiece)
- `register` — add or update a TableModel in the registry (idempotent by `id`); store as an OKF-shaped document (JSON body + frontmatter: title, provenance, schema fingerprint, tags) in a registry bundle, and update the index + `_INDEX-registry.md`.
- `query` — find tables across the whole registry by schema fingerprint, column name/type, provenance, tags, or cell content.
- `analyse` — global cross-table operations: schema-overlap / find-mergeable tables, column value distributions across tables, corpus stats, candidate reconciliation sets. Deterministic surfacing; the *decision* to merge stays the agent's.

The registry bundle is OKF-shaped so `@bridle/knowledge` reads it; the index may reuse a scout-core-style structured/FTS approach if content search is needed (kept simple first: schema+frontmatter index).

## Orchestration (host app, not the pack)

The host app's agent binds these tools through its Bridle Manifest and orchestrates:
- *"import tables from X"* → `capture-html` (HTML) or agent-reads-then-`validate` (PDF/image) → `register`.
- *"reformat / clean this table"* → `transform` + agent judgement, **ask user for feedback** → `register` (new version).
- *"what do all my tables say about Y"* → `query` / `analyse` over the registry.
No model call is inside tableweaver; the agent supplies judgement and user interaction.

## PACK.md sketch

- Scripts (all tier 1, locked env, offline): `validate`, `capture-html`, `export`, `transform`, `register`, `query`, `analyse`.
- Probes: none. `capture-html --url` fetch is a host capability grant, not bundled.
- Assets: none. No model weights, no provider.
- Golden: a synthetic complex table (merged cells + 2-level header + list-in-cell + nested table) → lossless JSON + Markdown export + CSV export *with loss report*; plus a mini-registry with two tables and a `query`/`analyse` example.

## Relationship to the ecosystem

- Downstream of `academic-pdf-to-mkd`: its extracted tables are prime input the agent captures + registers.
- Registry documents are OKF-shaped → `@bridle/knowledge` reads them; content search may reuse `scout-core`.
- First consumer: ArchiveScout (agent-driven table import/reformat + a registry over a vault). `@bridle/recipes` may later package the orchestration patterns.

## Non-goals

- **No model provider, no model call, no API key, no egress inside the pack.** Judgement is the host agent's.
- No flat-CSV-as-truth (CSV is a lossy export with a reported loss).
- No standalone UI (TabWeaver webapp stays separate).
- Not a general spreadsheet engine.

## Open decisions

1. **Canonical = rich JSON TableModel; CSV lossy** — settled 2026-07-05.
2. **No provider; agent drives, pack provides deterministic tools** — settled 2026-07-05.
3. **A data registry of all tables for global analysis is a first-class component** — settled 2026-07-05.
4. Registry index depth (frontmatter+schema only vs. scout-core-style content FTS) — start simple, revisit when global content-analysis needs it.

## Build phasing

- **Phase 1 (decision-free, unblocked):** TableModel contract + `validate` + `capture-html` + `export` (lossless JSON / lossy CSV-TSV-MD with loss reports) + `transform` + PACK.md + synthetic golden. The foundation the agent and registry both build on.
- **Phase 2 (the centrepiece):** Data Registry — `register` / `query` / `analyse` + the OKF registry bundle + index + a two-table golden. Built right after Phase 1's model exists.
- **Phase 3 (app-level, later):** orchestration recipes/examples showing a Bridle agent wielding these tools (import/reformat/analyse) with user feedback — likely `@bridle/recipes`, in ArchiveScout.
