# Bridle Script Packs

Reference Script Packs for Bridle Host Apps.

Packs are builder-side artefacts. A Host App copies a reviewed pack into its app bundle at build time, pins the pack by version and content hash, and grants scoped Manifest capabilities to specific pack entries. End users do not clone this repository, install pack dependencies, or see pack folders directly.

## Packs

- `packs/academic-pdf-to-mkd` — academic PDF to structured Markdown, derived from `~/gitrepos/05_skills/academic-pdf-to-mkd`.

## Validate

From this repository:

```bash
bun install
bun run validate
```

The validator uses `@bridle/packs` and checks every `packs/*/PACK.md`.

## Licence

Pack metadata and wrapper code in this repository are MIT licensed unless a pack says otherwise. Third-party engines keep their own licences. Encumbered dependencies and large model weights are declared as probes or managed assets; they are not committed to pack folders.
