---
type: bridle.script-pack
name: tableweaver
version: 0.1.0
source:
  skill_path: /Users/dominiklukes/gitrepos/06_apps-utilities/03_misc-utilities/bridle-packs/packs/tableweaver
  commit: 11e8d0f6a985b43ad14d16271d295b04eb90eab2
  design_path: packs/tableweaver/DESIGN.md
  phase: 2
scripts:
  - id: validate
    entry: scripts/pack-validate.py
    runtime: uv
    args_schema:
      type: object
      properties:
        table_path:
          type: string
        table:
          type: object
        print_schema:
          type: boolean
        output_path:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: capture-html
    entry: scripts/pack-capture-html.py
    runtime: uv
    args_schema:
      type: object
      properties:
        html:
          type: string
        input_html:
          type: string
        source:
          type: string
        captured_at:
          type: string
        output_json:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: export
    entry: scripts/pack-export.py
    runtime: uv
    args_schema:
      type: object
      required: [format]
      properties:
        table_path:
          type: string
        table:
          type: object
        table_index:
          type: integer
        format:
          enum: [json, markdown, csv, tsv]
        output_path:
          type: string
        loss_report_path:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: transform
    entry: scripts/pack-transform.py
    runtime: uv
    args_schema:
      type: object
      required: [transform]
      properties:
        table_path:
          type: string
        table:
          type: object
        table_index:
          type: integer
        transform:
          type: object
        output_json:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: register
    entry: scripts/pack-register.py
    runtime: uv
    args_schema:
      type: object
      required: [registry_dir]
      properties:
        registry_dir:
          type: string
        table_path:
          type: string
        table:
          type: object
        table_index:
          type: integer
        tags:
          type: array
          items:
            type: string
        output_path:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: query
    entry: scripts/pack-query.py
    runtime: uv
    args_schema:
      type: object
      required: [registry_dir]
      properties:
        registry_dir:
          type: string
        filter:
          type: object
        output_path:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
  - id: analyse
    entry: scripts/pack-analyse.py
    runtime: uv
    args_schema:
      type: object
      required: [registry_dir]
      properties:
        registry_dir:
          type: string
        column:
          type: string
        output_path:
          type: string
    tier: 1
    required_probes: []
    required_assets: []
probes: []
dependencies:
  - id: beautifulsoup4
    licence: MIT
    licence_class: permissive
    bundled: true
  - id: lxml
    licence: BSD-3-Clause
    licence_class: permissive
    bundled: true
  - id: jsonschema
    licence: MIT
    licence_class: permissive
    bundled: true
  - id: pytest
    licence: MIT
    licence_class: permissive
    bundled: true
assets: []
---

tableweaver Phase 2 provides offline, deterministic tier-1 scripts for the TableModel contract and Data Registry. The canonical representation is lossless rich JSON: hierarchical headers, multi-column row labels, merged-cell spans, and tagged rich cell values are preserved. Markdown, CSV, and TSV exports are derived views; CSV and TSV always emit an explicit loss report when structure is dropped. The registry stores every TableModel as an OKF-shaped document, keeps machine and human indexes, and supports cross-table query and deterministic corpus analysis.

This pack contains no model provider, no model/API call, no API key, and no runtime network egress. Judgement lives in the host app's agent, outside the pack. App orchestration remains intentionally out of scope.
