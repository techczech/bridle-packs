---
type: "tableweaver.tablemodel"
title: "Simple Archive Metrics"
id: "tbl_simple_archive_metrics"
provenance: {"capture_method": "manual-golden", "captured_at": "2026-07-05T00:00:00Z", "source": "golden/registry/simple-archive-metrics.json"}
schema_fingerprint: "677bea50c888dfb00ab5efb32fd8e863f53da4f1e18b2a0d5074be67dbb41a00"
tags: ["archive", "golden", "simple"]
column_leaf_paths: ["Metrics / Count", "Status"]
column_leaf_path_vectors: [["Metrics", "Count"], ["Status"]]
column_types: [{"name": "Metrics / Count", "path": ["Metrics", "Count"], "type": "integer"}, {"name": "Status", "path": ["Status"], "type": "string"}]
---
{
  "columns": [],
  "id": "tbl_simple_archive_metrics",
  "kind": "tablemodel",
  "model_version": "1.0",
  "provenance": {
    "capture_method": "manual-golden",
    "captured_at": "2026-07-05T00:00:00Z",
    "source": "golden/registry/simple-archive-metrics.json"
  },
  "row_header_columns": [
    {
      "index": 0,
      "path": [
        "Archive labels"
      ]
    }
  ],
  "rows": [
    {
      "cells": [
        {
          "data_type": "integer",
          "kind": "scalar",
          "value": 7
        },
        {
          "data_type": "string",
          "kind": "scalar",
          "value": "catalogued"
        }
      ],
      "index": 0,
      "labels": [
        {
          "data_type": "string",
          "kind": "scalar",
          "value": "Collection B"
        }
      ]
    },
    {
      "cells": [
        {
          "data_type": "integer",
          "kind": "scalar",
          "value": 5
        },
        {
          "data_type": "string",
          "kind": "scalar",
          "value": "needs review"
        }
      ],
      "index": 1,
      "labels": [
        {
          "data_type": "string",
          "kind": "scalar",
          "value": "Collection C"
        }
      ]
    }
  ],
  "schema_fingerprint": {
    "leaf_column_paths": [
      [
        "Metrics",
        "Count"
      ],
      [
        "Status"
      ]
    ],
    "types": [
      "integer",
      "string"
    ],
    "value": "677bea50c888dfb00ab5efb32fd8e863f53da4f1e18b2a0d5074be67dbb41a00"
  },
  "spans": [],
  "title": "Simple Archive Metrics"
}
