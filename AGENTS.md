# Agent Instructions: Bridle Packs

## Project

- Public reference Script Pack repository for Bridle.
- Packs are builder-side artefacts; end users do not clone this repository or run pack tooling directly.
- Primary pack for v0.3: `packs/academic-pdf-to-mkd`.

## First Move

- Check `git status --short`.
- Read `README.md`, `CONTEXT.md`, and the target pack's `PACK.md` before editing.

## Commands

- `bun run validate` — validate every pack through a local Bridle checkout.
- `bun run test` — run repository tests.
- `bun run evidence:docling -- --input /path/to/paper.pdf --dry-run` — verify the Docling evidence plan without downloading models.

If this repository is not cloned beside `../bridle`, set `BRIDLE_ROOT=/path/to/bridle` for validation and evidence commands.

## Constraints

- Do not commit secrets, virtual environments, compiled binaries, Homebrew/system assets, or downloaded model weights.
- Keep copyleft and system dependencies declared, not bundled, unless a licence review explicitly approves bundling.
- Managed assets must include source, size, checksum, and consent text.
- MinerU assets are declared for future math-heavy extraction; do not download them for the v0.3 Docling evidence path.
- Live model downloads require explicit consent and must honour `HF_HOME`.
