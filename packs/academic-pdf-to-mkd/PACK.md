---
type: bridle.script-pack
name: academic-pdf-to-mkd
version: 0.3.0
source:
  skill_path: /Users/dominiklukes/gitrepos/05_skills/academic-pdf-to-mkd
  commit: c6a29ddf8cac074b2743b7140177c23bd14feae6
scripts:
  - id: extract-docling
    entry: scripts/pack-docling.py
    runtime: uv
    args_schema:
      type: object
      required: [input_pdf, output_dir]
      properties:
        input_pdf:
          type: string
        output_dir:
          type: string
        paper_id:
          type: string
    tier: 1
    required_probes: []
    required_assets: [docling-models]
  - id: detect-engine
    entry: scripts/pack-detect-engine.py
    runtime: uv
    args_schema:
      type: object
      required: [input_pdf]
      properties:
        input_pdf:
          type: string
    tier: 1
    required_probes: [poppler-pdftotext, poppler-pdfinfo]
    required_assets: []
probes:
  - id: poppler-pdftotext
    kind: binary
    command: pdftotext
    version: ">=22.0.0"
  - id: poppler-pdfinfo
    kind: binary
    command: pdfinfo
    version: ">=22.0.0"
  - id: poppler-pdftoppm
    kind: binary
    command: pdftoppm
    version: ">=22.0.0"
  - id: ocrmypdf
    kind: binary
    command: ocrmypdf
  - id: ghostscript
    kind: binary
    command: gs
  - id: macos-mps
    kind: platform
    platform: darwin
dependencies:
  - id: docling
    licence: MIT
    licence_class: permissive
    bundled: true
  - id: pillow
    licence: HPND
    licence_class: permissive
    bundled: true
  - id: pypdfium2
    licence: Apache-2.0 OR BSD-3-Clause
    licence_class: permissive
    bundled: true
  - id: pymupdf4llm
    licence: AGPL-3.0
    licence_class: copyleft
    bundled: false
  - id: poppler
    licence: GPL-2.0-or-later
    licence_class: copyleft
    bundled: false
  - id: ocrmypdf
    licence: MPL-2.0
    licence_class: weak-copyleft
    bundled: false
  - id: ghostscript
    licence: AGPL-3.0
    licence_class: copyleft
    bundled: false
  - id: mineru
    licence: Apache-2.0 + commercial thresholds
    licence_class: permissive-with-use-thresholds
    bundled: false
assets:
  - id: docling-models
    description: Docling layout and table-structure models used by the tier-1 docling path.
    size_bytes: 358236338
    source:
      kind: hf
      repo: docling-project/docling-models
    checksum:
      algorithm: sha256
      value: "ba922466453a2dff0a71bf97954fc392ffd3bb1686dbc89b071d2a6c52aefe10"
    consent_text: Download Docling model assets into the configured Hugging Face cache before first conversion.
  - id: mineru-models
    description: MinerU math-heavy extraction model weights; declared for future math engine support and not downloaded by the v0.3 live path.
    size_bytes: 4831838208
    source:
      kind: hf
      repo: opendatalab/PDF-Extract-Kit-1.0
    checksum:
      algorithm: sha256
      value: "0000000000000000000000000000000000000000000000000000000000000000"
    consent_text: Download MinerU model assets for math-heavy PDFs. This is about 4.5 GB and is not part of the v0.3 docling validation path.
---

Academic PDF to Markdown reference pack derived from the local `academic-pdf-to-mkd` skill. The v0.3 runnable path is the tier-1 Docling extractor with a locked uv environment. Poppler, OCRmyPDF, Ghostscript, pymupdf4llm, and MinerU stay declared as probes, dependency facts, or managed assets; they are not bundled as executable system installs.
