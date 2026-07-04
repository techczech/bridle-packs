# tableweaver — Script Pack design

Status: design (brainstormed 2026-07-05, reframed after Dominik's "complex tables need JSON, not CSV" correction). A Bridle Script Pack for capturing and reshaping **structurally complex tables** whose full meaning survives only in a rich JSON model. Partly deterministic, partly agent-managed. Complements `academic-pdf-to-mkd` (which *produces* tables from PDFs — tableweaver *captures their true structure* and reshapes them).

Lineage:
- Deterministic HTML capture/conversion draws on Simon Willison's `html-table-extractor` (`simonw/tools`, **Apache-2.0**, verified 2026-07-05 — compatible with the pack's Apache/MIT licensing per ADR-0010). Reimplement the approach with attribution + an Apache-2.0 NOTICE; don't copy verbatim.
- Semantic capture/manipulation draws on Dominik's `semantictableweaver`/TabWeaver (Gemini-powered structural interpretation, list-in-cell arrays, typed values, labels).

## The core problem (Dominik, 2026-07-05)

Complex tables — **merged cells, multiple header rows, multiple row-label columns, cells containing formatted text (bullet lists) or even nested tables** — cannot be captured by a flat CSV grid without destroying the structure that carries the meaning. **The canonical representation is rich JSON.** CSV/TSV are lossy *exports*, not the model. And because real sources (PDF-extracted tables, images, messy pastes) rarely expose this structure mechanically, **agent judgement is the critical component** that recovers it.

## Key terms

- **TableModel** — the canonical, **lossless JSON** representation. It preserves:
  - **Hierarchical headers** — column headers over multiple levels (column groups → leaf columns as paths), and one or more leading row-label columns forming a row hierarchy.
  - **Spans** — merged cells kept as first-class structure, never silently flattened.
  - **Rich cell values** — a cell is a tagged union: `scalar` (string/number/bool/null) · `rich_text` (formatted, e.g. bullet/numbered lists) · `list` (array of values) · `table` (a nested **TableModel**, recursively).
  - Provenance + per-column semantic label and type.
- **Capture** — producing a correct TableModel from a source. Deterministic when the source is structured HTML (the DOM carries spans + nested `<table>`s); **agent-managed** when structure is ambiguous or lost (PDF tables, images, pasted/OCR'd text).
- **Export** — serializing a TableModel out. **JSON = lossless** (canonical). **Markdown = middle-fidelity** (lists-in-cells survive; nested tables degrade to indented/linked sub-tables). **CSV/TSV = lossy** (hierarchical headers flattened to dotted paths; rich/nested cells stringified) — the loss is explicit and reported, never silent.
- **Transform** — a reshape on a TableModel (transpose, group-by, aggregate, filter, sort, reorder/rename, split a list-cell, promote/demote a header level, flatten/unnest). Deterministic.

## Architecture

Two layers over one canonical **TableModel** (JSON) contract.

### Layer 1 — deterministic (tier-1 scripts, locked env)

- `capture-html` — HTML string / local `.html` → TableModel[]. Faithfully reads the DOM: multi-row headers, rowspan/colspan → spans, nested `<table>` → nested TableModel, cell inner formatting → `rich_text`/`list`. (Ports the html-table-extractor approach, extended to preserve — not flatten — structure.)
- `export` — TableModel → JSON (lossless) / Markdown (middle) / CSV / TSV (lossy, with a loss report). And parse JSON ← the canonical round-trip.
- `transform` — the reshapes above, operating on the rich model.

Decision-free and fully offline. Establishes the exact JSON model that Layer 2's agent must target.

### Layer 2 — agent-managed (semantic capture, via host model interface)

Where "agent judgement is critical." The pack **declares** a capture/normalise contract; the host app **provides** the model call (no provider/key/egress in the pack; ADR-0003/0011).

```
SemanticOp = (source | TableModel, op) => Promise<TableModel>   // strict output schema, host-validated
```

v1 semantic ops: `capture` (messy source — PDF-table text, image, pasted grid — → correct TableModel: infer header levels, merges, and whether a cell is a nested table vs formatted text vs list); `normalise` (types, list decomposition, clean hierarchical headers, human labels); `reconcile` (align/merge columns across differently-shaped tables); `summarise`. When `@bridle/cognition` (ADR-0014) ships it becomes the reference provider of this interface; until then the host wires it (ArchiveScout first). This keeps the pack buildable now and provider-agnostic.

## PACK.md sketch

- Scripts: `capture-html`, `export`, `transform` (tier 1, locked env); `semantic` entries declared as host-interface ops (not spawned by the tier-1 runner).
- Probes: none for the deterministic core. `--url` fetch for `capture-html` is a host grant, not a bundled tool.
- Assets: none.
- Golden: a synthetic complex table (merged cells + 2-level header + a list-in-cell + a nested table) captured to lossless JSON, plus its Markdown export and a CSV export *with its loss report*; a semantic-capture golden once Layer 2 lands.

## Relationship to the ecosystem

- Downstream of `academic-pdf-to-mkd`: its extracted tables (structurally ambiguous) are the prime input for Layer 2 `capture`/`normalise`.
- Consumed by ArchiveScout and any Bridle app; TableModels are OKF-shaped JSON+frontmatter → readable by `@bridle/knowledge`; agent-written converters may reference tableweaver scripts (`@bridle/recipes` later).

## Non-goals

- No flat-CSV-as-truth: CSV is always a lossy export with a reported loss, never the model.
- No standalone UI in this pack (TabWeaver webapp stays separate).
- No hardcoded model provider, no bundled weights, no `@bridle/cognition`/`@bridle/recipes` dependency for v1.
- Not a general spreadsheet engine.

## Open decisions

1. **Canonical = rich JSON TableModel; CSV/TSV lossy exports** — settled by Dominik 2026-07-05.
2. **Scope = capture (det HTML + agent for ambiguous sources) → normalise → reconcile** — layered.
3. **Semantic engine = host-injected model interface** (recommended; not a hardcoded provider, not blocking on `@bridle/cognition`). ⟵ **still needs Dominik's confirmation; it now gates the *critical* Layer-2 work.**

## Build phasing

- **Phase 1 (decision-free, unblocked):** the TableModel JSON contract + `capture-html` + `export` (lossless JSON / lossy CSV-TSV-MD with loss reports) + `transform` + PACK.md + synthetic golden. Lays the correct rich foundation.
- **Phase 2 (gated on decision 3):** Layer-2 semantic `capture`/`normalise`/`reconcile`/`summarise` via the host interface + a semantic golden. This is the part Dominik flagged as where agent judgement is critical.
