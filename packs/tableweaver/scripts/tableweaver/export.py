from __future__ import annotations

import csv
import io
import json
from typing import Any

from .model import cell_to_text, path_label
from .validate import validate_table_model


def load_table_model(encoded: str) -> dict[str, Any]:
    data = json.loads(encoded)
    if isinstance(data, list):
        if len(data) != 1:
            raise ValueError("Expected exactly one TableModel in JSON array")
        data = data[0]
    validate_table_model(data)
    return data


def export_json(table: dict[str, Any]) -> str:
    validate_table_model(table)
    return json.dumps(table, indent=2, sort_keys=True) + "\n"


def _headers(table: dict[str, Any]) -> list[str]:
    return [path_label(column["path"]) for column in table["row_header_columns"]] + [
        path_label(path) for path in table["schema_fingerprint"]["leaf_column_paths"]
    ]


def _project_rows(table: dict[str, Any]) -> list[list[str]]:
    rows = []
    for row in table["rows"]:
        rows.append([cell_to_text(label) for label in row["labels"]] + [cell_to_text(cell) for cell in row["cells"]])
    return rows


def export_markdown(table: dict[str, Any]) -> str:
    validate_table_model(table)
    headers = _headers(table)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in _project_rows(table):
        escaped = [cell.replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines) + "\n"


def _loss_report(table: dict[str, Any], format_name: str) -> dict[str, Any]:
    losses = []
    if table["spans"]:
        losses.append({"kind": "span", "detail": "rowspan/colspan structure was projected to a rectangular export"})
    for row in table["rows"]:
        for col_index, cell in enumerate(row["cells"]):
            if cell is None:
                losses.append({"kind": "covered_cell", "row": row["index"], "column": col_index, "detail": "covered span cell exported as empty"})
            elif cell.get("kind") == "list":
                losses.append({"kind": "list_cell", "row": row["index"], "column": col_index, "detail": "list items joined with semicolons"})
            elif cell.get("kind") == "rich_text":
                losses.append({"kind": "rich_text", "row": row["index"], "column": col_index, "detail": "rich text blocks joined as plain text"})
            elif cell.get("kind") == "table":
                losses.append({"kind": "nested_table", "row": row["index"], "column": col_index, "detail": "nested TableModel rendered as plain text summary"})
    return {"format": format_name, "lossless": not losses, "losses": losses}


def _delimited(table: dict[str, Any], delimiter: str, format_name: str) -> tuple[str, dict[str, Any]]:
    validate_table_model(table)
    handle = io.StringIO()
    writer = csv.writer(handle, delimiter=delimiter, lineterminator="\n")
    writer.writerow(_headers(table))
    writer.writerows(_project_rows(table))
    return handle.getvalue(), _loss_report(table, format_name)


def export_csv(table: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return _delimited(table, ",", "csv")


def export_tsv(table: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return _delimited(table, "\t", "tsv")
