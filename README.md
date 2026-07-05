# Bridle Script Packs

Reference Script Packs for Bridle Host Apps.

Packs are builder-side artefacts. A Host App copies a reviewed pack into its app bundle at build time, pins the pack by version and content hash, and grants scoped Manifest capabilities to specific pack entries. End users do not clone this repository, install pack dependencies, or see pack folders directly.

## Packs

- `packs/academic-pdf-to-mkd` — academic PDF to structured Markdown, derived from `~/gitrepos/05_skills/academic-pdf-to-mkd`.
- `packs/tableweaver` — offline rich TableModel capture, validation, export, and transform tools for structurally complex tables.

## Validate

From this repository:

```bash
bun install
bun run validate
```

The validator uses a local Bridle checkout and checks every `packs/*/PACK.md`. If this repository is not cloned beside `../bridle`, set `BRIDLE_ROOT`:

```bash
BRIDLE_ROOT=/path/to/bridle bun run validate
```

## Docling Evidence Run

Dry-run the academic PDF pack without downloading models:

```bash
bun run evidence:docling -- --input /path/to/paper.pdf --dry-run
```

The live evidence run is intentionally explicit because it downloads Docling model assets into `HF_HOME`:

```bash
HF_HOME=~/local-models bun run evidence:docling -- --input /path/to/paper.pdf --allow-download
```

The output tree is written under `packs/academic-pdf-to-mkd/golden/<paper-id>/`.

## Licence

Pack metadata and wrapper code in this repository are MIT licensed unless a pack says otherwise. Third-party engines keep their own licences. Encumbered dependencies and large model weights are declared as probes or managed assets; they are not committed to pack folders.
