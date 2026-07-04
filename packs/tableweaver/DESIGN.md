# tableweaver — Script Pack design

Status: design (brainstormed 2026-07-05). A Bridle Script Pack for extracting and reshaping complex tables. Partly deterministic (tier-1 scripts in locked envs), partly agent-managed (semantic operations via a host-injected model interface). Complements `academic-pdf-to-mkd` (which *produces* tables from PDFs — tableweaver *cleans and reshapes* them).

Lineage:
- Deterministic extraction/conversion draws on Simon Willison's `html-table-extractor` (client-side: DOM → grid with rowspan/colspan flattening, header detection, export to HTML/MD/CSV/TSV/JSON). `simonw/tools` is **Apache-2.0** (verified 2026-07-05) — compatible with the pack's Apache/MIT licensing (ADR-0010). Reimplement the approach in the pack's language with attribution and include the Apache-2.0 NOTICE; don't copy verbatim.
- Semantic operations draw on Dominik's `semantictableweaver`/TabWeaver (Gemini-powered: typed values, list-in-cell arrays, human column labels, summary; deterministic SmartTable ops sort/filter/group/aggregate/transpose).

## Purpose

Turn messy, structurally-complex tables from any source into clean, typed, well-shaped data — and let both deterministic scripts and an app's agent operate on them. The hard problem is **complex tables**: merged cells, multi-row headers, list-in-cell content, inconsistent columns, and reconciling differently-shaped tables into one.

## Key terms

- **Grid** — the canonical intermediate: a 2-D array of cells with a resolved header (rowspans/colspans flattened, no merged cells). Every extractor emits a Grid; every transform consumes/produces a Grid.
- **Table document** — a Grid plus metadata (source, detected header rows, column semantic labels, per-column type). Serialized as Markdown+YAML-frontmatter (OKF-shaped, so `@bridle/knowledge` can read it) with a paired CSV.
- **Deterministic op** — a tier-1 script: pure, no model, reproducible (extract, convert, transpose, group, aggregate, split list-cells on a delimiter).
- **Semantic op** — an agent-managed operation requiring judgement (infer types, decompose prose lists into arrays, assign human column labels, categorise, reconcile columns across tables, summarise). Routed through the host's model interface, never a hardcoded provider.

## Architecture

Two layers over one shared Grid contract.

### Layer 1 — deterministic (tier-1 scripts, locked env)

- `extract` — HTML/URL/Wikipedia → Grid[]. Flatten rowspan/colspan; detect header row count; drop nested tables. (Reimplements the html-table-extractor approach.)
- `convert` — Grid ↔ CSV / TSV / Markdown / JSON, RFC-4180 correct, round-trippable.
- `transform` — deterministic reshapes on a Grid: transpose, group-by, aggregate (sum/avg/count/min/max), filter, sort, reorder/rename columns, split a list-cell on a delimiter, promote/demote header rows.

All deterministic, testable with fixtures, no external services. This is the shippable core and depends on none of the open decisions below except "deterministic-first."

### Layer 2 — agent-managed (semantic ops via host interface)

The pack **declares** a semantic-op contract; the host app **provides** the model call. No provider or key inside the pack (deny-by-default egress; ADR-0003/0011).

```
SemanticOp = (table: TableDocument, op: SemanticRequest) => Promise<TableDocument>
```

Semantic requests (v1 set): `infer_types`, `decompose_list_cells`, `label_columns`, `categorise`, `reconcile` (align/merge columns across N tables), `summarise`. Each is a structured request with a strict output schema the host validates. When `@bridle/cognition` (ADR-0014) ships, it becomes the reference provider of this interface; until then the host wires it directly (ArchiveScout is the first provider). This keeps the pack buildable now and provider-agnostic.

## PACK.md sketch

- Scripts: `extract` (tier 1), `convert` (tier 1), `transform` (tier 1) — Python or TS in a locked env; `semantic` entries declared as host-interface ops (not spawned by the tier-1 runner).
- Probes: none required for the deterministic core (pure libs). A URL-fetch capability for `extract --url` is a host grant, not a bundled tool.
- Assets: none (no model weights — semantic ops use the host model).
- Golden: a complex real table (merged cells + multi-row header) extracted and reshaped, plus a semantic-op golden once Layer 2 lands. Licence-clean source (e.g. a Wikipedia table, CC BY-SA — attribute).

## Relationship to the ecosystem

- Downstream of `academic-pdf-to-mkd`: its `tables/*.csv` feed tableweaver's `transform`/semantic ops for cleaning.
- Consumed by ArchiveScout (triage/convert of vault tables) and any Bridle app; agent-written converters may reference tableweaver scripts (`@bridle/recipes` later).
- Table documents are OKF-shaped → readable by `@bridle/knowledge`.

## Non-goals

- No standalone UI in this pack (the TabWeaver webapp stays separate).
- No hardcoded model provider; no bundled model weights.
- No dependency on `@bridle/recipes`/`@bridle/cognition` for v1 (host provides the model interface).
- Not a general spreadsheet engine — tables in, reshaped tables out.

## Open decisions (chosen 2026-07-05 in Dominik's absence; easy to revisit)

1. **Scope = all three, layered** — extraction (deterministic) → cleaning → reconciliation (agent). 
2. **Semantic engine = host-injected interface** (not a hardcoded provider, not blocking on `@bridle/cognition`).
3. **Shape = pack-only, deterministic-first** — ship Layer 1, then layer Layer 2 via the host interface.

## Build phasing

- **Phase 1 (unblocked now):** Layer 1 deterministic scripts + Grid/TableDocument contract + PACK.md + golden. No open-decision risk.
- **Phase 2 (after Dominik confirms decision 2):** Layer 2 semantic-op contract + host-interface reference wiring + semantic golden.
