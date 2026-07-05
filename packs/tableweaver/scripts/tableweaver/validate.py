from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class TableModelValidationError(ValueError):
    pass


TABLEMODEL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://bridle.local/schema/tableweaver/tablemodel.schema.json",
    "title": "TableModel",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "kind",
        "model_version",
        "id",
        "title",
        "provenance",
        "schema_fingerprint",
        "columns",
        "row_header_columns",
        "rows",
        "spans",
    ],
    "properties": {
        "kind": {"const": "tablemodel"},
        "model_version": {"const": "1.0"},
        "id": {"type": "string", "minLength": 1},
        "title": {"type": "string"},
        "provenance": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source", "capture_method", "captured_at"],
            "properties": {
                "source": {"type": "string"},
                "capture_method": {"type": "string"},
                "captured_at": {"type": "string"},
            },
        },
        "schema_fingerprint": {
            "type": "object",
            "additionalProperties": False,
            "required": ["leaf_column_paths", "types", "value"],
            "properties": {
                "leaf_column_paths": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string", "minLength": 1}},
                },
                "types": {"type": "array", "items": {"type": "string"}},
                "value": {"type": "string"},
            },
        },
        "columns": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["level", "cells"],
                "additionalProperties": False,
                "properties": {
                    "level": {"type": "integer", "minimum": 0},
                    "cells": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/header_cell"},
                    },
                },
            },
        },
        "row_header_columns": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["index", "path"],
                "additionalProperties": False,
                "properties": {
                    "index": {"type": "integer", "minimum": 0},
                    "path": {"type": "array", "items": {"type": "string", "minLength": 1}},
                },
            },
        },
        "rows": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["index", "labels", "cells"],
                "additionalProperties": False,
                "properties": {
                    "index": {"type": "integer", "minimum": 0},
                    "labels": {"type": "array", "items": {"$ref": "#/$defs/cell_value"}},
                    "cells": {
                        "type": "array",
                        "items": {"oneOf": [{"$ref": "#/$defs/cell_value"}, {"type": "null"}]},
                    },
                },
            },
        },
        "spans": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "section", "row_start", "col_start", "rowspan", "colspan", "text"],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "section": {"enum": ["header", "body", "row_header"]},
                    "row_start": {"type": "integer", "minimum": 0},
                    "col_start": {"type": "integer", "minimum": 0},
                    "rowspan": {"type": "integer", "minimum": 1},
                    "colspan": {"type": "integer", "minimum": 1},
                    "text": {"type": "string"},
                },
            },
        },
    },
    "$defs": {
        "header_cell": {
            "type": "object",
            "required": ["id", "text", "row", "col_start", "rowspan", "colspan", "scope"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string"},
                "text": {"type": "string"},
                "row": {"type": "integer", "minimum": 0},
                "col_start": {"type": "integer", "minimum": 0},
                "rowspan": {"type": "integer", "minimum": 1},
                "colspan": {"type": "integer", "minimum": 1},
                "scope": {"enum": ["column", "column_group", "row_header"]},
                "path": {"type": "array", "items": {"type": "string"}},
            },
        },
        "cell_value": {
            "oneOf": [
                {
                    "type": "object",
                    "required": ["kind", "value", "data_type"],
                    "additionalProperties": False,
                    "properties": {
                        "kind": {"const": "scalar"},
                        "value": {"type": ["string", "number", "integer", "boolean"]},
                        "data_type": {"enum": ["string", "integer", "number", "boolean", "empty"]},
                    },
                },
                {
                    "type": "object",
                    "required": ["kind", "ordered", "items"],
                    "additionalProperties": False,
                    "properties": {
                        "kind": {"const": "list"},
                        "ordered": {"type": "boolean"},
                        "items": {"type": "array", "items": {"$ref": "#/$defs/cell_value"}},
                    },
                },
                {
                    "type": "object",
                    "required": ["kind", "blocks"],
                    "additionalProperties": False,
                    "properties": {
                        "kind": {"const": "rich_text"},
                        "blocks": {"type": "array", "items": {"type": "object"}},
                    },
                },
                {
                    "type": "object",
                    "required": ["kind", "table"],
                    "additionalProperties": False,
                    "properties": {
                        "kind": {"const": "table"},
                        "table": {"$ref": "#"},
                    },
                },
            ]
        },
    },
}


_VALIDATOR = Draft202012Validator(TABLEMODEL_SCHEMA)


def validate_table_model(table: dict[str, Any]) -> None:
    errors = sorted(_VALIDATOR.iter_errors(table), key=lambda error: list(error.path))
    if errors:
        message = "; ".join(f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}" for error in errors)
        raise TableModelValidationError(message)

    leaf_count = len(table["schema_fingerprint"]["leaf_column_paths"])
    if len(table["schema_fingerprint"]["types"]) != leaf_count:
        raise TableModelValidationError("schema_fingerprint.types must align with leaf_column_paths")
    for row in table["rows"]:
        if len(row["cells"]) != leaf_count:
            raise TableModelValidationError(f"row {row['index']} has {len(row['cells'])} cells, expected {leaf_count}")
        if len(row["labels"]) != len(table["row_header_columns"]):
            raise TableModelValidationError(f"row {row['index']} label count does not match row_header_columns")


def load_json(path_or_json: str | Path) -> Any:
    text = Path(path_or_json).read_text() if Path(str(path_or_json)).exists() else str(path_or_json)
    return json.loads(text)
